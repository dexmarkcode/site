from figlib import *
from matplotlib.patches import FancyBboxPatch
fig = plt.figure(figsize=(4.5, 3.4))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 4.5); ax.set_ylim(0, 3.4); ax.axis("off")
rungs = [("1", "Positional games", "push, touch the shoulder, own the outside, clinch, wall"),
         ("2", "Touch games", "touch kakie, touch knees, trap and touch"),
         ("3", "Light contact, limited tools", "hands only; hands and knees; trap-to-strike"),
         ("4", "Throws and takedowns", "on mats: throwing, sweeping, strike-to-throw"),
         ("5", "Integrated close-range sparring", "light to medium contact, full protection"),
         ("6", "Scenario training", "approach, grab, wall, two people, confined space")]
ax.plot([0.35, 0.35], [0.2, 3.25], color="black", lw=2.2); ax.plot([1.0, 1.0], [0.2, 3.25], color="black", lw=2.2)
for i, (n, t, d) in enumerate(rungs):
    y = 0.42 + i * 0.5
    ax.plot([0.35, 1.0], [y, y], color="black", lw=2.2)
    ax.add_patch(Circle((0.675, y + 0.16), 0.12, fc="black" if i >= 4 else "white", ec="black", lw=1))
    ax.text(0.675, y + 0.16, n, ha="center", va="center", fontsize=7, fontweight="bold", color="white" if i >= 4 else "black")
    ax.text(1.15, y + 0.12, t, fontsize=7.6, fontweight="bold", va="bottom")
    ax.text(1.15, y + 0.08, d, fontsize=6.2, va="top", style="italic")
arrow(ax, (4.3, 0.4), (4.3, 3.2), lw=1.4)
ax.text(4.18, 1.8, "more freedom and intensity", rotation=90, ha="center", va="center", fontsize=6.5)
save(fig, "fig17_1")
