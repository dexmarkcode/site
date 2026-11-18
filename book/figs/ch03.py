from common import *
import schemdraw
import schemdraw.elements as elm

schemdraw.config(fontsize=8, font="Source Sans 3", lw=1.1, color=NAVY)


def schem_on(ax, build):
    d = schemdraw.Drawing(canvas=ax, show=False)
    build(d)
    d.draw(show=False)
    ax.set_aspect("equal"); ax.axis("off")


def fig3_1():
    fig = plt.figure(figsize=(W, 2.3))
    ax1 = fig.add_axes([0.0, 0.0, 0.52, 1.0])
    ax2 = fig.add_axes([0.66, 0.2, 0.33, 0.7])

    def b(d):
        bat = d.add(elm.BatteryCell().up().at((0, 0)).label("$V_{batt}$", loc="left"))
        d.add(elm.Line().up(0.5).at(bat.end))
        d.add(elm.Line().right(0.8))
        A = d.add(elm.Dot())
        d.add(elm.Switch().right(2.4).label("main +", loc="bottom", fontsize=7))
        B = d.add(elm.Dot())
        d.add(elm.Line().up(1.4).at(A.center))
        d.add(elm.Switch().right(1.2).label("pre-charge", loc="top", fontsize=7))
        d.add(elm.Resistor().right(1.2).label("R", loc="top"))
        d.add(elm.Line().down(1.4))
        d.add(elm.Line().right(1.4).at(B.center))
        cap = d.add(elm.Capacitor().down(3.5).label("$C_{DC}$", loc="bottom", ofst=0.25))
        d.add(elm.Switch().left(2.4).label("main −", loc="bottom", fontsize=7))
        d.add(elm.Line().tox(bat.start))
        d.add(elm.Line().toy(bat.start))
    schem_on(ax1, b)
    ax1.text(0.02, 0.97, "(a)", transform=ax1.transAxes, fontsize=8, color=NAVY, fontweight="bold", va="top")
    t = np.linspace(0, 0.5, 300); tau = 0.1
    ax2.plot(t * 1000, 400 * (1 - np.exp(-t / tau)), color=TEAL)
    ax2.axhline(380, color=AMBER, ls="--", lw=0.8); ax2.axvline(300, color=GREY, ls=":", lw=0.8)
    ax2.text(310, 250, "main contactor\ncloses at 95 %", fontsize=6.5, color=NAVY)
    ax2.text(100, 150, "τ = RC", fontsize=7, color=TEAL)
    ax2.set_xlabel("Time (ms)"); ax2.set_ylabel("DC-link voltage (V)"); ax2.set_ylim(0, 430)
    ax2.text(-0.32, 1.12, "(b)", transform=ax2.transAxes, fontsize=8, color=NAVY, fontweight="bold")
    save(fig, "fig3_1")


def fig3_2():
    fig = plt.figure(figsize=(W, 2.1))
    ax1 = fig.add_axes([0.07, 0.2, 0.55, 0.72]); ax2 = fig.add_axes([0.68, 0.05, 0.31, 0.9])
    th = np.linspace(0, 4 * np.pi, 500)
    cols = [TEAL, AMBER, NAVY]; names = ["$v_a$", "$v_b$", "$v_c$"]
    for k in range(3):
        ax1.plot(np.degrees(th), np.sin(th - k * 2 * np.pi / 3), color=cols[k], label=names[k])
    ax1.set_xlim(0, 720); ax1.set_xticks([0, 120, 240, 360, 480, 600, 720]); ax1.set_ylim(-1.25, 1.35)
    ax1.set_xlabel("Electrical angle (°)"); ax1.set_ylabel("Voltage (p.u.)")
    ax1.legend(ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.18))
    ax1.text(-0.13, 1.1, "(a)", transform=ax1.transAxes, fontsize=8, color=NAVY, fontweight="bold")
    ax2.set_xlim(-1.4, 1.4); ax2.set_ylim(-1.4, 1.4); ax2.set_aspect("equal"); ax2.axis("off")
    ax2.add_patch(Circle((0, 0), 1, fill=False, ec="#d2dbe0", lw=0.6, ls="--"))
    for k in range(3):
        a = np.pi / 2 - k * 2 * np.pi / 3
        arrow(ax2, 0, 0, np.cos(a), np.sin(a), c=cols[k], lw=1.6)
        ax2.text(1.22 * np.cos(a), 1.22 * np.sin(a), names[k].replace("v", "V"), color=cols[k], ha="center", va="center", fontsize=9)
    a1, a2 = np.pi / 2, np.pi / 2 - 2 * np.pi / 3
    arrow(ax2, np.cos(a2), np.sin(a2), np.cos(a1), np.sin(a1), c=GREY, lw=1, ls="--")
    ax2.text(0.75, 0.25, "$V_{ab}=\\sqrt{3}\\,V$", fontsize=7, color=GREY)
    ax2.add_patch(Arc((0, 0), 0.6, 0.6, theta1=-30, theta2=90, color=NAVY, lw=0.6))
    ax2.text(0.32, 0.38, "120°", fontsize=6.5, color=NAVY)
    ax2.text(-1.4, 1.3, "(b)", fontsize=8, color=NAVY, fontweight="bold")
    save(fig, "fig3_2")


