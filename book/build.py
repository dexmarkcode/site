"""Assemble the Electric Circuits Workbook into PDF and EPUB.

    python3 build.py            # everything
"""
import html
import importlib
import os
import re
import subprocess
import sys
import uuid

import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "problems"))
from lib import FIGDIR  # noqa: E402

OUT = os.path.join(HERE, "output")
BUILD = os.path.join(HERE, "build")
os.makedirs(OUT, exist_ok=True)

TITLE = "Electric Circuits Workbook"
SUBTITLE = "800 Practice Problems With Step-by-Step Solutions for Circuit Analysis, Exams, and Self-Study"
AUTHOR = "Marcus J. Thornton, PhD"
YEAR = 2026

PARTS = [
    ("I", "Foundations of Circuit Analysis", [1, 2, 3],
     "Every circuit you will ever analyse obeys the same handful of rules. Part I builds them carefully: what current, voltage and power really are, how resistors combine, and the two laws named after Gustav Kirchhoff that hold the whole subject together. Take your time here. Most of the errors I see in final-year scripts started as small misunderstandings in this material."),
    ("II", "Systematic Methods and Network Theorems", [4, 5, 6],
     "Once circuits grow beyond a couple of loops, inspection and intuition stop being enough. Part II gives you two systematic methods, nodal and mesh analysis, that will solve any linear circuit if you follow them faithfully. It then adds the theorems that let you avoid solving most of the circuit at all."),
    ("III", "Energy Storage and Transient Response", [7, 8, 9],
     "Capacitors and inductors remember. Their present behaviour depends on what happened before, so circuits containing them respond to sudden changes with curves rather than jumps. Part III shows you how to predict those curves, first for one storage element, then for two, where the response may overshoot and ring."),
    ("IV", "Alternating Current and Power Systems", [10, 11, 12],
     "The mains supply, radio transmitters, audio amplifiers and most power electronics all deal in sinusoids. Part IV turns sinusoidal analysis back into algebra with phasors, explains what 'power' means once voltage and current fall out of step, and finishes with the three-phase systems that carry electricity across the country."),
]

CHAPTERS = {
    1: "Charge, Current, Voltage and Power",
    2: "Series and Parallel Resistive Networks",
    3: "Kirchhoff's Laws in Practice",
    4: "Nodal Analysis",
    5: "Mesh Analysis",
    6: "Network Theorems",
    7: "Capacitors and Inductors",
    8: "First-Order Transients: RC and RL Circuits",
    9: "Second-Order Circuits: RLC Response",
    10: "Sinusoids, Phasors and Impedance",
    11: "AC Power and Power Factor",
    12: "Three-Phase Circuits",
}

LEVELS = {1: ("Level 1", "Foundation", "Single-concept questions to build fluency and confidence."),
          2: ("Level 2", "Core Practice", "Multi-step problems of the kind set in most coursework and class tests."),
          3: ("Level 3", "Exam Standard", "Longer, less guided problems at the standard of end-of-year and professional examinations.")}
DOTS = {1: "●○○", 2: "●●○", 3: "●●●"}


# --------------------------------------------------------------------------
# Markdown with a few book-specific extensions
# --------------------------------------------------------------------------
class Ctx:
    def __init__(self, chap):
        self.chap = chap
        self.fig = 0
        self.ex = 0
        self.figs = []


def md(text):
    return markdown.markdown(text, extensions=["tables", "md_in_html", "attr_list", "sane_lists", "smarty"])


def figure_html(name, caption, label, epub, cls="tfig"):
    src = f"figs/{name}.png" if epub else f"file://{FIGDIR}/{name}.svg"
    cap = f'<figcaption><span class="flabel">{label}</span> {caption}</figcaption>' if label else ""
    return f'<figure class="{cls}"><img src="{src}" alt="{html.escape(caption or name)}"/>{cap}</figure>'


BOX_TITLES = {"example": "Worked Example", "tip": "From the Examiner's Desk", "pitfall": "Common Pitfall",
              "key": "Key Idea", "objectives": "In This Chapter", "lab": "On the Bench", "summary": "Chapter Summary"}


