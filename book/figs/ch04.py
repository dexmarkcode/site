from common import *
import schemdraw
import schemdraw.elements as elm
schemdraw.config(fontsize=8, font="Source Sans 3", lw=1.1, color=NAVY)
rng = np.random.default_rng(4)


def fig4_1():
    fig, ax = canvas(h=2.9, ylim=(0, 64))
    # current collectors
    ax.add_patch(Rectangle((6, 6), 3, 40, fc="#b87333", ec="none"))
    ax.add_patch(Rectangle((91, 6), 3, 40, fc="#b9c2c8", ec="none"))
    label(ax, 7.5, 3, "Cu foil", fs=6.5, c=GREY); label(ax, 92.5, 3, "Al foil", fs=6.5, c=GREY)
    # anode: graphite layers
    ax.add_patch(Rectangle((9, 6), 28, 40, fc="#e7ebee", ec=NAVY, lw=0.6))
    for y in np.arange(9, 45, 4):
        line(ax, [11, 35], [y, y], c="#3d4a51", lw=1.6)
    for y in np.arange(11, 45, 4):
        for x in rng.uniform(13, 33, 2):
            ax.add_patch(Circle((x, y), 0.8, fc=TEAL, ec="none"))
    # separator
    ax.add_patch(Rectangle((47, 6), 3, 40, fc="white", ec=GREY, lw=0.6, hatch="|||"))
    # cathode particles
    ax.add_patch(Rectangle((60, 6), 31, 40, fc=PALE, ec=NAVY, lw=0.6))
    for i in range(14):
        cx, cy = rng.uniform(64, 87), rng.uniform(10, 42)
        ax.add_patch(Circle((cx, cy), 3.2, fc="#e9c58b", ec=AMBER, lw=0.6))
    # ions crossing
    for y in (14, 24, 34):
        arrow(ax, 36, y, 62, y, c=TEAL, lw=1.2)
        ax.add_patch(Circle((44, y), 1.0, fc=TEAL, ec="none"))
        ax.text(44, y + 2.1, "Li⁺", fontsize=6.5, color=TEAL, ha="center")
    label(ax, 23, 49, "Graphite anode (−)", fs=7.2, c=NAVY, fontweight="semibold")
    label(ax, 48.5, 49, "Separator", fs=6.8, c=GREY)
    label(ax, 75.5, 49, "Metal-oxide cathode (+)", fs=7.2, c=NAVY, fontweight="semibold")
    label(ax, 54, 30, "electrolyte", fs=6.3, c=GREY, rotation=90)
    # external circuit
    line(ax, [7.5, 7.5, 40], [46, 58, 58], c=NAVY, lw=1.2)
    line(ax, [60, 92.5, 92.5], [58, 58, 46], c=NAVY, lw=1.2)
    box(ax, 40, 54, 20, 8, "Load", fc=NAVY, ec=NAVY, tc="white", fs=7)
    arrow(ax, 20, 58, 30, 58, c=AMBER, lw=1.4); arrow(ax, 70, 58, 80, 58, c=AMBER, lw=1.4)
    label(ax, 25, 61, "e⁻", fs=7.5, c=AMBER); label(ax, 75, 61, "e⁻", fs=7.5, c=AMBER)
    label(ax, 50, 1.5, "Discharge: ions and electrons both travel from anode to cathode", fs=6.5, c=NAVY)
    save(fig, "fig4_1")


