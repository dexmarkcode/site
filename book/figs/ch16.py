import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
import numpy as np

# 16.1 Thevenin source with variable load
d = drawing()
d += elm.SourceV().up().at((0, 0)).label("V$_{Th}$", loc="top")
d += elm.ResistorIEC().right().label("R$_{Th}$", loc="top")
d += elm.Line().right(1.6)
d += elm.ResistorVarIEC().down().label("R$_L$", loc="bot").color(COPPER)
d += elm.Line().at((0, 0)).to((4.6, 0))
for a, b in [((-1.4, -0.4), (3.5, -0.4)), ((3.5, -0.4), (3.5, 4.1)), ((3.5, 4.1), (-1.4, 4.1)), ((-1.4, 4.1), (-1.4, -0.4))]:
    d += elm.Line().at(a).to(b).linestyle("--").color(GREY)
d += elm.Label().at((1.05, 4.45)).label("the source", fontsize=10, color=GREY)
d += elm.Arrow().down(0.9).at((5.15, 2.5)).color(COPPER).label("I$_L$", loc="bot", color=COPPER)
save_drawing(d, "ch16_circuit")

# 16.2 Power against load resistance
RL = np.linspace(0.01, 36, 500)
P = 16 ** 2 * RL / (6 + RL) ** 2
fig, ax = plt.subplots(figsize=(5.6, 2.8))
ax.plot(RL, P, color=COPPER, lw=2.4)
ax.axvline(6, color=GREY, ls="--", lw=1)
ax.plot(6, 16 ** 2 / 24, "o", color=NAVY)
ax.annotate("maximum: 10.67 W\nat R$_L$ = R$_{Th}$ = 6 Ω", (6, 10.67), xytext=(12, 8.2), fontsize=9.5, color=NAVY,
            arrowprops=dict(arrowstyle="-|>", color=NAVY))
ax.set_xlabel("load resistance R$_L$ (Ω)"); ax.set_ylabel("load power P$_L$ (W)")
ax.set_ylim(0, 12); ax.grid(alpha=0.25)
save_fig(fig, "ch16_power")

# 16.3 Power and efficiency against RL/Rth
k = np.logspace(-2, 2, 400)
fig, ax = plt.subplots(figsize=(5.6, 2.8))
ax.semilogx(k, 4 * k / (1 + k) ** 2 * 100, color=COPPER, lw=2.2, label="load power (% of maximum)")
ax.semilogx(k, k / (1 + k) * 100, color=NAVY, lw=2.2, label="efficiency η (%)")
ax.axvline(1, color=GREY, ls="--", lw=1)
ax.text(1.12, 8, "matched\nR$_L$ = R$_{Th}$", fontsize=9, color=GREY)
ax.set_xlabel("R$_L$ / R$_{Th}$"); ax.set_ylabel("%"); ax.set_ylim(0, 105)
ax.legend(fontsize=8.5, frameon=False, loc="center left"); ax.grid(alpha=0.25, which="both")
save_fig(fig, "ch16_efficiency")

# 16.4 Solar cell I-V and P-V curves
V = np.linspace(0, 0.75, 500)
I = 8.5 - 1e-9 * (np.exp(V / 0.0257 / 1.2) - 1)
I = np.clip(I, 0, None)
V, I = V[I > 0], I[I > 0]
Pw = V * I
k = np.argmax(Pw)
fig, ax = plt.subplots(figsize=(5.6, 2.8))
ax.plot(V, I, color=NAVY, lw=2.2, label="current (A)")
ax2 = ax.twinx()
ax2.plot(V, Pw, color=COPPER, lw=2.2, label="power (W)")
ax2.plot(V[k], Pw[k], "o", color=COPPER)
ax2.annotate(f"maximum power point\n{V[k]:.2f} V, {Pw[k]:.1f} W", (V[k], Pw[k]), xytext=(0.05, Pw[k] * 0.55), fontsize=9, color=COPPER,
             arrowprops=dict(arrowstyle="-|>", color=COPPER))
ax.set_xlabel("cell voltage (V)"); ax.set_ylabel("current (A)", color=NAVY); ax2.set_ylabel("power (W)", color=COPPER)
ax.set_ylim(0, 10); ax2.set_ylim(0, 6); ax.grid(alpha=0.25)
ax2.spines["right"].set_visible(True)
save_fig(fig, "ch16_solar")
