import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
from matplotlib.patches import FancyBboxPatch

# 17.1 Decision flowchart
fig, ax = plt.subplots(figsize=(6.2, 6.4))
ax.set_xlim(0, 10); ax.set_ylim(0.6, 12); ax.axis("off")
def box(x, y, w, h, txt, fc=LIGHT, ec=NAVY, fs=9.2):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.15", fc=fc, ec=ec, lw=1.2))
    ax.text(x, y, txt, ha="center", va="center", fontsize=fs, color="#1b263b")
def arr(x1, y1, x2, y2, lab=None, dx=0.12, ha="left"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.2))
    if lab:
        ax.text((x1 + x2) / 2 + dx, (y1 + y2) / 2 + (0.28 if y1 == y2 else 0), lab, fontsize=8.5, color=COPPER, ha=ha, va="center")
Q = "#fbf5f0"
box(3.3, 11.2, 6.2, 1.0, "Redraw the circuit neatly and label every node.\nWhat exactly am I asked to find?", fc="#eef2f7")
arr(3.3, 10.7, 3.3, 10.0)
box(3.3, 9.5, 5.0, 0.9, "Only one source?", fc=Q, ec=COPPER)
arr(5.8, 9.5, 6.7, 9.5, "yes", dx=-0.25)
box(8.4, 9.5, 3.2, 1.1, "Series–parallel\nreduction and\ndivider rules")
arr(3.3, 9.05, 3.3, 8.35, "no")
box(3.3, 7.8, 5.0, 1.0, "Interested in one element,\nor a load that will change?", fc=Q, ec=COPPER)
arr(5.8, 7.8, 6.7, 7.8, "yes", dx=-0.3)
box(8.4, 7.8, 3.2, 1.1, "Thévenin or\nNorton\nequivalent")
arr(3.3, 7.3, 3.3, 6.6, "no")
box(3.3, 5.9, 6.2, 1.25, "Count the unknowns:\nnodal = (n − 1) − (voltage sources)\nmesh = m − (current sources)", fc=Q, ec=COPPER)
arr(2.0, 5.27, 1.9, 4.45, "nodal fewer", dx=-0.15, ha="right")
arr(4.6, 5.27, 4.9, 4.45, "mesh fewer")
box(1.9, 3.8, 3.4, 1.2, "Nodal analysis\n(supernodes for\nfloating V sources)")
box(5.4, 3.8, 3.4, 1.2, "Mesh analysis\n(supermeshes for\nshared I sources)")
arr(1.9, 3.2, 2.8, 2.35); arr(5.4, 3.2, 4.6, 2.35)
ax.plot([8.4, 8.4], [8.95, 7.25 + 0.0], color=GREY, lw=1.2) if False else None
ax.annotate("", xy=(8.4, 2.35), xytext=(8.4, 7.25), arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.2))
box(5.0, 1.75, 9.4, 1.1, "CHECK: KCL at a spare node, KVL round a spare loop,\npower balance, limiting cases, units and common sense", fc="#eff7f3", ec=TEAL)
save_fig(fig, "ch17_flow")

# 17.2 Case-study circuit
d = drawing()
d += elm.SourceV().up().at((0, 0)).label("24 V", loc="top")
d += elm.ResistorIEC().right().label("4 Ω", loc="top")
d += elm.Dot().label("1", loc="top", color=COPPER, fontsize=13)
d += elm.ResistorIEC().right().label("6 Ω", loc="top")
d += elm.Dot().label("2", loc="top", color=COPPER, fontsize=13)
d += elm.Line().right(2.5)
d += elm.SourceI().down().reverse().label("2 A", loc="bot")
d += elm.ResistorIEC().down().at((3, 3)).label("12 Ω", loc="bot")
d += elm.ResistorIEC().down().at((6, 3)).label("R$_L$ = 3 Ω", loc="bot").color(COPPER)
d += elm.Line().at((0, 0)).to((8.5, 0))
d += elm.Dot().at((3, 0)); d += elm.Dot().at((6, 0))
d += elm.Line().at((4.25, 0)).down(0.4); d += elm.Ground()
save_drawing(d, "ch17_case")

# 17.3 Sensor interface with ADC loading
d = drawing()
d += elm.SourceV().up().at((0, 0)).length(6).label("5 V", loc="top")
d += elm.Line().right(2)
d += elm.Thermistor().down().label("NTC", loc="top") if hasattr(elm, "Thermistor") else elm.ResistorVarIEC().down()
d += elm.Dot()
d += elm.ResistorIEC().down().label("R", loc="top")
d += elm.Line().left(2)
d += elm.Line().right(2.6).at((2, 3))
d += elm.ResistorIEC().down().label("ADC input\n20 kΩ", loc="bot").color(COPPER)
d += elm.Line().left(2.6)
d += elm.Dot().at((2, 0))
d += elm.Label().at((3.3, 3.45)).label("V$_{out}$", color=COPPER)
save_drawing(d, "ch17_sensor")
