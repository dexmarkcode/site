"""Three premium black-and-white front-cover options, 6 x 9 in at 300 dpi (1800 x 2700 px)."""
from common import *
from matplotlib.font_manager import FontProperties
from PIL import Image

OUT = ROOT / "covers"
OUT.mkdir(exist_ok=True)
DPI = 300
BLACK_FONT = FontProperties(fname="/usr/share/fonts/opentype/inter/InterDisplay-Black.otf")
JP_FONT = FontProperties(fname="/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf")
TITLE = "SANCHIN"
SUB = "Illustrated Textbook With Frame-by-Frame Diagrams, Testing Drills,\nPosture Corrections, and Strength Progressions\nfor the Foundational Form"
AUTHOR = "DR BEVERLY J. STIVERS"
rng = np.random.default_rng(7)


def new():
    fig = plt.figure(figsize=(6, 9), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 60); ax.set_ylim(0, 90); ax.axis("off")
    return fig, ax


def fit(fig, ax, x, y, s, width, ha="center", va="center", **kw):
    """Place text and scale its font size so it spans `width` data units."""
    t = ax.text(x, y, s, ha=ha, va=va, fontsize=50, **kw)
    fig.canvas.draw()
    bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
    cur = bb.width / (fig.dpi * 6) * 60
    t.set_fontsize(50 * width / cur)
    return t


def spaced(s, n=1):
    return (" " * n).join(s)


def enso(ax, cx, cy, r, color=K, max_w=26, seed=3, start=0.55, sweep=2 * math.pi - 0.75):
    """Brush-stroke ensō with dry-brush streaks towards the tail."""
    g = np.random.default_rng(seed)
    t = np.linspace(0, 1, 700)
    ang = start + sweep * t
    width = max_w * (0.45 + 0.55 * np.sin(np.pi * np.clip(t * 1.05, 0, 1)) ** 0.5) * (1 - 0.6 * t ** 4)
    rr = r * (1 + 0.012 * np.sin(ang * 2.3 + 1) + 0.006 * np.sin(ang * 7))
    xs, ys = cx + rr * np.cos(ang), cy + rr * np.sin(ang)
    for k in range(len(t) - 1):
        ax.plot(xs[k:k + 2], ys[k:k + 2], color=color, lw=width[k], solid_capstyle="round", zorder=3)
    # dry brush bristle streaks in the second half
    for b in range(26):
        off = g.uniform(-0.5, 0.5) * max_w * 0.022
        t0 = g.uniform(0.55, 0.85); t1 = min(1.0, t0 + g.uniform(0.08, 0.2))
        m = (t > t0) & (t < t1)
        ax.plot(cx + (rr[m] + off) * np.cos(ang[m]), cy + (rr[m] + off) * np.sin(ang[m]),
                color=color, lw=g.uniform(0.4, 1.6), alpha=g.uniform(0.5, 1), zorder=3)


def silhouette(ax, pose, ox, oy, sc, th, color=K, z=5):
    Figure(ax, pose, ox=ox, oy=oy, sc=sc, th=th, fill=color, edge=color, lw=1.2, belt=False, zorder=z, face=False)


def hanko(ax, x, y, s=5.0, bg=K, fg=WH):
    ax.add_patch(Rectangle((x, y), s, s * 1.9, fc=bg, ec=bg, zorder=8))
    ax.text(x + s / 2, y + s * 1.43, "三", fontproperties=JP_FONT, fontsize=s * 5.6, color=fg, ha="center", va="center", zorder=9)
    ax.text(x + s / 2, y + s * 0.5, "戦", fontproperties=JP_FONT, fontsize=s * 5.6, color=fg, ha="center", va="center", zorder=9)


def save_cover(fig, name):
    p = OUT / f"{name}.png"
    fig.savefig(p, dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)
    im = Image.open(p).convert("RGB")
    im.save(OUT / f"{name}.jpg", quality=95, dpi=(300, 300))
    p.unlink()
    print("saved", name, im.size)


STANCE = Pose("uke", "uke", "sanchin", "R")

IVORY = "#F3EBDD"; CRIMSON = "#9E1B1E"; GOLD = "#B88A3E"; INK = "#1B1B1F"; NAVY = "#0C1730"; NAVY2 = "#1E3158"
CREAM = "#F6F0E4"; CHAR = "#26262B"; LGOLD = "#D9B26A"


