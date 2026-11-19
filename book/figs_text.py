"""Illustrations used in the teaching sections of each chapter."""
import math
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm
from lib import ladder, bridge, star_delta, E, FIGDIR, save
import os

NAVY = "#1F3A5F"
COPPER = "#B5651D"
GREY = "#8A8F98"
SAGE = "#4F7A5A"

plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#444", "axes.linewidth": 0.8, "lines.linewidth": 1.8})


def savefig(fig, name):
    fig.savefig(os.path.join(FIGDIR, name + ".svg"), bbox_inches="tight")
    fig.savefig(os.path.join(FIGDIR, name + ".png"), dpi=170, bbox_inches="tight")
    plt.close(fig)


def vi_curves():
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    v = np.linspace(0, 12, 200)
    ax.plot(v, v / 100 * 1000, color=NAVY, label="100 Ω resistor (linear)")
    ax.plot(v, 120 * np.sqrt(v / 12), color=COPPER, label="filament lamp (non-linear)")
    ax.set_xlabel("Voltage $V$ (V)")
    ax.set_ylabel("Current $I$ (mA)")
    ax.legend(frameon=False)
    ax.grid(alpha=0.25)
    savefig(fig, "t01_vi")


def text_circuits():
    ladder("t01_basic", E("V", "V", "12 V"), [("S", E("R", "R", "100 Ω", cur="I")), ("P", E("Lamp", None, None))])
    ladder("t02_series", E("V", "V_s", "24 V"), [("S", E("R", "R_1", "2 kΩ")), ("S", E("R", "R_2", "4 kΩ")), ("P", E("R", "R_3", "6 kΩ"))])
    ladder("t02_parallel", E("V", "V_s", "12 V"), [("P", E("R", "R_1", "6 Ω")), ("P", E("R", "R_2", "12 Ω")), ("P", E("R", "R_3", "4 Ω"))])
    ladder("t02_divider", E("V", "V_in", "12 V"), [("S", E("R", "R_1", "10 kΩ")), ("P", E("R", "R_2", "4.7 kΩ", node="$V_{\\mathrm{out}}$"))])
    bridge("t02_bridge", E("V", "V_s", "V"), E("R", "R_1"), E("R", "R_2"), E("R", "R_3"), E("R", "R_x"), mid=E("G"))
    ladder("t03_tnet", E("V", "V_1", "12 V"), [("S", E("R", "R_1", "2 Ω", cur="I_1")), ("P", E("R", "R_2", "4 Ω", node="A", cur="I_2")), ("S", E("R", "R_3", "4 Ω", cur="I_3")), ("P", E("V", "V_2", "6 V"))])
    ladder("t04_nodal", E("I", "I_s", "3 A"), [("P", E("R", "R_1", "4 Ω", node="$v_1$")), ("S", E("R", "R_2", "2 Ω")), ("P", E("R", "R_3", "6 Ω", node="$v_2$")), ("P", E("I", "I_2", "1 A", rev=True))])
    ladder("t04_super", E("I", "I_s", "4 A"), [("P", E("R", "R_1", "2 Ω", node="$v_1$")), ("S", E("V", "V_s", "6 V")), ("P", E("R", "R_2", "4 Ω", node="$v_2$"))])
    # mesh with loop currents
    with schemdraw.Drawing(show=False) as d:
        d.config(unit=3)
        v1 = d.add(elm.SourceV().up().label("$V_1$\n10 V"))
        r1 = d.add(elm.Resistor().right().label("$R_1$\n2 Ω"))
        d.add(elm.Dot())
        d.push()
        r2 = d.add(elm.Resistor().down().label("$R_2$\n3 Ω", loc="bottom"))
        d.add(elm.Dot())
        d.pop()
        r3 = d.add(elm.Resistor().right().label("$R_3$\n1 Ω"))
        v2 = d.add(elm.SourceV().down().reverse().label("$V_2$\n5 V", loc="bottom"))
        b2 = d.add(elm.Line().left().length(3))
        b1 = d.add(elm.Line().left().length(3))
        d.add(elm.LoopCurrent([r1, r2, b1, v1], pad=0.7).label("$I_1$"))
        d.add(elm.LoopCurrent([r3, v2, b2, r2], pad=0.7).label("$I_2$"))
        save(d, "t05_mesh")
    ladder("t06_thev_orig", E("V", "V_s", "18 V"), [("S", E("R", "R_1", "6 Ω")), ("P", E("R", "R_2", "3 Ω")), ("S", E("R", "R_3", "2 Ω"))])
    ladder("t06_thev_eq", E("V", "V_Th", "6 V"), [("S", E("R", "R_Th", "4 Ω"))])
    ladder("t06_norton_eq", E("I", "I_N", "1.5 A"), [("P", E("R", "R_N", "4 Ω")), ("S", E("W"))])
    ladder("t07_dcss", E("V", "V_s", "12 V"), [("S", E("R", "R_1", "2 Ω")), ("P", E("C", "C", "100 μF")), ("S", E("L", "L", "50 mH")), ("P", E("R", "R_2", "4 Ω"))])
    ladder("t08_rc", E("V", "V_s", "10 V"), [("S", E("SWc")), ("S", E("R", "R", "10 kΩ")), ("P", E("C", "C", "100 μF"))])
    ladder("t08_rl", E("V", "V_s", "12 V"), [("S", E("SWc")), ("S", E("R", "R", "6 Ω")), ("P", E("L", "L", "0.3 H"))])
    ladder("t09_series", E("C", "C", "$v_C(0)=V_0$"), [("S", E("SWc")), ("S", E("R", "R")), ("P", E("L", "L"))])
    ladder("t09_parallel", E("R", "R"), [("P", E("L", "L")), ("P", E("C", "C"))])
    ladder("t10_series", E("Vac", "V_s", "10∠0° V"), [("S", E("R", "R", "30 Ω")), ("S", E("L", None, "j60 Ω")), ("P", E("C", None, "−j20 Ω"))])
    star_delta("t12_star", "Z", ["$Z_A$", "$Z_B$", "$Z_C$"], star=True)
    star_delta("t12_delta", "Z", ["$Z_{AB}$", "$Z_{BC}$", "$Z_{CA}$"], star=False)


