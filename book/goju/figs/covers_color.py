"""Three full-colour 6 x 9 in front covers (1800 x 2700 px) for Goju-Ryu Karate Kyohan."""
from body import *
from matplotlib import font_manager
from matplotlib.patches import Circle, Rectangle, Polygon as Pg
import matplotlib.patheffects as pe

OUT = ROOT / "output"
JP = font_manager.FontProperties(fname=str(ROOT / "fonts/ipag.ttf"))
TITLE1, TITLE2 = "GOJU-RYU", "KARATE KYOHAN"
SUB = ("ILLUSTRATED TEXTBOOK WITH 1200 LINE DRAWINGS\nSHOWING SANCHIN TENSION, ROOTING, IRON BODY METHODS,\n"
       "AND INTERNAL ENERGY TRAINING EXPLAINED STEP BY STEP")
AUTH = "DR BEVERLY J. STIVERS"


def base():
    fig = plt.figure(figsize=(6, 9))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 600); ax.set_ylim(0, 900); ax.axis("off")
    return fig, ax


def gradient(ax, top, bottom, extent=(0, 600, 0, 900), z=0):
    t = np.array(matplotlib.colors.to_rgb(top)); b = np.array(matplotlib.colors.to_rgb(bottom))
    g = np.linspace(0, 1, 512)[:, None, None]
    img = b + (t - b) * g
    ax.imshow(np.repeat(img, 2, axis=1), extent=extent, origin="lower", aspect="auto", zorder=z)


def glow(ax, x, y, r, color, n=40, alpha=0.5, z=1):
    for i in range(n):
        f = 1 - i / n
        ax.add_patch(Circle((x, y), r * (1 + 0.9 * (1 - f)), fc=color, ec="none", alpha=alpha / n * 2 * f, zorder=z))


def figure_panel(fig, rect, p, view, line="#000000", fill="white", far="#d9d9d9", marks=()):
    import body
    old = (body.INK, body.FAR)
    body.INK, body.FAR = line, far
    a2 = fig.add_axes(rect); a2.patch.set_alpha(0)
    render_panel(a2, dict(pose=p, view=view, marks=list(marks)), xr=78)
    for l in a2.lines:
        if l.get_xdata() is not None and len(l.get_xdata()) == 2 and abs(l.get_xdata()[0]) == 200:
            l.set_visible(False)  # hide ground line
    body.INK, body.FAR = old
    return a2


def text(ax, x, y, s, size, color, family="EB Garamond", weight="bold", stroke=None, **kw):
    t = ax.text(x, y, s, ha="center", va="center", fontsize=size, color=color, family=family, weight=weight, zorder=20, **kw)
    if stroke:
        t.set_path_effects([pe.withStroke(linewidth=stroke[1], foreground=stroke[0])])
    return t


# ---------------------------------------------------------------- 1. Crimson Sun (black / red / gold)
fig, ax = base()
gradient(ax, "#0b0b0d", "#1c0f10")
glow(ax, 300, 360, 150, "#e0311f", alpha=0.35)
ax.add_patch(Circle((300, 360), 150, fc="#c8241a", ec="none", zorder=2))
ax.add_patch(Circle((300, 360), 150, fc="none", ec="#e8b34a", lw=2, zorder=3))
for r in (175, 200):
    ax.add_patch(Circle((300, 360), r, fc="none", ec="#e8b34a", lw=0.6, alpha=0.45, zorder=3))
text(ax, 300, 845, "剛 柔 流", 30, "#e8b34a", fontproperties=JP)
text(ax, 300, 780, TITLE1, 60, "white", stroke=("#000000", 4))
text(ax, 300, 712, TITLE2, 38, "#e8b34a", stroke=("#000000", 3))
ax.plot([170, 430], [679, 679], color="#c8241a", lw=3, zorder=20)
text(ax, 300, 628, SUB, 9.6, "white", family="Source Sans 3", weight="bold", linespacing=1.55)
figure_panel(fig, [0.30, 0.215, 0.40, 0.385], pose("sanchin_r", "kamae"), 0, line="#111111")
ax.add_patch(Rectangle((0, 0), 600, 140, fc="#000000", alpha=0.75, zorder=10))
ax.plot([60, 540], [140, 140], color="#e8b34a", lw=1.5, zorder=11)
text(ax, 300, 96, AUTH, 22, "white")
text(ax, 300, 52, "SANCHIN  •  ROOTING  •  IRON BODY  •  INTERNAL ENERGY", 9, "#e8b34a", family="Source Sans 3")
fig.savefig(OUT / "Cover_Color_1_Crimson-Sun.jpg", dpi=300, facecolor="black", pil_kwargs={"quality": 93})
plt.close(fig)

