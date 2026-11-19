from common import *
from matplotlib.patches import Ellipse
from matplotlib.colors import LinearSegmentedColormap
rng = np.random.default_rng(8)


def fig8_1():
    psi, Ld, Lq, Imax = 0.08, 0.15e-3, 0.45e-3, 600
    fig, ax = plt.subplots(figsize=(W, 2.9))
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(Imax * np.cos(th), Imax * np.sin(th), color=NAVY, lw=1.6, label="Current limit")
    Vmax = 400 / np.sqrt(3)
    for w, c, lab in [(1700, TEAL, "ω₁"), (2800, AMBER, "ω₂"), (4200, RED, "ω₃")]:
        a = Vmax / (w * Ld); b = Vmax / (w * Lq)
        ax.plot(-psi / Ld + a * np.cos(th), b * np.sin(th), color=c, lw=1.3)
        ax.text(-psi / Ld + a * 0.72, b * 0.72, lab, color=c, fontsize=8)
    ax.plot(-psi / Ld, 0, "x", color=RED, ms=6); ax.text(-psi / Ld, -55, "$-\\psi_m/L_d$", fontsize=7.5, color=RED, ha="center")
    ax.axhline(0, color=GREY, lw=0.6); ax.axvline(0, color=GREY, lw=0.6)
    pts = [(-180, 570), (-330, 500), (-470, 370)]
    for (x, y), c in zip(pts, [TEAL, AMBER, RED]):
        ax.plot(x, y, "o", color=c, ms=4)
    ax.set_xlabel("$i_d$ (A)"); ax.set_ylabel("$i_q$ (A)")
    ax.set_xlim(-900, 650); ax.set_ylim(-150, 700); ax.set_aspect("equal")
    ax.text(250, 620, "current\nlimit circle", fontsize=6.8, color=NAVY)
    save(fig, "fig8_1")


def fig8_2():
    n = np.linspace(200, 16000, 300); T = np.linspace(2, 360, 300)
    N, TT = np.meshgrid(n, T)
    w = N * 2 * np.pi / 60
    Pm = TT * w
    Tmax = np.minimum(350, 150e3 / w)
    I = TT / 350 * 600
    cu = 3 * (I / np.sqrt(2)) ** 2 * 0.02
    f = N * 4 / 60
    Bfac = np.clip(1.0 - 0.45 * np.clip((N - 5000) / 11000, 0, 1), 0.5, 1) * (0.6 + 0.4 * TT / 350)
    fe = 50 * (0.02 * f * (1.4 * Bfac) ** 2 + 2e-5 * f ** 2 * (1.4 * Bfac) ** 2)
    mech = 4e-6 * N ** 2 + 0.01 * N + 150
    eta = Pm / (Pm + cu + fe + mech) * 100
    eta = np.where(TT <= Tmax, eta, np.nan)
    fig, ax = plt.subplots(figsize=(W, 2.9))
    cmap = LinearSegmentedColormap.from_list("ev", ["#e7eef1", "#9fd2d8", TEAL, NAVY])
    levels = [70, 80, 85, 88, 90, 92, 94, 95, 96, 97]
    cf = ax.contourf(N, TT, eta, levels=levels + [99], cmap=cmap, extend="min")
    cs = ax.contour(N, TT, eta, levels=levels, colors="white", linewidths=0.5)
    ax.clabel(cs, fmt="%d", fontsize=6, inline_spacing=2)
    ax.plot(n, np.minimum(350, 150e3 / (n * 2 * np.pi / 60)), color=AMBER, lw=1.8, label="Peak torque envelope")
    pn = rng.normal(7000, 2500, 260); pt = np.abs(rng.normal(35, 30, 260))
    ok = (pn > 300) & (pn < 15500) & (pt < np.minimum(350, 150e3 / (pn * 2 * np.pi / 60)))
    ax.plot(pn[ok], pt[ok], ".", color=RED, ms=2.2, alpha=0.7, label="Drive-cycle operating points")
    ax.set_xlabel("Motor speed (rpm)"); ax.set_ylabel("Torque (N·m)"); ax.grid(False)
    ax.set_xlim(0, 16000); ax.set_ylim(0, 380)
    cb = fig.colorbar(cf, ax=ax, pad=0.02); cb.set_label("Efficiency (%)", fontsize=7.5); cb.ax.tick_params(labelsize=6.5)
    ax.legend(loc="upper right", fontsize=6.5)
    save(fig, "fig8_2")


