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


# ------------------------------------------------------------------ Chapter 7
@fig("fig07_square_fourier")
def _():
    t = np.linspace(0, 2, 1200)
    sq = np.sign(np.sin(2 * np.pi * t))
    f, ax = plt.subplots(figsize=(6.4, 3.2))
    ax.plot(t, sq, color="#BBBBBB", lw=2.2, label="Square wave")
    for N, c in [(1, TEAL), (3, COPPER), (15, INK)]:
        y = sum(4 / (np.pi * n) * np.sin(2 * np.pi * n * t) for n in range(1, N + 1, 2))
        ax.plot(t, y, color=c, lw=1.4, label="Fundamental only" if N == 1 else f"Harmonics up to {N}")
    ax.set_xlabel("Time (periods)"); ax.set_ylabel("Amplitude ($A = 1$)")
    ax.legend(fontsize=8.5, ncol=2, loc="lower left"); ax.set_ylim(-1.7, 1.7)
    save(f, "fig07_square_fourier")


@fig("fig07_sampling")
def _():
    t = np.linspace(0, 2e-3, 2000)
    fs = 8000
    ts = np.arange(0, 2e-3 + 1e-9, 1 / fs)
    f, ax = plt.subplots(figsize=(6.6, 3.0))
    ax.plot(t * 1e3, np.cos(2 * np.pi * 7000 * t), color=COPPER, alpha=0.45, lw=1, label="7 kHz input")
    ax.plot(t * 1e3, np.cos(2 * np.pi * 1000 * t), color=INK, lw=1.8, label="1 kHz alias")
    ax.plot(ts * 1e3, np.cos(2 * np.pi * 7000 * ts), "o", color=RED, ms=6, label="Samples at 8 kHz")
    ax.set_xlabel("Time (ms)"); ax.set_yticks([-1, 0, 1]); ax.legend(loc="lower right", fontsize=8.5, ncol=3)
    ax.set_ylim(-1.5, 1.25)
    save(f, "fig07_sampling")


@fig("fig07_filters")
def _():
    f, ax = blank(7.0, 4.0)
    ax.set_xlim(0, 14); ax.set_ylim(-0.8, 7.2)
    def add(x, y):
        ax.add_patch(Circle((x, y), 0.32, fc="white", ec=INK, lw=1.2)); ax.text(x, y, "+", ha="center", va="center", fontsize=13, color=INK)
    def gain(x, y, lab):
        ax.add_patch(Polygon([(x - 0.35, y + 0.35), (x - 0.35, y - 0.35), (x + 0.35, y)], fc=LIGHT, ec=COPPER, lw=1.2))
        ax.text(x - 0.5, y + 0.45, lab, fontsize=10, color=COPPER)
    # FIR
    ax.text(0.2, 6.8, "FIR:  $y[n] = b_0x[n] + b_1x[n-1] + b_2x[n-2]$", fontsize=10.5, color=INK)
    ax.text(0.2, 5.6, "$x[n]$", fontsize=11)
    xs = [1.6, 5.0, 8.4]
    ax.plot([1.0, 9.0], [5.6, 5.6], color="#333")
    for x0 in [3.0, 6.4]:
        box(ax, x0, 5.25, 1.0, 0.7, "$z^{-1}$", fc="white")
    for i, x in enumerate(xs):
        ax.plot([x, x], [5.6, 4.6], color="#333"); gain(x, 4.25, f"$b_{i}$"); ax.plot([x, x], [3.9, 3.3], color="#333")
    ax.plot([1.6, 10.8], [3.0, 3.0], color="#333")
    for x in xs[1:]:
        add(x, 3.0)
    arrow(ax, (8.75, 3.0), (11.5, 3.0)); ax.text(11.6, 2.9, "$y[n]$", fontsize=11)
    # IIR
    ax.text(0.2, 1.95, "IIR:  $y[n] = x[n] + a\\,y[n-1]$", fontsize=10.5, color=INK)
    ax.text(0.2, 0.95, "$x[n]$", fontsize=11)
    arrow(ax, (1.2, 1.0), (4.65, 1.0)); add(5.0, 1.0)
    arrow(ax, (5.35, 1.0), (11.5, 1.0)); ax.text(11.6, 0.9, "$y[n]$", fontsize=11)
    ax.plot([9.5, 9.5], [1.0, 0.2], color="#333"); ax.plot([9.5, 8.6], [0.2, 0.2], color="#333")
    box(ax, 7.6, -0.15, 1.0, 0.7, "$z^{-1}$", fc="white")
    ax.plot([7.6, 6.8], [0.2, 0.2], color="#333"); gain(6.45, 0.2, "$a$")
    ax.plot([6.1, 5.0, 5.0], [0.2, 0.2, 0.68], color="#333")
    save(f, "fig07_filters")


