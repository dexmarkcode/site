"""Three 6 x 9 in cover designs for the Electric Circuits Workbook.

    python3 make_covers.py   ->  cover_1_*.png/pdf, cover_2_*, cover_3_*
"""
import math
import os
import random
import subprocess

from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(os.path.dirname(HERE), "fonts")
OUT = os.path.join(HERE, "output")
os.makedirs(OUT, exist_ok=True)

TITLE_A, TITLE_B = "Electric Circuits", "Workbook"
SUB = "800 Practice Problems With Step-by-Step Solutions for Circuit Analysis, Exams, and Self-Study"
AUTHOR = "Marcus J. Thornton, PhD"

FACES = f"""
@font-face {{ font-family: "EBG"; src: url("file://{FONTS}/EBGaramond-400.ttf"); font-weight: 400; }}
@font-face {{ font-family: "EBG"; src: url("file://{FONTS}/EBGaramond-400i.ttf"); font-style: italic; }}
@font-face {{ font-family: "EBG"; src: url("file://{FONTS}/EBGaramond-600.ttf"); font-weight: 600; }}
@font-face {{ font-family: "EBG"; src: url("file://{FONTS}/EBGaramond-700.ttf"); font-weight: 700; }}
@font-face {{ font-family: "Corm"; src: url("file://{FONTS}/CormorantGaramond-600.ttf"); font-weight: 600; }}
@font-face {{ font-family: "Corm"; src: url("file://{FONTS}/CormorantGaramond-700.ttf"); font-weight: 700; }}
@page {{ size: 6in 9in; margin: 0; }}
html, body {{ margin: 0; padding: 0; }}
.c {{ position: relative; width: 6in; height: 9in; overflow: hidden; }}
.abs {{ position: absolute; }}
"""


# --------------------------------------------------------------------------
# SVG helpers (coordinates in a 600 x 900 box = 6 x 9 in)
# --------------------------------------------------------------------------
def resistor(x, y, length, vertical=False, amp=9, n=6):
    """Zig-zag resistor path from (x,y) along +x (or +y)."""
    lead = length * 0.25
    body = length - 2 * lead
    step = body / (2 * n)
    pts = [(0, 0), (lead, 0)]
    for k in range(2 * n):
        pts.append((lead + step * (k + 0.5), amp if k % 2 == 0 else -amp))
    pts += [(lead + body, 0), (length, 0)]
    if vertical:
        pts = [(-b, a) for a, b in pts]
    return "M" + " L".join(f"{x + a:.1f},{y + b:.1f}" for a, b in pts)


def inductor(x, y, length, loops=4, r=None):
    lead = length * 0.2
    body = length - 2 * lead
    r = r or body / (2 * loops)
    d = f"M{x},{y} L{x + lead},{y}"
    cx = x + lead
    for _ in range(loops):
        d += f" A{r},{r} 0 0 1 {cx + 2 * r},{y}"
        cx += 2 * r
    d += f" L{x + length},{y}"
    return d


def capacitor(x, y, length, gap=10, plate=26):
    m = x + length / 2
    return (f"M{x},{y} L{m - gap / 2},{y} M{m - gap / 2},{y - plate / 2} L{m - gap / 2},{y + plate / 2} "
            f"M{m + gap / 2},{y - plate / 2} L{m + gap / 2},{y + plate / 2} M{m + gap / 2},{y} L{x + length},{y}")


def write(name, html_body, css):
    fc = FontConfiguration()
    pdf = os.path.join(OUT, name + ".pdf")
    HTML(string=f"<html><body>{html_body}</body></html>").write_pdf(
        pdf, stylesheets=[CSS(string=FACES + css, font_config=fc)], font_config=fc)
    subprocess.run(["pdftoppm", "-png", "-r", "300", "-singlefile", pdf, os.path.join(OUT, name)], check=True)
    subprocess.run(["pdftoppm", "-jpeg", "-jpegopt", "quality=92", "-r", "300", "-singlefile", pdf, os.path.join(OUT, name)], check=True)
    print("wrote", name)


