from common import *


def cells_row(ax, x, y, n, w, h, gap, fc=TEAL):
    for i in range(n):
        ax.add_patch(Rectangle((x + i * (w + gap), y), w, h, fc=fc, ec="white", lw=0.4))


def fig5_1():
    fig, axs = plt.subplots(1, 3, figsize=(W, 1.9))
    for ax, t in zip(axs, ["(a) Module-based", "(b) Cell-to-pack", "(c) Cell-to-body"]):
        ax.set_xlim(0, 40); ax.set_ylim(0, 34); ax.axis("off"); ax.set_aspect("equal")
        ax.set_title(t, fontsize=7.5, color=NAVY, fontweight="semibold")
    a = axs[0]
    a.add_patch(FancyBboxPatch((1, 3), 38, 26, boxstyle="round,pad=0,rounding_size=1", fc="#e6ecef", ec=NAVY, lw=1))
    for r in range(2):
        for c in range(3):
            x0, y0 = 3 + c * 12, 6 + r * 11.5
            a.add_patch(Rectangle((x0, y0), 10.5, 9.5, fc="white", ec=GREY, lw=0.9))
            cells_row(a, x0 + 0.8, y0 + 1, 6, 1.2, 7.5, 0.3)
    a.text(20, 0.5, "cells ≈ 55–60 % of pack mass", fontsize=6, color=GREY, ha="center")
    a = axs[1]
    a.add_patch(FancyBboxPatch((1, 3), 38, 26, boxstyle="round,pad=0,rounding_size=1", fc="#e6ecef", ec=NAVY, lw=1))
    for r in range(2):
        cells_row(a, 2.5, 5 + r * 12, 1, 35, 10.5, 0, fc="none")
        for k in range(17):
            a.add_patch(Rectangle((2.5 + k * 2.06, 5 + r * 12), 1.9, 10.5, fc=TEAL, ec="white", lw=0.3))
    a.text(20, 0.5, "≈ 70–80 %", fontsize=6, color=GREY, ha="center")
    a = axs[2]
    a.add_patch(Rectangle((1, 3), 38, 22, fc="#e6ecef", ec=NAVY, lw=1))
    for k in range(17):
        a.add_patch(Rectangle((2.5 + k * 2.06, 5), 1.9, 18, fc=TEAL, ec="white", lw=0.3))
    a.add_patch(Rectangle((0, 25), 40, 2.4, fc=AMBER, ec=NAVY, lw=0.8))
    a.text(20, 29.2, "pack lid = cabin floor", fontsize=6, color=AMBER, ha="center")
    a.text(20, 0.5, "cells carry body loads", fontsize=6, color=GREY, ha="center")
    fig.subplots_adjust(wspace=0.08)
    save(fig, "fig5_1")


def fig5_2():
    fig, ax = canvas(h=2.7, ylim=(0, 60))
    # cell string
    for i in range(8):
        x = 4 + i * 6.2 if i < 4 else 8 + i * 6.2
        ax.add_patch(Rectangle((x, 30), 4.5, 12, fc=TEAL, ec=NAVY, lw=0.6))
        if i not in (3, 7):
            line(ax, [x + 4.5, x + 6.2], [39, 39], c=NAVY, lw=1.6)
    box(ax, 28.6, 33, 7.2, 6, "MSD", fs=6, fc=PALE, ec=AMBER)
    line(ax, [27.1, 28.6], [39, 36], c=NAVY, lw=1.4); line(ax, [35.8, 37.2], [36, 39], c=NAVY, lw=1.4)
    label(ax, 30, 45.5, "series cell string (e.g. 96s or 192s)", fs=6.5, c=NAVY)
    label(ax, 32.2, 30.5, "service\ndisconnect", fs=5.5, c=AMBER, va="top")
    # BDU
    box(ax, 66, 18, 30, 34, "", fc="#f4f7f8", ec=NAVY)
    line(ax, [4, 4, 99], [30, 24, 24], c=NAVY, lw=1.8)
    label(ax, 81, 49, "Battery disconnect unit", fs=6.8, c=NAVY, fontweight="semibold")
    line(ax, [55.9, 70], [39, 39], c=RED, lw=1.8)
    box(ax, 70, 36, 7, 6, "F", fs=6.5, fc="white"); box(ax, 79, 36, 7, 6, "K+", fs=6.3, fc="white")
    line(ax, [77, 79], [39, 39], c=RED, lw=1.8); line(ax, [86, 99], [39, 39], c=RED, lw=1.8)
    box(ax, 78.5, 43.5, 8, 4, "PC+R", fs=5.5, fc="white")
    line(ax, [77.5, 78.5], [39, 45.5], c=RED, lw=0.9); line(ax, [86.5, 88], [45.5, 39], c=RED, lw=0.9)
    box(ax, 70, 21, 7, 6, "I", fs=6.5, fc="white", zorder=3); box(ax, 79, 21, 7, 6, "K−", fs=6.3, fc="white", zorder=3)
    box(ax, 89, 29, 6.5, 6, "pyro", fs=5.5, fc=PALE, ec=AMBER)
    label(ax, 99, 41.5, "HV+", fs=6.3, c=RED, ha="right"); label(ax, 99, 26.5, "HV−", fs=6.3, c=NAVY, ha="right")
    # CMUs and BMC
    for i in range(2):
        box(ax, 6 + i * 26, 8, 18, 7, "Cell monitor", fs=6, fc="white", ec=GREY)
        for j in range(4):
            line(ax, [8 + i * 26 + j * 4.5, 8 + i * 26 + j * 4.5], [15, 30], c=GREY, lw=0.5, ls=(0, (2, 1.5)))
    box(ax, 66, 4, 30, 9, "Battery management\ncontroller", fs=6.5, fc=NAVY, ec=NAVY, tc="white")
    line(ax, [24, 32], [11.5, 11.5], c=AMBER, lw=0.9); line(ax, [50, 66], [11.5, 8.5], c=AMBER, lw=0.9)
    label(ax, 37, 4.5, "isolated daisy chain / wireless", fs=5.5, c=AMBER)
    save(fig, "fig5_2")


