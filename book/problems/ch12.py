from common import *
import cmath

RAD = math.radians
D = math.degrees
S3 = math.sqrt(3)
VLS = [400, 415, 400, 11000, 690, 3300]


def zload(r):
    R = pick(r, [6, 8, 10, 12, 15, 20, 30, 40])
    X = pick(r, [0, 4, 6, 8, 9, 12, 16, 20, -8, -10])
    return complex(R, X)


def yy(r, tag):
    VL = pick(r, [400, 415, 400, 690])
    Z = zload(r)
    Vp = VL / S3
    I = Vp / abs(Z)
    pf = Z.real / abs(Z)
    P = 3 * I * I * Z.real
    fig = star_delta(tag, "Z", [f"$Z$ = {rect(Z).replace(NBSP, ' ').replace(MINUS, '−')} Ω"] * 3, star=True, supply=["A", "B", "C"])
    return Problem(
        f"A balanced star-connected load with <b>Z</b> = {rect(Z)} Ω per phase is supplied from a {VL} V (line) three-phase system. Find the phase voltage, the line current, the power factor and the total power.",
        [step("Phase voltage (star)", f"<i>V</i><sub>ph</sub> = <i>V</i><sub>L</sub>/√3 = {VL}/1.732 = {num(Vp)} V."),
         step("Line current", f"In star, line current equals phase current: <i>I</i><sub>L</sub> = <i>V</i><sub>ph</sub>/|<b>Z</b>| = {num(Vp)}/{num(abs(Z))} = {num(I)} A."),
         step("Power factor", f"cos φ = <i>R</i>/|<b>Z</b>| = {num(pf)} {'lagging' if Z.imag > 0 else ('leading' if Z.imag < 0 else '(unity)')}."),
         step("Total power", f"<i>P</i> = √3 <i>V</i><sub>L</sub><i>I</i><sub>L</sub> cos φ = 1.732 × {VL} × {num(I)} × {num(pf)} = {eng(P, 'W')}. Check: 3<i>I</i><sup>2</sup><i>R</i> = {eng(3 * I * I * Z.real, 'W')}.")],
        f"<i>V</i><sub>ph</sub> = {num(Vp)} V, <i>I</i><sub>L</sub> = {eng(I, 'A')}, <i>P</i> = {eng(P, 'W')}", level=1, fig=fig, topic="star load")


def delta(r, tag):
    VL = pick(r, [400, 415, 400, 690])
    Z = zload(r)
    Iph = VL / abs(Z)
    IL = Iph * S3
    pf = Z.real / abs(Z)
    P = 3 * Iph * Iph * Z.real
    fig = star_delta(tag, "Z", [f"$Z$ = {rect(Z).replace(NBSP, ' ').replace(MINUS, '−')} Ω"] * 3, star=False, supply=["A", "B", "C"])
    return Problem(
        f"A balanced delta-connected load of <b>Z</b> = {rect(Z)} Ω per phase is connected to a {VL} V three-phase supply. Find the phase current, the line current and the total power.",
        [step("Phase voltage (delta)", f"Each impedance sits between two lines, so <i>V</i><sub>ph</sub> = <i>V</i><sub>L</sub> = {VL} V."),
         step("Phase current", f"<i>I</i><sub>ph</sub> = {VL}/{num(abs(Z))} = {num(Iph)} A."),
         step("Line current", f"<i>I</i><sub>L</sub> = √3 <i>I</i><sub>ph</sub> = {num(IL)} A, lagging the corresponding phase currents by 30°."),
         step("Total power", f"<i>P</i> = 3<i>I</i><sub>ph</sub><sup>2</sup><i>R</i> = {eng(P, 'W')}; also √3<i>V</i><sub>L</sub><i>I</i><sub>L</sub> cos φ = {eng(S3 * VL * IL * pf, 'W')}.")],
        f"<i>I</i><sub>ph</sub> = {eng(Iph, 'A')}, <i>I</i><sub>L</sub> = {eng(IL, 'A')}, <i>P</i> = {eng(P, 'W')}", level=2, fig=fig, topic="delta load")


