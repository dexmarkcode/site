from common import *

E0 = 8.854e-12
MU0 = 4 * math.pi * 1e-7
CV = [1e-9, 2.2e-9, 4.7e-9, 10e-9, 47e-9, 100e-9, 220e-9, 1e-6, 2.2e-6, 4.7e-6, 10e-6, 22e-6, 47e-6, 100e-6, 470e-6, 1000e-6]


def qcv(r, tag):
    C = pick(r, CV)
    V = pick(r, [5, 9, 12, 16, 25, 50, 100, 400])
    Q = C * V
    W = 0.5 * C * V * V
    return Problem(
        f"A {eng(C, 'F')} capacitor is charged to {V} V. Find the charge stored and the energy stored.",
        [step("Charge", f"<i>Q</i> = <i>CV</i> = {num(C)} × {V} = {eng(Q, 'C')}."),
         step("Energy", f"<i>W</i> = ½<i>CV</i><sup>2</sup> = 0.5 × {num(C)} × {V}<sup>2</sup> = {eng(W, 'J')}."),
         step("Alternative forms", f"Equivalently <i>W</i> = ½<i>QV</i> = {eng(0.5 * Q * V, 'J')} or <i>Q</i><sup>2</sup>/(2<i>C</i>); all agree.")],
        f"<i>Q</i> = {eng(Q, 'C')}, <i>W</i> = {eng(W, 'J')}", level=1, topic="capacitance")


def plates(r, tag):
    A_cm2 = pick(r, [4, 10, 25, 50, 100, 400])
    d_mm = pick(r, [0.05, 0.1, 0.2, 0.5, 1, 2])
    er = pick(r, [(1.0, "air"), (2.2, "PTFE"), (3.5, "Mylar"), (6.0, "mica"), (4.5, "glass")])
    C = E0 * er[0] * A_cm2 * 1e-4 / (d_mm * 1e-3)
    return Problem(
        f"A parallel-plate capacitor has plates of area {A_cm2} cm<sup>2</sup>, separated by {d_mm} mm of {er[1]} (relative permittivity {er[0]}). Find its capacitance. Take ε<sub>0</sub> = 8.854 × 10<sup>−12</sup> F/m.",
        [step("Convert to SI units", f"<i>A</i> = {A_cm2} × 10<sup>−4</sup> m<sup>2</sup> = {num(A_cm2 * 1e-4)} m<sup>2</sup>; <i>d</i> = {num(d_mm * 1e-3)} m."),
         step("Formula", "<i>C</i> = ε<sub>0</sub>ε<sub>r</sub><i>A</i>/<i>d</i>."),
         step("Substitute", f"<i>C</i> = 8.854 × 10<sup>−12</sup> × {er[0]} × {num(A_cm2 * 1e-4)}/{num(d_mm * 1e-3)} = {num(C)} F."),
         step("Result", f"<i>C</i> = {eng(C, 'F')}. Even generous plates give only picofarads to nanofarads, which is why practical capacitors roll or stack very thin films.")],
        f"<i>C</i> = {eng(C, 'F')}", level=2, topic="capacitance")


def cap_combo(r, tag):
    base = pick(r, [1e-6, 1e-9])
    C1, C2, C3 = [pick(r, [1, 2, 3, 4, 6, 10, 12]) * base for _ in range(3)]
    V = pick(r, [12, 24, 50, 100])
    Cp = C2 + C3
    Ceq = C1 * Cp / (C1 + Cp)
    Q = Ceq * V
    V1 = Q / C1
    V2 = V - V1
    fig = ladder(tag, E("V", "V", f"{V} V"), [("S", E("C", "C_1", eng(C1, "F"))), ("P", E("C", "C_2", eng(C2, "F"))), ("P", E("C", "C_3", eng(C3, "F")))])
    return Problem(
        "The capacitor network shown is fully charged from the supply. Find the equivalent capacitance, the charge drawn from the supply and the voltage across each capacitor.",
        [step("Parallel capacitors add", f"<i>C</i><sub>2</sub> + <i>C</i><sub>3</sub> = {eng(Cp, 'F')}."),
         step("Series capacitors combine like parallel resistors", f"<i>C</i><sub>eq</sub> = {eng(C1, 'F')} × {eng(Cp, 'F')}/({eng(C1, 'F')} + {eng(Cp, 'F')}) = {eng(Ceq, 'F')}."),
         step("Charge from supply", f"<i>Q</i> = <i>C</i><sub>eq</sub><i>V</i> = {eng(Q, 'C')}. Series elements carry the same charge, so <i>C</i><sub>1</sub> holds all of it."),
         step("Voltages", f"<i>V</i><sub>1</sub> = <i>Q</i>/<i>C</i><sub>1</sub> = {eng(V1, 'V')}; the parallel pair has {eng(V2, 'V')}. The smaller capacitance takes the larger share of the voltage."),
         step("Charges in the pair", f"<i>Q</i><sub>2</sub> = {eng(C2 * V2, 'C')}, <i>Q</i><sub>3</sub> = {eng(C3 * V2, 'C')}; together they equal <i>Q</i>.")],
        f"<i>C</i><sub>eq</sub> = {eng(Ceq, 'F')}, <i>V</i><sub>1</sub> = {eng(V1, 'V')}, <i>V</i><sub>2</sub> = <i>V</i><sub>3</sub> = {eng(V2, 'V')}", level=1, fig=fig, topic="capacitor networks")


