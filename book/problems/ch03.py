from common import *
import numpy as np


def kcl_node(r, tag):
    n_in = pick(r, [2, 3])
    n_out = pick(r, [1, 2])
    ins = [pick(r, [0.5, 1.2, 2, 2.5, 3, 4.5, 6]) for _ in range(n_in)]
    outs = [pick(r, [0.3, 0.8, 1, 1.5, 2]) for _ in range(n_out)]
    unk = sum(ins) - sum(outs)
    direction = "leaving" if unk > 0 else "entering"
    return Problem(
        f"At a junction, currents of {', '.join(eng(i, 'A') for i in ins)} flow in, and {', '.join(eng(o, 'A') for o in outs)} flow out. One further wire, carrying an unknown current <i>I</i><sub>x</sub>, is connected to the junction. Find the magnitude and direction of <i>I</i><sub>x</sub>.",
        [step("State KCL", "The algebraic sum of currents entering a node is zero: what flows in must flow out."),
         step("Assume a direction", "Take <i>I</i><sub>x</sub> as leaving the node. Then Σ in = Σ out gives " + f"{' + '.join(num(i) for i in ins)} = {' + '.join(num(o) for o in outs)} + <i>I</i><sub>x</sub>."),
         step("Solve", f"<i>I</i><sub>x</sub> = {num(sum(ins))} − {num(sum(outs))} = {num(unk)} A."),
         step("Interpret the sign", "A positive result confirms the assumed direction." if unk > 0 else "The negative sign means the current actually enters the node.")],
        f"|<i>I</i><sub>x</sub>| = {eng(abs(unk), 'A')}, {direction} the junction", level=1, topic="KCL")


def kvl_loop(r, tag):
    Vs = pick(r, [9, 12, 15, 24, 30])
    v = [pick(r, [1.5, 2, 2.4, 3, 3.6, 4.2]) for _ in range(pick(r, [2, 3]))]
    if sum(v) >= Vs:
        Vs = sum(v) + pick(r, [1, 2, 3.5])
    vx = Vs - sum(v)
    return Problem(
        f"A {Vs} V source drives a single loop containing {len(v) + 1} resistors. The voltages measured across {len(v)} of them are {', '.join(eng(x, 'V') for x in v)}. What is the voltage across the remaining resistor?",
        [step("State KVL", "Around any closed loop the sum of the voltage rises equals the sum of the voltage drops."),
         step("Write the loop equation", f"{Vs} = {' + '.join(num(x) for x in v)} + <i>V</i><sub>x</sub>."),
         step("Solve", f"<i>V</i><sub>x</sub> = {Vs} − {num(sum(v))} = {num(vx)} V.")],
        f"<i>V</i><sub>x</sub> = {eng(vx, 'V')}", level=1, topic="KVL")


def loop2(r, tag):
    V1 = pick(r, [12, 15, 20, 24, 30])
    V2 = pick(r, [3, 5, 6, 9, 10, 18])
    R1, R2 = pick(r, RSMALL), pick(r, RSMALL)
    aid = r.random() < 0.35
    # V2 drawn on right; rev=False means + at top (opposes clockwise current from V1)
    I = (V1 + V2) / (R1 + R2) if aid else (V1 - V2) / (R1 + R2)
    fig = ladder(tag, E("V", "V_1", f"{V1} V"), [("S", E("R", "R_1", f"{R1} Ω", cur="I")), ("S", E("R", "R_2", f"{R2} Ω")), ("P", E("V", "V_2", f"{V2} V", rev=aid))])
    sgn = "+" if aid else "−"
    P1 = V1 * I
    P2 = (V2 * I) if aid else (-V2 * I)
    steps = [step("Choose the loop current", "Let <i>I</i> flow clockwise, out of the + terminal of <i>V</i><sub>1</sub>."),
             step("KVL clockwise", f"{V1} {sgn} {V2} = <i>I</i>({R1} + {R2}). " + ("Here <i>V</i><sub>2</sub> aids the current, because its + terminal is at the bottom on the right-hand side." if aid else "<i>V</i><sub>2</sub> opposes the clockwise current, since the current enters its + terminal.")),
             step("Solve for the current", f"<i>I</i> = {num(V1 + V2 if aid else V1 - V2)}/{R1 + R2} = {num(I)} A."),
             step("Element powers", f"<i>R</i><sub>1</sub> absorbs {num(I * I * R1)} W and <i>R</i><sub>2</sub> absorbs {num(I * I * R2)} W. <i>V</i><sub>1</sub> delivers {num(P1)} W. <i>V</i><sub>2</sub> " + (f"delivers {num(V2 * I)} W." if aid else (f"absorbs {num(V2 * I)} W (it is being charged)." if I > 0 else f"delivers {num(-V2 * I)} W."))),
             step("Power balance", f"Net power from the sources = {num(V1)} × {num(I)} {'+' if aid else '−'} {num(V2)} × {num(I)} = {num(V1 * I + (V2 * I if aid else -V2 * I))} W. Power absorbed by the resistors = <i>I</i><sup>2</sup>({R1} + {R2}) = {num(I * I * (R1 + R2))} W. The two agree, as conservation of energy requires.")]
    return Problem("For the single-loop circuit shown, find the loop current and the power absorbed or delivered by each element. Verify that power balances.",
                   steps, f"<i>I</i> = {eng(I, 'A')} (clockwise)", level=2, fig=fig, topic="single loop")


