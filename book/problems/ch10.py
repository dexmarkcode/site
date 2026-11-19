from common import *
import cmath
import numpy as np

D = math.degrees
RAD = math.radians


def sinus(r, tag):
    Vm = pick(r, [10, 25, 100, 170, 325, 340])
    f = pick(r, [50, 60, 400, 1000])
    ph = pick(r, [-60, -45, -30, 0, 20, 30, 45, 60])
    t = pick(r, [1, 2.5, 4, 5]) * 1e-3
    w = 2 * math.pi * f
    vt = Vm * math.sin(w * t + RAD(ph))
    phs = f" + {ph}°" if ph > 0 else (f" − {abs(ph)}°" if ph < 0 else "")
    return Problem(
        f"A voltage is described by <i>v</i>(<i>t</i>) = {Vm} sin({num(w)}<i>t</i>{phs}) V. State the amplitude, frequency, period and RMS value, and find <i>v</i> at <i>t</i> = {eng(t, 's')}.",
        [step("Read off amplitude and angular frequency", f"<i>V</i><sub>m</sub> = {Vm} V; ω = {num(w)} rad/s."),
         step("Frequency and period", f"<i>f</i> = ω/2π = {num(f)} Hz; <i>T</i> = 1/<i>f</i> = {eng(1 / f, 's')}."),
         step("RMS value", f"<i>V</i><sub>rms</sub> = <i>V</i><sub>m</sub>/√2 = {num(Vm / math.sqrt(2))} V."),
         step("Instantaneous value (careful with units)", f"ω<i>t</i> = {num(w * t)} rad = {num(D(w * t))}°; adding the phase gives {num(D(w * t) + ph)}°; <i>v</i> = {Vm} sin({num(D(w * t) + ph)}°) = {num(vt)} V."),
         step("Common trap", "Never mix radians and degrees inside the same bracket. Convert one of them first.")],
        f"<i>V</i><sub>m</sub> = {Vm} V, <i>f</i> = {f} Hz, <i>T</i> = {eng(1 / f, 's')}, <i>V</i><sub>rms</sub> = {num(Vm / math.sqrt(2))} V, <i>v</i> = {num(vt)} V", level=1, topic="sinusoids")


def convert(r, tag):
    if r.random() < 0.5:
        a, b = pick(r, [3, 4, 5, 6, 8, 10, 12, -3, -6]), pick(r, [4, -4, 5, 6, -8, 10, -12, 2])
        z = complex(a, b)
        quad = "second" if a < 0 and b > 0 else ("third" if a < 0 and b < 0 else ("fourth" if b < 0 else "first"))
        return Problem(
            f"Express the phasor <b>Z</b> = {rect(z)} in polar form.",
            [step("Magnitude", f"|<b>Z</b>| = √({num(a)}<sup>2</sup> + {num(b)}<sup>2</sup>) = {num(abs(z))}."),
             step("Angle", f"tan<sup>−1</sup>({num(b)}/{num(a)}) gives {num(D(math.atan(b / a)))}°, but the point lies in the {quad} quadrant, so θ = {num(D(cmath.phase(z)))}°." if a < 0 else f"θ = tan<sup>−1</sup>({num(b)}/{num(a)}) = {num(D(cmath.phase(z)))}° ({quad} quadrant)."),
             step("Result", f"<b>Z</b> = {polar(z)}. Always sketch the point roughly; it catches quadrant errors instantly.")],
            f"{polar(z)}", level=1, topic="phasors")
    m, th = pick(r, [5, 10, 20, 50, 120]), pick(r, [30, 45, 60, 120, -30, -60, 150, -135])
    z = cmath.rect(m, RAD(th))
    return Problem(
        f"Express the phasor <b>V</b> = {m}∠{th}° V in rectangular form.",
        [step("Real part", f"{m} cos({th}°) = {num(z.real)}."),
         step("Imaginary part", f"{m} sin({th}°) = {num(z.imag)}."),
         step("Result", f"<b>V</b> = {rect(z)} V.")],
        f"{rect(z)} V", level=1, topic="phasors")


