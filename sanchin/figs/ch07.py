from common import *
from matplotlib.patches import FancyBboxPatch


def trunk(ax, cx, inhale=True):
    """Schematic side view of the trunk: spine at back (left), front of belly at right."""
    bulge = 6 if inhale else 1.5
    back = [(cx - 14, 92), (cx - 16, 70), (cx - 15, 48), (cx - 14 - (2 if inhale else 0), 30), (cx - 13, 12)]
    front = [(cx + 13, 12), (cx + 15 + bulge, 30), (cx + 17 + bulge * 0.4, 48), (cx + 18, 70), (cx + 12, 92)]
    pts = back + front
    ax.add_patch(Polygon(pts, closed=True, fc=WH, ec=K, lw=1.1, zorder=2))
    # spine
    for y in np.arange(16, 90, 6):
        ax.add_patch(FancyBboxPatch((cx - 13, y), 4, 4.4, boxstyle="round,pad=0,rounding_size=0.8", fc=G1, ec=K, lw=0.5, zorder=3))
    # ribs
    for k in range(4):
        y0 = 84 - k * 7
        ax.add_patch(Arc((cx + 2, y0 - 6), 30, 16 + k, theta1=20, theta2=160, color=G2, lw=0.6, zorder=3))
    # diaphragm dome
    dy = 46 if inhale else 56
    t = np.linspace(0, math.pi, 50)
    ax.plot(cx + 1 + 14 * np.cos(t), dy + (4 if inhale else 9) * np.sin(t), color=K, lw=2.2, zorder=4)
    label(ax, cx + 1, dy + (8 if inhale else 13) + 2.5, "diaphragm", fs=5.4)
    if inhale:
        arrow(ax, cx + 1, dy + 6, cx + 1, dy - 5, lw=1.2, ms=7)
        for (x1, y1, x2, y2) in ((cx + 20, 32, cx + 28, 32), (cx - 17, 32, cx - 24, 32)):
            arrow(ax, x1, y1, x2, y2, lw=1.0, ms=6)
        label(ax, cx + 1, 3, "IN: flattens and descends;\nlower trunk widens", fs=5.8)
    else:
        arrow(ax, cx + 1, dy + 2, cx + 1, dy + 12, lw=1.2, ms=7)
        for (x1, y1, x2, y2) in ((cx + 26, 32, cx + 19, 32), (cx - 23, 32, cx - 17, 32)):
            arrow(ax, x1, y1, x2, y2, lw=1.0, ms=6)
        label(ax, cx + 1, 3, "OUT: rises; trunk firms\naround remaining air", fs=5.8)
    label(ax, cx - 14, 96, "back", fs=5.2); label(ax, cx + 14, 96, "front", fs=5.2)


fig, ax = canvas(W, 2.5, xlim=(0, 140), ylim=(-6, 100))
trunk(ax, 36, True)
trunk(ax, 104, False)
save(fig, "fig7_1")

# Figure 7.2 breath and movement chart
fig, ax = plt.subplots(figsize=(W, 1.9))
t = np.linspace(0, 10, 500)
vol = np.piecewise(t, [t < 3, (t >= 3) & (t < 8), (t >= 8) & (t < 9), t >= 9],
                   [lambda x: 0.3 + 0.6 * np.sin(x / 3 * np.pi / 2),
                    lambda x: 0.9 - 0.5 * (x - 3) / 5,
                    lambda x: 0.4 + 0.2 * (x - 8),
                    lambda x: 0.6 - 0.2 * (x - 9)])
ten = np.piecewise(t, [t < 3, (t >= 3) & (t < 8), t >= 8],
                   [0.32, lambda x: 0.32 + 0.6 * ((x - 3) / 5) ** 2, lambda x: 0.92 * np.exp(-(x - 8) * 1.2) + 0.25])
