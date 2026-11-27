from common import *

# Figure 18.1 programme timeline
fig, ax = canvas(W, 1.6, xlim=(0, 160), ylim=(0, 54))
for wk in range(13):
    x = 8 + wk * 12
    ax.plot([x, x], [10, 13], color=K, lw=0.6)
    if wk < 12:
        ax.text(x + 6, 6, str(wk + 1), ha="center", fontsize=5.6)
ax.plot([8, 152], [12, 12], color=K, lw=0.8)
ax.text(2, 6, "week", fontsize=5.4, ha="left", style="italic", family=SERIF)
phases = [(0, 3, "TOUCH\nLevel 1, fixed stance", WH), (3, 6, "PRESSURE\nLevel 2, fixed stance", G1),
          (6, 9, "IN MOTION\nLevel 2 during kata", WH), (9, 12, "CONSOLIDATE\nLevel 2 + light Level 3", G1)]
for a, b, t, fc in phases:
    ax.add_patch(Rectangle((8 + a * 12, 16), (b - a) * 12, 22, fc=fc, ec=K, lw=0.9))
    ax.text(8 + (a + b) * 6, 27, t, ha="center", va="center", fontsize=5.6, linespacing=1.15)
arrow(ax, 8, 44, 152, 44, lw=0.8, ms=6)
ax.text(80, 49, "two sessions a week, about fifteen minutes each", ha="center", fontsize=5.6, style="italic", family=SERIF)
save(fig, "fig18_1")

# Figure 18.2 moving test
uR = Pose("uke", "uke", "sanchin", "R"); uL = Pose("uke", "uke", "sanchin", "L"); st = Pose("uke", "uke", "step_mid", "L")
tester_pose = Pose("nukite", "nukite", "step_mid", "R")
for s in ("l", "r"):
    tester_pose.j[s + "el"] = tester_pose.j[s + "el"] + v(0, -2, 3)
    tester_pose.j[s + "wr"] = v(tester_pose.j[s + "wr"][0] * 1.6, 16, 84)
    tester_pose.j[s + "hd"] = v(tester_pose.j[s + "hd"][0] * 1.6, 23, 84)
fig, ax = canvas(W, 2.2, xlim=(0, 200), ylim=(-6, 106))
floor(ax, 2, 198)
for i, (pp, x) in enumerate(((uR, 50), (st, 105), (uL, 160))):
    Figure(ax, tester_pose, ox=x - 26, th=-90, zorder=1, sc=0.9)
    Figure(ax, pp, ox=x, th=-90, zorder=2, sc=0.9)
    numdot(ax, x - 40, 100, i + 1, r=4, fs=6.4)
ax.plot([20, 190], [96, 96], color=K, lw=0.5, ls=(0, (3, 2)))
label(ax, 192, 96, "head\nlevel", fs=5.4, ha="left")
for k, t in enumerate(("start of step", "feet passing", "landing")):
    sub_label(ax, 37 + k * 55, -1, t, fs=6.0)
save(fig, "fig18_2")

# Figure 18.3 bands
fig, ax = canvas(W, 2.5, xlim=(0, 140), ylim=(-6, 106))
floor(ax, 2, 138)
p = Pose("uke", "uke", "sanchin", "R")
f = Figure(ax, p, ox=35, th=0)
for s in (-1, 1):
    shp = f.P(v(s * 9, 0, 83)); ft = f.P(v(s * 7, 2, 1))
    ax.plot([shp[0], shp[0] + s * 3, ft[0]], [shp[1] + 1, 50, ft[1]], color=K, lw=1.8, zorder=30, solid_capstyle="round")
ax.plot([f.P(v(-9, 0, 83))[0], f.P(v(9, 0, 83))[0]], [f.P(v(0, 0, 84.5))[1]] * 2, color=K, lw=1.8, zorder=30)
label(ax, 35, 102, "band over shoulders", fs=5.8)
sub_label(ax, 35, -1, "Shoulder press with a band", fs=6.2)
p2 = Pose("tsuki", "uke", "sanchin", "R")
f2 = Figure(ax, p2, ox=100, th=-90)
hd = f2.joint("lhd")
anchor = (66, f2.P(v(0, 0, 56))[1])
ax.plot([anchor[0], hd[0]], [anchor[1], hd[1]], color=K, lw=1.8, zorder=1)
ax.add_patch(Rectangle((62, anchor[1] - 6), 4, 12, fc=G2, ec=K, lw=0.8))
label(ax, 64, anchor[1] + 10, "anchor", fs=5.6)
sub_label(ax, 100, -1, "Punch against a band", fs=6.2)
save(fig, "fig18_3")