def fig8_3():
    fig, axs = plt.subplots(1, 2, figsize=(W, 2.2))
    for ax, t in zip(axs, ["(a) Stranded round wire", "(b) Hairpin (4 layers)"]):
        ax.set_xlim(-12, 12); ax.set_ylim(-2, 32); ax.set_aspect("equal"); ax.axis("off")
        ax.set_title(t, fontsize=7.5, color=NAVY, fontweight="semibold")
        ax.add_patch(Polygon([[-12, 30], [12, 30], [12, -1], [1.5, -1], [1.5, 1.5], [-1.5, 1.5], [-1.5, -1], [-12, -1]], fc="#d9e0e4", ec=NAVY, lw=0.8))
        ax.add_patch(Rectangle((-5, 3), 10, 25, fc="white", ec=NAVY, lw=0.8))
        ax.add_patch(Rectangle((-4.7, 3.3), 9.4, 24.4, fc="none", ec=AMBER, lw=0.8))
        ax.text(0, -1.9, "slot opening", fontsize=6, color=GREY, ha="center", va="top")
    a = axs[0]
    for y in np.arange(4.3, 27.3, 1.25):
        for x in np.arange(-3.9, 4.2, 1.25):
            a.add_patch(Circle((x + (0.3 if int(y * 4) % 2 else 0), y), 0.5, fc="#c58a4a", ec="#7a4f22", lw=0.3))
    a.text(7, 15, "fill\n≈ 45 %", fontsize=7, color=NAVY)
    a = axs[1]
    cols = ["#e4a35c", "#d48d45", "#c27a33", "#b06a25"]
    for i, y in enumerate([4, 10, 16, 22]):
        a.add_patch(FancyBboxPatch((-4.2, y), 8.4, 5.4, boxstyle="round,pad=0,rounding_size=0.6", fc=cols[3 - i], ec="#7a4f22", lw=0.5))
    a.text(7, 15, "fill\n≈ 70 %", fontsize=7, color=NAVY)
    a.annotate("highest AC loss", xy=(4.2, 6.5), xytext=(6.2, 3.5), fontsize=6.2, color=RED, arrowprops=dict(arrowstyle="->", color=RED, lw=0.6))
    save(fig, "fig8_3")


def fig8_4():
    t = np.linspace(0, 600, 3000)
    T = np.zeros_like(t); T[0] = 95
    Tm = np.zeros_like(t); Tm[0] = 95
    for i in range(1, len(t)):
        dt = t[i] - t[i - 1]
        on = (t[i] % 75) < 12
        P = (9000 if T[i - 1] < 165 else 3500) if on else 900
        T[i] = T[i - 1] + dt * (P * (1 + 0.0039 * (T[i - 1] - 90)) - (T[i - 1] - 70) * 26) / 3080
        Tm[i] = Tm[i - 1] + dt * (1500 - (Tm[i - 1] - 70) * 26) / 6000
    T = np.where(T > 175, 175 - (T - 175) * 0, T)
    fig, ax = plt.subplots(figsize=(W, 2.3))
    ax.plot(t, T, color=RED, lw=1.2, label="Repeated peak accelerations (track)")
    ax.plot(t, Tm, color=TEAL, lw=1.6, label="Steady motorway, 120 km/h")
    ax.axhline(180, color=NAVY, ls="--", lw=0.8); ax.text(5, 182, "insulation hot-spot limit", fontsize=6.6, color=NAVY)
    ax.axhline(165, color=AMBER, ls=":", lw=0.8); ax.text(5, 158, "derating begins", fontsize=6.6, color=AMBER)
    ax.set_xlabel("Time (s)"); ax.set_ylabel("Winding hot-spot (°C)")
    ax.set_xlim(0, 600); ax.set_ylim(80, 195); ax.legend(loc="lower right", fontsize=6.6)
    save(fig, "fig8_4")


if __name__ == "__main__":
    fig8_1(); fig8_2(); fig8_3(); fig8_4()
