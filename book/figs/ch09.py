from common import *


def fig9_1():
    t = np.linspace(0, 2, 600) * 2 * np.pi
    ia, ib, ic = [np.cos(t - k * 2 * np.pi / 3) for k in range(3)]
    al = 2 / 3 * (ia - 0.5 * ib - 0.5 * ic); be = 2 / 3 * np.sqrt(3) / 2 * (ib - ic)
    th = t - 0.6
    d = al * np.cos(th) + be * np.sin(th); q = -al * np.sin(th) + be * np.cos(th)
    fig, axs = plt.subplots(1, 3, figsize=(W, 1.7), sharey=True)
    x = t / (2 * np.pi) * 360
    for a, (cur, lab, col), ttl in [(axs[0], [(ia, "$i_a$", TEAL), (ib, "$i_b$", AMBER), (ic, "$i_c$", NAVY)], "(a) Phase currents"),
                                    (axs[1], [(al, "$i_\\alpha$", TEAL), (be, "$i_\\beta$", AMBER)], "(b) Clarke: α–β"),
                                    (axs[2], [(d, "$i_d$", TEAL), (q, "$i_q$", AMBER)], "(c) Park: d–q")] if False else []:
        pass
    sets = [([(ia, "$i_a$", TEAL), (ib, "$i_b$", AMBER), (ic, "$i_c$", NAVY)], "(a) Phase currents"),
            ([(al, "$i_\\alpha$", TEAL), (be, "$i_\\beta$", AMBER)], "(b) Clarke: α–β"),
            ([(d, "$i_d$", TEAL), (q, "$i_q$", AMBER)], "(c) Park: d–q")]
    for a, (curves, ttl) in zip(axs, sets):
        for y, lab, col in curves:
            a.plot(x, y, color=col, lw=1.3, label=lab)
        a.set_title(ttl, fontsize=7.3, color=NAVY, fontweight="semibold")
        a.set_xticks([0, 360, 720]); a.set_xlabel("θ (°)", fontsize=7); a.set_ylim(-1.3, 1.5)
        a.legend(loc="upper center", ncol=3, fontsize=6.3, handlelength=1.2, columnspacing=0.8)
    axs[0].set_ylabel("Current (p.u.)")
    fig.subplots_adjust(wspace=0.12)
    save(fig, "fig9_1")


def fig9_2():
    fig, ax = canvas(h=2.7, ylim=(0, 60))
    def b(x, y, w, h, t, **k):
        box(ax, x, y, w, h, t, fs=5.3, **k)
    b(0, 36, 11, 10, "Torque\nrequest")
    b(14, 36, 13, 10, "MTPA /\nfield-weak.\ntables")
    b(31, 44, 9, 7, "PI d", fc="white"); b(31, 31, 9, 7, "PI q", fc="white")
    b(44, 36, 12, 10, "decoupling\n+ feed-\nforward", fc=PALE, ec=AMBER)
    b(60, 36, 10, 10, "inverse\nPark")
    b(73, 36, 11, 10, "SVPWM", fc=NAVY, ec=NAVY, tc="white")
    b(87, 36, 12, 10, "Inverter", fc=NAVY, ec=NAVY, tc="white")
    ax.add_patch(Circle((93, 21), 5.5, fc="white", ec=NAVY, lw=1)); label(ax, 93, 21, "M", fs=9, c=NAVY, fontweight="bold")
    b(79, 4, 11, 7, "resolver", fc="white", ec=GREY)
    b(52, 13, 11, 8, "Clarke +\nPark", fc="white")
    for (x1, y1, x2, y2) in [(11, 41, 14, 41), (27, 43, 31, 47.5), (27, 39, 31, 34.5), (40, 47.5, 44, 43), (40, 34.5, 44, 39),
                             (56, 41, 60, 41), (70, 41, 73, 41), (84, 41, 87, 41)]:
        arrow(ax, x1, y1, x2, y2, c=TEAL, lw=1.1, ms=6)
    arrow(ax, 93, 36, 93, 26.5, c=TEAL, lw=1.6, ms=6)
    label(ax, 95.5, 31, "$i_{abc}$", fs=5.8, c=GREY, ha="left")
    line(ax, [89, 75, 75], [21, 21, 17], c=GREY, lw=0.9); arrow(ax, 75, 17, 63, 17, c=GREY, lw=0.9, ms=5)
    label(ax, 76, 23, "phase currents", fs=5.6, c=GREY)
    line(ax, [93, 93], [15.5, 11], c=GREY, lw=0.9); line(ax, [89, 84.5], [7.5, 7.5], c=GREY, lw=0.9)
    line(ax, [79, 57.5], [7.5, 7.5], c=GREY, lw=0.9, ls="--"); arrow(ax, 57.5, 7.5, 57.5, 13, c=GREY, lw=0.9, ms=5)
    line(ax, [57.5, 65, 65], [7.5, 7.5, 36], c=GREY, lw=0.9, ls="--")
    label(ax, 70, 5, "$\\theta_e$", fs=6.5, c=GREY)
    line(ax, [52, 35.5, 35.5], [17, 17, 31], c=GREY, lw=0.9); arrow(ax, 35.5, 26, 35.5, 31, c=GREY, lw=0.9, ms=5)
    line(ax, [35.5, 28, 28, 35.5], [17, 17, 54, 54], c=GREY, lw=0.9); arrow(ax, 35.5, 54, 35.5, 51, c=GREY, lw=0.9, ms=5)
    label(ax, 42, 19, "measured $i_d$, $i_q$", fs=6, c=GREY)
    label(ax, 20.5, 49, "$i_d^*$, $i_q^*$", fs=6.5, c=TEAL)
    label(ax, 79, 49, "rotating frame → stationary frame", fs=5.6, c=GREY)
    save(fig, "fig9_2")


