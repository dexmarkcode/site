import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
import numpy as np
from matplotlib.patches import Circle

# 5.1 KCL at a node
fig, ax = plt.subplots(figsize=(3.6, 3.0))
ax.add_patch(Circle((0, 0), 0.1, color=NAVY))
spec = [(150, "I₁ = 3 A", 1), (210, "I₂ = 5 A", 1), (40, "I₃ = 2 A", -1), (-40, "I₄ = ?", -1)]
for ang, lab, inward in spec:
    a = np.radians(ang)
    x, y = 1.6 * np.cos(a), 1.6 * np.sin(a)
    ax.plot([0, x], [0, y], color=NAVY, lw=1.6)
    mx, my = 0.8 * np.cos(a), 0.8 * np.sin(a)
    dx, dy = 0.25 * np.cos(a), 0.25 * np.sin(a)
    if inward > 0:
        ax.annotate("", xy=(mx - dx, my - dy), xytext=(mx + dx, my + dy), arrowprops=dict(arrowstyle="-|>", color=COPPER, lw=2))
    else:
        ax.annotate("", xy=(mx + dx, my + dy), xytext=(mx - dx, my - dy), arrowprops=dict(arrowstyle="-|>", color=COPPER, lw=2))
    ax.text(1.95 * np.cos(a), 1.95 * np.sin(a), lab, ha="center", va="center", fontsize=11, color=NAVY)
ax.set_xlim(-2.6, 2.6); ax.set_ylim(-1.8, 1.8); ax.set_aspect("equal"); ax.axis("off")
save_fig(fig, "ch05_kcl_node")

# 5.2 Single loop with KVL polarities
d = drawing()
d += (s := elm.SourceV().up().label("24 V", loc="top"))
d += elm.Line().right(0.5)
d += elm.ResistorIEC().right().label("R$_1$", loc="top").label(("+", "V$_1$ = 8 V", "−"), loc="bot", fontsize=10.5)
d += elm.Line().right(0.5)
d += elm.ResistorIEC().down().label("R$_2$", loc="top").label(("+", "V$_2$", "−"), loc="bot", fontsize=10.5)
d += elm.Line().left(0.5)
d += elm.ResistorIEC().left().label("R$_3$", loc="bot").label(("+", "V$_3$ = 10 V", "−"), loc="top", fontsize=10.5)
d += elm.Line().left().tox(s.start)
d += elm.LoopArrow(direction="cw").at((2.4, 1.5)) if hasattr(elm, "LoopArrow") else elm.Label()
save_drawing(d, "ch05_kvl_loop")

# 5.3 Potential "staircase" round the loop
fig, ax = plt.subplots(figsize=(5.8, 2.6))
xs = [0, 1, 2, 3, 4, 5]
pot = [0, 24, 16, 10, 0]
labels = ["start\n(−) of source", "after source", "after R₁", "after R₂", "after R₃\n(back to start)"]
ax.step(range(5), pot, where="post", color=NAVY, lw=0)
for i in range(5):
    ax.plot([i - 0.3, i + 0.3], [pot[i], pot[i]], color=NAVY, lw=3)
    ax.text(i, pot[i] + 1.3, f"{pot[i]} V", ha="center", fontsize=10, color=NAVY)
for i in range(4):
    col = TEAL if pot[i + 1] > pot[i] else COPPER
    ax.annotate("", xy=(i + 0.7, pot[i + 1]), xytext=(i + 0.3, pot[i]), arrowprops=dict(arrowstyle="-|>", color=col, lw=1.6))
ax.set_xticks(range(5)); ax.set_xticklabels(labels, fontsize=8.5)
ax.set_ylabel("potential (V)"); ax.set_ylim(-3, 29)
ax.text(0.42, 12, "rise\n+24 V", color=TEAL, fontsize=9, ha="right")
for i, t in [(1, "drop 8 V"), (2, "drop 6 V"), (3, "drop 10 V")]:
    ax.text(i + 0.55, (pot[i] + pot[i + 1]) / 2 + 1.2, t, color=COPPER, fontsize=9, ha="left")
ax.grid(alpha=0.2, axis="y")
save_fig(fig, "ch05_staircase")

# 5.4 Two opposing sources in one loop
d = drawing()
d += (s1 := elm.SourceV().up().label("E$_1$ = 12 V", loc="top"))
d += elm.Line().right(0.5)
d += elm.ResistorIEC().right().label("R$_1$ = 2 Ω", loc="top")
d += elm.Line().right(0.5)
d += (s2 := elm.SourceV().down().reverse().label("E$_2$ = 4 V", loc="bot"))
d += elm.Line().left(0.5)
d += (r2 := elm.ResistorIEC().left().label("R$_2$ = 6 Ω", loc="bot"))
d += elm.Line().left().tox(s1.start)
d += elm.LoopCurrent([s1, elm.Line(), s2, r2], direction="cw").label("I") if False else elm.Label()
save_drawing(d, "ch05_two_sources")

# 5.5 Single node pair: current sources and resistors in parallel
d = drawing()
d += (i1 := elm.SourceI().up().label("6 A", loc="top"))
d += elm.Line().right(2)
d += (t1 := elm.Dot())
d += elm.ResistorIEC().down().label("R$_1$ = 4 Ω", loc="bot")
d += (b1 := elm.Dot())
d += elm.Line().right(2.2).at(t1.center)
d += (t2 := elm.Dot())
d += elm.ResistorIEC().down().label("R$_2$ = 12 Ω", loc="bot")
d += (b2 := elm.Dot())
d += elm.Line().right(2.2).at(t2.center)
d += elm.SourceI().down().label("2 A", loc="bot")
d += elm.Line().left().tox(b2.center)
d += elm.Line().left().tox(b1.center)
d += elm.Line().left().tox(i1.start)
d += elm.Label().at((1.0, 3.45)).label("+   V", fontsize=11)
save_drawing(d, "ch05_node_pair")

# 5.6 Branch-current example: two sources, three resistors
d = drawing()
d += (e1 := elm.SourceV().up().label("E$_1$ = 10 V", loc="top"))
d += elm.Line().right(0.5)
d += elm.ResistorIEC().right().label("R$_1$ = 2 Ω", loc="top")
d += elm.CurrentLabelInline(direction="in").at((2.1, 3)).label("I$_1$", loc="top") if False else elm.Label()
d += (top := elm.Dot().label("A", loc="top", color=COPPER, fontsize=13))
d += elm.ResistorIEC().right().label("R$_2$ = 1 Ω", loc="top")
d += elm.Line().right(0.5)
d += (e2 := elm.SourceV().down().reverse().label("E$_2$ = 5 V", loc="bot"))
d += elm.Line().left().tox(top.center)
d += (bot := elm.Dot().label("B", loc="bot", color=COPPER, fontsize=13))
d += elm.Line().left().tox(e1.start)
d += (r3 := elm.ResistorIEC().down().at(top.center).toy(bot.center).label("R$_3$ = 4 Ω", loc="bot"))
d += elm.Arrow().right(0.9).at((1.1, 2.55)).color(COPPER).label("I$_1$", loc="bot", color=COPPER)
d += elm.Arrow().left(0.9).at((6.0, 2.55)).color(COPPER).label("I$_2$", loc="bot", color=COPPER)
d += elm.Arrow().down(0.9).at((3.0, 2.0)).color(COPPER).label("I$_3$", loc="top", color=COPPER)
save_drawing(d, "ch05_branch")
