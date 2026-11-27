from figlib import *

@titled("Good: inside control, posture broken")
def g1(ax):
    a = Person(hip=(-0.4, 0.9), face=1, lean=8, hands={"near": (0.2, 1.52), "far": (0.16, 1.48)},
               feet={"near": (-0.15, 0.06), "far": (-0.7, 0.06)}); a.draw(ax)
    b = Person(hip=(0.5, 0.86), face=-1, lean=38, hands={"near": (-0.1, 1.15), "far": (-0.05, 1.1)},
               feet={"near": (0.2, 0.06), "far": (0.75, 0.06)}, style="B"); b.draw(ax)
    arrow(ax, (0.55, 1.75), (0.35, 1.45))
@titled("Poor: head pulled down")
def g2(ax):
    a = Person(hip=(-0.5, 0.86), face=1, lean=38, hands={"near": (0.1, 1.15), "far": (0.05, 1.1)},
               feet={"near": (-0.2, 0.06), "far": (-0.75, 0.06)}); a.draw(ax)
    b = Person(hip=(0.4, 0.9), face=-1, lean=8, hands={"near": (-0.2, 1.52), "far": (-0.16, 1.48)},
               feet={"near": (0.15, 0.06), "far": (0.7, 0.06)}, style="B"); b.draw(ax)
    tag(ax, -0.6, 1.85, "DANGER", 6)
sequence("fig9_1", [g1, g2], cols=2)

def pos(title, ah, af, bh, bf, ae=None, alean=8, blean=8):
    @titled(title)
    def p(ax):
        a = Person(hip=(-0.32, 0.9), face=1, lean=alean, hands={"near": ah, "far": af},
                   feet={"near": (-0.08, 0.06), "far": (-0.6, 0.06)}, epos=ae or {}); a.draw(ax)
        b = Person(hip=(0.32, 0.9), face=-1, lean=blean, hands={"near": bh, "far": bf},
                   feet={"near": (0.08, 0.06), "far": (0.6, 0.06)}, style="B"); b.draw(ax)
    return p
sequence("fig9_2", [pos("Double collar tie", (0.3, 1.6), (0.26, 1.58), (-0.05, 1.32), (0.0, 1.28), alean=10, blean=14),
                    pos("Collar and elbow", (0.3, 1.6), (0.15, 1.25), (-0.15, 1.5), (-0.1, 1.25)),
                    pos("Double underhooks", (0.4, 1.3), (0.36, 1.25), (-0.25, 1.55), (-0.2, 1.5), ae={"near": (0.1, 1.15), "far": (0.08, 1.1)}),
                    pos("Overhook and arm tie", (0.1, 1.15), (0.2, 1.42), (-0.1, 1.4), (-0.25, 1.2), ae={"near": (0.25, 1.4)})],
         cols=2, width=4.2, xlim=(-0.95, 0.95))

def wall(ax):
    ax.add_patch(Rectangle((-1, 0.62), 2, 0.12, fc="#bbbbbb", ec="black", lw=0.8, hatch="////"))
    ax.text(0.0, 0.85, "WALL", fontsize=6.5, ha="center", fontweight="bold")
@titled("Pinned square-on")
def w1(ax):
    wall(ax)
    top_person(ax, 0, 0.4, 270, "A", lhand=(0.15, 0.05), rhand=(-0.15, 0.05))
    top_person(ax, 0, -0.25, 90, "B", lhand=(-0.15, 0.25), rhand=(0.15, 0.25))
@titled("Underhook, shoulder to wall")
def w2(ax):
    wall(ax)
    top_person(ax, -0.05, 0.38, 330, "A", lhand=(0.25, 0.0), rhand=(0.15, -0.15))
    top_person(ax, 0.05, -0.28, 100, "B", lhand=(-0.2, 0.2), rhand=(0.2, 0.25))
    arrow(ax, (-0.45, 0.25), (-0.3, 0.0), rad=0.3)
@titled("Step along and reverse")
def w3(ax):
    wall(ax)
    top_person(ax, 0.35, 0.38, 270, "B")
    top_person(ax, 0.3, -0.3, 80, "A", lhand=(0.15, 0.15), rhand=(0.45, 0.15))
    arrow(ax, (-0.45, 0.2), (0.05, -0.35), rad=0.4)
plan_panels("fig9_3", [w1, w2, w3], lim=1.0)
