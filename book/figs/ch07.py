import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
import numpy as np

def vsrc(d, lab, at=None, length=None):
    e = elm.SourceV().up().label(lab, loc="top")
    if at is not None: e = e.at(at)
    if length: e = e.length(length)
    d += e
    return e

# 7.1 basic series-parallel
d = drawing()
s = vsrc(d, "24 V")
d += elm.Line().right(0.4)
d += elm.ResistorIEC().right().label("R$_1$ = 4 Ω", loc="top")
d += (t := elm.Dot().label("A", loc="top", color=COPPER))
d += elm.ResistorIEC().down().label("R$_2$ = 6 Ω", loc="top")
d += (b := elm.Dot())
d += elm.Line().left().tox(s.start)
d += elm.Line().right(2.4).at(t.center)
d += elm.ResistorIEC().down().label("R$_3$ = 12 Ω", loc="bot")
d += elm.Line().left(2.4)
save_drawing(d, "ch07_basic")

# 7.2 ladder
d = drawing()
s = vsrc(d, "30 V")
d += elm.Line().right(0.4)
d += elm.ResistorIEC().right().label("R$_1$ = 10 Ω", loc="top")
d += (a := elm.Dot().label("A", loc="top", color=COPPER))
d += elm.ResistorIEC().right().label("R$_3$ = 10 Ω", loc="top")
d += (bb := elm.Dot().label("B", loc="top", color=COPPER))
d += elm.Line().right(1.2)
d += elm.ResistorIEC().down().label("R$_4$ = 30 Ω", loc="bot")
d += elm.Line().left().tox(s.start)
d += elm.ResistorIEC().down().at(a.center).toy(0).label("R$_2$ = 40 Ω", loc="bot")
d += elm.Dot().at((a.center[0], 0))
d += elm.ResistorIEC().down().at(bb.center).toy(0).label("", loc="bot") if False else elm.Line().length(0.001)
save_drawing(d, "ch07_ladder")

# 7.3 same network, different terminals
d = drawing()
d += (a := elm.Dot(open=True).label("A", loc="left"))
d += elm.ResistorIEC().right().at((0, 0)).to((4, 0)).label("9 Ω", loc="bot")
d += (bdot := elm.Dot(open=True).label("B", loc="right"))
d += elm.ResistorIEC().at((0, 0)).to((2, 2.6)).label("6 Ω", loc="top")
d += (c := elm.Dot(open=True).label("C", loc="top"))
d += elm.ResistorIEC().at((2, 2.6)).to((4, 0)).label("3 Ω", loc="top")
save_drawing(d, "ch07_terminals")

# 7.4 multi-level network
d = drawing()
s = vsrc(d, "60 V")
d += elm.Line().right(0.4)
d += elm.ResistorIEC().right().label("R$_1$ = 5 Ω", loc="top")
d += (a := elm.Dot().label("A", loc="top", color=COPPER))
d += elm.ResistorIEC().down().label("R$_2$ = 20 Ω", loc="top")
d += (ab := elm.Dot())
d += elm.Line().left().tox(s.start)
d += elm.Line().right(0.6).at(a.center)
d += elm.ResistorIEC().right().label("R$_3$ = 12 Ω", loc="top")
d += (bnode := elm.Dot().label("B", loc="top", color=COPPER))
d += elm.ResistorIEC().down().label("R$_4$ = 12 Ω", loc="top")
d += (bb := elm.Dot())
d += elm.Line().left().tox(ab.center)
d += elm.Line().right(2.4).at(bnode.center)
d += elm.ResistorIEC().down().label("R$_5$ = 24 Ω", loc="bot")
d += elm.Line().left(2.4)
save_drawing(d, "ch07_multi")