# ------------------------------------------------------------------ Chapter 8
@fig("fig08_diode_iv")
def _():
    f, ax = plt.subplots(figsize=(5.8, 3.4))
    v = np.linspace(-0.2, 0.78, 400)
    i = 1e-12 * (np.exp(v / 0.035) - 1)
    ax.plot(v, np.clip(i * 1e3, -1, 30), color=INK)
    vr = np.linspace(-5.6, -0.2, 200)
    ir = np.where(vr < -5.1, -(np.abs(vr) - 5.1) * 60, -0.05 * np.ones_like(vr))
    ax.plot(vr, ir, color=COPPER)
    ax.axhline(0, color="#444", lw=0.8); ax.axvline(0, color="#444", lw=0.8)
    ax.annotate("Forward conduction\nnear 0.7 V", xy=(0.7, 12), xytext=(-2.6, 18), arrowprops=dict(arrowstyle="->", color=GREY), fontsize=9.5)
    ax.annotate("Zener / breakdown\nregion", xy=(-5.3, -12), xytext=(-4.4, -25), arrowprops=dict(arrowstyle="->", color=GREY), fontsize=9.5, color=COPPER)
    ax.text(-2.8, 1.5, "Reverse bias: tiny leakage", fontsize=9, color=GREY)
    ax.set_xlabel("Diode voltage $v_D$ (V)"); ax.set_ylabel("Current $i_D$ (mA)"); ax.set_ylim(-32, 30); ax.set_xlim(-6, 1.2)
    save(f, "fig08_diode_iv")


@fig("fig08_rectifier")
def _():
    t = np.linspace(0, 3 / 60, 3000)
    vin = np.abs(np.sin(2 * np.pi * 60 * t))
    hw = np.where(np.sin(2 * np.pi * 60 * t) > 0, np.sin(2 * np.pi * 60 * t), 0)
    def cap(src, tau):
        out = np.zeros_like(src); v = 0
        dt = t[1] - t[0]
        for k, s in enumerate(src):
            v = max(s, v * np.exp(-dt / tau)); out[k] = v
        return out
    f, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 2.8), sharey=True)
    a1.plot(t * 1e3, hw, color=GREY, lw=1, ls="--", label="Rectified"); a1.plot(t * 1e3, cap(hw, 0.08), color=INK, label="With capacitor")
    a2.plot(t * 1e3, vin, color=GREY, lw=1, ls="--"); a2.plot(t * 1e3, cap(vin, 0.08), color=COPPER)
    a1.set_title("Half-wave", fontsize=10); a2.set_title("Full-wave", fontsize=10)
    for a in (a1, a2):
        a.set_xlabel("Time (ms)"); a.set_ylim(-0.05, 1.12)
    a1.set_ylabel("$v/V_p$"); a1.legend(fontsize=8, loc="lower right")
    save(f, "fig08_rectifier")


