from figlib import *
def A(**kw): kw.setdefault("style", "A"); return Person(**kw)
def B(**kw): kw.setdefault("style", "B"); return Person(**kw)

@titled("Wrist gripped")
def g1(ax):
    A(hip=(-0.42, 0.88), face=1, lean=2, hands={"near": (0.02, 1.15), "far": (-0.15, 1.42)}, feet={"near": (-0.15, 0.06), "far": (-0.7, 0.06)}).draw(ax)
    B(hip=(0.42, 0.88), face=-1, lean=6, hands={"near": (0.04, 1.15), "far": (0.15, 1.45)}, feet={"near": (0.15, 0.06), "far": (0.7, 0.06)}).draw(ax)
@titled("Rotate towards the thumb")
def g2(ax):
    A(hip=(-0.32, 0.88), face=1, lean=10, hands={"near": (0.04, 1.32), "far": (-0.05, 1.5)}, epos={"near": (0.1, 1.05)}, feet={"near": (-0.05, 0.06), "far": (-0.6, 0.06)}).draw(ax)
    B(hip=(0.42, 0.88), face=-1, lean=6, hands={"near": (0.05, 1.28), "far": (0.15, 1.45)}, feet={"near": (0.15, 0.06), "far": (0.7, 0.06)}).draw(ax)
    arrow(ax, (-0.25, 0.85), (0.05, 1.0), rad=-0.2)
    ax.add_patch(Arc((0.04, 1.32), 0.35, 0.35, theta1=20, theta2=160, lw=1.1)); arrow(ax, (-0.12, 1.38), (-0.14, 1.32))
@titled("Free, near the face")
def g3(ax):
    A(hip=(-0.3, 0.88), face=1, lean=10, hands={"near": (0.32, 1.72), "far": (-0.05, 1.5)}, open_hand=("near",), feet={"near": (-0.05, 0.06), "far": (-0.6, 0.06)}).draw(ax)
    B(hip=(0.45, 0.88), face=-1, lean=-4, hands={"near": (0.1, 1.1), "far": (0.2, 1.45)}, feet={"near": (0.18, 0.06), "far": (0.72, 0.06)}).draw(ax)
    impact(ax, 0.4, 1.74)
sequence("fig15_1", [g1, g2, g3], cols=3)

def hug(ax, a_hip=(0.1, 0.88), drop=0.0, a_lean=4, b_hands=None, a_feet=None):
    hy = a_hip[1] - drop
    b = B(hip=(a_hip[0] - 0.28, 0.9), face=1, lean=10, hands=b_hands or {"near": (a_hip[0] + 0.12, hy + 0.35), "far": (a_hip[0] + 0.1, hy + 0.32)},
          feet={"near": (a_hip[0] - 0.05, 0.06), "far": (a_hip[0] - 0.55, 0.06)})
    b.draw(ax, zbase=5)
    a = A(hip=(a_hip[0], hy), face=1, lean=a_lean, hands={"near": (a_hip[0] + 0.25, hy + 0.15), "far": (a_hip[0] + 0.22, hy + 0.12)},
          feet=a_feet or {"near": (a_hip[0] + 0.3, 0.06), "far": (a_hip[0] - 0.2, 0.06)})
    a.draw(ax, zbase=10)
    # B's arms wrapping in front (near arm drawn over A)
    ax.plot([a_hip[0] - 0.1, a_hip[0] + 0.14], [hy + 0.38, hy + 0.36], color="black", lw=7, solid_capstyle="round", zorder=30)
    ax.plot([a_hip[0] - 0.1, a_hip[0] + 0.14], [hy + 0.38, hy + 0.36], color="white", lw=4.5, solid_capstyle="round", zorder=31)
@titled("Drop your weight, widen")
def h1(ax):
    hug(ax, drop=0.14, a_feet={"near": (0.45, 0.06), "far": (-0.25, 0.06)})
    arrow(ax, (0.55, 1.6), (0.55, 1.25))
@titled("Heel stamp on the foot")
def h2(ax):
    hug(ax, drop=0.12, a_feet={"near": (0.4, 0.06), "far": (-0.12, 0.12)})
    impact(ax, -0.15, 0.1)
@titled("Step aside, turn, elbow")
def h3(ax):
    B(hip=(-0.25, 0.9), face=1, lean=4, hands={"near": (0.05, 1.25), "far": (0.0, 1.2)}, feet={"near": (0.0, 0.06), "far": (-0.5, 0.06)}).draw(ax, zbase=5)
    A(hip=(0.38, 0.86), face=-1, lean=8, hands={"near": (0.25, 1.55), "far": (0.45, 1.5)}, epos={"near": (-0.05, 1.55)},
      feet={"near": (0.15, 0.06), "far": (0.65, 0.06)}).draw(ax, zbase=10)
    impact(ax, -0.1, 1.62)
    arrow(ax, (0.7, 0.35), (0.35, 0.3), rad=0.4)
sequence("fig15_2", [h1, h2, h3], cols=3)

def neck(ax, drop=0.0, turn=False):
    hy = 0.88 - drop
    B(hip=(-0.22, 0.9), face=1, lean=12, hands={"near": (0.15, 1.42 - drop * 0.5), "far": (0.0, 1.5)},
      epos={"near": (0.25, 1.22 - drop)}, feet={"near": (0.05, 0.06), "far": (-0.5, 0.06)}).draw(ax, zbase=20 if not turn else 5)
    A(hip=(0.12, hy), face=1, lean=4, hands={"near": (0.22, 1.5 - drop), "far": (0.2, 1.46 - drop)},
      feet={"near": (0.4, 0.06), "far": (-0.1, 0.06)}).draw(ax, zbase=10)
@titled("Chin tucked, pull the forearm")
def n1(ax):
    neck(ax)
    arrow(ax, (0.6, 1.6), (0.6, 1.3))
@titled("Drop and turn to the elbow")
def n2(ax):
    neck(ax, drop=0.18, turn=True)
    ax.add_patch(Arc((0.12, 1.2), 0.7, 0.4, theta1=200, theta2=340, lw=1.2)); arrow(ax, (0.4, 1.08), (0.45, 1.12))
@titled("Head slides free, elbow back")
def n3(ax):
    B(hip=(-0.3, 0.9), face=1, lean=8, hands={"near": (0.0, 1.45), "far": (-0.05, 1.4)}, feet={"near": (-0.05, 0.06), "far": (-0.55, 0.06)}).draw(ax, zbase=5)
    A(hip=(0.15, 0.82), face=1, lean=-10, hands={"near": (0.3, 1.2), "far": (0.35, 1.5)}, epos={"near": (-0.25, 1.1)},
      feet={"near": (0.45, 0.06), "far": (-0.1, 0.06)}).draw(ax, zbase=10)
    impact(ax, -0.25, 1.1)
sequence("fig15_3", [n1, n2, n3], cols=3)