# --------------------------------------------------------------------------
# Design 1: "Midnight Schematic" — navy, classic serif, copper circuit art
# --------------------------------------------------------------------------
def cover1():
    stroke = "#D9A066"
    paths = []
    # a real, readable two-mesh circuit drawn large across the middle
    y_top, y_bot = 470, 650
    paths.append(f'<circle cx="95" cy="{(y_top + y_bot) / 2}" r="26" fill="none" stroke="{stroke}" stroke-width="3"/>')
    paths.append(f'<text x="86" y="{(y_top + y_bot) / 2 - 4}" fill="{stroke}" font-size="22" font-family="EBG">+</text>')
    paths.append(f'<text x="88" y="{(y_top + y_bot) / 2 + 18}" fill="{stroke}" font-size="22" font-family="EBG">−</text>')
    segs = [
        f"M95,{y_top} L95,{(y_top + y_bot) / 2 - 26}", f"M95,{(y_top + y_bot) / 2 + 26} L95,{y_bot}",
        resistor(95, y_top, 190), inductor(285, y_top, 140), capacitor(425, y_top, 80),
        f"M505,{y_top} L505,{y_top + 20}", resistor(505, y_top + 20, 140, vertical=True),
        f"M505,{y_top + 160} L505,{y_bot}",
        f"M285,{y_top} L285,{y_top + 30}", resistor(285, y_top + 30, 120, vertical=True), f"M285,{y_top + 150} L285,{y_bot}",
        f"M95,{y_bot} L505,{y_bot}",
    ]
    for s in segs:
        paths.append(f'<path d="{s}" fill="none" stroke="{stroke}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>')
    for (cx, cy) in ((285, y_top), (285, y_bot)):
        paths.append(f'<circle cx="{cx}" cy="{cy}" r="6" fill="{stroke}"/>')
    # faint grid of traces behind
    r = random.Random(3)
    bg = []
    tries = 0
    while len(bg) < 26 and tries < 2000:
        tries += 1
        x, y = r.randrange(0, 600, 30), r.randrange(690, 770, 30)
        d = f"M{x},{y}"
        for _ in range(r.randint(2, 4)):
            if r.random() < 0.5:
                x += r.choice([-90, -60, 60, 90])
            else:
                y += r.choice([-60, -30, 30, 60])
            y = min(760, max(690, y))
            d += f" L{x},{y}"
        bg.append(f'<path d="{d}" fill="none" stroke="#3A5A82" stroke-width="1.6" stroke-opacity="0.55"/>'
                  f'<circle cx="{x}" cy="{y}" r="3.5" fill="#3A5A82" fill-opacity="0.8"/>')
    svg = f'<svg class="abs art" viewBox="0 0 600 900" xmlns="http://www.w3.org/2000/svg">{"".join(bg)}{"".join(paths)}</svg>'
    body = f"""<div class="c">{svg}
<div class="abs kicker">800 PROBLEMS &nbsp;·&nbsp; FULLY WORKED SOLUTIONS</div>
<div class="abs title"><span class="t1">{TITLE_A}</span><span class="t2">{TITLE_B}</span></div>
<div class="abs rule"></div>
<div class="abs sub">{SUB.replace("Self-Study", "Self&#8209;Study")}</div>
<div class="abs author">MARCUS J. THORNTON, PhD</div>
</div>"""
    css = """
.c { background: radial-gradient(ellipse at 50% 35%, #1B3557 0%, #0F2139 55%, #091526 100%); color: #F5EADB; }
.art { left: 0; top: 0; width: 6in; height: 9in; }
.kicker { top: 0.55in; left: 0; width: 6in; text-align: center; font-family: "EBG"; font-weight: 600; font-size: 9pt; letter-spacing: 0.32em; color: #D9A066; }
.title { top: 0.95in; left: 0.4in; width: 5.2in; text-align: center; }
.t1 { display: block; font-family: "Corm"; font-weight: 700; font-size: 50pt; line-height: 0.98; color: #FFF7EC; }
.t2 { display: block; font-family: "Corm"; font-weight: 600; font-size: 50pt; line-height: 1.0; color: #D9A066; font-style: normal; letter-spacing: 0.02em; }
.rule { top: 2.75in; left: 2.4in; width: 1.2in; height: 2px; background: #D9A066; }
.sub { top: 2.95in; left: 0.7in; width: 4.6in; text-align: center; font-family: "EBG"; font-style: italic; font-size: 13.5pt; line-height: 1.35; color: #E9DCC8; }
.author { bottom: 0.65in; left: 0; width: 6in; text-align: center; font-family: "EBG"; font-weight: 600; font-size: 17pt; letter-spacing: 0.24em; color: #FFF7EC; }
"""
    write("cover_1_midnight_schematic", body, css)


