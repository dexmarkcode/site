from figlib import *
from matplotlib.patches import FancyBboxPatch

fig = plt.figure(figsize=(4.5, 2.6))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 4.5); ax.set_ylim(0, 2.6); ax.axis("off")
rows = [("Go no sen", 2.05, 3.15, 3.95, "defend, then counter"),
        ("Sen no sen", 1.35, 2.45, 2.95, "counter as it develops"),
        ("Sen sen no sen", 0.65, 1.5, 2.15, "act as the intention forms")]
ax.plot([1.4, 4.35], [0.25, 0.25], color="black", lw=0.9)
arrow(ax, (4.2, 0.25), (4.4, 0.25), head=7)
for x, t in ((1.55, "intention"), (2.35, "attack starts"), (3.15, "attack lands")):
    ax.plot([x, x], [0.2, 2.45], color="#999999", lw=0.6, ls=(0, (2, 2)))
    ax.text(x, 0.12, t, ha="center", va="top", fontsize=6.3)
for name, y, x0, x1, note in rows:
    ax.text(0.1, y, name, fontsize=7.5, fontweight="bold", va="center")
    ax.add_patch(FancyBboxPatch((2.35, y - 0.11), 0.8, 0.22, boxstyle="round,pad=0.0,rounding_size=0.05", fc="white", ec="black", lw=0.8))
    ax.text(2.4, y + 0.2, "their attack", fontsize=5.5, va="bottom")
    ax.add_patch(FancyBboxPatch((x0, y - 0.07), x1 - x0, 0.14, boxstyle="round,pad=0.0,rounding_size=0.04", fc="black", ec="black"))
    ax.text(x0, y - 0.18, note, fontsize=6, style="italic", va="top")
ax.text(4.4, 2.5, "time", fontsize=6.5, ha="right")
save(fig, "fig16_1")

@titled("Angled counter v punch")
def c1(ax):
    b = stance(0.5, -1, "B", lean=10); b.hands["near"] = (-0.3, 1.75); b.draw(ax)
    a = stance(-0.32, 1, "A", lean=12); a.hands["far"] = (0.42, 1.72); a.hands["near"] = (-0.1, 1.68); a.draw(ax)
    impact(ax, 0.48, 1.75); arrow(ax, (-0.7, 0.25), (-0.4, 0.4), rad=-0.3)
@titled("Step-in jam v hook")
def c2(ax):
    b = stance(0.45, -1, "B", lean=6); b.hands["far"] = (0.0, 1.62); b.elbow["far"] = 1; b.draw(ax)
    a = stance(-0.25, 1, "A", lean=14); a.hands["near"] = (-0.05, 1.82); a.epos = {"near": (0.12, 1.6)}; a.hands["far"] = (0.38, 1.7); a.draw(ax)
    impact(ax, 0.45, 1.72)
@titled("Pivot and pass v push")
def c3(ax):
    b = Person(hip=(0.3, 0.88), face=-1, lean=22, hands={"near": (-0.4, 1.35), "far": (-0.35, 1.3)},
               feet={"near": (0.05, 0.06), "far": (0.6, 0.06)}, style="B"); b.draw(ax, zbase=5)
    a = Person(hip=(-0.55, 0.88), face=1, lean=8, hands={"near": (-0.25, 1.4), "far": (0.0, 1.6)},
               feet={"near": (-0.3, 0.06), "far": (-0.85, 0.06)}, open_hand=("near",)); a.draw(ax, zbase=10)
    impact(ax, 0.05, 1.62); arrow(ax, (0.4, 1.85), (-0.5, 1.85), dashed=True)
sequence("fig16_2", [c1, c2, c3], cols=3)