def cap_ind_waves():
    fig, axs = plt.subplots(2, 1, figsize=(5.6, 3.8), sharex=True)
    t = np.array([0, 1, 1, 3, 3, 5, 5, 6])
    v = np.array([0, 10, 10, 10, 10, 0, 0, 0])
    axs[0].plot([0, 1, 3, 5, 6], [0, 10, 10, 0, 0], color=NAVY)
    axs[0].set_ylabel("$v_C$ (V)")
    axs[1].step([0, 1, 3, 5, 6], [10, 0, -5, 0, 0], where="post", color=COPPER)
    axs[1].axhline(0, color="#999", lw=0.6)
    axs[1].set_ylabel("$i_C$ (mA)")
    axs[1].set_xlabel("time (ms), $C$ = 1 μF")
    for a in axs:
        a.grid(alpha=0.25)
    savefig(fig, "t07_ramp")


def rc_curves():
    fig, ax = plt.subplots(figsize=(5.8, 3.5))
    x = np.linspace(0, 5, 300)
    ax.plot(x, 1 - np.exp(-x), color=NAVY, label="charging  $1-e^{-t/\\tau}$")
    ax.plot(x, np.exp(-x), color=COPPER, label="discharging  $e^{-t/\\tau}$")
    for k in range(1, 6):
        ax.axvline(k, color="#bbb", lw=0.6)
        ax.annotate(f"{(1 - math.exp(-k)) * 100:.1f}%", (k, 1 - math.exp(-k)), textcoords="offset points", xytext=(-14, 6), fontsize=9, color=NAVY)
    ax.plot([0, 1], [0, 1], ls="--", color=GREY, lw=1)
    ax.set_xlabel("$t/\\tau$")
    ax.set_ylabel("fraction of final change")
    ax.legend(frameon=False, loc="center right")
    savefig(fig, "t08_curves")


