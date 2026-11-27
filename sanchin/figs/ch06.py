from common import *

# Figure 6.1 stacking and stick test
fig, ax = canvas(W, 2.8, xlim=(0, 140), ylim=(-12, 104))
floor(ax, 2, 138)
p = Pose("uke", "uke", "sanchin", "R")
f = Figure(ax, p, ox=38, th=-90)
x_ear = f.P(p.j["head"])[0]
ax.plot([x_ear - 0.5] * 2, [0, 102], color=K, lw=0.7, ls=(0, (4, 2.5)), zorder=13)
for z, t in ((93, "ear"), (81, "shoulder"), (51, "hip")):
    pt = f.P(v(0, 0.5 if z > 80 else 0, z))
    ax.add_patch(Circle((x_ear - 0.5, pt[1]), 1.5, fc=K, zorder=12))
    label(ax, x_ear - 9, pt[1], t, fs=5.8, ha="right")
sub_label(ax, 38, -3, "Stacked along the plumb line", fs=6.4)
f2 = Figure(ax, p, ox=102, th=-90)
# dowel behind the back
top = f2.P(v(0, -7.5, 101)); bot = f2.P(v(0, -7.8, 44))
ax.plot([top[0], bot[0]], [top[1], bot[1]], color=K, lw=3.2, zorder=14, solid_capstyle="round")
ax.plot([top[0], bot[0]], [top[1], bot[1]], color=WH, lw=1.6, zorder=14.1, solid_capstyle="round")
for z, t in ((93, "back of head"), (74, "between the\nshoulder blades"), (49, "sacrum")):
    pt = f2.P(v(0, -7.6, z))
    ax.add_patch(Circle(pt, 1.6, fc=K, zorder=15))
    callout(ax, pt[0], pt[1], 128, pt[1] + (4 if z > 90 else 0), t, fs=5.6)
gap = f2.P(v(0, -7.6, 60))
label(ax, gap[0] - 4, gap[1], "hand's\nwidth gap", fs=5.2, ha="right")
sub_label(ax, 102, -3, "The stick test", fs=6.4)
save(fig, "fig6_1")

# Figure 6.2 shoulders front
fig, ax = canvas(W, 2.4, xlim=(0, 120), ylim=(-12, 104))
floor(ax, 2, 118)
for i, (sh, ok, cap) in enumerate(((8, False, "Shoulders raised"), (0, True, "Shoulder blades drawn down"))):
    x = 30 + i * 60
    p = Pose("uke", "uke", "sanchin", "R", shrug=sh)
    f = Figure(ax, p, ox=x, th=0)
    hd = f.P(p.j["head"])
    for s in (-1, 1):
        shp = f.P(v(s * 9, 0, p.j["lsh"][2]))
        if ok:
            arrow(ax, shp[0], shp[1] + 4, shp[0], shp[1] - 9, lw=1.3, ms=7, z=12)
        else:
            arrow(ax, shp[0], shp[1] - 4, shp[0], shp[1] + 6, lw=1.0, ms=6, z=12, ls=(0, (2, 1.5)))
    dim(ax, x + 18, f.P(p.j["lsh"])[1], x + 18, hd[1] - 3, "", fs=5)
    (tick_mark if ok else cross_mark)(ax, x - 22, 95)
    sub_label(ax, x, -3, cap, fs=6.4)
save(fig, "fig6_2")

# Figure 6.3 back view arrows
fig, ax = canvas(W * 0.62, 2.5, xlim=(0, 80), ylim=(-6, 104))
floor(ax, 2, 78)
p = Pose("uke", "uke", "sanchin", "R")
f = Figure(ax, p, ox=40, th=180)
for s in (-1, 1):
    a = f.P(v(s * 5, -7, 78)); b = f.P(v(s * 3.5, -7, 66))
    arrow(ax, a[0], a[1], b[0], b[1], lw=1.4, ms=7, z=12)
    c = f.P(v(s * 6, -7, 66)); d = f.P(v(s * 11.5, -7, 60))
    arrow(ax, c[0], c[1], d[0], d[1], lw=1.4, ms=7, z=12)
    t = f.P(v(s * 9, -7, 82.5))
    ax.add_patch(Ellipse(t, 6, 3, fc="none", ec=K, lw=0.6, ls=(0, (1.5, 1)), zorder=12))
label(ax, 40, 101, "tops of shoulders soft (dotted)", fs=5.6)
save(fig, "fig6_3")

# Figure 6.4 head
fig, ax = canvas(W, 2.4, xlim=(0, 120), ylim=(-12, 104))
floor(ax, 2, 118)
for i, (ch, ok, cap) in enumerate(((5, False, "Chin poking forward"), (-1.2, True, "Chin slightly back, neck long"))):
    x = 32 + i * 60
    p = Pose("uke", "uke", "sanchin", "R", chin=ch, lean=1.5 if not ok else 0)
    f = Figure(ax, p, ox=x, th=-90)
    hd = f.P(p.j["head"]); shp = f.P(v(0, 0, p.j["lsh"][2]))
    ax.plot([shp[0]] * 2, [shp[1] - 30, hd[1] + 12], color=K, lw=0.6, ls=(0, (4, 2.5)), zorder=13)
    eye = hd + np.array([4, 0.8])
    arrow(ax, eye[0] + 4, eye[1], eye[0] + 16, eye[1] + (-3 if not ok else 0), lw=0.8, ms=5, ls=(0, (2, 1.5)))
    (tick_mark if ok else cross_mark)(ax, x - 24, 70)
    sub_label(ax, x, -3, cap, fs=6.4)
save(fig, "fig6_4")
