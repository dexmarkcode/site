from figlib import *

def arm(ax, sh, el, wr, style="B", lw=16):
    for p, q in ((sh, el), (el, wr)):
        ax.plot([p[0], q[0]], [p[1], q[1]], color="black", lw=lw, solid_capstyle="round", zorder=5)
        ax.plot([p[0], q[0]], [p[1], q[1]], color="white" if style == "B" else "black", lw=lw - 3, solid_capstyle="round", zorder=6)
    ax.add_patch(Circle(wr, 0.09, fc="white", ec="black", lw=1.2, zorder=7))

# 13.1 lever and fulcrum
fig = plt.figure(figsize=(4.5, 2.3))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(-0.2, 3.0); ax.set_ylim(-0.1, 1.55); ax.set_aspect("equal"); ax.axis("off")
sh, el, wr = (0.2, 0.75), (1.35, 0.75), (2.5, 0.75)
arm(ax, sh, el, wr)
ax.text(0.2, 1.05, "shoulder", ha="center", fontsize=7); ax.text(2.5, 1.05, "wrist", ha="center", fontsize=7)
ax.add_patch(Polygon([(1.2, 0.5), (1.5, 0.5), (1.35, 0.64)], fc="black", zorder=8))
numdot(ax, 1.35, 0.35, 1); ax.text(1.35, 0.17, "fulcrum: fixed just\nabove the elbow", ha="center", va="top", fontsize=6.5)
arrow(ax, (2.35, 1.35), (2.35, 0.9), lw=1.8); numdot(ax, 2.55, 1.3, 2)
ax.text(2.0, 1.42, "force at the wrist", ha="right", fontsize=6.5)
ax.annotate("", xy=(1.4, 1.2), xytext=(2.4, 1.2), arrowprops=dict(arrowstyle="<->", lw=0.7))
ax.text(1.9, 1.24, "long lever", ha="center", fontsize=6.5)
ax.plot([0.2, 1.35], [0.75, 0.75], color="black", lw=0)
save(fig, "fig13_1")

# 13.2 joints
fig = plt.figure(figsize=(4.5, 1.9))
def panel(rect, title):
    a = fig.add_axes(rect); a.set_xlim(-1, 1); a.set_ylim(-0.75, 0.9); a.set_aspect("equal"); a.set_xticks([]); a.set_yticks([])
    for s in a.spines.values(): s.set_linewidth(0.6)
    fig.text(rect[0] + rect[2] / 2, 0.06, title, ha="center", fontsize=7)
    return a
a = panel([0.01, 0.14, 0.31, 0.84], "Wrist")
arm(a, (-0.9, -0.1), (-0.5, -0.1), (0.15, -0.1), lw=14)
a.plot([0.15, 0.55], [-0.1, -0.1], color="black", lw=10, solid_capstyle="round")
a.add_patch(Arc((0.15, -0.1), 0.9, 0.9, theta1=10, theta2=75, lw=1.2)); arrow(a, (0.42, 0.25), (0.33, 0.33))
a.add_patch(Arc((0.15, -0.1), 0.9, 0.9, theta1=-75, theta2=-10, lw=1.2)); arrow(a, (0.42, -0.45), (0.33, -0.53))
a.text(0.0, 0.55, "bend forward / back\nand rotate", fontsize=5.8, ha="center")
b = panel([0.345, 0.14, 0.31, 0.84], "Elbow")
arm(b, (-0.9, -0.1), (0.0, -0.1), (0.85, -0.1), lw=14)
arrow(b, (0.0, 0.45), (0.0, 0.05), lw=1.6)
b.add_patch(Arc((0.0, -0.1), 1.3, 0.9, theta1=180 + 20, theta2=360 - 20, lw=1.0, ls=(0, (2, 2))))
b.text(0.0, 0.55, "hyperextend", fontsize=6, ha="center")
c = panel([0.68, 0.14, 0.31, 0.84], "Shoulder")
c.add_patch(Circle((-0.3, 0.0), 0.22, fc="white", ec="black", lw=1.2))
arm(c, (-0.3, 0.0), (0.25, -0.25), (0.6, 0.15), lw=12)
c.add_patch(Arc((-0.3, 0.0), 1.1, 1.1, theta1=-60, theta2=40, lw=1.2)); arrow(c, (0.12, 0.33), (0.0, 0.42))
c.text(0.1, 0.62, "rotate in / out", fontsize=6, ha="center")
save(fig, "fig13_2")
