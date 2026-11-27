from common import *

# Figure 25.1 comparison
fig, ax = canvas(W, 2.5, xlim=(0, 140), ylim=(-8, 106))
floor(ax, 2, 138)
p1 = Pose("tsuki", "uke", "sanchin", "R")
f1 = Figure(ax, p1, ox=34, th=-90)
a = f1.joint("lel"); b = f1.joint("lhd")
arrow(ax, a[0] - 6, a[1] + 8, b[0] + 6, b[1] + 8, lw=1.0, ms=6, z=30)
sub_label(ax, 34, -2, "Sanchin: straight, closed, braced", fs=6.2)
p2 = Pose("circle_a", "palm_chest", "sanchin", "R")
f2 = Figure(ax, p2, ox=104, th=-30)
c = f2.joint("lhd")
ax.add_patch(Arc(c, 22, 22, theta1=-40, theta2=230, color=K, lw=0.9, ls=(0, (2, 1.5)), zorder=30))
arrow(ax, c[0] + 8.4, c[1] - 7.1, c[0] + 10, c[1] - 4.5, lw=0.9, ms=6, z=30)
sub_label(ax, 104, -2, "Tensho: circular, open, flowing", fs=6.2)
save(fig, "fig25_1")

# Figure 25.2 structure in other stances
fig, ax = canvas(W, 2.4, xlim=(0, 165), ylim=(-8, 104))
floor(ax, 2, 163)
Figure(ax, Pose("uke", "uke", "sanchin", "R"), ox=28, th=-25)
sub_label(ax, 28, -2, "Sanchin dachi", fs=6.2)
Figure(ax, Pose("uke", "uke", "shiko"), ox=83, th=-15)
sub_label(ax, 83, -2, "Shiko dachi", fs=6.2)
neko = Pose("uke", "tora_down", "sanchin", "R")
neko.j["rank"] = v(-3, 10, 9); neko.j["rkn"] = v(-5, 12, 28)
neko.j["lank"] = v(5, -6, 4); neko.j["lkn"] = v(6, 4, 24)
for k in ("lhip", "rhip"):
    neko.j[k] = neko.j[k] + v(0, -2, -6)
for k in ("lsh", "rsh", "neck", "head", "lel", "rel", "lwr", "rwr", "lhd", "rhd"):
    neko.j[k] = neko.j[k] + v(0, -1, -6)
Figure(ax, neko, ox=138, th=-70)
sub_label(ax, 138, -2, "Neko ashi dachi", fs=6.2)
save(fig, "fig25_2")