def render_prose(src, ctx, epub):
    # boxes
    out, buf, kind, title = [], [], None, None
    for line in src.split("\n"):
        m = re.match(r"^:::(\w+)\s*(.*)$", line)
        if m and kind is None:
            kind, title = m.group(1), m.group(2).strip()
            buf = []
            continue
        if line.strip() == ":::" and kind is not None:
            inner = render_inline("\n".join(buf), ctx, epub)
            head = BOX_TITLES.get(kind, kind.title())
            if kind == "example":
                ctx.ex += 1
                head = f"Worked Example {ctx.chap}.{ctx.ex}"
            t = f'<p class="boxhead">{head}{(": <span>" + title + "</span>") if title else ""}</p>'
            out.append(f'<div class="box {kind}">{t}{inner}</div>')
            kind = None
            continue
        if kind is not None:
            buf.append(line)
        else:
            out.append(line)
    return render_inline("\n".join(out), ctx, epub)


def render_inline(src, ctx, epub):
    def fig(m):
        ctx.fig += 1
        name, cap = m.group(1), m.group(2)
        return "\n\n" + figure_html(name, cap, f"Figure {ctx.chap}.{ctx.fig}", epub) + "\n\n"
    src = re.sub(r"\{\{fig:([\w]+)\|(.*?)\}\}", fig, src)

    def eq(m):
        body, tag = m.group(1).strip(), m.group(2)
        t = f'<span class="eqn">({tag})</span>' if tag else ""
        return f'\n<p class="eq">{body}{t}</p>\n'
    src = re.sub(r"^\$\$ (.*?)(?:\s*\|\|\s*([\d.]+))?$", eq, src, flags=re.M)
    return md(src)


# --------------------------------------------------------------------------
# Chapters
# --------------------------------------------------------------------------
def problems_html(ch, probs, epub):
    out = ['<section class="problems">', f'<h2 class="sec">Practice Problems for Chapter {ch}</h2>',
           '<p class="intro">Try each problem on paper before turning to the solution. The dots show the level: ●○○ foundation, ●●○ core practice, ●●● exam standard. Numerical answers are given to three or four significant figures; your own working may differ slightly in the last digit.</p>']
    cur = None
    for p in probs:
        if p.level != cur:
            cur = p.level
            a, b, c = LEVELS[cur]
            out.append(f'<h3 class="lvl">{a} <span>· {b}</span></h3><p class="lvlnote">{c}</p>')
        figh = figure_html(p.fig, "", "", epub, cls="pfig") if p.fig else ""
        out.append(f'<div class="prob" id="p{p.number.replace(".", "-")}"><p><span class="pnum">{p.number}</span><span class="dots">{DOTS[p.level]}</span> {p.text}</p>{figh}</div>')
    out.append("</section>")
    return "\n".join(out)


def solutions_html(ch, probs):
    out = ['<section class="solutions">', f'<h2 class="sec">Step-by-Step Solutions for Chapter {ch}</h2>']
    for p in probs:
        steps = "".join(f"<li>{s}</li>" for s in p.steps)
        out.append(f'<div class="sol"><p class="solhead"><span class="pnum">{p.number}</span> <span class="topic">{p.topic}</span></p><ol>{steps}</ol><p class="ans"><span>Answer</span> {p.answer}</p></div>')
    out.append("</section>")
    return "\n".join(out)


def chapter_html(ch, epub=False):
    mod = importlib.import_module(f"ch{ch:02d}")
    probs = mod.problems()
    src = open(os.path.join(HERE, "content", f"ch{ch:02d}.md"), encoding="utf-8").read()
    ctx = Ctx(ch)
    body = render_prose(src, ctx, epub)
    head = (f'<div class="chap-open"><p class="chap-num">Chapter {ch}</p>'
            f'<h1 class="chap-title">{CHAPTERS[ch]}</h1><div class="chap-rule"></div></div>')
    return (f'<section class="chapter" id="ch{ch}">{head}<div class="prose">{body}</div>'
            f'{problems_html(ch, probs, epub)}{solutions_html(ch, probs)}</section>'), len(probs)