def add_sines(r, tag):
    A, B = pick(r, [5, 10, 12, 20]), pick(r, [4, 8, 10, 15])
    pa, pb = pick(r, [0, 30, 45, 60]), pick(r, [-90, -60, -30, 90, 120])
    w = pick(r, [100, 314, 377, 1000])
    s = cmath.rect(A, RAD(pa)) + cmath.rect(B, RAD(pb))
    return Problem(
        f"Use phasors to express <i>v</i>(<i>t</i>) = {A} cos({w}<i>t</i> + {pa}°) + {B} cos({w}<i>t</i> {'+' if pb >= 0 else '−'} {abs(pb)}°) as a single sinusoid.",
        [step("Write each term as a phasor", f"<b>V</b><sub>1</sub> = {A}∠{pa}° = {rect(cmath.rect(A, RAD(pa)))}; <b>V</b><sub>2</sub> = {B}∠{pb}° = {rect(cmath.rect(B, RAD(pb)))}."),
         step("Add in rectangular form", f"<b>V</b> = {rect(s)}."),
         step("Convert to polar", f"<b>V</b> = {polar(s)}."),
         step("Back to the time domain", f"<i>v</i>(<i>t</i>) = {num(abs(s))} cos({w}<i>t</i> {'+' if cmath.phase(s) >= 0 else '−'} {num(abs(D(cmath.phase(s))))}°). The phasor method works only because both terms share the same frequency.")],
        f"{num(abs(s))} cos({w}<i>t</i> {'+' if cmath.phase(s) >= 0 else '−'} {num(abs(D(cmath.phase(s))))}°)", level=2, topic="phasor addition")


def reactance(r, tag):
    L = pick(r, [1e-3, 10e-3, 47e-3, 0.1, 0.5])
    C = pick(r, [10e-9, 100e-9, 1e-6, 10e-6, 47e-6])
    f = pick(r, [50, 60, 1000, 10e3])
    XL = 2 * math.pi * f * L
    XC = 1 / (2 * math.pi * f * C)
    return Problem(
        f"Find the reactances of a {eng(L, 'H')} inductor and a {eng(C, 'F')} capacitor at {eng(f, 'Hz')}. What happens to each if the frequency is doubled?",
        [step("Inductive reactance", f"<i>X</i><sub>L</sub> = 2π<i>fL</i> = 2π × {num(f)} × {num(L)} = {eng(XL, 'Ω')}."),
         step("Capacitive reactance", f"<i>X</i><sub>C</sub> = 1/(2π<i>fC</i>) = 1/(2π × {num(f)} × {num(C)}) = {eng(XC, 'Ω')}."),
         step("Doubling the frequency", f"<i>X</i><sub>L</sub> doubles to {eng(2 * XL, 'Ω')}; <i>X</i><sub>C</sub> halves to {eng(XC / 2, 'Ω')}. Inductors block high frequencies, capacitors block low ones.")],
        f"<i>X</i><sub>L</sub> = {eng(XL, 'Ω')}, <i>X</i><sub>C</sub> = {eng(XC, 'Ω')}", level=1, topic="reactance")