@fig("fig08_bjt_bias")
def _():
    with schemdraw.Drawing(show=False) as d:
        d.config(unit=2.2)
        Q = elm.BjtNpn(circle=True).label("Q", loc="right")
        elm.Resistor().at(Q.collector).up().label("$R_C$", loc="bottom")
        top = elm.Dot()
        elm.Resistor().at(Q.emitter).down().label("$R_E$", loc="bottom")
        bot = elm.Dot()
        elm.Line().at(Q.base).left().length(1.5)
        b = elm.Dot()
        elm.Resistor().up().toy(top.center).label("$R_1$")
        elm.Line().to(top.center)
        elm.Line().right().at(top.center).length(1.2).label("$+V_{CC}$", loc="right")
        elm.Resistor().at(b.center).down().toy(bot.center).label("$R_2$")
        elm.Line().to(bot.center)
        elm.Ground().at(bot.center)
    sch_save(d, "fig08_bjt_bias")


@fig("fig08_opamps")
def _():
    from PIL import Image
    paths = []
    for kind in ("inv", "noninv"):
        with schemdraw.Drawing(show=False) as d:
            d.config(unit=2.2, fontsize=13)
            op = elm.Opamp(leads=True, flip=(kind != "inv"))
            if kind == "inv":
                elm.Line().at(op.in2).left().length(0.6)
                elm.Ground()
                elm.Line().at(op.in1).left().length(0.6)
                n = elm.Dot()
                elm.Resistor().left().label("$R_{in}$")
                elm.Dot(open=True).label("$v_{in}$", loc="left")
            else:
                elm.Line().at(op.in2).left().length(2.8)
                elm.Dot(open=True).label("$v_{in}$", loc="left")
                elm.Line().at(op.in1).left().length(0.6)
                n = elm.Dot()
                elm.Line().left().length(1.4)
                elm.Resistor().down().label("$R_1$", loc="bottom")
                elm.Ground()
            if kind == "inv":
                elm.Line().at(n.center).up().length(1.4)
                elm.Resistor().right().tox(op.out).label("$R_f$")
                elm.Line().down().toy(op.out)
            else:
                elm.Line().at(n.center).down().length(1.4)
                elm.Resistor().right().tox(op.out).label("$R_f$", loc="bottom")
                elm.Line().up().toy(op.out)
            elm.Dot()
            elm.Line().at(op.out).right().length(0.8)
            elm.Dot(open=True).label("$v_{out}$", loc="right")
            elm.Label().at((op.out[0] - 2.5, op.out[1] - (2.6 if kind == "inv" else 3.4))).label("Inverting:  $v_{out} = -(R_f/R_{in})\\,v_{in}$" if kind == "inv" else "Non-inverting:  $v_{out} = (1 + R_f/R_1)\\,v_{in}$", fontsize=12)
        pth = os.path.join(OUT, f"_tmp_{kind}.png"); d.save(pth, dpi=260); plt.close("all"); paths.append(pth)
    ims = [Image.open(p).convert("RGB") for p in paths]
    h = max(i.height for i in ims)
    out = Image.new("RGB", (sum(i.width for i in ims) + 120, h), "white")
    x = 0
    for i in ims:
        out.paste(i, (x, (h - i.height) // 2)); x += i.width + 120
    out.save(os.path.join(OUT, "fig08_opamps.png"))
    for p in paths:
        os.remove(p)


# ------------------------------------------------------------------ Chapter 9
@fig("fig09_field_lines")
def _():
    x, y = np.meshgrid(np.linspace(-3, 3, 300), np.linspace(-2.2, 2.2, 240))
    def E(q, x0):
        dx, dy = x - x0, y; r3 = (dx ** 2 + dy ** 2) ** 1.5 + 1e-9
        return q * dx / r3, q * dy / r3
    ex1, ey1 = E(1, -1); ex2, ey2 = E(-1, 1)
    f, ax = plt.subplots(figsize=(5.6, 4.0))
    ax.streamplot(x, y, ex1 + ex2, ey1 + ey2, color=INK, density=1.3, linewidth=0.8, arrowsize=0.9)
    ax.add_patch(Circle((-1, 0), 0.17, color=RED)); ax.text(-1, 0, "+", color="white", ha="center", va="center", fontsize=13, fontweight="bold")
    ax.add_patch(Circle((1, 0), 0.17, color=INK)); ax.text(1, -0.02, "−", color="white", ha="center", va="center", fontsize=14, fontweight="bold")
    ax.set_aspect("equal"); ax.axis("off")
    save(f, "fig09_field_lines")


@fig("fig09_capacitor")
def _():
    f, ax = blank(5.4, 3.0)
    ax.set_xlim(0, 10); ax.set_ylim(0, 5.5)
    ax.add_patch(Rectangle((1.5, 4.0), 7, 0.25, fc=RED, ec="none")); ax.add_patch(Rectangle((1.5, 1.0), 7, 0.25, fc=INK, ec="none"))
    ax.add_patch(Rectangle((1.5, 1.25), 7, 2.75, fc=COPPER, alpha=0.13, ec="none"))
    for k in range(9):
        x = 2.0 + 0.75 * k
        arrow(ax, (x, 3.9), (x, 1.35), color=COPPER, lw=1)
    for k in range(10):
        ax.text(1.8 + 0.7 * k, 4.4, "+", color=RED, fontsize=11, ha="center"); ax.text(1.8 + 0.7 * k, 0.55, "−", color=INK, fontsize=12, ha="center")
    ax.annotate("", xy=(9.2, 4.0), xytext=(9.2, 1.25), arrowprops=dict(arrowstyle="<->", color="#333")); ax.text(9.4, 2.55, "$d$", fontsize=13)
    ax.text(5.0, 2.55, "$E = V/d$\ndielectric $\\varepsilon_r$", ha="center", va="center", fontsize=10.5, color=INK, bbox=dict(fc="white", ec="none", alpha=0.8))
    ax.text(0.3, 4.1, "Area $A$", fontsize=10)
    save(f, "fig09_capacitor")


@fig("fig09_standing_wave")
def _():
    z = np.linspace(0, 1.5, 600)
    f, ax = plt.subplots(figsize=(6.2, 3.2))
    for G, c, lab in [(0, TEAL, "Matched ($\\Gamma = 0$, VSWR = 1)"), (1 / 3, COPPER, "$|\\Gamma| = 1/3$ (VSWR = 2)"), (0.8, RED, "$|\\Gamma| = 0.8$ (VSWR = 9)")]:
        env = np.abs(1 + G * np.exp(-1j * 4 * np.pi * z))
        ax.plot(z, env, color=c, label=lab)
    ax.set_xlabel("Distance from load (wavelengths)"); ax.set_ylabel("$|V(z)|/|V^+|$")
    ax.invert_xaxis(); ax.legend(fontsize=8.5, loc="upper right"); ax.set_ylim(0, 2.05)
    save(f, "fig09_standing_wave")


@fig("fig09_bh_curve")
def _():
    H = np.linspace(-1, 1, 400)
    up = np.tanh(3.2 * (H + 0.25)); dn = np.tanh(3.2 * (H - 0.25))
    f, ax = plt.subplots(figsize=(5.2, 3.8))
    ax.plot(H, up, color=INK); ax.plot(H, dn, color=INK)
    ax.plot(H, 0.55 * np.tanh(3.2 * (H + 0.06)), color=TEAL, ls="--", lw=1.2, label="Soft material")
    ax.axhline(0, color="#444", lw=0.8); ax.axvline(0, color="#444", lw=0.8)
    br = np.tanh(3.2 * 0.25)
    ax.plot(0, br, "o", color=COPPER); ax.text(0.05, br + 0.06, "$B_r$ (remanence)", color=COPPER, fontsize=9.5)
    ax.plot(-0.25, 0, "o", color=COPPER); ax.text(-0.95, 0.1, "$-H_c$ (coercive force)", color=COPPER, fontsize=9.5)
    ax.text(0.55, 1.08, "saturation", fontsize=9, color=GREY)
    ax.set_xlabel("Magnetic field intensity $H$"); ax.set_ylabel("Flux density $B$"); ax.set_xticks([]); ax.set_yticks([])
    ax.legend(loc="lower right", fontsize=8.5)
    save(f, "fig09_bh_curve")


# ------------------------------------------------------------------ Chapter 10
@fig("fig10_three_phase")
def _():
    t = np.linspace(0, 2, 800)
    f, ax = plt.subplots(figsize=(6.2, 2.9))
    for k, (c, lab) in enumerate([(INK, "$v_{an}$"), (COPPER, "$v_{bn}$"), (TEAL, "$v_{cn}$")]):
        ax.plot(t, np.cos(2 * np.pi * t - 2 * np.pi * k / 3), color=c, label=lab)
    ax.axhline(0, color="#555", lw=0.7)
    ax.set_xlabel("Time (cycles)"); ax.set_yticks([-1, 0, 1]); ax.legend(ncol=3, loc="upper right", fontsize=9)
    ax.set_ylim(-1.25, 1.5)
    save(f, "fig10_three_phase")


@fig("fig10_wye_delta")
def _():
    f, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.4))
    for a in (a1, a2):
        a.set_aspect("equal"); a.axis("off"); a.set_xlim(-1.6, 1.6); a.set_ylim(-1.35, 1.9)
    ang = [90, -30, 210]
    P = [np.array([np.cos(np.radians(g)), np.sin(np.radians(g))]) for g in ang]
    for p_, lab in zip(P, "abc"):
        a1.annotate("", xy=p_, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.8))
        a1.text(*(p_ * 1.13), f"$V_{{{lab}n}}$", ha="center", va="center", color=INK, fontsize=11)
    a1.annotate("", xy=P[0], xytext=P[1], arrowprops=dict(arrowstyle="-|>", color=COPPER, lw=1.6))
    a1.text(0.72, 0.45, "$V_{ab} = \\sqrt{3}\\,V_{an}\\angle 30°$", color=COPPER, fontsize=9.5)
    a1.set_title("Wye: line voltage = $\\sqrt{3}$ × phase voltage", fontsize=9.5, pad=14)
    tri = [np.array([0, 1.15]), np.array([1.0, -0.6]), np.array([-1.0, -0.6])]
    for i in range(3):
        p0, p1 = tri[i], tri[(i + 1) % 3]
        a2.plot([p0[0], p1[0]], [p0[1], p1[1]], color=INK, lw=2)
        m = (p0 + p1) / 2
        a2.text(*(m * 1.25), ["$I_{ab}$", "$I_{bc}$", "$I_{ca}$"][i], color=INK, fontsize=10, ha="center", va="center")
    for v, lab in zip(tri, "abc"):
        out = v * 1.35
        a2.annotate("", xy=v, xytext=out, arrowprops=dict(arrowstyle="-|>", color=COPPER, lw=1.5))
        a2.text(*(out * 1.05), f"$I_{lab}$", color=COPPER, ha="center", va="center", fontsize=11)
    a2.set_title("Delta: line current = $\\sqrt{3}$ × phase current", fontsize=9.5, pad=14)
    save(f, "fig10_wye_delta")


