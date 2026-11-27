#!/usr/bin/env python3
"""Build the manuscript into a print-ready PDF (WeasyPrint), an EPUB 3 and a
Word DOCX (pandoc).  Black and white, 6 x 9 in, single column.

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

TITLE, SUBTITLE, AUTHOR = BOOK["title"], BOOK["subtitle"], BOOK["author"]
STEM = "Goju-Ryu-Karate-Kyohan-Volume-Two_Dr-Beverly-J-Stivers"
MDFMT = "markdown+smart+fenced_divs+bracketed_spans+pipe_tables+grid_tables+definition_lists"
WORDS = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
         "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen",
         "Nineteen", "Twenty"]


def preprocess(md_text, chapter_no=None):
    out = []
    for line in md_text.splitlines():
        if chapter_no and line.startswith("## ") and "{.unnumbered}" not in line:
            pass
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


def uniq_ids(body_html, cid):
    return re.sub(r'<h([234]) id="([^"]+)"', lambda m: f'<h{m.group(1)} id="{cid}-{m.group(2)}"', body_html)


def chapters():
    n = 0
    for p_i, part in enumerate(BOOK["parts"], 1):
        for ch in part["chapters"]:
            n += 1
            yield p_i, n, ch


# ------------------------------------------------------------------ PDF
def build_pdf():
    from weasyprint import HTML
    parts_html, toc = [], []
    front_html = []
    for fm in BOOK["front"]:
        title, body = split_title((MS / fm["file"]).read_text())
        body = pandoc_html(body)
        fid = fm["file"].replace(".md", "")
        front_html.append(f'<section class="front front-page" id="{fid}"><h1 class="front-title">{html.escape(title)}</h1>{body}</section>')
        toc.append(f'<li class="tfront rom"><a href="#{fid}">{html.escape(title)}</a></li>')

    ch_no = 0
    for p_i, part in enumerate(BOOK["parts"], 1):
        pid = f"part{p_i}"
        toc.append(f'<li class="tpart"><a href="#{pid}">Part {WORDS[p_i]} &#8195; {html.escape(part["title"])}</a></li>')
        chap_list, chaps_html = [], []
        for ch in part["chapters"]:
            ch_no += 1
            if not (MS / ch).exists():
                continue
            title, body = split_title((MS / ch).read_text())
            body = pandoc_html(body)
            cid = f"ch{ch_no}"
            body = dropcap(uniq_ids(body, cid))
            chap_list.append(f"<div><span>{ch_no}</span>{html.escape(title)}</div>")
            toc.append(f'<li class="tch"><a href="#{cid}"><span class="n">{ch_no}</span>{html.escape(title)}</a></li>')
            chaps_html.append(
                f'<section class="chapter" id="{cid}"><div class="chap-head"><div class="clabel">Chapter {WORDS[ch_no]}</div>'
                f'<h1 class="ctitle">{html.escape(title)}</h1><div class="crule"></div></div>{body}</section>')
        intro = pandoc_html(part["intro"])
        fig = f'<img class="pfig" src="figures/part{p_i}.png" />' if (ROOT / f"figures/part{p_i}.png").exists() else ""
        style = ' style="page: partfirst"' if p_i == 1 else ""
        parts_html.append(
            f'<section class="part" id="{pid}"{style}><div class="pnum">Part {WORDS[p_i]}</div><div class="pbar"></div>'
            f'<h1 class="ptitle">{html.escape(part["title"])}</h1><div class="pintro">{intro}</div>'
            f'<div class="pchaps">{"".join(chap_list)}</div>{fig}</section>')
        parts_html.extend(chaps_html)

    back_html = []
    for bm in BOOK["back"]:
        if not (MS / bm["file"]).exists():
            continue
        title, body = split_title((MS / bm["file"]).read_text())
        body = pandoc_html(body)
        bid = bm["file"].replace(".md", "")
        cls = bm.get("cls", "")
        back_html.append(f'<section class="backmatter {cls}" id="{bid}"><h1 class="front-title">{html.escape(title)}</h1>{body}</section>')
        toc.append(f'<li class="tfront"><a href="#{bid}">{html.escape(title)}</a></li>')

    halftitle = '<section class="halftitle"><div class="h1">Goju-Ryu Karate Kyohan</div><div class="h2">Volume Two</div></section>'
    emblem = '<img src="figures/title_emblem.png" />' if (ROOT / "figures/title_emblem.png").exists() else ""
    titlepage = (f'<section class="titlepage"><div class="t0">Goju-Ryu</div><div class="t1">Karate Kyohan</div>'
                 f'<div class="tv">Volume Two</div><div class="rule"></div>'
                 f'<div class="t2">{html.escape(SUBTITLE)}</div>{emblem}'
                 f'<div class="auth">{html.escape(AUTHOR)}</div></section>')
    copyright_html = pandoc_html((MS / "copyright.md").read_text())
    dedication = pandoc_html((MS / "dedication.md").read_text())

    doc = f"""<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8"/>
