import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
import numpy as np

# 8.1 Loaded divider
d = drawing()
d += (s := elm.SourceV().up().length(6).label("12 V", loc="top"))
d += elm.Line().right(2)
d += elm.ResistorIEC().down().label("R$_1$ = 10 kΩ", loc="top")
d += (m := elm.Dot())
d += elm.ResistorIEC().down().label("R$_2$ = 10 kΩ", loc="top")
d += (b := elm.Dot())
d += elm.Line().left().tox(s.start)
d += elm.Line().right(2.6).at(m.center)
d += elm.Label().at((3.3, 3.35)).label("V$_{out}$", color=COPPER)
d += elm.ResistorIEC().down().label("R$_L$ (load)", loc="bot").color(COPPER)
d += elm.Line().left(2.6)
d += elm.Arrow().down(0.9).at((4.15, 2.6)).color(COPPER).label("I$_L$", loc="top", color=COPPER)
save_drawing(d, "ch08_loaded")

# 8.2 Output vs load resistance
r = np.logspace(-1, 2, 300)
fig, ax = plt.subplots(figsize=(5.6, 2.7))
vout = 12 * (r / (1 + r)) / (1 + r / (1 + r))
ax.semilogx(r, vout, color=NAVY, lw=2.2)
ax.axhline(6, color=COPPER, ls="--", lw=1.2)
ax.text(0.12, 6.2, "unloaded output, 6 V", color=COPPER, fontsize=9.5)
for k in [1, 10]:
    v = 12 * (k / (1 + k)) / (1 + k / (1 + k))
    ax.plot(k, v, "o", color=COPPER)
    ax.annotate(f"R$_L$ = {k}R$_2$: {v:.2f} V", (k, v), xytext=(8, -16), textcoords="offset points", fontsize=9, color=NAVY)
ax.set_xlabel("load resistance as a multiple of R$_2$ (R$_L$ / R$_2$)"); ax.set_ylabel("V$_{out}$ (V)")
ax.set_ylim(0, 7); ax.grid(alpha=0.25, which="both")
save_fig(fig, "ch08_load_curve")

# 8.3 Ammeter shunt
d = drawing()
d += elm.Dot(open=True).label("I = 1 A", loc="left")
d += elm.Line().right(1)
d += (j1 := elm.Dot())
d += elm.Line().up(1.2)
d += elm.MeterA().right(3).label("movement\n1 mA, 100 Ω", loc="top")
d += elm.Line().down(1.2)
d += (j2 := elm.Dot())
d += elm.ResistorIEC().left().at(j2.center).to(j1.center).label("R$_{sh}$ (shunt)", loc="bot").color(COPPER)
d += elm.Line().right(1).at(j2.center)
d += elm.Dot(open=True)
save_drawing(d, "ch08_shunt")

# 8.4 Voltmeter multiplier
d = drawing()
d += elm.Dot(open=True).label("+", loc="left")
d += elm.ResistorIEC().right().label("R$_{mult}$", loc="top").color(COPPER)
d += elm.MeterA().right().label("movement\n1 mA, 100 Ω", loc="top")
d += elm.Dot(open=True).label("−", loc="right")
d += elm.Label().at((3.0, -1.1)).label("10 V full scale  ⇒  total resistance 10 kΩ", fontsize=10, color=NAVY)
save_drawing(d, "ch08_multiplier")

# 8.5 Wheatstone bridge
d = drawing()
d += (s := elm.SourceV().up().length(4).label("V$_S$", loc="top"))
ox = 2.5
T, L, Rp, B = (ox + 1.8, 4), (ox, 2), (ox + 3.6, 2), (ox + 1.8, 0)
d += elm.Line().at((0, 4)).to(T)
d += elm.Dot().at(T)
d += elm.ResistorIEC().at(T).to(L).label("R$_1$", loc="top")
d += elm.ResistorIEC().at(T).to(Rp).label("R$_2$", loc="top")
d += elm.ResistorIEC().at(L).to(B).label("R$_3$", loc="bot")
d += elm.ResistorVarIEC().at(Rp).to(B).label("R$_4$", loc="bot")
d += elm.Line().at(L).to((ox + 0.9, 2))
d += elm.MeterA().endpoints((ox + 0.9, 2), (ox + 2.7, 2)).label("G", loc="top", fontsize=12, color=COPPER)
d += elm.Line().at((ox + 2.7, 2)).to(Rp)
d += elm.Dot().at(L).label("C", loc="left", color=COPPER); d += elm.Dot().at(Rp).label("D", loc="right", color=COPPER)
d += elm.Dot().at(B)
d += elm.Line().at(B).to((0, 0))
save_drawing(d, "ch08_wheatstone")

# 8.6 Strain gauge sketch
fig, ax = plt.subplots(figsize=(5.0, 2.0))
ax.add_patch(plt.Rectangle((0, 0), 6, 2.2, fc="#f6efe2", ec=GREY, lw=1))
xs = np.linspace(1.0, 5.0, 11)
path_x, path_y = [0.5, 1.0], [1.1, 1.1]
for i, x in enumerate(xs):
    y0, y1 = (0.4, 1.8) if i % 2 == 0 else (1.8, 0.4)
    path_x += [x, x]; path_y += [y0, y1]
path_x += [5.5]; path_y += [path_y[-1]]
path_x = [0.5, 1.0] + [v for i, x in enumerate(xs) for v in (x, x)] + [5.0]
path_y = [0.4, 0.4]
for i in range(len(xs)):
    path_y += [0.4, 1.8] if i % 2 == 0 else [1.8, 0.4]
path_y += [path_y[-1]]
ax.plot(path_x[:len(path_y)], path_y, color=COPPER, lw=2.2)
ax.annotate("", xy=(-0.9, 1.1), xytext=(-0.1, 1.1), arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.8))
ax.annotate("", xy=(6.9, 1.1), xytext=(6.1, 1.1), arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.8))
ax.text(3, -0.45, "stretching lengthens and narrows the foil, raising its resistance", ha="center", fontsize=9.5, color=GREY)
ax.set_xlim(-1.2, 7.2); ax.set_ylim(-0.8, 2.5); ax.set_aspect("equal"); ax.axis("off")
save_fig(fig, "ch08_strain")

# 8.7 Thermistor divider output
T = np.linspace(0, 100, 200)
R = 10 * np.exp(3950 * (1 / (T + 273.15) - 1 / 298.15))
fig, ax = plt.subplots(figsize=(5.4, 2.6))
ax.plot(T, 5 * 10 / (10 + R), color=COPPER, lw=2.2)
ax.set_xlabel("temperature (°C)"); ax.set_ylabel("V$_{out}$ (V)")
ax.grid(alpha=0.25)
ax.plot(25, 2.5, "o", color=NAVY); ax.annotate("2.50 V at 25 °C", (25, 2.5), xytext=(10, -14), textcoords="offset points", fontsize=9, color=NAVY)
save_fig(fig, "ch08_thermistor")
