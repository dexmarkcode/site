from common import *
import schemdraw
import schemdraw.elements as elm
schemdraw.config(fontsize=8, font="Source Sans 3", lw=1.1, color=NAVY)
rng = np.random.default_rng(6)


def fig6_1():
    t = np.linspace(0, 48, 2000)
    # true SoC: driving events and charging
    true = np.full_like(t, 80.0)
    s = 80.0
    for i in range(1, len(t)):
        h = t[i] % 24; dt = t[i] - t[i - 1]
        rate = 0
        if 8 <= h < 9 or 17 <= h < 18:
            rate = -14
        elif 1 <= h < 5:
            rate = 9
        s = min(95, s + rate * dt); true[i] = s
    cc = true - 6 - 0.3 / 150 * 100 * t  # offset drift
    ekf = true - 6 * np.exp(-t / 0.35) + 0.6 * np.sin(t * 1.3) * np.exp(-t / 30) + rng.normal(0, 0.15, len(t))
    fig, ax = plt.subplots(figsize=(W, 2.4))
    ax.plot(t, true, color=NAVY, lw=1.6, label="True SoC")
    ax.plot(t, cc, color=AMBER, lw=1.3, ls="--", label="Coulomb counting only")
    ax.plot(t, ekf, color=TEAL, lw=1.1, label="Model-based filter (EKF)")
    ax.set_xlabel("Time (h)"); ax.set_ylabel("State of charge (%)")
    ax.set_xlim(0, 48); ax.set_ylim(40, 115); ax.set_xticks(range(0, 49, 6))
    ax.legend(loc="upper center", ncol=3, fontsize=6.8)
    save(fig, "fig6_1")


def fig6_2():
    v = np.linspace(3.35, 4.15, 400)
    def peaks(sc, sh):
        g = lambda m, s, a: a * np.exp(-((v - m - sh) / s) ** 2)
        return sc * (g(3.48, 0.025, 160) + g(3.62, 0.04, 95) + g(3.92, 0.05, 70) + g(4.05, 0.03, 40)) + 15
    fig, ax = plt.subplots(figsize=(W, 2.3))
    ax.plot(v, peaks(1, 0), color=TEAL, label="New cell")
    ax.plot(v, peaks(0.72, 0.03), color=AMBER, label="Aged cell (≈ 82 % SoH)")
    ax.annotate("peak shrinks:\nloss of active material", xy=(3.51, 128), xytext=(3.62, 155), fontsize=6.6, color=NAVY,
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=0.6))
    ax.annotate("peak shifts:\nloss of lithium inventory", xy=(3.95, 66), xytext=(3.98, 110), fontsize=6.6, color=NAVY,
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=0.6))
    ax.set_xlabel("Cell voltage (V)"); ax.set_ylabel("dQ/dV (Ah/V)")
    ax.set_ylim(0, 190); ax.legend(loc="upper right")
    save(fig, "fig6_2")


def fig6_3():
    T = np.linspace(-30, 60, 300)
    dis = np.clip(260 * (1 / (1 + np.exp(-(T + 5) / 7))), 15, None)
    dis = np.where(T > 45, dis * np.clip(1 - (T - 45) / 20, 0.15, 1), dis)
    reg = np.clip(140 * (1 / (1 + np.exp(-(T - 12) / 6))), 2, None)
    reg = np.where(T > 45, reg * np.clip(1 - (T - 45) / 15, 0, 1), reg)
    fig, ax = plt.subplots(figsize=(W, 2.3))
    ax.plot(T, dis, color=TEAL, label="Discharge limit (10 s)")
    ax.plot(T, reg, color=AMBER, label="Regenerative / charge limit (10 s)")
    ax.axvspan(15, 35, color=GREEN, alpha=0.08); ax.text(25, 275, "preferred range", fontsize=6.6, color=GREEN, ha="center")
    ax.set_xlabel("Cell temperature (°C)"); ax.set_ylabel("Pack power limit (kW)")
    ax.set_xlim(-30, 60); ax.set_ylim(0, 290); ax.legend(loc="upper left")
    save(fig, "fig6_3")


def fig6_4():
    fig = plt.figure(figsize=(W, 2.2))
    ax1 = fig.add_axes([0.0, 0.0, 0.46, 0.92]); ax2 = fig.add_axes([0.52, 0.0, 0.46, 0.92])
    d = schemdraw.Drawing(canvas=ax1, show=False)
    c1 = d.add(elm.BatteryCell().up().label("cell n", loc="left"))
    d.add(elm.Line().right(1.2)); d.add(elm.Resistor().down(1.5).label("$R_{bal}$", loc="bottom"))
    d.add(elm.Switch().down(1.5).label("S", loc="bottom"))
    d.add(elm.Line().tox(c1.start))
    d.add(elm.Arrow().at((2.1, 2.6)).down(1.6).color(AMBER).label("heat", loc="bottom", color=AMBER, fontsize=7))
    d.draw(show=False); ax1.axis("off"); ax1.set_aspect("equal")
    ax1.text(0.0, 1.0, "(a) Passive", transform=ax1.transAxes, fontsize=8, color=NAVY, fontweight="bold")
    d = schemdraw.Drawing(canvas=ax2, show=False)
    a = d.add(elm.BatteryCell().up())
    b = d.add(elm.BatteryCell().up())
    d.add(elm.Label().at((-1.3, 1.5)).label("cell n+1", fontsize=7.5))
    d.add(elm.Label().at((-1.3, 4.5)).label("cell n", fontsize=7.5))
    d.add(elm.Line().right(1.2))
    d.add(elm.Switch().down().label("S1", loc="bottom"))
    mid = d.add(elm.Dot())
    d.add(elm.Switch().down().label("S2", loc="bottom"))
    d.add(elm.Line().tox(a.start))
    d.add(elm.Inductor2().at(mid.center).left().tox(a.end).label("L", loc="bottom"))
    d.draw(show=False); ax2.axis("off"); ax2.set_aspect("equal")
    ax2.text(0.0, 1.0, "(b) Active (inductive)", transform=ax2.transAxes, fontsize=8, color=NAVY, fontweight="bold")
    save(fig, "fig6_4")


def fig6_5():
    s = np.linspace(5, 100, 400)
    p = np.piecewise(s, [s < 10, (s >= 10) & (s < 40), (s >= 40) & (s < 60), (s >= 60) & (s < 80), s >= 80],
                     [lambda x: 120 + (x - 5) * 22, 230, lambda x: 230 - (x - 40) * 3, lambda x: 170 - (x - 60) * 3, lambda x: 110 * np.exp(-(x - 80) / 9)])
    p = np.convolve(p, np.ones(9) / 9, mode="same")
    p[:5] = p[5]
    fig, ax = plt.subplots(figsize=(W, 2.3))
    ax.plot(s, p, color=TEAL, lw=1.8, label="Warm battery (25–30 °C)")
    ax.plot(s, np.minimum(p, 120 + 0.9 * s), color=NAVY, lw=1.2, ls="--", label="Cold battery, no preconditioning")
    ax.axvspan(10, 80, color=AMBER, alpha=0.07); ax.text(45, 20, "10–80 % window", fontsize=6.8, color=AMBER, ha="center")
    ax.set_xlabel("State of charge (%)"); ax.set_ylabel("Charging power (kW)")
    ax.set_xlim(5, 100); ax.set_ylim(0, 260); ax.legend(loc="upper right")
    save(fig, "fig6_5")


if __name__ == "__main__":
    fig6_1(); fig6_2(); fig6_3(); fig6_4(); fig6_5()
