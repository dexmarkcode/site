from common import *


def kres(r, n, scale=1000):
    return [pick(r, RSMALL) * scale for _ in range(n)]


def _sc(r):
    return pick(r, [1, 10, 100, 1000, 1000])


def series(r, tag):
    n = pick(r, [2, 3, 3, 4])
    sc = _sc(r)
    Rs = kres(r, n, sc)
    V = pick(r, [6, 9, 12, 18, 24, 30, 48])
    Req = sum(Rs)
    I = V / Req
    items = [("S", E("R", f"R_{k+1}", eng(R, "Ω"))) for k, R in enumerate(Rs[:-1])] + [("P", E("R", f"R_{n}", eng(Rs[-1], "Ω")))]
    fig = ladder(tag, E("V", "V_s", f"{V} V"), items)
    drops = ", ".join(f"<i>V</i><sub>{k+1}</sub> = {eng(I * R, 'V')}" for k, R in enumerate(Rs))
    return Problem(
        f"For the series circuit shown, find the equivalent resistance seen by the source, the current, and the voltage across each resistor.",
        [step("Add the series resistances", f"<i>R</i><sub>eq</sub> = {' + '.join(eng(R, 'Ω') for R in Rs)} = {eng(Req, 'Ω')}."),
         step("Current (the same everywhere in a series loop)", f"<i>I</i> = <i>V</i><sub>s</sub>/<i>R</i><sub>eq</sub> = {V}/{num(Req)} = {eng(I, 'A')}."),
         step("Individual drops, V = IR", drops + "."),
         step("KVL check", f"The drops sum to {num(sum(I * R for R in Rs))} V, which equals the {V} V supply.")],
        f"<i>R</i><sub>eq</sub> = {eng(Req, 'Ω')}, <i>I</i> = {eng(I, 'A')}; {drops}", level=1, fig=fig, topic="series")


def parallel(r, tag):
    n = pick(r, [2, 3, 3, 4])
    sc = _sc(r)
    Rs = kres(r, n, sc)
    V = pick(r, [5, 10, 12, 24, 60, 120])
    Req = par(*Rs)
    items = [("P", E("R", f"R_{k+1}", eng(R, "Ω"))) for k, R in enumerate(Rs)]
    fig = ladder(tag, E("V", "V_s", f"{V} V"), items)
    br = ", ".join(f"<i>I</i><sub>{k+1}</sub> = {eng(V / R, 'A')}" for k, R in enumerate(Rs))
    gs = " + ".join(f"1/{num(R)}" for R in Rs)
    return Problem(
        "Find the equivalent resistance of the parallel network shown, the current in each branch, and the total supply current.",
        [step("Use conductances", f"1/<i>R</i><sub>eq</sub> = {gs} = {num(1 / Req)} S."),
         step("Equivalent resistance", f"<i>R</i><sub>eq</sub> = {eng(Req, 'Ω')}. Note that it is smaller than the smallest branch, as it must be."),
         step("Branch currents (each branch has the full supply voltage)", br + "."),
         step("Total current by KCL", f"<i>I</i> = {num(sum(V / R for R in Rs))} A, which agrees with <i>V</i>/<i>R</i><sub>eq</sub> = {num(V / Req)} A.")],
        f"<i>R</i><sub>eq</sub> = {eng(Req, 'Ω')}; <i>I</i> = {eng(V / Req, 'A')}", level=1, fig=fig, topic="parallel")