@fig("fig10_transformer")
def _():
    with schemdraw.Drawing(show=False) as d:
        d.config(unit=2.3)
        a = elm.Dot(open=True).label("$V_1$", loc="left")
        elm.Line().right().length(0.8)
        n = elm.Dot()
        elm.Resistor().right().label("$R_{eq}$")
        elm.Inductor().right().label("$jX_{eq}$")
        elm.Line().right().length(0.8)
        o = elm.Dot(open=True).label("$aV_2$", loc="right")
        elm.Line().at(n.center).down().length(0.6)
        elm.Line().left().length(0.7)
        elm.Resistor().down().label("$R_c$", loc="bottom")
        p1 = elm.Line().right().length(1.4)
        elm.Inductor().up().label("$jX_m$", loc="bottom")
        elm.Line().left().length(0.7)
        elm.Line().at(p1.center).down().length(0.6)
        bn = elm.Dot()
        elm.Line().left().tox(a.center)
        elm.Dot(open=True)
        elm.Line().at(bn.center).right().tox(o.center)
        elm.Dot(open=True)
    sch_save(d, "fig10_transformer")


@fig("fig10_torque_speed")
def _():
    s = np.linspace(0.001, 1, 500)
    R2, X = 0.05, 0.25
    T = (R2 / s) / ((0.03 + R2 / s) ** 2 + X ** 2)
    T = T / T.max() * 2.6
    n = 1 - s
    f, ax = plt.subplots(figsize=(5.8, 3.3))
    ax.plot(n, T, color=INK)
    k = np.argmax(T)
    ax.plot(n[k], T[k], "o", color=COPPER); ax.text(n[k] - 0.02, T[k] + 0.12, "Breakdown torque", ha="right", fontsize=9.5, color=COPPER)
    ax.plot(0, T[-1], "o", color=COPPER); ax.text(0.03, T[-1] + 0.14, "Starting torque", fontsize=9.5, color=COPPER)
    ax.axvspan(0.93, 1.0, color=TEAL, alpha=0.12); ax.text(0.9, 0.25, "Normal\noperating\nregion", ha="right", fontsize=9, color=TEAL)
    ax.set_xlabel("Speed (fraction of synchronous speed)"); ax.set_ylabel("Torque (per unit)"); ax.set_xlim(0, 1.02); ax.set_ylim(0, 3.0)
    save(f, "fig10_torque_speed")


