from common import *
from matplotlib.patches import Wedge


def fig7_1():
    fig, axs = plt.subplots(1, 4, figsize=(W, 1.5))
    cols = [TEAL, AMBER, NAVY]
    for k, ax in enumerate(axs):
        wt = k * np.pi / 3
        ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.6); ax.set_aspect("equal"); ax.axis("off")
        ax.add_patch(Circle((0, 0), 1.25, fill=False, ec="#c9d3d8", lw=4))
        tot = np.zeros(2)
        for ph in range(3):
            ang = ph * 2 * np.pi / 3
            mag = np.cos(wt - ang)
            vec = mag * np.array([np.cos(ang), np.sin(ang)])
            tot += vec
            if abs(mag) > 0.02:
                arrow(ax, 0, 0, vec[0] * 0.75, vec[1] * 0.75, c=cols[ph], lw=1.0, ms=5)
        tot *= 2 / 3
        arrow(ax, 0, 0, tot[0] * 1.05, tot[1] * 1.05, c=RED, lw=2.4, ms=9)
        ax.set_title(f"ωt = {k * 60}°", fontsize=7, color=NAVY, pad=1)
    axs[0].text(-1.5, -1.55, "phase fields: a b c", fontsize=5.8, color=GREY)
    axs[3].text(1.5, -1.55, "resultant", fontsize=6, color=RED, ha="right")
    fig.subplots_adjust(wspace=0.05)
    save(fig, "fig7_1")


def fig7_2():
    s = np.linspace(-0.4, 1, 600)
    sk = 0.12
    T = 2 * 1.0 / (s / sk + sk / np.where(s == 0, 1e-9, s))
    T = np.where(np.abs(s) < 1e-6, 0, T)
    n = 1 - s
    fig, ax = plt.subplots(figsize=(W, 2.3))
    ax.plot(n * 100, T, color=TEAL, lw=1.8)
    ax.axhline(0, color=GREY, lw=0.6); ax.axvline(100, color=GREY, lw=0.6, ls=":")
    ax.text(101, 1.05, "synchronous\nspeed", fontsize=6.6, color=GREY)
    ax.annotate("breakdown torque", xy=(88, 1.02), xytext=(45, 1.2), fontsize=6.8, color=NAVY, arrowprops=dict(arrowstyle="->", color=NAVY, lw=0.6))
    ax.axvspan(95, 100, color=AMBER, alpha=0.15); ax.text(93, -0.95, "normal\noperating\nregion", fontsize=6.2, color=AMBER, ha="right")
    ax.text(125, -1.2, "generating", fontsize=6.8, color=NAVY, ha="center"); ax.text(30, 0.5, "motoring", fontsize=6.8, color=NAVY)
    ax.set_xlabel("Rotor speed (% of synchronous)"); ax.set_ylabel("Torque (p.u.)")
    ax.set_xlim(0, 140); ax.set_ylim(-1.4, 1.45)
    save(fig, "fig7_2")


def stator(ax, slots=36):
    ax.add_patch(Circle((0, 0), 1.45, fc="#d9e0e4", ec=NAVY, lw=0.8))
    ax.add_patch(Circle((0, 0), 1.08, fc="white", ec=NAVY, lw=0.6))
    for i in range(slots):
        a = 2 * np.pi * i / slots
        ax.add_patch(Wedge((0, 0), 1.32, np.degrees(a) - 2.3, np.degrees(a) + 2.3, width=0.22, fc="#c58a4a", ec="none"))


def fig7_3():
    fig, axs = plt.subplots(1, 4, figsize=(W, 1.6))
    titles = ["(a) Surface PM", "(b) Interior PM (V)", "(c) Induction cage", "(d) Sync. reluctance"]
    for ax, t in zip(axs, titles):
        ax.set_xlim(-1.55, 1.55); ax.set_ylim(-1.55, 1.7); ax.set_aspect("equal"); ax.axis("off")
        ax.set_title(t, fontsize=6.6, color=NAVY, pad=1, fontweight="semibold")
        stator(ax)
        ax.add_patch(Circle((0, 0), 1.03, fc="#9aa8b0", ec=NAVY, lw=0.6))
        ax.add_patch(Circle((0, 0), 0.25, fc="white", ec=NAVY, lw=0.6))
    # SPM
    a = axs[0]
    for i in range(8):
        a.add_patch(Wedge((0, 0), 1.03, i * 45 + 4, i * 45 + 41, width=0.16, fc=TEAL if i % 2 else AMBER, ec="none"))
    # IPM V
    a = axs[1]
    for i in range(8):
        c = np.radians(i * 45 + 22.5)
        for sgn in (-1, 1):
            p0 = 0.5 * np.array([np.cos(c + sgn * 0.12), np.sin(c + sgn * 0.12)])
            p1 = 0.9 * np.array([np.cos(c + sgn * 0.33), np.sin(c + sgn * 0.33)])
            a.plot([p0[0], p1[0]], [p0[1], p1[1]], color=TEAL if i % 2 else AMBER, lw=3.2, solid_capstyle="butt")
    # cage
    a = axs[2]
    for i in range(28):
        ang = 2 * np.pi * i / 28
        a.add_patch(Circle((0.88 * np.cos(ang), 0.88 * np.sin(ang)), 0.07, fc="#c58a4a", ec="none"))
    # synrel barriers
    a = axs[3]
    for i in range(4):
        c = np.radians(i * 90 + 45)
        for r in (0.45, 0.62, 0.79):
            th = np.linspace(c - 0.62, c + 0.62, 30)
            depth = r
            xs = []; ys = []
            for t in th:
                rr = depth + (1.0 - depth) * ((t - c) / 0.62) ** 2 * 0.95
                xs.append(rr * np.cos(t)); ys.append(rr * np.sin(t))
            a.plot(xs, ys, color="white", lw=1.7)
    fig.subplots_adjust(wspace=0.04)
    save(fig, "fig7_3")


if __name__ == "__main__":
    fig7_1(); fig7_2(); fig7_3()
