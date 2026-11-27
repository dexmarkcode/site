from common import *
from matplotlib.patches import FancyBboxPatch


def arm_fist(ax, x0, y0, bend=0, ok=True, cap=""):
    """Schematic side view of forearm and fist. bend: wrist angle in degrees (+ up)."""
    ax.add_patch(Polygon([(x0, y0 - 4), (x0 + 34, y0 - 3.6), (x0 + 34, y0 + 3.6), (x0, y0 + 4)], closed=True, fc=WH, ec=K, lw=1.0))
    a = math.radians(bend)
    cx, cy = x0 + 34, y0
    # fist as rotated rounded rectangle
    pts = [(0, -5.2), (11, -5.6), (12.5, -3), (12.5, 3.5), (10.5, 5.6), (0, 5.2)]
    rp = [(cx + px * math.cos(a) - py * math.sin(a), cy + px * math.sin(a) + py * math.cos(a)) for px, py in pts]
    ax.add_patch(Polygon(rp, closed=True, fc=WH, ec=K, lw=1.0, joinstyle="round"))
    # knuckle marks
    for k in (-2.0, 1.5):
        kx, ky = cx + 12.5 * math.cos(a) - k * math.sin(a), cy + 12.5 * math.sin(a) + k * math.cos(a)
        ax.add_patch(Circle((kx, ky), 0.9, fc=K, zorder=5))
    # force line
    ax.plot([x0 - 4, x0 + 52], [y0, y0], color=K, lw=0.6, ls=(0, (3, 2)))
    if not ok:
        ex, ey = cx + 13 * math.cos(a), cy + 13 * math.sin(a)
        arrow(ax, ex, ey, ex + 6 * math.cos(a), ey + 6 * math.sin(a), lw=0.8, ms=5)
    (tick_mark if ok else cross_mark)(ax, x0 + 4, y0 + 14, r=3)
    label(ax, x0 + 24, y0 - 13, cap, fs=5.8, style="italic", family=SERIF)


fig, ax = canvas(W, 1.2, xlim=(0, 165), ylim=(0, 42))
arm_fist(ax, 4, 22, 0, True, "aligned")
arm_fist(ax, 60, 22, 22, False, "wrist bent up")
arm_fist(ax, 116, 22, -22, False, "wrist bent down")
save(fig, "fig14_1")

# Figure 14.2 path from above
fig, ax = canvas(W, 2.1, xlim=(0, 140), ylim=(0, 64))
cx = 70
ax.add_patch(Ellipse((cx, 16), 52, 18, fc=G1, ec=K, lw=1.0))
ax.add_patch(Circle((cx, 17), 7, fc=WH, ec=K, lw=1.0))
label(ax, cx, 4, "body from above", fs=5.4)
ax.plot([cx, cx], [26, 62], color=K, lw=0.5, ls=(0, (1.5, 1.5)))
label(ax, cx + 2, 61, "centre line", fs=5.2, ha="left")
start = (cx - 22, 24); end = (cx, 54)
ax.add_patch(Circle(start, 2.6, fc=WH, ec=K, lw=0.9, zorder=5)); label(ax, start[0] - 4, start[1], "fist at hip", fs=5.4, ha="right")
arrow(ax, start[0], start[1] + 3, end[0], end[1], lw=1.6, ms=8)
ax.add_patch(Circle(end, 2.6, fc=K, ec=K, zorder=5))
# faults
t = np.linspace(0, 1, 40)
px = start[0] - 14 * np.sin(np.pi * t) + (end[0] - start[0]) * t
py = start[1] + 3 + (end[1] - start[1] - 3) * t
ax.plot(px, py, color=K, lw=0.8, ls=(0, (3, 2)))
label(ax, start[0] - 16, 40, "swinging out\nand in", fs=5.4, ha="right")
arrow(ax, start[0] + 2, start[1] + 3, cx + 16, 52, lw=0.8, ms=5, ls=(0, (3, 2)))
label(ax, cx + 18, 52, "crossing the\ncentre line", fs=5.4, ha="left")
arrow(ax, 128, 20, 128, 40, lw=0.9); label(ax, 128, 44, "facing", fs=5.4)
save(fig, "fig14_2")

# Figure 14.3 rotation
fig, ax = canvas(W, 1.1, xlim=(0, 165), ylim=(0, 36))
ax.plot([10, 150], [18, 18], color=K, lw=0.6)
arrow(ax, 140, 18, 156, 18, lw=0.8, ms=6)
for i, (frac, ang, t) in enumerate(((0, 0, "start: palm up"), (0.33, 0, "1/3: palm up"), (0.66, 15, "2/3: begins to turn"),
                                    (0.85, 100, ""), (1.0, 180, "arrival: palm down"))):
    x = 14 + frac * 124
    a = math.radians(ang)
    ax.add_patch(Ellipse((x, 18), 10, 10, fc=WH, ec=K, lw=1.0, zorder=3))
    # palm marker: a dot on the palm side
    ax.add_patch(Circle((x + 3.6 * math.sin(a), 18 + 3.6 * math.cos(a)), 1.3, fc=K, zorder=4))
    if t:
        ax.text(x, 6, t, ha="center", fontsize=5.4)
ax.add_patch(Rectangle((14 + 0.66 * 124, 26), 124 * 0.34, 3, fc=G1, ec=K, lw=0.5))
label(ax, 14 + 0.83 * 124, 32.5, "rotation happens here", fs=5.4)
label(ax, 2, 30, "black dot = palm side", fs=5.0, ha="left", style="italic", family=SERIF)
save(fig, "fig14_3")

# Figure 14.4 driven from ground
fig, ax = canvas(W, 2.5, xlim=(0, 130), ylim=(-8, 104))
floor(ax, 2, 128)
p = Pose("tsuki", "uke", "sanchin", "R")
f = Figure(ax, p, ox=45, th=-90)
rear = f.P(p.j["lank"] + v(0, -3, -3))
arrow(ax, rear[0] - 2, rear[1] + 10, rear[0] - 6, rear[1] + 1, lw=1.4, ms=8, z=30)
label(ax, rear[0] - 8, rear[1] + 14, "rear foot\npresses", fs=5.6, ha="right")
pts = [f.P(p.j["lank"]), f.P(p.j["lkn"]), f.P(p.j["lhip"] + v(0, -2, 0)), f.P(v(0, -4, 72)), f.P(p.j["lel"]), f.P(p.j["lhd"])]
xs, ys = zip(*pts)
ax.plot(xs, ys, color=K, lw=2.0, zorder=25, alpha=0.85)
arrow(ax, *pts[-1], pts[-1][0] + 12, pts[-1][1], lw=2.0, ms=10, z=26)
callout(ax, *f.P(v(0, -6, 52)), 92, 40, "hips stay square", fs=5.6)
callout(ax, *f.P(v(0, -6, 72)), 92, 62, "back widens and\ndelivers the arm", fs=5.6)
callout(ax, *f.P(p.j["lsh"] + v(0, 0, 2)), 92, 92, "shoulder stays down", fs=5.6)
save(fig, "fig14_4")
