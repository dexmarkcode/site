from common import *

LV = [10e-3, 20e-3, 50e-3, 0.1, 0.2, 0.5, 1]
CVv = [1e-6, 2.2e-6, 4.7e-6, 10e-6, 22e-6, 47e-6, 100e-6]


def nice(x):
    """Round to a tidy two-significant-figure value."""
    e = math.floor(math.log10(x))
    return round(x / 10 ** e, 1) * 10 ** e


def regime(alpha, w0):
    if abs(alpha - w0) / w0 < 1e-9:
        return "critically damped"
    return "overdamped" if alpha > w0 else "underdamped"


def series_LC(r, factor):
    L, C = pick(r, LV), pick(r, CVv)
    Rc = 2 * math.sqrt(L / C)
    R = nice(Rc * factor)
    return L, C, R


def classify_series(r, tag):
    L, C, R = series_LC(r, pick(r, [0.2, 0.4, 0.7, 1.5, 2.5, 4]))
    a = R / (2 * L)
    w0 = 1 / math.sqrt(L * C)
    reg = regime(a, w0)
    extra = (f"Roots: <i>s</i> = −α ± √(α<sup>2</sup> − ω<sub>0</sub><sup>2</sup>) = {num(-a + math.sqrt(a * a - w0 * w0))} and {num(-a - math.sqrt(a * a - w0 * w0))} s<sup>−1</sup>, both real and negative."
             if a > w0 else f"Damped natural frequency ω<sub>d</sub> = √(ω<sub>0</sub><sup>2</sup> − α<sup>2</sup>) = {num(math.sqrt(w0 * w0 - a * a))} rad/s, so the response rings at about {eng(math.sqrt(w0 * w0 - a * a) / (2 * math.pi), 'Hz')}.")
    fig = ladder(tag, E("C", "C", eng(C, "F")), [("S", E("SWc")), ("S", E("R", "R", eng(R, "Ω"))), ("P", E("L", "L", eng(L, "H")))])
    return Problem(
        "For the source-free series RLC circuit shown, find the neper frequency α, the undamped natural frequency ω<sub>0</sub> and the damping ratio, and state the type of response.",
        [step("Series RLC formulas", "α = <i>R</i>/(2<i>L</i>), ω<sub>0</sub> = 1/√(<i>LC</i>), ζ = α/ω<sub>0</sub>."),
         step("Neper frequency", f"α = {num(R)}/(2 × {num(L)}) = {num(a)} s<sup>−1</sup>."),
         step("Natural frequency", f"ω<sub>0</sub> = 1/√({num(L)} × {num(C)}) = {num(w0)} rad/s."),
         step("Damping ratio", f"ζ = {num(a / w0)}, so the circuit is <b>{reg}</b>."),
         step("Detail", extra)],
        f"α = {num(a)} s<sup>−1</sup>, ω<sub>0</sub> = {num(w0)} rad/s, {reg}", level=1, fig=fig, topic="series RLC")


def classify_parallel(r, tag):
    L, C = pick(r, LV), pick(r, CVv)
    Rc = 0.5 * math.sqrt(L / C)
    R = nice(Rc * pick(r, [0.3, 0.6, 1.8, 3, 6]))
    a = 1 / (2 * R * C)
    w0 = 1 / math.sqrt(L * C)
    reg = regime(a, w0)
    fig = ladder(tag, E("R", "R", eng(R, "Ω")), [("P", E("L", "L", eng(L, "H"))), ("P", E("C", "C", eng(C, "F")))])
    return Problem(
        "Classify the natural response of the parallel RLC circuit shown.",
        [step("Parallel RLC formulas", "α = 1/(2<i>RC</i>) and ω<sub>0</sub> = 1/√(<i>LC</i>). Note that α is inversely proportional to <i>R</i>, the opposite of the series case."),
         step("Neper frequency", f"α = 1/(2 × {num(R)} × {num(C)}) = {num(a)} s<sup>−1</sup>."),
         step("Natural frequency", f"ω<sub>0</sub> = {num(w0)} rad/s."),
         step("Verdict", f"ζ = α/ω<sub>0</sub> = {num(a / w0)}: <b>{reg}</b>. " + ("A larger parallel resistance would reduce the damping further." if a < w0 else "Raising <i>R</i> would reduce the damping towards critical."))],
        f"α = {num(a)} s<sup>−1</sup>, ω<sub>0</sub> = {num(w0)} rad/s, {reg}", level=1, fig=fig, topic="parallel RLC")


