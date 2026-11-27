#!/usr/bin/env python3
"""Build the manuscript into a 6x9 print PDF (WeasyPrint), EPUB 3 and DOCX (pandoc).

Usage:  python3 build.py [pdf|epub|docx|all]
"""
import html, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MS, OUT, BUILD = ROOT / "manuscript", ROOT / "output", ROOT / "build"
for d in (OUT, BUILD):
    d.mkdir(parents=True, exist_ok=True)

from book_meta import BOOK  # noqa: E402

TITLE, SUBTITLE, AUTHOR, FILE = BOOK["title"], BOOK["subtitle"], BOOK["author"], BOOK["file"]
EXT = "markdown+smart+fenced_divs+bracketed_spans+pipe_tables+grid_tables+implicit_figures"
BOXES = {"drill": "Drill", "problem": "Problem", "kata": "Kata", "street": "Street", "fault": "Fault",
         "keypoints": "Key Points", "exercises": "Exercises", "chapter-intro": "Chapter Intro"}
WORDS = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"]


def number_sections(md_text, chapter_no):
    out, sec = [], 0
    for line in md_text.splitlines():
        if chapter_no and line.startswith("## ") and "{.unnumbered}" not in line:
            sec += 1
            line = f"## [{chapter_no}.{sec}]{{.secnum}} {line[3:].strip()}"
        out.append(line)
    return "\n".join(out)


def pandoc_html(md_text):
    r = subprocess.run(["pandoc", "-f", EXT, "-t", "html5", "--wrap=none"],
                       input=md_text, capture_output=True, text=True, check=True)
    return r.stdout


def split_title(md_text):
    lines = md_text.strip("\n").splitlines()
    assert lines[0].startswith("# "), lines[0]
    return lines[0][2:].strip(), "\n".join(lines[1:])


def dropcap(body_html):
    intro_end = body_html.find("</div>") if body_html.lstrip().startswith('<div class="chapter-intro"') else -1
    start = body_html.find("<p>", intro_end + 1 if intro_end >= 0 else 0)
    if start < 0:
        return body_html
    end = body_html.find("</p>", start)
    para = body_html[start + 3:end]
    words = para.split(" ")
    if len(words) > 4 and "<" not in " ".join(words[:4]):
        para = '<span class="lead">' + " ".join(words[:4]) + "</span> " + " ".join(words[4:])
    return body_html[:start] + '<p class="firstpara dropcap">' + para + body_html[end:]


def uniq_ids(body_html, prefix):
    return re.sub(r'id="([^"]+)"', lambda m: f'id="{prefix}-{m.group(1)}"', body_html)


def chapters():
    n = 0
    for p_i, part in enumerate(BOOK["parts"], 1):
        for ch in part["chapters"]:
            n += 1
            yield p_i, part, n, ch