def series_ac(r, tag):
    V = pick(r, [10, 12, 24, 100, 230])
    f = pick(r, [50, 60, 1000])
    R = pick(r, [10, 22, 47, 100, 220])
    w = 2 * math.pi * f
    XL_t = pick(r, [0.5, 1, 2, 3]) * R
    XC_t = pick(r, [0.3, 0.8, 1.5, 2.5]) * R
    L = nice_val(XL_t / w)
    C = nice_val(1 / (w * XC_t))
    Z = complex(R, w * L - 1 / (w * C))
    I = V / Z
    fig = ladder(tag, E("Vac", "V_s", f"{V}∠0° V, {f} Hz"), [("S", E("R", "R", f"{R} Ω")), ("S", E("L", "L", eng(L, "H"))), ("P", E("C", "C", eng(C, "F")))])
    return Problem(
        "For the series RLC circuit shown (source given as an RMS phasor), find the impedance, the current, the phase angle, and the voltage across each element.",
        [step("Reactances", f"<i>X</i><sub>L</sub> = ω<i>L</i> = {num(w * L)} Ω; <i>X</i><sub>C</sub> = 1/ω<i>C</i> = {num(1 / (w * C))} Ω (ω = {num(w)} rad/s)."),
         step("Impedance", f"<b>Z</b> = <i>R</i> + j(<i>X</i><sub>L</sub> − <i>X</i><sub>C</sub>) = {rect(Z)} Ω = {polar(Z)} Ω."),
         step("Current", f"<b>I</b> = <b>V</b>/<b>Z</b> = {V}∠0°/{polar(Z)} = {polar(I)} A."),
         step("Interpretation", f"The current {'lags' if Z.imag > 0 else 'leads'} the voltage by {num(abs(D(cmath.phase(Z))))}°, so the circuit is net {'inductive' if Z.imag > 0 else 'capacitive'}."),
         step("Element voltages", f"<b>V</b><sub>R</sub> = {polar(I * R)} V; <b>V</b><sub>L</sub> = {polar(I * 1j * w * L)} V; <b>V</b><sub>C</sub> = {polar(I / (1j * w * C))} V. Their magnitudes need not add to {V} V; their phasor sum does.")],
        f"<b>Z</b> = {polar(Z)} Ω, <b>I</b> = {polar(I)} A", level=2, fig=fig, topic="series AC")


def nice_val(x):
    e = math.floor(math.log10(x))
    m = x / 10 ** e
    choices = [1, 1.5, 2.2, 3.3, 4.7, 6.8, 10]
    best = min(choices, key=lambda c: abs(c - m))
    return best * 10 ** e


def parallel_ac(r, tag):
    V = pick(r, [12, 24, 120, 230])
    f = pick(r, [50, 60])
    w = 2 * math.pi * f
    R = pick(r, [20, 50, 100, 200])
    L = nice_val(pick(r, [0.5, 1, 2]) * R / w)
    C = nice_val(1 / (w * pick(r, [0.7, 1.5, 3]) * R))
    Y = 1 / R + 1 / (1j * w * L) + 1j * w * C
    I = V * Y
    fig = ladder(tag, E("Vac", "V_s", f"{V}∠0° V, {f} Hz"), [("P", E("R", "R", f"{R} Ω")), ("P", E("L", "L", eng(L, "H"))), ("P", E("C", "C", eng(C, "F")))])
    return Problem(
        "Find the total admittance, the total supply current and the current in each branch of the parallel circuit shown.",
        [step("Branch admittances", f"<b>Y</b><sub>R</sub> = 1/{R} = {num(1 / R)} S; <b>Y</b><sub>L</sub> = 1/(jω<i>L</i>) = −j{num(1 / (w * L))} S; <b>Y</b><sub>C</sub> = jω<i>C</i> = j{num(w * C)} S."),
         step("Total admittance", f"<b>Y</b> = {rect(Y)} S = {polar(Y)} S."),
         step("Branch currents", f"<b>I</b><sub>R</sub> = {polar(V / R)} A, <b>I</b><sub>L</sub> = {polar(V / (1j * w * L))} A, <b>I</b><sub>C</sub> = {polar(V * 1j * w * C)} A."),
         step("Supply current", f"<b>I</b> = <b>VY</b> = {polar(I)} A. Its magnitude is less than the arithmetic sum because <b>I</b><sub>L</sub> and <b>I</b><sub>C</sub> partly cancel."),
         step("Equivalent impedance", f"<b>Z</b> = 1/<b>Y</b> = {polar(1 / Y)} Ω.")],
        f"<b>Y</b> = {polar(Y)} S, <b>I</b> = {polar(I)} A", level=2, fig=fig, topic="parallel AC")