def node_pair(r, tag):
    I1 = pick(r, [2, 3, 4, 5, 6, 8])
    I2 = pick(r, [1, 1.5, 2, 3])
    R1, R2 = pick(r, [4, 6, 10, 12, 20]), pick(r, [3, 5, 8, 12, 15, 30])
    opp = r.random() < 0.6
    It = I1 - I2 if opp else I1 + I2
    Rp = par(R1, R2)
    V = It * Rp
    fig = ladder(tag, E("I", "I_1", f"{I1} A"), [("P", E("R", "R_1", f"{R1} Ω")), ("P", E("I", "I_2", f"{I2} A", rev=opp)), ("P", E("R", "R_2", f"{R2} Ω"))])
    return Problem(
        "All the elements shown share the same pair of nodes. Find the voltage <i>V</i> across them (top node positive) and the current in each resistor.",
        [step("Apply KCL at the top node", f"Current sources push {num(I1)} {'−' if opp else '+'} {num(I2)} = {num(It)} A into the node; this must leave through the resistors."),
         step("Combine the resistors", f"<i>R</i><sub>1</sub> ∥ <i>R</i><sub>2</sub> = {num(Rp)} Ω."),
         step("Node voltage", f"<i>V</i> = {num(It)} × {num(Rp)} = {num(V)} V."),
         step("Resistor currents", f"<i>I</i><sub>R1</sub> = {num(V)}/{R1} = {num(V / R1)} A; <i>I</i><sub>R2</sub> = {num(V)}/{R2} = {num(V / R2)} A; together {num(V / R1 + V / R2)} A, as required.")],
        f"<i>V</i> = {eng(V, 'V')}", level=2, fig=fig, topic="node pair")


def tnet(r, tag):
    V1 = pick(r, [10, 12, 20, 24, 30])
    V2 = pick(r, [4, 5, 6, 8, 10, 15])
    R1, R2, R3 = [pick(r, [2, 3, 4, 5, 6, 8, 10, 12]) for _ in range(3)]
    A = np.array([[1, -1, -1], [R1, R2, 0], [0, R2, -R3]], float)
    b = np.array([0, V1, V2], float)
    I1, I2, I3 = np.linalg.solve(A, b)
    fig = ladder(tag, E("V", "V_1", f"{V1} V"), [("S", E("R", "R_1", f"{R1} Ω", cur="I_1")), ("P", E("R", "R_2", f"{R2} Ω", node="A")), ("S", E("R", "R_3", f"{R3} Ω", cur="I_3")), ("P", E("V", "V_2", f"{V2} V"))])
    return Problem(
        "Use the branch-current method (KCL plus KVL) to find the three branch currents in the circuit shown. Take <i>I</i><sub>1</sub> and <i>I</i><sub>3</sub> flowing left to right and <i>I</i><sub>2</sub> flowing down through <i>R</i><sub>2</sub>.",
        [step("KCL at node A", "<i>I</i><sub>1</sub> = <i>I</i><sub>2</sub> + <i>I</i><sub>3</sub>."),
         step("KVL, left loop", f"{V1} = {R1}<i>I</i><sub>1</sub> + {R2}<i>I</i><sub>2</sub>."),
         step("KVL, right loop", f"Going round through <i>R</i><sub>2</sub> up, <i>R</i><sub>3</sub>, and <i>V</i><sub>2</sub>: {R2}<i>I</i><sub>2</sub> = {R3}<i>I</i><sub>3</sub> + {V2}, i.e. {R2}<i>I</i><sub>2</sub> − {R3}<i>I</i><sub>3</sub> = {V2}."),
         step("Solve the three equations", f"Substituting <i>I</i><sub>1</sub> = <i>I</i><sub>2</sub> + <i>I</i><sub>3</sub> into the left-loop equation gives {R1 + R2}<i>I</i><sub>2</sub> + {R1}<i>I</i><sub>3</sub> = {V1}. Solving simultaneously with the right-loop equation: <i>I</i><sub>2</sub> = {num(I2)} A, <i>I</i><sub>3</sub> = {num(I3)} A, <i>I</i><sub>1</sub> = {num(I1)} A."),
         step("Check", f"Voltage at A: {V1} − {R1} × {num(I1)} = {num(V1 - R1 * I1)} V, and {R2} × {num(I2)} = {num(R2 * I2)} V. They agree." + (" The negative <i>I</i><sub>3</sub> means current actually flows from <i>V</i><sub>2</sub> towards A." if I3 < 0 else ""))],
        f"<i>I</i><sub>1</sub> = {eng(I1, 'A')}, <i>I</i><sub>2</sub> = {eng(I2, 'A')}, <i>I</i><sub>3</sub> = {eng(I3, 'A')}", level=2, fig=fig, topic="branch currents")


