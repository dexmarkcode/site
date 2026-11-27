from common import *

# Figure 24.1 overview
fig, ax = canvas(W, 1.7, xlim=(0, 160), ylim=(0, 56))
for wk in range(12):
    x = 8 + wk * 12
    light = wk in (3, 7, 11)
    ax.add_patch(Rectangle((x, 14), 12, 14, fc=WH if light else G1, ec=K, lw=0.7))
    ax.text(x + 6, 21, str(wk + 1), ha="center", va="center", fontsize=6)
for i, (t, sub) in enumerate((("PHASE 1  FOUNDATION", "learn, light loads"), ("PHASE 2  BUILD", "more load, Stage 3"),
                              ("PHASE 3  CONSOLIDATE", "specific, testing"))):
    x = 8 + i * 48
    ax.plot([x + 1, x + 47], [32, 32], color=K, lw=0.8)
    ax.text(x + 24, 39, t, ha="center", fontsize=5.8, fontweight="bold")
    ax.text(x + 24, 34.5, sub, ha="center", fontsize=5.2, style="italic", family=SERIF)
for wk, t in ((0, "assess"), (6, "reassess"), (12, "reassess")):
    x = 8 + wk * 12
    ax.plot([x, x], [10, 30], color=K, lw=1.4)
    ax.text(x, 6, t, ha="center", fontsize=5.4, fontweight="bold")
ax.add_patch(Rectangle((8, 46), 6, 5, fc=WH, ec=K, lw=0.7)); ax.text(16, 48.5, "lighter week", fontsize=5.4, va="center")
ax.add_patch(Rectangle((56, 46), 6, 5, fc=G1, ec=K, lw=0.7)); ax.text(64, 48.5, "normal week", fontsize=5.4, va="center")
save(fig, "fig24_1")

# Figure 24.2 weekly calendar
fig, ax = canvas(W, 1.3, xlim=(0, 154), ylim=(0, 42))
days = [("MON", "A", "strength +\nSanchin"), ("TUE", "B / dojo", "skill +\nmobility"), ("WED", "A", "strength +\nSanchin"),
        ("THU", "B / dojo", "skill +\nmobility"), ("FRI", "A", "strength +\nSanchin"), ("SAT", "B", "skill +\ntesting"),
        ("SUN", "REST", "walk,\nstretch")]
for i, (d, s, t) in enumerate(days):
    x = 2 + i * 21.5
    fc = G1 if s == "A" else WH
    ax.add_patch(Rectangle((x, 2), 20, 36, fc=fc, ec=K, lw=0.8))
    ax.text(x + 10, 33, d, ha="center", fontsize=5.8, fontweight="bold")
    ax.text(x + 10, 23, s, ha="center", fontsize=7.2, fontweight="bold")
    ax.text(x + 10, 10, t, ha="center", va="center", fontsize=5.0, linespacing=1.05)
save(fig, "fig24_2")

# Figure 24.3 mobility icons
fig, ax = canvas(W, 1.5, xlim=(0, 340), ylim=(-14, 84))
ax.plot([2, 328], [0, 0], color=K, lw=0.6)
# 1 kneeling hip flexor: front foot flat, rear knee down
icon(ax, dict(head=(2, 68), neck=(2, 61), sh=(2, 57), el=(4, 42), hd=(10, 34), hip=(2, 28), kn=(-22, 3), ft=(-40, 2),
              kn2=(22, 28), ft2=(24, 2)), ox=40)
# 2 ankle rock: half-kneeling with knee forward over toes
icon(ax, dict(head=(-2, 66), neck=(-2, 59), sh=(-2, 55), el=(8, 44), hd=(18, 36), hip=(-4, 26), kn=(-24, 3), ft=(-40, 2),
              kn2=(24, 26), ft2=(16, 2)), ox=110)
arrow(ax, 136, 30, 144, 30, lw=0.8, ms=5, both=True)
# 3 hip rotation lying on back (side view): knees bent up
icon(ax, dict(head=(-36, 6), neck=(-30, 6.5), sh=(-24, 7), el=(-14, 3), hd=(-4, 3), hip=(4, 8), kn=(18, 26), ft=(26, 3)), ox=196)
ax.add_patch(Arc((214, 26), 12, 8, theta1=200, theta2=340, color=K, lw=0.7))
# 4 thoracic opener lying on side: arm arc
icon(ax, dict(head=(-26, 8), neck=(-20, 7), sh=(-14, 7), el=(-12, 20), hd=(-10, 32), hip=(6, 7), kn=(18, 16), ft=(28, 4)), ox=258)
ax.add_patch(Arc((244, 14), 34, 34, theta1=20, theta2=160, color=K, lw=0.7, ls=(0, (2, 2))))
# 5 doorway
ax.plot([300, 300], [0, 80], color=K, lw=1.6)
icon(ax, dict(head=(4, 92 * 0.8), neck=(4, 66), sh=(4, 62), el=(-8, 62), hd=(-6, 74), hip=(2, 38), kn=(4, 20), ft=(2, 2),
              kn2=(-6, 22), ft2=(-14, 2)), ox=310)
for x, t in ((40, "1 Hip flexor"), (110, "2 Ankle rocks"), (196, "3 Hip rotation"), (252, "4 Thoracic opener"), (310, "5 Doorway")):
    ax.text(x, -5, t, ha="center", va="top", fontsize=5.6)
save(fig, "fig24_3")
