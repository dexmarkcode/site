from common import *
import numpy as np
from ch04 import mat_html

RV = [1, 2, 3, 4, 5, 6, 8, 10, 12]


def I(n):
    return f"<i>I</i><sub>{n}</sub>"


def mesh_T(r, tag):
    V1, V2 = pick(r, [10, 12, 15, 20, 24, 30]), pick(r, [2, 4, 5, 6, 8, 10])
    R1, R2, R3 = [pick(r, RV) for _ in range(3)]
    Z = np.array([[R1 + R2, -R2], [-R2, R2 + R3]], float)
    b = np.array([V1, -V2], float)
    i = np.linalg.solve(Z, b)
    fig = ladder(tag, E("V", "V_1", f"{V1} V"), [("S", E("R", "R_1", f"{R1} Ω")), ("P", E("R", "R_2", f"{R2} Ω")), ("S", E("R", "R_3", f"{R3} Ω")), ("P", E("V", "V_2", f"{V2} V"))])
    return Problem(
        f"Using clockwise mesh currents {I(1)} (left) and {I(2)} (right), find both mesh currents, the current in <i>R</i><sub>2</sub>, and the power delivered by each source.",
        [step("Mesh 1", f"{V1} = {R1}{I(1)} + {R2}({I(1)} − {I(2)})."),
         step("Mesh 2", f"0 = {R2}({I(2)} − {I(1)}) + {R3}{I(2)} + {V2}. The clockwise current enters the + terminal of <i>V</i><sub>2</sub>, so it is a drop."),
         step("Resistance matrix", mat_html(Z) + f"× [{I(1)} {I(2)}]<sup>T</sup> = [{V1} {MINUS}{V2}]<sup>T</sup>."),
         step("Solve", f"Δ = {num(np.linalg.det(Z))}; {I(1)} = {num(i[0])} A, {I(2)} = {num(i[1])} A."),
         step("Branch current and powers", f"<i>R</i><sub>2</sub> carries {I(1)} − {I(2)} = {num(i[0] - i[1])} A downward. <i>V</i><sub>1</sub> delivers {num(V1 * i[0])} W; <i>V</i><sub>2</sub> {'absorbs' if i[1] > 0 else 'delivers'} {num(abs(V2 * i[1]))} W.")],
        f"{I(1)} = {eng(i[0], 'A', 4)}, {I(2)} = {eng(i[1], 'A', 4)}", level=1 if r.random() < 0.4 else 2, fig=fig, topic="mesh")


def mesh3(r, tag):
    V1 = pick(r, [12, 20, 24, 30, 48])
    R = [pick(r, RV) for _ in range(6)]
    end_src = r.random() < 0.5
    V2 = pick(r, [5, 6, 10]) if end_src else 0
    Z = np.array([[R[0] + R[1], -R[1], 0], [-R[1], R[1] + R[2] + R[3], -R[3]], [0, -R[3], R[3] + R[4] + (0 if end_src else R[5])]], float)
    b = np.array([V1, 0, -V2], float)
    i = np.linalg.solve(Z, b)
    items = [("S", E("R", "R_1", f"{R[0]} Ω")), ("P", E("R", "R_2", f"{R[1]} Ω")), ("S", E("R", "R_3", f"{R[2]} Ω")), ("P", E("R", "R_4", f"{R[3]} Ω")), ("S", E("R", "R_5", f"{R[4]} Ω"))]
    items.append(("P", E("V", "V_2", f"{V2} V")) if end_src else ("P", E("R", "R_6", f"{R[5]} Ω")))
    fig = ladder(tag, E("V", "V_1", f"{V1} V"), items)
    return Problem(
        f"Write the 3 × 3 mesh equations for the ladder shown by inspection (clockwise currents {I(1)}, {I(2)}, {I(3)} from left to right) and solve them.",
        [step("Diagonal entries", "Each is the total resistance round that mesh."),
         step("Off-diagonal entries", "Minus the resistance shared by the two meshes; zero for meshes that share nothing."),
         step("Matrix equation", mat_html(Z) + f"× [{I(1)} {I(2)} {I(3)}]<sup>T</sup> = [{V1} 0 {num(-V2)}]<sup>T</sup>."),
         step("Solve", f"{I(1)} = {num(i[0])} A, {I(2)} = {num(i[1])} A, {I(3)} = {num(i[2])} A."),
         step("Sense-check", f"Each mesh current should be smaller than the one before it in a resistive ladder driven only from the left{'.' if not end_src else ', unless the right-hand source pushes back, as it may here.'} The current in <i>R</i><sub>4</sub> is {I(2)} − {I(3)} = {num(i[1] - i[2])} A.")],
        f"{I(1)} = {eng(i[0], 'A', 4)}, {I(2)} = {eng(i[1], 'A', 4)}, {I(3)} = {eng(i[2], 'A', 4)}", level=2, fig=fig, topic="mesh matrix")


