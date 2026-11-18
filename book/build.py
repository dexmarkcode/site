#!/usr/bin/env python3
"""Build the manuscript into a print-ready PDF (WeasyPrint) and an EPUB 3 (pandoc).

Usage:  python3 build.py [pdf|epub|all]
"""
import hashlib, html, os, re, subprocess, sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
MS = ROOT / "manuscript"
OUT = ROOT / "output"
EQ = ROOT / "build" / "eqs"
BUILD = ROOT / "build"
for d in (OUT, EQ, BUILD):
    d.mkdir(parents=True, exist_ok=True)

from book_meta import BOOK  # noqa: E402

TITLE = BOOK["title"]
SUBTITLE = BOOK["subtitle"]
AUTHOR = BOOK["author"]

# ------------------------------------------------------------------ equations
plt.rcParams["mathtext.fontset"] = "stix"
plt.rcParams["svg.fonttype"] = "path"
EQ_RE = re.compile(r"^\$\$(.+?)\$\$\s*(?:\{([^}]*)\})?\s*$")


def render_eq(tex):
    key = hashlib.sha1(tex.encode()).hexdigest()[:12]
    svg, png = EQ / f"{key}.svg", EQ / f"{key}.png"
    if not svg.exists() or not png.exists():
        fig = plt.figure(figsize=(0.01, 0.01))
        fig.text(0, 0, f"${tex}$", fontsize=11.6, color="#1c1c1c")
        fig.savefig(svg, bbox_inches="tight", pad_inches=0.015, transparent=True)
        fig.savefig(png, bbox_inches="tight", pad_inches=0.015, transparent=True, dpi=300)
        plt.close(fig)
    txt = svg.read_text()
    w = float(re.search(r'width="([\d.]+)pt"', txt).group(1))
    return key, w


def preprocess(md_text, chapter_no=None, epub=False):
    """Number h2 headings, render display equations."""
    out, sec, in_code = [], 0, False
    for line in md_text.splitlines():
        if line.startswith("```"):
            in_code = not in_code
        if in_code:
            out.append(line)
            continue
        m = EQ_RE.match(line.strip())
        if m:
            tex, num = m.group(1).strip(), m.group(2)
            key, w = render_eq(tex)
            if epub:
                img = f'<img src="build/eqs/{key}.png" alt="equation" style="width:{w/11.2:.2f}em" />'
            else:
                img = f'<img src="build/eqs/{key}.svg" alt="equation" style="width:{w:.1f}pt" />'
            n = f'<span class="eqn">({num})</span>' if num else ""
            out.append("")
            out.append(f'<div class="eq">{img}{n}</div>')
            out.append("")
            continue
        if chapter_no and line.startswith("## ") and "{.unnumbered}" not in line:
            sec += 1
            line = f"## [{chapter_no}.{sec}]{{.secnum}} {line[3:].strip()}"
        out.append(line)
    return "\n".join(out)


def pandoc_html(md_text):
    r = subprocess.run(
        ["pandoc", "-f", "markdown+smart+fenced_divs+bracketed_spans+pipe_tables+grid_tables+superscript+subscript",
         "-t", "html5", "--wrap=none"],
        input=md_text, capture_output=True, text=True, check=True)
    return r.stdout


def split_title(md_text):
    lines = md_text.strip("\n").splitlines()
    assert lines[0].startswith("# "), lines[0]
    return lines[0][2:].strip(), "\n".join(lines[1:])


def number_word(n):
    return ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"][n]