# ------------------------------------------------------------------ PDF
def build_pdf():
    from weasyprint import HTML
    toc, parts_html = [], []
    front_html = []
    for fm in BOOK["front"]:
        if not (MS / fm["file"]).exists():
            continue
        title, body = split_title((MS / fm["file"]).read_text())
        fid = fm["file"].replace(".md", "")
        body = uniq_ids(pandoc_html(body), fid)
        front_html.append(f'<section class="front front-page" id="{fid}"><h1 class="front-title">{html.escape(title)}</h1>{body}</section>')
        toc.append(f'<li class="tfront rom"><a href="#{fid}">{html.escape(title)}</a></li>')

    ch_no = 0
    for p_i, part in enumerate(BOOK["parts"], 1):
        pid = f"part{p_i}"
        toc.append(f'<li class="tpart"><a href="#{pid}">Part {WORDS[p_i]} &#8226; {html.escape(part["title"])}</a></li>')
        chap_list, chaps_html = [], []
        for ch in part["chapters"]:
            ch_no += 1
            if not (MS / ch).exists():
                continue
            title, body = split_title((MS / ch).read_text())
            cid = f"ch{ch_no}"
            body = uniq_ids(pandoc_html(number_sections(body, ch_no)), cid)
            body = dropcap(body)
            chap_list.append(f"<div><span>{ch_no:02d}</span>{html.escape(title)}</div>")
            toc.append(f'<li class="tch"><a href="#{cid}"><span class="n">{ch_no}</span>{html.escape(title)}</a></li>')
            chaps_html.append(
                f'<section class="chapter" id="{cid}"><div class="chap-head"><div class="clabel">Chapter</div>'
                f'<div class="cnum">{ch_no}</div><h1 class="ctitle">{html.escape(title)}</h1><div class="crule"></div></div>'
                f"{body}</section>")
        intro = pandoc_html(part["intro"])
        style = ' style="page: partfirst"' if p_i == 1 else ""
        parts_html.append(
            f'<section class="part" id="{pid}"{style}><div class="pnum">Part</div><div class="pbig">{WORDS[p_i]}</div><div class="pbar"></div>'
            f'<h1 class="ptitle">{html.escape(part["title"])}</h1><div class="pintro">{intro}</div>'
            f'<div class="pchaps">{"".join(chap_list)}</div></section>')
        parts_html.extend(chaps_html)

    back_html = []
    for bm in BOOK["back"]:
        if not (MS / bm["file"]).exists():
            continue
        title, body = split_title((MS / bm["file"]).read_text())
        bid = bm["file"].replace(".md", "")
        body = uniq_ids(pandoc_html(body), bid)
        back_html.append(f'<section class="backmatter {bm.get("cls", "")}" id="{bid}"><h1 class="front-title">{html.escape(title)}</h1>{body}</section>')
        toc.append(f'<li class="tfront"><a href="#{bid}">{html.escape(title)}</a></li>')

    halftitle = f'<section class="halftitle">{html.escape(TITLE)}</section>'
    titlepage = (f'<section class="titlepage"><div class="kanji">Goju-Ryu Karate</div>'
                 f'<div class="t1">Close-Combat<br/>Masterclass</div>'
                 f'<div class="rule"></div><div class="t2">{html.escape(SUBTITLE)}</div>'
                 f'<div class="auth">{html.escape(AUTHOR)}</div></section>')
    copyright_html = pandoc_html((MS / "copyright.md").read_text())
    disclaimer_t, disclaimer_b = split_title((MS / "disclaimer.md").read_text())
    dedication = pandoc_html((MS / "dedication.md").read_text())

    doc = f"""<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8"/>
<title>{html.escape(TITLE)}</title><meta name="author" content="{html.escape(AUTHOR)}"/>
<link rel="stylesheet" href="style/print.css"/></head><body>
{halftitle}{titlepage}
<section class="copyright">{copyright_html}</section>
<section class="disclaimer front-page front"><h1 class="front-title">{html.escape(disclaimer_t)}</h1>{pandoc_html(disclaimer_b)}</section>
<section class="dedication">{dedication}</section>
<section class="toc"><h1 class="front-title">Contents</h1><ul>{''.join(toc)}</ul></section>
{''.join(front_html)}
{''.join(parts_html)}
{''.join(back_html)}
</body></html>"""
    (BUILD / "book.html").write_text(doc)
    print("Rendering PDF ...")
    d = HTML(string=doc, base_url=str(ROOT)).render()
    print("pages:", len(d.pages))
    d.write_pdf(OUT / f"{FILE}.pdf")
    return len(d.pages)


# ------------------------------------------------------------------ shared markdown for EPUB / DOCX
def full_markdown(target):
    md = []
    for fm in BOOK["front"]:
        if (MS / fm["file"]).exists():
            title, body = split_title((MS / fm["file"]).read_text())
            md.append(f"# {title} {{.unnumbered .front}}\n\n{body}\n")
    for p_i, part in enumerate(BOOK["parts"], 1):
        chs = []
        for ch in part["chapters"]:
            pass
        md.append(f'# Part {WORDS[p_i]}: {part["title"]} {{.part .unnumbered}}\n\n::: part-intro\n{part["intro"]}\n:::\n')
        n0 = sum(len(p["chapters"]) for p in BOOK["parts"][:p_i - 1])
        for k, ch in enumerate(part["chapters"], 1):
            if not (MS / ch).exists():
                continue
            title, body = split_title((MS / ch).read_text())
            num = n0 + k
            body = number_sections(body, num).replace("{.secnum}", "{.secnum}")
            if target == "epub":
                body = re.sub(r"^(#{2,5}) ", lambda m: "#" + m.group(1) + " ", body, flags=re.M)
                md.append(f"## Chapter {num}: {title} {{.unnumbered}}\n\n{body}\n")
            else:
                md.append(f"# Chapter {num}: {title} {{.unnumbered}}\n\n{body}\n")
    for bm in BOOK["back"]:
        if (MS / bm["file"]).exists():
            title, body = split_title((MS / bm["file"]).read_text())
            md.append(f"# {title} {{.unnumbered .backmatter}}\n\n{body}\n")
    return "\n\n".join(md)