# ------------------------------------------------------------------ Chapter 11
@fig("fig11_feedback")
def _():
    f, ax = blank(7.0, 2.4)
    ax.set_xlim(0, 14); ax.set_ylim(0, 4.6)
    ax.text(0.2, 3.1, "$R(s)$", fontsize=12)
    arrow(ax, (1.0, 3.0), (2.55, 3.0))
    ax.add_patch(Circle((2.9, 3.0), 0.35, fc="white", ec=INK, lw=1.3)); ax.text(2.55, 3.45, "+", fontsize=11); ax.text(2.55, 2.25, "−", fontsize=13)
    arrow(ax, (3.25, 3.0), (5.0, 3.0)); ax.text(3.7, 3.2, "$E(s)$", fontsize=10.5)
    box(ax, 5.0, 2.4, 2.2, 1.2, "Controller\n$G_c(s)$", fc=LIGHT, fs=10)
    arrow(ax, (7.2, 3.0), (8.4, 3.0))
    box(ax, 8.4, 2.4, 2.2, 1.2, "Plant\n$G_p(s)$", fc=LIGHT, fs=10)
    arrow(ax, (10.6, 3.0), (13.2, 3.0)); ax.text(12.4, 3.2, "$C(s)$", fontsize=12)
    ax.plot([11.8, 11.8, 9.2], [3.0, 0.9, 0.9], color="#333", lw=1.3)
    box(ax, 6.9, 0.35, 2.3, 1.1, "Sensor $H(s)$", fc="white", fs=10)
    ax.plot([6.9, 2.9], [0.9, 0.9], color="#333", lw=1.3); arrow(ax, (2.9, 0.9), (2.9, 2.62))
    save(f, "fig11_feedback")