def sp_a(r, tag):
    sc = _sc(r)
    R1, R2, R3 = kres(r, 3, sc)
    V = pick(r, [12, 15, 20, 24, 36])
    Rp = par(R2, R3)
    Req = R1 + Rp
    I = V / Req
    Vp = I * Rp
    fig = ladder(tag, E("V", "V_s", f"{V} V"), [("S", E("R", "R_1", eng(R1, "Ω"))), ("P", E("R", "R_2", eng(R2, "Ω"))), ("P", E("R", "R_3", eng(R3, "Ω")))])
    return Problem(
        "In the circuit shown, find the supply current, the voltage across <i>R</i><sub>2</sub> and the current in <i>R</i><sub>3</sub>.",
        [step("Combine the parallel pair", f"<i>R</i><sub>2</sub> ∥ <i>R</i><sub>3</sub> = ({num(R2)} × {num(R3)})/({num(R2)} + {num(R3)}) = {eng(Rp, 'Ω')}."),
         step("Add R<sub>1</sub> in series", f"<i>R</i><sub>eq</sub> = {eng(R1, 'Ω')} + {eng(Rp, 'Ω')} = {eng(Req, 'Ω')}."),
         step("Supply current", f"<i>I</i> = {V}/{num(Req)} = {eng(I, 'A')}."),
         step("Voltage across the parallel pair", f"<i>V</i><sub>2</sub> = <i>I</i> × {eng(Rp, 'Ω')} = {eng(Vp, 'V')}."),
         step("Current in R<sub>3</sub>", f"<i>I</i><sub>3</sub> = {num(Vp)}/{num(R3)} = {eng(Vp / R3, 'A')}.")],
        f"<i>I</i> = {eng(I, 'A')}, <i>V</i><sub>2</sub> = {eng(Vp, 'V')}, <i>I</i><sub>3</sub> = {eng(Vp / R3, 'A')}", level=1, fig=fig, topic="series-parallel")


def sp_b(r, tag):
    sc = _sc(r)
    R1, R2, R3 = kres(r, 3, sc)
    V = pick(r, [10, 12, 24, 48])
    Rser = R1 + R2
    Req = par(R3, Rser)
    fig = ladder(tag, E("V", "V_s", f"{V} V"), [("P", E("R", "R_3", eng(R3, "Ω"))), ("S", E("R", "R_1", eng(R1, "Ω"))), ("P", E("R", "R_2", eng(R2, "Ω")))])
    I2 = V / Rser
    return Problem(
        "For the network shown, find the equivalent resistance seen by the source, the total current and the voltage across <i>R</i><sub>2</sub>.",
        [step("Recognise the structure", f"<i>R</i><sub>1</sub> and <i>R</i><sub>2</sub> carry the same current, so they are in series; that series pair sits directly across the source, as does <i>R</i><sub>3</sub>."),
         step("Series pair", f"<i>R</i><sub>1</sub> + <i>R</i><sub>2</sub> = {eng(Rser, 'Ω')}."),
         step("Parallel with R<sub>3</sub>", f"<i>R</i><sub>eq</sub> = {eng(R3, 'Ω')} ∥ {eng(Rser, 'Ω')} = {eng(Req, 'Ω')}."),
         step("Total current", f"<i>I</i> = {V}/{num(Req)} = {eng(V / Req, 'A')}."),
         step("Voltage across R<sub>2</sub> by the divider rule", f"<i>V</i><sub>2</sub> = {V} × {num(R2)}/{num(Rser)} = {eng(V * R2 / Rser, 'V')} (branch current {eng(I2, 'A')}).")],
        f"<i>R</i><sub>eq</sub> = {eng(Req, 'Ω')}, <i>I</i> = {eng(V / Req, 'A')}, <i>V</i><sub>2</sub> = {eng(V * R2 / Rser, 'V')}", level=2, fig=fig, topic="series-parallel")