def fig9_3():
    psi, Ld, Lq, p = 0.08, 0.15e-3, 0.45e-3, 4
    idg = np.linspace(-700, 50, 400)
    fig, ax = plt.subplots(figsize=(W, 2.9))
    for T in (50, 100, 200, 300, 400):
        iq = T / (1.5 * p * (psi + (Ld - Lq) * idg))
        iq = np.where((psi + (Ld - Lq) * idg) > 0, iq, np.nan)
        ax.plot(idg, iq, color="#9fb3bd", lw=0.8)
        k = np.argmin(np.abs(idg + 650)); ax.text(-650, iq[k] + 8, f"{T} N·m", fontsize=6, color=GREY)
    th = np.linspace(0, np.pi, 300); I = 600
    ax.plot(I * np.cos(th), I * np.sin(th), color=NAVY, lw=1.5, label="Current limit")
    iq = np.linspace(0, 600, 200); dL = Lq - Ld
    idm = psi / (2 * dL) - np.sqrt(psi ** 2 / (4 * dL ** 2) + iq ** 2)
    ok = idm ** 2 + iq ** 2 <= I ** 2
    ax.plot(idm[ok], iq[ok], color=TEAL, lw=2, label="MTPA trajectory")
    w = 3000; Vmax = 400 / np.sqrt(3); a = Vmax / (w * Ld); b = Vmax / (w * Lq)
    t2 = np.linspace(0, 2 * np.pi, 400)
    ax.plot(-psi / Ld + a * np.cos(t2), b * np.sin(t2), color=AMBER, lw=1.5, label="Voltage limit at speed ω")
    ax.set_xlabel("$i_d$ (A)"); ax.set_ylabel("$i_q$ (A)")
    ax.set_xlim(-700, 100); ax.set_ylim(0, 650); ax.set_aspect("equal")
    ax.legend(loc="upper right", fontsize=6.5)
    save(fig, "fig9_3")


def fig9_4():
    t = np.linspace(-0.05, 0.6, 1500)
    wn = 2 * np.pi * 9; z = 0.06
    wd = wn * np.sqrt(1 - z ** 2)
    step = np.where(t > 0, 1 - np.exp(-z * wn * t) * (np.cos(wd * t) + z / np.sqrt(1 - z ** 2) * np.sin(wd * t)), 0)
    z2 = 0.75; wd2 = wn * np.sqrt(1 - z2 ** 2)
    damp = np.where(t > 0, 1 - np.exp(-z2 * wn * t) * (np.cos(wd2 * t) + z2 / np.sqrt(1 - z2 ** 2) * np.sin(wd2 * t)), 0)
    fig, ax = plt.subplots(figsize=(W, 2.2))
    ax.plot(t * 1000, np.where(t > 0, 1, 0), color=GREY, lw=0.9, ls="--", label="Torque request")
    ax.plot(t * 1000, step, color=RED, lw=1.3, label="Without active damping")
    ax.plot(t * 1000, damp, color=TEAL, lw=1.8, label="With active damping")
    ax.set_xlabel("Time (ms)"); ax.set_ylabel("Wheel torque (p.u.)")
    ax.set_xlim(-50, 600); ax.set_ylim(-0.1, 2.0); ax.legend(loc="upper right", fontsize=6.6)
    save(fig, "fig9_4")


if __name__ == "__main__":
    fig9_1(); fig9_2(); fig9_3(); fig9_4()
