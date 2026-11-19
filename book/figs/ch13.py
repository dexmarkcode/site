from common import *


def fig13_1():
    fig, ax = canvas(h=2.6, ylim=(0, 58))
    label(ax, 2, 55, "AC charging (Mode 3)", fs=7.3, c=NAVY, ha="left", fontweight="semibold")
    box(ax, 1, 36, 14, 12, "Grid\nAC", fs=6.3, fc="white", ec=GREY)
    box(ax, 21, 36, 18, 12, "Wallbox\nprotection,\ncontrol pilot", fs=5.8)
    ax.add_patch(Rectangle((44, 30), 54, 24, fc="none", ec=TEAL, lw=0.8, ls="--")); label(ax, 96, 51.5, "vehicle", fs=6, c=TEAL, ha="right")
    box(ax, 47, 36, 18, 12, "On-board\ncharger\nAC→DC", fs=5.8, fc=PALE, ec=AMBER)
    box(ax, 72, 36, 18, 12, "Battery\n+ BMS", fs=6.3, fc="white", ec=TEAL)
    for x1, x2 in [(15, 21), (39, 47), (65, 72)]:
        arrow(ax, x1, 42, x2, 42, c=TEAL, lw=1.4, ms=6)
    label(ax, 43, 45, "AC", fs=5.8, c=GREY)
    label(ax, 2, 25, "DC charging (Mode 4)", fs=7.3, c=NAVY, ha="left", fontweight="semibold")
    box(ax, 1, 4, 14, 12, "Grid\nAC", fs=6.3, fc="white", ec=GREY)
    box(ax, 21, 4, 18, 12, "Station:\nrectifier +\nisolated DC-DC", fs=5.6, fc=PALE, ec=AMBER)
    ax.add_patch(Rectangle((44, 0), 54, 22, fc="none", ec=TEAL, lw=0.8, ls="--"))
    box(ax, 47, 4, 18, 12, "On-board\ncharger\n(bypassed)", fs=5.6, fc="#f2f2f2", ec="#c0c6ca", tc=GREY)
    box(ax, 72, 4, 18, 12, "Battery\n+ BMS", fs=6.3, fc="white", ec=TEAL)
    arrow(ax, 15, 10, 21, 10, c=TEAL, lw=1.4, ms=6)
    line(ax, [39, 44, 44, 69, 69], [10, 10, 19, 19, 10], c=TEAL, lw=1.6); arrow(ax, 69, 10, 72, 10, c=TEAL, lw=1.6, ms=6)
    label(ax, 56, 20.5, "DC through inlet", fs=5.8, c=TEAL)
    arrow(ax, 81, 16, 81, 22, c=AMBER, lw=0.9, ms=5, ls="--"); label(ax, 92, 25, "current requests", fs=5.5, c=AMBER)
    save(fig, "fig13_1")


