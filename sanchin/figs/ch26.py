from common import *


def pair(ax, x, dpose, apose, gap=36, sc=0.8):
    fa = Figure(ax, apose, ox=x + gap / 2, th=90, sc=sc, zorder=1)
    fd = Figure(ax, dpose, ox=x - gap / 2, th=-90, sc=sc, zorder=2)
    return fd, fa


def scene(name, steps, captions, h=2.3):
    n = len(steps)
    fig, ax = canvas(W, h, xlim=(0, 80 * n), ylim=(-14, 104))
    floor(ax, 2, 80 * n - 2)
    for i, (d, a, extra) in enumerate(steps):
        x = 40 + i * 80
        fd, fa = pair(ax, x, d, a)
        numdot(ax, x - 34, 98, i + 1, r=4, fs=6.4)
        if extra:
            extra(ax, fd, fa)
        sub_label(ax, x, -3, captions[i], fs=6.0)
    save(fig, name)


att_punch = Pose("uke", "tsuki", "sanchin", "R")
scene("fig26_1",
      [(Pose("uke", "uke", "sanchin", "R"), att_punch, lambda ax, d, a: arrow(ax, *d.joint("lhd"), d.joint("lhd")[0] + 2, d.joint("lhd")[1] + 6, lw=0.9, ms=5)),
       (Pose("hikite_open", "uke", "sanchin", "R"), Pose("uke", "tsuki", "sanchin", "R", lean=4), None),
       (Pose("hikite", "tsuki", "sanchin", "R"), Pose("uke", "tsuki", "sanchin", "R", lean=6), None)],
      ["block deflects", "grab and pull", "punch as attacker\nis drawn in"])

scene("fig26_2",
      [(Pose("circle_a", "circle_b", "sanchin", "R"), Pose("uke", "nukite", "sanchin", "R"), None),
       (Pose("palm_chest", "palm_chest", "sanchin", "R"), Pose("uke", "tsuki_mid", "sanchin", "R"), None),
       (Pose("tora_down", "tora_up", "sanchin", "R"), Pose("uke", "side", "sanchin", "L", lean=-5), None)],
      ["circles meet the arm", "trap and draw in", "tiger's-mouth push"])

# Figure 26.3 kakie
fig, ax = canvas(W * 0.7, 2.4, xlim=(0, 100), ylim=(-8, 104))
floor(ax, 2, 98)
k = Pose("side", "uke", "sanchin", "R")
for s in ("r",):
    k.j[s + "el"] = v(-10, 12, 66); k.j[s + "wr"] = v(-4, 24, 74); k.j[s + "hd"] = v(-3, 27, 76)
k.j["lel"] = v(13, -2, 64); k.j["lwr"] = v(12, 6, 58); k.j["lhd"] = v(11, 9, 58); k.j["lht"] = "fist"
Figure(ax, k, ox=68, th=90, zorder=1)
Figure(ax, k, ox=32, th=-90, zorder=2)
ax.add_patch(Circle((50, 76 * 1.0 - 1), 3.5, fc="none", ec=K, lw=0.8, ls=(0, (2, 1.5)), zorder=40))
label(ax, 50, 102, "wrists in contact", fs=5.6)
save(fig, "fig26_3")
