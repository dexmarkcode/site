from common import *

# Figure 9.1 three timelines
fig, axs = plt.subplots(3, 1, figsize=(W, 2.6), sharex=True, gridspec_kw=dict(hspace=0.25))
t = np.linspace(0, 14, 700)
# phases: step in 0-3, block out 3-6? simplified: step(in 0-3), pull hand (in 3-6)?? use: step+pull in 0-3, punch out 3-8, return in 8-10 out 10-12, settle 12-14
breath = np.piecewise(t, [t < 3, (t >= 3) & (t < 8), (t >= 8) & (t < 10), (t >= 10) & (t < 12), t >= 12],
                      [lambda x: x / 3, lambda x: 1 - (x - 3) / 5 * 0.8, lambda x: 0.2 + (x - 8) / 2 * 0.4,
                       lambda x: 0.6 - (x - 10) / 2 * 0.35, 0.25])
move = np.piecewise(t, [t < 3, (t >= 3) & (t < 8), (t >= 8) & (t < 10), t >= 10],
                    [lambda x: 0.5 * np.sin(x / 3 * np.pi) ** 2, lambda x: np.sin((x - 3) / 5 * np.pi) ** 1.3,
                     lambda x: 0.5 * np.sin((x - 8) / 2 * np.pi), lambda x: 0.25 * np.sin(np.clip((x - 10) / 2, 0, 1) * np.pi)])
ten = 0.3 + 0.62 * np.exp(-((t - 8) / 1.7) ** 2) * (t <= 8) + 0.62 * np.exp(-((t - 8) / 0.9) ** 2) * (t > 8) + 0.18 * np.exp(-((t - 12) / 0.8) ** 2)
late = 0.3 + 0.62 * np.exp(-((t - 9.6) / 1.4) ** 2)
for ax, y, name in zip(axs, (breath, move, ten), ("breath\n(lung volume)", "movement\n(hand speed)", "tension")):
    ax.plot(t, y, color=K, lw=1.6)
    ax.set_yticks([]); ax.set_ylim(0, 1.1)
    ax.set_ylabel(name, fontsize=5.8, rotation=0, ha="right", va="center")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.axvline(8, color=K, lw=0.6, ls=(0, (1, 1.5)))
axs[2].plot(t, late, color=K, lw=1.0, ls=(0, (3, 2)))
axs[2].text(10.2, 0.85, "late peak (fault)", fontsize=5.4)
axs[0].text(7.9, 1.05, "turning point: breath ends,\npunch arrives, tension peaks", fontsize=5.2, va="top", ha="right")
axs[2].set_xticks([1.5, 5.5, 9, 11, 13])
axs[2].set_xticklabels(["step", "punch", "return", "settle", ""], fontsize=6)
for a, b in ((0, 3), (8, 10)):
    for ax in axs:
        ax.axvspan(a, b, color=G1, lw=0)
save(fig, "fig9_1")

# Figure 9.2 speed profiles
fig, ax = plt.subplots(figsize=(W, 1.6))
t = np.linspace(0, 15, 1500)
cont = np.abs(np.sin(t / 5 * np.pi)) ** 1.6
ss = np.zeros_like(t)
for k in range(3):
    a = k * 5 + 0.5
    m = (t >= a) & (t < a + 2.6)
    ss[m] = 1.0 * (np.sin((t[m] - a) / 2.6 * np.pi) ** 0.35)
ax.plot(t, cont, color=K, lw=1.8, label="continuous")
ax.plot(t, ss, color=K, lw=1.1, ls=(0, (3, 2)), label="stop-start")
for k in range(3):
    ax.text(k * 5 + 2.5, -0.18, f"movement {k + 1}", ha="center", fontsize=5.8)
ax.set_ylim(-0.25, 1.15); ax.set_xlim(0, 15)
ax.set_yticks([]); ax.set_xticks([])
ax.set_ylabel("hand speed", fontsize=6)
for s in ("top", "right", "bottom"):
    ax.spines[s].set_visible(False)
ax.axhline(0, color=K, lw=0.6)
ax.legend(fontsize=5.8, frameon=False, loc="upper right", ncol=2, bbox_to_anchor=(1, 1.18))
save(fig, "fig9_2")

# Figure 9.3 kata rhythm blocks
fig, ax = canvas(W, 1.35, xlim=(0, 200), ylim=(0, 46))
secs = [("Opening", 25, "measured,\nceremonial"), ("Advance", 55, "steady, regular\npulse"), ("Turns", 40, "slower; stance\nheld through turn"),
        ("Retreat and\nspear-hands", 40, "fuller breaths"), ("Circular\nblocks", 25, "long, flowing"), ("Close", 15, "settling")]
total = sum(s[1] for s in secs)
x = 2
for i, (n, w, d) in enumerate(secs):
    ww = w / total * 196
    ax.add_patch(Rectangle((x, 22), ww, 16, fc=G1 if i % 2 else WH, ec=K, lw=0.8))
    ax.text(x + ww / 2, 30, n, ha="center", va="center", fontsize=5.6, fontweight="bold", linespacing=1.0)
    ax.text(x + ww / 2, 18, d, ha="center", va="top", fontsize=5.0, linespacing=1.05)
    x += ww
ax.text(100, 43, "approximate share of a three-minute performance", ha="center", fontsize=5.6, style="italic", family=SERIF)
save(fig, "fig9_3")
