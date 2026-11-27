#!/usr/bin/env python3
"""Build the manuscript into a print-ready PDF (WeasyPrint), an EPUB 3 and a DOCX (pandoc).

Usage:  python3 build.py [pdf|epub|docx|all]
"""
import html, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MS = ROOT / "manuscript"
OUT = ROOT / "output"
BUILD = ROOT / "build"
for d in (OUT, BUILD):
    d.mkdir(parents=True, exist_ok=True)

from book_meta import BOOK  # noqa: E402

TITLE, SUBTITLE, AUTHOR, SLUG = BOOK["title"], BOOK["subtitle"], BOOK["author"], BOOK["slug"]
MDFMT = "markdown+smart+fenced_divs+bracketed_spans+pipe_tables+grid_tables+superscript+subscript"

ONES = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven",
        "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
TENS = {20: "Twenty", 30: "Thirty"}


def number_word(n):
    if n < 20:
        return ONES[n]
    t, o = (n // 10) * 10, n % 10
    return TENS[t] + ("-" + ONES[o] if o else "")


def preprocess(md_text, chapter_no=None):
    """Number h2 headings n.m."""
    out, sec = [], 0
    for line in md_text.splitlines():
        if chapter_no and line.startswith("## ") and "{.unnumbered}" not in line:
            sec += 1
            line = f"## [{chapter_no}.{sec}]{{.secnum}} {line[3:].strip()}"
        out.append(line)
    return "\n".join(out)


def pandoc_html(md_text):
    r = subprocess.run(["pandoc", "-f", MDFMT, "-t", "html5", "--wrap=none"],
                       input=md_text, capture_output=True, text=True, check=True)
    return r.stdout


def split_title(md_text):
    lines = md_text.strip("\n").splitlines()
    assert lines[0].startswith("# "), lines[0]
    return lines[0][2:].strip(), "\n".join(lines[1:])


def chapters():
    """Yield (part_index, part, chapter_no, filename)."""
    n = 0
    for p_i, part in enumerate(BOOK["parts"], 1):
        for ch in part["chapters"]:
            n += 1
            yield p_i, part, n, ch


# ------------------------------------------------------------------ PDF
def dropcap(body_html):
    intro_end = body_html.find("</div>") if body_html.lstrip().startswith('<div class="chapter-intro"') else -1
    start = body_html.find("<p>", intro_end + 1 if intro_end >= 0 else 0)
    if start < 0:
        return body_html
    end = body_html.find("</p>", start)
    para = body_html[start + 3:end]
    words = para.split(" ")
    lead_n = 4
    if len(words) > lead_n and "<" not in " ".join(words[:lead_n]):
        para = '<span class="lead">' + " ".join(words[:lead_n]) + "</span> " + " ".join(words[lead_n:])
    return body_html[:start] + '<p class="firstpara dropcap">' + para + body_html[end:]


def collect_sections(body_html, ch_id):
    secs = []

    def repl(m):
        attrs, inner = m.group(1), m.group(2)
        sid = f"{ch_id}-s{len(secs)+1}"
        attrs = re.sub(r'id="[^"]+"', "", attrs)
        secs.append((sid, re.sub(r"<[^>]+>", "", inner)))
        return f'<h2 id="{sid}"{attrs}>{inner}</h2>'
    body_html = re.sub(r"<h2([^>]*)>(.*?)</h2>", repl, body_html)
    body_html = re.sub(r'<h([34]) id="([^"]+)"', lambda m: f'<h{m.group(1)} id="{ch_id}-{m.group(2)}"', body_html)
    return body_html, secs


ORN = '<div class="orn"><span></span><i></i><span></span></div>'


def build_pdf():
    from weasyprint import HTML
    parts_html, toc = [], []

    front_html = []
    for fm in BOOK["front"]:
        title, body = split_title((MS / fm["file"]).read_text())
        body = pandoc_html(body)
        fid = fm["file"].replace(".md", "")
        front_html.append(f'<section class="front front-page" id="{fid}"><h1 class="front-title">{html.escape(title)}</h1>{ORN}{body}</section>')
        toc.append(f'<li class="tfront rom"><a href="#{fid}">{html.escape(title)}</a></li>')

    cur_part, chap_list, chaps_html = None, [], []

    def flush_part():
        if cur_part is None:
            return
        p_i, part = cur_part
        intro = pandoc_html(part["intro"])
        fig = f'<img class="pfig" src="figures/part{p_i}.png" />' if (ROOT / f"figures/part{p_i}.png").exists() else ""
        parts_html.append(
            f'<section class="part" id="part{p_i}"{" style=\"page: partfirst\"" if p_i == 1 else ""}>'
            f'<div class="pnum">Part {number_word(p_i)}</div>{fig}'
            f'<h1 class="ptitle">{html.escape(part["title"])}</h1>{ORN}<div class="pintro">{intro}</div>'
            f'<div class="pchaps">{"".join(chap_list)}</div></section>')
        parts_html.extend(chaps_html)

    for p_i, part, ch_no, ch in chapters():
        if cur_part is None or cur_part[0] != p_i:
            flush_part()
            cur_part, chap_list, chaps_html = (p_i, part), [], []
            toc.append(f'<li class="tpart"><a href="#part{p_i}">Part {number_word(p_i)} &#8194; {html.escape(part["title"])}</a></li>')
        if not (MS / ch).exists():
            continue
        title, body = split_title((MS / ch).read_text())
        body = pandoc_html(preprocess(body, ch_no))
        cid = f"ch{ch_no}"
        body, secs = collect_sections(body, cid)
        body = dropcap(body)
        chap_list.append(f"<div><span>{ch_no}</span>{html.escape(title)}</div>")
        toc.append(f'<li class="tch"><a href="#{cid}"><span class="n">{ch_no}</span>{html.escape(title)}</a></li>')
        chaps_html.append(
            f'<section class="chapter" id="{cid}"><div class="chap-head"><div class="clabel">Chapter {number_word(ch_no)}</div>'
            f'<h1 class="ctitle">{html.escape(title)}</h1>{ORN}</div>'
            f"{body}</section>")
    flush_part()

    back_html = []
    for bm in BOOK["back"]:
        if not (MS / bm["file"]).exists():
            continue
        title, body = split_title((MS / bm["file"]).read_text())
        body = pandoc_html(body)
        bid = bm["file"].replace(".md", "")
        cls = bm.get("cls", "")
        back_html.append(f'<section class="backmatter {cls}" id="{bid}"><h1 class="front-title">{html.escape(title)}</h1>{ORN}{body}</section>')
        toc.append(f'<li class="tfront"><a href="#{bid}">{html.escape(title)}</a></li>')

    halftitle = f'<section class="halftitle"><div class="ht">{html.escape(TITLE)}</div></section>'
    titlepage = (f'<section class="titlepage"><div class="t0">Goju-Ryu Karate</div><div class="t1">Sanchin<br/>Masterclass</div>'
                 f'{ORN}<div class="t2">{html.escape(SUBTITLE)}</div>'
                 f'<img class="tfig" src="figures/title.png" />'
                 f'<div class="auth">{html.escape(AUTHOR)}</div></section>')
    copyright_html = pandoc_html((MS / "copyright.md").read_text())
    dedication = pandoc_html((MS / "dedication.md").read_text())

    doc = f"""<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8"/>
<title>{html.escape(TITLE)}</title><meta name="author" content="{html.escape(AUTHOR)}"/>
<style>@page :left {{ @top-center {{ content: "{BOOK['running']}"; }} }}</style>
<link rel="stylesheet" href="style/print.css"/></head><body>
{halftitle}{titlepage}
<section class="copyright">{copyright_html}</section>
<section class="dedication">{dedication}</section>
<section class="toc"><h1 class="front-title">Contents</h1>{ORN}<ul>{''.join(toc)}</ul></section>
{''.join(front_html)}
{''.join(parts_html)}
{''.join(back_html)}
</body></html>"""
    (BUILD / "book.html").write_text(doc)
    print("Rendering PDF ...")
    doc_obj = HTML(string=doc, base_url=str(ROOT)).render()
    print("pages:", len(doc_obj.pages))
    doc_obj.write_pdf(OUT / f"{SLUG}.pdf")
    return len(doc_obj.pages)


# ------------------------------------------------------------------ EPUB / DOCX shared markdown
BOXES = {"drill": "Drill Box", "fault": "Fault Box", "note": "Note Box", "test": "Test Box",
         "keypoints": "Summary Box", "practice": "Practice Box", "chapter-intro": "Chapter Intro"}


def full_markdown(target):
    md = []
    for fm in BOOK["front"]:
        title, body = split_title((MS / fm["file"]).read_text())
        md.append(f"# {title} {{.unnumbered .front}}\n\n{body}\n")
    cur = None
    for p_i, part, ch_no, ch in chapters():
        if cur != p_i:
            cur = p_i
            md.append(f'# Part {number_word(p_i)}: {part["title"]} {{.part .unnumbered}}\n\n::: part-intro\n{part["intro"]}\n:::\n')
        if not (MS / ch).exists():
            continue
        title, body = split_title((MS / ch).read_text())
        body = preprocess(body, ch_no)
        body = re.sub(r"^(#{2,5}) ", lambda m: "#" + m.group(1) + " ", body, flags=re.M)
        md.append(f'## Chapter {ch_no}: {title} {{.unnumbered}}\n\n{body}\n')
    for bm in BOOK["back"]:
        if not (MS / bm["file"]).exists():
            continue
        title, body = split_title((MS / bm["file"]).read_text())
        md.append(f"# {title} {{.backmatter .unnumbered}}\n\n{body}\n")
    full = "\n\n".join(md)
    if target == "docx":
        # fenced div classes -> Word custom styles
        def div(m):
            cls = m.group(1)
            return f'::: {{custom-style="{BOXES[cls]}"}}' if cls in BOXES else m.group(0)
        full = re.sub(r"^::: ?([a-z-]+)\s*$", div, full, flags=re.M)
        full = full.replace("::: part-intro", '::: {custom-style="Part Intro"}')
        full = re.sub(r"\[(\d+\.\d+)\]\{\.secnum\}", r"\1 ", full)
    return full


def meta_block():
    return f"""---
title:
- type: main
  text: "{TITLE}"
- type: subtitle
  text: "{SUBTITLE}"
creator:
- role: author
  text: "{AUTHOR}"
author: "{AUTHOR}"
subtitle: "{SUBTITLE}"
lang: en-GB
rights: "Copyright © 2026 {AUTHOR}. All rights reserved."
subject: "Sports & Recreation / Martial Arts / Karate"
description: "{BOOK['blurb']}"
---

"""


def build_epub():
    copyright_md = (MS / "copyright.md").read_text()
    dedication_md = (MS / "dedication.md").read_text()
    pre = (f'# Copyright {{.unnumbered .unlisted .copyright}}\n\n{copyright_md}\n\n'
           f'# Dedication {{.unnumbered .unlisted .dedication}}\n\n{dedication_md}\n\n')
    src = BUILD / "book_epub.md"
    src.write_text(meta_block() + pre + full_markdown("epub"))
    cmd = ["pandoc", str(src), "-f", MDFMT, "-t", "epub3", "-o", str(OUT / f"{SLUG}.epub"),
           "--toc", "--toc-depth=2", "--split-level=2", "--resource-path", str(ROOT),
           "--css", str(ROOT / "style/epub.css"), "--epub-title-page=true"]
    for f in sorted((ROOT / "fonts").glob("*.ttf")):
        cmd += ["--epub-embed-font", str(f)]
    if (ROOT / "figures/cover.jpg").exists():
        cmd += ["--epub-cover-image", str(ROOT / "figures/cover.jpg")]
    subprocess.run(cmd, check=True, cwd=ROOT)
    print("EPUB written")


def build_docx():
    import make_reference
    ref = make_reference.build(BUILD / "reference.docx")
    copyright_md = (MS / "copyright.md").read_text()
    dedication_md = (MS / "dedication.md").read_text()
    titlepage = (f'::: {{custom-style="Book Title"}}\nGoju-Ryu Karate Sanchin Masterclass\n:::\n\n'
                 f'::: {{custom-style="Book Subtitle"}}\n{SUBTITLE}\n:::\n\n'
                 f'![](figures/title.png){{width=2.6in}}\n\n'
                 f'::: {{custom-style="Book Author"}}\n{AUTHOR}\n:::\n\n'
                 f'```{{=openxml}}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n\n'
                 f'::: {{custom-style="Copyright"}}\n{copyright_md}\n:::\n\n'
                 f'```{{=openxml}}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n\n'
                 f'::: {{custom-style="Dedication"}}\n{dedication_md}\n:::\n\n')
    meta = '---\nlang: en-GB\n---\n\n'
    toc_field = ('```{=openxml}\n<w:p><w:pPr><w:pStyle w:val="TOCHeading"/></w:pPr><w:r><w:t>Contents</w:t></w:r></w:p>'
                 '<w:p><w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>'
                 '<w:r><w:instrText xml:space="preserve"> TOC \\o "1-2" \\h \\z \\u </w:instrText></w:r>'
                 '<w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>Right-click and choose Update Field to build the contents list.</w:t></w:r>'
                 '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>'
                 '<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n\n')
    titlepage = titlepage + toc_field
    src = BUILD / "book_docx.md"
    src.write_text(meta + titlepage + full_markdown("docx"))
    cmd = ["pandoc", str(src), "-f", MDFMT, "-t", "docx", "-o", str(OUT / f"{SLUG}.docx"),
           "--reference-doc", str(ref), "--resource-path", str(ROOT), "--dpi=300"]
    subprocess.run(cmd, check=True, cwd=ROOT)
    make_reference.postprocess(OUT / f"{SLUG}.docx")
    print("DOCX written")


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("pdf", "all"):
        build_pdf()
    if what in ("epub", "all"):
        build_epub()
    if what in ("docx", "all"):
        build_docx()