def fig4_2():
    s = np.linspace(0, 1, 300)
    nmc = 3.0 + 0.55 * s + 0.65 * s ** 2 - 0.15 * s ** 3 + 0.25 * (1 - np.exp(-s / 0.03)) - 0.1 * np.exp(-(s - 0.0) / 0.02)
    nmc = 3.0 + (4.2 - 3.0) * (0.12 * (1 - np.exp(-s / 0.04)) + 0.55 * s + 0.33 * s ** 2.2)
    lfp = 2.6 + 0.6 * (1 - np.exp(-s / 0.025)) + 0.12 * s + 0.03 * np.tanh((s - 0.62) / 0.03) + 0.45 * np.exp((s - 1) / 0.018)
    fig, ax = plt.subplots(figsize=(W, 2.4))
    ax.plot(s * 100, nmc, color=TEAL, label="NMC / graphite")
    ax.plot(s * 100, lfp, color=AMBER, label="LFP / graphite")
    ax.axvspan(20, 90, color=AMBER, alpha=0.07)
    ax.text(55, 3.05, "LFP plateau: ~0.1 V across 70 % of SoC", fontsize=6.8, color=AMBER, ha="center")
    ax.set_xlabel("State of charge (%)"); ax.set_ylabel("Open-circuit voltage (V)")
    ax.set_xlim(0, 100); ax.set_ylim(2.5, 4.35); ax.legend(loc="upper left")
    save(fig, "fig4_2")


def fig4_3():
    fig, ax = canvas(h=2.3, ylim=(0, 50))
    # cylindrical
    ax.add_patch(Rectangle((8, 8), 16, 30, fc="#d8dee2", ec=NAVY, lw=0.9))
    from matplotlib.patches import Ellipse
    ax.add_patch(Ellipse((16, 38), 16, 5, fc="#eef1f3", ec=NAVY, lw=0.9))
    ax.add_patch(Ellipse((16, 8), 16, 5, fc="#d8dee2", ec=NAVY, lw=0.9))
    th = np.linspace(0, 6 * np.pi, 300); r = 0.2 + 0.36 * th
    ax.plot(16 + r * np.cos(th) * 0.95, 38 + r * np.sin(th) * 0.3, color=TEAL, lw=0.6)
    ax.add_patch(Rectangle((14.5, 39.5), 3, 2.2, fc=NAVY))
    label(ax, 16, 1.5, "Cylindrical", fs=7.5, c=NAVY, fontweight="semibold")
    # prismatic
    ax.add_patch(Polygon([[36, 8], [62, 8], [66, 12], [66, 40], [40, 40], [36, 36]], fc="#d8dee2", ec=NAVY, lw=0.9))
    line(ax, [36, 62, 62], [36, 36, 8], c=NAVY, lw=0.9); line(ax, [62, 66], [36, 40], c=NAVY, lw=0.9)
    ax.add_patch(Rectangle((41, 37), 4, 2.3, fc=NAVY)); ax.add_patch(Rectangle((54, 37), 4, 2.3, fc=AMBER))
    for y in np.arange(11, 34, 2.4):
        line(ax, [39, 59], [y, y], c=TEAL, lw=0.5)
    label(ax, 50, 1.5, "Prismatic", fs=7.5, c=NAVY, fontweight="semibold")
    # pouch
    ax.add_patch(Polygon([[75, 8], [96, 8], [96, 34], [75, 34]], fc="#e6ecef", ec=NAVY, lw=0.9))
    ax.add_patch(Rectangle((77, 10), 17, 22, fc="#d3dadf", ec=GREY, lw=0.5))
    ax.add_patch(Rectangle((78.5, 34), 4, 6, fc=NAVY)); ax.add_patch(Rectangle((88.5, 34), 4, 6, fc=AMBER))
    for y in np.arange(12, 31, 2.2):
        line(ax, [78, 93], [y, y], c=TEAL, lw=0.5)
    label(ax, 85.5, 1.5, "Pouch", fs=7.5, c=NAVY, fontweight="semibold")
    label(ax, 16, 45, "jelly roll in steel can", fs=6.3, c=GREY)
    label(ax, 51, 45, "rigid aluminium case", fs=6.3, c=GREY)
    label(ax, 85.5, 45, "laminated foil", fs=6.3, c=GREY)
    save(fig, "fig4_3")


