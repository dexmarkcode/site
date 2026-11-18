from common import *
import math


def fig2_1():
    fig, ax = canvas(h=2.7, ylim=(0, 60))
    th = math.radians(14)
    # slope
    x0, y0, L = 5, 6, 92
    ax.add_patch(Polygon([[x0, y0], [x0 + L, y0], [x0 + L, y0 + L * math.tan(th)]], fc="#e9eef1", ec=GREY, lw=0.8))
    ax.add_patch(Arc((x0, y0), 30, 30, theta1=0, theta2=14, color=NAVY, lw=0.8))
    label(ax, x0 + 18, y0 + 2.2, "θ", fs=9, c=NAVY)
    # car body along slope
    def P(s, h):  # point at distance s along slope, height h normal
        return (x0 + s * math.cos(th) - h * math.sin(th), y0 + s * math.sin(th) + h * math.cos(th))
    body = [P(29, 3.2), P(68, 3.2), P(69, 9), P(62, 10.5), P(55, 17), P(35, 17), P(29, 12)]
    ax.add_patch(Polygon(body, fc=TEAL, ec=NAVY, lw=0.9, alpha=0.9))
    for s in (37, 60):
        c = P(s, 3.0)
        ax.add_patch(Circle(c, 3.0, fc=NAVY, ec="white", lw=0.8))
    cg = P(48, 9)
    ax.add_patch(Circle(cg, 1.2, fc="white", ec=NAVY, lw=0.8))
    ux, uy = math.cos(th), math.sin(th)
    # weight
    arrow(ax, cg[0], cg[1], cg[0], cg[1] - 16, c=NAVY, lw=1.4)
    label(ax, cg[0] + 2.5, cg[1] - 14, "mg", fs=8, c=NAVY, ha="left", style="italic")
    # grade component
    arrow(ax, cg[0], cg[1], cg[0] - 13 * ux, cg[1] - 13 * uy, c=RED, lw=1.4)
    label(ax, cg[0] - 15 * ux - 2, cg[1] - 13 * uy + 3, "mg sin θ", fs=7.5, c=RED, style="italic")
    # tractive at wheel
    w = P(37, 0)
    arrow(ax, w[0], w[1], w[0] + 15 * ux, w[1] + 15 * uy, c=TEAL, lw=2)
    label(ax, w[0] + 13 * ux + 2, w[1] + 13 * uy + 3.5, "$F_t$", fs=9, c=TEAL)
    # aero drag at front
    f = P(66, 9)
    arrow(ax, f[0] + 14 * ux, f[1] + 14 * uy, f[0] + 1 * ux, f[1] + 1 * uy, c=AMBER, lw=1.6)
    label(ax, f[0] + 16 * ux, f[1] + 14 * uy + 3, "$F_{aero}$", fs=9, c=AMBER)
    # rolling at rear wheel
    w2 = P(60, 0)
    arrow(ax, w2[0] + 1, w2[1] - 4, w2[0] - 9 * ux + 1, w2[1] - 9 * uy - 4, c=GREY, lw=1.3)
    label(ax, w2[0] + 3, w2[1] - 8, "$F_{roll}$", fs=8.5, c=GREY)
    # direction of travel
    s = P(70, 26)
    arrow(ax, s[0], s[1], s[0] + 10 * ux, s[1] + 10 * uy, c=NAVY, lw=1, ls="--")
    label(ax, s[0] - 2, s[1] + 5, "direction of travel, v", fs=7, c=NAVY)
    save(fig, "fig2_1")


def fig2_2():
    m, crr, cda, rho = 1900, 0.009, 0.62, 1.2
    v = np.linspace(0, 160, 200) / 3.6
    pr = crr * m * 9.81 * v / 1000
    pa = 0.5 * rho * cda * v ** 3 / 1000
    fig, ax = plt.subplots(figsize=(W, 2.5))
    kmh = v * 3.6
    ax.fill_between(kmh, 0, pr, color=GREY, alpha=0.55, lw=0, label="Rolling resistance")
    ax.fill_between(kmh, pr, pr + pa, color=TEAL, alpha=0.75, lw=0, label="Aerodynamic drag")
    ax.plot(kmh, pr + pa, color=NAVY, lw=1.4, label="Total road-load power")
    ax.set_xlabel("Vehicle speed (km/h)"); ax.set_ylabel("Power at the wheels (kW)")
    ax.set_xlim(0, 160); ax.set_ylim(0, 40)
    vx = math.sqrt(crr * m * 9.81 / (0.5 * rho * cda)) * 3.6
    ax.axvline(vx, color=AMBER, lw=0.9, ls="--")
    ax.text(vx + 2, 30, f"drag = rolling\nat {vx:.0f} km/h", fontsize=7, color=AMBER)
    for s in (100, 130):
        vv = s / 3.6; p = (crr * m * 9.81 * vv + 0.5 * rho * cda * vv ** 3) / 1000
        ax.plot(s, p, "o", color=NAVY, ms=3.5); ax.text(s - 3, p + 1.5, f"{p:.1f} kW", fontsize=7, color=NAVY, ha="right")
    ax.legend(loc="upper left")
    save(fig, "fig2_2")


