import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
import numpy as np

def thev(d, ox, vlab, rlab):
    d += elm.SourceV().up().at((ox, 0)).label(vlab, loc="top")
    d += elm.ResistorIEC().right().label(rlab, loc="top")
    d += elm.Dot(open=True).label("a", loc="right")
    d += elm.Line().at((ox, 0)).to((ox + 3, 0))
    d += elm.Dot(open=True).at((ox + 3, 0)).label("b", loc="right")

def nort(d, ox, ilab, rlab):
    d += elm.SourceI().up().at((ox, 0)).label(ilab, loc="top")
    d += elm.Line().right(1.5)
    d += elm.Dot()
    d += elm.Line().right(1.5)
    d += elm.Dot(open=True).label("a", loc="right")
    d += elm.ResistorIEC().down().at((ox + 1.5, 3)).label(rlab, loc="bot")
    d += elm.Line().at((ox, 0)).to((ox + 3, 0))
    d += elm.Dot().at((ox + 1.5, 0))
    d += elm.Dot(open=True).at((ox + 3, 0)).label("b", loc="right")

# 15.1 Thevenin and Norton equivalents side by side
d = drawing()
thev(d, 0, "V$_{Th}$", "R$_{Th}$")
d += elm.Label().at((4.75, 1.5)).label("≡", fontsize=26, color=COPPER)
nort(d, 6.3, "I$_N$", "R$_N$")
d += elm.Label().at((1.5, -0.9)).label("Thévenin", fontsize=11)
d += elm.Label().at((7.8, -0.9)).label("Norton", fontsize=11)
save_drawing(d, "ch15_equiv")

# 15.2 Source transformation
d = drawing()
thev(d, 0, "E", "R")
d += elm.Label().at((4.75, 1.5)).label("≡", fontsize=26, color=COPPER)
nort(d, 7.2, "I = E / R", "R")
save_drawing(d, "ch15_transform")

# 15.3 Two-battery circuit transformed
d = drawing()
ox = 0
d += elm.SourceI().up().at((ox, 0)).label("5 A", loc="top")
d += elm.Line().right(1.4)
d += elm.ResistorIEC().down().label("2 Ω", loc="bot")
d += elm.Line().right(1.4).at((ox + 1.4, 3))
d += elm.Dot().label("A", loc="top", color=COPPER)
d += elm.ResistorIEC().down().label("4 Ω", loc="bot")
d += elm.Line().right(1.4).at((ox + 2.8, 3))
d += elm.ResistorIEC().down().label("1 Ω", loc="bot")
d += elm.Line().right(1.4).at((ox + 4.2, 3))
d += elm.SourceI().down().reverse().label("5 A", loc="bot")
d += elm.Line().at((ox, 0)).to((ox + 5.6, 0))
for x in (1.4, 2.8, 4.2): d += elm.Dot().at((ox + x, 0)); d += elm.Dot().at((ox + x, 3)) if x != 2.8 else elm.Line().length(0.001)
d += elm.Label().at((ox + 2.8, -1.0)).label("(a) both batteries transformed", fontsize=11)
ox = 9
d += elm.SourceI().up().at((ox, 0)).label("10 A", loc="top")
d += elm.Line().right(1.6)
d += elm.ResistorIEC().down().label("0.667 Ω", loc="bot")
d += elm.Line().right(1.6).at((ox + 1.6, 3))
d += elm.Dot().label("A", loc="top", color=COPPER)
d += elm.ResistorIEC().down().label("4 Ω", loc="bot")
d += elm.Line().at((ox, 0)).to((ox + 3.2, 0))
d += elm.Dot().at((ox + 1.6, 0)); d += elm.Dot().at((ox + 1.6, 3))
d += elm.Label().at((ox + 1.6, -1.0)).label("(b) sources and resistors combined", fontsize=11)
save_drawing(d, "ch15_twobatt")

# 15.4 Ladder by repeated transformation
d = drawing()
d += elm.SourceV().up().at((0, 0)).label("36 V", loc="top")
d += elm.ResistorIEC().right().label("6 Ω", loc="top")
d += elm.Dot()
d += elm.ResistorIEC().right().label("2 Ω", loc="top")
d += elm.Dot().label("a", loc="top", color=COPPER)
d += elm.ResistorIEC().down().label("R$_L$ = 4 Ω", loc="bot").color(COPPER)
d += elm.ResistorIEC().down().at((3, 3)).label("3 Ω", loc="bot")
d += elm.Line().at((0, 0)).to((6, 0)); d += elm.Dot().at((3, 0))
save_drawing(d, "ch15_ladder")

# 15.5 Terminal characteristic: V-I line of a Thevenin/Norton source
fig, ax = plt.subplots(figsize=(4.6, 2.7))
I = np.linspace(0, 2.667, 100)
ax.plot(I, 16 - 6 * I, color=NAVY, lw=2.4)
ax.plot(0, 16, "o", color=COPPER); ax.plot(2.667, 0, "o", color=COPPER)
ax.annotate("open circuit:\nV = V$_{Th}$ = 16 V", (0, 16), xytext=(0.35, 15.0), fontsize=9, color=COPPER)
ax.annotate("short circuit:\nI = I$_N$ = 2.67 A", (2.667, 0), xytext=(1.55, 3.2), fontsize=9, color=COPPER)
ax.text(1.0, 10.8, "slope = −R$_{Th}$ = −6 Ω", fontsize=9.5, color=NAVY, rotation=-38)
ax.set_xlabel("current drawn from terminals, I (A)"); ax.set_ylabel("terminal voltage V (V)")
ax.set_xlim(0, 3); ax.set_ylim(0, 18); ax.grid(alpha=0.25)
save_fig(fig, "ch15_line")

# 15.6 Batteries in parallel (Millman)
d = drawing()
vals = [("12.6 V", "0.05 Ω"), ("12.4 V", "0.04 Ω"), ("12.0 V", "0.1 Ω")]
for k, (e, r) in enumerate(vals):
    x = k * 2.6
    d += elm.BatteryCell().up().reverse().at((x, 0)).length(1.6).label(e, loc="top")
    d += elm.ResistorIEC().up().length(2).label(r, loc="top")
d += elm.Line().at((0, 3.6)).to((7.6, 3.6)); d += elm.Line().at((0, 0)).to((7.6, 0))
d += elm.Dot(open=True).at((7.6, 3.6)).label("+", loc="right"); d += elm.Dot(open=True).at((7.6, 0)).label("−", loc="right")
for k in range(1, 3): d += elm.Dot().at((k * 2.6, 3.6)); d += elm.Dot().at((k * 2.6, 0))
save_drawing(d, "ch15_millman")
