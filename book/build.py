#!/usr/bin/env python3
"""Build the PDF (WeasyPrint) and EPUB (pandoc) editions of the book."""
import html
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MS = os.path.join(HERE, "manuscript")
OUT = os.path.join(HERE, "output")
os.makedirs(OUT, exist_ok=True)

TITLE = "Circuit Analysis Made Simple"
SUBTITLE = "A Modern Textbook for Beginners – Ohm’s Law to Thévenin, Norton, and Mesh Analysis Explained Clearly"
AUTHOR = "Marcus J. Thornton, Ph.D."

PARTS = [
    ("One", "Foundations of Electricity",
     ["Before you can analyse a circuit you need to know, really know, what is moving through it and what is pushing it along.",
      "Part One builds that understanding from the ground up: charge, current, voltage, resistance, power and the law that ties them together."],
     [1, 2, 3]),
    ("Two", "The Language and Laws of Circuits",
     ["Every method in circuit analysis rests on two simple laws discovered by Gustav Kirchhoff in 1845.",
      "Here you will learn to read circuit diagrams fluently, apply Kirchhoff’s laws with confidence, and handle series and parallel circuits with ease."],
     [4, 5, 6]),
    ("Three", "Simplifying Networks",
     ["Most real circuits can be made smaller before they are solved.",
      "Part Three gives you the tools to reduce a tangled network to something you can handle: equivalent resistance, dividers, bridges and the delta–star transformation."],
     [7, 8, 9]),
    ("Four", "Systematic Methods: Nodal and Mesh Analysis",
     ["When simplification runs out, you need a method that works every time.",
      "Nodal and mesh analysis turn any linear circuit into a set of simultaneous equations, and Part Four shows you how to write and solve them without fear."],
     [10, 11, 12]),
    ("Five", "The Great Network Theorems",
     ["Superposition, Thévenin and Norton are the theorems that let engineers think about circuits in big, useful pieces.",
      "Part Five explains them carefully, proves why they work and shows how to use them in practice."],
     [13, 14, 15]),
    ("Six", "Putting It All Together",
     ["The final part brings everything together: maximum power transfer, a strategy for choosing the right method, and the real world of components, measurements and fault-finding."],
     [16, 17, 18]),
]

CHAPTERS = {
    1: ("What Electricity Really Is: Charge, Current and Voltage", "Charge, Current and Voltage"),
    2: ("Resistance, Power and Energy", "Resistance, Power and Energy"),
    3: ("Ohm’s Law in Practice", "Ohm’s Law in Practice"),
    4: ("Reading Circuits: Components, Sources and Diagrams", "Reading Circuits"),
    5: ("Kirchhoff’s Current and Voltage Laws", "Kirchhoff’s Laws"),
    6: ("Series and Parallel Circuits", "Series and Parallel Circuits"),
    7: ("Series–Parallel Networks and Equivalent Resistance", "Series–Parallel Networks"),
    8: ("Dividers, Bridges and the Loading Effect", "Dividers, Bridges and Loading"),
    9: ("Delta–Star Transformations", "Delta–Star Transformations"),
    10: ("Nodal Analysis", "Nodal Analysis"),
    11: ("Mesh Analysis", "Mesh Analysis"),
    12: ("Supernodes, Supermeshes and Dependent Sources", "Supernodes, Supermeshes and Dependent Sources"),
    13: ("Linearity and the Superposition Theorem", "Superposition"),
    14: ("Thévenin’s Theorem", "Thévenin’s Theorem"),
    15: ("Norton’s Theorem and Source Transformation", "Norton’s Theorem"),
    16: ("Maximum Power Transfer", "Maximum Power Transfer"),
    17: ("Choosing the Right Method: A Problem-Solving Strategy", "Choosing the Right Method"),
    18: ("Real Circuits: Measurement, Fault-Finding and the Road Ahead", "Real Circuits"),
}

FRONT = [("preface", "Preface"), ("howto", "How to Use This Book")]
BACK = [("appA", "Appendix A: Units, Symbols and the Resistor Colour Code"),
        ("appB", "Appendix B: Mathematics Toolkit – Solving Simultaneous Equations"),
        ("appC", "Appendix C: Answers to Exercises"),
        ("appD", "Appendix D: Formula Summary"),
        ("glossary", "Glossary"),
        ("about", "About the Author")]

