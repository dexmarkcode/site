from common import *

# Figure 13.1 block measurements
fig, ax = canvas(W, 2.8, xlim=(0, 150), ylim=(-12, 104))
floor(ax, 2, 148)
p = Pose("uke", "uke", "sanchin", "R")
f1 = Figure(ax, p, ox=38, th=0)
f2 = Figure(ax, p, ox=112, th=-90)
# front: fist in line with outer shoulder
for s in ("l",):
    sh = f1.P(p.j["lsh"] + v(1.5, 0, 0)); hd = f1.joint("lhd")
    ax.plot([sh[0], sh[0]], [sh[1] - 4, hd[1] + 8], color=K, lw=0.5, ls=(0, (2, 1.5)), zorder=20)
    callout(ax, hd[0], hd[1], 70, 96, "fist in line with\nouter edge of shoulder", fs=5.6)
    el = f1.joint("lel")
    dim(ax, el[0], el[1] - 6, f1.P(v(9.5, 0, 63))[0], el[1] - 6, "", fs=5)
    callout(ax, el[0] - 2, el[1] - 6, 70, 52, "elbow a fist's\nwidth from body", fs=5.6)
# side: forearm upright, fist at shoulder height
sh = f2.P(p.j["rsh"]); hd = f2.joint("rhd"); el = f2.joint("rel")
ax.plot([sh[0] - 4, hd[0] + 10], [sh[1], sh[1]], color=K, lw=0.5, ls=(0, (2, 1.5)), zorder=20)
label(ax, hd[0] + 11, sh[1], "shoulder\nheight", fs=5.4, ha="left")
ax.plot([el[0], el[0]], [el[1], hd[1] + 6], color=K, lw=0.5, ls=(0, (2, 1.5)), zorder=20)
callout(ax, el[0], el[1], 140, 50, "elbow down,\nin front of\nlower ribs", fs=5.6)
sub_label(ax, 38, -3, "Front", fs=6.6); sub_label(ax, 112, -3, "Side", fs=6.6)
save(fig, "fig13_1")

# Figure 13.2 forming the block
fig, ax = canvas(W, 2.5, xlim=(0, 130), ylim=(-12, 104))
floor(ax, 2, 128)
cross = Pose("cross", "cross", "sanchin", "R")
blk = Pose("uke", "uke", "sanchin", "R")
Figure(ax, cross, ox=35, th=0, ghost=True, zorder=1)
f = Figure(ax, blk, ox=35, th=0, zorder=2)
for s, sg in (("l", 1), ("r", -1)):
    a = f.P(cross.j[s + "hd"]); b = f.joint(s + "hd")
    arrow(ax, a[0], a[1], b[0] - sg * 1, b[1] - 3, rad=sg * 0.4, lw=1.0, ms=6, z=30)
    e = f.joint(s + "el")
    ax.add_patch(Circle(e, 2.2, fc="none", ec=K, lw=0.9, zorder=31))
sub_label(ax, 35, -3, "Double block from the cross", fs=6.2)
pun = Pose("uke", "tsuki", "sanchin", "R")
Figure(ax, pun, ox=98, th=-90, ghost=True, zorder=1)
f = Figure(ax, Pose("uke", "uke", "sanchin", "R"), ox=98, th=-90, zorder=2)
a = f.P(pun.j["rhd"]); b = f.joint("rhd")
arrow(ax, a[0], a[1] + 2, b[0] + 3, b[1] + 2, rad=0.45, lw=1.0, ms=6, z=30)
sub_label(ax, 98, -3, "Single block from the punch", fs=6.2)
save(fig, "fig13_2")

# Figure 13.3 faults
fig, ax = canvas(W, 2.6, xlim=(0, 165), ylim=(-12, 104))
floor(ax, 2, 163)
pf = Pose("uke", "uke", "sanchin", "R")
for s, sg in (("l", 1), ("r", -1)):
    pf.j[s + "el"] = pf.j[s + "el"] + v(sg * 7, -2, 2)
    pf.j[s + "wr"] = pf.j[s + "wr"] + v(-sg * 3, 0, 0)
    pf.j[s + "hd"] = pf.j[s + "hd"] + v(-sg * 3, 0, 0)
ph = Pose("uke", "uke", "sanchin", "R", shrug=4)
for s in ("l", "r"):
    for k in ("wr", "hd"):
        ph.j[s + k] = ph.j[s + k] + v(0, 0, 9)
    ph.j[s + "el"] = ph.j[s + "el"] + v(0, 0, 4)
for i, (pp, cap, ok) in enumerate(((pf, "Elbows flared", False), (ph, "Fists too high", False), (Pose("uke", "uke", "sanchin", "R"), "Correct", True))):
    x = 28 + i * 55
    Figure(ax, pp, ox=x, th=0)
    (tick_mark if ok else cross_mark)(ax, x - 22, 95)
    sub_label(ax, x, -3, cap, fs=6.4)
save(fig, "fig13_3")
