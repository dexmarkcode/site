from figlib import *

# 2.1 sanchin stance: plan view + side view
fig = plt.figure(figsize=(4.5, 2.6))
ax = plan_axes(fig, [0.01, 0.08, 0.48, 0.9], lim=0.55)
footprint(ax, -0.14, -0.12, 100, "L", s=1.3)
footprint(ax, 0.14, 0.14, 80, "R", s=1.3)
ax.plot([-0.4, 0.4], [-0.02 + 0.0, -0.02], color="black", lw=0.5, ls=":")
ax.annotate("", xy=(-0.14, -0.44), xytext=(0.14, -0.44), arrowprops=dict(arrowstyle="<->", lw=0.7))
ax.text(0, -0.5, "about shoulder width", ha="center", va="top", fontsize=6)
ax.text(0.5, 0.42, "front heel level\nwith rear toes", fontsize=6, ha="right", va="center")
ax.plot([0.0, 0.3], [0.0, 0.0], color="black", lw=0)
ax.text(-0.5, 0.48, "Seen from above", fontsize=7, fontweight="bold", va="top")
ax2 = panel_axes(fig, [0.51, 0.08, 0.48, 0.9], xlim=(-0.8, 0.8), ylim=(-0.1, 2.0))
ground(ax2, -0.8, 0.8)
p = Person(hip=(0, 0.88), face=1, lean=0, hands={"near": (0.34, 1.45), "far": (0.3, 1.42)},
           feet={"near": (0.14, 0.06), "far": (-0.14, 0.06)}, style="A")
p.draw(ax2)
ax2.plot([0.0, 0.0], [0.05, 1.9], color="black", lw=0.6, ls=(0, (2, 2)), zorder=80)
ax2.text(-0.75, 1.9, "Seen from the side", fontsize=7, fontweight="bold", va="top")
tag(ax2, -0.5, 0.9, "pelvis\ntucked", 5.8)
tag(ax2, 0.55, 1.15, "elbows\ndown", 5.8)
tag(ax2, 0.5, 0.45, "knees press\ngently in", 5.8)
save(fig, "fig2_1")

# 2.2 elbow alignment
@titled("Elbow down: the push is carried")
def e1(ax):
    a = Person(hip=(-0.35, 0.9), face=1, lean=4, hands={"near": (0.05, 1.5), "far": (-0.05, 1.42)},
               feet={"near": (-0.05, 0.06), "far": (-0.65, 0.06)})
    a.draw(ax)
    b = stance(0.6, -1, "B", lean=-14); b.hands["near"] = (0.12, 1.5); b.hands["far"] = (0.2, 1.3); b.draw(ax)
    arrow(ax, (0.55, 1.75), (0.15, 1.6))
    ax.plot([0.02, -0.15, -0.3, -0.35, -0.5], [1.5, 1.2, 1.38, 0.9, 0.08], color="black", lw=0.9, ls=(0, (2, 2)), zorder=80)
    tag(ax, -0.85, 0.6, "force to\nthe floor", 6)
@titled("Elbow flared: the arm folds")
def e2(ax):
    a = Person(hip=(-0.35, 0.9), face=1, lean=-6, hands={"near": (-0.02, 1.58), "far": (-0.05, 1.42)},
               feet={"near": (-0.05, 0.06), "far": (-0.65, 0.06)}, elbow={"near": 1, "far": -1})
    a.draw(ax)
    b = stance(0.55, -1, "B", lean=-14); b.hands["near"] = (0.05, 1.58); b.hands["far"] = (0.15, 1.3); b.draw(ax)
    arrow(ax, (0.55, 1.85), (0.0, 1.7))
    impact(ax, -0.2, 1.62, r=0.07)
    tag(ax, -0.55, 0.6, "arm collapses\ninto the body", 6)
sequence("fig2_2", [e1, e2], cols=2)

# 2.3 shime test points
@titled("Shime: where the partner checks")
def s1(ax):
    a = Person(hip=(0, 0.88), face=1, lean=0, hands={"near": (0.36, 1.45), "far": (0.3, 1.42)},
               feet={"near": (0.15, 0.06), "far": (-0.15, 0.06)}, style="A")
    a.draw(ax)
    pts = [((0.55, 1.75), (0.12, 1.42), 1), ((0.85, 1.45), (0.42, 1.45), 2), ((-0.6, 1.25), (-0.15, 1.25), 3),
           ((0.6, 1.05), (0.13, 1.05), 4), ((-0.6, 0.8), (-0.13, 0.85), 5), ((0.6, 0.55), (0.2, 0.55), 6)]
    for p, q, n in pts:
        arrow(ax, p, q)
        numdot(ax, p[0] + (0.06 if p[0] > 0 else -0.06), p[1], n)
    ax.text(1.18, 1.95, "1 shoulders\n2 forearms\n3 upper back\n4 abdomen\n5 hips\n6 thighs", fontsize=6, va="top", ha="right")
sequence("fig2_3", [s1], cols=1, width=3.4, xlim=(-1.2, 1.2))

# 2.4 hip errors
def single(lean, hipx, title, ok=False):
    @titled(title)
    def p(ax):
        a = Person(hip=(hipx, 0.85), face=1, lean=lean, hands={"near": (hipx + 0.45 + 0.6 * math.sin(math.radians(lean)), 1.45),
                   "far": (hipx + 0.35 + 0.6 * math.sin(math.radians(lean)), 1.4)},
                   feet={"near": (0.22, 0.06), "far": (-0.28, 0.06)})
        j = a.draw(ax)
        ax.plot([j["head"][0], j["head"][0]], [j["head"][1], 0.05], color="black", lw=0.7, ls=(0, (2, 2)), zorder=80)
        ax.plot([-0.28, 0.42], [0.02, 0.02], color="black", lw=3, zorder=79)
        tag(ax, 0, -0.0 + 1.98, "GOOD" if ok else "WEAK", 6)
    return p
sequence("fig2_4", [single(32, -0.2, "Hips back, head forward"), single(-20, 0.15, "Hips forward, head back"),
                    single(3, -0.02, "Head over hips over feet", True)], cols=3, xlim=(-0.9, 0.9))