# --------------------------------------------------------------------------
# Design 2: "Bold Signal" — cream, huge sans title, orange disc with waveform
# --------------------------------------------------------------------------
def cover2():
    pts = []
    for k in range(0, 401):
        x = 100 + k
        t = k / 400 * 4 * math.pi
        y = 600 - 85 * math.sin(t)
        pts.append(f"{x:.1f},{y:.1f}")
    pts2 = []
    for k in range(0, 401):
        x = 100 + k
        t = k / 400 * 4 * math.pi
        y = 600 - 85 * math.sin(t - math.pi / 3) * 0.6
        pts2.append(f"{x:.1f},{y:.1f}")
    grid = "".join(f'<line x1="{x}" y1="430" x2="{x}" y2="770" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1"/>' for x in range(130, 480, 40))
    grid += "".join(f'<line x1="130" y1="{y}" x2="470" y2="{y}" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1"/>' for y in range(450, 760, 40))
    svg = f'''<svg class="abs art" viewBox="0 0 600 900" xmlns="http://www.w3.org/2000/svg">
<defs><clipPath id="disc"><circle cx="300" cy="600" r="175"/></clipPath></defs>
<circle cx="300" cy="600" r="175" fill="#E2552B"/>
<g clip-path="url(#disc)">{grid}
<polyline points="{" ".join(pts2)}" fill="none" stroke="#1B1B1B" stroke-width="3" stroke-opacity="0.55"/>
<polyline points="{" ".join(pts)}" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/></g>
<circle cx="300" cy="600" r="175" fill="none" stroke="#1B1B1B" stroke-width="3"/>
</svg>'''
    body = f"""<div class="c">{svg}
<div class="abs band">THE COMPLETE PRACTICE BOOK</div>
<div class="abs title">ELECTRIC<br/>CIRCUITS<br/><span>WORKBOOK</span></div>
<div class="abs num">800</div><div class="abs numlab">PRACTICE<br/>PROBLEMS</div>
<div class="abs sub">With Step-by-Step Solutions for Circuit Analysis, Exams, and Self&#8209;Study</div>
<div class="abs author">MARCUS J. THORNTON, PhD</div>
</div>"""
    css = """
.c { background: #F4EEE3; color: #1B1B1B; }
.art { left: 0; top: 0; width: 6in; height: 9in; }
.band { top: 0.45in; left: 0.5in; font-family: "Inter"; font-weight: 700; font-size: 9pt; letter-spacing: 0.3em; color: #E2552B; }
.title { top: 0.72in; left: 0.45in; width: 5.2in; font-family: "Inter"; font-weight: 900; font-size: 50pt; line-height: 0.92; letter-spacing: -0.01em; }
.title span { color: #E2552B; }
.num { top: 0.86in; right: 0.45in; font-family: "Inter"; font-weight: 900; font-size: 30pt; color: #1B1B1B; text-align: right; }
.numlab { top: 1.36in; right: 0.45in; font-family: "Inter"; font-weight: 700; font-size: 7.5pt; letter-spacing: 0.18em; text-align: right; line-height: 1.25; }
.sub { top: 3.12in; left: 0.5in; width: 5in; font-family: "EBG"; font-style: italic; font-size: 14pt; line-height: 1.3; color: #333; }
.author { bottom: 0.5in; left: 0.5in; width: 5in; font-family: "Inter"; font-weight: 700; font-size: 14pt; letter-spacing: 0.2em; border-top: 2.5px solid #1B1B1B; padding-top: 0.14in; }
"""
    write("cover_2_bold_signal", body, css)


