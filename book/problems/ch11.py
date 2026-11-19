from common import *
import cmath

RAD = math.radians
D = math.degrees


def avg_power(r, tag):
    Vm = pick(r, [10, 50, 100, 170, 325])
    Im = pick(r, [0.5, 1, 2, 4, 10])
    tv, ti = pick(r, [0, 10, 30, 60]), pick(r, [-50, -30, -10, 0, 20, 40])
    th = tv - ti
    P = 0.5 * Vm * Im * math.cos(RAD(th))
    if abs(P) < 1e-9 * Vm * Im:
        P = 0.0
    return Problem(
        f"The voltage and current at the terminals of a load are <i>v</i> = {Vm} cos(ω<i>t</i> + {tv}°) V and <i>i</i> = {Im} cos(ω<i>t</i> {'+' if ti >= 0 else '−'} {abs(ti)}°) A. Find the average power absorbed and the power factor.",
        [step("Phase difference", f"θ = θ<sub>v</sub> − θ<sub>i</sub> = {tv} − ({num(ti)}) = {th}°."),
         step("Average power (peak values)", f"<i>P</i> = ½<i>V</i><sub>m</sub><i>I</i><sub>m</sub> cos θ = 0.5 × {Vm} × {Im} × cos {th}° = {num(P)} W."),
         step("Same thing with RMS values", f"<i>V</i><sub>rms</sub><i>I</i><sub>rms</sub> cos θ = {num(Vm / math.sqrt(2))} × {num(Im / math.sqrt(2))} × {num(math.cos(RAD(th)))} = {num(P)} W."),
         step("Power factor", f"pf = cos θ = {num(math.cos(RAD(th)))}, {'lagging (inductive)' if th > 0 else ('leading (capacitive)' if th < 0 else 'unity')}." + (" With θ = 90° the load is purely reactive: energy flows in and out every cycle but none is consumed." if abs(th) == 90 else ""))],
        f"<i>P</i> = {eng(P, 'W')}, pf = {num(math.cos(RAD(th)), 3)}", level=1, topic="average power")


def load_pqs(r, tag):
    V = pick(r, [110, 120, 230, 240])
    R = pick(r, [5, 10, 20, 30, 40])
    X = pick(r, [-20, -10, 5, 8, 15, 20, 30])
    Z = complex(R, X)
    I = V / abs(Z)
    S = V * V / Z.conjugate()
    return Problem(
        f"A load of impedance <b>Z</b> = {rect(Z)} Ω is connected to a {V} V RMS supply. Find the current, the real, reactive and apparent power, and the power factor.",
        [step("Current magnitude", f"|<b>Z</b>| = {num(abs(Z))} Ω, so <i>I</i> = {V}/{num(abs(Z))} = {num(I)} A RMS."),
         step("Real power", f"<i>P</i> = <i>I</i><sup>2</sup><i>R</i> = {num(I)}<sup>2</sup> × {R} = {num(S.real)} W."),
         step("Reactive power", f"<i>Q</i> = <i>I</i><sup>2</sup><i>X</i> = {num(S.imag)} var ({'absorbed: inductive' if X > 0 else 'negative: capacitive, it supplies vars'})."),
         step("Apparent power", f"<i>S</i> = <i>VI</i> = {num(abs(S))} VA; check √(<i>P</i><sup>2</sup> + <i>Q</i><sup>2</sup>) = {num(math.hypot(S.real, S.imag))} VA."),
         step("Power factor", f"pf = <i>P</i>/<i>S</i> = <i>R</i>/|<b>Z</b>| = {num(S.real / abs(S))} {'lagging' if X > 0 else 'leading'}.")],
        f"<i>P</i> = {eng(S.real, 'W')}, <i>Q</i> = {eng(S.imag, 'var')}, <i>S</i> = {eng(abs(S), 'VA')}, pf = {num(S.real / abs(S), 3)}", level=2, topic="complex power")


