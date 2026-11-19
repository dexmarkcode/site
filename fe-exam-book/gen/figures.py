"""All chapter illustrations. Run: python3 figures.py [name ...]"""
import os
import sys
import numpy as np
import figstyle
from figstyle import INK, COPPER, TEAL, RED, GREY, LIGHT
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch, Polygon, Arc
import schemdraw
import schemdraw.elements as elm
import schemdraw.logic as logic

OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
FIGS = {}


def fig(name):
    def deco(f):
        FIGS[name] = f
        return f
    return deco


def save(f, name):
    f.savefig(os.path.join(OUT, name + ".png"))
    plt.close("all")


def sch_save(d, name):
    d.save(os.path.join(OUT, name + ".png"), dpi=260)
    plt.close("all")


def box(ax, x, y, w, h, text, fc=LIGHT, ec=INK, fs=10, tc="#1a1a1a", bold=False, rs=0.08):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.02,rounding_size={rs}", fc=fc, ec=ec, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc, fontweight="bold" if bold else "normal")


def arrow(ax, p, q, color=INK, lw=1.3, style="-|>", ms=12, cs="arc3"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=ms, color=color, lw=lw, connectionstyle=cs))


def blank(w, h):
    f, ax = plt.subplots(figsize=(w, h))
    ax.axis("off")
    ax.grid(False)
    return f, ax


# ------------------------------------------------------------------ Chapter 1
@fig("fig01_blueprint")
def _():
    areas = [("Mathematics", 11, 17), ("Probability and Statistics", 4, 6), ("Ethics and Professional Practice", 3, 5),
             ("Engineering Economics", 3, 5), ("Properties of Electrical Materials", 4, 6), ("Circuit Analysis (DC and AC)", 15, 23),
             ("Linear Systems", 5, 8), ("Signal Processing", 5, 8), ("Electronics", 7, 11), ("Power Systems", 8, 12),
             ("Electromagnetics", 5, 8), ("Control Systems", 6, 9), ("Communications", 5, 8), ("Computer Networks", 3, 5),
             ("Digital Systems", 8, 12), ("Computer Systems", 5, 8), ("Software Engineering", 4, 6)]
    f, ax = plt.subplots(figsize=(6.6, 5.4))
    names = [a[0] for a in areas][::-1]
    lo = np.array([a[1] for a in areas][::-1])
    hi = np.array([a[2] for a in areas][::-1])
    mid = (lo + hi) / 2
    comp = {"Computer Networks", "Digital Systems", "Computer Systems", "Software Engineering"}
    gen = {"Mathematics", "Probability and Statistics", "Ethics and Professional Practice", "Engineering Economics"}
    cols = [TEAL if n in comp else (GREY if n in gen else INK) for n in names]
    cols = [COPPER if n.startswith("Circuit") else c for c, n in zip(cols, names)]
    y = np.arange(len(names))
    ax.barh(y, mid, color=cols, height=0.66, alpha=0.92)
    ax.errorbar(mid, y, xerr=[mid - lo, hi - mid], fmt="none", ecolor="#333333", elinewidth=0.9, capsize=2.5)
    for yi, m, l, h in zip(y, mid, lo, hi):
        ax.text(h + 0.4, yi, f"{l}–{h}", va="center", fontsize=8.5, color="#333333")
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=9.5)
    ax.set_xlabel("Number of questions (bar = midpoint; whiskers = NCEES range)")
    ax.set_xlim(0, 26)
    ax.grid(axis="y", visible=False)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=GREY, label="General"), Patch(color=COPPER, label="Circuits"), Patch(color=INK, label="Electrical"),
                       Patch(color=TEAL, label="Computing")], loc="lower right", fontsize=9)
    save(f, "fig01_blueprint")


