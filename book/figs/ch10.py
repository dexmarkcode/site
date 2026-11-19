import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
from matplotlib.patches import FancyBboxPatch

def gnd_rail(d, x0, x1, y=0, gx=None):
    d += elm.Line().at((x0, y)).to((x1, y))
    gx = (x0 + x1) / 2 if gx is None else gx
    d += elm.Line().at((gx, y)).down(0.4); d += elm.Ground()

# 10.1 two-node circuit with current sources
d = drawing()
d += elm.SourceI().up().at((0, 0)).label("6 A", loc="top")
d += elm.Line().right(2)
d += elm.Dot().label("1", loc="top", color=COPPER, fontsize=13)
d += elm.ResistorIEC().down().label("R$_1$ = 4 Ω", loc="top")
d += elm.ResistorIEC().right().at((2, 3)).label("R$_2$ = 4 Ω", loc="top")
d += elm.Dot().label("2", loc="top", color=COPPER, fontsize=13)
d += elm.ResistorIEC().down().label("R$_3$ = 8 Ω", loc="top")
d += elm.Line().right(2).at((5, 3))
d += elm.SourceI().down().reverse().label("1 A", loc="bot")
gnd_rail(d, 0, 7, gx=3.5)
d += elm.Dot().at((2, 0)); d += elm.Dot().at((5, 0))
save_drawing(d, "ch10_two_node")

# 10.2 single essential node: the Chapter 5 circuit
d = drawing()
d += elm.SourceV().up().at((0, 0)).label("10 V", loc="top")
d += elm.ResistorIEC().right().label("2 Ω", loc="top")
d += elm.Dot().label("V$_A$", loc="top", color=COPPER, fontsize=13)
d += elm.ResistorIEC().right().label("1 Ω", loc="top")
d += elm.SourceV().down().reverse().label("5 V", loc="bot")
d += elm.ResistorIEC().down().at((3, 3)).label("4 Ω", loc="bot")
gnd_rail(d, 0, 6, gx=3)
d += elm.Dot().at((3, 0))
save_drawing(d, "ch10_one_node")

# 10.3 three-node circuit
d = drawing()
d += elm.SourceV().up().at((0, 0)).label("20 V", loc="top")
d += elm.ResistorIEC().right().label("R$_a$ = 2 Ω", loc="top")
d += elm.Dot().label("1", loc="top", color=COPPER, fontsize=13)
d += elm.ResistorIEC().right().label("R$_c$ = 4 Ω", loc="top")
d += elm.Dot().label("2", loc="top", color=COPPER, fontsize=13)
d += elm.ResistorIEC().right().label("R$_e$ = 10 Ω", loc="top")
d += elm.Dot().label("3", loc="top", color=COPPER, fontsize=13)
d += elm.Line().right(2)
d += elm.SourceI().down().reverse().label("1 A", loc="bot")
d += elm.ResistorIEC().down().at((3, 3)).label("R$_b$ = 4 Ω", loc="top")
d += elm.ResistorIEC().down().at((6, 3)).label("R$_d$ = 10 Ω", loc="top")
d += elm.ResistorIEC().down().at((9, 3)).label("R$_f$ = 5 Ω", loc="top")
gnd_rail(d, 0, 11, gx=5.5)
for x in (3, 6, 9): d += elm.Dot().at((x, 0))
save_drawing(d, "ch10_three_node")

# 10.4 Flowchart of the method
steps = ["1. Choose a reference node\n(usually the one with most connections)",
         "2. Label the other node voltages\nV₁, V₂, … Mark any that are fixed by sources",
         "3. At each unknown node, write KCL:\nsum of currents LEAVING = 0, with I = (V$_{here}$ − V$_{there}$) / R",
         "4. Solve the simultaneous equations\n(elimination, Cramer's rule or software)",
         "5. Find branch currents and powers;\ncheck with KCL and a power balance"]
fig, ax = plt.subplots(figsize=(4.6, 5.0))
for i, s in enumerate(steps):
    y = 4.4 - i * 1.05
    ax.add_patch(FancyBboxPatch((0.2, y - 0.38), 4.2, 0.76, boxstyle="round,pad=0.02,rounding_size=0.12",
                                fc=LIGHT if i % 2 == 0 else "#fbf5f0", ec=NAVY if i % 2 == 0 else COPPER, lw=1.2))
    ax.text(2.3, y, s, ha="center", va="center", fontsize=9.6, color="#1b263b")
    if i < len(steps) - 1:
        ax.annotate("", xy=(2.3, y - 0.66), xytext=(2.3, y - 0.4), arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.4))
ax.set_xlim(0, 4.6); ax.set_ylim(-0.2, 4.95); ax.axis("off")
save_fig(fig, "ch10_flow")