def r_critical(r, tag):
    L, C = pick(r, LV), pick(r, CVv)
    w0 = 1 / math.sqrt(L * C)
    if r.random() < 0.5:
        R = 2 * math.sqrt(L / C)
        return Problem(
            f"What series resistance makes a series RLC circuit with <i>L</i> = {eng(L, 'H')} and <i>C</i> = {eng(C, 'F')} critically damped? What is the time constant of the resulting response?",
            [step("Condition", "Critical damping requires α = ω<sub>0</sub>, i.e. <i>R</i>/(2<i>L</i>) = 1/√(<i>LC</i>)."),
             step("Rearrange", "<i>R</i> = 2√(<i>L</i>/<i>C</i>)."),
             step("Substitute", f"<i>R</i> = 2√({num(L)}/{num(C)}) = {eng(R, 'Ω', 4)}."),
             step("Response", f"With α = ω<sub>0</sub> = {num(w0)} s<sup>−1</sup>, the response is (<i>A</i> + <i>Bt</i>)e<sup>−{num(w0)}<i>t</i></sup>, with characteristic time 1/α = {eng(1 / w0, 's')}.")],
            f"<i>R</i> = {eng(R, 'Ω', 4)}", level=2, topic="critical damping")
    R = 0.5 * math.sqrt(L / C)
    return Problem(
        f"A parallel RLC circuit has <i>L</i> = {eng(L, 'H')} and <i>C</i> = {eng(C, 'F')}. Find the value of <i>R</i> for critical damping, and say what happens if <i>R</i> is made larger.",
        [step("Condition", "1/(2<i>RC</i>) = 1/√(<i>LC</i>)."),
         step("Rearrange", "<i>R</i> = ½√(<i>L</i>/<i>C</i>)."),
         step("Substitute", f"<i>R</i> = 0.5 × √({num(L)}/{num(C)}) = {eng(R, 'Ω', 4)}."),
         step("Larger R", "Increasing a parallel resistance reduces α, so the circuit becomes underdamped and rings. In parallel circuits, more resistance means less damping.")],
        f"<i>R</i> = {eng(R, 'Ω', 4)}", level=2, topic="critical damping")


def over_nat(r, tag):
    while True:
        L, C, R = series_LC(r, pick(r, [1.6, 2, 2.5, 3]))
        a = R / (2 * L)
        w0 = 1 / math.sqrt(L * C)
        if a > w0 * 1.05:
            break
    V0 = pick(r, [10, 12, 20, 50, 100])
    s1 = -a + math.sqrt(a * a - w0 * w0)
    s2 = -a - math.sqrt(a * a - w0 * w0)
    A1 = s2 * V0 / (s2 - s1)
    A2 = -s1 * V0 / (s2 - s1)
    t1 = pick(r, [0.5, 1, 2]) / abs(s1)
    v1 = A1 * math.exp(s1 * t1) + A2 * math.exp(s2 * t1)
    fig = ladder(tag, E("C", "C", eng(C, "F")), [("S", E("SWc")), ("S", E("R", "R", eng(R, "Ω"))), ("P", E("L", "L", eng(L, "H")))])
    return Problem(
        f"In the circuit shown the capacitor is charged to {V0} V and the inductor current is zero when the switch closes. Find <i>v</i><sub>C</sub>(<i>t</i>) and evaluate it at <i>t</i> = {eng(t1, 's')}.",
        [step("Parameters", f"α = <i>R</i>/2<i>L</i> = {num(a)} s<sup>−1</sup>, ω<sub>0</sub> = {num(w0)} rad/s. Since α > ω<sub>0</sub>, the response is overdamped."),
         step("Characteristic roots", f"<i>s</i><sub>1</sub> = {num(s1)} s<sup>−1</sup>, <i>s</i><sub>2</sub> = {num(s2)} s<sup>−1</sup>."),
         step("Form of solution", "<i>v</i><sub>C</sub>(<i>t</i>) = <i>A</i><sub>1</sub>e<sup><i>s</i><sub>1</sub><i>t</i></sup> + <i>A</i><sub>2</sub>e<sup><i>s</i><sub>2</sub><i>t</i></sup>."),
         step("Initial conditions", f"<i>v</i><sub>C</sub>(0) = {V0} gives <i>A</i><sub>1</sub> + <i>A</i><sub>2</sub> = {V0}. Zero initial current means d<i>v</i><sub>C</sub>/d<i>t</i>(0) = 0: <i>s</i><sub>1</sub><i>A</i><sub>1</sub> + <i>s</i><sub>2</sub><i>A</i><sub>2</sub> = 0."),
         step("Solve", f"<i>A</i><sub>1</sub> = {num(A1)} V, <i>A</i><sub>2</sub> = {num(A2)} V."),
         step("Evaluate", f"<i>v</i><sub>C</sub>({eng(t1, 's')}) = {num(A1)}e<sup>{num(s1 * t1)}</sup> + ({num(A2)})e<sup>{num(s2 * t1)}</sup> = {eng(v1, 'V', 4)}.")],
        f"<i>v</i><sub>C</sub> = {num(A1)}e<sup>{num(s1)}<i>t</i></sup> {'+' if A2 >= 0 else '−'} {num(abs(A2))}e<sup>{num(s2)}<i>t</i></sup> V", level=3, fig=fig, topic="overdamped response")


