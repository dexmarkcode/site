import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
import numpy as np
from matplotlib.patches import Circle, Ellipse, Rectangle, FancyBboxPatch

# 2.1 Electron colliding with ions
fig, ax = plt.subplots(figsize=(6.2, 2.4))
for x in range(10):
    for y in range(3):
        ax.add_patch(Circle((x + 0.5 + 0.5 * (y % 2), y + 0.5), 0.27, fc=LIGHT, ec=NAVY, lw=1))
path = np.array([[0.1, 1.1], [1.0, 0.95], [1.6, 1.35], [2.5, 1.0], [3.2, 1.6], [4.1, 1.15], [4.8, 1.55], [5.9, 0.95], [6.6, 1.45], [7.7, 1.05], [8.4, 1.6], [9.4, 1.1], [10.3, 1.35]])
ax.plot(path[:, 0], path[:, 1], color=COPPER, lw=1.6)
ax.annotate("", xy=path[-1], xytext=path[-2], arrowprops=dict(arrowstyle="-|>", color=COPPER, lw=1.6))
for p in path[1:-1]:
    ax.plot(*p, marker="*", color=RED, ms=7)
ax.text(5.3, 3.35, "each collision (red star) turns some of the electron's energy into heat", ha="center", fontsize=9.5, color=GREY)
ax.set_xlim(-0.2, 11); ax.set_ylim(-0.1, 3.6); ax.set_aspect("equal"); ax.axis("off")
save_fig(fig, "ch02_collisions")

# 2.2 Wire geometry: length and cross-sectional area
fig, ax = plt.subplots(figsize=(6.0, 2.0))
ax.add_patch(Rectangle((1, 0.5), 6, 1, fc="#f4d6c4", ec=COPPER, lw=1.4))
ax.add_patch(Ellipse((1, 1), 0.45, 1, fc="#e9b08f", ec=COPPER, lw=1.4))
ax.add_patch(Ellipse((7, 1), 0.45, 1, fc="#f4d6c4", ec=COPPER, lw=1.4, ls="--"))
ax.annotate("", xy=(1, 0.15), xytext=(7, 0.15), arrowprops=dict(arrowstyle="<|-|>", color=NAVY))
ax.text(4, -0.05, "length, L", ha="center", va="top", color=NAVY, fontsize=11)
ax.annotate("cross-sectional\narea, A", xy=(1, 1), xytext=(-1.6, 1.3), fontsize=11, color=NAVY, ha="center",
            arrowprops=dict(arrowstyle="-|>", color=NAVY))
ax.text(8.0, 1.0, "R = ρL / A", fontsize=14, color=COPPER, va="center")
ax.set_xlim(-2.8, 10.5); ax.set_ylim(-0.6, 2.0); ax.set_aspect("equal"); ax.axis("off")
save_fig(fig, "ch02_geometry")

# 2.3 Resistance against temperature
T = np.linspace(-20, 120, 200)
fig, axs = plt.subplots(1, 2, figsize=(6.2, 2.5))
axs[0].plot(T, 100 * (1 + 0.0039 * (T - 20)), color=NAVY, lw=2)
axs[0].set_title("Copper (100 Ω at 20 °C)", fontsize=10.5, color=NAVY)
axs[0].set_xlabel("temperature (°C)"); axs[0].set_ylabel("resistance (Ω)")
B = 3950
R = 10000 * np.exp(B * (1 / (T + 273.15) - 1 / 298.15))
axs[1].plot(T, R / 1000, color=COPPER, lw=2)
axs[1].set_title("NTC thermistor (10 kΩ at 25 °C)", fontsize=10.5, color=COPPER)
axs[1].set_xlabel("temperature (°C)"); axs[1].set_ylabel("resistance (kΩ)")
axs[1].set_ylim(0, 80)
for a in axs:
    a.grid(alpha=0.25)
fig.tight_layout()
save_fig(fig, "ch02_temperature")

# 2.4 Resistor symbols
d = drawing()
d.config(fontsize=11)
items = [(elm.ResistorIEC, "fixed resistor\n(IEC / UK)"), (elm.Resistor, "fixed resistor\n(US style)"),
         (elm.ResistorVarIEC, "variable\nresistor"), (elm.PotentiometerIEC, "potentiometer"),
         (elm.Photoresistor, "light-dependent\nresistor (LDR)")]
x = 0
for e, lab in items:
    d += elm.Line().right(0.5).at((x, 0))
    el = e().right()
    d += el
    d += elm.Line().right(0.5)
    d += elm.Label().at((x + 1.75, -1.4)).label(lab, fontsize=10)
    x += 4.3
save_drawing(d, "ch02_symbols")

# 2.5 Through-hole resistor colour bands
fig, ax = plt.subplots(figsize=(5.4, 1.6))
ax.plot([0, 1.4], [0.5, 0.5], color="#8d8d8d", lw=2.5)
ax.plot([4.6, 6.0], [0.5, 0.5], color="#8d8d8d", lw=2.5)
ax.add_patch(FancyBboxPatch((1.4, 0.15), 3.2, 0.7, boxstyle="round,pad=0.02,rounding_size=0.3", fc="#e8d7b0", ec="#9a8457", lw=1.2))
for x, c, n in [(1.9, "#ffd700", "yellow\n4"), (2.35, "#7b2fbe", "violet\n7"), (2.8, "#d62728", "red\n× 100"), (3.95, "#c9a227", "gold\n± 5 %")]:
    ax.add_patch(Rectangle((x - 0.13, 0.15), 0.26, 0.7, fc=c, ec="none"))
    ax.text(x, -0.15, n, ha="center", va="top", fontsize=8.8, color=NAVY)
ax.text(6.3, 0.5, "= 4700 Ω\n= 4.7 kΩ ± 5 %", fontsize=11, va="center", color=COPPER)
ax.set_xlim(-0.2, 8.6); ax.set_ylim(-1.0, 1.0); ax.set_aspect("equal"); ax.axis("off")
save_fig(fig, "ch02_colour")

# 2.6 Power of household appliances
apps = ["Phone charger", "LED bulb", "Laptop", "Television", "Fridge (running)", "Microwave", "Hairdryer", "Kettle", "Electric shower"]
pw = [10, 8, 60, 100, 150, 900, 1800, 3000, 9500]
fig, ax = plt.subplots(figsize=(6.0, 3.1))
cols = [NAVY if p < 1000 else COPPER for p in pw]
ax.barh(apps, pw, color=cols)
ax.set_xscale("log"); ax.set_xlabel("typical power (W) – note the logarithmic scale")
for i, p in enumerate(pw):
    ax.text(p * 1.12, i, f"{p:,} W", va="center", fontsize=9, color=GREY)
ax.set_xlim(5, 40000)
ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
save_fig(fig, "ch02_appliances")