def ladder4(r, tag):
    sc = _sc(r)
    R1, R2, R3, R4 = kres(r, 4, sc)
    V = pick(r, [10, 12, 20, 24, 50, 100])
    Rb = R3 + R4
    Rc = par(R2, Rb)
    Req = R1 + Rc
    I = V / Req
    Va = I * Rc
    V4 = Va * R4 / Rb
    fig = ladder(tag, E("V", "V_s", f"{V} V"), [("S", E("R", "R_1", eng(R1, "Ω"))), ("P", E("R", "R_2", eng(R2, "Ω"), node="A")), ("S", E("R", "R_3", eng(R3, "Ω"))), ("P", E("R", "R_4", eng(R4, "Ω")))])
    return Problem(
        "Reduce the ladder network shown to find the current supplied by the source and the voltage across <i>R</i><sub>4</sub>.",
        [step("Start at the end furthest from the source", f"<i>R</i><sub>3</sub> + <i>R</i><sub>4</sub> = {eng(Rb, 'Ω')}."),
         step("Combine with R<sub>2</sub>", f"{eng(R2, 'Ω')} ∥ {eng(Rb, 'Ω')} = {eng(Rc, 'Ω')}."),
         step("Add R<sub>1</sub>", f"<i>R</i><sub>eq</sub> = {eng(R1, 'Ω')} + {eng(Rc, 'Ω')} = {eng(Req, 'Ω')}; <i>I</i> = {V}/{num(Req)} = {eng(I, 'A')}."),
         step("Voltage at node A", f"<i>V</i><sub>A</sub> = <i>I</i> × {eng(Rc, 'Ω')} = {eng(Va, 'V')}."),
         step("Divide down to R<sub>4</sub>", f"<i>V</i><sub>4</sub> = {num(Va)} × {num(R4)}/{num(Rb)} = {eng(V4, 'V')}.")],
        f"<i>I</i> = {eng(I, 'A')}, <i>V</i><sub>4</sub> = {eng(V4, 'V')}", level=2, fig=fig, topic="ladder")


def vdiv(r, tag):
    sc = _sc(r)
    R1, R2 = kres(r, 2, sc)
    V = pick(r, [5, 9, 12, 15, 24])
    Vo = V * R2 / (R1 + R2)
    fig = ladder(tag, E("V", "V_in", f"{V} V"), [("S", E("R", "R_1", eng(R1, "Ω"))), ("P", E("R", "R_2", eng(R2, "Ω"), node="$V_{\\mathrm{out}}$"))])
    return Problem(
        "Use the voltage-divider rule to find the output voltage of the unloaded divider shown.",
        [step("State the rule", "<i>V</i><sub>out</sub> = <i>V</i><sub>in</sub> × <i>R</i><sub>2</sub>/(<i>R</i><sub>1</sub> + <i>R</i><sub>2</sub>)."),
         step("Substitute", f"<i>V</i><sub>out</sub> = {V} × {num(R2)}/({num(R1)} + {num(R2)}) = {V} × {num(R2 / (R1 + R2))}."),
         step("Result", f"<i>V</i><sub>out</sub> = {eng(Vo, 'V')}. The output is the fraction of the total resistance occupied by <i>R</i><sub>2</sub>.")],
        f"<i>V</i><sub>out</sub> = {eng(Vo, 'V')}", level=1, fig=fig, topic="divider")


def cdiv(r, tag):
    sc = _sc(r)
    R1, R2 = kres(r, 2, sc)
    Is = pick(r, [2, 5, 10, 20, 50]) * (1e-3 if sc >= 100 else 0.1)
    I1 = Is * R2 / (R1 + R2)
    fig = ladder(tag, E("I", "I_s", eng(Is, "A")), [("P", E("R", "R_1", eng(R1, "Ω"))), ("P", E("R", "R_2", eng(R2, "Ω")))])
    return Problem(
        "A current source feeds two resistors in parallel, as shown. Find the current in each resistor.",
        [step("Current-divider rule", "For two branches, <i>I</i><sub>1</sub> = <i>I</i><sub>s</sub> × <i>R</i><sub>2</sub>/(<i>R</i><sub>1</sub> + <i>R</i><sub>2</sub>). Note the <em>opposite</em> resistor appears on top."),
         step("Current in R<sub>1</sub>", f"<i>I</i><sub>1</sub> = {eng(Is, 'A')} × {num(R2)}/{num(R1 + R2)} = {eng(I1, 'A')}."),
         step("Current in R<sub>2</sub>", f"<i>I</i><sub>2</sub> = {eng(Is, 'A')} − {eng(I1, 'A')} = {eng(Is - I1, 'A')}."),
         step("Check with the common voltage", f"<i>I</i><sub>1</sub><i>R</i><sub>1</sub> = {num(I1 * R1)} V and <i>I</i><sub>2</sub><i>R</i><sub>2</sub> = {num((Is - I1) * R2)} V; they agree.")],
        f"<i>I</i><sub>1</sub> = {eng(I1, 'A')}, <i>I</i><sub>2</sub> = {eng(Is - I1, 'A')}", level=1, fig=fig, topic="divider")


