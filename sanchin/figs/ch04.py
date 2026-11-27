from common import *

L = 24.0           # foot length in diagram units
WD = 1.35 * L      # heel-line separation


def stance(ax, cx, cy, lead="R", front_ang=25, rear_ang=6, length=None, width=None, ls="solid", fill=WH, toes=True, lw=0.9):
    """Top view of sanchin dachi. Figure faces up the page. Returns heel points."""
    length = L if length is None else length
    width = WD if width is None else width
    s = 1 if lead == "R" else -1   # page x side of the lead foot
    front_heel = (cx + s * width / 2, cy + length)
    rear_heel = (cx - s * width / 2, cy)
    # inward = toward centre line: right foot turns anticlockwise (negative angle)
    foot_top(ax, front_heel, -s * front_ang, L, left=(lead == "L"), ls=ls, fill=fill, toes=toes, lw=lw)
    foot_top(ax, rear_heel, s * rear_ang, L, left=(lead == "R"), ls=ls, fill=fill, toes=toes, lw=lw)
    return np.array(front_heel), np.array(rear_heel)


# Figure 4.1 measured stance
fig, ax = canvas(W, 3.0, xlim=(0, 140), ylim=(0, 94))
cx, cy = 62, 14
fh, rh = stance(ax, cx, cy, "R")
plumb(ax, fh[0], 4, 88); plumb(ax, rh[0], 4, 88)
ax.plot([rh[0] - 8, fh[0] + 16], [cy + L * 0.97, cy + L * 0.97], color=K, lw=0.5, ls=(0, (1, 1.5)))
label(ax, fh[0] + 17, cy + L * 0.97, "rear toe line = front heel line", fs=5.6, ha="left")
dim(ax, rh[0], 6, fh[0], 6, "about shoulder width", off=0, fs=5.6)
dim(ax, 12, cy, 12, cy + L, "about one\nfoot length", fs=5.4)
ax.plot([12, rh[0] - 3], [cy, cy], color=K, lw=0.4, ls=(0, (2, 2)))
ax.plot([12, fh[0] - 6], [cy + L, cy + L], color=K, lw=0.4, ls=(0, (2, 2)))
# angle arcs
for heel, ang, txt, side in ((fh, -25, "front foot\n20–30° in", 1), (rh, 6, "rear foot\n0–15° in", -1)):
    ax.add_patch(Arc(heel, 2 * L * 0.8, 2 * L * 0.8, theta1=90 + (0 if ang < 0 else -ang), theta2=90 + (-ang if ang < 0 else 0), color=K, lw=0.7))
    a = math.radians(ang)
    ax.plot([heel[0], heel[0] + math.sin(a) * L * 1.1], [heel[1], heel[1] + math.cos(a) * L * 1.1], color=K, lw=0.6)
tx, ty = fh[0] + 14, fh[1] + L * 0.85
label(ax, tx, ty, "front foot\n20–30° in", fs=5.6, ha="left")
label(ax, rh[0] + 12, rh[1] + 8, "rear foot\nstraight or\nup to 15° in", fs=5.6, ha="left")
arrow(ax, 128, 50, 128, 72, lw=0.9)
label(ax, 128, 76, "facing", fs=5.6)
save(fig, "fig4_1")

# Figure 4.2 foot tripod
fig, ax = canvas(W, 2.5, xlim=(0, 140), ylim=(0, 78))
heel = (40, 6)
pts = foot_top(ax, heel, 0, 62, left=False, lw=1.1)
# shaded wrong zones: inner arch and outer edge
from matplotlib.patches import Ellipse as E
ax.add_patch(E((34, 33), 8, 16, fc=G1, ec="none", zorder=2.5))
ax.add_patch(E((51, 30), 6, 18, fc=G1, ec="none", zorder=2.5))
for (x, y, t, tx, ty) in ((40.5, 11, "heel", 80, 10), (33, 49, "ball of\nbig toe", 6, 56), (52, 46, "ball of\nlittle toe", 80, 38)):
    ax.add_patch(Circle((x, y), 3.3, fc=K, ec=K, zorder=6))
    callout(ax, x, y, tx, ty, t, fs=6)
