import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
import numpy as np
from matplotlib.patches import FancyBboxPatch

# 14.1 Concept: any linear network -> Vth + Rth
fig, ax = plt.subplots(figsize=(6.2, 2.4))
ax.add_patch(FancyBboxPatch((0, 0.3), 2.6, 2.0, boxstyle="round,pad=0.05,rounding_size=0.15", fc=LIGHT, ec=NAVY, lw=1.5))
ax.text(1.3, 1.55, "any linear\nnetwork of sources\nand resistors", ha="center", va="center", fontsize=10, color=NAVY)
for y in (2.0, 0.6):
    ax.plot([2.6, 3.3], [y, y], color="k", lw=1.5); ax.plot(3.3, y, "o", mfc="white", mec="k", ms=7)
ax.text(3.45, 2.0, "a", fontsize=12, va="center"); ax.text(3.45, 0.6, "b", fontsize=12, va="center")
ax.text(4.05, 1.3, "≡", fontsize=26, ha="center", va="center", color=COPPER)
ox = 5.0
ax.add_patch(plt.Circle((ox + 0.4, 1.3), 0.38, fc="white", ec="k", lw=1.5))
ax.text(ox + 0.4, 1.45, "+", ha="center", va="center", fontsize=12); ax.text(ox + 0.4, 1.12, "−", ha="center", va="center", fontsize=12)
ax.text(ox - 0.05, 1.3, "V$_{Th}$", ha="right", va="center", fontsize=12, color=COPPER)
ax.plot([ox + 0.4, ox + 0.4], [1.68, 2.0], color="k", lw=1.5); ax.plot([ox + 0.4, ox + 0.4], [0.92, 0.6], color="k", lw=1.5)
ax.plot([ox + 0.4, ox + 0.8], [2.0, 2.0], color="k", lw=1.5)
ax.add_patch(plt.Rectangle((ox + 0.8, 1.88), 0.8, 0.24, fc="white", ec="k", lw=1.5))
ax.text(ox + 1.2, 2.35, "R$_{Th}$", ha="center", fontsize=12, color=COPPER)
ax.plot([ox + 1.6, ox + 2.2], [2.0, 2.0], color="k", lw=1.5); ax.plot([ox + 0.4, ox + 2.2], [0.6, 0.6], color="k", lw=1.5)
for y in (2.0, 0.6): ax.plot(ox + 2.2, y, "o", mfc="white", mec="k", ms=7)
ax.text(ox + 2.35, 2.0, "a", fontsize=12, va="center"); ax.text(ox + 2.35, 0.6, "b", fontsize=12, va="center")
ax.set_xlim(-0.1, 7.8); ax.set_ylim(0.1, 2.7); ax.set_aspect("equal"); ax.axis("off")
save_fig(fig, "ch14_concept")

# 14.2 Example circuit and its three stages
def base(d, ox, src=True, title="", load=None, short_ab=False):
    if src:
        d += elm.SourceV().up().at((ox, 0)).label("24 V", loc="top")
    else:
        d += elm.Line().up(3).at((ox, 0)).color(COPPER)
    d += elm.ResistorIEC().right().label("6 Ω", loc="top")
    d += elm.Dot()
    d += elm.ResistorIEC().right().label("2 Ω", loc="top")
    d += elm.Dot(open=True).label("a", loc="right")
    d += elm.ResistorIEC().down().at((ox + 3, 3)).label("12 Ω", loc="bot")
    d += elm.Line().at((ox, 0)).to((ox + 6, 0))
    d += elm.Dot().at((ox + 3, 0)); d += elm.Dot(open=True).at((ox + 6, 0)).label("b", loc="right")
    if load:
        d += elm.ResistorIEC().down().at((ox + 6, 3)).label(load, loc="bot").color(COPPER)
    d += elm.Label().at((ox + 3, -1.0)).label(title, fontsize=11)

d = drawing()
base(d, 0, True, "(a) the circuit with load R$_L$", load="R$_L$")
base(d, 9, True, "(b) load removed: find V$_{oc}$")
base(d, 18, False, "(c) source off: find R$_{Th}$")
save_drawing(d, "ch14_stages")

# 14.3 Load current against load resistance (Vth=16, Rth=6)
RL = np.linspace(0, 40, 400)
fig, axs = plt.subplots(1, 2, figsize=(6.2, 2.4))
axs[0].plot(RL, 16 / (6 + RL), color=NAVY, lw=2.2)
for r in (2, 6, 10):
    axs[0].plot(r, 16 / (6 + r), "o", color=COPPER)
axs[0].set_ylabel("load current (A)"); axs[0].set_ylim(0, 3)
axs[1].plot(RL, 16 * RL / (6 + RL), color=COPPER, lw=2.2)
axs[1].axhline(16, color=GREY, ls="--", lw=1); axs[1].text(20, 14.6, "V$_{Th}$ = 16 V", fontsize=9, color=GREY)
axs[1].set_ylabel("load voltage (V)"); axs[1].set_ylim(0, 17.5)
for a_ in axs:
    a_.set_xlabel("load resistance R$_L$ (Ω)"); a_.grid(alpha=0.25)
fig.tight_layout()
save_fig(fig, "ch14_load")

# 14.4 Bridge with R5 removed
d = drawing()
d += elm.SourceV().up().length(4).label("20 V", loc="top")
ox = 2.5
T, L, Rp, B = (ox + 1.8, 4), (ox, 2), (ox + 3.6, 2), (ox + 1.8, 0)
d += elm.Line().at((0, 4)).to(T)
d += elm.ResistorIEC().endpoints(T, L).label("6 Ω", loc="top")
d += elm.ResistorIEC().endpoints(T, Rp).label("3 Ω", loc="top")
d += elm.ResistorIEC().endpoints(L, B).label("5 Ω", loc="bot")
d += elm.ResistorIEC().endpoints(Rp, B).label("6.5 Ω", loc="bot")
d += elm.Dot(open=True).at(L).label("C", loc="left", color=COPPER); d += elm.Dot(open=True).at(Rp).label("D", loc="right", color=COPPER)
d += elm.Dot().at(T); d += elm.Dot().at(B)
d += elm.Line().at(B).to((0, 0))
d += elm.Label().at((ox + 1.8, 2.0)).label("R$_5$ removed", fontsize=10, color=GREY)
save_drawing(d, "ch14_bridge")

# 14.5 Network with dependent source
d = drawing()
d += elm.SourceV().up().at((0, 0)).label("6 V", loc="top")
d += elm.ResistorIEC().right().label("2 Ω", loc="top")
d += elm.Dot()
d += elm.Line().right(2)
d += elm.Dot(open=True).label("a", loc="right")
d += elm.SourceControlledI().down().at((3, 3)).label("0.25 V$_{ab}$", loc="bot")
d += elm.Line().at((0, 0)).to((5, 0))
d += elm.Dot().at((3, 0)); d += elm.Dot(open=True).at((5, 0)).label("b", loc="right")
save_drawing(d, "ch14_dependent")
