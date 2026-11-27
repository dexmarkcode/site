from figlib import *
from matplotlib.patches import FancyBboxPatch

def box(ax, x, y, w, h, text, size=7, bold=False, fill="white", lw=0.9):
    ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.02,rounding_size=0.04",
                 fc=fill, ec="black", lw=lw, zorder=5))
    ax.text(x, y, text, ha="center", va="center", fontsize=size, fontweight="bold" if bold else "normal",
            zorder=6, color="white" if fill == "black" else "black", linespacing=1.25)

# ---- 1.1 lineage
fig = plt.figure(figsize=(4.5, 3.9))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 4.5); ax.set_ylim(0, 3.9); ax.axis("off")
box(ax, 2.25, 3.55, 3.4, 0.42, "Southern Chinese boxing, Fuzhou\n(crane and related systems)", 7)
box(ax, 2.25, 2.85, 3.0, 0.42, "Kanryo Higaonna (Naha)\nstudies in China, teaches on return", 7, True)
box(ax, 2.25, 2.15, 3.0, 0.42, "Chojun Miyagi\nnames the art Goju-Ryu, c. 1930", 7, True, fill="black")
for y0, y1 in ((3.33, 3.07), (2.63, 2.37)):
    arrow(ax, (2.25, y0), (2.25, y1), head=7)
arrow(ax, (2.25, 1.93), (2.25, 1.62), head=7)
ax.text(0.15, 1.45, "Training kata", fontsize=7, fontweight="bold")
box(ax, 0.95, 1.05, 1.5, 0.45, "Sanchin\nTensho", 7)
ax.text(1.85, 1.45, "Introductory", fontsize=7, fontweight="bold")
box(ax, 2.5, 1.05, 1.35, 0.45, "Gekisai Dai Ichi\nGekisai Dai Ni", 6.5)
ax.text(4.4, 1.45, "Close-range kata", ha="right", fontsize=7, fontweight="bold")
ax.text(3.82, 0.82, "Saifa\nSeiyunchin\nShisochin\nSanseru\nSeipai\nKururunfa\nSeisan\nSuparinpei", fontsize=6.4,
        ha="center", va="center", linespacing=1.18,
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="black", lw=0.9))
ax.plot([0.95, 3.82], [1.6, 1.6], color="black", lw=0.8)
for x in (0.95, 2.5, 3.82):
    ax.plot([x, x], [1.6, 1.33 if x != 3.82 else 1.62], color="black", lw=0.8)
ax.text(0.15, 0.25, "Common thread: rooted stance, short strikes,\ngrabbing and pulling, throws, conditioning.",
        fontsize=6.8, style="italic", va="bottom")
save(fig, "fig1_1")

# ---- 1.2 ranges
def pair(gap, title, a_kw=None, b_kw=None):
    @titled(title)
    def p(ax):
        a = stance(-gap/2, 1, "A", width=0.55, guard="high")
        b = stance(gap/2, -1, "B", width=0.55, guard="high")
        if a_kw: a_kw(a)
        if b_kw: b_kw(b)
        a.draw(ax); b.draw(ax)
        ax.annotate("", xy=(-gap/2, 0.25), xytext=(gap/2, 0.25), arrowprops=dict(arrowstyle="<->", lw=0.8))
    return p
def touch(a):
    a.hands["near"] = (a.hip[0] + 0.5, 1.45)
def touchb(b):
    b.hands["near"] = (b.hip[0] - 0.5, 1.45)
def clinch(a):
    a.hands["near"] = (a.hip[0] + 0.42, 1.62); a.hands["far"] = (a.hip[0] + 0.38, 1.55); a.lean = 14
def clinchb(b):
    b.hands["near"] = (b.hip[0] - 0.38, 1.4); b.hands["far"] = (b.hip[0] - 0.35, 1.32); b.lean = 12
sequence("fig1_2", [pair(2.4, "Kicking range"), pair(1.6, "Punching range"),
                    pair(1.05, "Close (trapping) range", touch, touchb), pair(0.72, "Clinch and grappling range", clinch, clinchb)],
         cols=2, xlim=(-1.75, 1.75), ylim=(-0.12, 2.0))

# ---- 1.3 loop
fig = plt.figure(figsize=(4.5, 3.2))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(-2.25, 2.25); ax.set_ylim(-1.6, 1.6); ax.axis("off"); ax.set_aspect("equal")
labels = ["1  Problem", "2  Principle", "3  Technique", "4  Drill", "5  Pressure"]
pts = []
for i, t in enumerate(labels):
    a = math.radians(90 - i * 72)
    x, y = 1.6 * math.cos(a), 1.15 * math.sin(a)
    pts.append((x, y))
    box(ax, x, y, 1.15, 0.38, t, 7.5, True, fill="black" if i in (0, 4) else "white")
for i in range(5):
    p, q = pts[i], pts[(i + 1) % 5]
    mx, my = p[0] + (q[0]-p[0]) * 0.27, p[1] + (q[1]-p[1]) * 0.27
    nx, ny = p[0] + (q[0]-p[0]) * 0.73, p[1] + (q[1]-p[1]) * 0.73
    arrow(ax, (mx, my), (nx, ny), rad=-0.15, dashed=(i == 4), head=7)
ax.text(0, 0.05, "If it fails under\npressure, go back and\nre-examine the problem", ha="center", va="center", fontsize=7, style="italic")
save(fig, "fig1_3")

# ---- 1.4 conventions
@titled("You (black) and opponent (white)")
def c1(ax):
    stance(-0.5, 1, "A").draw(ax); stance(0.5, -1, "B").draw(ax)
    tag(ax, -0.5, 1.98, "YOU", 6); tag(ax, 0.5, 1.98, "OPPONENT", 6)
    tag(ax, -0.95, 0.75, "far leg\n(grey)", 5.5, box=False)
@titled("Arrows and impact")
def c2(ax):
    a = stance(-0.45, 1, "A", lean=10); a.hands["near"] = (0.35, 1.55); a.elbow["near"] = -1; a.draw(ax)
    stance(0.55, -1, "B").draw(ax)
    impact(ax, 0.42, 1.56)
    arrow(ax, (-0.25, 1.15), (0.25, 1.42), rad=-0.2)
    arrow(ax, (-0.95, 0.35), (-0.6, 0.35), dashed=True)
    numdot(ax, -0.1, 1.05, 1); numdot(ax, -1.0, 0.5, 2)
sequence("fig1_4", [c1, c2], cols=2)