@fig("fig01_studyplan")
def _():
    tasks = [("Part I: foundations, maths, prob/econ/ethics", 0, 2, GREY), ("Part II: circuits, AC power, transients", 2, 2.5, COPPER),
             ("Part III: signals, electronics, EM, materials", 4.5, 2, INK), ("Part IV: power, control, communications", 6.5, 2, INK),
             ("Part V: digital, computing, networks, software", 8.5, 1.5, TEAL), ("Mixed review, 20 min twice weekly", 3, 7, "#8FA9D6"),
             ("Ch. 16 strategy and timed drill", 9.5, 0.5, RED), ("Mock exam 1 and targeted repair", 10, 1, RED), ("Mock exam 2, error log, rest", 11, 1, RED)]
    f, ax = plt.subplots(figsize=(6.8, 3.5))
    n = len(tasks)
    for i, (t, s0, d, c) in enumerate(tasks):
        ax.barh(n - i, d, left=s0, color=c, height=0.6, alpha=0.92)
    ax.set_yticks([n - i for i in range(n)])
    ax.set_yticklabels([t[0] for t in tasks], fontsize=8.6)
    ax.set_xlim(0, 12)
    ax.set_xticks(np.arange(0.5, 12, 1))
    ax.set_xticklabels([f"Wk {i}" for i in range(1, 13)], fontsize=7.8)
    ax.grid(axis="y", visible=False)
    ax.tick_params(axis="y", length=0)
    save(f, "fig01_studyplan")


# ------------------------------------------------------------------ Chapter 2
@fig("fig02_complex_plane")
def _():
    f, ax = plt.subplots(figsize=(5.2, 4.2))
    ax.axhline(0, color="#444", lw=0.9); ax.axvline(0, color="#444", lw=0.9)
    a, b = 3, 2.2
    ax.annotate("", xy=(a, b), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=INK, lw=2))
    ax.plot([a, a], [0, b], ls="--", color=GREY, lw=1); ax.plot([0, a], [b, b], ls="--", color=GREY, lw=1)
    ax.text(a / 2, -0.32, "$a = M\\cos\\theta$", ha="center", fontsize=11)
    ax.text(a + 0.12, b / 2, "$b = M\\sin\\theta$", va="center", fontsize=11)
    ax.text(1.25, 1.25, "$M$", fontsize=13, color=INK)
    ax.add_patch(Arc((0, 0), 1.6, 1.6, theta1=0, theta2=np.degrees(np.arctan2(b, a)), color=COPPER, lw=1.6))
    ax.text(0.95, 0.28, "$\\theta$", color=COPPER, fontsize=13)
    ax.plot(a, b, "o", color=COPPER); ax.text(a + 0.1, b + 0.15, "$z = a + jb = M\\angle\\theta$", fontsize=11.5)
    p2 = (-2.2, 1.6); ax.plot(*p2, "o", color=RED)
    ax.annotate("", xy=p2, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.4))
    ax.text(-3.9, 2.05, "2nd quadrant: add 180° to\nthe calculator's $\\tan^{-1}(b/a)$", fontsize=9.5, color=RED)
    ax.set_xlim(-4, 5.2); ax.set_ylim(-1, 3.2)
    ax.set_xlabel("Real axis"); ax.set_ylabel("Imaginary axis ($j$)")
    ax.grid(alpha=0.4)
    save(f, "fig02_complex_plane")


@fig("fig02_ode_response")
def _():
    t = np.linspace(0, 10, 600)
    f, ax = plt.subplots(figsize=(6.2, 3.4))
    wn = 1.5
    for z, c, lab in [(0, RED, "$\\zeta = 0$ (undamped)"), (0.2, COPPER, "$\\zeta = 0.2$ (underdamped)"), (1.0, INK, "$\\zeta = 1$ (critically damped)"), (2.0, TEAL, "$\\zeta = 2$ (overdamped)")]:
        if z < 1:
            wd = wn * np.sqrt(1 - z * z)
            y = np.exp(-z * wn * t) * (np.cos(wd * t) + z * wn / wd * np.sin(wd * t))
        elif z == 1:
            y = (1 + wn * t) * np.exp(-wn * t)
        else:
            r1 = -wn * (z - np.sqrt(z * z - 1)); r2 = -wn * (z + np.sqrt(z * z - 1))
            y = (r2 * np.exp(r1 * t) - r1 * np.exp(r2 * t)) / (r2 - r1)
        ax.plot(t, y, color=c, label=lab, lw=1.6 if z else 1.1, alpha=1 if z else 0.6)
    ax.axhline(0, color="#444", lw=0.7)
    ax.set_xlabel("Time"); ax.set_ylabel("$y(t)$, released from $y(0)=1$")
    ax.legend(fontsize=8.8, loc="upper right", ncol=2)
    ax.set_ylim(-1.15, 1.45)
    save(f, "fig02_ode_response")