FRAC = re.compile(r"\{\{frac\|([^|{}]+)\|([^{}]+?)\}\}")


MAT = re.compile(r"\{\{mat\|([^{}]+?)\}\}")


def _mat(m):
    rows = [r.split(",") for r in m.group(1).split(";")]
    body = "".join("<tr>" + "".join(f"<td>{c.strip()}</td>" for c in r) + "</tr>" for r in rows)
    return f'<span class="mtx"><table>{body}</table></span>'


def prep(md):
    """Expand the manuscript's small macros into inline HTML."""
    md = MAT.sub(_mat, md)
    return FRAC.sub(lambda m: f'<span class="frac"><span class="num">{m.group(1).strip()}</span><span class="den">{m.group(2).strip()}</span></span>', md)


def read(name):
    p = os.path.join(MS, name + ".md")
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as f:
        return f.read()


def md2html(md):
    r = subprocess.run(["pandoc", "-f", "markdown+subscript+superscript+fenced_divs+pipe_tables+smart",
                        "-t", "html5", "--wrap=none"], input=prep(md), capture_output=True, text=True, check=True)
    return r.stdout


def answers_md():
    parts = []
    for n in CHAPTERS:
        a = read(f"answers/ch{n:02d}")
        if a:
            parts.append(f"## Chapter {n}: {CHAPTERS[n][1]}\n\n{a}\n")
    return "\n".join(parts)


def chapter_ids():
    return [n for n in CHAPTERS if read(f"ch{n:02d}") is not None]


# ---------------------------------------------------------------- PDF
def build_pdf():
    have = chapter_ids()
    out = []
    out.append('<section class="cover"><img src="cover/cover.png" alt="cover"/></section>')
    out.append(f'<section class="halftitle"><h1>{TITLE}</h1></section>')
    out.append(f'''<section class="titlepage"><p class="t1">{TITLE}</p>
<p class="t2">{SUBTITLE}</p><div class="rule"></div>
<p class="author">MARCUS J. THORNTON, PH.D.</p></section>''')
    out.append('<section class="copyright">' + md2html(read("copyright")) + '</section>')
    out.append('<section class="dedication">' + md2html(read("dedication")) + '</section>')
    # contents
    toc = ['<section class="toc"><h2>Contents</h2><ul>']
    for key, t in FRONT:
        toc.append(f'<li class="toc-fm"><a href="#{key}">{t}</a></li>')
    for num, ptitle, _, chs in PARTS:
        chs = [c for c in chs if c in have]
        if not chs:
            continue
        toc.append(f'<li class="toc-part"><a href="#part{num}">Part {num} · {ptitle}</a></li>')
        for c in chs:
            toc.append(f'<li class="toc-ch"><a href="#ch{c}"><span class="n">{c}</span>{CHAPTERS[c][0]}</a></li>')
    toc.append('<li class="toc-part"><a href="#back">Reference</a></li>')
    for key, t in BACK:
        if key == "appC" or read(key) is not None:
            toc.append(f'<li class="toc-fm"><a href="#{key}">{t}</a></li>')
    toc.append('</ul></section>')
    out.append("".join(toc))
    for key, t in FRONT:
        md = read(key)
        if md:
            out.append(f'<section class="frontsec" id="{key}"><h1>{t}</h1>' + md2html(md) + '</section>')
    first_main = True
    for num, ptitle, intro, chs in PARTS:
        chs = [c for c in chs if c in have]
        if not chs:
            continue
        cls = "part mainstart" if first_main else "part"
        first_main = False
        intro_html = "".join(f"<p>{html.escape(p)}</p>" for p in intro)
        chlist = "<br/>".join(f"Chapter {c} · {html.escape(CHAPTERS[c][1])}" for c in chs)
        out.append(f'<section class="{cls}" id="part{num}"><div class="pnum">Part {num}</div><h1>{ptitle}</h1>'
                   f'<div class="prule"></div><div class="pintro">{intro_html}</div><div class="pchaps">{chlist}</div></section>')
        out.append('<div class="part-blank"></div>')
        for c in chs:
            body = md2html(read(f"ch{c:02d}"))
            body = re.sub(r"^<p>(\W*)(\w)", r'<p class="first">\1<span class="dropcap">\2</span>', body, count=1)
            title, short = CHAPTERS[c]
            out.append(f'<section class="chapter" id="ch{c}"><div class="chapter-head" data-short="{html.escape(short)}">'
                       f'<div class="cbig">{c}</div><div class="cnum">Chapter {c}</div><h1>{title}</h1><div class="crule"></div></div>'
                       f'<div class="body">{body}</div></section>')
    first_back = True
    for key, t in BACK:
        md = answers_md() if key == "appC" else read(key)
        if not md:
            continue
        extra = ' id="back"' if first_back else ''
        first_back = False
        if extra:
            out.append(f'<div{extra}></div>')
        cls = "backsec glossary" if key == "glossary" else "backsec"
        out.append(f'<section class="{cls}" id="{key}"><h1>{t}</h1>' + md2html(md) + '</section>')
    doc = f'''<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8"/><title>{TITLE}</title>
<meta name="author" content="{AUTHOR}"/><meta name="description" content="{SUBTITLE}"/>
<link rel="stylesheet" href="style/print.css"/></head><body>{"".join(out)}</body></html>'''
    hp = os.path.join(HERE, "book_print.html")
    with open(hp, "w", encoding="utf-8") as f:
        f.write(doc)
    from weasyprint import HTML
    pdf = os.path.join(OUT, "Circuit_Analysis_Made_Simple_Marcus_J_Thornton.pdf")
    doc = HTML(hp, base_url=HERE).render()
    print("PDF pages:", len(doc.pages))
    doc.write_pdf(pdf)
    return pdf


