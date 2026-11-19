import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *

def loop(d, center, lab, r=0.55):
    d += elm.LoopArrow(direction="cw", width=1.1, height=1.1).at((center[0], center[1] + 0.55)).color(TEAL) if False else None

def mesh_arrow(d, cx, cy, lab):
    import numpy as np
    from schemdraw.segments import Segment, SegmentArc
    d += elm.Annotate() if False else elm.Label().at((cx + 0.5, cy)).label(lab, color=TEAL, fontsize=13)
    e = elm.Element()
    e.segments.append(SegmentArc((0, 0), 1.1, 1.1, theta1=-60, theta2=220, arrow="ccw" if False else "cw", color=TEAL, lw=1.4))
    d += e.at((cx + 0.45, cy))

# 11.1 two-mesh circuit (Chapter 5 example)
d = drawing()
d += elm.SourceV().up().at((0, 0)).label("10 V", loc="top")
d += elm.ResistorIEC().right().label("R$_1$ = 2 Ω", loc="top")
d += elm.Dot().label("A", loc="top", color=COPPER)
d += elm.ResistorIEC().right().label("R$_2$ = 1 Ω", loc="top")
d += elm.SourceV().down().reverse().label("5 V", loc="bot")
d += elm.Line().left(6)
d += elm.ResistorIEC().down().at((3, 3)).label("R$_3$\n4 Ω", loc="bot")
d += elm.Dot().at((3, 0))
mesh_arrow(d, 1.5, 1.5, "I$_1$"); mesh_arrow(d, 4.5, 1.5, "I$_2$")
save_drawing(d, "ch11_two_mesh")

# 11.2 three-mesh circuit
d = drawing()
d += elm.SourceV().up().at((0, 0)).label("E$_1$ = 30 V", loc="top")
d += elm.ResistorIEC().right().label("R$_1$ = 1 Ω", loc="top")
d += elm.ResistorIEC().right().label("R$_3$ = 1 Ω", loc="top")
d += elm.ResistorIEC().right().label("R$_5$ = 2 Ω", loc="top")
d += elm.SourceV().down().reverse().label("E$_2$ = 10 V", loc="bot")
d += elm.Line().left(9)
d += elm.ResistorIEC().down().at((3, 3)).label("R$_2$\n4 Ω", loc="bot")
d += elm.ResistorIEC().down().at((6, 3)).label("R$_4$\n6 Ω", loc="bot")
for x in (3, 6):
    d += elm.Dot().at((x, 3)); d += elm.Dot().at((x, 0))
mesh_arrow(d, 1.5, 1.5, "I$_1$"); mesh_arrow(d, 4.5, 1.5, "I$_2$"); mesh_arrow(d, 7.5, 1.5, "I$_3$")
save_drawing(d, "ch11_three_mesh")

# 11.3 current source on the outer boundary
d = drawing()
d += elm.SourceV().up().at((0, 0)).label("12 V", loc="top")
d += elm.ResistorIEC().right().label("R$_1$ = 2 Ω", loc="top")
d += elm.Dot().label("A", loc="top", color=COPPER)
d += elm.ResistorIEC().right().label("R$_3$ = 2 Ω", loc="top")
d += elm.Dot().label("B", loc="top", color=COPPER)
d += elm.SourceI().down().label("3 A", loc="bot")
d += elm.Line().left(6)
d += elm.ResistorIEC().down().at((3, 3)).label("R$_2$\n4 Ω", loc="bot")
d += elm.Dot().at((3, 0))
mesh_arrow(d, 1.5, 1.5, "I$_1$"); mesh_arrow(d, 4.5, 1.5, "I$_2$")
save_drawing(d, "ch11_current_source")