@fig("fig11_step_specs")
def _():
    z, wn = 0.35, 1.0
    t = np.linspace(0, 16, 800); wd = wn * np.sqrt(1 - z * z)
    y = 1 - np.exp(-z * wn * t) * (np.cos(wd * t) + z / wd * np.sin(wd * t))
    f, ax = plt.subplots(figsize=(6.2, 3.4))
    ax.plot(t, y, color=INK)
    ax.axhline(1, color="#555", lw=0.8, ls=":")
    ax.axhspan(0.98, 1.02, color=TEAL, alpha=0.15)
    Tp = np.pi / wd; ymax = 1 + np.exp(-z * np.pi / np.sqrt(1 - z * z))
    ax.plot([Tp, Tp], [0, ymax], color=COPPER, ls="--", lw=1); ax.text(Tp + 0.15, 0.12, "$T_p = \\pi/\\omega_d$", color=COPPER)
    ax.annotate("", xy=(Tp + 1.2, ymax), xytext=(Tp + 1.2, 1.0), arrowprops=dict(arrowstyle="<->", color=RED))
    ax.text(Tp + 1.4, (ymax + 1) / 2, "% overshoot", color=RED, va="center")
    Ts = 4 / (z * wn)
    ax.plot([Ts, Ts], [0, 1.02], color=TEAL, ls="--", lw=1); ax.text(Ts + 0.15, 0.3, "$T_s \\approx 4/\\zeta\\omega_n$\n(2% band)", color=TEAL)
    ax.set_xlabel("Time (s)"); ax.set_ylabel("$c(t)$"); ax.set_ylim(0, 1.5)
    save(f, "fig11_step_specs")


