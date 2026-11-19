import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
import numpy as np

# 18.1 Monte Carlo: divider output with 5 % resistors
rng = np.random.default_rng(1)
R1 = 10e3 * (1 + rng.uniform(-0.05, 0.05, 20000)); R2 = 10e3 * (1 + rng.uniform(-0.05, 0.05, 20000))
V = 12 * R2 / (R1 + R2)
fig, ax = plt.subplots(figsize=(5.4, 2.5))
ax.hist(V, bins=60, color=NAVY, alpha=0.85)
for x in (5.7, 6.3):
    ax.axvline(x, color=COPPER, ls="--", lw=1.4)
ax.text(5.71, ax.get_ylim()[1] * 0.85, "worst-case\nlimits", color=COPPER, fontsize=9)
ax.set_xlabel("divider output (V)"); ax.set_ylabel("number of circuits"); ax.set_xlim(5.6, 6.4)
save_fig(fig, "ch18_tolerance")

# 18.2 Four-wire (Kelvin) measurement
d = drawing()
d += elm.SourceI().up().at((0, 0)).label("test\ncurrent", loc="top")
d += elm.ResistorIEC().right().label("lead", loc="top").color(GREY)
d += elm.Line().right(1)
d += elm.Dot()
d += elm.ResistorIEC().down().label("R$_x$", loc="bot").color(COPPER)
d += elm.Dot()
d += elm.Line().left(1)
d += elm.ResistorIEC().left().label("lead", loc="bot").color(GREY)
d += elm.Line().right(2.2).at((4, 3)); d += elm.MeterV().down().label("voltmeter\n(sense leads)", loc="bot"); d += elm.Line().left(2.2)
save_drawing(d, "ch18_kelvin")

# 18.3 Fault-finding circuit with test points (Figure 7.2 circuit)
d = drawing()
d += elm.SourceV().up().at((0, 0)).label("60 V", loc="top")
d += elm.Line().right(0.4)
d += elm.ResistorIEC().right().label("R$_1$ = 5 Ω", loc="top")
d += elm.Dot().label("TP-A", loc="top", color=COPPER)
d += elm.ResistorIEC().down().label("R$_2$ = 20 Ω", loc="top")
d += elm.Line().at((3.4, 3)).right(0.6)
d += elm.ResistorIEC().right().label("R$_3$ = 12 Ω", loc="top")
d += elm.Dot().label("TP-B", loc="top", color=COPPER)
d += elm.ResistorIEC().down().label("R$_4$ = 12 Ω", loc="top")
d += elm.Line().at((7, 3)).right(2.4)
d += elm.ResistorIEC().down().label("R$_5$ = 24 Ω", loc="bot")
d += elm.Line().at((0, 0)).to((9.4, 0))
d += elm.Dot().at((3.4, 0)); d += elm.Dot().at((7, 0))
d += elm.Line().at((4.7, 0)).down(0.4); d += elm.Ground()
save_drawing(d, "ch18_fault")

# 18.4 Half-split search along a string
fig, ax = plt.subplots(figsize=(6.0, 1.7))
for i in range(8):
    x = i * 1.0
    c = RED if i == 5 else NAVY
    ax.add_patch(plt.Circle((x + 0.5, 0.5), 0.3, fc="white", ec=c, lw=1.6))
    ax.text(x + 0.5, 0.5, str(i + 1), ha="center", va="center", fontsize=10, color=c)
ax.plot([0, 8], [0.5, 0.5], color=GREY, lw=0.8, zorder=0)
ax.annotate("", xy=(4, 1.15), xytext=(4, 1.55), arrowprops=dict(arrowstyle="-|>", color=COPPER))
ax.text(4, 1.62, "1st test", ha="center", fontsize=9, color=COPPER)
ax.annotate("", xy=(6, 1.15), xytext=(6, 1.55), arrowprops=dict(arrowstyle="-|>", color=TEAL))
ax.text(6, 1.62, "2nd", ha="center", fontsize=9, color=TEAL)
ax.annotate("", xy=(5, 1.15), xytext=(5, 1.55), arrowprops=dict(arrowstyle="-|>", color=NAVY))
ax.text(5, 1.62, "3rd", ha="center", fontsize=9, color=NAVY)
ax.text(5.5, -0.1, "faulty", ha="center", fontsize=9, color=RED)
ax.set_xlim(-0.2, 8.2); ax.set_ylim(-0.3, 1.9); ax.set_aspect("equal"); ax.axis("off")
save_fig(fig, "ch18_halfsplit")

# 18.5 RC charging
t = np.linspace(0, 5, 300)
fig, ax = plt.subplots(figsize=(5.2, 2.5))
ax.plot(t, 12 * (1 - np.exp(-t)), color=COPPER, lw=2.2)
ax.axhline(12, color=GREY, ls="--", lw=1)
ax.plot(1, 12 * (1 - np.exp(-1)), "o", color=NAVY)
ax.annotate("after one time constant\n(RC = 1 s): 63 % of 12 V", (1, 7.59), xytext=(1.6, 4.0), fontsize=9, color=NAVY,
            arrowprops=dict(arrowstyle="-|>", color=NAVY))
ax.set_xlabel("time (s)"); ax.set_ylabel("capacitor voltage (V)"); ax.grid(alpha=0.25); ax.set_ylim(0, 13.5)
save_fig(fig, "ch18_rc")

# 18.6 LED load line
v = np.linspace(0, 5, 1000)
Is, n, Vt = 1e-19, 2.0, 0.02585
iled = Is * (np.exp(v / (n * Vt)) - 1) * 1000  # mA
iload = (5 - v) / 1.0  # mA with 1 kOhm
k = np.argmin(np.abs(iled - iload))
fig, ax = plt.subplots(figsize=(5.2, 2.7))
ax.plot(v, np.clip(iled, 0, 7), color=TEAL, lw=2.2, label="LED characteristic")
ax.plot(v, iload, color=NAVY, lw=2.2, label="load line: 5 V source, 1 kΩ")
ax.plot(v[k], iload[k], "o", color=COPPER, ms=7)
ax.annotate(f"operating point\n≈ {v[k]:.2f} V, {iload[k]:.1f} mA", (v[k], iload[k]), xytext=(2.7, 3.6), fontsize=9, color=COPPER,
            arrowprops=dict(arrowstyle="-|>", color=COPPER))
ax.set_xlabel("LED voltage (V)"); ax.set_ylabel("current (mA)"); ax.set_ylim(0, 7.5); ax.set_xlim(0, 5.2)
ax.legend(fontsize=8.5, frameon=False, loc="upper right"); ax.grid(alpha=0.25)
save_fig(fig, "ch18_loadline")
print("LED op point", v[k], iload[k])