def dep_loop(r, tag):
    Vs = pick(r, [10, 12, 20, 24])
    R1, R2 = pick(r, [2, 4, 5, 6, 10]), pick(r, [3, 4, 8, 10, 12])
    k = pick(r, [2, 3, 0.5, 4])
    # loop: Vs, R1 (Vx across R1), R2, dependent source k*Vx opposing (+ at top on right)
    I = Vs / (R1 + R2 + k * R1)
    fig = ladder(tag, E("V", "V_s", f"{Vs} V"), [("S", E("R", "R_1", f"{R1} Ω", cur="I")), ("S", E("R", "R_2", f"{R2} Ω")), ("P", E("DV", None, f"${num(k)}V_x$"))])
    Vx = I * R1
    return Problem(
        f"The loop shown contains a voltage-controlled voltage source of value {num(k)}<i>V</i><sub>x</sub>, where <i>V</i><sub>x</sub> is the voltage across <i>R</i><sub>1</sub> (positive at the left). Its + terminal is at the top. Find the loop current and <i>V</i><sub>x</sub>.",
        [step("Express the control variable", f"<i>V</i><sub>x</sub> = {R1}<i>I</i>, with <i>I</i> clockwise."),
         step("KVL clockwise", f"{Vs} = {R1}<i>I</i> + {R2}<i>I</i> + {num(k)}<i>V</i><sub>x</sub> = {R1}<i>I</i> + {R2}<i>I</i> + {num(k * R1)}<i>I</i>."),
         step("Solve", f"<i>I</i> = {Vs}/{num(R1 + R2 + k * R1)} = {num(I)} A."),
         step("Control voltage", f"<i>V</i><sub>x</sub> = {R1} × {num(I)} = {num(Vx)} V; dependent source voltage = {num(k * Vx)} V."),
         step("Lesson", "Treat a dependent source like an independent one when writing KVL, then add one extra equation linking its control variable to the unknowns.")],
        f"<i>I</i> = {eng(I, 'A')}, <i>V</i><sub>x</sub> = {eng(Vx, 'V')}", level=3, fig=fig, topic="dependent sources")


