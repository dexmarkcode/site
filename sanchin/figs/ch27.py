from common import *

fig, ax = plt.subplots(figsize=(W, 1.9))
t = np.linspace(0, 60, 400)
phys = 0.25 + 0.65 * np.exp(-((t - 14) / 12) ** 2) + 0.1 * np.exp(-t / 50)
ref = 0.1 + 0.85 * (1 - np.exp(-t / 22))
ax.plot(t, phys, color=K, lw=1.8, label="physical intensity")
ax.plot(t, ref, color=K, lw=1.2, ls=(0, (4, 2)), label="refinement and mind")
for x0, x1, s in ((0, 3, "learning"), (3, 12, "developing"), (12, 35, "mature"), (35, 60, "later life")):
    ax.axvline(x1, color=G2, lw=0.5)
    ax.text((x0 + x1) / 2, 1.05, s, ha="center", fontsize=5.6)
ax.set_xlim(0, 60); ax.set_ylim(0, 1.15)
ax.set_xlabel("years of practice (approximate)", fontsize=6)
ax.set_yticks([])
ax.tick_params(labelsize=6)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.legend(fontsize=5.8, frameon=False, loc="lower right")
save(fig, "fig27_1")

fig, ax = canvas(W * 0.6, 2.4, xlim=(0, 80), ylim=(-6, 104))
floor(ax, 10, 70)
Figure(ax, Pose("uke", "uke", "sanchin", "R"), ox=40, th=-30)
save(fig, "fig27_2")