@fig("fig02_newton")
def _():
    x = np.linspace(0.9, 3.3, 300)
    fx = lambda v: v ** 3 - 10
    dfx = lambda v: 3 * v ** 2
    f, ax = plt.subplots(figsize=(5.6, 3.6))
    ax.plot(x, fx(x), color=INK, label="$f(x) = x^3 - 10$")
    ax.axhline(0, color="#444", lw=0.8)
    xn = 3.2
    for k in range(3):
        y = fx(xn); xn1 = xn - y / dfx(xn)
        xx = np.linspace(xn1, xn, 50)
        ax.plot(xx, y + dfx(xn) * (xx - xn), color=COPPER, lw=1.2, ls="--")
        ax.plot([xn, xn], [0, y], color=GREY, lw=0.8, ls=":")
        ax.plot(xn, y, "o", color=COPPER, ms=4)
        ax.text(xn, -2.6, f"$x_{k}$", ha="center", fontsize=11)
        xn = xn1
    ax.plot(10 ** (1 / 3), 0, "o", color=RED, ms=5); ax.text(10 ** (1 / 3) - 0.05, 1.5, "root", color=RED, ha="right")
    ax.set_ylim(-4, 24); ax.set_xlabel("$x$"); ax.set_ylabel("$f(x)$")
    ax.legend(loc="upper left")
    save(f, "fig02_newton")


# ------------------------------------------------------------------ Chapter 3
@fig("fig03_normal")
def _():
    z = np.linspace(-3.6, 3.6, 500); pdf = np.exp(-z * z / 2) / np.sqrt(2 * np.pi)
    f, ax = plt.subplots(figsize=(6, 3.2))
    ax.plot(z, pdf, color=INK)
    m = z >= 1.5
    ax.fill_between(z[m], pdf[m], color=COPPER, alpha=0.55)
    m2 = z <= 1.5
    ax.fill_between(z[m2], pdf[m2], color=INK, alpha=0.08)
    for k, lab in [(1, "68%"), (2, "95%")]:
        ax.annotate("", xy=(-k, 0.43 - 0.06 * k), xytext=(k, 0.43 - 0.06 * k), arrowprops=dict(arrowstyle="<->", color=GREY, lw=0.9))
        ax.text(0, 0.44 - 0.06 * k, lab, ha="center", fontsize=9, color=GREY)
    ax.text(2.05, 0.08, "$R(z) = 1 - F(z)$", color=COPPER, fontsize=10.5)
    ax.text(-2.9, 0.25, "$F(z)$: area to\nthe left of $z$", color=INK, fontsize=10)
    ax.axvline(1.5, color=COPPER, lw=1, ls="--"); ax.text(1.5, -0.035, "$z$", ha="center", color=COPPER)
    ax.set_xticks(range(-3, 4)); ax.set_xticklabels(["$\\mu-3\\sigma$", "$\\mu-2\\sigma$", "$\\mu-\\sigma$", "$\\mu$", "$\\mu+\\sigma$", "$\\mu+2\\sigma$", "$\\mu+3\\sigma$"], fontsize=8.5)
    ax.set_yticks([]); ax.spines["left"].set_visible(False); ax.grid(False)
    ax.set_ylim(-0.05, 0.46)
    save(f, "fig03_normal")


