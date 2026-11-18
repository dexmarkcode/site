import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import plt, NAVY, COPPER
import numpy as np
from matplotlib.patches import Rectangle, Circle
from matplotlib import font_manager

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 6.25, 10.0
fig = plt.figure(figsize=(W, H), dpi=256)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

# background gradient
grad = np.linspace(0, 1, 512).reshape(-1, 1)
from matplotlib.colors import LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list("bg", ["#0b1a2e", "#14284a", "#1d3557"])
ax.imshow(grad, extent=[0, W, 0, H], cmap=cmap, aspect="auto", zorder=0, origin="lower")

# faint PCB traces
rng = np.random.default_rng(7)
for i in range(46):
    x, y = rng.uniform(0, W), rng.uniform(0, H)
    pts = [(x, y)]
    for _ in range(rng.integers(2, 5)):
        dx, dy = rng.choice([-1, 0, 1]) * rng.uniform(0.3, 1.2), rng.choice([-1, 0, 1]) * rng.uniform(0.3, 1.2)
        if dx and dy:
            dy = np.sign(dy) * abs(dx)  # 45-degree bends like a PCB
        x, y = x + dx, y + dy; pts.append((x, y))
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color="#3a5a85", lw=1.1, alpha=0.35, zorder=1, solid_capstyle="round")
    ax.add_patch(Circle(pts[-1], 0.045, fc="#3a5a85", alpha=0.45, zorder=1))

# central schematic: a bridge-like network in copper
c = COPPER
def wire(x1, y1, x2, y2, lw=2.6):
    ax.plot([x1, x2], [y1, y2], color=c, lw=lw, zorder=3, solid_capstyle="round")
def res_h(x, y, w=0.62, h=0.22):
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc="#14284a", ec=c, lw=2.6, zorder=4))
def res_v(x, y, w=0.22, h=0.62):
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc="#14284a", ec=c, lw=2.6, zorder=4))
def node(x, y):
    ax.add_patch(Circle((x, y), 0.07, fc=c, ec=c, zorder=5))

y0, y1 = 3.15, 5.15
xl, xm, xr = 1.2, 3.125, 5.05
wire(xl, y0, xl, y1); wire(xl, y1, xr, y1); wire(xr, y1, xr, y0); wire(xl, y0, xr, y0); wire(xm, y0, xm, y1)
# source on left
ax.add_patch(Circle((xl, (y0 + y1) / 2), 0.32, fc="#14284a", ec=c, lw=2.6, zorder=4))
ax.text(xl, (y0 + y1) / 2 + 0.08, "+", color=c, ha="center", va="center", fontsize=15, zorder=6, fontweight="bold")
ax.text(xl, (y0 + y1) / 2 - 0.13, "–", color=c, ha="center", va="center", fontsize=15, zorder=6, fontweight="bold")
res_h((xl + xm) / 2, y1); res_h((xm + xr) / 2, y1); res_v(xm, (y0 + y1) / 2); res_v(xr, (y0 + y1) / 2)
for p in [(xm, y1), (xm, y0)]:
    node(*p)
# mesh current arrows
for cx in [(xl + xm) / 2, (xm + xr) / 2]:
    th = np.linspace(np.pi * 0.95, -np.pi * 0.55, 60)
    ax.plot(cx + 0.42 * np.cos(th), (y0 + y1) / 2 + 0.42 * np.sin(th), color="#f3c19f", lw=1.6, zorder=3)
    ax.annotate("", xy=(cx + 0.42 * np.cos(th[-1]), (y0 + y1) / 2 + 0.42 * np.sin(th[-1])),
                xytext=(cx + 0.42 * np.cos(th[-3]), (y0 + y1) / 2 + 0.42 * np.sin(th[-3])),
                arrowprops=dict(arrowstyle="-|>", color="#f3c19f", lw=1.6), zorder=3)
ax.text((xl + xm) / 2, (y0 + y1) / 2, "I₁", color="#f3c19f", ha="center", va="center", fontsize=13, family="Source Sans 3")
ax.text((xm + xr) / 2, (y0 + y1) / 2, "I₂", color="#f3c19f", ha="center", va="center", fontsize=13, family="Source Sans 3")

# Typography
ax.plot([0.55, W - 0.55], [9.42, 9.42], color=c, lw=1.2)
ax.text(W / 2, 9.55, "A MODERN TEXTBOOK FOR BEGINNERS", color="#f3c19f", ha="center", va="bottom",
        fontsize=11.5, family="Source Sans 3", fontweight="semibold")
ax.text(W / 2, 8.55, "Circuit Analysis", color="white", ha="center", va="center", fontsize=44, family="EB Garamond")
ax.text(W / 2, 7.65, "Made Simple", color="white", ha="center", va="center", fontsize=44, family="EB Garamond")
ax.plot([W / 2 - 0.8, W / 2 + 0.8], [7.0, 7.0], color=c, lw=2)
ax.text(W / 2, 6.45, "Ohm’s Law to Thévenin, Norton, and Mesh Analysis\nExplained Clearly",
        color="#dbe4ef", ha="center", va="center", fontsize=13.5, family="Crimson Text", style="italic", linespacing=1.35)

ax.text(W / 2, 2.25, "Over 100 worked examples  ·  Illustrated throughout  ·  Exercises with answers",
        color="#aebfd4", ha="center", va="center", fontsize=9.6, family="Source Sans 3")
ax.plot([0.55, W - 0.55], [1.75, 1.75], color=c, lw=1.2)
ax.text(W / 2, 1.05, "MARCUS J. THORNTON, PH.D.", color="white", ha="center", va="center",
        fontsize=19, family="Source Sans 3", fontweight="semibold")

fig.savefig(os.path.join(OUT, "cover.png"), dpi=256)
fig.savefig(os.path.join(OUT, "cover.jpg"), dpi=256, pil_kwargs={"quality": 93})
print("cover done")