def cap_ramp(r, tag):
    C = pick(r, [0.1e-6, 1e-6, 4.7e-6, 10e-6, 47e-6])
    dv = pick(r, [5, 10, 12, 20, 50])
    dt = pick(r, [10e-6, 100e-6, 1e-3, 5e-3, 20e-3])
    i = C * dv / dt
    return Problem(
        f"The voltage across a {eng(C, 'F')} capacitor rises linearly from 0 to {dv} V in {eng(dt, 's')}, stays constant for a while, then falls linearly back to zero in twice that time. Find the capacitor current in each interval.",
        [step("Governing law", "<i>i</i> = <i>C</i> d<i>v</i>/d<i>t</i>. The current depends on how fast the voltage changes, not on its value."),
         step("Rising ramp", f"d<i>v</i>/d<i>t</i> = {dv}/{num(dt)} = {num(dv / dt)} V/s, so <i>i</i> = {num(C)} × {num(dv / dt)} = {eng(i, 'A')}."),
         step("Flat section", "d<i>v</i>/d<i>t</i> = 0, so <i>i</i> = 0. A capacitor at constant voltage behaves as an open circuit."),
         step("Falling ramp", f"Slope is −{num(dv / (2 * dt))} V/s, so <i>i</i> = −{eng(i / 2, 'A')}; the current reverses as the capacitor gives its charge back.")],
        f"{eng(i, 'A')}, 0, −{eng(i / 2, 'A')}", level=2, topic="capacitor current")


def ind_ramp(r, tag):
    L = pick(r, [1e-3, 5e-3, 10e-3, 50e-3, 0.2, 0.5, 2])
    di = pick(r, [0.1, 0.5, 1, 2, 4])
    dt = pick(r, [1e-6, 10e-6, 1e-3, 10e-3, 50e-3])
    v = L * di / dt
    return Problem(
        f"The current in a {eng(L, 'H')} inductor rises steadily by {eng(di, 'A')} in {eng(dt, 's')}. What voltage appears across the inductor during this time?",
        [step("Governing law", "<i>v</i> = <i>L</i> d<i>i</i>/d<i>t</i>."),
         step("Rate of change of current", f"d<i>i</i>/d<i>t</i> = {num(di)}/{num(dt)} = {num(di / dt)} A/s."),
         step("Voltage", f"<i>v</i> = {num(L)} × {num(di / dt)} = {eng(v, 'V')}."),
         step("Comment", "Fast changes of inductor current demand large voltages, the principle behind ignition coils, boost converters and the arcs at relay contacts." if v > 50 else "The polarity opposes the change in current, as Lenz's law requires.")],
        f"<i>v</i> = {eng(v, 'V')}", level=2, topic="inductor voltage")


def ind_energy(r, tag):
    L = pick(r, [10e-3, 50e-3, 0.1, 0.5, 1, 2.5, 10])
    I = pick(r, [0.2, 0.5, 1, 2, 5, 10])
    W = 0.5 * L * I * I
    return Problem(
        f"How much energy is stored in the magnetic field of a {eng(L, 'H')} inductor carrying {eng(I, 'A')}? What current would double that energy?",
        [step("Energy", f"<i>W</i> = ½<i>LI</i><sup>2</sup> = 0.5 × {num(L)} × {num(I)}<sup>2</sup> = {eng(W, 'J')}."),
         step("Doubling the energy", f"Energy goes with <i>I</i><sup>2</sup>, so the current must rise by √2: <i>I</i> = {eng(I * math.sqrt(2), 'A')}.")],
        f"<i>W</i> = {eng(W, 'J')}; <i>I</i> = {eng(I * math.sqrt(2), 'A')}", level=1, topic="inductor energy")


