from common import *

# Figure 10.1 floor pattern schematic
fig, ax = canvas(W, 3.4, xlim=(0, 150), ylim=(-4, 108))
X = 75
ax.plot([X - 4, X - 4], [8, 82], color=K, lw=1.0); ax.plot([X + 4, X + 4], [8, 82], color=K, lw=1.0)
ax.add_patch(Arc((X, 82), 8, 8, theta1=0, theta2=180, color=K, lw=1.0))
arrow(ax, X - 9, 30, X - 9, 50, lw=0.8, ms=5); arrow(ax, X + 9, 50, X + 9, 30, lw=0.8, ms=5)
ax.text(X, 104, "FRONT", ha="center", fontsize=6, fontweight="bold")
arrow(ax, X, 94, X, 101, lw=0.9, ms=6)
adv = [(8, "1–3", "attention, bow, ready"), (22, "4–10", "step, double block, first cycle"),
       (42, "11–15", "step, cycle"), (62, "16–19", "step, cycle"), (82, "20–23", "turn to rear, cycle")]
ret = [(70, "24–27", "step (facing rear), cycle"), (56, "28–31", "turn to front, cycle"), (44, "32–34", "step back, spear-hands"),
       (32, "35–36", "step back, spear-hands"), (20, "37–42", "step back, right circular block"),
       (8, "43–48", "step back, left circular block; close")]
for y, fr, t in adv:
    ax.add_patch(Circle((X - 4, y), 2.6, fc=WH, ec=K, lw=1.0, zorder=5))
    ax.text(X - 12, y, fr, ha="right", va="center", fontsize=6.4, fontweight="bold")
    ax.text(X - 28, y, t, ha="right", va="center", fontsize=5.8)
for y, fr, t in ret:
    ax.add_patch(Circle((X + 4, y), 2.6, fc=K, ec=K, lw=1.0, zorder=5))
    ax.text(X + 12, y, fr, ha="left", va="center", fontsize=6.4, fontweight="bold")
    ax.text(X + 28, y, t, ha="left", va="center", fontsize=5.8)
ax.text(2, -2, "Both lanes lie on the same line; they are drawn apart for clarity. White: moving forward. Black: after the first turn.", fontsize=5.4, style="italic", family=SERIF)
save(fig, "fig10_1")

# Figure 10.2 frames 1-3
p1 = Pose("side", "side", "musubi")
p2 = Pose("side", "side", "heisoku", lean=9, shrug=-3, chin=4)
p3 = Pose("yoi", "yoi", "musubi")
strip([dict(pose=p1, th=0, num=1, title="Attention", sub="musubi dachi", breath="natural"),
       dict(pose=p2, th=-90, num=2, title="Bow", sub="rei", breath="natural"),
       dict(pose=p3, th=0, num=3, title="Ready", sub="yoi", breath="IN / OUT",
            arrows=lambda ax, f: move_arrow(ax, f, "rhd", dx=4, dz=4, rad=-0.3))],
      "fig10_2", gap=50, sc=0.85)

# Figure 10.3 frames 4-6
p4 = Pose("cross", "cross", "sanchin", "R")
p5 = Pose("uke", "uke", "sanchin", "R")
strip([dict(pose=p4, ghost=p3, th=-30, num=4, title="Step and cross", sub="right foot crescent", breath="IN",
            arrows=lambda ax, f: step_arrow(ax, f, (-3, 0, 1), (-10, 8, 1), rad=-0.4)),
       dict(pose=p5, ghost=p4, th=-30, num=5, title="Double block", sub="morote chudan uke", breath="OUT",
            arrows=lambda ax, f: (move_arrow(ax, f, "lhd", dx=-5, dy=-5, dz=-6, rad=0.3), move_arrow(ax, f, "rhd", dx=5, dy=-5, dz=-6, rad=-0.3))),
       dict(pose=p5, th=-30, num=6, title="Settle", sub="peak, then ease", breath="end OUT")],
      "fig10_3", gap=50, sc=0.85)

# Figure 10.4 frames 7-10
p7 = Pose("hikite", "uke", "sanchin", "R")
p8 = Pose("tsuki", "uke", "sanchin", "R")
strip([dict(pose=p7, ghost=p5, th=-55, num=7, title="Pulling hand", sub="left hikite", breath="IN"),
       dict(pose=p8, th=-55, num=8, title="Punch", sub="left chudan tsuki", breath="OUT",
            arrows=lambda ax, f: move_arrow(ax, f, "lhd", dy=8)),
       dict(pose=p5, ghost=p8, th=-55, num=9, title="Return", sub="left arm to block", breath="in/out"),
       dict(pose=p5, th=-55, num=10, title="Settle", sub="ready to step", breath="end OUT")],
      "fig10_4", gap=46, sc=0.8)
