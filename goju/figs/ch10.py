from figlib import *

def bal(title, lean, hipx, cogshift):
    @titled(title)
    def p(ax):
        a = Person(hip=(hipx, 0.86), face=1, lean=lean, style="B",
                   hands={"near": (hipx + 0.35 + 0.5 * math.sin(math.radians(lean)), 1.35 if lean >= 0 else 1.55),
                          "far": (hipx + 0.25 + 0.5 * math.sin(math.radians(lean)), 1.3 if lean >= 0 else 1.5)},
                   feet={"near": (0.18, 0.06), "far": (-0.22, 0.06)})
        a.draw(ax)
        cx = hipx + 0.2 * math.sin(math.radians(lean)) + cogshift
        ax.add_patch(Circle((cx, 1.0), 0.06, fc="black", ec="black", zorder=60))
        ax.plot([cx, cx], [1.0, 0.02], color="black", lw=0.9, ls=(0, (2, 2)), zorder=59)
        ax.plot([-0.25, 0.4], [-0.02, -0.02], color="black", lw=4, zorder=58)
        ax.text(0.07, -0.1, "base", fontsize=6, ha="center", va="top")
    return p
sequence("fig10_1", [bal("Balanced", 2, -0.02, 0.0), bal("Broken forward", 38, 0.0, 0.32), bal("Broken backward", -26, 0.08, -0.32)],
         cols=3, xlim=(-0.85, 0.95), ylim=(-0.25, 2.0))

@titled("Eight directions (left foot forward)")
def e1(ax):
    footprint(ax, -0.15, 0.22, 90, "L", fill="white", s=1.3)
    footprint(ax, 0.18, -0.22, 90, "R", fill="white", s=1.3)
    for k in range(8):
        a = math.radians(90 - k * 45)
        bold = k in (1, 5)
        p0 = (0.42 * math.cos(a), 0.42 * math.sin(a))
        p1 = (0.82 * math.cos(a), 0.82 * math.sin(a))
        arrow(ax, p0, p1, lw=2.6 if bold else 0.9, head=12 if bold else 7)
    ax.text(0.0, 0.92, "front", ha="center", fontsize=6.5)
    ax.text(0.62, 0.42, "weak", fontsize=6.5, fontweight="bold")
    ax.text(-0.75, -0.48, "weak", fontsize=6.5, fontweight="bold")
plan_panels("fig10_2", [e1], width=3.0, lim=1.0)

@titled("Chin push: up and back")
def h1(ax):
    a = stance(-0.2, 1, "A", lean=14); a.hands["near"] = (0.58, 1.6); a.open_hand = ("near",); a.hands["far"] = (0.1, 1.3); a.draw(ax)
    b = Person(hip=(0.45, 0.88), face=-1, lean=-18, hands={"near": (0.05, 1.5), "far": (0.15, 1.45)},
               feet={"near": (0.25, 0.06), "far": (0.7, 0.06)}, style="B"); b.draw(ax)
    arrow(ax, (0.15, 1.9), (0.6, 2.0), rad=-0.2)
@titled("Head pull: down and forward")
def h2(ax):
    a = stance(-0.45, 1, "A", lean=4); a.hands["near"] = (0.0, 1.35); a.hands["far"] = (-0.05, 1.3); a.draw(ax)
    b = Person(hip=(0.42, 0.88), face=-1, lean=42, hands={"near": (-0.15, 1.0), "far": (-0.1, 0.95)},
               feet={"near": (0.18, 0.06), "far": (0.68, 0.06)}, style="B"); b.draw(ax)
    arrow(ax, (0.25, 1.65), (-0.15, 1.25), rad=0.3)
sequence("fig10_3", [h1, h2], cols=2)