def fig4_4():
    fig = plt.figure(figsize=(W, 2.3))
    ax1 = fig.add_axes([0.0, 0.1, 0.48, 0.8]); ax2 = fig.add_axes([0.6, 0.2, 0.39, 0.7])
    d = schemdraw.Drawing(canvas=ax1, show=False)
    src = d.add(elm.SourceV().up().label("$V_{OCV}$", loc="left"))
    d.add(elm.Resistor().right(1.8).label("$R_0$"))
    d.add(elm.RBox().right(1.8).label("$R_1 \\| C_1$"))
    d.add(elm.RBox().right(1.8).label("$R_2 \\| C_2$"))
    d.add(elm.Line().right(0.6))
    d.add(elm.Dot(open=True).label("+", loc="right"))
    d.add(elm.Gap().down().label("$V_t$", loc="right", ofst=0.3))
    d.add(elm.Dot(open=True).label("−", loc="right"))
    d.add(elm.Line().tox(src.start))
    d.draw(show=False); ax1.axis("off"); ax1.set_aspect("equal")
    ax1.text(0.0, 1.02, "(a)", transform=ax1.transAxes, fontsize=8, color=NAVY, fontweight="bold")
    t = np.linspace(-5, 40, 900)
    I = np.where((t >= 0) & (t < 10), 1, 0)
    V = np.full_like(t, 3.70)
    on = (t >= 0) & (t < 10)
    V[on] = 3.70 - 0.24 - 0.16 * (1 - np.exp(-t[on] / 20))
    v10 = 0.16 * (1 - np.exp(-0.5))
    off = t >= 10
    V[off] = 3.70 - v10 * np.exp(-(t[off] - 10) / 20)
    ax2.plot(t, V, color=TEAL)
    ax2.set_xlabel("Time (s)"); ax2.set_ylabel("Terminal voltage (V)")
    ax2.annotate("$IR_0$ step", xy=(0.3, 3.47), xytext=(12, 3.5), fontsize=6.8, color=NAVY, arrowprops=dict(arrowstyle="->", color=NAVY, lw=0.6))
    ax2.annotate("RC sag", xy=(8, 3.405), xytext=(13, 3.40), fontsize=6.8, color=NAVY, arrowprops=dict(arrowstyle="->", color=NAVY, lw=0.6))
    ax2.text(24, 3.62, "recovery", fontsize=6.8, color=NAVY)
    ax2.axvspan(0, 10, color=AMBER, alpha=0.1); ax2.text(5, 3.72, "pulse", fontsize=6.5, color=AMBER, ha="center")
    ax2.set_ylim(3.35, 3.75)
    ax2.text(-0.3, 1.05, "(b)", transform=ax2.transAxes, fontsize=8, color=NAVY, fontweight="bold")
    save(fig, "fig4_4")


def fig4_5():
    n = np.linspace(0, 2500, 300)
    fig, ax = plt.subplots(figsize=(W, 2.4))
    def fade(a, b, knee=None, kr=0):
        f = 100 - a * np.sqrt(n / 100) - b * n / 100
        if knee:
            f -= np.where(n > knee, kr * ((n - knee) / 100) ** 2, 0)
        return f
    ax.plot(n, fade(1.2, 0.25), color=TEAL, label="25 °C, 20–80 % SoC window")
    ax.plot(n, fade(1.8, 0.45), color=NAVY, label="25 °C, 0–100 % SoC")
    ax.plot(n, fade(2.8, 0.6), color=AMBER, label="40 °C, 0–100 % SoC")
    ax.plot(n, fade(2.0, 0.5, 900, 0.35), color=RED, ls="--", label="fast charge at 5 °C (plating)")
    ax.axhline(70, color=GREY, lw=0.8, ls=":"); ax.text(2480, 71, "typical warranty threshold (70 %)", fontsize=6.5, color=GREY, ha="right")
    ax.annotate("knee", xy=(1350, 77), xytext=(1550, 88), fontsize=7, color=RED, arrowprops=dict(arrowstyle="->", color=RED, lw=0.7))
    ax.set_xlabel("Equivalent full cycles"); ax.set_ylabel("Capacity retained (%)")
    ax.set_ylim(55, 101); ax.set_xlim(0, 2500); ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=6.8)
    save(fig, "fig4_5")


if __name__ == "__main__":
    fig4_1(); fig4_2(); fig4_3(); fig4_4(); fig4_5()