def gradient(ax, c1, c2, zorder=0.5, vertical=True):
    import matplotlib.colors as mc
    a1, a2 = np.array(mc.to_rgb(c1)), np.array(mc.to_rgb(c2))
    t = np.linspace(0, 1, 400)[:, None, None]
    img = a1 * (1 - t) + a2 * t
    img = np.repeat(img, 10, axis=1)
    ax.imshow(img, extent=(0, 60, 0, 90), origin="lower", aspect="auto", zorder=zorder, interpolation="bicubic")


def glow(ax, cx, cy, rx, ry, color, strength=0.9, zorder=1):
    import matplotlib.colors as mc
    yy, xx = np.mgrid[0:90:450j, 0:60:300j]
    d = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
    a = np.clip(1 - d, 0, 1) ** 2 * strength
    rgba = np.zeros(a.shape + (4,)); rgba[..., :3] = mc.to_rgb(color); rgba[..., 3] = a
    ax.imshow(rgba, extent=(0, 60, 0, 90), origin="lower", aspect="auto", zorder=zorder, interpolation="bicubic")


# ---------------------------------------------------------------- A: Ensō Classic (ivory, crimson, gold)
fig, ax = new()
ax.add_patch(Rectangle((0, 0), 60, 90, fc=IVORY))
glow(ax, 30, 40, 30, 30, "#FFFFFF", 0.55)
ax.add_patch(Rectangle((2.2, 2.2), 55.6, 85.6, fc="none", ec=GOLD, lw=1.4, zorder=2))
ax.add_patch(Rectangle((2.9, 2.9), 54.2, 84.2, fc="none", ec=GOLD, lw=0.5, zorder=2))
fit(fig, ax, 30, 83.6, spaced("GOJU-RYU KARATE", 1), 28, color=CRIMSON, family="Source Sans 3", fontweight="bold")
fit(fig, ax, 30, 74.6, TITLE, 50, color=INK, fontproperties=BLACK_FONT)
fit(fig, ax, 30, 66.4, spaced("MASTERCLASS", 1), 38, color=INK, family=SERIF)
ax.plot([20, 27], [62.4, 62.4], color=GOLD, lw=1.2); ax.plot([33, 40], [62.4, 62.4], color=GOLD, lw=1.2)
ax.add_patch(Polygon([(30, 61.6), (30.8, 62.4), (30, 63.2), (29.2, 62.4)], fc=GOLD, ec="none"))
enso(ax, 30, 38.0, 14.6, color=CRIMSON, max_w=26, seed=4, start=1.2)
silhouette(ax, STANCE, 30, 26.0, 0.215, -32, color=INK)
ax.add_patch(Ellipse((30, 25.8), 12, 1.0, fc="#D8CDB8", ec="none", zorder=4))
hanko(ax, 50.0, 21.0, 3.4, bg=CRIMSON, fg=IVORY)
ax.text(30, 15.0, SUB, ha="center", va="center", fontsize=10.2, color=CHAR, family=SERIF, style="italic", linespacing=1.35)
ax.plot([24, 36], [9.6, 9.6], color=GOLD, lw=1.0)
fit(fig, ax, 30, 5.8, AUTHOR, 38, color=INK, family=SERIF, fontweight="bold")
save_cover(fig, "cover_A_enso_classic")

# ---------------------------------------------------------------- B: Night Dojo (midnight navy and gold)
fig, ax = new()
fig.set_facecolor(NAVY)
gradient(ax, "#070D1C", NAVY2, zorder=0.5)
glow(ax, 30, 34, 24, 30, "#E8B45A", 0.55, zorder=1)
glow(ax, 30, 30, 12, 16, "#FFE6B0", 0.45, zorder=1.1)
ax.text(30, 52, "三戦", fontproperties=JP_FONT, fontsize=150, color="#8E1B22", alpha=0.55, ha="center", va="center", zorder=2)
fit(fig, ax, 30, 85.4, spaced("GOJU-RYU KARATE", 1), 28, color=LGOLD, family="Source Sans 3", fontweight="semibold", zorder=6)
fit(fig, ax, 30, 77.2, TITLE, 54, color="#FFFFFF", fontproperties=BLACK_FONT, zorder=6)
fit(fig, ax, 30, 69.4, spaced("MASTERCLASS", 2), 46, color=LGOLD, family="Source Sans 3", fontweight="light", zorder=6)
ax.add_patch(Ellipse((30, 15.6), 22, 2.0, fc="#05080F", ec="none", alpha=0.7, zorder=4))
silhouette(ax, Pose("uke", "uke", "sanchin", "R"), 30, 16.0, 0.39, -30, color="#0A0F1C")
ax.plot([6, 54], [12.2, 12.2], color=GOLD, lw=0.8, zorder=6)
ax.text(30, 8.6, SUB.replace("\n", " ").replace("Drills, ", "Drills,\n").replace("Progressions ", "Progressions\n"),
        ha="center", va="center", fontsize=9.6, color="#EDE3CF", family=SERIF, style="italic", linespacing=1.3, zorder=6)