def under_nat(r, tag):
    while True:
        L, C, R = series_LC(r, pick(r, [0.1, 0.2, 0.3, 0.5]))
        a = R / (2 * L)
        w0 = 1 / math.sqrt(L * C)
        if a < w0 * 0.95:
            break
    V0 = pick(r, [10, 12, 20, 50])
    wd = math.sqrt(w0 * w0 - a * a)
    B2 = a * V0 / wd
    t1 = pick(r, [0.25, 0.5, 1]) * 2 * math.pi / wd
    v1 = math.exp(-a * t1) * (V0 * math.cos(wd * t1) + B2 * math.sin(wd * t1))
    fig = ladder(tag, E("C", "C", eng(C, "F")), [("S", E("SWc")), ("S", E("R", "R", eng(R, "Ω"))), ("P", E("L", "L", eng(L, "H")))])
    return Problem(
        f"The capacitor is charged to {V0} V with zero inductor current when the switch closes. Find <i>v</i><sub>C</sub>(<i>t</i>), the ringing frequency, and <i>v</i><sub>C</sub> at <i>t</i> = {eng(t1, 's')}.",
        [step("Parameters", f"α = {num(a)} s<sup>−1</sup>, ω<sub>0</sub> = {num(w0)} rad/s; α < ω<sub>0</sub>, so the response is underdamped."),
         step("Damped frequency", f"ω<sub>d</sub> = √(ω<sub>0</sub><sup>2</sup> − α<sup>2</sup>) = {num(wd)} rad/s, i.e. <i>f</i><sub>d</sub> = {eng(wd / (2 * math.pi), 'Hz')}."),
         step("Form of solution", "<i>v</i><sub>C</sub> = e<sup>−α<i>t</i></sup>(<i>B</i><sub>1</sub> cos ω<sub>d</sub><i>t</i> + <i>B</i><sub>2</sub> sin ω<sub>d</sub><i>t</i>)."),
         step("Constants", f"<i>v</i>(0) = {V0} ⇒ <i>B</i><sub>1</sub> = {V0}. d<i>v</i>/d<i>t</i>(0) = −α<i>B</i><sub>1</sub> + ω<sub>d</sub><i>B</i><sub>2</sub> = 0 ⇒ <i>B</i><sub>2</sub> = α<i>V</i><sub>0</sub>/ω<sub>d</sub> = {num(B2)} V."),
         step("Evaluate", f"At <i>t</i> = {eng(t1, 's')}: e<sup>−α<i>t</i></sup> = {num(math.exp(-a * t1))}, ω<sub>d</sub><i>t</i> = {num(wd * t1)} rad; <i>v</i><sub>C</sub> = {eng(v1, 'V', 4)}.")],
        f"<i>v</i><sub>C</sub> = e<sup>−{num(a)}<i>t</i></sup>({V0} cos {num(wd)}<i>t</i> + {num(B2)} sin {num(wd)}<i>t</i>) V", level=3, fig=fig, topic="underdamped response")


