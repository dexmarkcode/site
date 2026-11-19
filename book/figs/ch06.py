import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *

# 6.1 Series fairy lights vs parallel
d = drawing()
d += (s := elm.SourceV().up().label("230 V", loc="top"))
for i in range(4):
    d += elm.Line().right(0.3)
    d += elm.Lamp().right().scale(0.8)
d += elm.Line().right(0.3)
d += elm.Line().down().toy(s.start)
d += elm.Line().left().tox(s.start)
d += elm.Label().at((5.5, -1.0)).label("(a) series: one failed lamp breaks the whole chain", fontsize=10.5)
ox = 16.5
d += (s2 := elm.SourceV().up().at((ox, 0)).label("230 V", loc="top"))
d += elm.Line().right(1.2)
xs = []
for i in range(4):
    d += (t := elm.Dot())
    d += elm.Lamp().down().at(t.center).toy(0).scale(0.8)
    if i < 3:
        d += elm.Line().right(1.6).at(t.center)
d += elm.Line().left().at((ox + 1.2 + 3 * 1.6, 0)).tox(ox)
d += elm.Label().at((ox + 3.5, -1.0)).label("(b) parallel: each lamp has its own path", fontsize=10.5)
save_drawing(d, "ch06_fairy")

# 6.2 Series resistors
d = drawing()
d += (s := elm.SourceV().up().label("24 V", loc="top"))
d += elm.Line().right(0.4)
d += elm.ResistorIEC().right().label("R$_1$ = 2 Ω", loc="top").label(("+", "V$_1$", "−"), loc="bot", fontsize=10)
d += elm.ResistorIEC().right().label("R$_2$ = 4 Ω", loc="top").label(("+", "V$_2$", "−"), loc="bot", fontsize=10)
d += elm.Line().right(0.4)
d += elm.ResistorIEC().down().label("R$_3$ = 6 Ω", loc="bot").label(("+", "V$_3$", "−"), loc="top", fontsize=10)
d += (ret := elm.Line().left().tox(s.start))
d += elm.CurrentLabelInline(direction="in").at(ret).label("I", loc="bot")
save_drawing(d, "ch06_series")

# 6.3 Voltage divider
d = drawing()
d += (s := elm.SourceV().up().label("V$_S$", loc="top"))
d += elm.Line().right(2)
d += elm.ResistorIEC().down().label("R$_1$", loc="top")
d += (mid := elm.Dot())
d += elm.ResistorIEC().down().label("R$_2$", loc="top")
d += (bot := elm.Dot())
d += elm.Line().left().tox(s.start)
d += elm.Line().up().toy(s.start)
d += elm.Line().right(1.6).at(mid.center)
d += (o := elm.Dot(open=True))
d += elm.Line().right(1.6).at(bot.center)
d += (o2 := elm.Dot(open=True))
d += elm.Gap().up().at(o2.center).to(o.center).label(("−", "V$_{out}$", "+"), loc="bot")
d += elm.Line().down(0.4).at((2, -3)); d += elm.Ground()
save_drawing(d, "ch06_divider")

# 6.4 Parallel resistors
d = drawing()
d += (s := elm.SourceV().up().label("24 V", loc="top"))
d += elm.Line().right(1.2)
labs = ["R$_1$ = 6 Ω", "R$_2$ = 12 Ω", "R$_3$ = 4 Ω"]
for i, lab in enumerate(labs):
    d += (t := elm.Dot()) if i < 2 else elm.Line().length(0.001)
    x = 1.2 + 2.4 * i
    d += elm.ResistorIEC().down().at((x, 3)).label(lab, loc="bot")
    d += elm.Arrow().down(0.8).at((x - 0.45, 2.55)).color(COPPER).label(f"I$_{i+1}$", loc="top", color=COPPER)
    if i < 2:
        d += elm.Line().right(2.4).at((x, 3))
        d += elm.Line().right(2.4).at((x, 0))
d += elm.Line().left(1.2).at((1.2, 0))
d += elm.Dot().at((1.2, 0)); d += elm.Dot().at((3.6, 0)); d += elm.Dot().at((1.2, 3)); d += elm.Dot().at((3.6, 3))
d += elm.Arrow().right(0.8).at((0.2, 3.35)).color(COPPER).label("I$_T$", loc="top", color=COPPER)
save_drawing(d, "ch06_parallel")

# 6.5 Current divider
d = drawing()
d += (s := elm.SourceI().up().label("I$_T$", loc="top"))
d += elm.Line().right(2)
d += (t := elm.Dot())
d += elm.ResistorIEC().down().label("R$_1$", loc="bot")
d += (b := elm.Dot())
d += elm.Line().left().tox(s.start)
d += elm.Line().right(2.4).at(t.center)
d += elm.ResistorIEC().down().label("R$_2$", loc="bot")
d += elm.Line().left(2.4)
d += elm.Arrow().down(0.8).at((1.55, 2.5)).color(COPPER).label("I$_1$", loc="top", color=COPPER)
d += elm.Arrow().down(0.8).at((3.95, 2.5)).color(COPPER).label("I$_2$", loc="top", color=COPPER)
save_drawing(d, "ch06_current_divider")

# 6.6 Household loads in parallel
d = drawing()
d += (s := elm.SourceSin().up().label("230 V\n50 Hz", loc="top"))
d += elm.Line().right(1)
d += elm.FuseIEC().right().label("32 A", loc="top")
loads = ["kettle\n3 kW", "toaster\n1 kW", "lamp\n100 W"]
x0 = 4.0
for i, lab in enumerate(loads):
    x = x0 + 2.4 * i
    if i == 0:
        d += elm.Line().right(1).at((3.0, 3))
    else:
        d += elm.Line().right(2.4).at((x - 2.4, 3))
    d += elm.Dot().at((x, 3)) if i < 2 else elm.Line().length(0.001)
    d += (elm.Lamp() if i == 2 else elm.ResistorIEC()).down().at((x, 3)).label(lab, loc="bot")
d += elm.Line().left().at((x0 + 4.8, 0)).tox(0)
d += elm.Label().at((0.3, 3.45)).label("L", fontsize=10, color=GREY)
d += elm.Label().at((0.3, -0.45)).label("N", fontsize=10, color=GREY)
save_drawing(d, "ch06_house")
