from figlib import *
from matplotlib.patches import FancyBboxPatch

# 18.1 layers
fig = plt.figure(figsize=(4.0, 3.4))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(-2, 2); ax.set_ylim(-1.7, 1.7); ax.set_aspect("equal"); ax.axis("off")
layers = ["1 Awareness", "2 Avoidance", "3 De-escalation", "4 Escape", "5 Physical"]
for i, t in enumerate(layers):
    r = 1.6 - i * 0.3
    ax.add_patch(Circle((0, 0), r, fc="black" if i == 4 else ("#f2f2f2" if i % 2 == 0 else "white"), ec="black", lw=1))
    ax.text(0, r - 0.15 if i < 4 else 0, t, ha="center", va="center", fontsize=7.5 if i < 4 else 7,
            fontweight="bold", color="white" if i == 4 else "black")
save(fig, "fig18_1")

# 18.2 fence
@titled("The fence")
def f1(ax):
    a = Person(hip=(-0.4, 0.88), face=1, lean=4, hands={"near": (0.08, 1.48), "far": (-0.05, 1.42)},
               feet={"near": (-0.15, 0.06), "far": (-0.68, 0.06)}, open_hand=("near", "far"), elbow={"near": -1, "far": -1})
    a.draw(ax)
    b = stance(0.55, -1, "B", lean=8, guard="low"); b.hands["near"] = (0.25, 1.55); b.open_hand = ("near",); b.draw(ax)
    ax.annotate("", xy=(0.1, 0.3), xytext=(0.55, 0.3), arrowprops=dict(arrowstyle="<->", lw=0.7))
    ax.text(0.33, 0.36, "edge of reach", fontsize=6, ha="center")
    tag(ax, -0.85, 1.85, "open hands,\nelbows down", 6); tag(ax, -0.95, 0.7, "soft knees", 6)
sequence("fig18_2", [f1], cols=1, width=3.6, xlim=(-1.25, 1.25))

# 18.3 aftermath flow
fig = plt.figure(figsize=(4.5, 2.2))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 4.5); ax.set_ylim(0, 2.2); ax.axis("off")
steps = ["Get safe", "Check for\ninjuries", "Call 999\nif needed", "Legal advice\nbefore statement", "Note witnesses\nand cameras", "Write your\naccount", "Look after\nyourself"]
pos = [(0.55, 1.65), (1.7, 1.65), (2.85, 1.65), (4.0, 1.65), (3.45, 0.55), (2.25, 0.55), (1.05, 0.55)]
for i, (t, (x, y)) in enumerate(zip(steps, pos)):
    ax.add_patch(FancyBboxPatch((x - 0.48, y - 0.27), 0.96, 0.54, boxstyle="round,pad=0.02,rounding_size=0.06",
                                fc="black" if i in (0, 6) else "white", ec="black", lw=0.9))
    ax.text(x, y, t, ha="center", va="center", fontsize=6.6, color="white" if i in (0, 6) else "black", fontweight="bold")
for i in range(6):
    (x0, y0), (x1, y1) = pos[i], pos[i + 1]
    if y0 == y1:
        d = 0.5 if x1 > x0 else -0.5
        arrow(ax, (x0 + d, y0), (x1 - d, y1), head=6)
    else:
        arrow(ax, (x0, y0 - 0.29), (x1 + 0.2, y1 + 0.29), head=6)
save(fig, "fig18_3")