@fig("fig11_root_locus")
def _():
    import numpy.polynomial.polynomial as Pn
    Ks = np.concatenate([np.linspace(0, 50, 800), np.linspace(50, 200, 400)])
    roots = []
    for K in Ks:
        r = np.roots([1, 6, 8, K]); roots.append(sorted(r, key=lambda z: (z.imag, z.real)))
    roots = np.array(roots)
    f, ax = plt.subplots(figsize=(5.4, 4.0))
    for k in range(3):
        ax.plot(roots[:, k].real, roots[:, k].imag, ".", ms=1.6, color=INK)
    for p_ in [0, -2, -4]:
        ax.plot(p_, 0, "x", ms=10, mew=2, color=COPPER)
    ax.axhline(0, color="#555", lw=0.7); ax.axvline(0, color="#555", lw=0.8)
    ax.plot([0, 0], [np.sqrt(8), -np.sqrt(8)], "o", color=RED, ms=5)
    ax.text(0.15, np.sqrt(8) + 0.2, "$j\\omega$ crossing at $K = 48$", color=RED, fontsize=9)
    ax.text(-0.85, -0.6, "breakaway", fontsize=9, color=GREY)
    ax.set_xlim(-7, 2.5); ax.set_ylim(-5, 5); ax.set_xlabel("$\\sigma$"); ax.set_ylabel("$j\\omega$")
    ax.text(-6.8, 4.3, "× open-loop poles", color=COPPER, fontsize=9.5)
    save(f, "fig11_root_locus")


@fig("fig11_bode")
def _():
    w = np.logspace(-1, 2, 600)
    G = 12 / (1j * w * (1j * w + 2) * (1j * w + 5))
    mag = 20 * np.log10(np.abs(G)); ph = np.degrees(np.unwrap(np.angle(G)))
    f, (a1, a2) = plt.subplots(2, 1, figsize=(6.0, 4.6), sharex=True)
    a1.semilogx(w, mag, color=INK); a1.axhline(0, color="#555", lw=0.8)
    a2.semilogx(w, ph, color=COPPER); a2.axhline(-180, color="#555", lw=0.8)
    wgc = w[np.argmin(np.abs(mag))]; wpc = w[np.argmin(np.abs(ph + 180))]
    pm = 180 + np.interp(wgc, w, ph); gm = -np.interp(wpc, w, mag)
    a1.annotate("", xy=(wpc, 0), xytext=(wpc, -gm), arrowprops=dict(arrowstyle="<->", color=RED)); a1.text(wpc * 1.1, -gm / 2, f"GM ≈ {gm:.0f} dB", color=RED, fontsize=9.5)
    a2.annotate("", xy=(wgc, -180), xytext=(wgc, -180 + pm), arrowprops=dict(arrowstyle="<->", color=TEAL)); a2.text(wgc * 0.35, -165, f"PM ≈ {pm:.0f}°", color=TEAL, fontsize=9.5)
    a1.axvline(wgc, color=TEAL, ls=":", lw=0.9); a2.axvline(wgc, color=TEAL, ls=":", lw=0.9)
    a1.axvline(wpc, color=RED, ls=":", lw=0.9); a2.axvline(wpc, color=RED, ls=":", lw=0.9)
    a1.set_ylabel("Magnitude (dB)"); a2.set_ylabel("Phase (°)"); a2.set_xlabel("$\\omega$ (rad/s)")
    a1.set_ylim(-60, 40); a2.set_ylim(-270, -60)
    save(f, "fig11_bode")