def wltc_sketch():
    # simplified: list of micro-trips (accel, cruise, decel) per phase to approximate shape
    phases = [("Low", 589, [(0, 18, 25), (20, 30, 30), (30, 56.5, 40), (10, 25, 25), (15, 35, 30), (0, 47, 35)]),
              ("Medium", 433, [(0, 50, 45), (20, 76.6, 60), (0, 55, 50), (30, 70, 55), (0, 40, 30)]),
              ("High", 455, [(0, 60, 50), (30, 97.4, 90), (40, 80, 70), (0, 70, 45)]),
              ("Extra High", 323, [(0, 90, 70), (100, 131.3, 120), (60, 110, 60)])]
    t, v = [], []
    T = 0
    for name, dur, trips in phases:
        n = len(trips); seg = dur / n
        for (vs, vp, hold) in trips:
            tt = np.linspace(0, seg, int(seg))
            idle = 0.15 * seg if vs == 0 else 0
            prof = []
            for x in tt:
                if x < idle:
                    prof.append(0)
                else:
                    r = (x - idle) / (seg - idle)
                    prof.append(vp * np.sin(np.pi * r) ** 1.3 * (0.92 + 0.08 * np.sin(9 * np.pi * r)))
            t.extend(T + tt); v.extend(prof); T += seg
    return np.array(t), np.array(v), phases


def fig2_3():
    t, v, phases = wltc_sketch()
    fig, ax = plt.subplots(figsize=(W, 2.2))
    ax.plot(t, v, color=TEAL, lw=1.1)
    ax.fill_between(t, 0, v, color=TEAL, alpha=0.12, lw=0)
    T = 0
    cols = ["#f4f8f9", "white"]
    for i, (name, dur, trips) in enumerate(phases):
        ax.axvspan(T, T + dur, color=cols[i % 2], zorder=-1)
        ax.text(T + dur / 2, 140, name, ha="center", fontsize=7.2, color=NAVY, fontweight="semibold")
        ax.text(T + dur / 2, 131 if name != "Extra High" else 117, f"{dur} s", ha="center", fontsize=6.5, color=GREY)
        if i:
            ax.axvline(T, color=GREY, lw=0.6, ls=":")
        T += dur
    ax.set_xlim(0, 1800); ax.set_ylim(0, 150)
    ax.set_xlabel("Time (s)"); ax.set_ylabel("Speed (km/h)")
    save(fig, "fig2_3")


def fig2_4():
    m, crr, cda, rho = 1900, 0.009, 0.62, 1.2
    T, P, G, r, e = 350, 160e3, 9.0, 0.34, 0.95
    v = np.linspace(0.1, 230, 400) / 3.6
    Fmax = T * G * e / r
    F = np.minimum(Fmax, P * e / v)
    vmax = 16000 * 2 * np.pi / 60 * r / G
    F = np.where(v <= vmax, F, np.nan)
    fig, ax = plt.subplots(figsize=(W, 2.6))
    kmh = v * 3.6
    ax.plot(kmh, F / 1000, color=NAVY, lw=2, label="Peak tractive effort")
    ax.plot(kmh, np.where(v <= vmax, np.minimum(0.55 * Fmax, 0.5 * P * e / v), np.nan) / 1000, color=NAVY, lw=1.2, ls="--", label="Continuous rating (≈50 %)")
    for gpc, c in [(0, TEAL), (6, AMBER), (12, RED), (20, GREY)]:
        th = math.atan(gpc / 100)
        RL = crr * m * 9.81 * math.cos(th) + m * 9.81 * math.sin(th) + 0.5 * rho * cda * v ** 2
        ax.plot(kmh, RL / 1000, color=c, lw=1.2)
        ax.text(205 if gpc < 12 else 150, RL[340 if gpc < 12 else 260] / 1000 + 0.25, f"{gpc} %", color=c, fontsize=7, fontweight="semibold")
    vb = P * e / Fmax * 3.6
    ax.axvline(vb, color=GREY, lw=0.6, ls=":")
    ax.text(vb + 2, 9.4, "base speed", fontsize=6.8, color=GREY)
    ax.text(15, 9.4, "constant torque", fontsize=6.8, color=NAVY)
    ax.text(100, 6.2, "constant power", fontsize=6.8, color=NAVY)
    ax.set_xlabel("Vehicle speed (km/h)"); ax.set_ylabel("Force at the wheels (kN)")
    ax.set_xlim(0, 235); ax.set_ylim(0, 10.5)
    ax.legend(loc="upper right", bbox_to_anchor=(1, 0.88))
    save(fig, "fig2_4")


def fig2_5():
    m, crr, cda = 1900, 0.009, 0.62
    v = np.linspace(20, 140, 100)
    fig, ax = plt.subplots(figsize=(W, 2.5))
    for T, rho, crrf, aux, c, lab in [(20, 1.2, 1.0, 0.4, TEAL, "+20 °C, mild"), (0, 1.29, 1.05, 2.0, AMBER, "0 °C, heater on"),
                                      (-10, 1.34, 1.10, 3.2, NAVY, "−10 °C, heater on")]:
        vs = v / 3.6
        F = crr * crrf * m * 9.81 + 0.5 * rho * cda * vs ** 2
        E = F * 100000 / 3.6e6 / 0.88 + aux * 100 / v
        usable = 75 * (1 if T > 10 else (0.95 if T == 0 else 0.9))
        ax.plot(v, usable / E * 100, color=c, lw=1.8, label=lab)
    ax.set_xlabel("Steady speed (km/h)"); ax.set_ylabel("Range (km)")
    ax.set_xlim(20, 140); ax.set_ylim(0, 800)
    ax.legend(loc="upper right")
    save(fig, "fig2_5")


if __name__ == "__main__":
    fig2_1(); fig2_2(); fig2_3(); fig2_4(); fig2_5()