arrow(ax, 24, 24, 31, 30, lw=0.9, ms=6)
label(ax, 22, 21, "arch lifts", fs=5.6, ha="right")
callout(ax, 36, 63, 80, 62, "toes long, pads press\ndown, no curling", fs=6)
callout(ax, 52, 31, 80, 24, "shaded: weight should\nnot collect here", fs=5.6)
label(ax, 108, 72, "Right foot, seen from above", fs=6, style="italic", family=SERIF)
save(fig, "fig4_2")

# Figure 4.3 four steps
fig, ax = canvas(W, 1.7, xlim=(0, 260), ylim=(-12, 85))
for i, x in enumerate((32, 97, 162, 227)):
    numdot(ax, x - 26, 76, i + 1, r=4.5, fs=7)
    if i == 0:
        foot_top(ax, (x + WD / 2, 12), 0, L, left=False); foot_top(ax, (x - WD / 2, 12), 0, L, left=True)
    elif i == 1:
        foot_top(ax, (x + WD / 2, 12), 0, L, left=False, ls=(0, (2, 2)), fill=G1, toes=False)
        foot_top(ax, (x + WD / 2, 12 + L), 0, L, left=False); foot_top(ax, (x - WD / 2, 12), 0, L, left=True)
        arrow(ax, x + WD / 2 + 14, 22, x + WD / 2 + 14, 22 + L, lw=0.8, ms=5)
    elif i == 2:
        foot_top(ax, (x + WD / 2, 12 + L), 0, L, left=False, ls=(0, (2, 2)), fill=G1, toes=False)
        foot_top(ax, (x + WD / 2, 12 + L), -25, L, left=False); foot_top(ax, (x - WD / 2, 12), 6, L, left=True)
        ax.add_patch(Arc((x + WD / 2, 12 + L), 30, 30, theta1=90, theta2=115, color=K, lw=0.8))
    else:
        stance(ax, x, 12, "R")

labels = ["parallel", "slide forward", "turn front toes in", "bend, grip, set"]
for i, x in enumerate((32, 97, 162, 227)):
    sub_label(ax, x, -2, labels[i], fs=6.4)
save(fig, "fig4_3")

# Figure 4.4 crescent step
fig, ax = canvas(W, 2.8, xlim=(0, 140), ylim=(-6, 98))
cx = 70
# start: right sanchin, right foot forward at y = 30+L ... moving left foot
fh = (cx + WD / 2, 30)
foot_top(ax, fh, -25, L, left=False)                       # standing right foot
foot_top(ax, (cx - WD / 2, 30 - L), 6, L, left=True, ls=(0, (2, 2)), fill=G1, toes=False)   # start of left
foot_top(ax, (cx - 6, 30 + 2), 0, L, left=True, ls=(0, (2, 2)), fill=WH, toes=False)          # passing
foot_top(ax, (cx - WD / 2, 30 + L), 25, L, left=True)       # arrival
# crescent path for left heel
t = np.linspace(0, 1, 60)
px = (cx - WD / 2) + (WD / 2 - 6) * np.sin(np.pi * t) * 1.0
py = (30 - L + 8) + (2 * L) * t
ax.plot(px, py, color=K, lw=1.1, zorder=7)
arrow(ax, px[-6], py[-6], px[-1], py[-1], lw=1.1, ms=7, z=7)
label(ax, cx - WD / 2 - 6, 30 - L + 4, "start", fs=5.8, ha="right")
label(ax, cx - 26, 46, "pass close to\nstanding foot", fs=5.8, ha="right")
label(ax, cx - WD / 2 - 6, 30 + L + 14, "arrive and\nturn in", fs=5.8, ha="right")
label(ax, fh[0] + 16, 40, "standing\nfoot grips", fs=5.8, ha="left")
arrow(ax, 128, 40, 128, 62, lw=0.9); label(ax, 128, 66, "facing", fs=5.6)
save(fig, "fig4_4")