def fig5_3():
    fig = plt.figure(figsize=(W, 2.3))
    ax1 = fig.add_axes([0, 0, 0.48, 1]); ax2 = fig.add_axes([0.52, 0, 0.48, 1])
    for a in (ax1, ax2):
        a.set_xlim(0, 50); a.set_ylim(0, 50); a.axis("off"); a.set_aspect("equal")
    a = ax1
    a.add_patch(Rectangle((8, 20), 34, 26, fc=TEAL, ec=NAVY, lw=0.8)); a.text(25, 36, "cell", color="white", ha="center", fontsize=8, fontweight="semibold")
    for k in range(5):
        a.plot([25 + k * 1.5 - 3, 25 + k * 1.5 - 3], [24, 30], color=AMBER, lw=0.8)
    a.text(25, 22, "heat", color=AMBER, ha="center", fontsize=6.5)
    a.add_patch(Rectangle((8, 17.5), 34, 2.5, fc="#cfd8dc", ec=GREY, lw=0.6)); a.text(43, 18.2, "TIM", fontsize=6.3, color=GREY)
    a.add_patch(Rectangle((5, 8), 40, 9.5, fc="#b9c2c8", ec=NAVY, lw=0.8))
    for x in range(9, 40, 6):
        a.add_patch(Rectangle((x, 10), 5, 5, fc="#7fd3dc", ec=NAVY, lw=0.5))
    a.text(46, 12, "cold\nplate", fontsize=6.3, color=NAVY, va="center")
    a.text(25, 4, "coolant channels", fontsize=6.3, color=TEAL, ha="center")
    a.text(1, 47, "(a)", fontsize=8, color=NAVY, fontweight="bold")
    a = ax2
    nodes = [("$T_{core}$", 44), ("", 36), ("", 28), ("", 20), ("", 12), ("$T_{coolant}$", 4)]
    names = ["$R_{int}$", "$R_{case}$", "$R_{TIM}$", "$R_{plate}$", "$R_{conv}$"]
    for i in range(5):
        y1, y2 = nodes[i][1], nodes[i + 1][1]
        ys = np.linspace(y1 - 1.5, y2 + 1.5, 9)
        xs = [22] + [22 + (1.6 if k % 2 else -1.6) for k in range(1, 8)] + [22]
        a.plot([22, 22], [y1, y1 - 1.5], color=NAVY, lw=1); a.plot(xs, ys, color=NAVY, lw=1); a.plot([22, 22], [y2 + 1.5, y2], color=NAVY, lw=1)
        a.text(26, (y1 + y2) / 2, names[i], fontsize=8, va="center", color=NAVY)
    for t, y in nodes:
        a.add_patch(Circle((22, y), 0.9, fc=NAVY))
        if t:
            a.text(18, y, t, fontsize=8, ha="right", va="center", color=TEAL)
    arrow(a, 38, 42, 38, 6, c=AMBER, lw=1.6); a.text(40, 24, "$\\dot{Q}$", fontsize=10, color=AMBER)
    a.text(1, 47, "(b)", fontsize=8, color=NAVY, fontweight="bold")
    save(fig, "fig5_3")


def fig5_4():
    fig = plt.figure(figsize=(W, 2.4))
    ax = fig.add_axes([0.1, 0.18, 0.88, 0.75])
    t = np.linspace(0, 600, 600)
    def tr(t0, peak=750):
        T = np.where(t < t0, 30 + (np.maximum(t - (t0 - 120), 0)) * 0.9, 0)
        rise = peak * np.exp(-(t - t0) / 260) * (1 - np.exp(-(t - t0) / 6))
        return np.where(t < t0, np.minimum(T, 140), 140 + np.maximum(rise, 0))
    for k, t0 in enumerate([20, 110, 210, 320]):
        ax.plot(t, tr(t0), color=[RED, AMBER, NAVY, GREY][k], lw=1.3, label=f"cell {k + 1}" if k else "cell 1 (trigger)")
    T2 = 30 + 70 * (1 - np.exp(-t / 250))
    ax.plot(t, T2, color=TEAL, lw=1.8, ls="--", label="cell 2 with aerogel barrier")
    ax.axhline(140, color=GREY, lw=0.6, ls=":"); ax.text(590, 150, "runaway onset (indicative)", fontsize=6.3, color=GREY, ha="right")
    ax.set_xlabel("Time after trigger (s)"); ax.set_ylabel("Cell temperature (°C)")
    ax.set_xlim(0, 600); ax.set_ylim(0, 950); ax.legend(loc="upper right", fontsize=6.5, ncol=1)
    save(fig, "fig5_4")


if __name__ == "__main__":
    fig5_1(); fig5_2(); fig5_3(); fig5_4()
