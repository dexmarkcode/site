from common import *

# Figure 8.1 tension scale
fig, ax = canvas(W, 1.25, xlim=(0, 150), ylim=(0, 42))
for i in range(11):
    x = 10 + i * 12
    fill = G1 if i in (3, 4) else (G2 if i in (5, 6, 7, 8) else WH)
    if i < 10:
        ax.add_patch(Rectangle((x, 18), 12, 9, fc=fill, ec=K, lw=0.7))
    ax.text(x, 14, str(i), ha="center", va="top", fontsize=6.4)
ax.text(10, 34, "relaxed", fontsize=5.8, ha="left")
ax.text(130, 34, "maximum", fontsize=5.8, ha="right")
for x0, x1, t in ((46, 70, "baseline\n3–4"), (70, 118, "technique peak 5–8"), (118, 130, "rare")):
    ax.plot([x0 + 0.5, x1 - 0.5], [4, 4], color=K, lw=0.6)
    ax.plot([x0 + 0.5] * 2, [3, 5], color=K, lw=0.6); ax.plot([x1 - 0.5] * 2, [3, 5], color=K, lw=0.6)
    ax.text((x0 + x1) / 2, 1, t, ha="center", va="top", fontsize=5.4, linespacing=1.0)
ax.set_ylim(-8, 42)
save(fig, "fig8_1")

# Figure 8.2 three zones on front figure
fig, ax = canvas(W, 2.9, xlim=(0, 140), ylim=(-6, 104))
floor(ax, 20, 80)
p = Pose("uke", "uke", "sanchin", "R")
f = Figure(ax, p, ox=50, th=0)
peak = [v(-13, 6, 70), v(13, 6, 70), v(-9, 6, 74), v(9, 6, 74), v(0, 7, 62), v(-6, 7, 66), f and v(6, 7, 66)]
base = [v(-8, 4, 38), v(8, 4, 38), v(-9, 4, 16), v(9, 4, 16), v(0, 5, 55), v(-5, 5, 52), v(5, 5, 52)]
soft = [v(0, 6, 93), v(0, 6, 86), v(-7, 2, 82.5), v(7, 2, 82.5)]
for pts, fc in ((peak, K), (base, G2), (soft, WH)):
    for q in pts:
        ax.add_patch(Circle(f.P(q), 2.3, fc=fc, ec=K, lw=0.8, zorder=20))
lx = 96
for i, (fc, t) in enumerate(((K, "PEAK ZONE  5–8 at end of technique\narms, lats, chest, sides, abdomen"),
                             (G2, "BASELINE ZONE  3–4 throughout\nfeet, legs, buttocks, pelvis, back"),
                             (WH, "SOFT ZONE  1–2, never above 4\nface, jaw, throat, neck, tops of\nshoulders"))):
    y = 84 - i * 24
    ax.add_patch(Circle((lx, y), 2.6, fc=fc, ec=K, lw=0.8))
    ax.text(lx + 5, y, t, fontsize=5.6, va="center", ha="left", linespacing=1.15)
save(fig, "fig8_2")

# Figure 8.3 sequence from ground up, side view punch
fig, ax = canvas(W, 2.8, xlim=(0, 152), ylim=(-6, 104))
floor(ax, 2, 110)
p = Pose("tsuki", "hikite", "sanchin", "R")
f = Figure(ax, p, ox=40, th=-90)
pts = [p.j["lank"] + v(0, 0, -2), (p.j["lkn"] + p.j["lhip"]) / 2, p.j["lhip"] + v(0, -2, 1), v(0, 3, 62), v(0, -5, 72),
       p.j["lel"], p.j["lhd"]]
names = ["feet press", "legs brace", "pelvis firms", "trunk firms", "back spreads", "arm extends", "fist closes"]
scr = [f.P(q) for q in pts]
xs, ys = zip(*scr)
ax.plot(xs, ys, color=K, lw=1.0, ls=(0, (2, 1.5)), zorder=19)
for i, (q, n) in enumerate(zip(scr, names)):
    numdot(ax, q[0], q[1], i + 1, r=3.0, fs=6, z=21)
for i, n in enumerate(names):
    y = 8 + i * 13
    numdot(ax, 108, y, i + 1, r=3.0, fs=6, inv=False)
    ax.text(113, y, n, fontsize=6.2, va="center")
arrow(ax, 142, 6, 142, 90, lw=0.8, ms=6)
ax.text(146, 50, "one out-breath", rotation=90, fontsize=5.6, va="center")
save(fig, "fig8_3")