def multi_load(r, tag):
    V = pick(r, [230, 400, 415])
    loads = []
    for _ in range(pick(r, [2, 3])):
        P = pick(r, [2, 3, 5, 8, 10, 15]) * 1000
        pf = pick(r, [0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 1.0])
        lead = pf < 1 and r.random() < 0.25
        loads.append((P, pf, lead))
    Ptot = sum(P for P, _, _ in loads)
    Qs = [P * math.tan(math.acos(pf)) * (-1 if lead else 1) for P, pf, lead in loads]
    Qtot = sum(Qs)
    S = math.hypot(Ptot, Qtot)
    desc = "; ".join(f"{eng(P, 'W')} at pf {pf}{'' if pf == 1 else (' leading' if lead else ' lagging')}" for P, pf, lead in loads)
    rows = " ".join(f"Load {k+1}: <i>Q</i> = {num(P)} × tan(cos<sup>−1</sup> {pf}) = {num(q)} var." for k, ((P, pf, lead), q) in enumerate(zip(loads, Qs)))
    return Problem(
        f"A single-phase {V} V supply feeds the following loads in parallel: {desc}. Find the total real and reactive power, the overall power factor and the supply current.",
        [step("Reactive power of each load", "Use <i>Q</i> = <i>P</i> tan θ with θ = cos<sup>−1</sup>(pf); leading loads have negative <i>Q</i>. " + rows),
         step("Totals (real and reactive powers add separately)", f"<i>P</i> = {num(Ptot)} W; <i>Q</i> = {num(Qtot)} var."),
         step("Apparent power and pf", f"<i>S</i> = √(<i>P</i><sup>2</sup> + <i>Q</i><sup>2</sup>) = {num(S)} VA; pf = {num(Ptot / S, 3)} {'lagging' if Qtot > 0 else 'leading'}."),
         step("Supply current", f"<i>I</i> = <i>S</i>/<i>V</i> = {num(S)}/{V} = {num(S / V)} A. Apparent powers do not add arithmetically; only the complex powers do.")],
        f"<i>P</i> = {eng(Ptot, 'W')}, <i>Q</i> = {eng(Qtot, 'var')}, pf = {num(Ptot / S, 3)}, <i>I</i> = {eng(S / V, 'A')}", level=2, topic="multiple loads")


def pf_correct(r, tag):
    V = pick(r, [230, 240, 415])
    f = pick(r, [50, 50, 60])
    P = pick(r, [2, 5, 10, 20, 50]) * 1000
    pf1 = pick(r, [0.6, 0.65, 0.7, 0.75, 0.8])
    pf2 = pick(r, [0.9, 0.95, 0.98, 1.0])
    Q1 = P * math.tan(math.acos(pf1))
    Q2 = P * math.tan(math.acos(pf2))
    Qc = Q1 - Q2
    C = Qc / (2 * math.pi * f * V * V)
    return Problem(
        f"A {eng(P, 'W')} induction-motor load operates at a power factor of {pf1} lagging from a {V} V, {f} Hz supply. Find the capacitance that must be connected in parallel to raise the power factor to {pf2}{'' if pf2 == 1 else ' lagging'}, and the reduction in supply current.",
        [step("Original reactive power", f"θ<sub>1</sub> = cos<sup>−1</sup> {pf1} = {num(D(math.acos(pf1)))}°; <i>Q</i><sub>1</sub> = <i>P</i> tan θ<sub>1</sub> = {num(Q1)} var."),
         step("Target reactive power", f"θ<sub>2</sub> = cos<sup>−1</sup> {pf2} = {num(D(math.acos(pf2)))}°; <i>Q</i><sub>2</sub> = {num(Q2)} var."),
         step("Capacitor must supply", f"<i>Q</i><sub>C</sub> = {num(Q1)} − {num(Q2)} = {num(Qc)} var."),
         step("Capacitance", f"<i>Q</i><sub>C</sub> = <i>V</i><sup>2</sup>ω<i>C</i> ⇒ <i>C</i> = {num(Qc)}/({V}<sup>2</sup> × 2π × {f}) = {eng(C, 'F')}."),
         step("Current saving", f"Before: <i>I</i> = <i>P</i>/(<i>V</i> pf) = {num(P / (V * pf1))} A; after: {num(P / (V * pf2))} A. The real power is unchanged, but the cables, switchgear and transformer carry {num((1 - pf1 / pf2) * 100, 3)} % less current.")],
        f"<i>C</i> = {eng(C, 'F')}; current falls from {eng(P / (V * pf1), 'A')} to {eng(P / (V * pf2), 'A')}", level=2, topic="pf correction")