def ac_divider(r, tag):
    R = pick(r, [1, 2.2, 4.7, 10]) * 1000
    C = pick(r, [10e-9, 47e-9, 100e-9])
    fc = 1 / (2 * math.pi * R * C)
    f = fc * pick(r, [0.2, 0.5, 1, 2, 5])
    Vin = pick(r, [1, 5, 10])
    w = 2 * math.pi * f
    H = 1 / (1 + 1j * w * R * C)
    fig = ladder(tag, E("Vac", "V_in", f"{Vin}∠0° V"), [("S", E("R", "R", eng(R, "Ω"))), ("P", E("C", "C", eng(C, "F"), node="$V_o$"))])
    return Problem(
        f"The RC network shown is driven at {eng(f, 'Hz')}. Find the output phasor <b>V</b><sub>o</sub> and the cut-off frequency of the network.",
        [step("Impedance divider", "<b>V</b><sub>o</sub> = <b>V</b><sub>in</sub> × <b>Z</b><sub>C</sub>/(<i>R</i> + <b>Z</b><sub>C</sub>) = <b>V</b><sub>in</sub>/(1 + jω<i>RC</i>)."),
         step("Evaluate ωRC", f"ω<i>RC</i> = 2π × {num(f)} × {num(R)} × {num(C)} = {num(w * R * C)}."),
         step("Output", f"<b>V</b><sub>o</sub> = {Vin}/(1 + j{num(w * R * C)}) = {polar(Vin * H)} V."),
         step("Cut-off frequency", f"<i>f</i><sub>c</sub> = 1/(2π<i>RC</i>) = {eng(fc, 'Hz')}. At <i>f</i><sub>c</sub> the output is 0.707 of the input and lags by 45°; this is a first-order low-pass filter.")],
        f"<b>V</b><sub>o</sub> = {polar(Vin * H)} V, <i>f</i><sub>c</sub> = {eng(fc, 'Hz')}", level=2, fig=fig, topic="AC divider")


def series_res(r, tag):
    L = pick(r, [1e-3, 10e-3, 50e-3, 0.1])
    C = pick(r, [10e-9, 100e-9, 1e-6, 10e-6])
    R = pick(r, [2, 5, 10, 20, 50])
    V = pick(r, [1, 5, 10])
    w0 = 1 / math.sqrt(L * C)
    f0 = w0 / (2 * math.pi)
    Q = w0 * L / R
    BW = f0 / Q
    return Problem(
        f"A series RLC circuit has <i>R</i> = {R} Ω, <i>L</i> = {eng(L, 'H')} and <i>C</i> = {eng(C, 'F')}, and is driven by {V} V RMS. Find the resonant frequency, the quality factor, the bandwidth, the current at resonance and the capacitor voltage at resonance.",
        [step("Resonant frequency", f"<i>f</i><sub>0</sub> = 1/(2π√(<i>LC</i>)) = {eng(f0, 'Hz')} (ω<sub>0</sub> = {num(w0)} rad/s)."),
         step("Quality factor", f"<i>Q</i> = ω<sub>0</sub><i>L</i>/<i>R</i> = {num(w0 * L)}/{R} = {num(Q)}."),
         step("Bandwidth", f"<i>B</i> = <i>f</i><sub>0</sub>/<i>Q</i> = <i>R</i>/(2π<i>L</i>) = {eng(BW, 'Hz')}."),
         step("Current at resonance", f"The reactances cancel, so <b>Z</b> = <i>R</i> and <i>I</i> = {V}/{R} = {eng(V / R, 'A')}."),
         step("Capacitor voltage", f"<i>V</i><sub>C</sub> = <i>QV</i> = {eng(Q * V, 'V')}. " + ("That is far larger than the supply, so component voltage ratings matter." if Q > 3 else "With a modest <i>Q</i>, magnification is small."))],
        f"<i>f</i><sub>0</sub> = {eng(f0, 'Hz')}, <i>Q</i> = {num(Q)}, <i>B</i> = {eng(BW, 'Hz')}, <i>V</i><sub>C</sub> = {eng(Q * V, 'V')}", level=2, topic="series resonance")