def loaded(r, tag):
    R1 = pick(r, [10, 15, 22, 47]) * 1000
    R2 = R1 * pick(r, [1, 2, 0.5])
    RL = pick(r, [5, 10, 22, 47, 100, 470]) * 1000
    V = pick(r, [10, 12, 15])
    Vu = V * R2 / (R1 + R2)
    Rp = par(R2, RL)
    Vl = V * Rp / (R1 + Rp)
    fig = ladder(tag, E("V", "V_s", f"{V} V"), [("S", E("R", "R_1", eng(R1, "Ω"))), ("P", E("R", "R_2", eng(R2, "Ω"), node="$V_o$")), ("P", E("R", "R_L", eng(RL, "Ω")))])
    return Problem(
        "A voltage divider is loaded by <i>R</i><sub>L</sub> as shown. Find the output voltage with and without the load, and the percentage drop caused by loading.",
        [step("Unloaded output", f"<i>V</i><sub>o</sub> = {V} × {num(R2)}/{num(R1 + R2)} = {eng(Vu, 'V')}."),
         step("Lower leg when loaded", f"<i>R</i><sub>2</sub> ∥ <i>R</i><sub>L</sub> = {eng(Rp, 'Ω')}."),
         step("Loaded output", f"<i>V</i><sub>o</sub> = {V} × {num(Rp)}/({num(R1)} + {num(Rp)}) = {eng(Vl, 'V')}."),
         step("Loading error", f"Drop = ({num(Vu)} − {num(Vl)})/{num(Vu)} × 100 = {num((Vu - Vl) / Vu * 100, 3)} %. A divider only holds its ratio when the load is much larger than <i>R</i><sub>2</sub>.")],
        f"unloaded {eng(Vu, 'V')}, loaded {eng(Vl, 'V')} ({num((Vu - Vl) / Vu * 100, 3)} % drop)", level=2, fig=fig, topic="loading")


def delta_y(r, tag):
    Ra, Rb, Rc = [pick(r, [6, 9, 10, 12, 15, 18, 20, 30, 60]) for _ in range(3)]
    S = Ra + Rb + Rc
    fig = star_delta(tag, "R", [f"$R_{{ab}}$\n{Ra} Ω", f"$R_{{bc}}$\n{Rb} Ω", f"$R_{{ca}}$\n{Rc} Ω"], star=False)
    R1 = Ra * Rc / S
    R2 = Ra * Rb / S
    R3 = Rb * Rc / S
    return Problem(
        "Convert the delta (Δ) network shown into an equivalent star (Y), giving the resistance connected to each terminal a, b and c.",
        [step("Sum of the delta resistances", f"Σ = {Ra} + {Rb} + {Rc} = {S} Ω."),
         step("Rule", "Each star arm equals the product of the two delta resistors that meet at that terminal, divided by the sum."),
         step("Arm at a", f"<i>R</i><sub>a</sub> = <i>R</i><sub>ab</sub><i>R</i><sub>ca</sub>/Σ = {Ra} × {Rc}/{S} = {num(R1)} Ω."),
         step("Arm at b", f"<i>R</i><sub>b</sub> = <i>R</i><sub>ab</sub><i>R</i><sub>bc</sub>/Σ = {Ra} × {Rb}/{S} = {num(R2)} Ω."),
         step("Arm at c", f"<i>R</i><sub>c</sub> = <i>R</i><sub>bc</sub><i>R</i><sub>ca</sub>/Σ = {Rb} × {Rc}/{S} = {num(R3)} Ω."),
         step("Check", f"Between a and b with c open, the delta gives {Ra} ∥ ({Rb} + {Rc}) = {num(par(Ra, Rb + Rc))} Ω; the star gives {num(R1)} + {num(R2)} = {num(R1 + R2)} Ω.")],
        f"<i>R</i><sub>a</sub> = {num(R1)} Ω, <i>R</i><sub>b</sub> = {num(R2)} Ω, <i>R</i><sub>c</sub> = {num(R3)} Ω", level=2, fig=fig, topic="delta-star")