def part_html(num, title, intro, chs):
    lst = "".join(f"<li><span>Chapter {c}</span> {CHAPTERS[c]}</li>" for c in chs)
    return (f'<section class="part" id="part{num}"><p class="part-num">Part {num}</p><h1 class="part-title">{title}</h1>'
            f'<div class="part-rule"></div><p class="part-intro">{intro}</p><ul class="part-list">{lst}</ul></section>')


def front_html(epub=False):
    fm = open(os.path.join(HERE, "content", "front.md"), encoding="utf-8").read()
    sections = re.split(r"^## ", fm, flags=re.M)[1:]
    parts = []
    for s in sections:
        title, body = s.split("\n", 1)
        sid = re.sub(r"\W+", "-", title.lower()).strip("-")
        parts.append(f'<section class="front" id="{sid}"><h1 class="front-title">{title}</h1>{render_prose(body, Ctx(0), epub)}</section>')
    return parts


def back_html(epub=False):
    bm = open(os.path.join(HERE, "content", "back.md"), encoding="utf-8").read()
    sections = re.split(r"^## ", bm, flags=re.M)[1:]
    out = []
    for s in sections:
        title, body = s.split("\n", 1)
        sid = re.sub(r"\W+", "-", title.lower()).strip("-")
        out.append(f'<section class="back" id="{sid}"><h1 class="front-title">{title}</h1>{render_prose(body, Ctx("A"), epub)}</section>')
    return out


def toc_html(front_titles, back_titles):
    rows = []
    for t in front_titles:
        sid = re.sub(r"\W+", "-", t.lower()).strip("-")
        rows.append(f'<li class="toc-front"><a href="#{sid}">{t}</a></li>')
    for num, title, chs, _ in PARTS:
        rows.append(f'<li class="toc-part"><a href="#part{num}">Part {num} · {title}</a></li>')
        for c in chs:
            rows.append(f'<li class="toc-ch"><a href="#ch{c}"><span class="tn">{c}</span>{CHAPTERS[c]}</a></li>')
    for t in back_titles:
        sid = re.sub(r"\W+", "-", t.lower()).strip("-")
        rows.append(f'<li class="toc-back"><a href="#{sid}">{t}</a></li>')
    return f'<section class="toc" id="contents"><h1 class="front-title">Contents</h1><ul>{"".join(rows)}</ul></section>'


def titles(path):
    return [re.match(r"^## (.*)$", l).group(1) for l in open(path, encoding="utf-8") if l.startswith("## ")]


