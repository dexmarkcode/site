from common import *

RK = [1, 2, 4.7, 5, 10, 22, 47, 100]
CK = [1e-6, 2.2e-6, 4.7e-6, 10e-6, 22e-6, 47e-6, 100e-6]


def rc_charge(r, tag):
    V = pick(r, [5, 9, 12, 15, 24])
    R = pick(r, RK) * 1000
    C = pick(r, CK)
    tau = R * C
    t1 = tau * pick(r, [0.5, 1, 1.5, 2, 3])
    v1 = V * (1 - math.exp(-t1 / tau))
    frac = pick(r, [0.5, 0.8, 0.9, 0.95, 0.99])
    t2 = -tau * math.log(1 - frac)
    fig = ladder(tag, E("V", "V_s", f"{V} V"), [("S", E("SWc")), ("S", E("R", "R", eng(R, "Ω"))), ("P", E("C", "C", eng(C, "F")))])
    return Problem(
        f"The capacitor shown is initially uncharged and the switch closes at <i>t</i> = 0. Find (a) the time constant, (b) the capacitor voltage at <i>t</i> = {eng(t1, 's')}, and (c) the time taken to reach {int(frac * 100)} % of the supply voltage.",
        [step("Time constant", f"τ = <i>RC</i> = {num(R)} × {num(C)} = {eng(tau, 's')}."),
         step("Charging equation", f"<i>v</i><sub>C</sub>(<i>t</i>) = <i>V</i><sub>s</sub>(1 − e<sup>−<i>t</i>/τ</sup>) = {V}(1 − e<sup>−<i>t</i>/{eng(tau, 's')}</sup>)."),
         step("(b) Evaluate", f"<i>t</i>/τ = {num(t1 / tau)}; e<sup>−{num(t1 / tau)}</sup> = {num(math.exp(-t1 / tau))}; <i>v</i><sub>C</sub> = {V} × {num(1 - math.exp(-t1 / tau))} = {eng(v1, 'V', 4)}."),
         step("(c) Rearrange for time", f"1 − e<sup>−<i>t</i>/τ</sup> = {frac} ⇒ <i>t</i> = −τ ln(1 − {frac}) = {num(-math.log(1 - frac))}τ = {eng(t2, 's')}."),
         step("Rule of thumb", "After 5τ the capacitor is within 1 % of its final value; engineers usually call that 'fully charged'.")],
        f"τ = {eng(tau, 's')}, <i>v</i><sub>C</sub> = {eng(v1, 'V', 4)}, <i>t</i> = {eng(t2, 's')}", level=1, fig=fig, topic="RC charging")


def rc_discharge(r, tag):
    V0 = pick(r, [10, 12, 50, 100, 300])
    R = pick(r, RK) * 1000
    C = pick(r, CK)
    tau = R * C
    t1 = tau * pick(r, [0.25, 0.7, 1, 2, 4])
    v1 = V0 * math.exp(-t1 / tau)
    vs = pick(r, [0.5, 1, 2]) if V0 <= 20 else pick(r, [5, 30, 50])
    tsafe = tau * math.log(V0 / vs)
    fig = ladder(tag, E("C", "C", eng(C, "F")), [("S", E("SWc")), ("P", E("R", "R", eng(R, "Ω")))])
    return Problem(
        f"A {eng(C, 'F')} capacitor charged to {V0} V is discharged through {eng(R, 'Ω')} by closing the switch at <i>t</i> = 0. Find the voltage at <i>t</i> = {eng(t1, 's')}, the initial current, and the time for the voltage to fall to {vs} V.",
        [step("Time constant", f"τ = <i>RC</i> = {eng(tau, 's')}."),
         step("Discharge law", f"<i>v</i>(<i>t</i>) = {V0} e<sup>−<i>t</i>/τ</sup>."),
         step("Voltage at the given time", f"<i>v</i> = {V0} × e<sup>−{num(t1 / tau)}</sup> = {eng(v1, 'V', 4)}."),
         step("Initial current", f"At <i>t</i> = 0<sup>+</sup> the full {V0} V appears across <i>R</i>: <i>i</i>(0<sup>+</sup>) = {eng(V0 / R, 'A')}."),
         step("Time to fall", f"<i>t</i> = τ ln({V0}/{vs}) = {eng(tau, 's')} × {num(math.log(V0 / vs))} = {eng(tsafe, 's')}.")],
        f"<i>v</i> = {eng(v1, 'V', 4)}, <i>i</i>(0<sup>+</sup>) = {eng(V0 / R, 'A')}, <i>t</i> = {eng(tsafe, 's')}", level=1, fig=fig, topic="RC discharge")