def damping():
    fig, ax = plt.subplots(figsize=(5.8, 3.5))
    t = np.linspace(0, 10, 500)
    for z, c, lab in ((0.2, COPPER, "underdamped (ζ = 0.2)"), (1.0, NAVY, "critically damped (ζ = 1)"), (2.5, SAGE, "overdamped (ζ = 2.5)")):
        w0 = 1
        if z < 1:
            wd = math.sqrt(1 - z * z)
            y = 1 - np.exp(-z * t) * (np.cos(wd * t) + z / wd * np.sin(wd * t))
        elif z == 1:
            y = 1 - (1 + t) * np.exp(-t)
        else:
            s1 = -z + math.sqrt(z * z - 1)
            s2 = -z - math.sqrt(z * z - 1)
            y = 1 - (s2 * np.exp(s1 * t) - s1 * np.exp(s2 * t)) / (s2 - s1)
        ax.plot(t, y, color=c, label=lab)
    ax.axhline(1, color="#999", lw=0.6, ls="--")
    ax.set_xlabel("$\\omega_0 t$")
    ax.set_ylabel("$v_C / V_s$")
    ax.legend(frameon=False, loc="lower right")
    savefig(fig, "t09_damping")


def sinusoid():
    fig, ax = plt.subplots(figsize=(5.8, 3.2))
    t = np.linspace(0, 40e-3, 600)
    ax.plot(t * 1e3, 325 * np.sin(2 * math.pi * 50 * t), color=NAVY, label="$v(t)=325\\sin(100\\pi t)$")
    ax.plot(t * 1e3, 325 * np.sin(2 * math.pi * 50 * t - math.pi / 3), color=COPPER, label="lagging by 60°")
    ax.axhline(230, color=GREY, ls="--", lw=0.8)
    ax.text(41, 230, "RMS 230 V", va="center", fontsize=9, color=GREY)
    ax.set_xlabel("time (ms)")
    ax.set_ylabel("voltage (V)")
    ax.legend(frameon=False, loc="lower left", fontsize=9)
    savefig(fig, "t10_sine")


def phasor_diagram():
    fig, ax = plt.subplots(figsize=(4.2, 4.2))
    ax.set_aspect("equal")
    def arrow(z, c, lab, off=(0.05, 0.05)):
        ax.annotate("", xy=(z.real, z.imag), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=c, lw=1.8))
        ax.text(z.real + off[0], z.imag + off[1], lab, color=c, fontsize=11)
    V = 1 + 0j
    I = 0.75 * np.exp(-1j * math.radians(40))
    arrow(V, NAVY, "$\\mathbf{V}$")
    arrow(I, COPPER, "$\\mathbf{I}$", (0.03, -0.12))
    th = np.linspace(-math.radians(40), 0, 30)
    ax.plot(0.35 * np.cos(th), 0.35 * np.sin(th), color=GREY, lw=1)
    ax.text(0.38, -0.14, "θ", color=GREY)
    ax.axhline(0, color="#ccc", lw=0.6)
    ax.axvline(0, color="#ccc", lw=0.6)
    ax.set_xlim(-0.3, 1.25)
    ax.set_ylim(-0.75, 0.6)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.text(1.12, 0.03, "Re", fontsize=9, color="#777")
    ax.text(0.02, 0.55, "Im", fontsize=9, color="#777")
    savefig(fig, "t10_phasor")


def resonance():
    fig, ax = plt.subplots(figsize=(5.8, 3.3))
    f = np.linspace(0.5, 1.5, 600)
    for Q, c in ((2, SAGE), (5, NAVY), (15, COPPER)):
        y = 1 / np.sqrt(1 + Q ** 2 * (f - 1 / f) ** 2)
        ax.plot(f, y, color=c, label=f"$Q$ = {Q}")
    ax.axhline(1 / math.sqrt(2), color=GREY, ls="--", lw=0.8)
    ax.text(1.42, 0.73, "0.707", fontsize=9, color=GREY)
    ax.set_xlabel("$f/f_0$")
    ax.set_ylabel("$I/I_{\\max}$")
    ax.legend(frameon=False)
    savefig(fig, "t10_resonance")