def phasor_set(r, tag):
    Vp = pick(r, [230, 240, 120, 127, 6350])
    ang = pick(r, [0, 0, 30, -30, 90])
    seq = pick(r, ["positive (ABC)", "positive (ABC)", "negative (ACB)"])
    pos = seq.startswith("positive")
    a = ang
    b = ang - 120 if pos else ang + 120
    c = ang + 120 if pos else ang - 120
    Va, Vb = cmath.rect(Vp, RAD(a)), cmath.rect(Vp, RAD(b))
    Vab = Va - Vb

    def wrap(x):
        return (x + 180) % 360 - 180
    return Problem(
        f"In a balanced three-phase system with {seq} phase sequence, <b>V</b><sub>an</sub> = {Vp}∠{a}° V. Write down <b>V</b><sub>bn</sub>, <b>V</b><sub>cn</sub> and the line voltage <b>V</b><sub>ab</sub>.",
        [step("Phase displacement", f"The phases are 120° apart. In {'positive' if pos else 'negative'} sequence, <b>V</b><sub>bn</sub> {'lags' if pos else 'leads'} <b>V</b><sub>an</sub> by 120°."),
         step("Phase voltages", f"<b>V</b><sub>bn</sub> = {Vp}∠{num(wrap(b))}° V; <b>V</b><sub>cn</sub> = {Vp}∠{num(wrap(c))}° V."),
         step("Line voltage", f"<b>V</b><sub>ab</sub> = <b>V</b><sub>an</sub> − <b>V</b><sub>bn</sub> = {polar(Vab)} V."),
         step("Rule", f"Magnitude is √3 × {Vp} = {num(Vp * S3)} V, and the angle is shifted by {'+' if pos else '−'}30° from <b>V</b><sub>an</sub>. That is the source of the familiar 230 V / 400 V pair.")],
        f"<b>V</b><sub>bn</sub> = {Vp}∠{num(wrap(b))}°, <b>V</b><sub>cn</sub> = {Vp}∠{num(wrap(c))}°, <b>V</b><sub>ab</sub> = {polar(Vab)} V", level=1, topic="phase sequence")


def power_line(r, tag):
    VL = pick(r, VLS)
    P = pick(r, [7.5, 15, 22, 37, 55, 90, 250]) * 1000
    pf = pick(r, [0.8, 0.85, 0.88, 0.9])
    eta = pick(r, [0.88, 0.9, 0.92, 0.94])
    Pin = P / eta
    IL = Pin / (S3 * VL * pf)
    return Problem(
        f"A three-phase induction motor delivers {eng(P, 'W')} of mechanical output at an efficiency of {int(eta * 100)} % and a power factor of {pf}, from a {eng(VL, 'V')} supply. Find the line current.",
        [step("Electrical input", f"<i>P</i><sub>in</sub> = <i>P</i><sub>out</sub>/η = {num(P)}/{eta} = {num(Pin)} W."),
         step("Three-phase power equation", "<i>P</i> = √3 <i>V</i><sub>L</sub><i>I</i><sub>L</sub> cos φ, valid for star and delta alike."),
         step("Line current", f"<i>I</i><sub>L</sub> = {num(Pin)}/(1.732 × {VL} × {pf}) = {num(IL)} A."),
         step("Apparent power", f"<i>S</i> = √3<i>V</i><sub>L</sub><i>I</i><sub>L</sub> = {eng(S3 * VL * IL, 'VA')}, the figure used to size the supply cable and protective device.")],
        f"<i>I</i><sub>L</sub> = {eng(IL, 'A')}", level=1, topic="three-phase power")