def parallel_res(r, tag):
    L = pick(r, [10e-6, 100e-6, 1e-3, 10e-3])
    C = pick(r, [100e-12, 1e-9, 10e-9, 100e-9])
    R = pick(r, [1, 5, 10, 47, 100]) * 1000
    w0 = 1 / math.sqrt(L * C)
    Q = R * math.sqrt(C / L)
    f0 = w0 / (2 * math.pi)
    return Problem(
        f"An ideal parallel RLC tank has <i>R</i> = {eng(R, 'Ω')}, <i>L</i> = {eng(L, 'H')}, <i>C</i> = {eng(C, 'F')}. Find the resonant frequency, <i>Q</i>, bandwidth and the impedance at resonance.",
        [step("Resonant frequency", f"<i>f</i><sub>0</sub> = 1/(2π√(<i>LC</i>)) = {eng(f0, 'Hz')}."),
         step("Quality factor (parallel form)", f"<i>Q</i> = <i>R</i>√(<i>C</i>/<i>L</i>) = ω<sub>0</sub><i>RC</i> = {num(Q)}."),
         step("Bandwidth", f"<i>B</i> = <i>f</i><sub>0</sub>/<i>Q</i> = 1/(2π<i>RC</i>) = {eng(f0 / Q, 'Hz')}."),
         step("Impedance at resonance", f"The inductor and capacitor admittances cancel, leaving <i>Z</i> = <i>R</i> = {eng(R, 'Ω')}, the maximum. That is why a tank circuit selects one frequency.")],
        f"<i>f</i><sub>0</sub> = {eng(f0, 'Hz')}, <i>Q</i> = {num(Q)}, <i>B</i> = {eng(f0 / Q, 'Hz')}", level=2, topic="parallel resonance")


def ac_nodal(r, tag):
    V1 = pick(r, [10, 20, 50, 100])
    V2a = pick(r, [0, 30, 60, 90, -30])
    V2m = pick(r, [5, 10, 20])
    R = pick(r, [2, 4, 5, 10])
    XL = pick(r, [2, 4, 5, 8])
    XC = pick(r, [2, 4, 5, 10])
    Z1, Z2, Z3 = complex(R, 0), complex(0, XL), complex(0, -XC)
    Vs2 = cmath.rect(V2m, RAD(V2a))
    VA = (V1 / Z1 + Vs2 / Z3) / (1 / Z1 + 1 / Z2 + 1 / Z3)
    fig = ladder(tag, E("Vac", "V_1", f"{V1}∠0° V"), [("S", E("R", "R", f"{R} Ω")), ("P", E("L", None, f"j{XL} Ω", node="A")), ("S", E("C", None, f"−j{XC} Ω")), ("P", E("Vac", "V_2", f"{V2m}∠{V2a}° V"))])
    IL = VA / Z2
    return Problem(
        "Using nodal analysis with phasors, find the voltage at node A and the current in the inductor. Impedances are marked on the diagram.",
        [step("Single unknown node", "Exactly as in DC, but with complex impedances: (<b>V</b><sub>A</sub> − <b>V</b><sub>1</sub>)/<b>Z</b><sub>R</sub> + <b>V</b><sub>A</sub>/<b>Z</b><sub>L</sub> + (<b>V</b><sub>A</sub> − <b>V</b><sub>2</sub>)/<b>Z</b><sub>C</sub> = 0."),
         step("Admittances", f"1/{R} = {num(1 / R)}; 1/(j{XL}) = −j{num(1 / XL)}; 1/(−j{XC}) = j{num(1 / XC)} S. Sum = {rect(1 / Z1 + 1 / Z2 + 1 / Z3)} S."),
         step("Source terms", f"<b>V</b><sub>1</sub>/<b>Z</b><sub>R</sub> + <b>V</b><sub>2</sub>/<b>Z</b><sub>C</sub> = {rect(V1 / Z1 + Vs2 / Z3)} A."),
         step("Solve", f"<b>V</b><sub>A</sub> = ({rect(V1 / Z1 + Vs2 / Z3)})/({rect(1 / Z1 + 1 / Z2 + 1 / Z3)}) = {polar(VA)} V."),
         step("Inductor current", f"<b>I</b><sub>L</sub> = <b>V</b><sub>A</sub>/j{XL} = {polar(IL)} A.")],
        f"<b>V</b><sub>A</sub> = {polar(VA)} V, <b>I</b><sub>L</sub> = {polar(IL)} A", level=3, fig=fig, topic="AC nodal")


def problems():
    plan = [(sinus, 7), (convert, 6), (add_sines, 6), (reactance, 7), (series_ac, 9), (parallel_ac, 7), (ac_divider, 6), (series_res, 7), (parallel_res, 5), (ac_nodal, 7)]
    return build(10, plan, 1010)