def power_triangle():
    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    P, Q = 4, 3
    ax.plot([0, P, P, 0], [0, 0, Q, 0], color=NAVY)
    ax.text(P / 2, -0.35, "$P$ (W)", ha="center")
    ax.text(P + 0.12, Q / 2, "$Q$ (var)", va="center")
    ax.text(P / 2 - 0.5, Q / 2 + 0.3, "$S$ (VA)", rotation=math.degrees(math.atan2(Q, P)), color=COPPER)
    th = np.linspace(0, math.atan2(Q, P), 30)
    ax.plot(0.9 * np.cos(th), 0.9 * np.sin(th), color=GREY)
    ax.text(1.0, 0.25, "θ", color=GREY)
    ax.set_xlim(-0.3, 5.4)
    ax.set_ylim(-0.6, 3.4)
    ax.axis("off")
    savefig(fig, "t11_triangle")


def inst_power():
    fig, ax = plt.subplots(figsize=(5.8, 3.3))
    t = np.linspace(0, 2, 600)
    th = math.radians(50)
    v = np.cos(2 * math.pi * t)
    i = 0.8 * np.cos(2 * math.pi * t - th)
    p = v * i
    ax.plot(t, v, color=NAVY, lw=1.2, label="$v$")
    ax.plot(t, i, color=SAGE, lw=1.2, label="$i$")
    ax.plot(t, p, color=COPPER, lw=2, label="$p = vi$")
    ax.axhline(p.mean(), color=COPPER, ls="--", lw=0.9)
    ax.text(2.02, p.mean(), "$P$", color=COPPER, va="center")
    ax.axhline(0, color="#aaa", lw=0.6)
    ax.set_xlabel("time (cycles)")
    ax.legend(frameon=False, ncol=3, loc="lower left", fontsize=9)
    savefig(fig, "t11_instpower")


def three_phase():
    fig, ax = plt.subplots(figsize=(5.8, 3.2))
    t = np.linspace(0, 1, 500)
    for k, c, lab in ((0, NAVY, "$v_{an}$"), (1, COPPER, "$v_{bn}$"), (2, SAGE, "$v_{cn}$")):
        ax.plot(t * 20, 325 * np.sin(2 * math.pi * t - k * 2 * math.pi / 3), color=c, label=lab)
    ax.set_xlabel("time (ms)")
    ax.set_ylabel("voltage (V)")
    ax.legend(frameon=False, ncol=3, loc="lower left", fontsize=9)
    savefig(fig, "t12_waves")
    fig, ax = plt.subplots(figsize=(4.4, 4.4))
    ax.set_aspect("equal")
    ph = {"a": 0, "b": -120, "c": 120}
    pts = {}
    for n, a in ph.items():
        z = np.exp(1j * math.radians(a))
        pts[n] = z
        ax.annotate("", xy=(z.real, z.imag), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.8))
        ax.text(z.real * 1.12, z.imag * 1.12, f"$\\mathbf{{V}}_{{{n}n}}$", color=NAVY, ha="center", va="center")
    zab = pts["a"] - pts["b"]
    ax.annotate("", xy=(pts["a"].real, pts["a"].imag), xytext=(pts["b"].real, pts["b"].imag), arrowprops=dict(arrowstyle="-|>", color=COPPER, lw=1.6, ls="--"))
    ax.text(0.62, -0.35, "$\\mathbf{V}_{ab}$", color=COPPER)
    ax.set_xlim(-1.3, 1.4)
    ax.set_ylim(-1.3, 1.3)
    ax.axis("off")
    savefig(fig, "t12_phasors")


def build_all():
    vi_curves()
    text_circuits()
    cap_ind_waves()
    rc_curves()
    damping()
    sinusoid()
    phasor_diagram()
    resonance()
    power_triangle()
    inst_power()
    three_phase()


if __name__ == "__main__":
    build_all()
