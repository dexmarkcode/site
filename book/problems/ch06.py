from common import *
import numpy as np

RV = [2, 3, 4, 5, 6, 8, 10, 12, 15, 20]


def sup_vv(r, tag):
    V1, V2 = pick(r, [10, 12, 20, 24, 30]), pick(r, [4, 5, 6, 9, 12])
    R1, R2, R3 = [pick(r, RV) for _ in range(3)]
    a = V1 * par(R2, R3) / (R1 + par(R2, R3))
    b = V2 * par(R1, R2) / (R3 + par(R1, R2))
    fig = ladder(tag, E("V", "V_1", f"{V1} V"), [("S", E("R", "R_1", f"{R1} Ω")), ("P", E("R", "R_2", f"{R2} Ω", node="A")), ("S", E("R", "R_3", f"{R3} Ω")), ("P", E("V", "V_2", f"{V2} V"))])
    return Problem(
        "Use the superposition theorem to find the voltage across <i>R</i><sub>2</sub> and the current through it.",
        [step("V<sub>1</sub> acting alone", f"Replace <i>V</i><sub>2</sub> by a short circuit. <i>R</i><sub>2</sub> ∥ <i>R</i><sub>3</sub> = {num(par(R2, R3))} Ω, so <i>V</i>′ = {V1} × {num(par(R2, R3))}/({R1} + {num(par(R2, R3))}) = {num(a)} V."),
         step("V<sub>2</sub> acting alone", f"Short <i>V</i><sub>1</sub>. <i>R</i><sub>1</sub> ∥ <i>R</i><sub>2</sub> = {num(par(R1, R2))} Ω, so <i>V</i>″ = {V2} × {num(par(R1, R2))}/({R3} + {num(par(R1, R2))}) = {num(b)} V."),
         step("Add the contributions", f"<i>V</i><sub>A</sub> = {num(a)} + {num(b)} = {num(a + b)} V; <i>I</i><sub>R2</sub> = {num(a + b)}/{R2} = {num((a + b) / R2)} A."),
         step("Warning", "Superposition works for voltages and currents, but never add the powers from each case. Power goes with the square of current, which is not linear.")],
        f"<i>V</i><sub>R2</sub> = {eng(a + b, 'V', 4)}, <i>I</i><sub>R2</sub> = {eng((a + b) / R2, 'A', 4)}", level=1, fig=fig, topic="superposition")


def sup_vi(r, tag):
    V1 = pick(r, [10, 12, 18, 24])
    Is = pick(r, [1, 2, 3, 4])
    R1, R2, R3 = [pick(r, RV) for _ in range(3)]
    i_a = V1 / (R1 + R2)
    i_b = Is * R1 / (R1 + R2)
    fig = ladder(tag, E("V", "V_1", f"{V1} V"), [("S", E("R", "R_1", f"{R1} Ω")), ("P", E("R", "R_2", f"{R2} Ω", cur="I_2")), ("S", E("R", "R_3", f"{R3} Ω")), ("P", E("I", "I_s", f"{Is} A"))])
    return Problem(
        "By superposition, find the downward current <i>I</i><sub>2</sub> in <i>R</i><sub>2</sub>.",
        [step("Voltage source alone", f"Open-circuit the current source (a dead current source is an open circuit). <i>R</i><sub>3</sub> then carries nothing, and <i>I</i><sub>2</sub>′ = {V1}/({R1} + {R2}) = {num(i_a)} A."),
         step("Current source alone", f"Short the voltage source. The {Is} A enters node A through <i>R</i><sub>3</sub> and splits between <i>R</i><sub>1</sub> and <i>R</i><sub>2</sub>: <i>I</i><sub>2</sub>″ = {Is} × {R1}/({R1} + {R2}) = {num(i_b)} A."),
         step("Total", f"<i>I</i><sub>2</sub> = {num(i_a)} + {num(i_b)} = {num(i_a + i_b)} A."),
         step("Note on R<sub>3</sub>", f"<i>R</i><sub>3</sub> never affects <i>I</i><sub>2</sub>: anything in series with an ideal current source is irrelevant to the rest of the circuit.")],
        f"<i>I</i><sub>2</sub> = {eng(i_a + i_b, 'A', 4)}", level=2, fig=fig, topic="superposition")