<title>{html.escape(TITLE)}</title><meta name="author" content="{html.escape(AUTHOR)}"/>
<link rel="stylesheet" href="style/print.css"/></head><body>
{halftitle}{titlepage}
<section class="copyright">{copyright_html}</section>
<section class="dedication">{dedication}</section>
<section class="toc"><h1 class="front-title">Contents</h1><ul>{''.join(toc)}</ul></section>
{''.join(front_html)}
{''.join(parts_html)}
{''.join(back_html)}
</body></html>"""
    (BUILD / "book.html").write_text(doc)
    print("Rendering PDF ...")
    doc_obj = HTML(string=doc, base_url=str(ROOT)).render()
    print("pages:", len(doc_obj.pages))
    doc_obj.write_pdf(OUT / f"{STEM}.pdf")
    return len(doc_obj.pages)


# ------------------------------------------------------------------ shared markdown for EPUB / DOCX
def full_markdown(target):
    md = []
    for fm in BOOK["front"]:
        title, body = split_title((MS / fm["file"]).read_text())
        md.append(f"# {title} {{.unnumbered .front}}\n\n{body}\n")
    ch_no = 0
    for p_i, part in enumerate(BOOK["parts"], 1):
        chs = []
        for ch in part["chapters"]:
            ch_no += 1
            if not (MS / ch).exists():
                continue
            title, body = split_title((MS / ch).read_text())
            body = re.sub(r"^(#{2,5}) ", lambda m: "#" + m.group(1) + " ", body, flags=re.M)
            if target == "docx":
                body = re.sub(r"(!\[[^\]]*\]\([^)]+\))(?!\{)", r"\1{width=4.3in}", body)
            chs.append(f"## Chapter {WORDS[ch_no]}: {title}\n\n{body}\n")
        md.append(f'# Part {WORDS[p_i]}: {part["title"]} {{.part}}\n\n::: part-intro\n{part["intro"]}\n:::\n\n' + "\n".join(chs))
    for bm in BOOK["back"]:
        if not (MS / bm["file"]).exists():
            continue
        title, body = split_title((MS / bm["file"]).read_text())
        md.append(f"# {title} {{.backmatter}}\n\n{body}\n")
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
    copyright_md = (MS / "copyright.md").read_text()
    dedication_md = (MS / "dedication.md").read_text()
    pre = (f"# Copyright {{.unnumbered .unlisted .copyright}}\n\n{copyright_md}\n\n"
           f"# Dedication {{.unnumbered .unlisted .dedication}}\n\n{dedication_md}\n\n")
    src = BUILD / "book_epub.md"
    src.write_text(meta_block() + pre + full_markdown("epub"))
    cmd = ["pandoc", str(src), "-f", MDFMT, "-t", "epub3", "-o", str(OUT / f"{STEM}.epub"),
           "--toc", "--toc-depth=2", "--split-level=2", "--resource-path", str(ROOT),
           "--css", str(ROOT / "style/epub.css"), "--epub-title-page=true"]
    for f in sorted((ROOT / "fonts").glob("EBGaramond*.ttf")):
        cmd += ["--epub-embed-font", str(f)]
    if (ROOT / "figures/cover.png").exists():
        cmd += ["--epub-cover-image", str(ROOT / "figures/cover.png")]
    subprocess.run(cmd, check=True, cwd=ROOT)
    print("EPUB written")


def build_docx():
    ref = BUILD / "reference.docx"
    make_reference(ref)
    copyright_md = (MS / "copyright.md").read_text()
    dedication_md = (MS / "dedication.md").read_text()
    pre = (f"# Copyright {{.unnumbered}}\n\n{copyright_md}\n\n"
           f"# Dedication {{.unnumbered}}\n\n{dedication_md}\n\n")
    src = BUILD / "book_docx.md"
    src.write_text(meta_block() + pre + full_markdown("docx"))
    out = OUT / f"{STEM}.docx"
    subprocess.run(["pandoc", str(src), "-f", MDFMT, "-t", "docx", "-o", str(out), "--toc", "--toc-depth=2",
                    "--resource-path", str(ROOT), "--reference-doc", str(ref)], check=True, cwd=ROOT)
    finish_docx(out)
    print("DOCX written")


def make_reference(path):
    from docx import Document
    from docx.shared import Pt, Inches, RGBColor
    raw = subprocess.run(["pandoc", "-o", str(path), "--print-default-data-file", "reference.docx"], capture_output=True)
    path.write_bytes(raw.stdout)
    d = Document(str(path))
    for sec in d.sections:
        sec.page_width, sec.page_height = Inches(6), Inches(9)
        sec.top_margin, sec.bottom_margin = Inches(0.8), Inches(0.8)
        sec.left_margin, sec.right_margin = Inches(0.85), Inches(0.6)
        sec.gutter = Inches(0)
    black = RGBColor(0, 0, 0)
    for st in d.styles:
        try:
            f = st.font
        except Exception:
            continue
        if f is None:
            continue
        f.color.rgb = black
        f.name = "Garamond"
    for name, size in (("Normal", 11), ("Body Text", 11), ("First Paragraph", 11), ("Heading 1", 20), ("Heading 2", 17),
                       ("Heading 3", 11), ("Heading 4", 12), ("Heading 5", 10), ("Title", 26), ("Subtitle", 13),
                       ("Author", 13), ("Image Caption", 9), ("Block Text", 10.5)):
        try:
            d.styles[name].font.size = Pt(size)
            d.styles[name].font.color.rgb = black
        except KeyError:
            pass
    for name in ("Body Text", "First Paragraph"):
        try:
            pf = d.styles[name].paragraph_format
            pf.line_spacing = 1.2
            pf.space_after = Pt(4)
            from docx.enum.text import WD_ALIGN_PARAGRAPH
            pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        except KeyError:
            pass
    d.save(str(path))


def finish_docx(path):
    from docx import Document
    from docx.shared import Inches
    from docx.enum.section import WD_SECTION
    d = Document(str(path))
    for sec in d.sections:
        sec.page_width, sec.page_height = Inches(6), Inches(9)
        sec.top_margin, sec.bottom_margin = Inches(0.8), Inches(0.8)
        sec.left_margin, sec.right_margin = Inches(0.85), Inches(0.6)
    # page break before every Heading 1 and Heading 2
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    for p in d.paragraphs:
        if p.style.name in ("Heading 1", "Heading 2"):
            pPr = p._p.get_or_add_pPr()
            pb = OxmlElement("w:pageBreakBefore")
            pPr.insert(0, pb)
    d.save(str(path))


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("pdf", "all"):
        build_pdf()
    if what in ("epub", "all"):
        build_epub()
    if what in ("docx", "all"):
        build_docx()