# --------------------------------------------------------------------------
# Design 3: "Copper Oscilloscope" — charcoal, glowing damped waveform
# --------------------------------------------------------------------------
def cover3():
    def wave(amp_scale=1.0):
        pts = []
        for k in range(0, 561):
            x = 20 + k
            t = k / 560 * 7 * math.pi
            y = 560 - 120 * amp_scale * math.exp(-t / 9) * math.sin(t)
            pts.append(f"{x:.1f},{y:.1f}")
        return " ".join(pts)
    w = wave()
    glow = "".join(f'<polyline points="{w}" fill="none" stroke="#F0A35E" stroke-width="{sw}" stroke-opacity="{op}" stroke-linecap="round" stroke-linejoin="round"/>'
                   for sw, op in ((22, 0.05), (14, 0.08), (8, 0.15), (4, 0.6), (2, 1.0)))
    grid = "".join(f'<line x1="{x}" y1="380" x2="{x}" y2="740" stroke="#7A8590" stroke-opacity="{0.35 if x == 300 else 0.15}" stroke-width="1"/>' for x in range(20, 600, 56))
    grid += "".join(f'<line x1="0" y1="{y}" x2="600" y2="{y}" stroke="#7A8590" stroke-opacity="{0.35 if y == 560 else 0.15}" stroke-width="1"/>' for y in range(380, 760, 45))
    ticks = "".join(f'<line x1="{x}" y1="555" x2="{x}" y2="565" stroke="#7A8590" stroke-opacity="0.5"/>' for x in range(20, 600, 11))
    svg = f'<svg class="abs art" viewBox="0 0 600 900" xmlns="http://www.w3.org/2000/svg">{grid}{ticks}{glow}</svg>'
    body = f"""<div class="c">{svg}
<div class="abs top"><div class="t1">Electric Circuits</div><div class="t2">WORKBOOK</div></div>
<div class="abs sub">800 Practice Problems With Step-by-Step Solutions<br/>for Circuit Analysis, Exams, and Self-Study</div>
<div class="abs tags">DC &nbsp;·&nbsp; AC &nbsp;·&nbsp; TRANSIENTS &nbsp;·&nbsp; THÉVENIN &nbsp;·&nbsp; PHASORS &nbsp;·&nbsp; THREE-PHASE</div>
<div class="abs author">Marcus J. Thornton, PhD</div>
</div>"""
    css = """
.c { background: linear-gradient(180deg, #23272C 0%, #181B1F 60%, #121417 100%); color: #EFE7DC; }
.art { left: 0; top: 0; width: 6in; height: 9in; }
.top { top: 0.7in; left: 0.45in; width: 5.1in; }
.t1 { font-family: "Corm"; font-weight: 700; font-size: 48pt; line-height: 1.0; color: #F6EFE5; }
.t2 { font-family: "Inter"; font-weight: 800; font-size: 30pt; letter-spacing: 0.42em; color: #E8954E; margin-top: 0.08in; }
.sub { top: 2.4in; left: 0.45in; width: 5.1in; font-family: "EBG"; font-style: italic; font-size: 13pt; line-height: 1.35; color: #CFC5B8; border-left: 3px solid #E8954E; padding-left: 0.16in; }
.tags { top: 7.45in; left: 0; width: 6in; text-align: center; font-family: "Inter"; font-weight: 600; font-size: 7.5pt; letter-spacing: 0.2em; color: #9AA3AD; }
.author { bottom: 0.55in; left: 0; width: 6in; text-align: center; font-family: "Corm"; font-weight: 700; font-size: 24pt; letter-spacing: 0.04em; color: #F6EFE5; }
"""
    write("cover_3_copper_oscilloscope", body, css)


if __name__ == "__main__":
    cover1()
    cover2()
    cover3()
