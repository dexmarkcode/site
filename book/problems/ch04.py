from common import *
import numpy as np

RV = [2, 3, 4, 5, 6, 8, 10, 12, 15, 20]


def mat_html(G, unit=""):
    rows = "".join("<tr>" + "".join(f"<td>{num(x, 4)}</td>" for x in row) + "</tr>" for row in G)
    return f'<table class="matrix">{rows}</table>'


def vec_txt(names, vals, unit):
    return ", ".join(f"{n} = {eng(v, unit, 4)}" for n, v in zip(names, vals))


def millman_T(r, tag):
    V1, V2 = pick(r, [10, 12, 20, 24, 30]), pick(r, [5, 6, 8, 9, 15])
    R1, R2, R3 = [pick(r, RV) for _ in range(3)]
    G = 1 / R1 + 1 / R2 + 1 / R3
    VA = (V1 / R1 + V2 / R3) / G
    fig = ladder(tag, E("V", "V_1", f"{V1} V"), [("S", E("R", "R_1", f"{R1} Ω")), ("P", E("R", "R_2", f"{R2} Ω", node="$v_A$")), ("S", E("R", "R_3", f"{R3} Ω")), ("P", E("V", "V_2", f"{V2} V"))])
    return Problem(
        "Take the bottom rail as reference and use nodal analysis to find the voltage <i>v</i><sub>A</sub>, then the current in each resistor.",
        [step("One unknown node", "Only node A has an unknown voltage; the tops of the two sources are fixed at <i>V</i><sub>1</sub> and <i>V</i><sub>2</sub>."),
         step("KCL at A (currents leaving)", f"(<i>v</i><sub>A</sub> − {V1})/{R1} + <i>v</i><sub>A</sub>/{R2} + (<i>v</i><sub>A</sub> − {V2})/{R3} = 0."),
         step("Collect terms", f"<i>v</i><sub>A</sub>(1/{R1} + 1/{R2} + 1/{R3}) = {V1}/{R1} + {V2}/{R3}, i.e. {num(G)}<i>v</i><sub>A</sub> = {num(V1 / R1 + V2 / R3)}."),
         step("Solve", f"<i>v</i><sub>A</sub> = {num(VA)} V."),
         step("Currents", f"<i>R</i><sub>1</sub>: {num((V1 - VA) / R1)} A to the right; <i>R</i><sub>2</sub>: {num(VA / R2)} A downward; <i>R</i><sub>3</sub>: {num((VA - V2) / R3)} A to the right (negative means leftward).")],
        f"<i>v</i><sub>A</sub> = {eng(VA, 'V', 4)}", level=1, fig=fig, topic="nodal")


def two_node_cs(r, tag):
    I1, I2 = pick(r, [1, 2, 3, 4, 5]), pick(r, [0.5, 1, 2, 3])
    R1, R2, R3 = [pick(r, RV) for _ in range(3)]
    out = r.random() < 0.4
    s2 = -I2 if out else I2
    G = np.array([[1 / R1 + 1 / R2, -1 / R2], [-1 / R2, 1 / R2 + 1 / R3]])
    b = np.array([I1, s2])
    v = np.linalg.solve(G, b)
    fig = ladder(tag, E("I", "I_1", f"{I1} A"), [("P", E("R", "R_1", f"{R1} Ω", node="$v_1$")), ("S", E("R", "R_2", f"{R2} Ω")), ("P", E("R", "R_3", f"{R3} Ω", node="$v_2$")), ("P", E("I", "I_2", f"{I2} A", rev=out))])
    return Problem(
        "Find the node voltages <i>v</i><sub>1</sub> and <i>v</i><sub>2</sub> in the circuit shown, and the current in <i>R</i><sub>2</sub>.",
        [step("KCL at node 1 (leaving = entering)", f"<i>v</i><sub>1</sub>/{R1} + (<i>v</i><sub>1</sub> − <i>v</i><sub>2</sub>)/{R2} = {I1}."),
         step("KCL at node 2", f"(<i>v</i><sub>2</sub> − <i>v</i><sub>1</sub>)/{R2} + <i>v</i><sub>2</sub>/{R3} = {num(s2)}" + (" (the source draws current out of the node)." if out else ".")),
         step("Matrix form, written by inspection", "Diagonal terms are the total conductance at each node; off-diagonal terms are minus the conductance linking the nodes:" + mat_html(G) + f"multiplying [<i>v</i><sub>1</sub> <i>v</i><sub>2</sub>]<sup>T</sup> equals [{num(I1)} {num(s2)}]<sup>T</sup>."),
         step("Solve (Cramer's rule or elimination)", f"Δ = {num(np.linalg.det(G))}; <i>v</i><sub>1</sub> = {num(v[0])} V, <i>v</i><sub>2</sub> = {num(v[1])} V."),
         step("Current in R<sub>2</sub>", f"(<i>v</i><sub>1</sub> − <i>v</i><sub>2</sub>)/{R2} = {num((v[0] - v[1]) / R2)} A, from node 1 towards node 2.")],
        f"<i>v</i><sub>1</sub> = {eng(v[0], 'V', 4)}, <i>v</i><sub>2</sub> = {eng(v[1], 'V', 4)}", level=2, fig=fig, topic="nodal")


