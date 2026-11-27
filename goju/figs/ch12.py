from figlib import *

def P(**kw):
    kw.setdefault("style", "A")
    return Person(**kw)

@titled("Squat, chin tucked")
def b1(ax):
    P(hip=(0.0, 0.5), face=1, lean=35, hands={"near": (0.3, 0.95), "far": (0.28, 0.92)},
      feet={"near": (0.25, 0.06), "far": (0.15, 0.06)}).draw(ax)
@titled("Roll onto the rounded back")
def b2(ax):
    P(hip=(0.05, 0.22), face=1, lean=-55, head=60, hands={"near": (0.2, 0.75), "far": (0.18, 0.72)},
      feet={"near": (0.55, 0.45), "far": (0.5, 0.4)}).draw(ax)
    arrow(ax, (0.6, 1.05), (-0.3, 0.95), rad=0.4)
@titled("Arms strike the mat")
def b3(ax):
    P(hip=(0.25, 0.2), face=1, lean=-78, head=65, hands={"near": (-0.7, 0.06), "far": (-0.75, 0.08)},
      feet={"near": (0.75, 0.75), "far": (0.7, 0.68)}, knee={"near": -1, "far": -1}).draw(ax)
    impact(ax, -0.75, 0.08)
    tag(ax, -0.2, 0.75, "head clear", 6)
sequence("fig12_1", [b1, b2, b3], cols=3, xlim=(-1.0, 1.0), ylim=(-0.12, 1.4))

@titled("Side breakfall")
def s1(ax):
    P(hip=(0.15, 0.18), face=1, lean=-82, head=55, hands={"near": (-0.6, 0.06), "far": (0.0, 0.55)},
      feet={"near": (0.75, 0.12), "far": (0.65, 0.4)}).draw(ax)
    impact(ax, -0.65, 0.08)
    arrow(ax, (-0.2, 0.9), (-0.55, 0.3), rad=0.3)
@titled("Forward roll")
def s2(ax):
    P(hip=(-0.45, 0.6), face=1, lean=60, head=40, hands={"near": (-0.05, 0.08), "far": (-0.1, 0.25)},
      feet={"near": (-0.6, 0.06), "far": (-0.75, 0.1)}).draw(ax)
    ax.add_patch(Arc((0.4, 0.42), 0.75, 0.75, theta1=-40, theta2=200, lw=1.3, ls=(0, (3, 2))))
    arrow(ax, (0.68, 0.18), (0.72, 0.1))
    ax.text(0.4, 0.42, "shoulder\nto opposite\nhip", ha="center", va="center", fontsize=6)
sequence("fig12_2", [s1, s2], cols=2, xlim=(-1.0, 1.0), ylim=(-0.12, 1.4))

@titled("Feet towards the opponent, head guarded")
def g1(ax):
    P(hip=(-0.35, 0.18), face=1, lean=-80, head=60, hands={"near": (-0.78, 0.48), "far": (-0.82, 0.42)},
      feet={"near": (0.3, 0.5), "far": (0.2, 0.3)}, knee={"near": -1, "far": -1}, elbow={"near": 1, "far": 1}).draw(ax)
    stance(0.75, -1, "B", lean=10).draw(ax)
    arrow(ax, (-0.2, 0.85), (0.15, 0.85), dashed=True)
sequence("fig12_3", [g1], cols=1, width=3.8, xlim=(-1.2, 1.3))

@titled("Post hand, plant foot")
def t1(ax):
    P(hip=(-0.1, 0.18), face=1, lean=-35, hands={"near": (0.35, 0.9), "far": (-0.55, 0.06)}, open_hand=("near",),
      feet={"near": (0.35, 0.06), "far": (0.6, 0.06)}).draw(ax)
@titled("Lift the hips")
def t2(ax):
    P(hip=(-0.1, 0.42), face=1, lean=-30, hands={"near": (0.35, 1.05), "far": (-0.55, 0.06)}, open_hand=("near",),
      feet={"near": (0.3, 0.06), "far": (0.15, 0.3)}).draw(ax)
    arrow(ax, (0.0, 0.05), (0.0, 0.35))
@titled("Swing the leg back")
def t3(ax):
    P(hip=(-0.15, 0.5), face=1, lean=-5, hands={"near": (0.3, 1.15), "far": (-0.5, 0.1)}, open_hand=("near",),
      feet={"near": (0.25, 0.06), "far": (-0.55, 0.06)}).draw(ax)
    arrow(ax, (0.15, 0.25), (-0.5, 0.2), rad=-0.4)
@titled("Guarded stance")
def t4(ax):
    stance(-0.05, 1, "A", lean=4, hip_h=0.82).draw(ax)
sequence("fig12_4", [t1, t2, t3, t4], cols=4, width=4.6, xlim=(-0.85, 0.85), ylim=(-0.12, 1.9))