def thev(r, tag, mp=False):
    V = pick(r, [10, 12, 15, 20, 24, 30, 48])
    R1, R2, R3 = [pick(r, RV) for _ in range(3)]
    sc = pick(r, [1, 1000])
    R1, R2, R3 = R1 * sc, R2 * sc, R3 * sc
    Vth = V * R2 / (R1 + R2)
    Rth = R3 + par(R1, R2)
    fig = ladder(tag, E("V", "V_s", f"{V} V"), [("S", E("R", "R_1", eng(R1, "Ω"))), ("P", E("R", "R_2", eng(R2, "Ω"))), ("S", E("R", "R_3", eng(R3, "Ω")))])
    steps = [step("Open-circuit voltage", f"With a–b open, <i>R</i><sub>3</sub> carries no current, so <i>V</i><sub>Th</sub> is the voltage across <i>R</i><sub>2</sub>: {V} × {num(R2)}/({num(R1)} + {num(R2)}) = {num(Vth)} V."),
             step("Thévenin resistance", f"Kill the source (short it) and look back into a–b: <i>R</i><sub>Th</sub> = <i>R</i><sub>3</sub> + <i>R</i><sub>1</sub> ∥ <i>R</i><sub>2</sub> = {eng(R3, 'Ω')} + {eng(par(R1, R2), 'Ω')} = {eng(Rth, 'Ω')}.")]
    if not mp:
        RL = pick(r, [1, 2, 5, 10]) * sc
        IL = Vth / (Rth + RL)
        steps.append(step("Connect the load", f"<i>I</i><sub>L</sub> = <i>V</i><sub>Th</sub>/(<i>R</i><sub>Th</sub> + <i>R</i><sub>L</sub>) = {num(Vth)}/({num(Rth)} + {num(RL)}) = {eng(IL, 'A')}; <i>V</i><sub>L</sub> = {eng(IL * RL, 'V')}."))
        steps.append(step("Why bother?", "Once the Thévenin model is known, any number of different loads can be tried with one line of arithmetic each."))
        return Problem(f"Find the Thévenin equivalent of the network shown, as seen from terminals a–b. Hence find the current in a load of {eng(RL, 'Ω')} connected across a–b.",
                       steps, f"<i>V</i><sub>Th</sub> = {eng(Vth, 'V', 4)}, <i>R</i><sub>Th</sub> = {eng(Rth, 'Ω', 4)}, <i>I</i><sub>L</sub> = {eng(IL, 'A')}", level=2, fig=fig, topic="Thévenin")
    Pmax = Vth ** 2 / (4 * Rth)
    steps.append(step("Maximum power condition", f"Maximum power is transferred when <i>R</i><sub>L</sub> = <i>R</i><sub>Th</sub> = {eng(Rth, 'Ω')}."))
    steps.append(step("Maximum power", f"<i>P</i><sub>max</sub> = <i>V</i><sub>Th</sub><sup>2</sup>/(4<i>R</i><sub>Th</sub>) = {num(Vth)}<sup>2</sup>/(4 × {num(Rth)}) = {eng(Pmax, 'W')}."))
    steps.append(step("Efficiency at that point", "Exactly half the power generated is lost inside the source network, so efficiency is only 50 %. That is fine for signals, but no power company would run a grid this way."))
    return Problem("What load resistance connected across a–b of the network shown will absorb the maximum possible power, and what is that power?",
                   steps, f"<i>R</i><sub>L</sub> = {eng(Rth, 'Ω', 4)}, <i>P</i><sub>max</sub> = {eng(Pmax, 'W')}", level=2, fig=fig, topic="maximum power")


def thevenin(r, tag):
    return thev(r, tag)


def maxpower(r, tag):
    return thev(r, tag, mp=True)


