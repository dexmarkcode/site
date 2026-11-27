from common import *

# Figure 22.1 step pyramid
fig, ax = canvas(W, 2.0, xlim=(0, 150), ylim=(0, 64))
levels = ["MOBILITY  hips, ankles, upper back", "STABILITY  feet, trunk, shoulder blades", "STRENGTH  legs, hips, back, grip",
          "ENDURANCE  the whole kata", "SANCHIN"]
for i, t in enumerate(levels):
    y0 = 3 + i * 11.5
    wdt = 146 - i * 24
    ax.add_patch(Rectangle((75 - wdt / 2, y0), wdt, 11.5, fc=G1 if i % 2 == 0 else WH, ec=K, lw=0.9))
    ax.text(75, y0 + 5.8, t, ha="center", va="center", fontsize=5.8 if i < 4 else 6.4, fontweight="bold" if i == 4 else "normal")
save(fig, "fig22_1")

# Figure 22.2 assessment icons (2D)
fig, ax = canvas(W, 2.4, xlim=(0, 320), ylim=(-14, 110))
ax.plot([2, 318], [0, 0], color=K, lw=0.6)
# A: sanchin stance (use mannequin)
Figure(ax, Pose("uke", "uke", "sanchin", "R"), ox=18, th=-90, sc=0.85)
# B: wall sit
ax.plot([46, 46], [0, 90], color=K, lw=1.4)
icon(ax, dict(head=(8, 74), neck=(8, 66), sh=(8, 62), el=(10, 48), hd=(16, 40), hip=(8, 36), kn=(32, 38), ft=(34, 4)), ox=40)
# C: front plank
icon(ax, dict(head=(76, 20), neck=(70, 18), sh=(66, 16), el=(66, 2), hd=(76, 2), hip=(36, 14), kn=(20, 10), ft=(4, 4)), ox=78)
# D: side plank (seen from front, rotated) - approximate as plank on one arm
icon(ax, dict(head=(70, 40), neck=(64, 36), sh=(60, 32), el=(62, 4), hd=(70, 3), hip=(34, 20), kn=(18, 12), ft=(2, 4),
              el2=(64, 46), hd2=(66, 58)), ox=158)
# E: single-leg balance
icon(ax, dict(head=(0, 93), neck=(0, 86), sh=(0, 81), el=(6, 64), hd=(4, 54), hip=(0, 50), kn=(1, 27), ft=(0, 3),
              kn2=(4, 30), ft2=(2, 10)), ox=246)
# F: glute bridge
# G: dead hang
ax.plot([268, 296], [104, 104], color=K, lw=1.8)
icon(ax, dict(head=(0, 82), neck=(0, 76), sh=(0, 71), el=(-2, 88), hd=(-2, 102), hip=(0, 40), kn=(1, 20), ft=(1, 2)), ox=282, sc=0.95)
# H: bridge drawn second row? keep simple: put bridge under plank area
labels = [(18, "A Stance hold"), (58, "B Wall sit"), (118, "C Front plank"), (196, "D Side plank"),
          (246, "E Balance"), (282, "G Dead hang")]
for x, t in labels:
    ax.text(x, -6, t, ha="center", va="top", fontsize=5.6)
save(fig, "fig22_2")

fig, ax = canvas(W, 1.2, xlim=(0, 200), ylim=(-12, 50))
ax.plot([2, 198], [0, 0], color=K, lw=0.6)
icon(ax, dict(head=(6, 7), neck=(12, 7.5), sh=(18, 8), el=(28, 3.5), hd=(38, 2.5), hip=(50, 24), kn=(72, 32), ft=(78, 3)), ox=8)
icon(ax, dict(head=(70, 20), neck=(64, 18), sh=(60, 16), el=(64, 8), hd=(62, 2), hip=(32, 13), kn=(18, 9), ft=(4, 3)), ox=110)
ax.text(48, -5, "F Glute bridge hold", ha="center", va="top", fontsize=5.6)
ax.text(150, -5, "H Press-up (body straight, elbows close)", ha="center", va="top", fontsize=5.6)
save(fig, "fig22_3")