def two_watt(r, tag):
    if r.random() < 0.5:
        W1 = pick(r, [5, 8, 10, 12, 15, 20]) * 1000
        W2 = pick(r, [-2, 1, 2, 4, 6, 9]) * 1000
        P = W1 + W2
        phi = math.atan(S3 * (W1 - W2) / (W1 + W2))
        return Problem(
            f"The two-wattmeter method is used on a balanced three-phase load, and the meters read {eng(W1, 'W')} and {eng(W2, 'W')}. Find the total power, the reactive power and the power factor.",
            [step("Total power", f"<i>P</i> = <i>W</i><sub>1</sub> + <i>W</i><sub>2</sub> = {eng(P, 'W')}." + (" A negative reading is perfectly genuine; the meter's current coil had to be reversed to read it." if W2 < 0 else "")),
             step("Reactive power", f"<i>Q</i> = √3(<i>W</i><sub>1</sub> − <i>W</i><sub>2</sub>) = 1.732 × {num(W1 - W2)} = {eng(S3 * (W1 - W2), 'var')}."),
             step("Phase angle", f"tan φ = √3(<i>W</i><sub>1</sub> − <i>W</i><sub>2</sub>)/(<i>W</i><sub>1</sub> + <i>W</i><sub>2</sub>) = {num(math.tan(phi))}, φ = {num(D(phi))}°."),
             step("Power factor", f"cos φ = {num(math.cos(phi), 3)}." + (" One meter reading negative always means pf < 0.5." if W2 < 0 else ""))],
            f"<i>P</i> = {eng(P, 'W')}, pf = {num(math.cos(phi), 3)}", level=3, topic="two-wattmeter method")
    VL = pick(r, [400, 415])
    IL = pick(r, [10, 20, 32, 50])
    pf = pick(r, [0.5, 0.7, 0.8, 0.9, 1.0])
    phi = math.acos(pf)
    W1 = VL * IL * math.cos(RAD(30) - phi)
    W2 = VL * IL * math.cos(RAD(30) + phi)
    W2 = 0.0 if abs(W2) < 1e-6 * W1 else W2
    pftxt = "at unity power factor" if pf == 1.0 else f"at a lagging power factor of {pf}"
    return Problem(
        f"A balanced load takes {IL} A per line from a {VL} V supply {pftxt}. What will each wattmeter read if the two-wattmeter method is used?",
        [step("Meter equations", "<i>W</i><sub>1</sub> = <i>V</i><sub>L</sub><i>I</i><sub>L</sub> cos(30° − φ), <i>W</i><sub>2</sub> = <i>V</i><sub>L</sub><i>I</i><sub>L</sub> cos(30° + φ)."),
         step("Angle", f"φ = cos<sup>−1</sup> {pf} = {num(D(phi))}°."),
         step("Readings", f"<i>W</i><sub>1</sub> = {VL} × {IL} × cos({num(30 - D(phi))}°) = {eng(W1, 'W')}; <i>W</i><sub>2</sub> = {VL} × {IL} × cos({num(30 + D(phi))}°) = {eng(W2, 'W')}."),
         step("Check", f"<i>W</i><sub>1</sub> + <i>W</i><sub>2</sub> = {eng(W1 + W2, 'W')}, which equals √3<i>V</i><sub>L</sub><i>I</i><sub>L</sub> cos φ = {eng(S3 * VL * IL * pf, 'W')}.")],
        f"<i>W</i><sub>1</sub> = {eng(W1, 'W')}, <i>W</i><sub>2</sub> = {eng(W2, 'W')}", level=3, topic="two-wattmeter method")


def pf3(r, tag):
    VL = pick(r, [400, 415])
    f = 50
    P = pick(r, [20, 30, 50, 75, 100]) * 1000
    pf1 = pick(r, [0.7, 0.75, 0.8])
    pf2 = pick(r, [0.92, 0.95, 0.98])
    Qc = P * (math.tan(math.acos(pf1)) - math.tan(math.acos(pf2)))
    Cd = Qc / 3 / (VL ** 2 * 2 * math.pi * f)
    Cy = Qc / 3 / ((VL / S3) ** 2 * 2 * math.pi * f)
    return Problem(
        f"A factory takes {eng(P, 'W')} at {pf1} lagging from a {VL} V, {f} Hz three-phase supply. Find the capacitance per phase needed to raise the power factor to {pf2} lagging, (a) with the capacitors in delta and (b) in star.",
        [step("Total reactive power to cancel", f"<i>Q</i><sub>C</sub> = <i>P</i>(tan φ<sub>1</sub> − tan φ<sub>2</sub>) = {num(P)} × ({num(math.tan(math.acos(pf1)))} − {num(math.tan(math.acos(pf2)))}) = {num(Qc)} var; per phase {num(Qc / 3)} var."),
         step("(a) Delta", f"Each capacitor sees {VL} V: <i>C</i> = <i>Q</i><sub>ph</sub>/(<i>V</i><sub>L</sub><sup>2</sup>ω) = {eng(Cd, 'F')}."),
         step("(b) Star", f"Each sees {num(VL / S3)} V: <i>C</i> = {eng(Cy, 'F')}, three times larger."),
         step("Choice", "Delta needs a third of the capacitance (but at full line voltage), which is why low-voltage correction banks are usually delta-connected.")],
        f"(a) {eng(Cd, 'F')} per phase; (b) {eng(Cy, 'F')} per phase", level=3, topic="three-phase pf correction")