def norton(r, tag):
    Is = pick(r, [1, 2, 3, 4, 5]) * pick(r, [1, 0.001])
    sc = 1 if Is >= 1 else 1000
    R1, R2, R3, R4 = [pick(r, RV) * sc for _ in range(4)]
    ibr = Is * R1 / (R1 + R2 + R3)
    Voc = ibr * R3
    Rn = R4 + par(R3, R1 + R2)
    In = Voc / Rn
    fig = ladder(tag, E("I", "I_s", eng(Is, "A")), [("P", E("R", "R_1", eng(R1, "Ω"))), ("S", E("R", "R_2", eng(R2, "Ω"))), ("P", E("R", "R_3", eng(R3, "Ω"))), ("S", E("R", "R_4", eng(R4, "Ω")))])
    return Problem(
        "Find the Norton equivalent of the network shown at terminals a–b.",
        [step("Norton resistance", f"Open the current source. Looking in from a–b: <i>R</i><sub>N</sub> = <i>R</i><sub>4</sub> + <i>R</i><sub>3</sub> ∥ (<i>R</i><sub>1</sub> + <i>R</i><sub>2</sub>) = {eng(R4, 'Ω')} + {eng(par(R3, R1 + R2), 'Ω')} = {eng(Rn, 'Ω')}."),
         step("Open-circuit voltage first (often easier)", f"With a–b open, <i>I</i><sub>s</sub> divides between <i>R</i><sub>1</sub> and the path <i>R</i><sub>2</sub> + <i>R</i><sub>3</sub>: current in <i>R</i><sub>3</sub> = {eng(Is, 'A')} × {num(R1)}/{num(R1 + R2 + R3)} = {eng(ibr, 'A')}; <i>V</i><sub>oc</sub> = {eng(Voc, 'V')}."),
         step("Norton current", f"<i>I</i><sub>N</sub> = <i>V</i><sub>oc</sub>/<i>R</i><sub>N</sub> = {eng(In, 'A')}, which equals the short-circuit current at a–b."),
         step("Equivalent", f"A {eng(In, 'A')} source in parallel with {eng(Rn, 'Ω')}. Converting to Thévenin form gives {eng(Voc, 'V')} in series with the same resistance.")],
        f"<i>I</i><sub>N</sub> = {eng(In, 'A', 4)}, <i>R</i><sub>N</sub> = {eng(Rn, 'Ω', 4)}", level=2, fig=fig, topic="Norton")


def src_transform(r, tag):
    V1, V2 = pick(r, [12, 12.6, 13, 24]), pick(r, [6, 9, 10, 12])
    R1, R2, RL = pick(r, [1, 2, 3, 4]), pick(r, [2, 3, 6]), pick(r, [4, 5, 6, 10, 12])
    Ieq = V1 / R1 + V2 / R2
    Req = par(R1, R2)
    V = Ieq * par(Req, RL)
    fig = ladder(tag, E("V", "V_1", f"{V1} V"), [("S", E("R", "R_1", f"{R1} Ω")), ("P", E("R", "R_L", f"{RL} Ω")), ("S", E("R", "R_2", f"{R2} Ω")), ("P", E("V", "V_2", f"{V2} V"))])
    return Problem(
        "Two practical sources share the load <i>R</i><sub>L</sub>. Using source transformations only, find the voltage across and current through <i>R</i><sub>L</sub>.",
        [step("Transform each voltage source", f"<i>V</i><sub>1</sub> with <i>R</i><sub>1</sub> becomes {num(V1 / R1)} A in parallel with {R1} Ω; <i>V</i><sub>2</sub> with <i>R</i><sub>2</sub> becomes {num(V2 / R2)} A in parallel with {R2} Ω. Both currents point up into the top rail."),
         step("Combine parallel current sources and resistors", f"<i>I</i> = {num(Ieq)} A; <i>R</i><sub>1</sub> ∥ <i>R</i><sub>2</sub> = {num(Req)} Ω."),
         step("Optionally transform back", f"Equivalent single source: {num(Ieq * Req)} V in series with {num(Req)} Ω."),
         step("Load quantities", f"<i>V</i><sub>L</sub> = {num(Ieq * Req)} × {RL}/({num(Req)} + {RL}) = {num(V)} V; <i>I</i><sub>L</sub> = {num(V / RL)} A.")],
        f"<i>V</i><sub>L</sub> = {eng(V, 'V', 4)}, <i>I</i><sub>L</sub> = {eng(V / RL, 'A', 4)}", level=1, fig=fig, topic="source transformation")


