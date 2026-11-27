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


def hanko(ax, x, y, s=5.0):
    ax.add_patch(Rectangle((x, y), s, s * 1.9, fc=K, ec=K, zorder=8))
    ax.text(x + s / 2, y + s * 1.43, "三", fontproperties=JP_FONT, fontsize=s * 5.6, color=WH, ha="center", va="center", zorder=9)
    ax.text(x + s / 2, y + s * 0.5, "戦", fontproperties=JP_FONT, fontsize=s * 5.6, color=WH, ha="center", va="center", zorder=9)


def save_cover(fig, name):
    p = OUT / f"{name}.png"
    fig.savefig(p, dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)
    im = Image.open(p).convert("L").convert("RGB")
    im.save(OUT / f"{name}.jpg", quality=95, dpi=(300, 300))
    p.unlink()
    print("saved", name, im.size)


STANCE = Pose("uke", "uke", "sanchin", "R")

# ---------------------------------------------------------------- A: Ensō Classic (white)
fig, ax = new()
ax.add_patch(Rectangle((0, 0), 60, 90, fc=WH))
fit(fig, ax, 30, 84.2, spaced("GOJU-RYU KARATE", 1), 30, color=K, family="Source Sans 3", fontweight="semibold")
fit(fig, ax, 30, 75.0, TITLE, 52, color=K, fontproperties=BLACK_FONT)
fit(fig, ax, 30, 66.6, spaced("MASTERCLASS", 1), 40, color=K, family=SERIF)
ax.plot([18, 42], [62.6, 62.6], color=K, lw=1.0)
enso(ax, 30, 38.0, 14.6, max_w=24, seed=4, start=1.2)
silhouette(ax, STANCE, 30, 26.0, 0.215, -32)
ax.add_patch(Ellipse((30, 25.8), 12, 1.0, fc=G1, ec="none", zorder=4))
hanko(ax, 50.0, 21.0, 3.4)
ax.text(30, 15.2, SUB, ha="center", va="center", fontsize=10.2, color=K, family=SERIF, style="italic", linespacing=1.35)
ax.plot([22, 38], [9.4, 9.4], color=K, lw=0.8)
fit(fig, ax, 30, 5.6, AUTHOR, 40, color=K, family=SERIF, fontweight="bold")
save_cover(fig, "cover_A_enso_classic")

# ---------------------------------------------------------------- B: Night Dojo (black)
fig, ax = new()
fig.set_facecolor(K)
ax.add_patch(Rectangle((0, 0), 60, 90, fc=K))
# spotlight gradient
yy, xx = np.mgrid[0:90:400j, 0:60:270j]
d = np.sqrt(((xx - 30) / 26) ** 2 + ((yy - 36) / 30) ** 2)
glow = np.clip(1 - d, 0, 1) ** 1.8
ax.imshow(glow, extent=(0, 60, 0, 90), origin="lower", cmap="gray", vmin=0, vmax=2.4, zorder=1, interpolation="bicubic")
# kanji watermark
ax.text(30, 52, "三戦", fontproperties=JP_FONT, fontsize=150, color="#262626", ha="center", va="center", zorder=2)
fit(fig, ax, 30, 85.4, spaced("GOJU-RYU KARATE", 1), 28, color="#cfcfcf", family="Source Sans 3", fontweight="semibold", zorder=6)
fit(fig, ax, 30, 77.2, TITLE, 54, color=WH, fontproperties=BLACK_FONT, zorder=6)
fit(fig, ax, 30, 69.4, spaced("MASTERCLASS", 2), 46, color=WH, family="Source Sans 3", fontweight="light", zorder=6)
ax.add_patch(Ellipse((30, 15.6), 22, 2.0, fc="#3a3a3a", ec="none", zorder=4))
silhouette(ax, Pose("uke", "uke", "sanchin", "R"), 30, 16.0, 0.39, -30, color=WH)
ax.plot([4, 56], [12.2, 12.2], color="#7a7a7a", lw=0.5, zorder=6)
ax.text(30, 8.6, SUB.replace("\n", " ").replace("Drills, ", "Drills,\n").replace("Progressions ", "Progressions\n"),
        ha="center", va="center", fontsize=9.6, color="#e6e6e6", family=SERIF, style="italic", linespacing=1.3, zorder=6)