def y_delta(r, tag):
    R1, R2, R3 = [pick(r, [2, 3, 4, 5, 6, 8, 10, 12]) for _ in range(3)]
    fig = star_delta(tag, "R", [f"$R_a$\n{R1} Ω", f"$R_b$\n{R2} Ω", f"$R_c$\n{R3} Ω"], star=True)
    P = R1 * R2 + R2 * R3 + R3 * R1
    Rab, Rbc, Rca = P / R3, P / R1, P / R2
    return Problem(
        "Convert the star (Y) network shown into an equivalent delta (Δ).",
        [step("Sum of pairwise products", f"<i>P</i> = {R1}×{R2} + {R2}×{R3} + {R3}×{R1} = {num(P)} Ω<sup>2</sup>."),
         step("Rule", "Each delta resistor equals <i>P</i> divided by the star arm on the <em>opposite</em> terminal."),
         step("Delta resistors", f"<i>R</i><sub>ab</sub> = <i>P</i>/<i>R</i><sub>c</sub> = {num(Rab)} Ω; <i>R</i><sub>bc</sub> = <i>P</i>/<i>R</i><sub>a</sub> = {num(Rbc)} Ω; <i>R</i><sub>ca</sub> = <i>P</i>/<i>R</i><sub>b</sub> = {num(Rca)} Ω."),
         step("Check", f"Resistance a–b, terminal c open: star {R1 + R2} Ω; delta {num(Rab)} ∥ ({num(Rbc)} + {num(Rca)}) = {num(par(Rab, Rbc + Rca))} Ω.")],
        f"<i>R</i><sub>ab</sub> = {num(Rab)} Ω, <i>R</i><sub>bc</sub> = {num(Rbc)} Ω, <i>R</i><sub>ca</sub> = {num(Rca)} Ω", level=3, fig=fig, topic="delta-star")


def bridge_bal(r, tag):
    R1 = pick(r, [100, 200, 500, 1000, 2000])
    R2 = pick(r, [150, 330, 470, 680, 1000, 1200])
    R3 = pick(r, [120, 250, 400, 560, 750, 1500])
    Rx = R2 * R3 / R1
    V = pick(r, [5, 6, 10, 12])
    fig = bridge(tag, E("V", "V_s", f"{V} V"), E("R", "R_1", eng(R1, "Ω")), E("R", "R_2", eng(R2, "Ω")), E("R", "R_3", eng(R3, "Ω")), E("R", "R_x", "?"), mid=E("G", None, None))
    return Problem(
        "The Wheatstone bridge shown is adjusted until the galvanometer G reads zero. Find the unknown resistance <i>R</i><sub>x</sub>.",
        [step("Meaning of balance", "No current through G means nodes a and b are at the same potential, so each side divides the supply in the same ratio."),
         step("Balance condition", "<i>R</i><sub>1</sub>/<i>R</i><sub>3</sub> = <i>R</i><sub>2</sub>/<i>R</i><sub>x</sub>, so <i>R</i><sub>x</sub> = <i>R</i><sub>2</sub><i>R</i><sub>3</sub>/<i>R</i><sub>1</sub>."),
         step("Substitute", f"<i>R</i><sub>x</sub> = {R2} × {R3}/{R1} = {num(Rx)} Ω."),
         step("Note", f"The supply voltage ({V} V) does not appear in the answer; balance depends only on ratios, which is why the bridge is so accurate.")],
        f"<i>R</i><sub>x</sub> = {eng(Rx, 'Ω', 4)}", level=2, fig=fig, topic="bridge")


