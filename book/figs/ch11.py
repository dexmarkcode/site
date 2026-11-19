from common import *
import schemdraw
import schemdraw.elements as elm
schemdraw.config(fontsize=8, font="Source Sans 3", lw=1.0, color=NAVY)


def sw(ax, x, y, name):
    # switch body
    box(ax, x - 3, y - 4, 6, 8, name, fs=6.5, fc="white", ec=NAVY, r=0.6)
    # antiparallel diode
    xd = x + 6
    ax.add_patch(Polygon([[xd - 1.6, y - 1.2], [xd + 1.6, y - 1.2], [xd, y + 1.2]], fc=NAVY, ec=NAVY))
    line(ax, [xd - 1.6, xd + 1.6], [y + 1.2, y + 1.2], c=NAVY, lw=1)
    line(ax, [x, xd, xd], [y + 4, y + 4, y + 1.2], c=NAVY, lw=0.8)
    line(ax, [x, xd, xd], [y - 4, y - 4, y - 1.2], c=NAVY, lw=0.8)


def fig11_1():
    fig, ax = canvas(h=2.5, ylim=(0, 56))
    T, B = 50, 4
    line(ax, [6, 82], [T, T], c=RED, lw=1.6); line(ax, [6, 82], [B, B], c=NAVY, lw=1.6)
    # battery
    line(ax, [6, 6], [T, 31], c=RED, lw=1.2); line(ax, [6, 6], [B, 25], c=NAVY, lw=1.2)
    for yy, w in ((31, 6), (29, 3.4), (27, 6), (25, 3.4)):
        line(ax, [6 - w / 2, 6 + w / 2], [yy, yy], c=NAVY, lw=1.4)
    label(ax, 1.5, 28, "$V_{DC}$", fs=8, c=NAVY, ha="right")
    # capacitor
    line(ax, [18, 18], [T, 28.5], c=NAVY, lw=1); line(ax, [18, 18], [B, 25.5], c=NAVY, lw=1)
    line(ax, [15, 21], [28.5, 28.5], c=NAVY, lw=1.6); line(ax, [15, 21], [25.5, 25.5], c=NAVY, lw=1.6)
    label(ax, 23.5, 27, "$C_{DC}$", fs=8, c=NAVY, ha="left")
    for k, x in enumerate((36, 56, 76)):
        line(ax, [x, x], [T, 42], c=NAVY, lw=1); sw(ax, x, 38, f"S{k+1}")
        line(ax, [x, x], [34, 20], c=NAVY, lw=1); sw(ax, x, 16, f"S{k+4}")
        line(ax, [x, x], [12, B], c=NAVY, lw=1)
        ax.add_patch(Circle((x, 27), 0.8, fc=NAVY))
        line(ax, [x, x + 12], [27, 27], c=TEAL, lw=1.6)
        label(ax, x + 13.5, 27, "abc"[k], fs=8.5, c=TEAL, fontweight="semibold")
    label(ax, 100, 27, "to motor\nphases", fs=7, c=TEAL)
    label(ax, 44, 53, "+ rail", fs=6.5, c=RED); label(ax, 44, 1, "− rail", fs=6.5, c=NAVY)
    save(fig, "fig11_1")


