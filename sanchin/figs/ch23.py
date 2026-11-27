from common import *
from matplotlib.patches import FancyBboxPatch


def chi_ishi(ax, x, y, ang=90, L=26, scale=1.0):
    a = math.radians(ang)
    ex, ey = x + L * math.cos(a) * scale, y + L * math.sin(a) * scale
    ax.plot([x, ex], [y, ey], color=K, lw=3.4 * scale, solid_capstyle="round", zorder=5)
    ax.plot([x, ex], [y, ey], color=WH, lw=2.0 * scale, solid_capstyle="round", zorder=5.1)
    ax.add_patch(Polygon(capsule((ex - 3 * math.cos(a) * scale, ey - 3 * math.sin(a) * scale),
                                 (ex + 5 * math.cos(a) * scale, ey + 5 * math.sin(a) * scale), 11 * scale),
                         closed=True, fc=G1, ec=K, lw=0.9, zorder=6))


def jar(ax, x, y, s=1.0, z=6):
    pts = [(-4, 0), (-6.5, 4), (-7, 10), (-5, 15), (-3.2, 16.5), (-4.2, 18.5), (4.2, 18.5), (3.2, 16.5), (5, 15), (7, 10), (6.5, 4), (4, 0)]
    ax.add_patch(Polygon([(x + px * s, y + py * s) for px, py in pts], closed=True, fc=G1, ec=K, lw=0.9, zorder=z))


# Figure 23.1 tools
fig, ax = canvas(W, 1.4, xlim=(0, 200), ylim=(-12, 50))
chi_ishi(ax, 18, 2, 90, 30)
jar(ax, 52, 2, 1.4)
# ishi sashi padlock
ax.add_patch(FancyBboxPatch((80, 2), 22, 18, boxstyle="round,pad=0,rounding_size=3", fc=G1, ec=K, lw=0.9))
ax.add_patch(Arc((91, 20), 14, 18, theta1=0, theta2=180, color=K, lw=2.6))
# makiage kigu
ax.plot([116, 150], [38, 38], color=K, lw=3.2, solid_capstyle="round")
ax.plot([133, 133], [38, 14], color=K, lw=0.7)
ax.add_patch(Rectangle((128, 5), 10, 9, fc=G1, ec=K, lw=0.9))
# jari bako bucket
ax.add_patch(Polygon([(164, 2), (192, 2), (196, 26), (160, 26)], closed=True, fc=WH, ec=K, lw=0.9))
for k in range(30):
    ax.add_patch(Circle((162 + (k * 7.3) % 32, 22 + (k % 3) * 1.4), 1.0, fc=G2, ec="none"))
for x, t in ((18, "chi ishi"), (52, "nigiri game"), (91, "ishi sashi"), (133, "makiage kigu"), (178, "jari bako")):
    ax.text(x, -5, t, ha="center", va="top", fontsize=6, style="italic", family=SERIF)
save(fig, "fig23_1")

# Figure 23.2 chi ishi exercises
fig, ax = canvas(W, 2.4, xlim=(0, 140), ylim=(-8, 106))
floor(ax, 2, 138)
p1 = Pose("nukite", "side_fist", "sanchin", "R")
f1 = Figure(ax, p1, ox=35, th=-90)
hd = f1.joint("lhd")
chi_ishi(ax, hd[0], hd[1], 60, 18, 0.9)
a0 = f1.P(p1.j["lsh"])
ax.add_patch(Arc(a0, 70, 70, theta1=-80, theta2=-5, color=K, lw=0.7, ls=(0, (2, 2))))
sub_label(ax, 35, -2, "Forward raise", fs=6.2)
p2 = Pose("uke", "side_fist", "sanchin", "R")
f2 = Figure(ax, p2, ox=102, th=-90)
hd = f2.joint("lhd")
chi_ishi(ax, hd[0], hd[1], 90, 18, 0.9)
Figure  # noqa
ax.plot([hd[0], hd[0] + 16], [hd[1], hd[1]], color=G2, lw=2.0, ls=(0, (2, 2)), zorder=4)
ax.add_patch(Arc(hd, 30, 30, theta1=5, theta2=85, color=K, lw=0.8))
arrow(ax, hd[0] + 13.5, hd[1] + 6, hd[0] + 14.6, hd[1] + 3.5, lw=0.8, ms=5)
sub_label(ax, 102, -2, "Block lever", fs=6.2)
save(fig, "fig23_2")

# Figure 23.3 nigiri game walk
fig, ax = canvas(W, 2.4, xlim=(0, 170), ylim=(-8, 106))
floor(ax, 2, 168)
for i, (pp, x) in enumerate(((Pose("side_fist", "side_fist", "sanchin", "R"), 35),
                             (Pose("side_fist", "side_fist", "step_mid", "L"), 85),
                             (Pose("side_fist", "side_fist", "sanchin", "L"), 135))):
    f = Figure(ax, pp, ox=x, th=-35)
    for s in ("l", "r"):
        h = f.joint(s + "hd")
        jar(ax, h[0], h[1] - 20, 1.0, z=1 if s == "r" else 9)
for k, t in enumerate(("right sanchin dachi", "crescent step", "left sanchin dachi")):
    sub_label(ax, 35 + k * 50, -2, t, fs=6.0)
arrow(ax, 20, 100, 150, 100, lw=0.7, ms=5)
save(fig, "fig23_3")

# Figure 23.4 makiage and jari bako
fig, ax = canvas(W, 2.4, xlim=(0, 140), ylim=(-8, 106))
floor(ax, 2, 138)
p = Pose("nukite", "nukite", "sanchin", "R")
f = Figure(ax, p, ox=35, th=-90)
h = f.joint("lhd")
ax.plot([h[0] - 1, h[0] - 1], [h[1] - 2, h[1] + 2], color=K, lw=4)
ax.plot([h[0], h[0]], [h[1], 30], color=K, lw=0.7, zorder=20)
ax.add_patch(Rectangle((h[0] - 4, 22), 8, 8, fc=G1, ec=K, lw=0.9, zorder=20))
sub_label(ax, 35, -2, "Makiage kigu", fs=6.2)
# jari bako: standing figure with hand in bucket
bx = 112
ax.add_patch(Polygon([(bx - 12, 0), (bx + 12, 0), (bx + 14, 30), (bx - 14, 30)], closed=True, fc=WH, ec=K, lw=0.9, zorder=6))
for k in range(30):
    ax.add_patch(Circle((bx - 12 + (k * 7.7) % 24, 26 + (k % 4) * 1.0), 1.0, fc=G2, ec="none", zorder=6.1))
icon(ax, dict(head=(-2, 92), neck=(-1, 85), sh=(0, 80), el=(6, 60), hd=(10, 34), hip=(-2, 50), kn=(-1, 27), ft=(-2, 2),
              kn2=(-6, 27), ft2=(-8, 2)), ox=bx - 10, z=3)
sub_label(ax, 108, -2, "Jari bako (rice bucket)", fs=6.2)
save(fig, "fig23_4")