def bridge_v(r, tag):
    R1, R2, R3, R4 = [pick(r, [1, 2, 3, 4, 5, 6, 8, 10]) * 1000 for _ in range(4)]
    V = pick(r, [10, 12, 15, 20])
    Va = V * R3 / (R1 + R3)
    Vb = V * R4 / (R2 + R4)
    fig = bridge(tag, E("V", "V_s", f"{V} V"), E("R", "R_1", eng(R1, "Ω")), E("R", "R_2", eng(R2, "Ω")), E("R", "R_3", eng(R3, "Ω")), E("R", "R_4", eng(R4, "Ω")), mid=None)
    return Problem(
        "Find the open-circuit voltage <i>V</i><sub>ab</sub> of the bridge shown (potential of a relative to b).",
        [step("Treat each side as a divider", "With a and b open, each side of the bridge is a simple series pair across the supply."),
         step("Potential at a (measured from the bottom rail)", f"<i>V</i><sub>a</sub> = {V} × {num(R3)}/({num(R1)} + {num(R3)}) = {num(Va)} V."),
         step("Potential at b", f"<i>V</i><sub>b</sub> = {V} × {num(R4)}/({num(R2)} + {num(R4)}) = {num(Vb)} V."),
         step("Difference", f"<i>V</i><sub>ab</sub> = <i>V</i><sub>a</sub> − <i>V</i><sub>b</sub> = {num(Va - Vb)} V.")],
        f"<i>V</i><sub>ab</sub> = {eng(Va - Vb, 'V')}", level=2, fig=fig, topic="bridge")


def meter(r, tag):
    Ifs = pick(r, [50e-6, 100e-6, 1e-3, 2e-3])
    Rm = pick(r, [50, 100, 200, 500, 1000])
    if r.random() < 0.5:
        Imax = pick(r, [0.1, 0.5, 1, 5, 10])
        Rsh = Ifs * Rm / (Imax - Ifs)
        return Problem(
            f"A moving-coil movement has a full-scale current of {eng(Ifs, 'A')} and a coil resistance of {eng(Rm, 'Ω')}. Find the shunt resistance needed to make it read {eng(Imax, 'A')} at full scale.",
            [step("Voltage across the movement at full scale", f"<i>V</i><sub>m</sub> = <i>I</i><sub>fs</sub><i>R</i><sub>m</sub> = {num(Ifs)} × {Rm} = {eng(Ifs * Rm, 'V')}."),
             step("Shunt current", f"<i>I</i><sub>sh</sub> = {num(Imax)} − {num(Ifs)} = {num(Imax - Ifs)} A."),
             step("Shunt resistance (same voltage, it is in parallel)", f"<i>R</i><sub>sh</sub> = {num(Ifs * Rm)}/{num(Imax - Ifs)} = {eng(Rsh, 'Ω')}."),
             step("Practical point", "Such small shunts are usually four-terminal manganin strips, so lead and contact resistance do not spoil the reading.")],
            f"<i>R</i><sub>sh</sub> = {eng(Rsh, 'Ω')}", level=2, topic="meters")
    Vmax = pick(r, [10, 50, 100, 250])
    Rse = Vmax / Ifs - Rm
    return Problem(
        f"The same kind of movement, with full-scale current {eng(Ifs, 'A')} and coil resistance {eng(Rm, 'Ω')}, is to be used as a {Vmax} V voltmeter. Find the series multiplier resistance and the sensitivity in Ω/V.",
        [step("Total resistance needed", f"<i>R</i><sub>total</sub> = <i>V</i><sub>fs</sub>/<i>I</i><sub>fs</sub> = {Vmax}/{num(Ifs)} = {eng(Vmax / Ifs, 'Ω')}."),
         step("Multiplier", f"<i>R</i><sub>se</sub> = {eng(Vmax / Ifs, 'Ω')} − {eng(Rm, 'Ω')} = {eng(Rse, 'Ω', 4)}."),
         step("Sensitivity", f"1/<i>I</i><sub>fs</sub> = {eng(1 / Ifs, 'Ω')} per volt. Higher sensitivity means less loading of the circuit under test.")],
        f"<i>R</i><sub>se</sub> = {eng(Rse, 'Ω', 4)}; {eng(1 / Ifs, 'Ω')}/V", level=2, topic="meters")


def problems():
    plan = [(series, 6), (parallel, 6), (sp_a, 6), (sp_b, 5), (ladder4, 6), (vdiv, 5), (cdiv, 5), (loaded, 5),
            (delta_y, 5), (y_delta, 4), (bridge_bal, 5), (bridge_v, 5), (meter, 4)]
    return build(2, plan, 202)