def crit_nat(r, tag):
    L, C = pick(r, LV), pick(r, CVv)
    R = 2 * math.sqrt(L / C)
    a = R / (2 * L)
    V0 = pick(r, [10, 20, 50])
    t1 = pick(r, [0.5, 1, 2]) / a
    v1 = (V0 + a * V0 * t1) * math.exp(-a * t1)
    return Problem(
        f"A series RLC circuit with <i>L</i> = {eng(L, 'H')}, <i>C</i> = {eng(C, 'F')} and <i>R</i> = {eng(R, 'Ω', 4)} has its capacitor charged to {V0} V and zero current at <i>t</i> = 0. Find <i>v</i><sub>C</sub>(<i>t</i>) and its value at <i>t</i> = {eng(t1, 's')}.",
        [step("Check the damping", f"α = <i>R</i>/2<i>L</i> = {num(a)} s<sup>−1</sup> and ω<sub>0</sub> = {num(1 / math.sqrt(L * C))} rad/s are equal: critically damped."),
         step("Form", "<i>v</i><sub>C</sub>(<i>t</i>) = (<i>D</i><sub>1</sub> + <i>D</i><sub>2</sub><i>t</i>)e<sup>−α<i>t</i></sup>."),
         step("Constants", f"<i>D</i><sub>1</sub> = {V0}; d<i>v</i>/d<i>t</i>(0) = <i>D</i><sub>2</sub> − α<i>D</i><sub>1</sub> = 0 ⇒ <i>D</i><sub>2</sub> = {num(a * V0)} V/s."),
         step("Evaluate", f"<i>v</i><sub>C</sub> = ({V0} + {num(a * V0)} × {num(t1)})e<sup>−{num(a * t1)}</sup> = {eng(v1, 'V', 4)}.")],
        f"<i>v</i><sub>C</sub> = ({V0} + {num(a * V0)}<i>t</i>)e<sup>−{num(a)}<i>t</i></sup> V", level=3, topic="critically damped response")


def step_series(r, tag):
    while True:
        L, C, R = series_LC(r, pick(r, [0.1, 0.2, 0.3, 0.4]))
        a = R / (2 * L)
        w0 = 1 / math.sqrt(L * C)
        if a < w0 * 0.95:
            break
    Vs = pick(r, [5, 10, 12, 24])
    wd = math.sqrt(w0 * w0 - a * a)
    tp = math.pi / wd
    os_ = math.exp(-a * math.pi / wd)
    fig = ladder(tag, E("V", "V_s", f"{Vs} V"), [("S", E("SWc")), ("S", E("R", "R", eng(R, "Ω"))), ("S", E("L", "L", eng(L, "H"))), ("P", E("C", "C", eng(C, "F")))])
    return Problem(
        "The circuit shown is completely de-energised when the switch closes. Find the final capacitor voltage, the time of the first peak, the peak capacitor voltage and the percentage overshoot.",
        [step("Final value", f"In DC steady state <i>C</i> is open and <i>L</i> a short, so <i>v</i><sub>C</sub>(∞) = {Vs} V."),
         step("Parameters", f"α = {num(a)} s<sup>−1</sup>, ω<sub>0</sub> = {num(w0)} rad/s, ω<sub>d</sub> = {num(wd)} rad/s (underdamped)."),
         step("Step response", f"<i>v</i><sub>C</sub>(<i>t</i>) = {Vs} − e<sup>−α<i>t</i></sup>({Vs} cos ω<sub>d</sub><i>t</i> + {num(a * Vs / wd)} sin ω<sub>d</sub><i>t</i>)."),
         step("First peak", f"Peaks occur when the current is zero, i.e. sin ω<sub>d</sub><i>t</i> = 0, first at <i>t</i><sub>p</sub> = π/ω<sub>d</sub> = {eng(tp, 's')}."),
         step("Peak value and overshoot", f"<i>v</i><sub>pk</sub> = {Vs}(1 + e<sup>−απ/ω<sub>d</sub></sup>) = {Vs} × {num(1 + os_)} = {eng(Vs * (1 + os_), 'V', 4)}; overshoot = {num(os_ * 100, 3)} %.")],
        f"<i>v</i>(∞) = {Vs} V, <i>t</i><sub>p</sub> = {eng(tp, 's')}, <i>v</i><sub>pk</sub> = {eng(Vs * (1 + os_), 'V', 4)} ({num(os_ * 100, 3)} %)", level=3, fig=fig, topic="step response")