def v_between(r, tag):
    V = pick(r, [12, 18, 24, 36])
    Rs = [pick(r, [1, 2, 3, 4, 5, 6]) * 1000 for _ in range(4)]
    I = V / sum(Rs)
    pts = [V, V - I * Rs[0], V - I * (Rs[0] + Rs[1]), V - I * (Rs[0] + Rs[1] + Rs[2])]
    fig = ladder(tag, E("V", "V_s", f"{V} V"), [("S", E("R", "R_1", eng(Rs[0], "Ω"), node="B")), ("S", E("R", "R_2", eng(Rs[1], "Ω"), node="C")), ("S", E("R", "R_3", eng(Rs[2], "Ω"), node="D")), ("P", E("R", "R_4", eng(Rs[3], "Ω")))])
    return Problem(
        "In the series circuit shown the negative terminal of the source is the reference (0 V), and its positive terminal is point A. Find the potentials at B, C and D, and the voltage <i>V</i><sub>BD</sub>.",
        [step("Loop current", f"<i>I</i> = {V}/{num(sum(Rs))} = {eng(I, 'A')}."),
         step("Walk round the loop from A", f"<i>V</i><sub>B</sub> = {V} − <i>IR</i><sub>1</sub> = {num(pts[1])} V; <i>V</i><sub>C</sub> = {num(pts[2])} V; <i>V</i><sub>D</sub> = {num(pts[3])} V."),
         step("Check", f"<i>V</i><sub>D</sub> should equal the drop across <i>R</i><sub>4</sub>: {num(I * Rs[3])} V. It does."),
         step("Required voltage", f"<i>V</i><sub>BD</sub> = <i>V</i><sub>B</sub> − <i>V</i><sub>D</sub> = {num(pts[1] - pts[3])} V.")],
        f"<i>V</i><sub>B</sub> = {num(pts[1])} V, <i>V</i><sub>C</sub> = {num(pts[2])} V, <i>V</i><sub>D</sub> = {num(pts[3])} V, <i>V</i><sub>BD</sub> = {num(pts[1] - pts[3])} V", level=1, fig=fig, topic="potentials")


def dep_node(r, tag):
    Is = pick(r, [2, 3, 4, 5, 6])
    R1, R2 = pick(r, [2, 4, 5, 10]), pick(r, [4, 6, 8, 12])
    k = pick(r, [2, 3, 0.5])
    # Is up, R1 (current I1 down), CCCS k*I1 down, R2
    # KCL: Is = I1 + k I1 + V/R2 with I1 = V/R1
    V = Is / (1 / R1 + k / R1 + 1 / R2)
    fig = ladder(tag, E("I", "I_s", f"{Is} A"), [("P", E("R", "R_1", f"{R1} Ω", cur="I_1")), ("P", E("DI", None, f"${num(k)}I_1$", rev=True)), ("P", E("R", "R_2", f"{R2} Ω"))])
    return Problem(
        f"In the circuit shown, the current-controlled current source draws {num(k)}<i>I</i><sub>1</sub> downward from the top node, where <i>I</i><sub>1</sub> is the downward current in <i>R</i><sub>1</sub>. Find the node voltage <i>V</i> and <i>I</i><sub>1</sub>.",
        [step("Control variable", f"<i>I</i><sub>1</sub> = <i>V</i>/{R1}."),
         step("KCL at the top node", f"{Is} = <i>V</i>/{R1} + {num(k)}<i>V</i>/{R1} + <i>V</i>/{R2}."),
         step("Solve", f"<i>V</i> = {Is}/({num(1 / R1)} + {num(k / R1)} + {num(1 / R2)}) = {num(V)} V."),
         step("Current", f"<i>I</i><sub>1</sub> = {num(V / R1)} A; the dependent source carries {num(k * V / R1)} A and <i>R</i><sub>2</sub> carries {num(V / R2)} A, totalling {num(V / R1 * (1 + k) + V / R2)} A.")],
        f"<i>V</i> = {eng(V, 'V')}, <i>I</i><sub>1</sub> = {eng(V / R1, 'A')}", level=3, fig=fig, topic="dependent sources")


def kcl_multi(r, tag):
    a = pick(r, [5, 6, 8, 10])
    b = pick(r, [1, 2, 3])
    c = pick(r, [1, 1.5, 2])
    # Nodes P,Q,R. a enters P. P->Q = x, P->R = b. Q->R = c, Q leaves = y. R leaves = z.
    x = a - b
    y = x - c
    z = b + c
    return Problem(
        f"A current of {a} A enters node P of a network. From P, {b} A flows to node R and the remainder to node Q. From Q, {c} A flows on to R, and the rest leaves the network through an external wire at Q. All the current reaching R leaves the network through a wire at R. Find the current in the branch P–Q and in each external wire.",
        [step("KCL at P", f"{a} = {b} + <i>I</i><sub>PQ</sub>, so <i>I</i><sub>PQ</sub> = {num(x)} A."),
         step("KCL at Q", f"{num(x)} = {c} + <i>I</i><sub>Q,out</sub>, so <i>I</i><sub>Q,out</sub> = {num(y)} A."),
         step("KCL at R", f"<i>I</i><sub>R,out</sub> = {b} + {c} = {num(z)} A."),
         step("Whole-network check", f"Total out = {num(y)} + {num(z)} = {num(y + z)} A, matching the {a} A in. KCL applies to any closed surface, not just single nodes.")],
        f"<i>I</i><sub>PQ</sub> = {num(x)} A, <i>I</i><sub>Q,out</sub> = {num(y)} A, <i>I</i><sub>R,out</sub> = {num(z)} A", level=1, topic="KCL")


