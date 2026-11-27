from common import *

uR = Pose("uke", "uke", "sanchin", "R"); uL = Pose("uke", "uke", "sanchin", "L")
TH = 125

# Figure 12.1 frames 25-31 (7 frames)
strip([dict(pose=Pose("hikite", "uke", "sanchin", "R"), th=TH, num=25, title="Pull", sub="left, facing rear", breath="IN"),
       dict(pose=Pose("tsuki", "uke", "sanchin", "R"), th=TH, num=26, title="Punch", sub="left tsuki", breath="OUT"),
       dict(pose=uR, th=TH, num=27, title="Return", sub="settle", breath="in/out"),
       dict(pose=Pose("cross", "cross", "step_mid", "L"), th=TH, num=28, title="Slide", sub="left foot across", breath="IN"),
       dict(pose=uL, th=-35, num=29, title="Pivot, block", sub="facing front", breath="OUT"),
       dict(pose=Pose("uke", "tsuki", "sanchin", "L"), th=-35, num=30, title="Pull, punch", sub="right tsuki", breath="IN/OUT"),
       dict(pose=uL, th=-35, num=31, title="Return", sub="last punch done", breath="in/out")],
      "fig12_1", gap=40, sc=0.78)

# Figure 12.2 frames 32-36
ch = Pose("nukite_chamber", "nukite_chamber", "sanchin", "R")
nk = Pose("nukite", "nukite", "sanchin", "R")
chL = Pose("nukite_chamber", "nukite_chamber", "sanchin", "L")
nkL = Pose("nukite", "nukite", "sanchin", "L")
strip([dict(pose=ch, ghost=uL, gdx=5, th=-40, num=32, title="Step back", sub="hands to hips", breath="IN"),
       dict(pose=nk, th=-40, num=33, title="Spear-hands", sub="morote nukite", breath="OUT",
            arrows=lambda ax, f: move_arrow(ax, f, "lhd", dy=8)),
       dict(pose=ch, ghost=nk, th=-40, num=34, title="Return", sub="hands to hips", breath="IN"),
       dict(pose=chL, ghost=ch, gdx=5, th=-40, num=35, title="Step back", sub="right foot back", breath="IN"),
       dict(pose=nkL, th=-40, num=36, title="Spear-hands", sub="morote nukite", breath="OUT")],
      "fig12_2", gap=44, sc=0.8)

# Figure 12.3 frames 37-42 right circular block
draw = Pose("palm_chest", "palm_chest", "sanchin", "R")
ca = Pose("circle_b", "circle_a", "sanchin", "R")   # right hand up, left down
cb = Pose("circle_a", "circle_b", "sanchin", "R")
tc = Pose("tora_down", "palm_chest", "sanchin", "R")
tg = Pose("tora_down", "tora_up", "sanchin", "R")


def circ(ax, f, cw=True):
    c = f.P(v(0, 20, 68))
    ax.add_patch(Arc(c, 30, 32, theta1=20, theta2=160, color=K, lw=0.8, ls=(0, (2, 1.5)), zorder=30))
    ax.add_patch(Arc(c, 30, 32, theta1=200, theta2=340, color=K, lw=0.8, ls=(0, (2, 1.5)), zorder=30))
    arrow(ax, c[0] + (14 if cw else -14), c[1] + 6, c[0] + (15 if cw else -15), c[1] + 2, lw=0.8, ms=5)
    arrow(ax, c[0] - (14 if cw else -14), c[1] - 6, c[0] - (15 if cw else -15), c[1] - 2, lw=0.8, ms=5)


strip([dict(pose=draw, ghost=nkL, gdx=5, th=-20, num=37, title="Step back", sub="hands draw in", breath="IN"),
       dict(pose=ca, th=-20, num=38, title="Circle", sub="begins", breath="IN", arrows=lambda ax, f: circ(ax, f)),
       dict(pose=cb, th=-20, num=39, title="Circle", sub="continues", breath="IN", arrows=lambda ax, f: circ(ax, f)),
       dict(pose=Pose("tora_down", "tora_up", "sanchin", "R"), th=-20, num=40, title="Draw to chest", sub="tiger's mouth", breath="end IN"),
       dict(pose=tg, th=-70, num=41, title="Push", sub="tora guchi", breath="OUT",
            arrows=lambda ax, f: move_arrow(ax, f, "rhd", dy=8)),
       dict(pose=tg, th=-20, num=42, title="Settle", sub="right hand above", breath="end OUT")],
      "fig12_3", gap=40, sc=0.78)

# Figure 12.4 frames 43-48
draw_L = Pose("palm_chest", "palm_chest", "sanchin", "L")
tgL = Pose("tora_up", "tora_down", "sanchin", "L")
strip([dict(pose=draw_L, ghost=tg, gdx=5, th=-20, num=43, title="Step back", sub="hands draw in", breath="IN"),
       dict(pose=Pose("circle_a", "circle_b", "sanchin", "L"), th=-20, num=44, title="Circle", sub="opposite way", breath="IN",
            arrows=lambda ax, f: circ(ax, f, cw=False)),
       dict(pose=tgL, th=-70, num=45, title="Push", sub="left hand above", breath="OUT"),
       dict(pose=tgL, th=-20, num=46, title="Settle", sub="", breath="end OUT"),
       dict(pose=Pose("yoi", "yoi", "musubi"), th=0, num=47, title="Ready", sub="feet together", breath="IN/OUT"),
       dict(pose=Pose("side", "side", "heisoku", lean=9, shrug=-3, chin=4), th=-90, num=48, title="Bow", sub="zanshin", breath="natural")],
      "fig12_4", gap=40, sc=0.78)