def meta_block():
    return f"""---
title:
- type: main
  text: "{TITLE}"
- type: subtitle
  text: "{SUBTITLE}"
subtitle: "{SUBTITLE}"
author: "{AUTHOR}"
creator:
- role: author
  text: "{AUTHOR}"
lang: en-GB
rights: "Copyright © 2026 {AUTHOR}. All rights reserved."
subject: "Sports & Recreation / Martial Arts / Karate"
description: "{BOOK['blurb']}"
---

"""


def build_epub():
    pre = (f"# Copyright {{.unnumbered .unlisted .copyright}}\n\n{(MS / 'copyright.md').read_text()}\n\n"
           f"{(MS / 'disclaimer.md').read_text().replace('# ', '# ', 1).rstrip()}\n\n"
           f"# Dedication {{.unnumbered .unlisted .dedication}}\n\n{(MS / 'dedication.md').read_text()}\n\n")
    pre = pre.replace("# Disclaimer", "# Disclaimer {.unnumbered .unlisted}", 1)
    src = BUILD / "book_epub.md"
    src.write_text(meta_block() + pre + full_markdown("epub"))
    cmd = ["pandoc", str(src), "-f", EXT, "-t", "epub3", "-o", str(OUT / f"{FILE}.epub"),
           "--toc", "--toc-depth=2", "--split-level=2", "--resource-path", str(ROOT),
           "--css", str(ROOT / "style/epub.css"), "--epub-title-page=true"]
    for f in ["EBGaramond-Regular", "EBGaramond-Italic", "EBGaramond-Bold", "SourceSans3-Regular", "SourceSans3-Bold"]:
        cmd += ["--epub-embed-font", str(ROOT / "fonts" / f"{f}.ttf")]
    if (ROOT / "figures/cover.jpg").exists():
        cmd += ["--epub-cover-image", str(ROOT / "figures/cover.jpg")]
    subprocess.run(cmd, check=True, cwd=ROOT)
    print("EPUB written")


def build_docx():
    import docx_ref
    ref = docx_ref.make_reference(BUILD / "reference.docx")
    body = full_markdown("docx")
    for cls, style in BOXES.items():
        body = re.sub(rf"^::: ?{re.escape(cls)}\s*$", f'::: {{custom-style="{style}"}}', body, flags=re.M)
    body = body.replace("::: part-intro", '::: {custom-style="Part Intro"}')
    front = (f"::: {{custom-style=\"Title Block\"}}\n**{TITLE}**\n:::\n\n"
             f"::: {{custom-style=\"Subtitle Block\"}}\n{SUBTITLE}\n:::\n\n"
             f"::: {{custom-style=\"Author Block\"}}\n{AUTHOR}\n:::\n\n"
             f"# Copyright {{.unnumbered}}\n\n{(MS / 'copyright.md').read_text()}\n\n"
             f"{(MS / 'disclaimer.md').read_text()}\n\n"
             f"# Dedication {{.unnumbered}}\n\n{(MS / 'dedication.md').read_text()}\n\n")
    src = BUILD / "book_docx.md"
    src.write_text(meta_block().replace('title:\n- type: main\n  text: "' + TITLE + '"\n- type: subtitle\n  text: "' + SUBTITLE + '"\n', f'title: "{TITLE}"\n') + front + body)
    out = OUT / f"{FILE}.docx"
    subprocess.run(["pandoc", str(src), "-f", EXT, "-t", "docx", "-o", str(out), "--toc", "--toc-depth=1",
                    "--reference-doc", str(ref), "--resource-path", str(ROOT)], check=True, cwd=ROOT)
    docx_ref.postprocess(out)
    print("DOCX written")


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("pdf", "all"):
        build_pdf()
    if what in ("epub", "all"):
        build_epub()
    if what in ("docx", "all"):
        build_docx()