@fig("fig03_cashflow")
def _():
    f, ax = blank(6.4, 3.0)
    ax.set_xlim(-0.6, 9.6); ax.set_ylim(-3.2, 2.0)
    ax.plot([0, 9], [0, 0], color="#333", lw=1.2)
    for k in range(10):
        ax.plot([k, k], [-0.06, 0.06], color="#333"); ax.text(k, 0.15, str(k) if k < 9 else "n", ha="center", fontsize=9)
    arrow(ax, (0, 0), (0, -2.8), color=RED, lw=2); ax.text(0.15, -2.7, "First cost $P$", color=RED, fontsize=10)
    for k in range(1, 10):
        arrow(ax, (k, 0), (k, -0.9), color=COPPER, lw=1.4)
    ax.text(4.5, -1.25, "Annual operating costs $A$ (end of each year)", ha="center", color=COPPER, fontsize=10)
    arrow(ax, (9, 0), (9, 1.5), color=TEAL, lw=2); ax.text(8.85, 1.6, "Salvage $S$", color=TEAL, fontsize=10, ha="right")
    ax.text(4.5, 0.55, "Years", ha="center", fontsize=9.5, color=GREY)
    save(f, "fig03_cashflow")


@fig("fig03_reliability")
def _():
    f, ax = blank(7, 2.6)
    ax.set_xlim(0, 14); ax.set_ylim(0, 5)
    ax.text(2.6, 4.6, "Series:  $R = R_1R_2$", ha="center", fontsize=11, color=INK)
    ax.plot([0.2, 5], [2.5, 2.5], color="#333")
    box(ax, 0.8, 2.0, 1.4, 1.0, "$R_1$", fs=14); box(ax, 3.0, 2.0, 1.4, 1.0, "$R_2$", fs=14)
    ax.text(10.2, 4.6, "Parallel:  $R = 1 - (1-R_1)(1-R_2)$", ha="center", fontsize=11, color=INK)
    ax.plot([7, 8], [2.5, 2.5], color="#333"); ax.plot([12.4, 13.6], [2.5, 2.5], color="#333")
    ax.plot([8, 8], [1.2, 3.8], color="#333"); ax.plot([12.4, 12.4], [1.2, 3.8], color="#333")
    for y, lab in [(3.8, "$R_1$"), (1.2, "$R_2$")]:
        ax.plot([8, 12.4], [y, y], color="#333"); box(ax, 9.5, y - 0.5, 1.4, 1.0, lab, fs=14)
    save(f, "fig03_reliability")


# ------------------------------------------------------------------ Chapter 4
@fig("fig04_divider")
def _():
    with schemdraw.Drawing(show=False) as d:
        d.config(unit=2.4)
        S = elm.SourceV().up().label("$V_s$")
        elm.Resistor().right().label("$R_1$")
        elm.Dot()
        elm.Line().right().length(1)
        o = elm.Dot(open=True).label("$V_o$", loc="right")
        elm.Gap().down().length(2.4)
        elm.Dot(open=True)
        elm.Line().left().length(1)
        elm.Dot()
        d.push()
        elm.Resistor().up().label("$R_2$", loc="bottom")
        d.pop()
        elm.Line().to(S.start)
        elm.Label().at((3.2, -1.0)).label("Unloaded")
        d.move(7.5, 0)
        S2 = elm.SourceV().up().label("$V_s$")
        elm.Resistor().right().label("$R_1$")
        elm.Dot()
        d.push()
        elm.Resistor().down().label("$R_2$", loc="bottom")
        d.pop()
        elm.Line().right().length(2)
        elm.Resistor().down().label("$R_L$", loc="bottom", color=COPPER)
        elm.Line().to(S2.start)
        elm.Label().at((11.2, -1.0)).label("Loaded: use $R_2 \\parallel R_L$")
    sch_save(d, "fig04_divider")


