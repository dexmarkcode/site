from figlib import *

def kpair(ax, ah, bh, a_far=None, b_far=None, a_open=("near",), b_open=("near",), alean=3, blean=3):
    a = Person(hip=(-0.42, 0.9), face=1, lean=alean, hands={"near": ah, "far": a_far or (-0.1, 1.4)},
               feet={"near": (-0.15, 0.06), "far": (-0.7, 0.06)}, open_hand=a_open)
    b = Person(hip=(0.42, 0.9), face=-1, lean=blean, hands={"near": bh, "far": b_far or (0.1, 1.4)},
               feet={"near": (0.15, 0.06), "far": (0.7, 0.06)}, open_hand=b_open, style="B")
    a.draw(ax); b.draw(ax)

@titled("Wrists touching at chest height")
def f1(ax):
    kpair(ax, (0.0, 1.45), (0.0, 1.45))
    impact(ax, 0.0, 1.47, r=0.0, n=1)
    tag(ax, 0.0, 1.85, "contact point", 6)
    ax.annotate("", xy=(0.0, 1.5), xytext=(0.0, 1.78), arrowprops=dict(arrowstyle="-", lw=0.6))
    tag(ax, -0.85, 0.95, "elbow\ndown", 6); tag(ax, 0.85, 1.75, "free hand\nnear chest", 6)
sequence("fig4_1", [f1], cols=1, width=3.6)

@titled("You push, partner yields")
def c1(ax):
    kpair(ax, (0.22, 1.55), (0.22, 1.55), alean=8, blean=-3)
    arrow(ax, (-0.15, 1.82), (0.25, 1.82))
@titled("Partner turns the push aside")
def c2(ax):
    kpair(ax, (0.12, 1.32), (0.12, 1.32), alean=5, blean=2)
    arrow(ax, (0.32, 1.65), (0.3, 1.2), rad=-0.5)
@titled("Partner pushes, you yield")
def c3(ax):
    kpair(ax, (-0.22, 1.5), (-0.22, 1.5), alean=-3, blean=8)
    arrow(ax, (0.15, 1.82), (-0.25, 1.82))
sequence("fig4_2", [c1, c2, c3], cols=3)

@titled("Double-arm contact")
def d1(ax):
    kpair(ax, (0.02, 1.52), (0.02, 1.52), a_far=(0.0, 1.25), b_far=(0.0, 1.25), a_open=("near", "far"), b_open=("near", "far"))
    tag(ax, 0.55, 1.95, "upper contact", 6); tag(ax, -0.75, 1.0, "lower contact", 6)
sequence("fig4_3", [d1], cols=1, width=3.6)