def two_node_vs(r, tag):
    V1 = pick(r, [10, 12, 18, 24, 36])
    I2 = pick(r, [0.5, 1, 1.5, 2])
    R1, R2, R3, R4 = [pick(r, RV) for _ in range(4)]
    G = np.array([[1 / R1 + 1 / R2 + 1 / R3, -1 / R3], [-1 / R3, 1 / R3 + 1 / R4]])
    b = np.array([V1 / R1, I2])
    v = np.linalg.solve(G, b)
    fig = ladder(tag, E("V", "V_1", f"{V1} V"), [("S", E("R", "R_1", f"{R1} Ω")), ("P", E("R", "R_2", f"{R2} Ω", node="$v_1$")), ("S", E("R", "R_3", f"{R3} Ω")), ("P", E("R", "R_4", f"{R4} Ω", node="$v_2$")), ("P", E("I", "I_2", f"{I2} A"))])
    return Problem(
        "Use nodal analysis to find <i>v</i><sub>1</sub> and <i>v</i><sub>2</sub>, and hence the power delivered by each source.",
        [step("Node 1", f"(<i>v</i><sub>1</sub> − {V1})/{R1} + <i>v</i><sub>1</sub>/{R2} + (<i>v</i><sub>1</sub> − <i>v</i><sub>2</sub>)/{R3} = 0."),
         step("Node 2", f"(<i>v</i><sub>2</sub> − <i>v</i><sub>1</sub>)/{R3} + <i>v</i><sub>2</sub>/{R4} = {I2}."),
         step("Matrix form", "The voltage source in series with <i>R</i><sub>1</sub> contributes a source term " + f"{V1}/{R1} = {num(V1 / R1)} A at node 1:" + mat_html(G) + f"× [<i>v</i><sub>1</sub> <i>v</i><sub>2</sub>]<sup>T</sup> = [{num(V1 / R1)} {num(I2)}]<sup>T</sup>."),
         step("Solve", f"<i>v</i><sub>1</sub> = {num(v[0])} V, <i>v</i><sub>2</sub> = {num(v[1])} V."),
         step("Source powers", f"Current out of <i>V</i><sub>1</sub>: ({V1} − {num(v[0])})/{R1} = {num((V1 - v[0]) / R1)} A, so it delivers {num(V1 * (V1 - v[0]) / R1)} W. The current source delivers {num(I2)} × {num(v[1])} = {num(I2 * v[1])} W.")],
        f"<i>v</i><sub>1</sub> = {eng(v[0], 'V', 4)}, <i>v</i><sub>2</sub> = {eng(v[1], 'V', 4)}", level=2, fig=fig, topic="nodal")