# ------------------------------------------------------------------ PDF
def dropcap(body_html):
    """Apply a drop cap and small-caps lead-in to the first body paragraph after the intro."""
    m = re.search(r'(</div>\s*)?<p>(?!<img)', body_html)
    # find first <p> that is not inside the chapter-intro div
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
        idm = re.search(r'id="([^"]+)"', attrs)
        sid = f"{ch_id}-{idm.group(1)}" if idm else f"{ch_id}-s{len(secs)+1}"
        attrs = re.sub(r'id="[^"]+"', "", attrs)
        secs.append((sid, re.sub(r"<[^>]+>", "", inner)))
        return f'<h2 id="{sid}"{attrs}>{inner}</h2>'
    body_html = re.sub(r"<h2([^>]*)>(.*?)</h2>", repl, body_html)
    # make other ids unique too
    body_html = re.sub(r'<h([34]) id="([^"]+)"', lambda m: f'<h{m.group(1)} id="{ch_id}-{m.group(2)}"', body_html)
    return body_html, secs


def build_pdf():
    from weasyprint import HTML
    parts_html, toc = [], []

    # front matter files
    front_html = []
    for fm in BOOK["front"]:
        title, body = split_title((MS / fm["file"]).read_text())
        body = pandoc_html(preprocess(body))
        fid = fm["file"].replace(".md", "")
        front_html.append(f'<section class="front front-page" id="{fid}"><h1 class="front-title">{html.escape(title)}</h1>{body}</section>')
        toc.append(f'<li class="tfront rom"><a href="#{fid}">{html.escape(title)}</a></li>')

    ch_no = 0
    for p_i, part in enumerate(BOOK["parts"], 1):
        pid = f"part{p_i}"
        toc.append(f'<li class="tpart"><a href="#{pid}">Part {number_word(p_i)} &#8226; {html.escape(part["title"])}</a></li>')
        chap_list = []
        chaps_html = []
        for ch in part["chapters"]:
            ch_no += 1
            if not (MS / ch).exists():
                continue
            title, body = split_title((MS / ch).read_text())
            body = pandoc_html(preprocess(body, ch_no))
            cid = f"ch{ch_no}"
            body, secs = collect_sections(body, cid)
            body = dropcap(body)
            chap_list.append(f"<div><span>{ch_no:02d}</span>{html.escape(title)}</div>")
            toc.append(f'<li class="tch"><a href="#{cid}"><span class="n">{ch_no}</span>{html.escape(title)}</a></li>')
            for sid, st in secs:
                toc.append(f'<li class="tsec"><a href="#{sid}">{html.escape(st)}</a></li>')
            chaps_html.append(
                f'<section class="chapter" id="{cid}"><div class="chap-head"><div class="clabel">Chapter</div>'
                f'<div class="cnum">{ch_no:02d}</div><h1 class="ctitle">{html.escape(title)}</h1><div class="crule"></div></div>'
                f"{body}</section>")
        intro = pandoc_html(part["intro"])
        fig = f'<img class="pfig" src="figures/part{p_i}.png" />' if (ROOT / f"figures/part{p_i}.png").exists() else ""
        parts_html.append(
            f'<section class="part" id="{pid}"{" style=\"page: partfirst\"" if p_i == 1 else ""}><div class="pnum">Part {number_word(p_i)}</div><div class="pbar"></div>'
            f'<h1 class="ptitle">{html.escape(part["title"])}</h1><div class="pintro">{intro}</div>'
            f'<div class="pchaps">{"".join(chap_list)}</div>{fig}</section>')
        parts_html.extend(chaps_html)

    back_html = []
    for bm in BOOK["back"]:
        if not (MS / bm["file"]).exists():
            continue
        title, body = split_title((MS / bm["file"]).read_text())
        body = pandoc_html(preprocess(body))
        bid = bm["file"].replace(".md", "")
        cls = bm.get("cls", "")
        back_html.append(f'<section class="backmatter {cls}" id="{bid}"><h1 class="front-title">{html.escape(title)}</h1>{body}</section>')
        toc.append(f'<li class="tfront"><a href="#{bid}">{html.escape(title)}</a></li>')

    cover = '<section class="cover"><img src="figures/cover.png" /></section>' if (ROOT / "figures/cover.png").exists() else ""
    titlepage = (f'<section class="titlepage"><div class="t1">Electric Vehicle<br/>Engineering</div>'
                 f'<div class="t2">{html.escape(SUBTITLE)}</div><div class="bolt"></div>'
                 f'<div class="auth">{html.escape(AUTHOR)}</div><div class="ed">First Edition</div></section>')
    copyright_html = pandoc_html((MS / "copyright.md").read_text())
    dedication = pandoc_html((MS / "dedication.md").read_text())

    doc = f"""<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8"/>
<title>{html.escape(TITLE)}</title><meta name="author" content="{html.escape(AUTHOR)}"/>
<link rel="stylesheet" href="style/print.css"/></head><body>
{cover}{titlepage}
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
    doc_obj.write_pdf(OUT / "Electric-Vehicle-Engineering_Marcus-J-Thornton.pdf")
    return len(doc_obj.pages)


# ------------------------------------------------------------------ EPUB
def build_epub():
    md = []
    for fm in BOOK["front"]:
        title, body = split_title((MS / fm["file"]).read_text())
        md.append(f"# {title} {{.unnumbered .front}}\n\n{preprocess(body, epub=True)}\n")
    ch_no = 0
    for p_i, part in enumerate(BOOK["parts"], 1):
        chs = []
        for ch in part["chapters"]:
            ch_no += 1
            if not (MS / ch).exists():
                continue
            title, body = split_title((MS / ch).read_text())
            body = preprocess(body, ch_no, epub=True)
            # shift headings down one level (part = h1, chapter = h2)
            body = re.sub(r"^(#{2,5}) ", lambda m: "#" + m.group(1) + " ", body, flags=re.M)
            chs.append(f'## Chapter {ch_no}: {title}\n\n{body}\n')
        md.append(f'# Part {number_word(p_i)}: {part["title"]} {{.part}}\n\n::: part-intro\n{part["intro"]}\n:::\n\n' + "\n".join(chs))
    for bm in BOOK["back"]:
        if not (MS / bm["file"]).exists():
            continue
        title, body = split_title((MS / bm["file"]).read_text())
        md.append(f"# {title} {{.backmatter}}\n\n{preprocess(body, epub=True)}\n")

    copyright_md = (MS / "copyright.md").read_text()
    dedication_md = (MS / "dedication.md").read_text()
    full = "\n\n".join(md)
    meta = f"""---