def thev_bridge(r, tag):
    Vs = pick(r, [5, 10, 12, 15])
    R1, R2, R3, R4 = [pick(r, [1, 2, 3, 4, 5, 6, 8]) * 100 for _ in range(4)]
    Rg = pick(r, [20, 50, 100])
    Va = Vs * R3 / (R1 + R3)
    Vb = Vs * R4 / (R2 + R4)
    Rth = par(R1, R3) + par(R2, R4)
    Ig = (Va - Vb) / (Rth + Rg)
    G = np.array([[1 / R1 + 1 / R3 + 1 / Rg, -1 / Rg], [-1 / Rg, 1 / R2 + 1 / R4 + 1 / Rg]])
    v = np.linalg.solve(G, [Vs / R1, Vs / R2])
    assert abs((v[0] - v[1]) / Rg - Ig) < 1e-9
    fig = bridge(tag, E("V", "V_s", f"{Vs} V"), E("R", "R_1", eng(R1, "Ω")), E("R", "R_2", eng(R2, "Ω")), E("R", "R_3", eng(R3, "Ω")), E("R", "R_4", eng(R4, "Ω")), mid=E("G", None, None))
    return Problem(
        f"The galvanometer in the bridge shown has a resistance of {Rg} Ω. Use Thévenin's theorem to find the current through it.",
        [step("Remove the galvanometer", "Find the Thévenin equivalent seen by the galvanometer between a and b."),
         step("Open-circuit voltage", f"<i>V</i><sub>a</sub> = {Vs} × {R3}/{R1 + R3} = {num(Va)} V; <i>V</i><sub>b</sub> = {Vs} × {R4}/{R2 + R4} = {num(Vb)} V; <i>V</i><sub>Th</sub> = {num(Va - Vb)} V."),
         step("Thévenin resistance", f"Shorting the source joins the top and bottom nodes, so <i>R</i><sub>Th</sub> = (<i>R</i><sub>1</sub> ∥ <i>R</i><sub>3</sub>) + (<i>R</i><sub>2</sub> ∥ <i>R</i><sub>4</sub>) = {num(par(R1, R3))} + {num(par(R2, R4))} = {num(Rth)} Ω."),
         step("Reconnect the galvanometer", f"<i>I</i><sub>g</sub> = {num(Va - Vb)}/({num(Rth)} + {Rg}) = {eng(Ig, 'A', 4)}, flowing from a to b{'.' if Ig > 0 else ' (negative: actually b to a).'}")],
        f"<i>I</i><sub>g</sub> = {eng(Ig, 'A', 4)}", level=3, fig=fig, topic="Thévenin bridge")