def find_R(r, tag):
    V1 = pick(r, [12, 24, 30])
    V2 = pick(r, [3, 6, 9])
    R1 = pick(r, [2, 4, 5, 6])
    I = pick(r, [0.5, 0.75, 1, 1.5])
    Rx = (V1 - V2) / I - R1
    if Rx <= 0:
        I = (V1 - V2) / (R1 + 4)
        Rx = 4
    fig = ladder(tag, E("V", "V_1", f"{V1} V"), [("S", E("R", "R_1", f"{R1} Ω", cur="I")), ("S", E("R", "R_x", "?")), ("P", E("V", "V_2", f"{V2} V"))])
    return Problem(
        f"In the loop shown, the measured clockwise current is {eng(I, 'A')}. Find the unknown resistance <i>R</i><sub>x</sub>.",
        [step("KVL clockwise", f"{V1} − {V2} = <i>I</i>({R1} + <i>R</i><sub>x</sub>). <i>V</i><sub>2</sub> opposes the current."),
         step("Rearrange", f"<i>R</i><sub>x</sub> = ({V1} − {V2})/<i>I</i> − {R1} = {num(V1 - V2)}/{num(I)} − {R1}."),
         step("Result", f"<i>R</i><sub>x</sub> = {num(Rx)} Ω.")],
        f"<i>R</i><sub>x</sub> = {eng(Rx, 'Ω')}", level=1, fig=fig, topic="KVL")


def tnet_cs(r, tag):
    V1 = pick(r, [10, 12, 18, 24])
    Is = pick(r, [1, 2, 3])
    R1, R2, R3 = [pick(r, [2, 3, 4, 6, 8]) for _ in range(3)]
    # V1 - R1 - node A - R2 down; R3 from A to node B; current source Is up into node B
    # node A: (V1-VA)/R1 + (VB-VA)/R3 = VA/R2 ; node B: Is = (VB-VA)/R3 -> VB = VA + Is R3
    VA = (V1 / R1 + Is) / (1 / R1 + 1 / R2)
    I1 = (V1 - VA) / R1
    I2 = VA / R2
    fig = ladder(tag, E("V", "V_1", f"{V1} V"), [("S", E("R", "R_1", f"{R1} Ω", cur="I_1")), ("P", E("R", "R_2", f"{R2} Ω", node="A")), ("S", E("R", "R_3", f"{R3} Ω")), ("P", E("I", "I_s", f"{Is} A"))])
    return Problem(
        "Find the currents in <i>R</i><sub>1</sub> and <i>R</i><sub>2</sub>, and the voltage across the current source, for the circuit shown.",
        [step("The current source fixes one branch", f"The right-hand branch carries exactly {Is} A, flowing up through the source and leftward through <i>R</i><sub>3</sub> into node A."),
         step("KCL at A", f"<i>I</i><sub>1</sub> + {Is} = <i>I</i><sub>2</sub>."),
         step("KVL in the left loop", f"{V1} = {R1}<i>I</i><sub>1</sub> + {R2}<i>I</i><sub>2</sub> = {R1}<i>I</i><sub>1</sub> + {R2}(<i>I</i><sub>1</sub> + {Is})."),
         step("Solve", f"<i>I</i><sub>1</sub> = ({V1} − {R2 * Is})/{R1 + R2} = {num(I1)} A; <i>I</i><sub>2</sub> = {num(I2)} A."),
         step("Source voltage", f"<i>V</i><sub>A</sub> = {R2} × {num(I2)} = {num(VA)} V. The source's top terminal is at <i>V</i><sub>A</sub> + {Is} × {R3} = {num(VA + Is * R3)} V. A current source takes whatever voltage the circuit demands.")],
        f"<i>I</i><sub>1</sub> = {eng(I1, 'A')}, <i>I</i><sub>2</sub> = {eng(I2, 'A')}, source voltage {eng(VA + Is * R3, 'V')}", level=2, fig=fig, topic="branch currents")


def problems():
    plan = [(kcl_node, 6), (kvl_loop, 6), (loop2, 7), (node_pair, 6), (tnet, 7), (dep_loop, 5), (v_between, 5),
            (dep_node, 5), (kcl_multi, 5), (find_R, 5), (tnet_cs, 10)]
    return build(3, plan, 303)