def three_node(r, tag):
    Is = pick(r, [1, 2, 3, 4, 6])
    R = [pick(r, RV) for _ in range(5)]
    G = np.array([[1 / R[0] + 1 / R[1], -1 / R[1], 0],
                  [-1 / R[1], 1 / R[1] + 1 / R[2] + 1 / R[3], -1 / R[3]],
                  [0, -1 / R[3], 1 / R[3] + 1 / R[4]]])
    b = np.array([Is, 0, 0])
    v = np.linalg.solve(G, b)
    fig = ladder(tag, E("I", "I_s", f"{Is} A"), [("P", E("R", "R_1", f"{R[0]} Ω", node="$v_1$")), ("S", E("R", "R_2", f"{R[1]} Ω")), ("P", E("R", "R_3", f"{R[2]} Ω", node="$v_2$")), ("S", E("R", "R_4", f"{R[3]} Ω")), ("P", E("R", "R_5", f"{R[4]} Ω", node="$v_3$"))])
    return Problem(
        "Write the nodal equations for the three-node ladder shown in matrix form by inspection, and solve for all node voltages.",
        [step("Conductances", ", ".join(f"<i>G</i><sub>{k+1}</sub> = 1/{R[k]} = {num(1 / R[k])} S" for k in range(5)) + "."),
         step("Conductance matrix by inspection", mat_html(G) + "The matrix is symmetric, a useful check whenever there are no dependent sources."),
         step("Source vector", f"[{Is} 0 0]<sup>T</sup> A: only node 1 receives current from a source."),
         step("Solve", f"<i>v</i><sub>1</sub> = {num(v[0])} V, <i>v</i><sub>2</sub> = {num(v[1])} V, <i>v</i><sub>3</sub> = {num(v[2])} V."),
         step("Check KCL at node 3", f"Current in through <i>R</i><sub>4</sub>: ({num(v[1])} − {num(v[2])})/{R[3]} = {num((v[1] - v[2]) / R[3])} A; out through <i>R</i><sub>5</sub>: {num(v[2] / R[4])} A. Balanced.")],
        f"<i>v</i><sub>1</sub> = {eng(v[0], 'V', 4)}, <i>v</i><sub>2</sub> = {eng(v[1], 'V', 4)}, <i>v</i><sub>3</sub> = {eng(v[2], 'V', 4)}", level=2, fig=fig, topic="nodal matrix")


def supernode(r, tag):
    Is = pick(r, [2, 3, 4, 5, 6])
    Vs = pick(r, [2, 4, 5, 6, 10])
    R1, R2, R3 = [pick(r, RV) for _ in range(3)]
    # v2 = v1 + Vs; Is = v1/R1 + v2/R2 + v2/R3
    v1 = (Is - Vs / R2 - Vs / R3) / (1 / R1 + 1 / R2 + 1 / R3)
    v2 = v1 + Vs
    Ivs = Is - v1 / R1
    fig = ladder(tag, E("I", "I_s", f"{Is} A"), [("P", E("R", "R_1", f"{R1} Ω", node="$v_1$")), ("S", E("V", "V_s", f"{Vs} V")), ("P", E("R", "R_2", f"{R2} Ω", node="$v_2$")), ("P", E("R", "R_3", f"{R3} Ω"))])
    return Problem(
        "A voltage source sits between nodes 1 and 2 (positive terminal on the right). Use a supernode to find <i>v</i><sub>1</sub>, <i>v</i><sub>2</sub> and the current through the voltage source.",
        [step("Why a supernode?", "The current through an ideal voltage source cannot be written in terms of its terminal voltages, so we draw one surface round both nodes and the source."),
         step("Constraint equation", f"<i>v</i><sub>2</sub> − <i>v</i><sub>1</sub> = {Vs}."),
         step("KCL for the supernode", f"{Is} = <i>v</i><sub>1</sub>/{R1} + <i>v</i><sub>2</sub>/{R2} + <i>v</i><sub>2</sub>/{R3}."),
         step("Substitute and solve", f"{Is} = <i>v</i><sub>1</sub>({num(1 / R1 + 1 / R2 + 1 / R3)}) + {Vs} × {num(1 / R2 + 1 / R3)}, so <i>v</i><sub>1</sub> = {num(v1)} V and <i>v</i><sub>2</sub> = {num(v2)} V."),
         step("Source current", f"KCL at node 1 alone: current through the source to the right = {Is} − {num(v1)}/{R1} = {num(Ivs)} A.")],
        f"<i>v</i><sub>1</sub> = {eng(v1, 'V', 4)}, <i>v</i><sub>2</sub> = {eng(v2, 'V', 4)}, <i>I</i><sub>Vs</sub> = {eng(Ivs, 'A', 4)}", level=3, fig=fig, topic="supernode")