def thev_dep(r, tag):
    V = pick(r, [10, 12, 20, 24])
    R1 = pick(r, [6, 8, 10, 12, 20])
    R2 = pick(r, [4, 5, 10, 20])
    k = pick(r, [1, 2, 3, 4])
    Ix_oc = V / (R1 + R2)
    Voc = V * R2 / (R1 + R2) + k * Ix_oc
    Ix_sc = V / (R1 - k)
    Isc = Ix_sc + k * Ix_sc / R2
    Rth = Voc / Isc
    fig = ladder(tag, E("V", "V_s", f"{V} V"), [("S", E("R", "R_1", f"{R1} Ω", cur="I_x")), ("P", E("R", "R_2", f"{R2} Ω", node="A")), ("S", E("DV", None, f"${k}I_x$"))])
    return Problem(
        f"The network contains a current-controlled voltage source {k}<i>I</i><sub>x</sub> (+ terminal towards a). Find its Thévenin equivalent at a–b using the open-circuit voltage and short-circuit current.",
        [step("Open circuit", f"No current flows through the dependent source, so <i>I</i><sub>x</sub> = {V}/({R1} + {R2}) = {num(Ix_oc)} A and <i>v</i><sub>A</sub> = {num(V * R2 / (R1 + R2))} V."),
         step("Open-circuit voltage", f"<i>V</i><sub>oc</sub> = <i>v</i><sub>A</sub> + {k}<i>I</i><sub>x</sub> = {num(V * R2 / (R1 + R2))} + {num(k * Ix_oc)} = {num(Voc)} V."),
         step("Short circuit a–b", f"Now <i>v</i><sub>A</sub> + {k}<i>I</i><sub>x</sub> = 0, so <i>v</i><sub>A</sub> = −{k}<i>I</i><sub>x</sub>. With <i>I</i><sub>x</sub> = ({V} − <i>v</i><sub>A</sub>)/{R1}: {R1}<i>I</i><sub>x</sub> = {V} + {k}<i>I</i><sub>x</sub>, so <i>I</i><sub>x</sub> = {V}/{R1 - k} = {num(Ix_sc)} A."),
         step("Short-circuit current", f"KCL at A: <i>I</i><sub>sc</sub> = <i>I</i><sub>x</sub> − <i>v</i><sub>A</sub>/{R2} = {num(Ix_sc)} + {num(k * Ix_sc / R2)} = {num(Isc)} A."),
         step("Thévenin resistance", f"<i>R</i><sub>Th</sub> = <i>V</i><sub>oc</sub>/<i>I</i><sub>sc</sub> = {num(Voc)}/{num(Isc)} = {num(Rth)} Ω. With dependent sources present, you cannot find <i>R</i><sub>Th</sub> by simply combining resistors.")],
        f"<i>V</i><sub>Th</sub> = {eng(Voc, 'V', 4)}, <i>R</i><sub>Th</sub> = {eng(Rth, 'Ω', 4)}", level=3, fig=fig, topic="Thévenin, dependent source")


def thev_cs(r, tag):
    Is = pick(r, [0.5, 1, 2, 3])
    V = pick(r, [3, 5, 6, 10])
    R1, R2 = pick(r, RV), pick(r, RV)
    plus_right = r.random() < 0.6
    Vth = Is * R1 + (V if plus_right else -V)
    fig = ladder(tag, E("I", "I_s", f"{Is} A"), [("P", E("R", "R_1", f"{R1} Ω")), ("S", E("R", "R_2", f"{R2} Ω")), ("S", E("V", "V", f"{V} V", rev=not plus_right))])
    return Problem(
        f"Find the Thévenin equivalent at a–b of the network shown. The {V} V source has its + terminal towards {'a' if plus_right else 'the left'}.",
        [step("Open-circuit voltage", f"No current flows in <i>R</i><sub>2</sub> or in the voltage source when a–b is open, so all {Is} A goes through <i>R</i><sub>1</sub>: <i>v</i><sub>R1</sub> = {num(Is * R1)} V."),
         step("Add the series source", f"<i>V</i><sub>Th</sub> = {num(Is * R1)} {'+' if plus_right else '−'} {V} = {num(Vth)} V."),
         step("Thévenin resistance", f"Open the current source, short the voltage source: <i>R</i><sub>Th</sub> = {R1} + {R2} = {R1 + R2} Ω.")],
        f"<i>V</i><sub>Th</sub> = {eng(Vth, 'V', 4)}, <i>R</i><sub>Th</sub> = {R1 + R2} Ω", level=1, fig=fig, topic="Thévenin")


def problems():
    plan = [(sup_vv, 8), (sup_vi, 7), (thevenin, 8), (norton, 7), (maxpower, 8), (src_transform, 7), (thev_bridge, 7), (thev_dep, 7), (thev_cs, 8)]
    return build(6, plan, 606)