def fig11_2():
    t = np.linspace(0, 1, 4000)
    fc = 15; m = 0.85
    ref = m * np.sin(2 * np.pi * t)
    car = 2 * np.abs(2 * ((t * fc) % 1) - 1) - 1
    out = np.where(ref > car, 1, -1)
    fig, axs = plt.subplots(2, 1, figsize=(W, 2.6), sharex=True)
    axs[0].plot(t * 360, car, color=GREY, lw=0.6, label="carrier")
    axs[0].plot(t * 360, ref, color=TEAL, lw=1.6, label="reference")
    axs[0].legend(loc="upper right", ncol=2, fontsize=6.5); axs[0].set_ylim(-1.3, 1.5)
    axs[0].text(-0.1, 0.9, "(a)", transform=axs[0].transAxes, fontsize=8, color=NAVY, fontweight="bold")
    axs[1].fill_between(t * 360, 0, out, step="pre", color=NAVY, alpha=0.18, lw=0)
    axs[1].plot(t * 360, out, color=NAVY, lw=0.7)
    avg = np.convolve(out, np.ones(267) / 267, mode="same")
    axs[1].plot(t * 360, avg, color=AMBER, lw=1.6, label="local average")
    axs[1].set_yticks([-1, 0, 1]); axs[1].set_yticklabels(["$-V_{DC}/2$", "0", "$+V_{DC}/2$"])
    axs[1].legend(loc="upper right", fontsize=6.5); axs[1].set_ylim(-1.3, 1.5)
    axs[1].set_xlabel("Electrical angle (°)"); axs[1].set_xticks([0, 90, 180, 270, 360])
    axs[1].text(-0.1, 0.9, "(b)", transform=axs[1].transAxes, fontsize=8, color=NAVY, fontweight="bold")
    save(fig, "fig11_2")


def fig11_3():
    fig, ax = plt.subplots(figsize=(W, 2.8))
    ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.1, 1.15); ax.set_aspect("equal"); ax.axis("off")
    labels = ["100", "110", "010", "011", "001", "101"]
    pts = [(2 / 3 * np.cos(k * np.pi / 3), 2 / 3 * np.sin(k * np.pi / 3)) for k in range(6)]
    pts = [(p[0] * 1.5, p[1] * 1.5) for p in pts]
    ax.add_patch(Polygon(pts, closed=True, fc=LIGHT, ec=NAVY, lw=1.2))
    r = 1.0 * np.cos(np.pi / 6)
    ax.add_patch(Circle((0, 0), r, fill=False, ec=AMBER, lw=1.2, ls="--"))
    for k, (x, y) in enumerate(pts):
        arrow(ax, 0, 0, x, y, c=TEAL, lw=1.2, ms=7)
        ax.text(x * 1.15, y * 1.15, f"V{k+1}\n({labels[k]})", ha="center", va="center", fontsize=6.6, color=NAVY)
    ax.plot(0, 0, "o", color=NAVY, ms=4); ax.text(0.05, -0.12, "V0 (000), V7 (111)", fontsize=6.3, color=NAVY)
    a = np.radians(22)
    arrow(ax, 0, 0, 0.8 * np.cos(a), 0.8 * np.sin(a), c=RED, lw=2, ms=9)
    ax.text(0.82 * np.cos(a) + 0.03, 0.82 * np.sin(a), "$v^*$", fontsize=9, color=RED)
    ax.text(0.55, 0.12, "sector I", fontsize=6.5, color=GREY)
    save(fig, "fig11_3")


def fig11_4():
    P = np.linspace(2, 150, 300)
    def eff(V0, r, Esw):
        I = P * 1000 / (np.sqrt(3) * 260 * 0.9) * np.sqrt(2)
        cond = 6 * (V0 * I * 0.26 + r * I ** 2 * 0.21)
        sw = 6 * 10000 / np.pi * Esw * I / 400
        fixed = 150 if V0 > 0 else 60
        return P * 1000 / (P * 1000 + cond + sw + fixed) * 100
    fig, ax = plt.subplots(figsize=(W, 2.3))
    ax.plot(P, eff(0.9, 1.6e-3, 0.055), color=NAVY, lw=1.6, label="Si IGBT inverter")
    ax.plot(P, eff(0.0, 3.0e-3, 0.012), color=TEAL, lw=1.8, label="SiC MOSFET inverter")
    ax.axvspan(2, 30, color=AMBER, alpha=0.08); ax.text(16, 91.3, "where most\ndriving happens", fontsize=6.5, color=AMBER, ha="center")
    ax.set_xlabel("Output power (kW)"); ax.set_ylabel("Efficiency (%)")
    ax.set_xlim(0, 150); ax.set_ylim(90, 100); ax.legend(loc="lower right")
    save(fig, "fig11_4")


if __name__ == "__main__":
    fig11_1(); fig11_2(); fig11_3(); fig11_4()
