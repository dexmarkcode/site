import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
from schemdraw.segments import SegmentArc
from matplotlib.patches import Ellipse

def gnd_rail(d, x0, x1, gx):
    d += elm.Line().at((x0, 0)).to((x1, 0))
    d += elm.Line().at((gx, 0)).down(0.4); d += elm.Ground()

def mesh_arrow(d, cx, cy, lab):
    d += elm.Label().at((cx + 0.5, cy)).label(lab, color=TEAL, fontsize=13)
    e = elm.Element()
    e.segments.append(SegmentArc((0, 0), 1.1, 1.1, theta1=-60, theta2=220, arrow="cw", color=TEAL, lw=1.4))
    d += e.at((cx + 0.45, cy))

# 12.1 Supernode example (Ex 12.2)
d = drawing()
d += elm.SourceV().up().at((0, 0)).label("20 V", loc="top")
d += elm.ResistorIEC().right().label("4 Ω", loc="top")
d += elm.Dot().label("1", loc="top", color=COPPER, fontsize=13)
d += elm.SourceV().right().reverse().label("5 V", loc="top")
d += elm.Dot().label("2", loc="top", color=COPPER, fontsize=13)
d += elm.ResistorIEC().down().label("4 Ω", loc="bot")
d += elm.ResistorIEC().down().at((3, 3)).label("8 Ω", loc="top")
gnd_rail(d, 0, 6, 4.5)
d += elm.Dot().at((3, 0))
d += elm.EncircleBox([d.elements[3], d.elements[4], d.elements[5]], padx=0.35, pady=0.45).linestyle("--").color(COPPER) if False else elm.Line().length(0.001)
save_drawing(d, "ch12_supernode")

# add dashed supernode outline with matplotlib overlay: simpler to draw as rectangle element
d = drawing()
d += elm.SourceV().up().at((0, 0)).label("20 V", loc="top")
d += elm.ResistorIEC().right().label("4 Ω", loc="top")
d += elm.Dot().label("1", loc="top", color=COPPER, fontsize=13)
d += elm.SourceV().right().reverse().label("5 V", loc="top")
d += elm.Dot().label("2", loc="top", color=COPPER, fontsize=13)
d += elm.ResistorIEC().down().label("4 Ω", loc="bot")
d += elm.ResistorIEC().down().at((3, 3)).label("8 Ω", loc="top")
gnd_rail(d, 0, 6, 4.5)
d += elm.Dot().at((3, 0))
for (a, b) in [((2.6, 2.45), (6.4, 2.45)), ((6.4, 2.45), (6.4, 4.25)), ((6.4, 4.25), (2.6, 4.25)), ((2.6, 4.25), (2.6, 2.45))]:
    d += elm.Line().at(a).to(b).linestyle("--").color(COPPER)
d += elm.Label().at((4.5, 4.6)).label("supernode", color=COPPER, fontsize=10.5)
save_drawing(d, "ch12_supernode")

# 12.2 Supermesh example
d = drawing()
d += elm.SourceV().up().at((0, 0)).label("32 V", loc="top")
d += elm.ResistorIEC().right().label("2 Ω", loc="top")
d += elm.Dot()
d += elm.ResistorIEC().right().label("4 Ω", loc="top")
d += elm.ResistorIEC().down().label("6 Ω", loc="bot")
d += elm.Line().left(6)
d += elm.SourceI().up().at((3, 0)).label("2 A", loc="bot")
d += elm.Dot().at((3, 0))
mesh_arrow(d, 1.2, 1.5, "I$_1$"); mesh_arrow(d, 4.2, 1.5, "I$_2$")
save_drawing(d, "ch12_supermesh")

# 12.3 Dependent source symbols
d = drawing()
d.config(fontsize=10.5)
items = [(elm.SourceControlledV, "μ·v$_x$", "VCVS\nvoltage-controlled\nvoltage source"),
         (elm.SourceControlledV, "r·i$_x$", "CCVS\ncurrent-controlled\nvoltage source"),
         (elm.SourceControlledI, "g·v$_x$", "VCCS\nvoltage-controlled\ncurrent source"),
         (elm.SourceControlledI, "β·i$_x$", "CCCS\ncurrent-controlled\ncurrent source")]
for i, (e, val, lab) in enumerate(items):
    x = i * 4.2
    d += elm.Line().up(0.5).at((x, 0))
    d += e().up().label(val, loc="bot")
    d += elm.Line().up(0.5)
    d += elm.Label().at((x, -1.4)).label(lab)
save_drawing(d, "ch12_dependent")

# 12.4 VCCS amplifier model
d = drawing()
d += elm.SourceV().up().at((0, 0)).label("2 V", loc="top")
d += elm.ResistorIEC().right().label("R$_s$ = 1 kΩ", loc="top")
d += elm.Dot().label("1", loc="top", color=COPPER, fontsize=13)
d += elm.ResistorIEC().right().length(4).label("R$_f$ = 10 kΩ", loc="top")
d += elm.Dot().label("2", loc="top", color=COPPER, fontsize=13)
d += elm.Line().right(2.2)
d += elm.ResistorIEC().down().label("R$_L$ = 2 kΩ", loc="bot")
d += elm.ResistorIEC().down().at((3, 3)).label(("+", "v$_x$", "−"), loc="bot").label("R$_1$ = 1 kΩ", loc="top")
d += elm.SourceControlledI().down().at((7, 3)).label("g·v$_x$\ng = 4 mS", loc="bot")
gnd_rail(d, 0, 9.2, 5)
d += elm.Dot().at((3, 0)); d += elm.Dot().at((7, 0))
save_drawing(d, "ch12_amp")

# 12.5 CCVS mesh example
d = drawing()
d += elm.SourceV().up().at((0, 0)).label("10 V", loc="top")
d += elm.ResistorIEC().right().label("2 Ω", loc="top")
d += elm.Dot()
d += elm.ResistorIEC().right().label("2 Ω", loc="top")
d += elm.SourceControlledV().down().reverse().label("3 i$_x$", loc="bot")
d += elm.Line().left(6)
d += elm.ResistorIEC().down().at((3, 3)).label("4 Ω", loc="bot")
d += elm.Arrow().down(0.8).at((2.55, 2.4)).color(COPPER).label("i$_x$", loc="top", color=COPPER)
d += elm.Dot().at((3, 0))
mesh_arrow(d, 0.9, 1.5, "I$_1$"); mesh_arrow(d, 4.3, 1.5, "I$_2$")
save_drawing(d, "ch12_ccvs")
