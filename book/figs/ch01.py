import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle, FancyBboxPatch

# 1.1 Free electrons drifting through a copper lattice
fig, ax = plt.subplots(figsize=(6.2, 2.6))
rng = np.random.default_rng(4)
for x in range(12):
    for y in range(4):
        ax.add_patch(Circle((x + 0.5, y + 0.5), 0.28, fc=LIGHT, ec=NAVY, lw=1))
        ax.text(x + 0.5, y + 0.5, "+", ha="center", va="center", color=NAVY, fontsize=9)
for _ in range(34):
    ex, ey = rng.uniform(0.1, 11.9), rng.uniform(0.1, 3.9)
    ax.add_patch(Circle((ex, ey), 0.09, fc=COPPER, ec="none"))
ax.add_patch(Rectangle((0, 0), 12, 4, fill=False, ec=NAVY, lw=1.5))
ax.annotate("", xy=(0.4, 4.55), xytext=(4.4, 4.55), arrowprops=dict(arrowstyle="-|>", color=COPPER, lw=1.8))
ax.text(2.4, 4.85, "electron drift (slow)", ha="center", color=COPPER, fontsize=10)
ax.annotate("", xy=(11.6, 4.55), xytext=(7.6, 4.55), arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.8))
ax.text(9.6, 4.85, "conventional current, I", ha="center", color=NAVY, fontsize=10)
ax.text(-0.25, 2, "−", fontsize=20, ha="right", va="center", color=NAVY)
ax.text(12.25, 2, "+", fontsize=18, ha="left", va="center", color=NAVY)
ax.set_xlim(-1, 13); ax.set_ylim(-0.3, 5.3); ax.set_aspect("equal"); ax.axis("off")
ax.text(6, -0.25, "fixed copper ions (+)  and  free electrons (●)", ha="center", va="top", fontsize=9.5, color=GREY)
save_fig(fig, "ch01_lattice")

# 1.2 Simple circuit: battery, switch, lamp with current direction
d = drawing()
d += (b := elm.BatteryCell().up().label("9 V", loc="top"))
d += elm.Line().right(1)
d += elm.Switch(action="close").right().label("S", loc="top")
d += elm.Line().right(1)
d += (lamp := elm.Lamp().down().label("lamp", loc="bot"))
d += elm.Line().left().tox(b.start)
d += elm.CurrentLabelInline(direction="in").at(lamp).label("I")
save_drawing(d, "ch01_simple_circuit")

# 1.3 Water analogy
fig, ax = plt.subplots(figsize=(6.2, 3.0))
ax.add_patch(Rectangle((0.3, 2.2), 1.6, 1.6, fc="#cfe3f3", ec=NAVY, lw=1.4))
ax.add_patch(Rectangle((0.3, 2.2), 1.6, 1.1, fc="#7fb3d5", ec="none"))
ax.text(1.1, 3.95, "high tank", ha="center", fontsize=10, color=NAVY)
ax.add_patch(Rectangle((7.4, 0.2), 1.6, 1.6, fc="#cfe3f3", ec=NAVY, lw=1.4))
ax.add_patch(Rectangle((7.4, 0.2), 1.6, 0.5, fc="#7fb3d5", ec="none"))
ax.text(8.2, 1.95, "low tank", ha="center", fontsize=10, color=NAVY)
ax.plot([1.9, 3.5], [2.45, 2.45], color=NAVY, lw=6, solid_capstyle="butt")
ax.add_patch(Rectangle((3.5, 2.30), 1.6, 0.30, fc="#f4d6c4", ec=COPPER, lw=1.4))
ax.text(4.3, 2.75, "narrow section\n(resistance)", ha="center", va="bottom", fontsize=9.5, color=COPPER)
ax.plot([5.1, 6.2], [2.45, 2.45], color=NAVY, lw=6, solid_capstyle="butt")
ax.plot([6.2, 6.2, 7.4], [2.45, 1.0, 1.0], color=NAVY, lw=6, solid_capstyle="butt")
ax.annotate("", xy=(6.0, 3.75), xytext=(2.4, 3.75), arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.5))
ax.text(6.2, 3.65, "flow rate ↔ current", fontsize=9.5, color=TEAL)
ax.annotate("", xy=(0.0, 3.3), xytext=(0.0, 0.7), arrowprops=dict(arrowstyle="<|-|>", color=RED, lw=1.4))
ax.text(-0.15, 2.0, "height\ndifference\n↔ voltage", ha="right", va="center", fontsize=9.5, color=RED)
ax.plot([-0.25, 9.3], [0.7, 0.7], ls=":", color=GREY, lw=1)
ax.plot([-0.25, 1.9], [3.3, 3.3], ls=":", color=GREY, lw=1)
ax.text(4.6, 0.6, "pump returns the water to the top  ↔  the battery", ha="center", fontsize=9.5, color=GREY, va="top")
ax.set_xlim(-2.2, 9.6); ax.set_ylim(-0.1, 4.3); ax.set_aspect("equal"); ax.axis("off")
save_fig(fig, "ch01_water")

# 1.4 Connecting an ammeter (series) and a voltmeter (parallel)
d = drawing()
d += (src := elm.SourceV().up().label("12 V", loc="top"))
d += elm.Line().right(1)
d += elm.MeterA().right().label("ammeter\nin series", loc="top")
d += elm.Line().right(1)
d += (r := elm.ResistorIEC().down().label("R", loc="top"))
d += elm.Line().left().tox(src.start)
d += elm.Line().right(2).at(r.start)
d += elm.MeterV().down().label("voltmeter\nin parallel", loc="bot", ofst=0.3)
d += elm.Line().left(2)
save_drawing(d, "ch01_meters")

# 1.5 DC versus AC
t = np.linspace(0, 0.04, 800)
fig, axs = plt.subplots(1, 2, figsize=(6.2, 2.3), sharey=True)
axs[0].plot(t * 1000, np.full_like(t, 9), color=NAVY, lw=2)
axs[0].set_title("Direct current (battery)", fontsize=10.5, color=NAVY)
axs[1].plot(t * 1000, 325 / 36 * np.sin(2 * np.pi * 50 * t), color=COPPER, lw=2)
axs[1].set_title("Alternating current (50 Hz mains, scaled)", fontsize=10.5, color=COPPER)
for a in axs:
    a.axhline(0, color=GREY, lw=0.8)
    a.set_xlabel("time (ms)")
axs[0].set_ylabel("voltage")
axs[0].set_yticks([])
fig.tight_layout()
save_fig(fig, "ch01_dc_ac")