# ------------------------------------------------------------------ Chapter 12
@fig("fig12_am")
def _():
    t = np.linspace(0, 2, 4000)
    m = 0.5
    env = 1 + m * np.cos(2 * np.pi * t)
    f, ax = plt.subplots(figsize=(6.4, 2.8))
    ax.plot(t, env * np.cos(2 * np.pi * 25 * t), color=INK, lw=0.8)
    ax.plot(t, env, color=COPPER, ls="--", lw=1.4); ax.plot(t, -env, color=COPPER, ls="--", lw=1.4)
    ax.annotate("", xy=(0, 1.5), xytext=(0, -1.5), arrowprops=dict(arrowstyle="<->", color=RED)); ax.text(-0.16, 1.55, "$V_{max}$", color=RED)
    ax.annotate("", xy=(0.5, 0.5), xytext=(0.5, -0.5), arrowprops=dict(arrowstyle="<->", color=TEAL, lw=1.6)); ax.text(0.42, -0.85, "$V_{min}$", color=TEAL, fontsize=11, bbox=dict(fc="white", ec="none"))
    ax.set_yticks([]); ax.set_xlabel("Time (message periods)"); ax.set_ylim(-1.8, 1.8)
    save(f, "fig12_am")


@fig("fig12_spectrum")
def _():
    f, ax = plt.subplots(figsize=(5.8, 2.8))
    for x, h, c, lab in [(-1, 0.45, COPPER, "LSB\n$f_c - f_m$"), (0, 1.0, INK, "Carrier\n$f_c$"), (1, 0.45, COPPER, "USB\n$f_c + f_m$")]:
        ax.plot([x, x], [0, h], color=c, lw=3); ax.plot(x, h, "o", color=c)
        ax.text(x, h + 0.08, lab, ha="center", fontsize=9.5, color=c)
    ax.annotate("", xy=(-1, -0.12), xytext=(1, -0.12), arrowprops=dict(arrowstyle="<->", color=GREY)); ax.text(0, -0.24, "Bandwidth $2f_m$", ha="center", color=GREY, fontsize=9.5)
    ax.set_xlim(-2, 2); ax.set_ylim(-0.32, 1.35); ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    ax.spines["left"].set_visible(False); ax.set_xlabel("Frequency")
    save(f, "fig12_spectrum")


@fig("fig12_qam")
def _():
    f, ax = plt.subplots(figsize=(3.8, 3.8))
    g = [0, 1, 3, 2]
    for i, x in enumerate([-3, -1, 1, 3]):
        for j, y in enumerate([-3, -1, 1, 3]):
            ax.plot(x, y, "o", color=INK, ms=8)
            ax.text(x, y + 0.42, f"{g[i]:02b}{g[j]:02b}", ha="center", fontsize=7.5, color=COPPER)
    ax.axhline(0, color="#555", lw=0.8); ax.axvline(0, color="#555", lw=0.8)
    ax.set_xlim(-4.2, 4.2); ax.set_ylim(-4.2, 4.4); ax.set_aspect("equal")
    ax.set_xlabel("In-phase (I)"); ax.set_ylabel("Quadrature (Q)"); ax.set_xticks([]); ax.set_yticks([])
    save(f, "fig12_qam")


if __name__ == "__main__":
    names = sys.argv[1:] or list(FIGS)
    for n in names:
        FIGS[n]()
        print("made", n)