def energy_init(r, tag):
    L, C = pick(r, LV), pick(r, CVv)
    V0 = pick(r, [5, 10, 20, 50])
    I0 = pick(r, [0.1, 0.2, 0.5, 1])
    W = 0.5 * C * V0 ** 2 + 0.5 * L * I0 ** 2
    w0 = 1 / math.sqrt(L * C)
    Vmax = math.sqrt(2 * W / C)
    Imax = math.sqrt(2 * W / L)
    return Problem(
        f"An ideal (lossless) LC circuit has <i>L</i> = {eng(L, 'H')} and <i>C</i> = {eng(C, 'F')}. At <i>t</i> = 0 the capacitor voltage is {V0} V and the inductor current is {I0} A. Find the total energy, the oscillation frequency, and the maximum capacitor voltage and inductor current.",
        [step("Total energy", f"<i>W</i> = ½<i>CV</i><sub>0</sub><sup>2</sup> + ½<i>LI</i><sub>0</sub><sup>2</sup> = {eng(0.5 * C * V0 ** 2, 'J')} + {eng(0.5 * L * I0 ** 2, 'J')} = {eng(W, 'J')}."),
         step("Frequency", f"ω<sub>0</sub> = 1/√(<i>LC</i>) = {num(w0)} rad/s, <i>f</i><sub>0</sub> = {eng(w0 / (2 * math.pi), 'Hz')}."),
         step("Maximum capacitor voltage", f"All energy in <i>C</i>: <i>V</i><sub>max</sub> = √(2<i>W</i>/<i>C</i>) = {eng(Vmax, 'V', 4)}."),
         step("Maximum inductor current", f"All energy in <i>L</i>: <i>I</i><sub>max</sub> = √(2<i>W</i>/<i>L</i>) = {eng(Imax, 'A', 4)}. Energy swaps between the two stores twice per cycle.")],
        f"<i>W</i> = {eng(W, 'J')}, <i>f</i><sub>0</sub> = {eng(w0 / (2 * math.pi), 'Hz')}, <i>V</i><sub>max</sub> = {eng(Vmax, 'V', 4)}, <i>I</i><sub>max</sub> = {eng(Imax, 'A', 4)}", level=2, topic="energy exchange")


def design(r, tag):
    L = pick(r, [1e-3, 10e-3, 47e-3, 0.1])
    f0 = pick(r, [50, 100, 500, 1000, 5000])
    zeta = pick(r, [0.1, 0.25, 0.5, 0.707, 1])
    w0 = 2 * math.pi * f0
    C = 1 / (w0 * w0 * L)
    R = 2 * zeta * w0 * L
    return Problem(
        f"Design a series RLC circuit using a {eng(L, 'H')} inductor so that its undamped natural frequency is {eng(f0, 'Hz')} and its damping ratio is {zeta}. Find <i>C</i> and <i>R</i>.",
        [step("Angular frequency", f"ω<sub>0</sub> = 2π × {f0} = {num(w0)} rad/s."),
         step("Capacitance", f"From ω<sub>0</sub> = 1/√(<i>LC</i>): <i>C</i> = 1/(ω<sub>0</sub><sup>2</sup><i>L</i>) = {eng(C, 'F')}."),
         step("Resistance", f"ζ = α/ω<sub>0</sub> with α = <i>R</i>/2<i>L</i>, so <i>R</i> = 2ζω<sub>0</sub><i>L</i> = {eng(R, 'Ω')}."),
         step("Practical note", "Remember to subtract the inductor's own winding resistance from <i>R</i>. At low damping ratios it can be the dominant loss.")],
        f"<i>C</i> = {eng(C, 'F')}, <i>R</i> = {eng(R, 'Ω')}", level=2, topic="design")


def problems():
    plan = [(classify_series, 9), (classify_parallel, 8), (r_critical, 7), (over_nat, 8), (under_nat, 8), (crit_nat, 6), (step_series, 8), (energy_init, 6), (design, 6)]
    return build(9, plan, 909)