# ---------------------------------------------------------------- EPUB
def shift(md, by=1):
    out, fence = [], False
    for line in md.splitlines():
        if line.startswith("```"):
            fence = not fence
        if not fence and re.match(r"^#{1,5} ", line):
            line = "#" * by + line
        out.append(line)
    return "\n".join(out)


def build_epub():
    have = chapter_ids()
    parts = []
    for key, t in FRONT:
        md = read(key)
        if md:
            parts.append(f"# {t} {{.unnumbered}}\n\n{shift(md)}\n")
    for num, ptitle, intro, chs in PARTS:
        chs = [c for c in chs if c in have]
        if not chs:
            continue
        parts.append(f"# Part {num}: {ptitle} {{.unnumbered .part}}\n\n" + "\n\n".join(f"*{p}*" for p in intro) + "\n")
        for c in chs:
            parts.append(f"## Chapter {c} · {CHAPTERS[c][0]} {{.unnumbered}}\n\n{shift(read(f'ch{c:02d}'), 1)}\n")
    parts.append("# Reference {.unnumbered}\n\n")
    for key, t in BACK:
        md = answers_md() if key == "appC" else read(key)
        if md:
            parts.append(f"## {t} {{.unnumbered}}\n\n{shift(md, 1)}\n")
    md = prep("\n\n".join(parts))
    md = re.sub(r"\(fig/([\w\-]+)\.svg\)", r"(fig/\1.png)", md)
    src = os.path.join(HERE, "book_epub.md")
    with open(src, "w", encoding="utf-8") as f:
        f.write(md)
    meta = os.path.join(HERE, "epub_meta.yaml")
    with open(meta, "w", encoding="utf-8") as f:
        f.write(f'''---
title:
- type: main
  text: "{TITLE}"
- type: subtitle
  text: "{SUBTITLE}"
creator:
- role: author
  text: "{AUTHOR}"
lang: en-GB
rights: "Copyright © 2026 Marcus J. Thornton. All rights reserved."
subject: "Electrical engineering; Circuit analysis; Electronics"
description: "{SUBTITLE}. A problem-solving textbook for beginners."
...
''')
    epub = os.path.join(OUT, "Circuit_Analysis_Made_Simple_Marcus_J_Thornton.epub")
    subprocess.run(["pandoc", meta, src, "-f", "markdown+subscript+superscript+fenced_divs+pipe_tables+smart",
                    "-o", epub, "--toc", "--toc-depth=2", "--split-level=2",
                    "--css", os.path.join(HERE, "style", "epub.css"),
                    "--epub-cover-image", os.path.join(HERE, "cover", "cover.png"),
                    "--epub-title-page=true",
                    "--resource-path", HERE], check=True, cwd=HERE)
    return epub


if __name__ == "__main__":
    what = sys.argv[1:] or ["pdf", "epub"]
    if "pdf" in what:
        print(build_pdf())
    if "epub" in what:
        print(build_epub())