def line_loss(r, tag):
    VL = pick(r, [400, 415])
    Zl = complex(pick(r, [0.1, 0.2, 0.5, 1]), pick(r, [0.1, 0.3, 0.5, 1]))
    Z = zload(r)
    Vp = VL / S3
    I = Vp / (Z + Zl)
    VLoad = I * Z
    Ploss = 3 * abs(I) ** 2 * Zl.real
    PL = 3 * abs(I) ** 2 * Z.real
    return Problem(
        f"A balanced star load of {rect(Z)} Ω per phase is fed through lines each of impedance {rect(Zl)} Ω from a {VL} V star-connected source. Find the line current, the load phase voltage and the power lost in the lines.",
        [step("Per-phase equivalent", f"Analyse one phase: source <b>V</b><sub>an</sub> = {num(Vp)}∠0° V driving <b>Z</b><sub>line</sub> + <b>Z</b> = {rect(Z + Zl)} Ω. The neutral carries nothing in a balanced system."),
         step("Line current", f"<b>I</b> = {num(Vp)}/{polar(Z + Zl)} = {polar(I)} A."),
         step("Load phase voltage", f"<b>V</b><sub>load</sub> = <b>IZ</b> = {polar(VLoad)} V (line value {num(abs(VLoad) * S3)} V)."),
         step("Losses and efficiency", f"Line loss = 3|<i>I</i>|<sup>2</sup><i>R</i><sub>line</sub> = {eng(Ploss, 'W')}; load power = {eng(PL, 'W')}; transmission efficiency = {num(PL / (PL + Ploss) * 100, 3)} %.")],
        f"<i>I</i> = {eng(abs(I), 'A')}, <i>V</i><sub>load</sub> = {eng(abs(VLoad), 'V', 4)}, loss {eng(Ploss, 'W')}", level=3, topic="line losses")


def star_vs_delta(r, tag):
    VL = pick(r, [400, 415])
    R = pick(r, [20, 30, 40, 50, 60])
    Py = 3 * (VL / S3) ** 2 / R
    Pd = 3 * VL ** 2 / R
    return Problem(
        f"Three identical {R} Ω heating elements are connected to a {VL} V three-phase supply, first in star and then in delta. Compare the line current and total power in each case.",
        [step("Star", f"Each element sees {num(VL / S3)} V: <i>I</i><sub>L</sub> = {num(VL / S3 / R)} A; <i>P</i> = 3 × {num(VL / S3)}<sup>2</sup>/{R} = {eng(Py, 'W')}."),
         step("Delta", f"Each element sees {VL} V: <i>I</i><sub>ph</sub> = {num(VL / R)} A, <i>I</i><sub>L</sub> = √3 × {num(VL / R)} = {num(S3 * VL / R)} A; <i>P</i> = {eng(Pd, 'W')}."),
         step("Comparison", "Delta takes exactly three times the power and three times the line current of star. This is the basis of the star–delta starter for motors and of two-rate heaters.")],
        f"star {eng(Py, 'W')}, delta {eng(Pd, 'W')} (ratio 3)", level=2, topic="star vs delta")


def y_delta_source_load(r, tag):
    VL = pick(r, [400, 415])
    Z = zload(r)
    if Z.imag == 0:
        Z = complex(Z.real, 9)
    Zy = Z / 3
    Vp = VL / S3
    IL = Vp / abs(Zy)
    Iph = IL / S3
    pf = Z.real / abs(Z)
    return Problem(
        f"A balanced delta load of {rect(Z)} Ω per phase is to be analysed using the per-phase star equivalent. The supply is {VL} V. Find the equivalent star impedance, the line current, the delta phase current and the total complex power.",
        [step("Δ → Y for a balanced load", f"<b>Z</b><sub>Y</sub> = <b>Z</b><sub>Δ</sub>/3 = {rect(Zy)} Ω."),
         step("Line current from the star equivalent", f"<i>I</i><sub>L</sub> = ({VL}/√3)/|<b>Z</b><sub>Y</sub>| = {num(Vp)}/{num(abs(Zy))} = {num(IL)} A."),
         step("Back to the delta", f"<i>I</i><sub>ph</sub> = <i>I</i><sub>L</sub>/√3 = {num(Iph)} A (check: {VL}/{num(abs(Z))} = {num(VL / abs(Z))} A)."),
         step("Complex power", f"<b>S</b> = 3<i>I</i><sub>L</sub><sup>2</sup><b>Z</b><sub>Y</sub> = {rect(3 * IL * IL * Zy)} VA, power factor {num(pf)} {'lagging' if Z.imag > 0 else 'leading'}.")],
        f"<b>Z</b><sub>Y</sub> = {rect(Zy)} Ω, <i>I</i><sub>L</sub> = {eng(IL, 'A')}, <i>I</i><sub>ph</sub> = {eng(Iph, 'A')}", level=2, topic="per-phase equivalent")


def problems():
    plan = [(yy, 8), (delta, 8), (y_delta_source_load, 7), (power_line, 7), (two_watt, 8), (pf3, 7), (line_loss, 7), (star_vs_delta, 6), (phasor_set, 8)]
    return build(12, plan, 1212)