fit(fig, ax, 30, 3.0, AUTHOR, 34, color=WH, family="Source Sans 3", fontweight="bold", zorder=6)
save_cover(fig, "cover_B_night_dojo")

# ---------------------------------------------------------------- C: Frame by Frame (split)
fig, ax = new()
ax.add_patch(Rectangle((0, 0), 60, 90, fc=WH))
ax.add_patch(Rectangle((0, 46), 60, 44, fc=K, zorder=1))
fit(fig, ax, 30, 83.6, spaced("GOJU-RYU KARATE", 1), 26, color="#bdbdbd", family="Source Sans 3", fontweight="semibold", zorder=3)
fit(fig, ax, 30, 73.4, TITLE, 54, color=WH, fontproperties=BLACK_FONT, zorder=3)
fit(fig, ax, 30, 63.4, "MASTERCLASS", 54, color=WH, fontproperties=BLACK_FONT, zorder=3)
ax.text(30, 52.6, SUB, ha="center", va="center", fontsize=10.0, color="#e0e0e0", family=SERIF, style="italic", linespacing=1.3, zorder=3)
# frame-by-frame sequence
seq = [Pose("yoi", "yoi", "musubi"), Pose("uke", "uke", "sanchin", "R"), Pose("hikite", "uke", "sanchin", "R"),
       Pose("tsuki", "uke", "sanchin", "R"), Pose("uke", "uke", "step_mid", "L"), Pose("tora_down", "tora_up", "sanchin", "R")]
ths = [-20, -25, -40, -40, -35, -25]
for i, (pp, th) in enumerate(zip(seq, ths)):
    x = 6 + i * 9.6
    silhouette(ax, pp, x, 14.5, 0.205, th)
    ax.add_patch(Circle((x, 40.0), 1.6, fc=K, zorder=6))
    ax.text(x, 39.95, str(i + 1), color=WH, fontsize=8, ha="center", va="center", fontweight="bold", zorder=7)
ax.plot([1.5, 58.5], [14.4, 14.4], color=K, lw=1.1, zorder=4)
for xx in np.arange(1.5, 58.5, 0.9):
    ax.plot([xx, xx - 0.6], [14.4, 13.8], color=K, lw=0.4, zorder=4)
ax.add_patch(Rectangle((0, 0), 60, 10.5, fc=K, zorder=6))
fit(fig, ax, 30, 5.2, AUTHOR, 42, color=WH, family=SERIF, fontweight="bold", zorder=7)
hanko(ax, 54.0, 47.4, 3.0)
save_cover(fig, "cover_C_frame_by_frame")

# ---------------------------------------------------------------- preview sheet
ims = [Image.open(OUT / f) for f in ("cover_A_enso_classic.jpg", "cover_B_night_dojo.jpg", "cover_C_frame_by_frame.jpg")]
ims = [i.resize((600, 900)) for i in ims]
sheet = Image.new("RGB", (600 * 3 + 80, 980), "#8a8a8a")
from PIL import ImageDraw, ImageFont
dr = ImageDraw.Draw(sheet)
f = ImageFont.truetype(str(ROOT / "fonts/SourceSans3-Bold.ttf"), 34)
for k, im in enumerate(ims):
    sheet.paste(im, (20 + k * 620, 20))
    dr.text((20 + k * 620 + 300, 950), f"OPTION {'ABC'[k]}", fill="white", font=f, anchor="mm")
sheet.save(OUT / "covers_preview.jpg", quality=90)
print("preview saved")