# 7.5 Reduction steps for 7.4
fig, axs = plt.subplots(1, 4, figsize=(6.4, 1.7))
steps = [("R$_4$ || R$_5$", "12 || 24 = 8 Ω"), ("+ R$_3$", "12 + 8 = 20 Ω"), ("|| R$_2$", "20 || 20 = 10 Ω"), ("+ R$_1$", "5 + 10 = 15 Ω")]
for ax, (a_, b_) in zip(axs, steps):
    ax.add_patch(plt.Rectangle((0.05, 0.1), 0.9, 0.8, fc=LIGHT, ec=NAVY, lw=1.2, transform=ax.transAxes))
    ax.text(0.5, 0.65, a_, ha="center", va="center", fontsize=11, color=COPPER, transform=ax.transAxes)
    ax.text(0.5, 0.35, b_, ha="center", va="center", fontsize=10.5, color=NAVY, transform=ax.transAxes)
    ax.axis("off")

save_fig(fig, "ch07_steps")

# 7.6 Cube of resistors
fig, ax = plt.subplots(figsize=(3.4, 3.2))
P = {0: (0, 0), 1: (2, 0), 2: (2, 2), 3: (0, 2), 4: (0.9, 0.8), 5: (2.9, 0.8), 6: (2.9, 2.8), 7: (0.9, 2.8)}
edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
for i, j in edges:
    (x1, y1), (x2, y2) = P[i], P[j]
    ax.plot([x1, x2], [y1, y2], color=NAVY, lw=1.2, ls="--" if 4 in (i, j) else "-")
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ang = np.degrees(np.arctan2(y2 - y1, x2 - x1))
    w = plt.Rectangle((-0.22, -0.07), 0.44, 0.14, fc="white", ec=COPPER, lw=1.3,
                      transform=matplotlib.transforms.Affine2D().rotate_deg(ang).translate(mx, my) + ax.transData)
    ax.add_patch(w)
for k, (x, y) in P.items():
    ax.plot(x, y, "o", color=NAVY, ms=4)
ax.plot(*P[0], "o", color=COPPER, ms=8); ax.plot(*P[6], "o", color=COPPER, ms=8)
ax.text(-0.15, -0.2, "A", color=COPPER, fontsize=13, ha="right")
ax.text(3.05, 2.95, "B", color=COPPER, fontsize=13)
ax.set_xlim(-0.6, 3.5); ax.set_ylim(-0.5, 3.3); ax.set_aspect("equal"); ax.axis("off")
import matplotlib
save_fig(fig, "ch07_cube")

# 7.7 Bridge: not series-parallel
d = drawing()
s = vsrc(d, "V$_S$", length=4)
d += elm.Line().right(1.5)
top = d.elements[-1]
d += elm.ResistorIEC().at(top.center).to((0, 0) if False else (top.center[0] - 1.6, 2)).label("R$_1$", loc="top") if False else elm.Line().length(0.001)
T = (1.5, 4); L = (0, 2); Rn = (3, 2); B = (1.5, 0)
L = (-0.2 + 1.5 - 1.7, 2)
L = (-0.2, 2)
L = (0.0 + 0.0, 2)
Lp, Rp = (0.0, 2), (3.0, 2)
# draw a diamond to the right of the source instead
ox = 2.5
T, Lp, Rp, B = (ox + 1.8, 4), (ox, 2), (ox + 3.6, 2), (ox + 1.8, 0)
d += elm.Line().at((1.5, 4)).to(T)
d += elm.Dot().at(T)
d += elm.ResistorIEC().at(T).to(Lp).label("R$_1$", loc="top")
d += elm.ResistorIEC().at(T).to(Rp).label("R$_2$", loc="top")
d += elm.ResistorIEC().at(Lp).to(B).label("R$_3$", loc="bot")
d += elm.ResistorIEC().at(Rp).to(B).label("R$_4$", loc="bot")
d += elm.ResistorIEC().at(Lp).to(Rp).label("R$_5$", loc="top")
d += elm.Dot().at(Lp).label("C", loc="left", color=COPPER); d += elm.Dot().at(Rp).label("D", loc="right", color=COPPER)
d += elm.Dot().at(B)
d += elm.Line().at(B).to((0, 0))
save_drawing(d, "ch07_bridge")