def mesh_cs_outer(r, tag):
    V1 = pick(r, [10, 12, 20, 24])
    Is = pick(r, [0.5, 1, 2, 3])
    R1, R2, R3 = [pick(r, RV) for _ in range(3)]
    i2 = -Is
    i1 = (V1 + R2 * i2) / (R1 + R2)
    fig = ladder(tag, E("V", "V_1", f"{V1} V"), [("S", E("R", "R_1", f"{R1} Ω")), ("P", E("R", "R_2", f"{R2} Ω")), ("S", E("R", "R_3", f"{R3} Ω")), ("P", E("I", "I_s", f"{Is} A"))])
    vs = R2 * (i1 - i2) - R3 * i2
    return Problem(
        "The right-hand branch contains a current source that pushes current upward. With clockwise mesh currents, find both mesh currents and the voltage across the current source.",
        [step("The current source fixes mesh 2", f"Only mesh 2 passes through the source, and clockwise means downward in that branch, so {I(2)} = {MINUS}{Is} A."),
         step("Mesh 1", f"{V1} = {R1}{I(1)} + {R2}({I(1)} − {I(2)}) = {R1 + R2}{I(1)} + {R2 * Is}."),
         step("Solve", f"{I(1)} = ({V1} − {R2 * Is})/{R1 + R2} = {num(i1)} A."),
         step("Source voltage (top relative to bottom)", f"Top of source = voltage across <i>R</i><sub>2</sub> plus drop across <i>R</i><sub>3</sub> travelling towards the source: {R2}({num(i1)} − ({num(i2)})) + {R3} × {Is} = {num(vs)} V. You could not write this as a mesh equation directly; it falls out afterwards.")],
        f"{I(1)} = {eng(i1, 'A', 4)}, {I(2)} = {eng(i2, 'A', 4)}, <i>V</i><sub>Is</sub> = {eng(vs, 'V', 4)}", level=2, fig=fig, topic="mesh with current source")


def supermesh(r, tag):
    V1, V2 = pick(r, [12, 20, 24, 30]), pick(r, [3, 4, 6, 9])
    Is = pick(r, [1, 2, 3])
    R1, R3 = pick(r, RV), pick(r, RV)
    i2 = (V1 - V2 + R1 * Is) / (R1 + R3)
    i1 = i2 - Is
    fig = ladder(tag, E("V", "V_1", f"{V1} V"), [("S", E("R", "R_1", f"{R1} Ω")), ("P", E("I", "I_s", f"{Is} A")), ("S", E("R", "R_3", f"{R3} Ω")), ("P", E("V", "V_2", f"{V2} V"))])
    return Problem(
        "A current source is shared by both meshes. Use a supermesh to find the clockwise mesh currents and the voltage across the current source.",
        [step("Constraint", f"The source pushes {Is} A upward. Mesh 1 flows down that branch and mesh 2 flows up it, so {I(2)} − {I(1)} = {Is}."),
         step("Supermesh", f"Go round the outside, avoiding the current source: {V1} − {R1}{I(1)} − {R3}{I(2)} − {V2} = 0."),
         step("Substitute", f"{V1} − {V2} = {R1}({I(2)} − {Is}) + {R3}{I(2)}, so {I(2)} = ({num(V1 - V2)} + {R1 * Is})/{R1 + R3} = {num(i2)} A."),
         step("Other mesh", f"{I(1)} = {num(i2)} − {Is} = {num(i1)} A."),
         step("Source voltage", f"Top relative to bottom: {V1} − {R1} × {num(i1)} = {num(V1 - R1 * i1)} V.")],
        f"{I(1)} = {eng(i1, 'A', 4)}, {I(2)} = {eng(i2, 'A', 4)}", level=3, fig=fig, topic="supermesh")