def ac_mpt(r, tag):
    Vth = pick(r, [10, 20, 50, 100])
    R = pick(r, [5, 8, 10, 25, 50])
    X = pick(r, [-20, -10, 5, 10, 15, 30])
    Zth = complex(R, X)
    P = Vth ** 2 / (4 * R)
    return Problem(
        f"A source has Thévenin equivalent <b>V</b><sub>Th</sub> = {Vth}∠0° V RMS and <b>Z</b><sub>Th</sub> = {rect(Zth)} Ω. Find the load impedance for maximum power transfer and the maximum power. How much power would a purely resistive load of {num(abs(Zth))} Ω receive instead?",
        [step("Conjugate match", f"For maximum power, <b>Z</b><sub>L</sub> = <b>Z</b><sub>Th</sub>* = {rect(Zth.conjugate())} Ω. The load reactance cancels the source reactance."),
         step("Maximum power", f"The circuit is then purely resistive (2<i>R</i>): <i>P</i><sub>max</sub> = <i>V</i><sub>Th</sub><sup>2</sup>/(4<i>R</i><sub>Th</sub>) = {Vth}<sup>2</sup>/(4 × {R}) = {eng(P, 'W')}."),
         step("Resistive load only", f"If only a resistor may be used, the best value is <i>R</i><sub>L</sub> = |<b>Z</b><sub>Th</sub>| = {num(abs(Zth))} Ω. Then <i>I</i> = {Vth}/|{rect(complex(R + abs(Zth), X))}| = {num(Vth / abs(complex(R + abs(Zth), X)))} A and <i>P</i> = <i>I</i><sup>2</sup><i>R</i><sub>L</sub> = {eng((Vth / abs(complex(R + abs(Zth), X))) ** 2 * abs(Zth), 'W')}, which is less than the conjugate-matched value.")],
        f"<b>Z</b><sub>L</sub> = {rect(Zth.conjugate())} Ω, <i>P</i><sub>max</sub> = {eng(P, 'W')}", level=3, topic="AC maximum power")


def rms_wave(r, tag):
    kind = r.randrange(4)
    Vm = pick(r, [5, 10, 12, 20, 100])
    if kind == 0:
        Vdc = pick(r, [2, 3, 5, 6])
        v = math.sqrt(Vdc ** 2 + Vm ** 2 / 2)
        return Problem(
            f"Find the RMS value of <i>v</i>(<i>t</i>) = {Vdc} + {Vm} sin ω<i>t</i> V, and the power it delivers to a 10 Ω resistor.",
            [step("Principle", "For a sum of a DC term and a sinusoid, the mean of the cross term over a period is zero, so the squares add: <i>V</i><sub>rms</sub><sup>2</sup> = <i>V</i><sub>dc</sub><sup>2</sup> + (<i>V</i><sub>m</sub>/√2)<sup>2</sup>."),
             step("Evaluate", f"<i>V</i><sub>rms</sub> = √({Vdc}<sup>2</sup> + {Vm}<sup>2</sup>/2) = {num(v)} V."),
             step("Power", f"<i>P</i> = <i>V</i><sub>rms</sub><sup>2</sup>/<i>R</i> = {num(v * v)}/10 = {num(v * v / 10)} W.")],
            f"<i>V</i><sub>rms</sub> = {num(v)} V, <i>P</i> = {num(v * v / 10)} W", level=2, topic="RMS")
    names = ["a symmetrical square wave of ±{0} V", "a symmetrical triangular wave of peak {0} V", "a half-wave rectified sine of peak {0} V"]
    vals = [Vm, Vm / math.sqrt(3), Vm / 2]
    explain = ["The square of the waveform is constant at <i>V</i><sub>m</sub><sup>2</sup>, so <i>V</i><sub>rms</sub> = <i>V</i><sub>m</sub>.",
               "Over a quarter period <i>v</i> = <i>V</i><sub>m</sub>(<i>t</i>/τ); the mean of (<i>t</i>/τ)<sup>2</sup> over 0 to τ is 1/3, so <i>V</i><sub>rms</sub> = <i>V</i><sub>m</sub>/√3.",
               "The squared sine averages to <i>V</i><sub>m</sub><sup>2</sup>/2 over the half-cycle it exists, and zero over the other half, giving a mean square of <i>V</i><sub>m</sub><sup>2</sup>/4, so <i>V</i><sub>rms</sub> = <i>V</i><sub>m</sub>/2."]
    k = kind - 1
    return Problem(
        f"Find the RMS value of {names[k].format(Vm)}, and the form factor (RMS ÷ rectified mean).",
        [step("Definition", "<i>V</i><sub>rms</sub> = √(mean of <i>v</i><sup>2</sup> over one period)."),
         step("Apply it", explain[k]),
         step("Result", f"<i>V</i><sub>rms</sub> = {num(vals[k])} V."),
         step("Form factor", f"Rectified mean = {num([Vm, Vm / 2, Vm / math.pi][k])} V, so form factor = {num(vals[k] / [Vm, Vm / 2, Vm / math.pi][k])}. Cheap 'average-responding' meters assume 1.111 (the sine value) and so misread other shapes.")],
        f"<i>V</i><sub>rms</sub> = {num(vals[k])} V", level=2, topic="RMS")