ax.plot(t, vol, color=K, lw=1.8, label="lung volume")
ax.plot(t, ten, color=K, lw=1.2, ls=(0, (4, 2)), label="tension")
ax.axvspan(0, 3, color=G1, lw=0); ax.axvspan(8, 9, color=G1, lw=0)
for x0, x1, s in ((0, 3, "pull hand\nto hip: IN"), (3, 8, "punch drives out: OUT"), (8, 10, "return\nto block")):
    ax.text((x0 + x1) / 2, 1.03, s, ha="center", va="bottom", fontsize=5.8)
ax.annotate("breath ends as\npunch tightens", xy=(8, 0.41), xytext=(6.1, 0.12), fontsize=5.6,
            arrowprops=dict(arrowstyle="-|>", lw=0.6, color=K))
ax.set_xlim(0, 10); ax.set_ylim(0, 1.25)
ax.set_xticks([]); ax.set_yticks([])
ax.set_xlabel("time (seconds, approximate)", fontsize=6)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.legend(fontsize=5.8, loc="lower right", frameon=False)
save(fig, "fig7_2")

# Figure 7.3 cross-section of waist
fig, ax = canvas(W, 1.9, xlim=(0, 140), ylim=(0, 70))
for i, (cx, even, cap, ok) in enumerate(((36, False, "Front only: belly pushes forward,\nlower back hollows", False),
                                       (104, True, "All the way round:\nfront, sides and back", True))):
    ax.add_patch(Ellipse((cx, 38), 44, 30, fc=G1, ec=K, lw=0.8, ls=(0, (2, 2)), zorder=2))
    if even:
        ax.add_patch(Ellipse((cx, 38), 52, 36, fc="none", ec=K, lw=1.3, zorder=3))
        for a in range(0, 360, 45):
            r = math.radians(a)
            arrow(ax, cx + 20 * math.cos(r), 38 + 13 * math.sin(r), cx + 27 * math.cos(r), 38 + 18 * math.sin(r), lw=0.8, ms=5)
    else:
        pts = [(cx + 22 * math.cos(r) + (9 * max(0, math.sin(r)) ** 2), 38 + 15 * math.sin(r) + 8 * max(0, math.sin(r)) ** 3)
               for r in np.linspace(0, 2 * math.pi, 60)]
        ax.add_patch(Polygon(pts, closed=True, fc="none", ec=K, lw=1.3, zorder=3))
        arrow(ax, cx, 50, cx, 62, lw=1.0, ms=6)
    ax.add_patch(Circle((cx, 26), 3, fc=K, zorder=4))
    label(ax, cx + 5, 26, "spine", fs=5.2, ha="left")
    label(ax, cx, 64 if even else 66, "front", fs=5.2)
    (tick_mark if ok else cross_mark)(ax, cx - 30, 60)
    label(ax, cx, 5, cap, fs=5.8, style="italic", family=SERIF)
save(fig, "fig7_3")

# Figure 7.4 progression staircase
fig, ax = canvas(W, 2.3, xlim=(0, 150), ylim=(0, 76))
stages = [("1", "Natural\nbreathing", "posture only"), ("2", "Low, quiet", "nogare; light\ntension"),
          ("3", "Audible", "soft 'haa';\nmoderate"), ("4", "Firm", "stronger breath;\nfirm trunk"),
          ("5", "Full Sanchin", "ibuki; strong\npeak tension")]
for i, (n, t1, t2) in enumerate(stages):
    x = 6 + i * 28.5; h = 24 + i * 7.5
    ax.add_patch(Rectangle((x, 6), 26, h, fc=G1 if i in (2, 3) else WH, ec=K, lw=0.9))
    numdot(ax, x + 13, 6 + h + 6, n, r=3.6, fs=6.5)
    ax.text(x + 13, 6 + h - 4, t1, ha="center", va="top", fontsize=6.0, fontweight="bold", linespacing=1.05)
    ax.text(x + 13, 9, t2, ha="center", va="bottom", fontsize=5.0, linespacing=1.05)
label(ax, 40, 72, "Shaded: where most training time is spent", fs=5.8, style="italic", family=SERIF)
save(fig, "fig7_4")