def dep_nodal(r, tag):
    V1 = pick(r, [10, 12, 20, 24])
    R1, R2, R3, R4 = [pick(r, RV) for _ in range(4)]
    k = pick(r, [0.5, 1, 2])
    # node1: (v1-V1)/R1 + v1/R2 + (v1-v2)/R3 = 0 ; node2: (v2-v1)/R3 + v2/R4 = k*v1/R2
    G = np.array([[1 / R1 + 1 / R2 + 1 / R3, -1 / R3], [-1 / R3 - k / R2, 1 / R3 + 1 / R4]])
    b = np.array([V1 / R1, 0])
    v = np.linalg.solve(G, b)
    fig = ladder(tag, E("V", "V_1", f"{V1} V"), [("S", E("R", "R_1", f"{R1} Ω")), ("P", E("R", "R_2", f"{R2} Ω", node="$v_1$", cur="I_x")), ("S", E("R", "R_3", f"{R3} Ω")), ("P", E("DI", None, f"${num(k)}I_x$")), ("P", E("R", "R_4", f"{R4} Ω", node="$v_2$"))])
    return Problem(
        f"The dependent current source injects {num(k)}<i>I</i><sub>x</sub> upward into node 2, where <i>I</i><sub>x</sub> is the downward current in <i>R</i><sub>2</sub>. Find <i>v</i><sub>1</sub>, <i>v</i><sub>2</sub> and <i>I</i><sub>x</sub>.",
        [step("Control variable in node voltages", f"<i>I</i><sub>x</sub> = <i>v</i><sub>1</sub>/{R2}."),
         step("Node 1", f"(<i>v</i><sub>1</sub> − {V1})/{R1} + <i>v</i><sub>1</sub>/{R2} + (<i>v</i><sub>1</sub> − <i>v</i><sub>2</sub>)/{R3} = 0."),
         step("Node 2", f"(<i>v</i><sub>2</sub> − <i>v</i><sub>1</sub>)/{R3} + <i>v</i><sub>2</sub>/{R4} = {num(k)}<i>v</i><sub>1</sub>/{R2}."),
         step("Matrix (no longer symmetric)", mat_html(G) + f"× [<i>v</i><sub>1</sub> <i>v</i><sub>2</sub>]<sup>T</sup> = [{num(V1 / R1)} 0]<sup>T</sup>. The asymmetry is the fingerprint of the dependent source."),
         step("Solve", f"<i>v</i><sub>1</sub> = {num(v[0])} V, <i>v</i><sub>2</sub> = {num(v[1])} V, <i>I</i><sub>x</sub> = {num(v[0] / R2)} A.")],
        f"<i>v</i><sub>1</sub> = {eng(v[0], 'V', 4)}, <i>v</i><sub>2</sub> = {eng(v[1], 'V', 4)}, <i>I</i><sub>x</sub> = {eng(v[0] / R2, 'A', 4)}", level=3, fig=fig, topic="dependent sources")