def ac_cost(r, tag):
    V = pick(r, [230, 240])
    I = pick(r, [2, 4.5, 8, 12])
    pf = pick(r, [0.7, 0.8, 0.85, 0.9])
    hrs = pick(r, [4, 6, 8, 10])
    days = pick(r, [5, 20, 22, 30])
    price = pick(r, [24.5, 26.0, 27.3])
    P = V * I * pf
    kwh = P / 1000 * hrs * days
    return Problem(
        f"A workshop machine draws {I} A at {V} V with a power factor of {pf}. It runs {hrs} h per day for {days} days. At {price}p per kWh, what does the energy cost, and why does the supplier not charge for the apparent power?",
        [step("Real power", f"<i>P</i> = <i>VI</i> cos φ = {V} × {I} × {pf} = {num(P)} W."),
         step("Energy", f"{num(P / 1000)} kW × {hrs * days} h = {num(kwh)} kWh."),
         step("Cost", f"{num(kwh)} × {price}p = {money(kwh * price / 100)}."),
         step("Why not VA?", "Domestic and small commercial meters record real energy only. Large industrial users, though, are often charged for kVA or reactive energy, which is the commercial reason for power-factor correction.")],
        f"{num(kwh)} kWh, {money(kwh * price / 100)}", level=1, topic="energy cost")


def kva(r, tag):
    S = pick(r, [5, 10, 25, 50, 100]) * 1000
    V = pick(r, [230, 240, 400])
    pf = pick(r, [0.7, 0.8, 0.9, 1.0])
    I = S / V
    return Problem(
        f"A single-phase transformer is rated at {eng(S, 'VA')}, {V} V on its secondary. What is the full-load current, and what real power can it supply to a load of power factor {pf}?",
        [step("Ratings are in VA", "Heating depends on current (and core loss on voltage), not on power factor, so transformers and generators are rated in volt-amperes."),
         step("Full-load current", f"<i>I</i> = <i>S</i>/<i>V</i> = {num(S)}/{V} = {num(I)} A."),
         step("Real power", f"<i>P</i> = <i>S</i> × pf = {num(S)} × {pf} = {eng(S * pf, 'W')}.")],
        f"<i>I</i> = {eng(I, 'A')}, <i>P</i> = {eng(S * pf, 'W')}", level=1, topic="ratings")


def from_meters(r, tag):
    V = pick(r, [100, 120, 230])
    I = pick(r, [2, 2.5, 4, 5])
    pf = pick(r, [0.4, 0.5, 0.6, 0.8])
    f = 50
    P = V * I * pf
    Z = V / I
    R = Z * pf
    X = Z * math.sin(math.acos(pf))
    L = X / (2 * math.pi * f)
    return Problem(
        f"A coil connected to a {V} V, {f} Hz supply draws {I} A, and a wattmeter reads {num(P)} W. Find the power factor, the resistance and the inductance of the coil.",
        [step("Power factor", f"pf = <i>P</i>/(<i>VI</i>) = {num(P)}/({V} × {I}) = {num(pf)}."),
         step("Impedance", f"|<b>Z</b>| = <i>V</i>/<i>I</i> = {num(Z)} Ω."),
         step("Resistance", f"The wattmeter sees only resistive loss: <i>R</i> = <i>P</i>/<i>I</i><sup>2</sup> = {num(R)} Ω."),
         step("Reactance and inductance", f"<i>X</i> = √(<i>Z</i><sup>2</sup> − <i>R</i><sup>2</sup>) = {num(X)} Ω; <i>L</i> = <i>X</i>/(2π<i>f</i>) = {eng(L, 'H')}.")],
        f"pf = {num(pf)}, <i>R</i> = {num(R)} Ω, <i>L</i> = {eng(L, 'H')}", level=3, topic="measurement")


def triangle(r, tag):
    P = pick(r, [1.2, 3, 4, 6, 8, 12]) * 1000
    pf = pick(r, [0.6, 0.8, 0.866, 0.9])
    S = P / pf
    Q = math.sqrt(S * S - P * P)
    return Problem(
        f"A load absorbs {eng(P, 'W')} at a lagging power factor of {pf}. Sketch the power triangle and find the apparent power and the reactive power.",
        [step("The power triangle", "Real power <i>P</i> is the horizontal side, reactive power <i>Q</i> the vertical side (upwards for lagging), and apparent power <i>S</i> the hypotenuse, at angle θ = cos<sup>−1</sup>(pf)."),
         step("Apparent power", f"<i>S</i> = <i>P</i>/pf = {eng(S, 'VA')}."),
         step("Reactive power", f"<i>Q</i> = √(<i>S</i><sup>2</sup> − <i>P</i><sup>2</sup>) = {eng(Q, 'var')}; θ = {num(D(math.acos(pf)))}°.")],
        f"<i>S</i> = {eng(S, 'VA')}, <i>Q</i> = {eng(Q, 'var')}", level=1, topic="power triangle")


def problems():
    plan = [(avg_power, 7), (load_pqs, 8), (multi_load, 8), (pf_correct, 7), (ac_mpt, 7), (rms_wave, 7), (ac_cost, 6), (kva, 6), (from_meters, 5), (triangle, 5)]
    return build(11, plan, 1111)