@fig("fig04_nodal")
def _():
    with schemdraw.Drawing(show=False) as d:
        d.config(unit=2.6)
        S1 = elm.SourceV().up().label("$V_1$")
        elm.Resistor().right().label("$R_1$")
        elm.Dot().label("x", loc="top")
        d.push()
        elm.Resistor().down().label("$R_2$", loc="bottom")
        elm.Dot()
        d.pop()
        elm.Line().right().length(1)
        elm.Resistor().right().label("$R_3$")
        elm.SourceV().down().reverse().label("$V_2$", loc="bottom")
        elm.Line().to(S1.start)
        elm.Ground().at(S1.start)
    sch_save(d, "fig04_nodal")


@fig("fig04_thevenin")
def _():
    with schemdraw.Drawing(show=False) as d:
        d.config(unit=2.4)
        S = elm.SourceV().up().label("$V_{Th}$")
        elm.Resistor().right().label("$R_{Th}$")
        elm.Dot(open=True).label("a", loc="right")
        elm.Gap().down().length(2.4)
        elm.Dot(open=True).label("b", loc="right")
        elm.Line().to(S.start)
        elm.Label().at((1.2, -1.0)).label("Thévenin")
        elm.Label().at((4.4, 1.2)).label("$\\equiv$", fontsize=22)
        d.move(3.6, 0)
        I = elm.SourceI().up().label("$I_N$")
        elm.Line().right().length(2.0)
        elm.Dot()
        d.push()
        elm.Resistor().down().label("$R_{Th}$", loc="bottom")
        d.pop()
        elm.Line().right().length(1.4)
        elm.Dot(open=True).label("a", loc="right")
        elm.Gap().down().length(2.4)
        elm.Dot(open=True).label("b", loc="right")
        elm.Line().to(I.start)
        elm.Label().at((9.2, -1.0)).label("Norton")
    sch_save(d, "fig04_thevenin")


@fig("fig04_maxpower")
def _():
    r = np.linspace(0.02, 5, 400)
    p = 4 * r / (1 + r) ** 2
    eta = r / (1 + r)
    f, ax = plt.subplots(figsize=(5.8, 3.3))
    ax.plot(r, p, color=INK, label="$P_L/P_{max}$")
    ax.plot(r, eta, color=COPPER, ls="--", label="Efficiency $R_L/(R_L + R_{Th})$")
    ax.axvline(1, color=GREY, lw=0.8, ls=":")
    ax.annotate("Maximum at $R_L = R_{Th}$,\nefficiency 50%", xy=(1, 1), xytext=(1.6, 0.6), arrowprops=dict(arrowstyle="->", color=GREY), fontsize=9.5)
    ax.set_xlabel("$R_L / R_{Th}$"); ax.set_ylim(0, 1.08); ax.legend(loc="lower right")
    save(f, "fig04_maxpower")


# ------------------------------------------------------------------ Chapter 5
@fig("fig05_phasor")
def _():
    f, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.1), gridspec_kw={"width_ratios": [1, 1.6]})
    th = np.radians(40)
    a1.axhline(0, color="#555", lw=0.8); a1.axvline(0, color="#555", lw=0.8)
    a1.annotate("", xy=(1, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=INK, lw=2))
    a1.annotate("", xy=(0.7 * np.cos(-th), 0.7 * np.sin(-th)), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=COPPER, lw=2))
    a1.text(1.0, 0.07, "$\\mathbf{V}$", color=INK, fontsize=13); a1.text(0.55, -0.62, "$\\mathbf{I}$", color=COPPER, fontsize=13)
    a1.add_patch(Arc((0, 0), 0.6, 0.6, theta1=-40, theta2=0, color=GREY)); a1.text(0.33, -0.15, "$\\theta$", fontsize=11)
    a1.set_xlim(-0.3, 1.25); a1.set_ylim(-0.8, 0.6); a1.set_aspect("equal"); a1.axis("off")
    a1.set_title("Phasors (current lags)", fontsize=10)
    t = np.linspace(0, 4 * np.pi, 500)
    a2.plot(t, np.cos(t), color=INK, label="$v(t)$")
    a2.plot(t, 0.7 * np.cos(t - th), color=COPPER, label="$i(t)$")
    a2.axhline(0, color="#555", lw=0.7); a2.set_xticks([]); a2.set_yticks([]); a2.legend(loc="upper right", fontsize=9)
    a2.set_title("Time domain", fontsize=10); a2.set_xlabel("$\\omega t$")
    save(f, "fig05_phasor")