def millman(r, tag):
    n = pick(r, [3, 3, 4])
    Vs = [pick(r, [11.8, 12, 12.4, 12.6, 12.8, 13.2]) for _ in range(n)]
    Rs = [pick(r, [0.05, 0.08, 0.1, 0.12, 0.15, 0.2]) for _ in range(n)]
    RL = pick(r, [0.5, 1, 2, 4])
    num_ = sum(v / R for v, R in zip(Vs, Rs))
    den = sum(1 / R for R in Rs) + 1 / RL
    V = num_ / den
    cells = "; ".join(f"cell {k+1}: {Vs[k]} V, {Rs[k]} Ω" for k in range(n))
    cur = ", ".join(f"<i>I</i><sub>{k+1}</sub> = ({Vs[k]} − {num(V)})/{Rs[k]} = {num((Vs[k] - V) / Rs[k])} A" for k in range(n))
    return Problem(
        f"{n} batteries, each modelled as an EMF in series with an internal resistance, are connected in parallel across a {RL} Ω load ({cells}). Use Millman's theorem to find the load voltage and the current supplied by each battery.",
        [step("Millman's theorem", "For parallel branches, each an EMF <i>E</i><sub>k</sub> in series with <i>R</i><sub>k</sub>: <i>V</i> = Σ(<i>E</i><sub>k</sub>/<i>R</i><sub>k</sub>)/Σ(1/<i>R</i><sub>k</sub>), with the load counted as a branch of zero EMF. It is simply nodal analysis with one unknown."),
         step("Numerator", f"Σ <i>E</i>/<i>R</i> = {num(num_)} A."),
         step("Denominator", f"Σ 1/<i>R</i> = {num(den)} S (including 1/{RL} for the load)."),
         step("Load voltage", f"<i>V</i> = {num(num_)}/{num(den)} = {num(V)} V; load current {num(V / RL)} A."),
         step("Battery currents", cur + ". A negative value means that battery is being charged by the others, a real hazard with mismatched cells.")],
        f"<i>V</i> = {eng(V, 'V', 4)}", level=2, topic="Millman")


def bridge_nodal(r, tag):
    Vs = pick(r, [10, 12, 15, 20])
    R1, R2, R3, R4 = [pick(r, [1, 2, 3, 4, 5, 6]) * 100 for _ in range(4)]
    Rg = pick(r, [50, 100, 200])
    G = np.array([[1 / R1 + 1 / R3 + 1 / Rg, -1 / Rg], [-1 / Rg, 1 / R2 + 1 / R4 + 1 / Rg]])
    b = np.array([Vs / R1, Vs / R2])
    v = np.linalg.solve(G, b)
    Ig = (v[0] - v[1]) / Rg
    fig = bridge(tag, E("V", "V_s", f"{Vs} V"), E("R", "R_1", eng(R1, "Ω")), E("R", "R_2", eng(R2, "Ω")), E("R", "R_3", eng(R3, "Ω")), E("R", "R_4", eng(R4, "Ω")), mid=E("R", "R_g", eng(Rg, "Ω")))
    return Problem(
        "The bridge shown is unbalanced. Using the bottom node as reference, find the voltages at a and b and the current through <i>R</i><sub>g</sub>.",
        [step("Known node", f"The top node is held at {Vs} V by the source, leaving two unknowns, <i>v</i><sub>a</sub> and <i>v</i><sub>b</sub>."),
         step("Node a", f"(<i>v</i><sub>a</sub> − {Vs})/{R1} + <i>v</i><sub>a</sub>/{R3} + (<i>v</i><sub>a</sub> − <i>v</i><sub>b</sub>)/{Rg} = 0."),
         step("Node b", f"(<i>v</i><sub>b</sub> − {Vs})/{R2} + <i>v</i><sub>b</sub>/{R4} + (<i>v</i><sub>b</sub> − <i>v</i><sub>a</sub>)/{Rg} = 0."),
         step("Matrix form", mat_html(G) + f"× [<i>v</i><sub>a</sub> <i>v</i><sub>b</sub>]<sup>T</sup> = [{num(Vs / R1)} {num(Vs / R2)}]<sup>T</sup>."),
         step("Solve", f"<i>v</i><sub>a</sub> = {num(v[0])} V, <i>v</i><sub>b</sub> = {num(v[1])} V, so <i>I</i><sub>g</sub> = ({num(v[0])} − {num(v[1])})/{Rg} = {eng(Ig, 'A', 4)} from a to b.")],
        f"<i>v</i><sub>a</sub> = {eng(v[0], 'V', 4)}, <i>v</i><sub>b</sub> = {eng(v[1], 'V', 4)}, <i>I</i><sub>g</sub> = {eng(Ig, 'A', 4)}", level=3, fig=fig, topic="bridge")


def problems():
    plan = [(millman_T, 8), (two_node_cs, 9), (two_node_vs, 9), (three_node, 9), (supernode, 9), (dep_nodal, 8), (millman, 7), (bridge_nodal, 8)]
    return build(4, plan, 404)