def mesh_dep(r, tag):
    V1 = pick(r, [10, 12, 18, 24])
    R1, R3, R4 = [pick(r, RV) for _ in range(3)]
    k = pick(r, [2, 3, 4, 5])
    i1 = V1 / (R1 + k)
    i2 = k * i1 / (R3 + R4)
    fig = ladder(tag, E("V", "V_1", f"{V1} V"), [("S", E("R", "R_1", f"{R1} Ω", cur="I_x")), ("P", E("DV", None, f"${k}I_x$")), ("S", E("R", "R_3", f"{R3} Ω")), ("P", E("R", "R_4", f"{R4} Ω"))])
    return Problem(
        f"The middle branch is a current-controlled voltage source of value {k}<i>I</i><sub>x</sub> volts (with <i>I</i><sub>x</sub> in amperes), + at the top. Find <i>I</i><sub>x</sub> and the current in <i>R</i><sub>4</sub>.",
        [step("Relate the control current to the meshes", f"<i>I</i><sub>x</sub> is the current in <i>R</i><sub>1</sub>, which is mesh current {I(1)}."),
         step("Mesh 1", f"{V1} = {R1}{I(1)} + {k}{I(1)}, since clockwise current enters the + terminal of the dependent source."),
         step("Solve mesh 1", f"{I(1)} = <i>I</i><sub>x</sub> = {V1}/{R1 + k} = {num(i1)} A. The dependent source behaves like an extra {k} Ω here, a handy insight."),
         step("Mesh 2", f"Going clockwise, mesh 2 rises through the source: {k}<i>I</i><sub>x</sub> = ({R3} + {R4}){I(2)}, so {I(2)} = {num(k * i1)}/{R3 + R4} = {num(i2)} A."),
         step("Answer", f"<i>R</i><sub>4</sub> carries {num(i2)} A downward.")],
        f"<i>I</i><sub>x</sub> = {eng(i1, 'A', 4)}, <i>I</i><sub>R4</sub> = {eng(i2, 'A', 4)}", level=2, fig=fig, topic="dependent sources")