def fig3_3():
    fig = plt.figure(figsize=(W, 2.4))
    ax1 = fig.add_axes([0.0, 0.05, 0.5, 0.9]); ax2 = fig.add_axes([0.6, 0.55, 0.39, 0.38]); ax3 = fig.add_axes([0.6, 0.12, 0.39, 0.38])

    def b(d):
        src = d.add(elm.SourceV().up().label("$V_{in}$", loc="left"))
        d.add(elm.Switch().right().label("S", loc="top"))
        node = d.add(elm.Dot())
        d.push()
        d.add(elm.Diode().down().reverse().label("D", loc="bottom"))
        d.pop()
        d.add(elm.Inductor2().right().label("L", loc="top"))
        d.add(elm.Dot())
        d.push(); d.add(elm.Capacitor().down().label("C", loc="bottom")); d.pop()
        d.add(elm.Line().right(1.4))
        d.add(elm.Resistor().down().label("load", loc="bottom"))
        d.add(elm.Line().tox(src.start))
        d.add(elm.Label().at((node.center[0], node.center[1] + 0.9)).label("switch\nnode", fontsize=6.5, color=GREY))
    schem_on(ax1, b)
    ax1.text(0.0, 0.98, "(a)", transform=ax1.transAxes, fontsize=8, color=NAVY, fontweight="bold", va="top")
    t = np.linspace(0, 3, 900); D = 0.4
    vsw = np.where((t % 1) < D, 1, 0)
    ax2.plot(t, vsw, color=NAVY, lw=1.1); ax2.axhline(D, color=AMBER, ls="--", lw=0.9)
    ax2.text(3.02, D, " average\n = $DV_{in}$", fontsize=6.3, color=AMBER, va="center")
    ax2.set_yticks([0, 1]); ax2.set_yticklabels(["0", "$V_{in}$"]); ax2.set_xticks([]); ax2.set_ylim(-0.15, 1.25)
    ax2.set_ylabel("$v_{sw}$", fontsize=8)
    ax2.text(-0.25, 1.05, "(b)", transform=ax2.transAxes, fontsize=8, color=NAVY, fontweight="bold")
    ph = t % 1
    il = np.where(ph < D, -0.5 + ph / D, 0.5 - (ph - D) / (1 - D)) * 0.3 + 1
    ax3.plot(t, il, color=TEAL); ax3.axhline(1, color=GREY, ls=":", lw=0.8)
    ax3.set_yticks([1]); ax3.set_yticklabels(["$I_{load}$"]); ax3.set_xticks([0, 1, 2, 3]); ax3.set_xticklabels(["0", "$T_s$", "$2T_s$", "$3T_s$"])
    ax3.set_ylabel("$i_L$", fontsize=8); ax3.set_ylim(0.7, 1.3)
    save(fig, "fig3_3")


def fig3_4():
    fig, ax = canvas(h=2.5, ylim=(0, 56))
    # chassis bar
    ax.add_patch(Rectangle((3, 3), 94, 4, fc="#d9e1e5", ec=GREY, lw=0.7))
    label(ax, 50, 5, "vehicle chassis (protective earth)", fs=6.8, c=NAVY)
    # battery
    box(ax, 6, 22, 18, 24, "Traction\nbattery", fc="white", ec=TEAL, fs=7.5)
    label(ax, 28, 46.5, "HV +", fs=6.5, c=RED); label(ax, 28, 21.5, "HV −", fs=6.5, c=NAVY)
    line(ax, [24, 70], [44, 44], c=RED, lw=2); line(ax, [24, 70], [24, 24], c=NAVY, lw=2)
    box(ax, 70, 20, 22, 28, "Inverter /\nloads", fs=7.5)
    # isolation resistors (as zigzags)
    def zig(x, y1, y2, c):
        ys = np.linspace(y1, y2, 11)
        xs = [x] + [x + (1.4 if i % 2 else -1.4) for i in range(1, 10)] + [x]
        ax.plot(xs, ys, color=c, lw=1)
    line(ax, [38, 38], [44, 36], c=GREY); zig(38, 36, 28, GREY); line(ax, [38, 38], [28, 26], c=GREY)
    ax.text(40.5, 32, "$R_{iso+}$", fontsize=7.5, color=GREY)
    # dashed down to chassis
    line(ax, [38, 38], [26, 7], c=GREY, ls=(0, (2, 2)))
    line(ax, [50, 50], [24, 18], c=GREY); zig(50, 18, 10, GREY); line(ax, [50, 50], [10, 7], c=GREY)
    ax.text(52.5, 13, "$R_{iso-}$", fontsize=7.5, color=GREY)
    box(ax, 56, 30, 12, 8, "IMD", fs=7, fc=PALE, ec=AMBER)
    line(ax, [62, 62], [38, 44], c=AMBER, lw=0.8); line(ax, [62, 62], [30, 24], c=AMBER, lw=0.8)
    line(ax, [68, 69], [34, 34], c=AMBER, lw=0.8)
    # bonding
    for x in (15, 81):
        line(ax, [x, x], [22 if x == 15 else 20, 7], c=GREEN, lw=1.2)
    label(ax, 88, 13, "bonding", fs=6.5, c=GREEN)
    label(ax, 47, 50.5, "floating HV system: no intentional connection to chassis", fs=6.8, c=NAVY)
    save(fig, "fig3_4")


if __name__ == "__main__":
    fig3_1(); fig3_2(); fig3_3(); fig3_4()
