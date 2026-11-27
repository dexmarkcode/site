from common import *

p = Pose("uke", "uke", "sanchin", "R")


def mapfig(name, th, points, side_text):
    fig, ax = canvas(W, 3.0, xlim=(0, 140), ylim=(-6, 106))
    floor(ax, 20, 80)
    f = Figure(ax, p, ox=50, th=th)
    for n, pt3, (dx, dy) in points:
        c = f.P(pt3)
        ax.add_patch(Circle(c, 1.3, fc=K, zorder=40))
        tx, ty = c[0] + dx, c[1] + dy
        ax.plot([c[0], tx], [c[1], ty], color=K, lw=0.45, zorder=39)
        numdot(ax, tx, ty, n, r=3.0, fs=5.8, z=41)
    y = 98
    for t in side_text:
        ax.text(96, y, t, fontsize=5.7, va="top", ha="left")
        y -= 7.6
    save(fig, name)


front = [
    (1, v(0, 1, 99.5), (-14, 4)),
    (2, v(-8, 0, 82), (-22, 2)),
    (5, p.j["lhd"] + v(0, 0, 3), (14, 6)),
    (6, p.j["rwr"], (-20, -2)),
    (7, p.j["lel"] + v(0, 0, -2.5), (18, -4)),
    (8, v(0, 30, 71), (14, 0)),
    (10, v(0, 7, 56), (-28, -2)),
    (11, v(9.5, 6, 61), (20, -8)),
    (13, v(-10, 0, 51), (-18, -4)),
    (15, p.j["lkn"] + v(-3, 0, 0), (20, 2)),
    (16, (p.j["rhip"] + p.j["rkn"]) / 2 + v(0, 4, 0), (-20, 0)),
]
mapfig("fig17_1", 0, front, ["1  Crown", "2  Shoulder press", "5  Fist push down", "6  Forearm out / in",
                             "7  Elbow lift", "8  Punch push-back (at", "    end of a punch)", "10  Abdomen (out-breath)",
                             "11  Sides of trunk", "13  Hip push", "15  Knees out / in", "16  Thighs"])
back = [
    (2, v(7, 0, 82), (-22, 4)),
    (3, v(4, -7, 74), (-20, 0)),
    (4, v(10, -5, 70), (22, 2)),
    (9, v(-13, -3, 70), (-18, -6)),
    (12, v(0, -7, 55), (20, -6)),
    (14, v(5, -7, 46), (-22, -6)),
    (16, (p.j["lhip"] + p.j["lkn"]) / 2 + v(0, -4, 0), (20, 0)),
    (17, (p.j["rkn"] + p.j["rank"]) / 2 + v(0, -4, 0), (-20, 0)),
]
mapfig("fig17_2", 180, back, ["2  Shoulder press", "3  Shoulder blades", "4  Latissimus", "9  Upper arms",
                              "12  Lower back (touch only)", "14  Buttocks", "16  Thighs", "17  Calves"])

# Figure 17.3 whole body pushes
fig, ax = canvas(W, 2.5, xlim=(0, 130), ylim=(-8, 104))
floor(ax, 2, 128)
for i, (x, front_) in enumerate(((35, True), (98, False))):
    f = Figure(ax, p, ox=x, th=-90)
    if front_:
        c = f.P(v(0, 6, 76))
        arrow(ax, c[0] + 16, c[1], c[0] + 2, c[1], lw=1.6, ms=9, z=40)
        path = [f.P(v(0, 2, 74)), f.P(p.j["lhip"]), f.P(p.j["lkn"]), f.P(p.j["lank"])]
        cap = "Front push: into the rear leg"
    else:
        c = f.P(v(0, -7, 74))
        arrow(ax, c[0] - 16, c[1], c[0] - 2, c[1], lw=1.6, ms=9, z=40)
        path = [f.P(v(0, -2, 74)), f.P(p.j["rhip"]), f.P(p.j["rkn"]), f.P(p.j["rank"])]
        cap = "Back push: into the front leg"
    xs, ys = zip(*path)
    ax.plot(xs, ys, color=K, lw=1.2, ls=(0, (3, 2)), zorder=39)
    sub_label(ax, x, -2, cap, fs=6.2)
save(fig, "fig17_3")
