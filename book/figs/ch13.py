import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
import numpy as np

def gnd_rail(d, x0, x1, gx):
    d += elm.Line().at((x0, 0)).to((x1, 0))
    d += elm.Line().at((gx, 0)).down(0.4); d += elm.Ground()

# 13.1 Superposition on the two-battery circuit: original and two partial circuits
def two_batt(d, ox, left=True, right=True, title=""):
    if left:
        d += elm.SourceV().up().at((ox, 0)).label("10 V", loc="top")
    else:
        d += elm.Line().up(3).at((ox, 0)).color(COPPER)
    d += elm.ResistorIEC().right().label("2 Ω", loc="top")
    d += elm.Dot().label("A", loc="top", color=COPPER)
    d += elm.ResistorIEC().right().label("1 Ω", loc="top")
    if right:
        d += elm.SourceV().down().reverse().label("5 V", loc="bot")
    else:
        d += elm.Line().down(3).color(COPPER)
    d += elm.ResistorIEC().down().at((ox + 3, 3)).label("4 Ω", loc="bot")
    d += elm.Line().at((ox, 0)).to((ox + 6, 0))
    d += elm.Dot().at((ox + 3, 0))
    d += elm.Label().at((ox + 3, -1.0)).label(title, fontsize=11)

d = drawing()
two_batt(d, 0, True, True, "(a) both sources")
two_batt(d, 8.5, True, False, "(b) 10 V only (5 V shorted)")
two_batt(d, 17, False, True, "(c) 5 V only (10 V shorted)")
save_drawing(d, "ch13_superpos")

# 13.2 Switching off sources
d = drawing()
d += elm.SourceV().up().at((0, 0)).label("V", loc="top")
d += elm.Arrow().right(1.6).at((1.0, 1.5)).color(GREY)
d += elm.Line().up(3).at((3.4, 0)).color(COPPER)
d += elm.Label().at((1.7, -0.9)).label("voltage source → short circuit", fontsize=10.5)
ox = 7.5
d += elm.SourceI().up().at((ox, 0)).label("I", loc="top")
d += elm.Arrow().right(1.6).at((ox + 1.0, 1.5)).color(GREY)
d += elm.Dot(open=True).at((ox + 3.4, 3)); d += elm.Dot(open=True).at((ox + 3.4, 0))
d += elm.Line().at((ox + 3.4, 3)).up(0.4) if False else elm.Label().at((ox + 3.4, 1.5)).label("(open)", fontsize=10, color=COPPER)
d += elm.Label().at((ox + 1.7, -0.9)).label("current source → open circuit", fontsize=10.5)
save_drawing(d, "ch13_switchoff")

# 13.3 Mixed sources
def mixed(d, ox, v=True, i=True, title=""):
    if v:
        d += elm.SourceV().up().at((ox, 0)).label("24 V", loc="top")
    else:
        d += elm.Line().up(3).at((ox, 0)).color(COPPER)
    d += elm.ResistorIEC().right().label("6 Ω", loc="top")
    d += elm.Dot().label("A", loc="top", color=COPPER)
    d += elm.Line().right(2.5)
    if i:
        d += elm.SourceI().down().reverse().label("3 A", loc="bot")
    else:
        d += elm.Dot(open=True); d += elm.Dot(open=True).at((ox + 5.5, 0))
    d += elm.ResistorIEC().down().at((ox + 3, 3)).label("3 Ω", loc="bot")
    d += elm.Line().at((ox, 0)).to((ox + 5.5 if i else ox + 3, 0))
    d += elm.Dot().at((ox + 3, 0))
    d += elm.Label().at((ox + 2.75, -1.0)).label(title, fontsize=11)

d = drawing()
mixed(d, 0, True, True, "(a) both sources")
mixed(d, 8, True, False, "(b) 24 V only")
mixed(d, 16, False, True, "(c) 3 A only")
save_drawing(d, "ch13_mixed")

# 13.4 Passive summing network
d = drawing()
for k, (y, lab) in enumerate([(4, "V$_1$"), (2, "V$_2$"), (0, "V$_3$")]):
    d += elm.Dot(open=True).at((0, y)).label(lab, loc="left")
    d += elm.ResistorIEC().right().label("10 kΩ", loc="top")
    d += elm.Line().right(0.6)
d += elm.Line().at((3.6, 0)).to((3.6, 4))
d += elm.Dot().at((3.6, 2)).label("V$_{out}$", loc="right", color=COPPER)
d += elm.Line().at((3.6, 0)).down(0.6)
d += elm.ResistorIEC().down().label("10 kΩ", loc="bot")
d += elm.Ground()
save_drawing(d, "ch13_mixer")

# 13.5 DC bias plus signal
t = np.linspace(0, 2e-3, 600)
fig, axs = plt.subplots(1, 3, figsize=(6.3, 2.0), sharey=True)
dc = np.full_like(t, 2.5); ac = 0.8 * np.sin(2 * np.pi * 1000 * t)
for ax, y, ttl, c in [(axs[0], dc, "DC bias alone", NAVY), (axs[1], ac, "signal alone", TEAL), (axs[2], dc + ac, "both together", COPPER)]:
    ax.plot(t * 1000, y, color=c, lw=2); ax.set_title(ttl, fontsize=10, color=c); ax.axhline(0, color=GREY, lw=0.7)
    ax.set_xlabel("time (ms)")
axs[0].set_ylabel("voltage (V)")
fig.text(0.355, 0.5, "+", fontsize=18, ha="center", color=GREY); fig.text(0.665, 0.5, "=", fontsize=18, ha="center", color=GREY)
fig.tight_layout()
save_fig(fig, "ch13_bias")

# 13.6 Linearity: output proportional to input
fig, ax = plt.subplots(figsize=(4.4, 2.5))
x = np.linspace(0, 30, 50)
ax.plot(x, x / 2, color=NAVY, lw=2.2, label="linear: V$_B$ = 0.5 V$_S$")
ax.plot(x, 15 * (1 - np.exp(-x / 12)), color=COPPER, lw=1.8, ls="--", label="non-linear (for contrast)")
ax.plot([2, 30], [1, 15], "o", color=TEAL)
ax.set_xlabel("source voltage V$_S$ (V)"); ax.set_ylabel("output V$_B$ (V)")
ax.legend(fontsize=8.5, frameon=False); ax.grid(alpha=0.25)
save_fig(fig, "ch13_linear")