def rl_energise(r, tag):
    V = pick(r, [6, 12, 24, 48])
    R = pick(r, [2, 4, 5, 10, 20, 50, 100])
    L = pick(r, [10e-3, 50e-3, 0.1, 0.5, 1, 2])
    tau = L / R
    If = V / R
    t1 = tau * pick(r, [0.5, 1, 2, 3])
    i1 = If * (1 - math.exp(-t1 / tau))
    fig = ladder(tag, E("V", "V_s", f"{V} V"), [("S", E("SWc")), ("S", E("R", "R", f"{R} Ω")), ("P", E("L", "L", eng(L, "H")))])
    return Problem(
        f"The switch in the RL circuit shown closes at <i>t</i> = 0. Find the time constant, the final current, the current at <i>t</i> = {eng(t1, 's')} and the inductor voltage at that instant.",
        [step("Initial and final values", f"The inductor current cannot jump, so <i>i</i>(0<sup>+</sup>) = 0. Finally <i>L</i> acts as a short: <i>I</i><sub>f</sub> = {V}/{R} = {eng(If, 'A')}."),
         step("Time constant", f"τ = <i>L</i>/<i>R</i> = {num(L)}/{R} = {eng(tau, 's')}."),
         step("Current", f"<i>i</i>(<i>t</i>) = {num(If)}(1 − e<sup>−<i>t</i>/τ</sup>); at <i>t</i> = {eng(t1, 's')}: <i>i</i> = {eng(i1, 'A', 4)}."),
         step("Inductor voltage", f"<i>v</i><sub>L</sub> = <i>V</i><sub>s</sub> − <i>iR</i> = {V} e<sup>−<i>t</i>/τ</sup> = {eng(V * math.exp(-t1 / tau), 'V', 4)}.")],
        f"τ = {eng(tau, 's')}, <i>I</i><sub>f</sub> = {eng(If, 'A')}, <i>i</i> = {eng(i1, 'A', 4)}", level=1, fig=fig, topic="RL energising")


def rl_decay(r, tag):
    I0 = pick(r, [0.5, 1, 2, 3, 5])
    R = pick(r, [5, 10, 20, 47, 100])
    L = pick(r, [20e-3, 0.1, 0.25, 1])
    tau = L / R
    t1 = tau * pick(r, [0.5, 1, 2])
    i1 = I0 * math.exp(-t1 / tau)
    W = 0.5 * L * I0 ** 2
    return Problem(
        f"An inductor of {eng(L, 'H')} carrying {I0} A is suddenly disconnected from its supply and simultaneously shorted through a {R} Ω resistor. Find the current after {eng(t1, 's')} and the total energy dissipated in the resistor.",
        [step("Decay equation", f"<i>i</i>(<i>t</i>) = <i>I</i><sub>0</sub> e<sup>−<i>t</i>/τ</sup> with τ = <i>L</i>/<i>R</i> = {eng(tau, 's')}."),
         step("Evaluate", f"<i>i</i> = {I0} × e<sup>−{num(t1 / tau)}</sup> = {eng(i1, 'A', 4)}."),
         step("Total energy", f"All the initial stored energy ends up as heat in <i>R</i>: <i>W</i> = ½<i>LI</i><sub>0</sub><sup>2</sup> = {eng(W, 'J')}. (Integrating <i>i</i><sup>2</sup><i>R</i> from 0 to ∞ gives the same result.)")],
        f"<i>i</i> = {eng(i1, 'A', 4)}, <i>W</i> = {eng(W, 'J')}", level=2, topic="RL decay")


