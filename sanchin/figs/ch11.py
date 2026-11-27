from common import *

p_uke_R = Pose("uke", "uke", "sanchin", "R")
p_uke_L = Pose("uke", "uke", "sanchin", "L")
p_step_L = Pose("uke", "uke", "step_mid", "L")
p_step_R = Pose("uke", "uke", "step_mid", "R")

# Figure 11.1 frames 11-15
strip([dict(pose=p_step_L, ghost=p_uke_R, gdx=-6, th=-35, num=11, title="Step forward", sub="left foot, crescent", breath="IN",
            arrows=lambda ax, f: step_arrow(ax, f, (6, -8, 1), (6, 10, 1), rad=0.4)),
       dict(pose=p_uke_L, th=-35, num=12, title="Set", sub="left sanchin dachi", breath="end IN"),
       dict(pose=Pose("uke", "hikite", "sanchin", "L"), th=-35, num=13, title="Pulling hand", sub="right hikite", breath="IN"),
       dict(pose=Pose("uke", "tsuki", "sanchin", "L"), th=-35, num=14, title="Punch", sub="right chudan tsuki", breath="OUT",
            arrows=lambda ax, f: move_arrow(ax, f, "rhd", dy=8)),
       dict(pose=p_uke_L, ghost=Pose("uke", "tsuki", "sanchin", "L"), th=-35, num=15, title="Return", sub="right arm to block", breath="in/out")],
      "fig11_1", gap=44, sc=0.8)

# Figure 11.2 frames 16-19
strip([dict(pose=p_uke_R, ghost=p_uke_L, gdx=-6, th=-35, num=16, title="Step and set", sub="right foot forward", breath="IN"),
       dict(pose=Pose("hikite", "uke", "sanchin", "R"), th=-35, num=17, title="Pulling hand", sub="left hikite", breath="IN"),
       dict(pose=Pose("tsuki", "uke", "sanchin", "R"), th=-35, num=18, title="Punch", sub="left chudan tsuki", breath="OUT",
            arrows=lambda ax, f: move_arrow(ax, f, "lhd", dy=8)),
       dict(pose=p_uke_R, th=-35, num=19, title="Return", sub="settle before turn", breath="in/out")],
      "fig11_2", gap=46, sc=0.8)

# Figure 11.3 turn from above
fig, ax = canvas(W, 2.4, xlim=(0, 165), ylim=(0, 86))
L, WD = 20.0, 26.0
panels = [(28, "1  Start: right foot forward,\nfacing front"), (83, "2  Left foot slides across\nbehind the right heel"), (138, "3  Pivot 180°: left sanchin\ndachi facing the rear")]
for cx, cap in panels:
    label(ax, cx, 6, cap, fs=5.8)
# panel 1
cx = 28; base = 22
foot_top(ax, (cx + WD / 2, base + L), -25, L, left=False)
foot_top(ax, (cx - WD / 2, base), 6, L, left=True)
arrow(ax, cx, 68, cx, 80, lw=0.9, ms=6); label(ax, cx + 3, 76, "facing", fs=5.2, ha="left")
# panel 2
cx = 83
foot_top(ax, (cx - WD / 2 + 2, base), 6, L, left=True, ls=(0, (2, 2)), fill=G1, toes=False)
foot_top(ax, (cx + WD / 2 - 6, base + L), -25, L, left=False)
foot_top(ax, (cx + WD / 2 + WD - 8, base), 0, L, left=True)
arrow(ax, cx - WD / 2 + 8, base + 2, cx + WD / 2 + WD - 14, base + 2, lw=1.0, ms=6, rad=-0.2)
# panel 3: rotated stance facing down the page
cx = 138
foot_top(ax, (cx - WD / 2 + 4, base + 2 * L + 4), 180 - 6, L, left=False)
foot_top(ax, (cx + WD / 2 - 2, base + L + 4), 180 + 25, L, left=True)
label(ax, cx - 22, 40, "both feet\npivot", fs=5.4)
arrow(ax, cx, 30, cx, 18, lw=0.9, ms=6); label(ax, cx + 3, 24, "facing", fs=5.2, ha="left")
save(fig, "fig11_3")

# Figure 11.4 frames 20-24
cross_R = Pose("cross", "cross", "step_mid", "L")
strip([dict(pose=cross_R, ghost=p_uke_R, th=-35, num=20, title="Slide across", sub="left foot behind", breath="IN"),
       dict(pose=p_uke_L, th=125, num=21, title="Pivot and block", sub="facing the rear", breath="OUT"),
       dict(pose=Pose("uke", "hikite", "sanchin", "L"), th=125, num=22, title="Pulling hand", sub="right hikite", breath="IN"),
       dict(pose=Pose("uke", "tsuki", "sanchin", "L"), th=125, num=23, title="Punch, return", sub="right tsuki", breath="OUT"),
       dict(pose=p_uke_R, ghost=p_uke_L, gdx=6, th=125, num=24, title="Step forward", sub="right foot, facing rear", breath="IN")],
      "fig11_4", gap=44, sc=0.8)