fit(fig, ax, 30, 3.0, AUTHOR, 34, color=LGOLD, family="Source Sans 3", fontweight="bold", zorder=6)
save_cover(fig, "cover_B_night_dojo")

# ---------------------------------------------------------------- C: Frame by Frame (crimson, cream, gold)
fig, ax = new()
ax.add_patch(Rectangle((0, 0), 60, 90, fc=CREAM))
ax.add_patch(Rectangle((0, 46), 60, 44, fc=CRIMSON, zorder=1))
gradient_top = glow(ax, 30, 80, 40, 22, "#C8343A", 0.6, zorder=1.05)
ax.plot([0, 60], [46, 46], color=GOLD, lw=3.0, zorder=2)
fit(fig, ax, 30, 83.6, spaced("GOJU-RYU KARATE", 1), 26, color=LGOLD, family="Source Sans 3", fontweight="bold", zorder=3)
fit(fig, ax, 30, 73.4, TITLE, 54, color="#FFFFFF", fontproperties=BLACK_FONT, zorder=3)
fit(fig, ax, 30, 63.4, "MASTERCLASS", 54, color="#FFFFFF", fontproperties=BLACK_FONT, zorder=3)
ax.text(30, 52.6, SUB, ha="center", va="center", fontsize=10.0, color="#F7E9D6", family=SERIF, style="italic", linespacing=1.3, zorder=3)
seq = [Pose("yoi", "yoi", "musubi"), Pose("uke", "uke", "sanchin", "R"), Pose("hikite", "uke", "sanchin", "R"),
       Pose("tsuki", "uke", "sanchin", "R"), Pose("uke", "uke", "step_mid", "L"), Pose("tora_down", "tora_up", "sanchin", "R")]
ths = [-20, -25, -40, -40, -35, -25]
for i, (pp, th) in enumerate(zip(seq, ths)):
    x = 6 + i * 9.6
    silhouette(ax, pp, x, 14.5, 0.205, th, color=CHAR)
    ax.add_patch(Circle((x, 40.0), 1.6, fc=CRIMSON, ec=GOLD, lw=0.8, zorder=6))
    ax.text(x, 39.95, str(i + 1), color="#FFFFFF", fontsize=8, ha="center", va="center", fontweight="bold", zorder=7)
ax.plot([1.5, 58.5], [14.4, 14.4], color=CHAR, lw=1.1, zorder=4)
for xx in np.arange(1.5, 58.5, 0.9):
    ax.plot([xx, xx - 0.6], [14.4, 13.8], color=CHAR, lw=0.4, zorder=4)
ax.add_patch(Rectangle((0, 0), 60, 10.5, fc=INK, zorder=6))
ax.plot([0, 60], [10.5, 10.5], color=GOLD, lw=2.0, zorder=7)
fit(fig, ax, 30, 5.2, AUTHOR, 42, color=LGOLD, family=SERIF, fontweight="bold", zorder=7)
hanko(ax, 54.0, 47.6, 3.0, bg=GOLD, fg=CRIMSON)
save_cover(fig, "cover_C_frame_by_frame")

# ---------------------------------------------------------------- preview sheet
ims = [Image.open(OUT / f) for f in ("cover_A_enso_classic.jpg", "cover_B_night_dojo.jpg", "cover_C_frame_by_frame.jpg")]
ims = [i.resize((600, 900)) for i in ims]
sheet = Image.new("RGB", (600 * 3 + 80, 980), "#3b3b40")
from PIL import ImageDraw, ImageFont
dr = ImageDraw.Draw(sheet)
f = ImageFont.truetype(str(ROOT / "fonts/SourceSans3-Bold.ttf"), 34)
for k, im in enumerate(ims):
    sheet.paste(im, (20 + k * 620, 20))
    dr.text((20 + k * 620 + 300, 950), f"OPTION {'ABC'[k]}", fill="white", font=f, anchor="mm")
sheet.save(OUT / "covers_preview.jpg", quality=90)
print("preview saved")
