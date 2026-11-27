from common import *
from ch20 import flowchart

flowchart("fig21_1",
          ["Dizzy or red-faced\nafter kata", "End of technique\nsoft or silent", "Neck or jaw ache",
           "Head drops at\nturns", "Kata too short or\nhurried", "Worse in front\nof others"],
          ["21.1 Holding the breath", "21.2 Upper-chest breathing", "21.3 Gasping in-breath", "21.4 Running out",
           "21.5 Out of step", "21.6 Strangled out-breath", "21.7 Theatrical breathing", "21.8 Gaze dropping",
           "21.9 Eyes wandering", "21.10 Grimacing, clenching", "21.11 Rushing", "21.12 Anticipation",
           "21.13 Wandering mind", "21.14 Nerves", "21.15 Trying too hard"],
          {0: [0, 5, 14], 1: [3, 4], 2: [9, 5, 1], 3: [7, 12], 4: [10, 2], 5: [13, 11, 6]}, h=3.1)

# Figure 21.2 breath faults
fig, ax = plt.subplots(figsize=(W, 1.8))
t = np.linspace(0, 3, 900)
ph = t % 1
good = np.where(ph < 0.35, 0.3 + 0.6 * np.sin(ph / 0.35 * np.pi / 2), 0.9 - 0.55 * (ph - 0.35) / 0.65)
held = np.where(ph < 0.3, 0.3 + 0.6 * np.sin(ph / 0.3 * np.pi / 2), np.where(ph < 0.6, 0.9, 0.9 - 0.6 * (ph - 0.6) / 0.4))
run = np.where(ph < 0.35, 0.3 + 0.6 * np.sin(ph / 0.35 * np.pi / 2), np.maximum(0.15, 0.9 - 1.6 * (ph - 0.35)))
ax.plot(t, good, color=K, lw=1.8, label="correct")
ax.plot(t, held, color=K, lw=1.1, ls=(0, (4, 2)), label="breath held")
ax.plot(t, run, color=K, lw=1.1, ls=(0, (1, 1.5)), label="running out")
for k in range(3):
    ax.axvline(k + 1, color=G2, lw=0.6)
    ax.text(k + 0.97, 1.02, "technique\narrives", fontsize=5.0, ha="right", va="bottom")
ax.set_ylim(0, 1.25); ax.set_xlim(0, 3)
ax.set_yticks([]); ax.set_xticks([])
ax.set_ylabel("lung volume", fontsize=6)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.legend(fontsize=5.6, frameon=False, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.25))
save(fig, "fig21_2")

# Figure 21.3 gaze
fig, ax = canvas(W, 2.2, xlim=(0, 165), ylim=(-12, 104))
floor(ax, 2, 163)
cfg = [(Pose("uke", "uke", "sanchin", "R", chin=4, lean=2), -0.6, "Gaze dropping", False),
       (Pose("uke", "uke", "sanchin", "R", chin=-3), 0.35, "Gaze rising", False),
       (Pose("uke", "uke", "sanchin", "R"), 0.0, "Level gaze", True)]
for i, (pp, slope, cap, ok) in enumerate(cfg):
    x = 26 + i * 55
    f = Figure(ax, pp, ox=x, th=-90)
    e = f.P(pp.j["head"]) + np.array([3.4, 0.8])
    arrow(ax, e[0] + 2, e[1], e[0] + 24, e[1] + slope * 22, lw=0.8, ms=5, ls=(0, (2, 1.5)), z=30)
    (tick_mark if ok else cross_mark)(ax, x - 20, 96, r=3.2)
    sub_label(ax, x, -3, cap, fs=6.2)
save(fig, "fig21_3")