title:
- type: main
  text: "Electric Vehicle Engineering"
- type: subtitle
  text: "{SUBTITLE}"
creator:
- role: author
  text: "{AUTHOR}"
lang: en-GB
rights: "Copyright © 2026 {AUTHOR}. All rights reserved."
subject: "Technology & Engineering / Automotive"
description: "{BOOK['blurb']}"
---

"""
    pre = f'# Copyright {{.unnumbered .unlisted .copyright}}\n\n{copyright_md}\n\n# Dedication {{.unnumbered .unlisted .dedication}}\n\n{dedication_md}\n\n'
    src = BUILD / "book_epub.md"
    src.write_text(meta + pre + full)
    cmd = ["pandoc", str(src), "-f", "markdown+smart+fenced_divs+bracketed_spans+pipe_tables+grid_tables+superscript+subscript",
           "-t", "epub3", "-o", str(OUT / "Electric-Vehicle-Engineering_Marcus-J-Thornton.epub"),
           "--toc", "--toc-depth=2", "--split-level=2", "--resource-path", str(ROOT),
           "--css", str(ROOT / "style/epub.css"), "--epub-title-page=true"]
    for f in sorted((ROOT / "fonts").glob("*.ttf")):
        cmd += ["--epub-embed-font", str(f)]
    if (ROOT / "figures/cover.png").exists():
        cmd += ["--epub-cover-image", str(ROOT / "figures/cover.png")]
    subprocess.run(cmd, check=True, cwd=ROOT)
    print("EPUB written")


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("pdf", "all"):
        build_pdf()
    if what in ("epub", "all"):
        build_epub()
