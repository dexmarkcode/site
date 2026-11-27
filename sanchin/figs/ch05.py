from common import *

# Figure 5.1 knee alignment, front view
fig, ax = canvas(W, 2.75, xlim=(0, 165), ylim=(-14, 103))
floor(ax, 2, 163)
poses = [("sanchin", "Correct: knee over toes", True), ("sanchin_kneesout", "Fault: knees drift out", False),
         ("sanchin_collapse", "Fault: knees collapse in", False)]
for i, (st, cap, ok) in enumerate(poses):
    x = 28 + i * 55
    p = Pose("uke", "uke", st, "R")
    f = Figure(ax, p, ox=x, th=0)
    for s in ("l", "r"):
        hip, kn = f.joint(s + "hip"), f.joint(s + "kn")
        ank = p.j[s + "ank"]; d = unit(p.j[s + "dir"])
        toe = f.P(v(*(ank[:2] + d[:2] * 9), 0))
        ax.plot([hip[0], kn[0], toe[0]], [hip[1], kn[1], toe[1]], color=K, lw=1.0, ls=(0, (2.5, 1.5)), zorder=9)
        ax.add_patch(Circle(kn, 1.6, fc=K, zorder=10))
    (tick_mark if ok else cross_mark)(ax, x - 20, 92)
    sub_label(ax, x, -4, cap, fs=6.4)
save(fig, "fig5_1")

# Figure 5.2 pelvis from the side
fig, ax = canvas(W, 2.75, xlim=(0, 165), ylim=(-14, 103))
floor(ax, 2, 163)
cfg = [(dict(hipshift=-6, lean=5), "Tilted forward:\nhollow back", False, 20),
       (dict(), "Sanchin: slightly tucked,\nlong lower back", True, 0),
       (dict(hipshift=5, lean=-5), "Over-tucked:\nhips forward, leaning back", False, -22)]
for i, (kw, cap, ok, tilt) in enumerate(cfg):
    x = 28 + i * 55
    p = Pose("uke", "uke", "sanchin", "R", **kw)
    f = Figure(ax, p, ox=x, th=-90)
    # pelvis indicator: tilted ellipse at hip
    c = f.P(v(0, p.j["lhip"][1], p.j["lhip"][2] + 2))
    ax.add_patch(Ellipse(c, 15, 6, angle=tilt, fc="none", ec=K, lw=1.3, zorder=12))
    a = math.radians(tilt)
    ax.plot([c[0] - 10 * math.cos(a), c[0] + 10 * math.cos(a)], [c[1] - 10 * math.sin(a), c[1] + 10 * math.sin(a)], color=K, lw=0.6, zorder=12)
    # spine line
    sh = f.P(v(0, p.j["lsh"][1] - 5, p.j["lsh"][2]))
    lb = f.P(v(0, p.j["lhip"][1] - 6 - (3 if tilt > 0 else 0), 62))
    hb = f.P(v(0, p.j["lhip"][1] - 6, p.j["lhip"][2]))
    (tick_mark if ok else cross_mark)(ax, x - 20, 92)
    sub_label(ax, x, -3, cap, fs=6.0)
save(fig, "fig5_2")

# Figure 5.3 partner checks
fig, ax = canvas(W, 2.4, xlim=(0, 200), ylim=(-16, 100))
floor(ax, 2, 198)
names = ["Knee-out test", "Knee-in test", "Hip push", "Back-of-pelvis check"]
for i in range(4):
    x = 25 + i * 50
    p = Pose("uke", "uke", "sanchin", "R")
    th = 0 if i < 3 else 180
    f = Figure(ax, p, ox=x, th=th, sc=0.9)
    if i == 0:
        k = f.joint("rkn"); arrow(ax, k[0] + 4, k[1], k[0] - 9, k[1], lw=1.4, ms=8, z=12)
        k = f.joint("lkn"); arrow(ax, k[0] - 4, k[1], k[0] + 9, k[1], lw=1.4, ms=8, z=12)
    elif i == 1:
        k = f.joint("rkn"); arrow(ax, k[0] - 14, k[1], k[0] - 4, k[1], lw=1.4, ms=8, z=12)
        k = f.joint("lkn"); arrow(ax, k[0] + 14, k[1], k[0] + 4, k[1], lw=1.4, ms=8, z=12)
    elif i == 2:
        h = f.joint("rhip"); arrow(ax, h[0] - 18, h[1] + 4, h[0] - 7, h[1] + 4, lw=1.6, ms=9, z=12)
    else:
        c = f.P(v(0, -6, 57))
        ax.add_patch(Rectangle((c[0] - 6, c[1] - 3), 12, 7, fc=G1, ec=K, lw=0.7, zorder=12))
        arrow(ax, c[0] - 9, c[1] + 1, c[0] - 16, c[1] + 1, lw=0.8, ms=5, z=12)
        arrow(ax, c[0] + 9, c[1] + 1, c[0] + 16, c[1] + 1, lw=0.8, ms=5, z=12)
        label(ax, c[0], c[1] + 9, "back widens", fs=5.2, z=13, bbox=dict(fc=WH, ec="none", pad=0.5))
    sub_label(ax, x, -4, names[i], fs=6.2)
save(fig, "fig5_3")