def ind_combo(r, tag):
    base = pick(r, [1e-3, 1e-6])
    L1, L2, L3 = [pick(r, [2, 3, 4, 6, 8, 10, 12, 20]) * base for _ in range(3)]
    Lp = L2 * L3 / (L2 + L3)
    Leq = L1 + Lp
    return Problem(
        f"Inductors <i>L</i><sub>2</sub> = {eng(L2, 'H')} and <i>L</i><sub>3</sub> = {eng(L3, 'H')} are connected in parallel, and the pair is placed in series with <i>L</i><sub>1</sub> = {eng(L1, 'H')}. Assuming no mutual coupling, find the equivalent inductance.",
        [step("Inductors combine like resistors", "Series inductances add; parallel inductances combine by the reciprocal rule."),
         step("Parallel pair", f"<i>L</i><sub>2</sub> ∥ <i>L</i><sub>3</sub> = {eng(L2, 'H')} × {eng(L3, 'H')}/({eng(L2 + L3, 'H')}) = {eng(Lp, 'H')}."),
         step("Add the series inductor", f"<i>L</i><sub>eq</sub> = {eng(L1, 'H')} + {eng(Lp, 'H')} = {eng(Leq, 'H')}.")],
        f"<i>L</i><sub>eq</sub> = {eng(Leq, 'H')}", level=1, topic="inductor networks")


def charge_share(r, tag):
    C1 = pick(r, [1, 2, 4, 10, 22]) * 1e-6
    C2 = pick(r, [1, 2, 3, 5, 10]) * 1e-6
    V0 = pick(r, [10, 12, 20, 50, 100])
    Vf = C1 * V0 / (C1 + C2)
    W0 = 0.5 * C1 * V0 ** 2
    Wf = 0.5 * (C1 + C2) * Vf ** 2
    return Problem(
        f"A {eng(C1, 'F')} capacitor charged to {V0} V is connected across an uncharged {eng(C2, 'F')} capacitor. Find the final common voltage and the energy lost in the transfer.",
        [step("Charge is conserved", f"<i>Q</i> = {eng(C1, 'F')} × {V0} = {eng(C1 * V0, 'C')}, now shared by {eng(C1 + C2, 'F')}."),
         step("Final voltage", f"<i>V</i><sub>f</sub> = <i>Q</i>/(<i>C</i><sub>1</sub> + <i>C</i><sub>2</sub>) = {eng(Vf, 'V', 4)}."),
         step("Energy before and after", f"<i>W</i><sub>0</sub> = {eng(W0, 'J', 4)}; <i>W</i><sub>f</sub> = ½ × {eng(C1 + C2, 'F')} × {num(Vf)}<sup>2</sup> = {eng(Wf, 'J', 4)}."),
         step("Energy lost", f"Δ<i>W</i> = {eng(W0 - Wf, 'J', 4)} ({num((W0 - Wf) / W0 * 100, 3)} %). It is dissipated in wiring resistance and radiation, and remarkably it does not depend on how small that resistance is.")],
        f"<i>V</i><sub>f</sub> = {eng(Vf, 'V', 4)}, loss {eng(W0 - Wf, 'J', 4)}", level=3, topic="charge sharing")