# --------------------------------------------------------------------------
# PDF
# --------------------------------------------------------------------------
def build_pdf():
    from weasyprint import HTML
    css = open(os.path.join(HERE, "style", "print.css"), encoding="utf-8").read().replace("FONTDIR", os.path.join(HERE, "fonts"))
    ft, bt = titles(os.path.join(HERE, "content", "front.md")), titles(os.path.join(HERE, "content", "back.md"))
    body = []
    body.append(f'<section class="cover"><img src="file://{BUILD}/cover.png"/></section>')
    body.append(f'<section class="halftitle"><p class="ht">{TITLE}</p></section>')
    body.append(f'''<section class="titlepage"><p class="tp-title">Electric Circuits<br/>Workbook</p><div class="tp-rule"></div>
<p class="tp-sub">{SUBTITLE}</p><p class="tp-author">{AUTHOR}</p></section>''')
    body.append(open(os.path.join(HERE, "content", "copyright.html"), encoding="utf-8").read())
    body.append(open(os.path.join(HERE, "content", "dedication.html"), encoding="utf-8").read())
    body.append(toc_html(ft, bt))
    body.extend(front_html())
    total = 0
    first = True
    only = os.environ.get("ONLY")
    only = {int(x) for x in only.split(",")} if only else None
    for num, title, chs, intro in PARTS:
        if only:
            chs = [c for c in chs if c in only]
            if not chs:
                continue
        p = part_html(num, title, intro, chs)
        if first:
            p = p.replace('class="part"', 'class="part first-main"', 1)
            first = False
        body.append(p)
        for c in chs:
            h, n = chapter_html(c)
            total += n
            body.append(h)
            print(f"  chapter {c}: {n} problems", flush=True)
    body.extend(back_html())
    doc = f'<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8"/><title>{TITLE}</title></head><body>{"".join(body)}</body></html>'
    with open(os.path.join(BUILD, "book.html"), "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"total problems: {total}")
    from weasyprint import CSS
    from weasyprint.text.fonts import FontConfiguration
    fc = FontConfiguration()
    pdf = os.path.join(OUT, "Electric_Circuits_Workbook_Marcus_J_Thornton.pdf")
    HTML(string=doc, base_url=HERE).write_pdf(pdf, stylesheets=[CSS(string=css, font_config=fc)], font_config=fc)
    print("PDF:", pdf)
    return pdf


# --------------------------------------------------------------------------
# Cover
# --------------------------------------------------------------------------
def build_cover():
    from weasyprint import HTML, CSS
    css = open(os.path.join(HERE, "style", "cover.css"), encoding="utf-8").read().replace("FONTDIR", os.path.join(HERE, "fonts"))
    art = cover_art()
    doc = f'''<html><body><div class="c">{art}<div class="top"><p class="kicker">800 PRACTICE PROBLEMS · FULLY WORKED SOLUTIONS</p>
<p class="t1">Electric Circuits</p><p class="t2">Workbook</p><div class="rule"></div>
<p class="sub">800 Practice Problems With Step-by-Step Solutions<br/>for Circuit Analysis, Exams, and Self-Study</p></div>
<div class="bottom"><p class="feat">DC · Kirchhoff · Nodal &amp; Mesh · Thévenin &amp; Norton · Transients · RLC · Phasors · AC Power · Three-Phase</p>
<p class="auth">MARCUS J. THORNTON, PhD</p></div></div></body></html>'''
    pdf = os.path.join(BUILD, "cover.pdf")
    from weasyprint.text.fonts import FontConfiguration
    fc = FontConfiguration()
    HTML(string=doc).write_pdf(pdf, stylesheets=[CSS(string=css, font_config=fc)], font_config=fc)
    subprocess.run(["pdftoppm", "-png", "-r", "228", "-singlefile", pdf, os.path.join(BUILD, "cover")], check=True)
    return os.path.join(BUILD, "cover.png")


def cover_art():
    """Abstract circuit-trace artwork as inline SVG."""
    import random
    r = random.Random(7)
    lines = []
    for k in range(26):
        x = r.choice(range(40, 680, 40))
        y = r.choice(range(600, 860, 40))
        path = f"M{x},{y}"
        for _ in range(r.randint(2, 5)):
            if r.random() < 0.5:
                x = min(700, max(20, x + r.choice([-120, -80, 80, 120, 160])))
            else:
                y = min(860, max(580, y + r.choice([-80, -40, 40, 80])))
            path += f" L{x},{y}"
        lines.append(f'<path d="{path}" stroke="#B5651D" stroke-opacity="{r.uniform(0.25, 0.7):.2f}" stroke-width="3" fill="none"/>'
                     f'<circle cx="{x}" cy="{y}" r="7" fill="#0F2238" stroke="#D49A5E" stroke-width="3"/>')
    # a stylised resistor and capacitor
    lines.append('<path d="M60,720 L200,720 l15,-25 l30,50 l30,-50 l30,50 l30,-50 l30,50 l15,-25 L560,720" stroke="#E8C9A0" stroke-width="5" fill="none"/>')
    lines.append('<path d="M560,660 L560,780 M590,660 L590,780 M590,720 L700,720" stroke="#E8C9A0" stroke-width="5" fill="none"/>')
    return f'<svg class="art" viewBox="0 0 720 1080" xmlns="http://www.w3.org/2000/svg">{"".join(lines)}</svg>'


# --------------------------------------------------------------------------
# EPUB
# --------------------------------------------------------------------------
def build_epub():
    from ebooklib import epub
    book = epub.EpubBook()
    book.set_identifier("urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, "electric-circuits-workbook-thornton")))
    book.set_title(f"{TITLE}: {SUBTITLE}")
    book.set_language("en-GB")
    book.add_author("Marcus J. Thornton")
    book.add_metadata("DC", "publisher", "Marcus J. Thornton")
    book.add_metadata("DC", "description", "Eight hundred graded circuit-analysis problems with complete step-by-step solutions, from Ohm's law to three-phase power.")
    book.set_cover("cover.png", open(os.path.join(BUILD, "cover.png"), "rb").read())
    css = open(os.path.join(HERE, "style", "epub.css"), encoding="utf-8").read()
    ncss = epub.EpubItem(uid="style", file_name="style/book.css", media_type="text/css", content=css)
    book.add_item(ncss)
    for fn in ("EBGaramond-400.ttf", "EBGaramond-400i.ttf", "EBGaramond-600.ttf", "EBGaramond-600i.ttf", "CormorantGaramond-600.ttf"):
        book.add_item(epub.EpubItem(uid=fn, file_name=f"fonts/{fn}", media_type="font/ttf", content=open(os.path.join(HERE, "fonts", fn), "rb").read()))

    used = set()

    def page(fname, title, body):
        for m in re.findall(r'src="figs/([\w]+)\.png"', body):
            used.add(m)
        it = epub.EpubHtml(title=title, file_name=fname, lang="en-GB")
        it.content = f'<html xmlns="http://www.w3.org/1999/xhtml"><head><title>{html.escape(title)}</title></head><body>{body}</body></html>'
        it.add_item(ncss)
        book.add_item(it)
        return it

    spine, toc = ["nav"], []
    tp = page("title.xhtml", "Title Page", f'<section class="titlepage"><p class="tp-title">Electric Circuits Workbook</p><p class="tp-sub">{SUBTITLE}</p><p class="tp-author">{AUTHOR}</p></section>')
    spine.append(tp)
    cp = page("copyright.xhtml", "Copyright", open(os.path.join(HERE, "content", "copyright.html"), encoding="utf-8").read())
    spine.append(cp)
    dp = page("dedication.xhtml", "Dedication", open(os.path.join(HERE, "content", "dedication.html"), encoding="utf-8").read())
    spine.append(dp)
    for k, (t, h) in enumerate(zip(titles(os.path.join(HERE, "content", "front.md")), front_html(epub=True))):
        it = page(f"front{k}.xhtml", t, h)
        spine.append(it)
        toc.append(it)
    for num, title, chs, intro in PARTS:
        pi = page(f"part{num}.xhtml", f"Part {num}: {title}", part_html(num, title, intro, chs))
        spine.append(pi)
        sub = []
        for c in chs:
            h, _ = chapter_html(c, epub=True)
            ci = page(f"ch{c:02d}.xhtml", f"Chapter {c}: {CHAPTERS[c]}", h)
            spine.append(ci)
            sub.append(ci)
        toc.append((epub.Section(f"Part {num}: {title}", href=f"part{num}.xhtml"), sub))
    for k, (t, h) in enumerate(zip(titles(os.path.join(HERE, "content", "back.md")), back_html(epub=True))):
        it = page(f"back{k}.xhtml", t, h)
        spine.append(it)
        toc.append(it)
    for name in sorted(used):
        book.add_item(epub.EpubItem(uid="img_" + name, file_name=f"figs/{name}.png", media_type="image/png",
                                    content=open(os.path.join(FIGDIR, name + ".png"), "rb").read()))
    book.toc = toc
    book.spine = spine
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    path = os.path.join(OUT, "Electric_Circuits_Workbook_Marcus_J_Thornton.epub")
    epub.write_epub(path, book)
    print("EPUB:", path, f"({len(used)} images)")
    return path


if __name__ == "__main__":
    import figs_text
    figs_text.build_all()
    build_cover()
    build_pdf()
    if not os.environ.get("ONLY"):
        build_epub()
