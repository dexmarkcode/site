import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
import numpy as np

# 4.1 Symbol library
d = drawing()
d.config(fontsize=10.5)
items = [
    (lambda: elm.BatteryCell().right(), "cell"),
    (lambda: elm.Battery().right(), "battery"),
    (lambda: elm.SourceV().right(), "DC voltage\nsource"),
    (lambda: elm.SourceI().right(), "current\nsource"),
    (lambda: elm.SourceControlledV().right(), "dependent\nvoltage source"),
    (lambda: elm.ResistorIEC().right(), "resistor"),
    (lambda: elm.Switch().right(), "switch (open)"),
    (lambda: elm.FuseIEC().right(), "fuse"),
    (lambda: elm.Lamp().right(), "lamp"),
    (lambda: elm.Diode().right(), "diode"),
    (lambda: elm.LED().right(), "LED"),
    (lambda: elm.Capacitor().right(), "capacitor"),
]
for i, (mk, lab) in enumerate(items):
    x, y = (i % 4) * 4.4, -(i // 4) * 3.4
    d += elm.Line().right(0.4).at((x, y))
    d += mk()
    d += elm.Line().right(0.4)
    d += elm.Label().at((x + 1.9, y - 1.35)).label(lab)
x, y = 0, -3 * 3.4
d += elm.Line().down(0.6).at((x + 1.5, y + 0.4)); d += elm.GroundChassis() if False else elm.Ground()
d += elm.Label().at((x + 1.5, y - 1.45)).label("ground / 0 V\nreference")
d += elm.Line().down(0.6).at((x + 5.9, y + 0.4)); d += elm.GroundSignal()
d += elm.Label().at((x + 5.9, y - 1.45)).label("signal ground")
d += elm.Line().right(0.4).at((x + 8.8, y)); d += elm.MeterA().right(); d += elm.Line().right(0.4)
d += elm.Label().at((x + 10.7, y - 1.35)).label("ammeter")
d += elm.Line().right(0.4).at((x + 13.2, y)); d += elm.MeterV().right(); d += elm.Line().right(0.4)
d += elm.Label().at((x + 15.1, y - 1.35)).label("voltmeter")
save_drawing(d, "ch04_symbols")

# 4.2 Ideal source characteristics
fig, axs = plt.subplots(1, 2, figsize=(6.2, 2.4))
i = np.linspace(0, 5, 50)
axs[0].plot(i, np.full_like(i, 12), color=NAVY, lw=2.2, label="ideal")
axs[0].plot(i, 12 - 0.8 * i, color=COPPER, lw=1.8, ls="--", label="real (with r)")
axs[0].set_xlabel("current drawn (A)"); axs[0].set_ylabel("terminal voltage (V)")
axs[0].set_title("Voltage source", fontsize=10.5, color=NAVY); axs[0].set_ylim(0, 15); axs[0].legend(fontsize=8.5, frameon=False)
v = np.linspace(0, 20, 50)
axs[1].plot(v, np.full_like(v, 2), color=NAVY, lw=2.2, label="ideal")
axs[1].plot(v, 2 - v / 25, color=COPPER, lw=1.8, ls="--", label="real (with R$_p$)")
axs[1].set_xlabel("terminal voltage (V)"); axs[1].set_ylabel("current delivered (A)")
axs[1].set_title("Current source", fontsize=10.5, color=NAVY); axs[1].set_ylim(0, 2.6); axs[1].legend(fontsize=8.5, frameon=False, loc="lower left")
for a in axs: a.grid(alpha=0.25)
fig.tight_layout()
save_fig(fig, "ch04_source_graphs")

# 4.3 Topology: nodes, branches, meshes
d = drawing()
d += (vs := elm.SourceV().up().label("10 V", loc="top"))
d += elm.Line().right(0.5)
d += (r1 := elm.ResistorIEC().right().label("R$_1$", loc="top"))
d += (na := elm.Dot().label("A", loc="top", color=COPPER, fontsize=13))
d += (r3 := elm.ResistorIEC().right().label("R$_3$", loc="top"))
d += (nb := elm.Dot().label("B", loc="top", color=COPPER, fontsize=13))
d += elm.Line().right(2.6)
d += (is_ := elm.SourceI().down().label("2 A", loc="bot"))
d += elm.Line().left(2.6)
d += (nd := elm.Dot())
d += elm.Line().left().tox(r3.start)
d += (nc := elm.Dot().label("C", loc="bot", color=COPPER, fontsize=13))
d += elm.Line().left().tox(vs.start)
d += elm.ResistorIEC().down().at(na.center).toy(nc.center).label("R$_2$", loc="top")
d += elm.ResistorIEC().down().at(nb.center).toy(nd.center).label("R$_4$", loc="top")
d += elm.Label().at((1.6, 1.5)).label("mesh 1", color=TEAL, fontsize=10)
d += elm.Label().at((4.6, 1.5)).label("mesh 2", color=TEAL, fontsize=10)
d += elm.Label().at((7.6, 1.5)).label("mesh 3", color=TEAL, fontsize=10)
save_drawing(d, "ch04_topology")

# 4.4 Same circuit drawn two ways
d = drawing()
d += (s := elm.SourceV().up().label("V$_S$", loc="top"))
d += elm.Line().right(1)
d += (t := elm.Dot())
d += elm.ResistorIEC().down().label("R$_1$", loc="bot")
d += (b := elm.Dot())
d += elm.Line().right(2.5).at(t.center)
d += elm.Line().down(0.5)
d += elm.ResistorIEC().down().length(2).label("R$_2$", loc="bot")
d += elm.Line().down(0.5)
d += elm.Line().left(2.5)
d += elm.Line().left().tox(s.start)
d += elm.Label().at((2.3, -1.4)).label("(a)", fontsize=12)
ox = 7.5
d += (s2 := elm.SourceV().up().at((ox, 0)).length(3).label("V$_S$", loc="top"))
d += elm.Line().right(1.2)
d += (j1 := elm.Dot())
d += elm.Line().right(3.3)
d += elm.ResistorIEC().down().length(3).label("R$_2$", loc="bot")
d += elm.Line().left(1.2)
d += (j2 := elm.Dot())
d += elm.Line().left().tox(ox)
d += elm.Line().down(1.4).at(j1.center)
d += elm.ResistorIEC().right().length(2.1).label("R$_1$", loc="top")
d += elm.Line().down().toy(0)
d += elm.Label().at((ox + 2.3, -1.4)).label("(b)", fontsize=12)
save_drawing(d, "ch04_redraw")

# 4.5 Reference node and node voltages
d = drawing()
d += (s := elm.SourceV().up().label("12 V", loc="top"))
d += (a := elm.Dot().label("A", loc="top", color=COPPER, fontsize=13))
d += elm.ResistorIEC().right().label("4 Ω", loc="top")
d += (b := elm.Dot().label("B", loc="top", color=COPPER, fontsize=13))
d += elm.ResistorIEC().down().label("2 Ω", loc="bot")
d += (c := elm.Dot())
d += elm.Line().left().tox(s.start)
d += elm.Line().down(0.6).at(c.center.__class__((1.5, 0))) if False else elm.Line().down(0.5).at((1.5, 0))
d += elm.Ground()
save_drawing(d, "ch04_reference")

# 4.6 Passive sign convention
d = drawing()
d += (w := elm.Line().right(2))
d += elm.Arrow().right(1.2).at((0.4, 0.45)).color(COPPER).label("I", loc="top", color=COPPER)
d += (r := elm.ResistorIEC().right().label(("+", "V", "−"), loc="top"))
d += elm.Line().right(1)
d += elm.Label().at((3.0, -1.2)).label("current enters at + :  P = VI is power ABSORBED", fontsize=10.5, color=NAVY)
save_drawing(d, "ch04_psc")
