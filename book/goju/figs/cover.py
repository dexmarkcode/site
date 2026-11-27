from body import *
from matplotlib import font_manager
fig = plt.figure(figsize=(6, 9))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 600); ax.set_ylim(0, 900); ax.axis("off")
ax.add_patch(plt.Rectangle((0, 0), 600, 900, fc="white", ec="none"))
ax.add_patch(plt.Rectangle((22, 22), 556, 856, fc="none", ec=INK, lw=2.2))
ax.add_patch(plt.Rectangle((30, 30), 540, 840, fc="none", ec=INK, lw=0.6))
jp = font_manager.FontProperties(fname=str(ROOT / "fonts/ipag.ttf"))
ax.text(300, 815, "剛 柔 流", ha="center", va="center", fontsize=40, fontproperties=jp)
ax.text(300, 742, "GOJU-RYU", ha="center", fontsize=44, family="EB Garamond", weight="semibold")
ax.text(300, 690, "KARATE KYOHAN", ha="center", fontsize=34, family="EB Garamond", weight="semibold")
ax.plot([240, 360], [678, 678], color=INK, lw=1.4)
sub = ("Illustrated Textbook With 1200 Line Drawings\nShowing Sanchin Tension, Rooting, Iron Body Methods,\n"
       "and Internal Energy Training Explained Step by Step")
ax.text(300, 622, sub, ha="center", va="center", fontsize=11.5, family="EB Garamond", style="italic", linespacing=1.4)
# three figures
poses = [(pose("sanchin_r", "kamae"), 0), (pose("sanchin_r", lh=(16, -38, -10), rh=(-8, -8, 44), rhand="open", rroll=90), 60),
         (pose("shiko", lh=(16, -38, -10), rh=(-16, -20, 44), props=(("chiishi", "r", (0, 1, 0), 40),)), 30)]
for i, (p, v) in enumerate(poses):
    a2 = fig.add_axes([0.08 + i * 0.29, 0.17, 0.26, 0.44])
    render_panel(a2, dict(pose=p, view=v, marks=[("root", "la", "ra")] if i == 0 else []), xr=78)
ax.text(300, 112, "DR BEVERLY J. STIVERS", ha="center", fontsize=19, family="EB Garamond", weight="semibold")
ax.text(300, 72, "SANCHIN  ·  TENSHO  ·  HOJO UNDŌ  ·  KAKIE", ha="center", fontsize=8.5, family="Source Sans 3")
fig.savefig(FIG / "cover.png", dpi=300, facecolor="white")