# ---------------------------------------------------------------- 2. Ink and Parchment (cream / black / red seal)
fig, ax = base()
gradient(ax, "#f6ecd6", "#e7d4ad")
rng = np.random.default_rng(3)
for _ in range(900):  # paper fibre texture
    x, y = rng.uniform(0, 600), rng.uniform(0, 900)
    ax.plot([x, x + rng.uniform(-6, 6)], [y, y + rng.uniform(-2, 2)], color="#b89b6a", lw=0.3, alpha=0.25, zorder=1)
# ink brush circle (enso)
th = np.linspace(0.35, 2 * np.pi - 0.1, 400)
for k in range(26):
    r = 205 + rng.normal(0, 3)
    w = 9 * np.sin(np.linspace(0.2, np.pi - 0.2, 400)) + rng.uniform(0, 2)
    ax.plot(300 + r * np.cos(th), 350 + r * np.sin(th), color="#1a1a1a", lw=0.9 + k * 0.05, alpha=0.08, zorder=2)
ax.plot(300 + 205 * np.cos(th), 350 + 205 * np.sin(th), color="#111111", lw=7, alpha=0.85, solid_capstyle="round", zorder=2)
text(ax, 300, 812, TITLE1, 62, "#111111")
text(ax, 300, 755, TITLE2, 38, "#a3201b")
ax.plot([150, 450], [722, 722], color="#111111", lw=1.6, zorder=20)
text(ax, 300, 670, SUB, 9.6, "#222222", family="Source Sans 3", weight="bold", linespacing=1.55)
figure_panel(fig, [0.23, 0.17, 0.54, 0.44], pose("sanchin_r", lh=(16, -38, -10), rh=(-8, -8, 44), rhand="open", rroll=90), 55,
             line="#111111", fill="white", far="#e6d6b8")
# red hanko seal
ax.add_patch(Rectangle((468, 470), 58, 74, fc="#b3241c", ec="#7c140f", lw=1.2, zorder=21))
for i, ch in enumerate("剛柔"):
    ax.text(497, 525 - i * 33, ch, ha="center", va="center", fontsize=19, color="#f6ecd6", fontproperties=JP, zorder=22)
ax.plot([60, 540], [118, 118], color="#a3201b", lw=2, zorder=20)
text(ax, 300, 80, AUTH, 22, "#111111")
text(ax, 300, 40, "THE COMPLETE PROBLEM-SOLVING TEXTBOOK", 9, "#a3201b", family="Source Sans 3")
fig.savefig(OUT / "Cover_Color_2_Ink-and-Parchment.jpg", dpi=300, facecolor="#f6ecd6", pil_kwargs={"quality": 93})
plt.close(fig)

# ---------------------------------------------------------------- 3. Midnight Navy and Gold (energy rings)
fig, ax = base()
gradient(ax, "#0a1a33", "#030914")
glow(ax, 300, 330, 120, "#2f6fd6", alpha=0.45)
for i, r in enumerate((120, 150, 182, 216, 252)):
    ax.add_patch(Circle((300, 330), r, fc="none", ec="#d9a93f", lw=2.2 - i * 0.35, alpha=0.9 - i * 0.15, zorder=3))
for a in np.linspace(0, 2 * np.pi, 24, endpoint=False):  # radiating lines from the tanden
    ax.plot([300 + 125 * np.cos(a), 300 + 270 * np.cos(a)], [330 + 125 * np.sin(a), 330 + 270 * np.sin(a)],
            color="#d9a93f", lw=0.5, alpha=0.35, zorder=2)
ax.add_patch(Rectangle((40, 630), 520, 236, fc="#000000", alpha=0.35, zorder=4))
text(ax, 300, 820, TITLE1, 60, "#f3d37a", stroke=("#3a2a05", 2))
text(ax, 300, 763, TITLE2, 38, "white")
ax.plot([170, 430], [724, 724], color="#d9a93f", lw=2, zorder=20)
text(ax, 300, 674, SUB, 9.2, "#e9eef7", family="Source Sans 3", weight="bold", linespacing=1.5)
figure_panel(fig, [0.28, 0.15, 0.44, 0.42], pose("shiko", "kamae"), 0, line="#0a1a33", far="#c9d4e6",
             marks=[("dantien",)])
text(ax, 300, 95, AUTH, 22, "#f3d37a")
text(ax, 300, 52, "SANCHIN  •  TENSHO  •  HOJO UNDŌ  •  KAKIE", 9, "#c9d4e6", family="Source Sans 3")
fig.savefig(OUT / "Cover_Color_3_Midnight-Gold.jpg", dpi=300, facecolor="#030914", pil_kwargs={"quality": 93})
plt.close(fig)
print("done")