@fig("fig05_resonance")
def _():
    w = np.linspace(0.3, 2.0, 600)
    f, ax = plt.subplots(figsize=(5.8, 3.3))
    for Qv, c in [(2, TEAL), (5, COPPER), (15, INK)]:
        I = 1 / np.sqrt(1 + Qv ** 2 * (w - 1 / w) ** 2)
        ax.plot(w, I, color=c, label=f"$Q = {Qv}$")
    ax.axhline(1 / np.sqrt(2), color=GREY, ls=":", lw=0.9); ax.text(1.62, 0.73, "half-power ($1/\\sqrt{2}$)", fontsize=8.5, color=GREY)
    ax.set_xlabel("$\\omega / \\omega_0$"); ax.set_ylabel("$|I| / I_{max}$"); ax.legend()
    save(f, "fig05_resonance")


@fig("fig05_powertriangle")
def _():
    f, ax = blank(4.6, 3.0)
    P, Qv = 4, 3
    ax.add_patch(Polygon([(0, 0), (P, 0), (P, Qv)], closed=True, fc=LIGHT, ec="none"))
    ax.annotate("", xy=(P, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=INK, lw=2))
    ax.annotate("", xy=(P, Qv), xytext=(P, 0), arrowprops=dict(arrowstyle="-|>", color=COPPER, lw=2))
    ax.annotate("", xy=(P, Qv), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2))
    ax.text(P / 2, -0.38, "Real power $P$ (W)", ha="center", color=INK)
    ax.text(P + 0.12, Qv / 2, "Reactive\npower $Q$ (var)", va="center", color=COPPER)
    ax.text(P / 2 - 0.5, Qv / 2 + 0.35, "Apparent power\n$|S|$ (VA)", ha="center", color=TEAL, rotation=33)
    ax.add_patch(Arc((0, 0), 1.6, 1.6, theta1=0, theta2=36.87, color=GREY)); ax.text(0.9, 0.2, "$\\theta$")
    ax.set_xlim(-0.3, 6.2); ax.set_ylim(-0.7, 3.4)
    save(f, "fig05_powertriangle")


# ------------------------------------------------------------------ Chapter 6
@fig("fig06_rc_charge")
def _():
    t = np.linspace(0, 5, 500)
    f, ax = plt.subplots(figsize=(6.0, 3.3))
    ax.plot(t, 1 - np.exp(-t), color=INK, label="Charging: $1 - e^{-t/\\tau}$")
    ax.plot(t, np.exp(-t), color=COPPER, label="Discharging: $e^{-t/\\tau}$")
    for k, v in [(1, 0.632), (2, 0.865), (3, 0.950)]:
        ax.plot([k, k], [0, v], color=GREY, ls=":", lw=0.9); ax.plot(k, v, "o", color=INK, ms=4)
        ax.text(k + 0.06, v - 0.07, f"{v*100:.1f}%", fontsize=8.5, color=INK)
    ax.plot(1, 0.368, "o", color=COPPER, ms=4); ax.text(1.06, 0.39, "36.8%", fontsize=8.5, color=COPPER)
    ax.set_xticks(range(6)); ax.set_xticklabels(["0", "$\\tau$", "$2\\tau$", "$3\\tau$", "$4\\tau$", "$5\\tau$"])
    ax.set_ylabel("Fraction of total change"); ax.legend(loc="center right")
    save(f, "fig06_rc_charge")


