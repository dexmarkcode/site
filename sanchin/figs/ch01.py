from common import *
from matplotlib.patches import FancyBboxPatch


def rbox(ax, x, y, w, h, text, fs=7, fill=WH, lw=0.8, bold=False, tc=K, ls="solid"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.6", fc=fill, ec=K, lw=lw, ls=ls, zorder=3))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc,
            fontweight="bold" if bold else "normal", zorder=4, linespacing=1.15)


# Figure 1.1 three views of the Sanchin posture
fig, ax = canvas(W, 2.75, xlim=(0, 165), ylim=(-12, 103))
p = Pose("uke", "uke", "sanchin", "R")
floor(ax, 2, 163)
f1 = Figure(ax, p, ox=28, th=0)
f2 = Figure(ax, p, ox=82, th=-35)
f3 = Figure(ax, p, ox=132, th=-90)
for x, s in ((28, "Front"), (82, "Three-quarter"), (132, "Side")):
    sub_label(ax, x, -4, s, fs=7.5)
callout(ax, *f3.joint("lhd"), 152, 88, "fist at\nshoulder height", fs=5.8)
callout(ax, *(f3.P(v(0, -6, 56))), 152, 58, "hips tucked", fs=5.8)
callout(ax, *f3.joint("rkn"), 152, 30, "knees drawn\nin and forward", fs=5.8)
callout(ax, *(f1.P(v(0, 0, 4))), 4, 12, "feet grip\nthe floor", fs=5.8)
save(fig, "fig1_1")

# Figure 1.2 kata tree
fig, ax = canvas(W, 3.1, xlim=(0, 150), ylim=(0, 104))
rbox(ax, 30, 3, 62, 13, "SANCHIN\nstance, breath, structure", fs=7.2, fill=G1, lw=1.3, bold=True)
rbox(ax, 102, 4.5, 40, 10, "TENSHO\nthe soft partner", fs=6.4)
line(ax, [92, 102], [9.5, 9.5], lw=0.8)
ax.text(146, 21.5, "HEISHU KATA  develop the body and breath", ha="right", fontsize=5.8, fontweight="bold")
ax.plot([4, 146], [25.5, 25.5], color=K, lw=0.4, ls=(0, (3, 2)))
ax.text(146, 29.0, "KAISHU KATA  build technique on the foundation", ha="right", fontsize=5.8, fontweight="bold")
kata = ["Gekisai Dai Ichi", "Gekisai Dai Ni", "Saifa", "Seiyunchin", "Shisochin", "Sanseiru", "Sepai", "Kururunfa", "Seisan", "Suparinpei"]
cols = [38, 112]
for cx in cols:
    ax.plot([cx, cx], [16 if cx == 38 else 34, 94], color=K, lw=1.0, zorder=1)
ax.plot([61, 61, 112, 112], [16, 34, 34, 36], color=K, lw=1.0, zorder=1)
for i, k in enumerate(kata):
    row = i // 2
    cx = cols[i % 2]
    yy = 36 + row * 12
    rbox(ax, cx - 22, yy, 44, 8.5, k, fs=6.6)
ax.text(75, 102, "Common teaching order, rising from the root (associations vary)", ha="center", va="top", fontsize=6.2, style="italic", family=SERIF)
save(fig, "fig1_2")

# Figure 1.3 Check Cause Correct Confirm loop
fig, ax = canvas(W, 2.6, xlim=(0, 150), ylim=(-2, 85))
cx, cy, R = 75, 41, 27
pts = {"CHECK": (cx, cy + R + 3), "CAUSE": (cx + R * 1.85, cy), "CORRECT": (cx, cy - R - 3), "CONFIRM": (cx - R * 1.85, cy)}
desc = {"CHECK": "What exactly is happening?", "CAUSE": "Why? Look away from\nwhere the fault shows.",
        "CORRECT": "Change one thing,\nwith one drill.", "CONFIRM": "Repeat the check.\nFixed? Make it habit."}
order = ["CHECK", "CAUSE", "CORRECT", "CONFIRM"]
for i, k in enumerate(order):
    x, y = pts[k]
    fill = G1 if k in ("CAUSE", "CONFIRM") else WH
    rbox(ax, x - 21, y - 8.5, 42, 17, f"{i+1}  {k}\n" + desc[k], fs=5.9, fill=fill, lw=1.0)
for a, b, rad in (("CHECK", "CAUSE", -0.3), ("CAUSE", "CORRECT", -0.3), ("CORRECT", "CONFIRM", -0.3), ("CONFIRM", "CHECK", -0.3)):
    (x1, y1), (x2, y2) = pts[a], pts[b]
    sx = 18 if x2 > x1 else -18 if x2 < x1 else 0
    if a == "CHECK":
        p1, p2 = (x1 + 21, y1), (x2, y2 + 8.5)
    elif a == "CAUSE":
        p1, p2 = (x1, y1 - 8.5), (x2 + 21, y2)
    elif a == "CORRECT":
        p1, p2 = (x1 - 21, y1), (x2, y2 - 8.5)
    else:
        p1, p2 = (x1, y1 + 8.5), (x2 - 21, y2)
    arrow(ax, *p1, *p2, rad=rad, lw=1.0)
ax.text(cx, cy, "Shaded steps\nare the ones\nmost often\nskipped", ha="center", va="center", fontsize=5.8, style="italic", family=SERIF)
save(fig, "fig1_3")