def dc_steady(r, tag):
    V = pick(r, [10, 12, 20, 24])
    R1, R2 = pick(r, [2, 4, 5, 6, 10]), pick(r, [4, 6, 8, 10, 20])
    C = pick(r, [10e-6, 47e-6, 100e-6, 220e-6])
    L = pick(r, [10e-3, 50e-3, 0.1, 0.5])
    I = V / (R1 + R2)
    VC = I * R2
    fig = ladder(tag, E("V", "V_s", f"{V} V"), [("S", E("R", "R_1", f"{R1} Ω")), ("P", E("C", "C", eng(C, "F"))), ("S", E("L", "L", eng(L, "H"))), ("P", E("R", "R_2", f"{R2} Ω"))])
    WC, WL = 0.5 * C * VC ** 2, 0.5 * L * I ** 2
    return Problem(
        "The circuit shown has been connected for a long time. Find the inductor current, the capacitor voltage and the energy stored in each.",
        [step("DC steady-state models", "After a long time all derivatives are zero: a capacitor behaves as an open circuit, an inductor as a short circuit."),
         step("Redraw mentally", f"With <i>C</i> open and <i>L</i> shorted, the circuit is just <i>R</i><sub>1</sub> and <i>R</i><sub>2</sub> in series: <i>I</i> = {V}/({R1} + {R2}) = {num(I)} A. This is the inductor current."),
         step("Capacitor voltage", f"<i>C</i> is in parallel with the path <i>L</i> + <i>R</i><sub>2</sub>, and the shorted inductor drops nothing, so <i>V</i><sub>C</sub> = <i>IR</i><sub>2</sub> = {num(VC)} V."),
         step("Stored energies", f"<i>W</i><sub>C</sub> = ½ × {eng(C, 'F')} × {num(VC)}<sup>2</sup> = {eng(WC, 'J')}; <i>W</i><sub>L</sub> = ½ × {eng(L, 'H')} × {num(I)}<sup>2</sup> = {eng(WL, 'J')}.")],
        f"<i>I</i><sub>L</sub> = {eng(I, 'A')}, <i>V</i><sub>C</sub> = {eng(VC, 'V')}, <i>W</i><sub>C</sub> = {eng(WC, 'J')}, <i>W</i><sub>L</sub> = {eng(WL, 'J')}", level=2, fig=fig, topic="DC steady state")


def solenoid(r, tag):
    N = pick(r, [100, 200, 400, 500, 1000])
    d_cm = pick(r, [1, 2, 3, 5])
    l_cm = pick(r, [5, 10, 15, 20])
    mur = pick(r, [1, 1, 200, 1000])
    A = math.pi * (d_cm / 100) ** 2 / 4
    L = MU0 * mur * N ** 2 * A / (l_cm / 100)
    core = "an air core" if mur == 1 else f"a core of relative permeability {mur}"
    return Problem(
        f"Estimate the inductance of a long solenoid of {N} turns wound uniformly on {core}, of diameter {d_cm} cm and length {l_cm} cm. Take μ<sub>0</sub> = 4π × 10<sup>−7</sup> H/m.",
        [step("Cross-sectional area", f"<i>A</i> = π({num(d_cm / 100)})<sup>2</sup>/4 = {num(A)} m<sup>2</sup>."),
         step("Long-solenoid formula", "<i>L</i> = μ<sub>0</sub>μ<sub>r</sub><i>N</i><sup>2</sup><i>A</i>/<i>l</i>."),
         step("Substitute", f"<i>L</i> = 4π × 10<sup>−7</sup> × {mur} × {N}<sup>2</sup> × {num(A)}/{num(l_cm / 100)} = {eng(L, 'H')}."),
         step("Caveat", "The formula ignores end effects and assumes the core is not saturated; real inductance of short coils is noticeably lower.")],
        f"<i>L</i> ≈ {eng(L, 'H')}", level=2, topic="inductance")


def cap_integrate(r, tag):
    C = pick(r, [1e-6, 10e-6, 47e-6, 100e-6])
    I = pick(r, [0.1e-3, 1e-3, 5e-3, 20e-3])
    t = pick(r, [1e-3, 5e-3, 10e-3, 50e-3])
    v0 = pick(r, [0, 2, 5])
    v = v0 + I * t / C
    return Problem(
        f"A constant current of {eng(I, 'A')} is forced into a {eng(C, 'F')} capacitor whose initial voltage is {v0} V. Find the voltage after {eng(t, 's')}.",
        [step("Integral form", "<i>v</i>(<i>t</i>) = <i>v</i>(0) + (1/<i>C</i>)∫<i>i</i> d<i>t</i>."),
         step("Constant current", f"∫<i>i</i> d<i>t</i> = <i>It</i> = {num(I)} × {num(t)} = {eng(I * t, 'C')}."),
         step("Voltage", f"<i>v</i> = {v0} + {num(I * t)}/{num(C)} = {eng(v, 'V')}. This linear ramp is the basis of every integrating ADC and sawtooth generator.")],
        f"<i>v</i> = {eng(v, 'V')}", level=1, topic="capacitor voltage")


def problems():
    plan = [(qcv, 7), (plates, 6), (cap_combo, 7), (cap_ramp, 6), (ind_ramp, 6), (ind_energy, 6), (ind_combo, 6),
            (charge_share, 6), (dc_steady, 8), (solenoid, 4), (cap_integrate, 4)]
    return build(7, plan, 707)
