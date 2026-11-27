from figlib import *

def elb(a, side="far", up=1.62, fwd=0.08, where="in"):
    x = a.hip[0]; f = a.face
    a.hands[side] = (x + f * (0.25 + fwd) + f * 0.5 * math.sin(math.radians(a.lean)) * 0.0, up)
    a.elbow[side] = where

@titled("Arm raised, hand by the ear")
def h1(ax):
    a = stance(-0.32, 1, "A", lean=6); a.hands["far"] = (-0.12, 1.62); a.epos["far"] = (-0.45, 1.58); a.draw(ax)
    stance(0.48, -1, "B").draw(ax)
@titled("Turn: elbow across to the jaw")
def h2(ax):
    a = stance(-0.25, 1, "A", lean=14); a.hands["far"] = (-0.05, 1.68); a.epos["far"] = (0.4, 1.62); a.draw(ax)
    b = stance(0.5, -1, "B", lean=-8); b.draw(ax)
    impact(ax, 0.38, 1.72); arrow(ax, (-0.2, 1.95), (0.2, 1.95), rad=-0.3)
sequence("fig7_1", [h1, h2], cols=2)

def solo(title, hand, ep, lean=8, mark=None, arr=None, hip_h=0.86, side="near", face=1):
    @titled(title)
    def p(ax):
        a = stance(0.0, face, "A", lean=lean, hip_h=hip_h)
        a.hands[side] = hand; a.epos[side] = ep
        a.hands["far"] = (0.12 * face, 1.62)
        j = a.draw(ax)
        if arr: arrow(ax, *arr)
        if mark:
            ex, ey = j[side + "_el"]
            impact(ax, ex + 0.06 * face, ey)
    return p
P = [solo("Horizontal", (0.02, 1.58), (0.5, 1.48), lean=10, arr=((0.05, 1.85), (0.6, 1.62), -0.3), mark=(0.42, 1.52)),
     solo("Rising", (0.1, 1.98), (0.32, 1.85), lean=6, arr=((0.5, 1.2), (0.5, 1.8), 0), mark=(0.3, 1.88)),
     solo("Downward", (0.12, 1.42), (0.38, 0.95), lean=30, hip_h=0.78, arr=((0.62, 1.55), (0.62, 1.0), 0), mark=(0.42, 0.97)),
     solo("Forward", (0.0, 1.38), (0.6, 1.3), lean=14, arr=((0.45, 1.12), (0.85, 1.12), 0), mark=(0.42, 1.3)),
     solo("Backward", (-0.12, 1.38), (0.5, 1.28), lean=-2, face=-1, arr=((0.3, 1.1), (0.7, 1.1), 0), mark=(0.34, 1.28)),
     solo("Downward diagonal", (0.02, 1.66), (0.55, 1.62), lean=16, arr=((0.25, 1.95), (0.7, 1.45), -0.2), mark=(0.48, 1.58))]
sequence("fig7_2", P, cols=3, xlim=(-0.9, 1.0))

# 7.3 target map
fig = plt.figure(figsize=(3.6, 3.9))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(-1.1, 1.1); ax.set_ylim(-0.05, 2.0); ax.set_aspect("equal"); ax.axis("off")
front_body(ax)
pts = [(0.0, 1.62, "nose and face", False, "r"), (0.09, 1.55, "jaw", True, "l"), (0.1, 1.71, "temple", False, "r"),
       (0.12, 1.47, "collarbone", False, "r"), (0.0, 1.2, "solar plexus", True, "l"), (-0.17, 1.12, "ribs", True, "l"),
       (0.28, 0.95, "arm / bicep", True, "r"), (-0.12, 0.62, "thigh", True, "l")]
for x, y, t, safe, side in pts:
    x = -abs(x) if side == "l" else abs(x)
    ax.add_patch(Circle((x, y), 0.035, fc="black" if safe else "white", ec="black", lw=1.1, zorder=20))
    tx = -0.95 if side == "l" else 0.95
    ax.plot([x, tx * 0.62], [y, y], color="black", lw=0.5, zorder=19)
    ax.text(tx * 0.64, y, t, fontsize=6.5, ha="right" if side == "l" else "left", va="center")
ax.add_patch(Circle((0.25, 0.32), 0.035, fc="black", ec="black")); ax.text(0.32, 0.32, "training target (with protection)", fontsize=6, va="center")
ax.add_patch(Circle((0.25, 0.2), 0.035, fc="white", ec="black")); ax.text(0.32, 0.2, "pads or genuine self-defence only", fontsize=6, va="center")
save(fig, "fig7_3")

@titled("Hook the wrist")
def r1(ax):
    a = stance(-0.42, 1, "A", lean=6); a.hands["near"] = (0.02, 1.45); a.open_hand = ("near",); a.draw(ax)
    b = stance(0.45, -1, "B"); b.hands["near"] = (0.0, 1.45); b.draw(ax)
@titled("Pull: head comes forward")
def r2(ax):
    a = stance(-0.45, 1, "A", lean=2); a.hands["near"] = (-0.3, 1.05); a.draw(ax)
    b = Person(hip=(0.32, 0.86), face=-1, lean=28, hands={"near": (-0.28, 1.07), "far": (-0.02, 1.4)},
               feet={"near": (0.02, 0.06), "far": (0.65, 0.06)}, style="B"); b.draw(ax)
    arrow(ax, (0.1, 0.85), (-0.3, 0.85))
@titled("Rising elbow")
def r3(ax):
    a = stance(-0.45, 1, "A", lean=8); a.hands["near"] = (-0.32, 1.05); a.hands["far"] = (-0.45, 1.6); a.epos["far"] = (-0.12, 1.75); a.draw(ax)
    b = Person(hip=(0.3, 0.86), face=-1, lean=32, hands={"near": (-0.3, 1.07), "far": (-0.05, 1.35)},
               feet={"near": (0.0, 0.06), "far": (0.65, 0.06)}, style="B"); b.draw(ax)
    impact(ax, -0.08, 1.6); arrow(ax, (-0.7, 1.2), (-0.7, 1.75))
sequence("fig7_4", [r1, r2, r3], cols=3)