def bridge_mesh(r, tag):
    Vs = pick(r, [6, 10, 12, 24])
    R1, R2, R3, R4 = [pick(r, [1, 2, 3, 4, 5, 6, 8]) * 10 for _ in range(4)]
    Rg = pick(r, [5, 10, 20, 40])
    Z = np.array([[R1 + R3, -R1, -R3], [-R1, R1 + R2 + Rg, -Rg], [-R3, -Rg, R3 + Rg + R4]], float)
    b = np.array([Vs, 0, 0], float)
    i = np.linalg.solve(Z, b)
    Ig = i[2] - i[1]
    # independent nodal check
    G = np.array([[1 / R1 + 1 / R3 + 1 / Rg, -1 / Rg], [-1 / Rg, 1 / R2 + 1 / R4 + 1 / Rg]])
    v = np.linalg.solve(G, [Vs / R1, Vs / R2])
    assert abs((v[0] - v[1]) / Rg - Ig) < 1e-9
    fig = bridge(tag, E("V", "V_s", f"{Vs} V"), E("R", "R_1", f"{R1} Ω"), E("R", "R_2", f"{R2} Ω"), E("R", "R_3", f"{R3} Ω"), E("R", "R_4", f"{R4} Ω"), mid=E("R", "R_g", f"{Rg} Ω"))
    return Problem(
        f"Use mesh analysis to find the current through <i>R</i><sub>g</sub>. Define {I(1)} round the loop source → <i>R</i><sub>1</sub> → <i>R</i><sub>3</sub>; {I(2)} round the upper triangle <i>R</i><sub>1</sub>, <i>R</i><sub>2</sub>, <i>R</i><sub>g</sub> (passing through <i>R</i><sub>2</sub> from top to b and through <i>R</i><sub>g</sub> from b to a); and {I(3)} round the lower triangle (through <i>R</i><sub>g</sub> from a to b, then down <i>R</i><sub>4</sub>).",
        [step("Mesh 1", f"{Vs} = {R1}({I(1)} − {I(2)}) + {R3}({I(1)} − {I(3)})."),
         step("Mesh 2", f"0 = {R1}({I(2)} − {I(1)}) + {R2}{I(2)} + {Rg}({I(2)} − {I(3)})."),
         step("Mesh 3", f"0 = {R3}({I(3)} − {I(1)}) + {Rg}({I(3)} − {I(2)}) + {R4}{I(3)}."),
         step("Matrix", mat_html(Z) + f"× [{I(1)} {I(2)} {I(3)}]<sup>T</sup> = [{Vs} 0 0]<sup>T</sup>."),
         step("Solve", f"{I(1)} = {num(i[0])} A, {I(2)} = {num(i[1])} A, {I(3)} = {num(i[2])} A."),
         step("Galvanometer branch", f"Current a → b in <i>R</i><sub>g</sub> = {I(3)} − {I(2)} = {eng(Ig, 'A', 4)}. (A nodal solution gives the same figure, which is a worthwhile cross-check.)")],
        f"<i>I</i><sub>g</sub> = {eng(Ig, 'A', 4)} (a → b)", level=3, fig=fig, topic="bridge")


def mesh_midV(r, tag):
    V1, V2, V3 = pick(r, [12, 15, 24]), pick(r, [3, 5, 6]), pick(r, [6, 8, 9, 10])
    R1, R3 = pick(r, RV), pick(r, RV)
    i1 = (V1 - V3) / R1
    i2 = (V3 - V2) / R3
    fig = ladder(tag, E("V", "V_1", f"{V1} V"), [("S", E("R", "R_1", f"{R1} Ω")), ("P", E("V", "V_3", f"{V3} V")), ("S", E("R", "R_3", f"{R3} Ω")), ("P", E("V", "V_2", f"{V2} V"))])
    return Problem(
        "Find the clockwise mesh currents and the current through the centre source <i>V</i><sub>3</sub>.",
        [step("Mesh 1", f"{V1} − {R1}{I(1)} − {V3} = 0, so {I(1)} = {num(V1 - V3)}/{R1} = {num(i1)} A."),
         step("Mesh 2", f"Mesh 2 rises through <i>V</i><sub>3</sub> and falls through <i>V</i><sub>2</sub>: {V3} − {R3}{I(2)} − {V2} = 0, so {I(2)} = {num(i2)} A."),
         step("Centre branch", f"The source carries {I(1)} − {I(2)} = {num(i1 - i2)} A downward. An ideal voltage source between two meshes decouples them completely, a neat simplification.")],
        f"{I(1)} = {eng(i1, 'A', 4)}, {I(2)} = {eng(i2, 'A', 4)}", level=1, fig=fig, topic="mesh")


def problems():
    plan = [(mesh_T, 13), (mesh3, 17), (mesh_cs_outer, 8), (supermesh, 8), (mesh_dep, 7), (bridge_mesh, 8), (mesh_midV, 6)]
    return build(5, plan, 505)
