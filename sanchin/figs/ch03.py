from common import *

# Figure 3.1 three readings: three triangles
fig, ax = canvas(W, 1.85, xlim=(0, 150), ylim=(0, 62))
sets = [("Mind, body\nand breath", ("Mind", "Body", "Breath")),
        ("Upper, middle\nand lower body", ("Upper", "Middle", "Lower")),
        ("Hard, soft\nand change", ("Hard", "Soft", "Change"))]
for i, (title, (a, b, c)) in enumerate(sets):
    cx = 25 + i * 50
    pts = [(cx, 50), (cx - 18, 18), (cx + 18, 18)]
    ax.add_patch(Polygon(pts, closed=True, fc=G1 if i == 1 else WH, ec=K, lw=0.9))
    for (x, y), t in zip(pts, (a, b, c)):
        ax.add_patch(Circle((x, y), 6.6, fc=WH, ec=K, lw=0.9, zorder=4))
        ax.text(x, y, t, fontsize=4.7, ha="center", va="center", zorder=5, fontweight="bold")
    ax.text(cx, 30, "SANCHIN", fontsize=4.8, ha="center", va="center", zorder=5)
    ax.text(cx, 6, title, fontsize=6.4, ha="center", va="center", style="italic", family=SERIF)
save(fig, "fig3_1")

# Figure 3.2 closing: force path, good vs leaking
fig, ax = canvas(W, 2.8, xlim=(0, 160), ylim=(-12, 104))
floor(ax, 2, 158)
good = Pose("tsuki", "hikite", "sanchin", "R")
bad = Pose("tsuki", "hikite", "sanchin", "R", hipshift=-6, lean=5, shrug=3.5)
fg = Figure(ax, good, ox=38, th=-90)
fb = Figure(ax, bad, ox=110, th=-90)
# force path on good figure: from rear (left) foot to left fist
path = [fg.P(good.j["lank"]), fg.P(good.j["lkn"]), fg.P(good.j["lhip"] + v(0, -3, 0)),
        fg.P(v(0, -5, 66)), fg.P(good.j["lsh"] + v(0, -4, 0)), fg.P(good.j["lel"]), fg.P(good.j["lhd"])]
xs, ys = zip(*path)
ax.plot(xs, ys, color=K, lw=2.2, zorder=9, alpha=0.9, solid_capstyle="round")
arrow(ax, *path[-2], *(path[-1] + np.array([6, 0])), lw=2.2, ms=10, z=9)
tick_mark(ax, 8, 92)
# leaking path
pb = [fb.P(bad.j["lank"]), fb.P(bad.j["lkn"]), fb.P(bad.j["lhip"] + v(0, -3, 0))]
xs, ys = zip(*pb)
ax.plot(xs, ys, color=K, lw=2.2, zorder=9, solid_capstyle="round")
hip = pb[-1]
for k in range(3):
    arrow(ax, hip[0], hip[1] + 2, hip[0] - 10 - k * 2, hip[1] + 6 + k * 5, lw=0.8, ms=5, ls=(0, (2, 1.5)), z=9)
sh = fb.P(bad.j["lsh"])
for k in range(2):
    arrow(ax, sh[0], sh[1], sh[0] - 8, sh[1] + 6 + k * 5, lw=0.8, ms=5, ls=(0, (2, 1.5)), z=9)
callout(ax, hip[0] - 2, hip[1] + 6, 132, 44, "hollow back:\nforce leaks\nat the waist", fs=5.6)
callout(ax, sh[0] + 1, sh[1] + 1, 140, 98, "raised shoulder:\narm disconnects", fs=5.6)
cross_mark(ax, 88, 92)
sub_label(ax, 38, -4, "Closed: force travels floor to fist", fs=6.6)
sub_label(ax, 112, -4, "Open: force leaks away", fs=6.6)
save(fig, "fig3_2")

# Figure 3.3 tension curve
fig, ax = plt.subplots(figsize=(W, 2.0))
t = np.linspace(0, 3, 600)
wave = 0.38 + 0.52 * np.clip(np.sin(np.pi * (t % 1) / 1.0) ** 3 * ((t % 1) > 0.15) + 0, 0, 1)
wave = 0.35 + 0.55 * (np.clip((t % 1 - 0.25) / 0.6, 0, 1) ** 2) * (t % 1 < 0.85) + 0.55 * (t % 1 >= 0.85) * np.exp(-((t % 1) - 0.85) * 14)
ax.plot(t, np.full_like(t, 0.97), color=K, lw=1.2, ls=(0, (4, 2)), label="rigid: maximum tension throughout")
ax.plot(t, wave, color=K, lw=1.8, label="Goju rhythm: build, peak, ease")
ax.axhline(0.33, color=G2, lw=0.6)
ax.text(3.02, 0.33, "structure stays\nclosed above\nthis line", fontsize=5.4, va="center", ha="left")
for k in range(3):
    ax.axvspan(k, k + 0.25, color=G1, lw=0)
    ax.text(k + 0.125, 0.06, "in", fontsize=5.6, ha="center")
    ax.text(k + 0.6, 0.06, "out", fontsize=5.6, ha="center")
ax.set_ylim(0, 1.08); ax.set_xlim(0, 3)
ax.set_yticks([0, 0.5, 1]); ax.set_yticklabels(["none", "moderate", "maximum"], fontsize=6)
ax.set_xticks([0.5, 1.5, 2.5]); ax.set_xticklabels(["movement 1", "movement 2", "movement 3"], fontsize=6)
ax.set_ylabel("tension", fontsize=6.5)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.legend(fontsize=5.8, loc="upper center", bbox_to_anchor=(0.5, 1.22), ncol=2, frameon=False)
save(fig, "fig3_3")