def fig13_2():
    fig = plt.figure(figsize=(W, 2.4))
    ax = fig.add_axes([0, 0, 0.47, 1]); ax.set_xlim(0, 50); ax.set_ylim(0, 50); ax.set_aspect("equal"); ax.axis("off")
    box(ax, 1, 14, 13, 22, "±12 V\n1 kHz\nPWM", fs=6, fc=PALE, ec=AMBER)
    line(ax, [14, 18], [30, 30], c=NAVY)
    ax.add_patch(Rectangle((18, 28.5), 6, 3, fc="white", ec=NAVY, lw=0.8)); label(ax, 21, 34, "1 kΩ", fs=6, c=NAVY)
    line(ax, [24, 34], [30, 30], c=NAVY); label(ax, 29, 32.5, "CP", fs=6.5, c=TEAL, fontweight="bold")
    ax.add_patch(Polygon([[34, 31.5], [34, 28.5], [36.6, 30]], fc=NAVY))
    line(ax, [36.6, 40], [30, 30], c=NAVY); line(ax, [40, 40], [30, 26], c=NAVY)
    ax.add_patch(Rectangle((38.5, 18), 3, 8, fc="white", ec=NAVY, lw=0.8)); label(ax, 37.5, 22, "2.74 kΩ", fs=5.8, c=NAVY, ha="right")
    line(ax, [40, 47.5, 47.5], [30, 30, 28], c=NAVY)
    ax.add_patch(Rectangle((46, 20), 3, 8, fc="white", ec=NAVY, lw=0.8)); label(ax, 47.5, 17, "1.3 kΩ\n+ switch", fs=5.4, c=NAVY)
    line(ax, [40, 40], [18, 10], c=NAVY); line(ax, [1, 49], [10, 10], c=GREEN, lw=1.2); label(ax, 25, 7.5, "protective earth", fs=5.8, c=GREEN)
    line(ax, [7.5, 7.5], [14, 10], c=NAVY)
    ax.add_patch(Rectangle((31, 12), 19, 34, fc="none", ec=TEAL, lw=0.7, ls="--")); label(ax, 40.5, 43.5, "vehicle", fs=6, c=TEAL)
    ax.text(0.5, 47, "(a)", fontsize=8, color=NAVY, fontweight="bold")
    ax2 = fig.add_axes([0.62, 0.17, 0.37, 0.75])
    t = np.linspace(0, 7, 2000)
    sig = np.full_like(t, 12.0)
    sig[(t >= 1) & (t < 2.5)] = 9
    pw = (t >= 2.5) & (t < 4)
    sig[pw] = np.where(((t[pw] - 2.5) * 4) % 1 < 0.5, 9, -12)
    ch = t >= 4
    sig[ch] = np.where(((t[ch] - 4) * 4) % 1 < 0.5, 6, -12)
    ax2.plot(t, sig, color=NAVY, lw=1)
    for x, s in [(0.5, "A"), (1.75, "B"), (3.25, "B\n+PWM"), (5.5, "C: charging")]:
        ax2.text(x, 13.5, s, ha="center", fontsize=6.3, color=TEAL)
    ax2.set_yticks([-12, 0, 6, 9, 12]); ax2.set_xticks([]); ax2.set_ylim(-14, 18); ax2.set_ylabel("CP voltage (V)")
    ax2.text(-0.25, 1.02, "(b)", transform=ax2.transAxes, fontsize=8, color=NAVY, fontweight="bold")
    ax2.set_xlabel("time")
    save(fig, "fig13_2")


def fig13_3():
    fig, ax = plt.subplots(figsize=(W, 2.6))
    phases = [("1", 0, 4), ("2", 4, 12), ("3", 12, 16), ("4", 16, 22), ("5", 22, 26), ("6  energy transfer", 26, 92), ("7", 92, 100)]
    for i, (n, a, b) in enumerate(phases):
        ax.axvspan(a, b, color=["#f4f8f9", "white"][i % 2], zorder=-2)
        ax.text((a + b) / 2, 1.5, n, ha="center", fontsize=6.8, color=NAVY, va="bottom")
    t = np.linspace(0, 100, 1000)
    V = np.where(t < 16, 0, np.where(t < 22, 0.85, np.where(t < 26, (t - 22) / 4 * 0.72, 0.72 + 0.12 * (t - 26) / 66)))
    V = np.where(t > 94, np.maximum(0, 0.84 - (t - 94) / 3), V)
    V = np.where((t >= 16) & (t < 17), (t - 16) * 0.85, V)
    I = np.where(t < 26.5, 0, np.minimum((t - 26.5) / 2, 1.0))
    I = np.where(t > 45, 1 - (t - 45) / 47 * 0.65, I)
    I = np.where(t > 92, np.maximum(0, 0.35 - (t - 92) / 1.5), I)
    ax.plot(t, V, color=AMBER, lw=1.6, label="station output voltage")
    ax.plot(t, I, color=TEAL, lw=1.8, label="charging current (follows vehicle request)")
    ax.set_xlim(0, 100); ax.set_ylim(0, 1.65); ax.set_yticks([]); ax.set_xticks([])
    ax.set_xlabel("session time (not to scale)"); ax.set_ylabel("p.u.")
    ax.legend(loc="upper center", fontsize=6.5, ncol=2, bbox_to_anchor=(0.6, 0.9))
    save(fig, "fig13_3")


if __name__ == "__main__":
    fig13_1(); fig13_2(); fig13_3()
