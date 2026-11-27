from figlib import *

def A(**kw): kw.setdefault("style", "A"); return Person(**kw)
def B(**kw): kw.setdefault("style", "B"); return Person(**kw)

@titled("Circle your hand outward")
def w1(ax):
    A(hip=(-0.42, 0.88), face=1, lean=4, hands={"near": (0.0, 1.22), "far": (-0.1, 1.5)}, feet={"near": (-0.15, 0.06), "far": (-0.7, 0.06)}).draw(ax)
    B(hip=(0.42, 0.88), face=-1, lean=6, hands={"near": (0.02, 1.2), "far": (0.15, 1.5)}, feet={"near": (0.15, 0.06), "far": (0.7, 0.06)}).draw(ax)
    ax.add_patch(Arc((0.0, 1.22), 0.4, 0.4, theta1=200, theta2=340, lw=1.2)); arrow(ax, (0.18, 1.12), (0.2, 1.2))
@titled("Thumbs on their hand")
def w2(ax):
    A(hip=(-0.42, 0.88), face=1, lean=8, hands={"near": (0.0, 1.25), "far": (0.02, 1.3)}, feet={"near": (-0.15, 0.06), "far": (-0.7, 0.06)}, open_hand=("near", "far")).draw(ax)
    B(hip=(0.42, 0.88), face=-1, lean=8, hands={"near": (0.05, 1.28), "far": (0.15, 1.5)}, feet={"near": (0.15, 0.06), "far": (0.7, 0.06)}).draw(ax)
@titled("Large turn: they fall")
def w3(ax):
    A(hip=(-0.5, 0.86), face=1, lean=10, hands={"near": (-0.05, 0.95), "far": (-0.02, 1.0)}, feet={"near": (-0.25, 0.06), "far": (-0.8, 0.06)}, open_hand=("near", "far")).draw(ax)
    B(hip=(0.45, 0.6), face=-1, lean=-50, hands={"near": (0.0, 0.98), "far": (0.6, 1.05)}, feet={"near": (0.1, 0.06), "far": (0.85, 0.15)}).draw(ax)
    arrow(ax, (-0.15, 1.6), (0.7, 1.35), rad=-0.4)
sequence("fig14_1", [w1, w2, w3], cols=3, xlim=(-1.1, 1.15))

@titled("Pin the grabbing hand")
def l1(ax):
    A(hip=(-0.35, 0.88), face=1, lean=2, hands={"near": (-0.18, 1.32), "far": (-0.2, 1.45)}, feet={"near": (-0.1, 0.06), "far": (-0.62, 0.06)}, open_hand=("near", "far")).draw(ax)
    B(hip=(0.42, 0.88), face=-1, lean=8, hands={"near": (-0.2, 1.3), "far": (0.15, 1.5)}, feet={"near": (0.15, 0.06), "far": (0.7, 0.06)}).draw(ax)
@titled("Forearm over the wrist, bow forward")
def l2(ax):
    A(hip=(-0.42, 0.88), face=1, lean=18, hands={"near": (-0.05, 1.18), "far": (0.15, 1.1)}, epos={"far": (-0.05, 1.42)}, feet={"near": (-0.15, 0.06), "far": (-0.7, 0.06)}, open_hand=("near",)).draw(ax)
    B(hip=(0.42, 0.66), face=-1, lean=24, hands={"near": (-0.02, 1.15), "far": (0.15, 1.2)}, feet={"near": (0.1, 0.06), "far": (0.6, 0.06)}).draw(ax)
    arrow(ax, (0.4, 1.6), (0.35, 1.25))
sequence("fig14_2", [l1, l2], cols=2)

@titled("Bent-arm lock behind the back")
def h1(ax):
    b = B(hip=(0.3, 0.88), face=1, lean=25, hands={"near": (-0.05, 1.05), "far": (0.6, 1.2)}, epos={"near": (0.05, 1.5)},
          feet={"near": (0.6, 0.06), "far": (0.05, 0.06)})
    b.draw(ax, zbase=10)
    A(hip=(-0.35, 0.88), face=1, lean=12, hands={"near": (-0.02, 1.08), "far": (0.08, 1.35)}, open_hand=("near", "far"),
      feet={"near": (-0.05, 0.06), "far": (-0.6, 0.06)}).draw(ax, zbase=20)
    arrow(ax, (0.0, 1.55), (0.12, 1.85)); ax.text(0.2, 1.9, "lift the elbow", fontsize=6)
    arrow(ax, (0.9, 1.7), (1.1, 1.55), dashed=True); ax.text(0.75, 1.82, "driven forward", fontsize=6)
sequence("fig14_3", [h1], cols=1, width=3.6, xlim=(-1.1, 1.3))

@titled("Wrist lock escort")
def e1(ax):
    b = B(hip=(0.35, 0.9), face=1, lean=8, hands={"near": (0.0, 1.55), "far": (0.6, 1.25)}, epos={"near": (0.0, 1.25)},
          feet={"near": (0.6, 0.06), "far": (0.15, 0.06)}, open_hand=("near",))
    b.draw(ax, zbase=20)
    A(hip=(-0.25, 0.88), face=1, lean=5, hands={"near": (0.05, 1.58), "far": (0.0, 1.3)}, open_hand=("near",),
      feet={"near": (0.0, 0.06), "far": (-0.5, 0.06)}).draw(ax, zbase=10)
    tag(ax, -0.75, 1.65, "wrist bent,\nfingers down", 6); tag(ax, -0.75, 1.05, "elbow held\nto your side", 6)
    arrow(ax, (0.4, 0.35), (0.95, 0.35), dashed=True)
sequence("fig14_4", [e1], cols=1, width=3.6, xlim=(-1.1, 1.3))