def rc_thev(r, tag):
    V = pick(r, [10, 12, 20, 24])
    R1, R2 = pick(r, RK) * 1000, pick(r, RK) * 1000
    C = pick(r, CK)
    Vf = V * R2 / (R1 + R2)
    Rth = par(R1, R2)
    tau = Rth * C
    t1 = tau * pick(r, [0.5, 1, 2])
    fig = ladder(tag, E("V", "V_s", f"{V} V"), [("S", E("SWc")), ("S", E("R", "R_1", eng(R1, "Ω"))), ("P", E("R", "R_2", eng(R2, "Ω"))), ("P", E("C", "C", eng(C, "F")))])
    return Problem(
        f"The capacitor is uncharged when the switch closes at <i>t</i> = 0. Find an expression for <i>v</i><sub>C</sub>(<i>t</i>) and its value at <i>t</i> = {eng(t1, 's')}.",
        [step("Thévenin view from the capacitor", f"<i>V</i><sub>Th</sub> = {V} × {num(R2)}/{num(R1 + R2)} = {num(Vf)} V; <i>R</i><sub>Th</sub> = <i>R</i><sub>1</sub> ∥ <i>R</i><sub>2</sub> = {eng(Rth, 'Ω')}."),
         step("Time constant", f"τ = <i>R</i><sub>Th</sub><i>C</i> = {eng(tau, 's')}. A common mistake is to use <i>R</i><sub>1</sub> alone."),
         step("Universal first-order formula", f"<i>v</i>(<i>t</i>) = <i>v</i>(∞) + [<i>v</i>(0) − <i>v</i>(∞)]e<sup>−<i>t</i>/τ</sup> = {num(Vf)}(1 − e<sup>−<i>t</i>/{eng(tau, 's')}</sup>) V."),
         step("Evaluate", f"<i>v</i><sub>C</sub>({eng(t1, 's')}) = {num(Vf)} × {num(1 - math.exp(-t1 / tau))} = {eng(Vf * (1 - math.exp(-t1 / tau)), 'V', 4)}.")],
        f"<i>v</i><sub>C</sub> = {num(Vf)}(1 − e<sup>−<i>t</i>/τ</sup>) V, τ = {eng(tau, 's')}", level=2, fig=fig, topic="RC with Thévenin")


def rc_switch(r, tag):
    V = pick(r, [12, 15, 20, 24])
    R1, R2 = pick(r, RK) * 1000, pick(r, RK) * 1000
    C = pick(r, CK)
    v0 = V * R2 / (R1 + R2)
    tau = R1 * C
    t1 = tau * pick(r, [0.5, 1, 2])
    v1 = V + (v0 - V) * math.exp(-t1 / tau)
    fig = ladder(tag, E("V", "V_s", f"{V} V"), [("S", E("R", "R_1", eng(R1, "Ω"))), ("P", E("C", "C", eng(C, "F"))), ("S", E("SWo")), ("P", E("R", "R_2", eng(R2, "Ω")))])
    return Problem(
        f"The switch has been closed for a long time and opens at <i>t</i> = 0, disconnecting <i>R</i><sub>2</sub>. Find <i>v</i><sub>C</sub>(<i>t</i>) for <i>t</i> > 0 and evaluate it at {eng(t1, 's')}.",
        [step("Initial value (t < 0, steady state)", f"<i>C</i> is open; <i>R</i><sub>1</sub> and <i>R</i><sub>2</sub> form a divider: <i>v</i><sub>C</sub>(0<sup>−</sup>) = {V} × {num(R2)}/{num(R1 + R2)} = {num(v0)} V. Capacitor voltage cannot jump, so <i>v</i>(0<sup>+</sup>) = {num(v0)} V."),
         step("Final value", f"With <i>R</i><sub>2</sub> gone, the capacitor eventually charges to the full supply: <i>v</i>(∞) = {V} V."),
         step("Time constant", f"The capacitor now sees only <i>R</i><sub>1</sub>: τ = {eng(tau, 's')}."),
         step("Expression", f"<i>v</i><sub>C</sub>(<i>t</i>) = {V} − {num(V - v0)}e<sup>−<i>t</i>/τ</sup> V."),
         step("Evaluate", f"<i>v</i><sub>C</sub>({eng(t1, 's')}) = {eng(v1, 'V', 4)}.")],
        f"<i>v</i><sub>C</sub>(<i>t</i>) = {V} − {num(V - v0)}e<sup>−<i>t</i>/{eng(tau, 's')}</sup> V", level=3, fig=fig, topic="switched RC")


