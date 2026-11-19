"""Three alternative front covers (1600 x 2286 px, matching the 7 x 10 in trim)."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath
from matplotlib.patches import PathPatch, Circle, Rectangle, FancyBboxPatch, Polygon
from matplotlib.transforms import Affine2D
from matplotlib.colors import LinearSegmentedColormap

OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
G = "/usr/share/texmf/fonts/opentype/public/tex-gyre/"
CN = FontProperties(fname=G + "texgyreheroscn-bold.otf")
CNR = FontProperties(fname=G + "texgyreheroscn-regular.otf")
HB = FontProperties(fname=G + "texgyreheros-bold.otf")
HR = FontProperties(fname=G + "texgyreheros-regular.otf")
PB = FontProperties(fname=G + "texgyrepagella-bold.otf")
PR = FontProperties(fname=G + "texgyrepagella-regular.otf")
PI = FontProperties(fname=G + "texgyrepagella-italic.otf")
GB = FontProperties(fname="/usr/share/fonts/truetype/ebgaramond/EBGaramond12-Bold.ttf")
GI = FontProperties(fname="/usr/share/fonts/truetype/ebgaramond/EBGaramond12-Italic.ttf")

W, H = 7.0, 10.0
DPI = 228.6


def canvas(bg):
    fig = plt.figure(figsize=(W, H), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), W, H, fc=bg, ec="none", zorder=0))
    return fig, ax


def fit_text(ax, s, fp, x, y, width, color="black", ha="center", zorder=5, max_h=None, spacing=0.0):
    """Draw text as a path scaled to an exact width (in inches) — true display typography."""
    tp = TextPath((0, 0), s, size=1, prop=fp)
    bb = tp.get_extents()
    sc = width / bb.width
    if max_h and bb.height * sc > max_h:
        sc = max_h / bb.height
    w = bb.width * sc
    x0 = {"center": x - w / 2, "left": x, "right": x - w}[ha]
    tr = Affine2D().translate(-bb.x0, 0).scale(sc).translate(x0, y)
    p = PathPatch(tr.transform_path(tp), fc=color, ec="none", zorder=zorder)
    ax.add_patch(p)
    return p, bb.height * sc


def gradient_fill(ax, patch, cmap, extent, zorder=6, vertical=True):
    g = np.linspace(0, 1, 256).reshape(-1, 1) if vertical else np.linspace(0, 1, 256).reshape(1, -1)
    im = ax.imshow(g, extent=extent, cmap=cmap, aspect="auto", origin="lower", zorder=zorder)
    im.set_clip_path(patch)
    patch.set_facecolor("none")


def text(ax, x, y, s, fp, size, color, ha="center", va="center", ls=None, z=6, **kw):
    return ax.text(x, y, s, fontproperties=fp, fontsize=size, color=color, ha=ha, va=va, zorder=z, **kw)


def spaced(s, n=1):
    return (" " * n).join(list(s))


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=DPI, pad_inches=0)
    plt.close(fig)


# ===================================================================== A: BOLD CLASSIC
def cover_a():
    RED, INKC, CREAM = "#B3261E", "#111111", "#F3EEE4"
    fig, ax = canvas(CREAM)
    # subtle paper vignette
    yy, xx = np.mgrid[0:1:300j, 0:1:210j]
    v = ((xx - 0.5) ** 2 + (yy - 0.55) ** 2)
    ax.imshow(v, extent=[0, W, 0, H], cmap=LinearSegmentedColormap.from_list("v", [(1, 1, 1, 0), (0.55, 0.45, 0.3, 0.16)]),
              origin="lower", zorder=1, aspect="auto")
    # top line
    text(ax, W / 2, 9.45, "THE  COMPLETE  STUDY  GUIDE   •   2026 – 2027  EDITION", HB, 11.5, INKC)
    ax.plot([0.6, 6.4], [9.18, 9.18], color=INKC, lw=1.2, zorder=5)
    # giant title
    fit_text(ax, "ELECTRICAL", CN, W / 2, 7.72, 6.0, INKC)
    fit_text(ax, "ENGINEERING", CN, W / 2, 6.42, 6.0, INKC)
    fit_text(ax, "FE EXAM PREP", CN, W / 2, 4.95, 6.0, RED)
    # sine line art with phasor
    t = np.linspace(0.6, 6.4, 600)
    ax.plot(t, 4.42 + 0.17 * np.sin(2 * np.pi * (t - 0.6) / 1.45), color=RED, lw=2.4, zorder=5)
    ax.plot(t, 4.42 + 0.17 * np.sin(2 * np.pi * (t - 0.6) / 1.45 - 2.1), color=INKC, lw=1.0, alpha=0.55, zorder=5)
    # subtitle
    text(ax, W / 2, 3.72, "800 Practice Questions, Formulas, and Mock Exams", GI, 21, INKC)
    text(ax, W / 2, 3.33, "to Pass First Time", GI, 21, INKC)
    # badge
    ax.add_patch(Circle((5.72, 2.42), 0.62, fc=RED, ec="none", zorder=6))
    ax.add_patch(Circle((5.72, 2.42), 0.55, fc="none", ec=CREAM, lw=1.2, zorder=7))
    text(ax, 5.72, 2.58, "800", CN, 25, CREAM, z=8)
    text(ax, 5.72, 2.22, "QUESTIONS\nSOLVED", HB, 6.8, CREAM, z=8, linespacing=1.05)
    text(ax, 0.62, 2.62, "Includes two full-length mock exams,", PI, 13, "#333333", ha="left")
    text(ax, 0.62, 2.30, "every formula you need and", PI, 13, "#333333", ha="left")
    text(ax, 0.62, 1.98, "Reference Handbook strategies", PI, 13, "#333333", ha="left")
    # author
    ax.plot([0.6, 6.4], [1.42, 1.42], color=INKC, lw=1.2, zorder=5)
    fit_text(ax, "MARCUS J. THORNTON, PH.D.", CN, W / 2, 0.55, 5.6, INKC)
    save(fig, "cover_A_bold_classic.png")


# ===================================================================== B: MIDNIGHT GOLD
def cover_b():
    BLACK = "#07090F"
    fig, ax = canvas(BLACK)
    # radial glow
    yy, xx = np.mgrid[0:1:400j, 0:1:280j]
    r = np.sqrt((xx - 0.5) ** 2 + ((yy - 0.47) * 1.3) ** 2)
    glow = np.clip(1 - r / 0.75, 0, 1) ** 2
    ax.imshow(glow, extent=[0, W, 0, H], origin="lower", aspect="auto", zorder=1,
              cmap=LinearSegmentedColormap.from_list("g", [(0.03, 0.04, 0.07, 0), (0.16, 0.20, 0.34, 0.9)]))
    gold = LinearSegmentedColormap.from_list("gold", ["#8C6420", "#E9C46A", "#FFF1C1", "#D4A440", "#8C6420"])
    # top
    text(ax, W / 2, 9.38, spaced("2026–2027 EDITION"), PR, 12.5, "#D9B65C")
    ax.plot([2.3, 4.7], [9.1, 9.1], color="#D9B65C", lw=0.8, zorder=5)
    # title in gold gradient serif caps
    p1, h1 = fit_text(ax, "ELECTRICAL", PB, W / 2, 7.95, 5.9)
    gradient_fill(ax, p1, gold, [0.5, 6.5, 7.9, 8.85])
    p2, h2 = fit_text(ax, "ENGINEERING", PB, W / 2, 6.95, 5.9)
    gradient_fill(ax, p2, gold, [0.5, 6.5, 6.9, 7.85])
    fit_text(ax, "F E   E X A M   P R E P", PB, W / 2, 6.15, 5.3, "#F4F1EA")
    # oscilloscope emblem
    cx, cy, R = W / 2, 4.25, 1.2
    ax.add_patch(Circle((cx, cy), R + 0.07, fc="none", ec="#D9B65C", lw=2.0, zorder=5))
    ax.add_patch(Circle((cx, cy), R, fc="#0D1424", ec="#5A4520", lw=1, zorder=5))
    for k in np.linspace(-R, R, 9)[1:-1]:
        hh = np.sqrt(R * R - k * k)
        ax.plot([cx + k, cx + k], [cy - hh, cy + hh], color="#2A3550", lw=0.6, zorder=6)
        ax.plot([cx - hh, cx + hh], [cy + k, cy + k], color="#2A3550", lw=0.6, zorder=6)
    t = np.linspace(-R * 0.96, R * 0.96, 500)
    y = 0.62 * np.sin(2 * np.pi * t / 1.25) * np.exp(-0.0 * t)
    for lw, al in [(9, 0.06), (5, 0.12), (2.6, 0.35), (1.3, 1.0)]:
        ax.plot(cx + t, cy + y, color="#FFD77A", lw=lw, alpha=al, zorder=7, solid_capstyle="round")
    y2 = 0.42 * np.sin(2 * np.pi * t / 1.25 - 1.4)
    ax.plot(cx + t, cy + y2, color="#7FB2FF", lw=1.1, alpha=0.75, zorder=7)
    text(ax, W / 2, 2.62, "The Complete Study Guide", GI, 24, "#F4F1EA")
    text(ax, W / 2, 2.18, spaced("800 PRACTICE QUESTIONS  ·  2 MOCK EXAMS  ·  EVERY FORMULA"), PR, 8.2, "#D9B65C")
    ax.plot([1.1, 5.9], [1.82, 1.82], color="#3A3420", lw=0.8, zorder=5)
    text(ax, W / 2, 1.5, "Pass First Time", PI, 15, "#C9C3B4")
    p3, _ = fit_text(ax, "MARCUS J. THORNTON, PH.D.", PB, W / 2, 0.55, 5.0)
    gradient_fill(ax, p3, gold, [1.0, 6.0, 0.5, 0.95])
    save(fig, "cover_B_midnight_gold.png")


# ===================================================================== C: ELECTRIC
def cover_c():
    NAVY, BLUE1, BLUE2, AMBER, WHITE = "#0A1F44", "#0B3D91", "#1565C0", "#FFC233", "#FFFFFF"
    fig, ax = canvas(WHITE)
    # blue top block with gradient
    g = np.linspace(0, 1, 256).reshape(-1, 1)
    ax.imshow(g, extent=[0, W, 4.1, H], origin="lower", aspect="auto", zorder=1,
              cmap=LinearSegmentedColormap.from_list("b", [BLUE1, "#0E4FB3", BLUE2]))
    # faint grid on blue
    for x in np.arange(0, W, 0.35):
        ax.plot([x, x], [4.1, H], color="white", lw=0.4, alpha=0.06, zorder=2)
    for y in np.arange(4.1, H, 0.35):
        ax.plot([0, W], [y, y], color="white", lw=0.4, alpha=0.06, zorder=2)
    text(ax, W / 2, 9.45, spaced("2026 – 2027  EDITION"), HB, 12, AMBER)
    fit_text(ax, "ELECTRICAL", CN, W / 2, 7.85, 6.1, WHITE)
    fit_text(ax, "ENGINEERING", CN, W / 2, 6.6, 6.1, WHITE)
    fit_text(ax, "FE EXAM PREP", CN, W / 2, 5.25, 6.1, AMBER)
    text(ax, W / 2, 4.72, "The Complete Study Guide", PI, 22, WHITE)
    # diagonal amber band
    ax.add_patch(Polygon([(0, 3.62), (W, 4.02), (W, 4.42), (0, 4.02)], fc=AMBER, ec="none", zorder=4))
    ax.add_patch(Polygon([(0, 3.52), (W, 3.92), (W, 4.02), (0, 3.62)], fc=NAVY, ec="none", zorder=4))
    tx = ax.text(W / 2, 4.02, spaced("PASS  FIRST  TIME"), fontproperties=HB, fontsize=17, color=NAVY,
                 ha="center", va="center", rotation=np.degrees(np.arctan(0.4 / W)), zorder=6)
    # circuit line art (RLC with source) in navy
    lw = 2.2
    def res(x0, y0, x1):
        xs = np.linspace(x0, x1, 13); ys = [y0] + [y0 + (0.09 if i % 2 else -0.09) for i in range(1, 12)] + [y0]
        ax.plot(xs, ys, color=NAVY, lw=lw, zorder=6)
    def ind(x0, y0, x1):
        n = 4; w = (x1 - x0) / n
        for i in range(n):
            th = np.linspace(np.pi, 0, 30)
            ax.plot(x0 + w * i + w / 2 + w / 2 * np.cos(th), y0 + 0.13 * np.sin(th), color=NAVY, lw=lw, zorder=6)
    yT, yB = 3.0, 1.95
    ax.plot([1.0, 1.0], [yB, 2.25], color=NAVY, lw=lw, zorder=6); ax.plot([1.0, 1.0], [2.7, yT], color=NAVY, lw=lw, zorder=6)
    ax.add_patch(Circle((1.0, 2.475), 0.225, fc=WHITE, ec=NAVY, lw=lw, zorder=6))
    t = np.linspace(-0.13, 0.13, 50); ax.plot(1.0 + t, 2.475 + 0.07 * np.sin(t / 0.13 * np.pi), color=NAVY, lw=1.6, zorder=7)
    ax.plot([1.0, 1.6], [yT, yT], color=NAVY, lw=lw, zorder=6); res(1.6, yT, 2.6)
    ax.plot([2.6, 3.0], [yT, yT], color=NAVY, lw=lw, zorder=6); ind(3.0, yT, 4.1)
    ax.plot([4.1, 4.6], [yT, yT], color=NAVY, lw=lw, zorder=6)
    ax.plot([4.6, 4.6], [yT, 2.53], color=NAVY, lw=lw, zorder=6)
    ax.plot([4.35, 4.85], [2.53, 2.53], color=NAVY, lw=lw, zorder=6); ax.plot([4.35, 4.85], [2.42, 2.42], color=NAVY, lw=lw, zorder=6)
    ax.plot([4.6, 4.6], [2.42, yB], color=NAVY, lw=lw, zorder=6); ax.plot([1.0, 4.6], [yB, yB], color=NAVY, lw=lw, zorder=6)
    for x0 in (4.6,):
        ax.plot([x0, 5.4], [yT, yT], color=NAVY, lw=lw, zorder=6)
    ax.add_patch(Circle((5.45, yT), 0.05, fc=WHITE, ec=NAVY, lw=1.6, zorder=7))
    # stats column
    for i, (big, small) in enumerate([("800", "PRACTICE QUESTIONS"), ("2", "FULL MOCK EXAMS"), ("100%", "WORKED SOLUTIONS")]):
        y = 3.05 - i * 0.52
        text(ax, 6.55, y + 0.02, big, CN, 22, BLUE1, ha="right")
        text(ax, 6.55, y - 0.21, small, HB, 7.2, NAVY, ha="right")
    # author bar
    ax.add_patch(Rectangle((0, 0), W, 1.25, fc=NAVY, ec="none", zorder=4))
    fit_text(ax, "MARCUS J. THORNTON, PH.D.", CN, W / 2, 0.42, 5.4, WHITE)
    save(fig, "cover_C_electric.png")


if __name__ == "__main__":
    cover_a()
    cover_b()
    cover_c()
    from PIL import Image, ImageDraw, ImageFont
    names = ["cover_A_bold_classic.png", "cover_B_midnight_gold.png", "cover_C_electric.png"]
    ims = [Image.open(os.path.join(OUT, n)).convert("RGB").resize((560, 800)) for n in names]
    sheet = Image.new("RGB", (560 * 3 + 80, 880), "#E8E8E8")
    f = ImageFont.truetype(G + "texgyreheros-bold.otf", 24)
    d = ImageDraw.Draw(sheet)
    for i, (im, lab) in enumerate(zip(ims, ["A  Bold Classic", "B  Midnight Gold", "C  Electric"])):
        sheet.paste(im, (20 + i * 580, 20))
        d.text((20 + i * 580 + 280, 848), lab, fill="#222222", font=f, anchor="mm")
    sheet.save(os.path.join(OUT, "cover_comparison.png"))
    print("done")