@fig("fig06_rl_switch")
def _():
    with schemdraw.Drawing(show=False) as d:
        d.config(unit=2.6)
        S = elm.SourceV().up().label("$V_s$")
        elm.Resistor().right().label("$R_1$")
        elm.Switch(action="open").right().label("opens at $t = 0$")
        elm.Dot()
        d.push()
        elm.Inductor().down().label("$L$", loc="bottom")
        elm.Dot()
        d.pop()
        elm.Line().right().length(2.2)
        elm.Resistor().down().label("$R_2$", loc="bottom")
        elm.Line().to(S.start)
    sch_save(d, "fig06_rl_switch")


@fig("fig06_step_zeta")
def _():
    t = np.linspace(0, 12, 600)
    f, ax = plt.subplots(figsize=(6.0, 3.3))
    for z, c in [(0.1, RED), (0.3, COPPER), (0.7, INK), (1.0, TEAL), (2.0, GREY)]:
        if z < 1:
            wd = np.sqrt(1 - z * z); y = 1 - np.exp(-z * t) * (np.cos(wd * t) + z / wd * np.sin(wd * t))
        elif z == 1:
            y = 1 - (1 + t) * np.exp(-t)
        else:
            r1 = -(z - np.sqrt(z * z - 1)); r2 = -(z + np.sqrt(z * z - 1)); y = 1 + (r2 * np.exp(r1 * t) - r1 * np.exp(r2 * t)) / (r1 - r2)
        ax.plot(t, y, color=c, label=f"$\\zeta = {z}$")
    ax.axhline(1, color="#555", lw=0.7, ls=":")
    ax.set_xlabel("$\\omega_n t$"); ax.set_ylabel("Step response"); ax.legend(ncol=3, fontsize=8.6, loc="lower right")
    save(f, "fig06_step_zeta")


@fig("fig06_pole_zero")
def _():
    f = plt.figure(figsize=(7.0, 4.0))
    ax = f.add_axes([0.06, 0.1, 0.42, 0.8])
    ax.axhline(0, color="#444", lw=0.8); ax.axvline(0, color="#444", lw=0.8)
    ax.axvspan(-3.2, 0, color=TEAL, alpha=0.07); ax.axvspan(0, 2.2, color=RED, alpha=0.06)
    pts = [(-2.2, 0, "a"), (-1, 1.6, "b"), (-1, -1.6, "b"), (0, 1.2, "c"), (0, -1.2, "c"), (1.2, 0, "d")]
    for x, y, l in pts:
        ax.plot(x, y, "x", ms=9, mew=2, color=INK)
        ax.text(x + 0.12, y + 0.15, l, fontsize=11, color=COPPER, fontweight="bold")
    ax.text(-2.9, 2.2, "Stable", color=TEAL, fontsize=10); ax.text(0.6, 2.2, "Unstable", color=RED, fontsize=10)
    ax.set_xlim(-3.2, 2.2); ax.set_ylim(-2.6, 2.6); ax.set_xlabel("$\\sigma$"); ax.set_ylabel("$j\\omega$"); ax.set_title("s-plane", fontsize=10.5)
    t = np.linspace(0, 6, 300)
    resp = [("a", np.exp(-1.0 * t)), ("b", np.exp(-0.45 * t) * np.cos(3 * t)), ("c", np.cos(3 * t)), ("d", np.exp(0.35 * t) * 0.15)]
    for i, (l, y) in enumerate(resp):
        a = f.add_axes([0.58, 0.72 - i * 0.205, 0.38, 0.16])
        a.plot(t, y, color=[INK, COPPER, GREY, RED][i], lw=1.4); a.axhline(0, color="#999", lw=0.6)
        a.set_xticks([]); a.set_yticks([]); a.grid(False)
        a.text(-0.6, 0, l, fontsize=11, color=COPPER, fontweight="bold", va="center")
    save(f, "fig06_pole_zero")


if __name__ == "__main__":
    names = sys.argv[1:] or list(FIGS)
    for n in names:
        FIGS[n]()
        print("made", n)