def rl_thev(r, tag):
    V = pick(r, [12, 20, 24, 30])
    R1, R2, R3 = pick(r, [2, 4, 6, 10]), pick(r, [4, 6, 12, 20]), pick(r, [1, 2, 3, 5])
    L = pick(r, [0.1, 0.2, 0.5, 1])
    Vth = V * R2 / (R1 + R2)
    Rt = par(R1, R2) + R3
    If = Vth / Rt
    tau = L / Rt
    fig = ladder(tag, E("V", "V_s", f"{V} V"), [("S", E("R", "R_1", f"{R1} Ω")), ("P", E("R", "R_2", f"{R2} Ω")), ("S", E("R", "R_3", f"{R3} Ω")), ("S", E("SWc")), ("P", E("L", "L", eng(L, "H")))])
    return Problem(
        "The switch closes at <i>t</i> = 0 with the inductor initially carrying no current. Find the inductor current <i>i</i><sub>L</sub>(<i>t</i>) and the time at which it reaches half its final value.",
        [step("Thévenin equivalent seen by the inductor", f"<i>V</i><sub>Th</sub> = {V} × {R2}/{R1 + R2} = {num(Vth)} V; <i>R</i><sub>Th</sub> = <i>R</i><sub>1</sub> ∥ <i>R</i><sub>2</sub> + <i>R</i><sub>3</sub> = {num(Rt)} Ω."),
         step("Final current and time constant", f"<i>I</i><sub>f</sub> = {num(Vth)}/{num(Rt)} = {eng(If, 'A', 4)}; τ = <i>L</i>/<i>R</i><sub>Th</sub> = {eng(tau, 's')}."),
         step("Expression", f"<i>i</i><sub>L</sub>(<i>t</i>) = {num(If)}(1 − e<sup>−<i>t</i>/τ</sup>) A."),
         step("Half-value time", f"<i>t</i> = τ ln 2 = 0.693τ = {eng(tau * math.log(2), 's')}.")],
        f"<i>i</i><sub>L</sub> = {num(If)}(1 − e<sup>−<i>t</i>/{eng(tau, 's')}</sup>) A; <i>t</i><sub>½</sub> = {eng(tau * math.log(2), 's')}", level=2, fig=fig, topic="RL with Thévenin")


def rc_energy(r, tag):
    V = pick(r, [5, 10, 12, 24, 50])
    R = pick(r, RK) * 1000
    C = pick(r, CK)
    W = 0.5 * C * V * V
    return Problem(
        f"A {eng(C, 'F')} capacitor is charged from zero to {V} V through a {eng(R, 'Ω')} resistor from a constant {V} V supply. How much energy is delivered by the supply, how much ends up in the capacitor, and how much is dissipated in the resistor?",
        [step("Charge delivered", f"<i>Q</i> = <i>CV</i> = {eng(C * V, 'C')}. The supply is at a constant {V} V, so it delivers <i>W</i><sub>s</sub> = <i>QV</i> = <i>CV</i><sup>2</sup> = {eng(2 * W, 'J')}."),
         step("Stored energy", f"<i>W</i><sub>C</sub> = ½<i>CV</i><sup>2</sup> = {eng(W, 'J')}."),
         step("Dissipated energy", f"<i>W</i><sub>R</sub> = {eng(2 * W, 'J')} − {eng(W, 'J')} = {eng(W, 'J')}."),
         step("The surprising part", f"Exactly half the energy is lost, whatever the value of <i>R</i>. A bigger resistor only stretches the loss out over a longer time (τ = {eng(R * C, 's')} here).")],
        f"supply {eng(2 * W, 'J')}; stored {eng(W, 'J')}; lost {eng(W, 'J')}", level=2, topic="RC energy")


def flyback(r, tag):
    I0 = pick(r, [0.1, 0.25, 0.5, 1])
    R = pick(r, [100, 470, 1000, 4700, 10000])
    L = pick(r, [10e-3, 50e-3, 0.2, 1])
    Vsup = pick(r, [12, 24])
    vpk = I0 * R
    return Problem(
        f"A relay coil ({eng(L, 'H')}) carries {eng(I0, 'A')} from a {Vsup} V supply. When the driving transistor turns off, the coil current is forced through a {eng(R, 'Ω')} protection resistor. Find the peak voltage across the coil and the time for the current to fall to 1 % of its initial value.",
        [step("Continuity of inductor current", f"At the instant of switching the coil still carries {eng(I0, 'A')}, now pushed through {eng(R, 'Ω')}."),
         step("Peak voltage", f"<i>v</i><sub>pk</sub> = <i>I</i><sub>0</sub><i>R</i> = {eng(vpk, 'V')}. The transistor sees roughly this plus the supply: about {eng(vpk + Vsup, 'V')}."),
         step("Decay time", f"τ = <i>L</i>/<i>R</i> = {eng(L / R, 's')}; to fall to 1 % takes τ ln 100 = 4.61τ = {eng(4.61 * L / R, 's')}."),
         step("Design trade-off", "A larger resistor releases the relay faster but stresses the transistor with a higher spike. A plain flyback diode gives the lowest spike but the slowest release.")],
        f"<i>v</i><sub>pk</sub> = {eng(vpk, 'V')}, <i>t</i> = {eng(4.61 * L / R, 's')}", level=3, topic="inductive kick")


def problems():
    plan = [(rc_charge, 9), (rc_discharge, 8), (rl_energise, 8), (rl_decay, 7), (rc_thev, 8), (rc_switch, 8), (rl_thev, 7), (rc_energy, 6), (flyback, 6)]
    return build(8, plan, 808)
