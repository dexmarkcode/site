"""Electrical materials, DC circuits, AC circuits, transients and linear systems."""
import math
import cmath
from qcore import *
import qfig

PI = math.pi
EPS0 = 8.854e-12
Q_E = 1.602e-19


def deg(v, sig=3):
    return fnum(v, sig) + "°"


def par(a, b):
    return a * b / (a + b)


# =============================================================== MATERIALS


@tpl("materials")
def wire_resistance(rng):
    mat, rho = rng.choice([("copper", 1.72e-8), ("aluminium", 2.82e-8)])
    L = rng.choice([50, 100, 150, 250, 500])
    dmm = rng.choice([0.5, 0.8, 1.0, 1.5, 2.0])
    A = PI * (dmm / 1000) ** 2 / 4
    Rw = rho * L / A
    stem = (f"What is the resistance of {L} m of {mat} wire of diameter {fnum(dmm)} mm at 20 °C? "
            f"Take $\\rho = {mnum(rho)}\\ \\Omega\\cdot\\text{{m}}$.")
    sol = (f"Cross-sectional area $A = \\pi d^2/4 = \\pi({mnum(dmm/1000)})^2/4 = {mnum(A)}\\ \\text{{m}}^2$.\n\n"
           f"$$R = {frac('\\rho L','A')} = {frac(f'({mnum(rho)})({L})', mnum(A))} = {em(Rw,'Ω')}$$\n\n"
           "Treating the diameter as the radius divides the answer by four; forgetting to convert millimetres to metres changes it by a factor of a million.")
    wr = [Rw / 4, rho * L / (dmm / 1000) ** 2, Rw * 4, Rw * PI / 4]
    return make(stem, num_mcq(rng, Rw, wr, lambda v: eng(v, "Ω")), sol)


@tpl("materials")
def temp_coeff(rng):
    R20 = rng.choice([10, 25, 50, 100, 120])
    T = rng.choice([60, 75, 90, 105, -10, 0])
    a = 0.00393
    RT = R20 * (1 + a * (T - 20))
    stem = (f"A copper winding measures {R20} Ω at 20 °C. What is its resistance at {T} °C? "
            "Take the temperature coefficient of resistance of copper as $\\alpha_{20} = 0.00393\\ /^\\circ\\text{C}$.")
    sol = (f"$$R_T = R_{{20}}\\left[1 + \\alpha_{{20}}(T - 20)\\right] = {R20}\\left[1 + 0.00393({T} - 20)\\right] = {mnum(RT,4)}\\ \\Omega$$\n\n"
           "Use the temperature *difference* from the reference, not the absolute temperature. Metals have positive coefficients, so resistance rises with heat.")
    wr = [R20 * (1 + a * T), R20 * a * abs(T - 20), R20 * (1 - a * (T - 20))]
    return make(stem, num_mcq(rng, RT, wr, lambda v: fu(v, "Ω", 4)), sol)


@tpl("materials")
def doped_resistivity(rng):
    ND = rng.choice([1e15, 2e15, 5e15, 1e16, 5e16])
    mun, mup = 1350, 480
    kind = rng.choice(["n", "p"])
    mu_ = mun if kind == "n" else mup
    wrongmu = mup if kind == "n" else mun
    sigma = Q_E * ND * mu_
    rho = 1 / sigma
    dop = "donor" if kind == "n" else "acceptor"
    stem = (f"Silicon is doped with {fnum(ND)} {dop} atoms per cm³ (all ionised). With $\\mu_n = 1350$ and $\\mu_p = 480\\ \\text{{cm}}^2/(\\text{{V·s}})$, "
            "what is the resistivity? Neglect minority carriers.")
    sol = (f"The material is {kind}-type, so conduction is by {'electrons' if kind=='n' else 'holes'}:\n\n"
           f"$$\\sigma = q N \\mu = (1.602\\times10^{{-19}})({mnum(ND)})({mu_}) = {mnum(sigma)}\\ \\text{{S/cm}}$$\n\n"
           f"$$\\rho = 1/\\sigma = {mnum(rho)}\\ \\Omega\\cdot\\text{{cm}}$$\n\n"
           "Using the wrong carrier mobility is the usual slip; also keep track of whether the answer is in Ω·cm or Ω·m (factor of 100).")
    wr = [1 / (Q_E * ND * wrongmu), rho / 100, rho * 100]
    return make(stem, num_mcq(rng, rho, wr, lambda v: fu(v, "Ω·cm")), sol)


@tpl("materials")
def dielectric_cap(rng):
    er, name = rng.choice([(2.2, "PTFE"), (3.5, "polyimide"), (4.4, "FR-4"), (6.0, "mica"), (10.0, "alumina")])
    Acm2 = rng.choice([1, 2, 4, 5, 10, 25])
    dmm = rng.choice([0.1, 0.2, 0.5, 1.0])
    C = EPS0 * er * Acm2 * 1e-4 / (dmm * 1e-3)
    stem = (f"A parallel-plate capacitor has plates of area {Acm2} cm² separated by {fnum(dmm)} mm of {name} ($\\varepsilon_r = {fnum(er)}$). "
            "Neglecting fringing, what is its capacitance?")
    sol = (f"$$C = {frac('\\varepsilon_0\\varepsilon_r A','d')} = {frac(f'(8.854\\times10^{{-12}})({fnum(er)})({mnum(Acm2*1e-4)})', mnum(dmm*1e-3))} = {em(C,'F')}$$\n\n"
           "Convert cm² to m² (×10⁻⁴) and mm to m (×10⁻³) before substituting.")
    wr = [C / er, C * 10, C / 10, C * 100]
    return make(stem, num_mcq(rng, C, wr, lambda v: eng(v, "F")), sol)


@tpl("materials")
def stretched_wire(rng):
    R0 = rng.choice([2, 4, 5, 8, 10, 12])
    n = rng.choice([2, 3, 1.5, 4])
    Rn = R0 * n * n
    stem = (f"A wire of resistance {R0} Ω is drawn out uniformly to {fnum(n)} times its original length, its volume unchanged. What is its new resistance?")
    sol = (f"Length increases by ${fnum(n)}$ and, because volume is constant, area falls by the same factor. Therefore\n\n"
           f"$$R' = \\rho{frac(f'{fnum(n)}L', f'A/{fnum(n)}')} = {fnum(n)}^2 R = {mnum(Rn)}\\ \\Omega$$\n\n"
           "Scaling only the length (×n) misses the thinning of the wire.")
    return make(stem, num_mcq(rng, Rn, [R0 * n, R0 / n, R0 * n ** 3], lambda v: fu(v, "Ω")), sol)


@tpl("materials")
def bandgap_wavelength(rng):
    mat, Eg = rng.choice([("GaAs", 1.42), ("silicon", 1.12), ("GaP", 2.26), ("InP", 1.34), ("GaN", 3.4)])
    lam = 1240 / Eg
    stem = (f"What is the longest wavelength of light that can create electron–hole pairs in {mat} ($E_g = {fnum(Eg)}$ eV)?")
    sol = (f"A photon must have energy at least $E_g$. With $E = hc/\\lambda$ and $hc = 1240$ eV·nm:\n\n"
           f"$$\\lambda_{{max}} = {frac('1240', fnum(Eg))} = {mnum(lam)}\\ \\text{{nm}}$$\n\n"
           "Longer wavelengths carry less energy and pass straight through the material.")
    return make(stem, num_mcq(rng, lam, [620 / Eg, 2480 / Eg, 1240 / Eg / 1.5], lambda v: fu(v, "nm")), sol)


# =============================================================== DC CIRCUITS


@tpl("dc")
def series_parallel(rng):
    Vs = rng.choice([9, 12, 15, 20, 24, 30, 48])
    R1, R2, R3 = R(rng, 100, 4700), R(rng, 220, 10000), R(rng, 220, 10000)
    Rp = par(R2, R3)
    Req = R1 + Rp
    I = Vs / Req
    variant = rng.choice(["I", "V2", "I3"])
    fig = qfig.series_parallel(Vs, R1, R2, R3)
    if variant == "I":
        stem = "For the circuit shown, what current does the source deliver?"
        ans, wr, fmt = I, [Vs / (R1 + R2 + R3), Vs / R1, Vs / (R1 + R2 * R3 / (R2 + R3) * 2)], lambda v: eng(v, "A")
        tail = f"$$I = {frac('V_s', 'R_{eq}')} = {frac(Vs, em(Req,'Ω',4))} = {em(I,'A')}$$"
    elif variant == "V2":
        V2 = I * Rp
        stem = "For the circuit shown, what is the voltage across $R_2$?"
        ans, wr, fmt = V2, [Vs * R2 / (R1 + R2), Vs * R1 / Req, Vs - V2 / 2], lambda v: eng(v, "V")
        tail = (f"$$V_2 = V_s{frac('R_2\\parallel R_3','R_1 + R_2\\parallel R_3')} = {Vs}\\times{frac(em(Rp,'Ω',4), em(Req,'Ω',4))} = {em(V2,'V')}$$")
    else:
        I3 = I * R2 / (R2 + R3)
        stem = "For the circuit shown, what is the current through $R_3$?"
        ans, wr, fmt = I3, [I * R3 / (R2 + R3), I, Vs / (R1 + R3)], lambda v: eng(v, "A")
        tail = (f"Total current $I = {em(I,'A')}$; by current division\n\n$$I_3 = I{frac('R_2','R_2+R_3')} = {em(I3,'A')}$$")
    sol = (f"$R_2$ and $R_3$ are in parallel: $R_2\\parallel R_3 = {frac('R_2R_3','R_2+R_3')} = {em(Rp,'Ω',4)}$. "
           f"Adding $R_1$ in series, $R_{{eq}} = {em(Req,'Ω',4)}$.\n\n{tail}\n\n"
           "Redraw the circuit if needed: parallel elements share both end nodes, not just one.")
    return make(stem, num_mcq(rng, ans, wr, fmt), sol, fig=fig)


@tpl("dc")
def loaded_divider(rng):
    Vs = rng.choice([5, 10, 12, 15, 24])
    R1, R2 = R(rng, 1000, 10000), R(rng, 1000, 10000)
    RL = R(rng, 1000, 22000)
    Rp = par(R2, RL)
    Vo = Vs * Rp / (R1 + Rp)
    stem = (f"A {Vs} V source feeds a divider of $R_1 = {em(R1,'Ω')}$ (top) and $R_2 = {em(R2,'Ω')}$ (bottom). "
            f"A load of {eng(RL,'Ω')} is connected across $R_2$. What is the load voltage?")
    sol = (f"The load sits in parallel with $R_2$: $R_2\\parallel R_L = {em(Rp,'Ω',4)}$. Then\n\n"
           f"$$V_o = V_s{frac('R_2\\parallel R_L','R_1 + R_2\\parallel R_L')} = {Vs}\\times{frac(em(Rp,'Ω',4), em(R1+Rp,'Ω',4))} = {em(Vo,'V')}$$\n\n"
           f"The unloaded divider would give {eng(Vs*R2/(R1+R2),'V')}; loading always pulls the output down.")
    wr = [Vs * R2 / (R1 + R2), Vs * RL / (R1 + RL), Vs * R1 / (R1 + Rp)]
    return make(stem, num_mcq(rng, Vo, wr, lambda v: eng(v, "V")), sol)


@tpl("dc")
def current_divider(rng):
    I = rng.choice([10e-3, 25e-3, 50e-3, 0.1, 2, 5])
    R1, R2 = R(rng, 100, 4700), R(rng, 100, 4700)
    while R2 == R1:
        R2 = R(rng, 100, 4700)
    I1 = I * R2 / (R1 + R2)
    stem = (f"A current of {eng(I,'A')} divides between two parallel resistors, $R_1 = {em(R1,'Ω')}$ and $R_2 = {em(R2,'Ω')}$. "
            "What current flows through $R_1$?")
    sol = (f"$$I_1 = I{frac('R_2','R_1 + R_2')} = {em(I,'A')}\\times{frac(em(R2,'Ω'), em(R1+R2,'Ω'))} = {em(I1,'A')}$$\n\n"
           "The *opposite* resistor goes on top: more current takes the lower-resistance path.")
    return make(stem, num_mcq(rng, I1, [I * R1 / (R1 + R2), I / 2, I * R1 / R2 if R1 < R2 else I * R2 / R1 / 2], lambda v: eng(v, "A")), sol)


@tpl("dc")
def thevenin_T(rng):
    Vs = rng.choice([10, 12, 18, 20, 24, 36])
    R1, R2, R3 = R(rng, 470, 6800), R(rng, 470, 10000), R(rng, 100, 4700)
    Vth = Vs * R2 / (R1 + R2)
    Rth = par(R1, R2) + R3
    variant = rng.choice(["Vth", "Rth", "IL"])
    if variant == "IL":
        RL = R(rng, 470, 10000)
        fig = qfig.t_network(Vs, R1, R2, R3, load=RL)
        IL = Vth / (Rth + RL)
        stem = "In the circuit shown, what current flows in the load resistor $R_L$?"
        ans, wr, fmt = IL, [Vs / (R1 + R2 + R3 + RL), Vth / RL, Vs / (R1 + R3 + RL)], lambda v: eng(v, "A")
        tail = (f"$$I_L = {frac('V_{Th}','R_{Th} + R_L')} = {frac(em(Vth,'V',4), em(Rth+RL,'Ω',4))} = {em(IL,'A')}$$")
    else:
        fig = qfig.t_network(Vs, R1, R2, R3)
        if variant == "Vth":
            stem = "What is the Thévenin equivalent voltage $V_{ab}$ of the circuit shown, seen from terminals a–b?"
            ans, wr, fmt = Vth, [Vs * R2 / (R1 + R2 + R3), Vs * R1 / (R1 + R2), Vs], lambda v: eng(v, "V")
            tail = "No current flows in $R_3$ on open circuit, so $R_3$ drops no voltage and $V_{Th}$ is simply the divider output."
        else:
            stem = "What is the Thévenin equivalent resistance of the circuit shown, seen from terminals a–b?"
            ans, wr, fmt = Rth, [R1 + R2 + R3, par(R1 + R3, R2), par(R1, R2)], lambda v: eng(v, "Ω")
            tail = "Kill the source (replace it with a short), then look back into a–b: $R_1$ and $R_2$ are in parallel, in series with $R_3$."
    sol = (f"Open-circuit voltage: $V_{{Th}} = V_s{frac('R_2','R_1 + R_2')} = {Vs}\\times{frac(em(R2,'Ω'), em(R1+R2,'Ω'))} = {em(Vth,'V',4)}$.\n\n"
           f"Equivalent resistance: $R_{{Th}} = R_1\\parallel R_2 + R_3 = {em(par(R1,R2),'Ω',4)} + {em(R3,'Ω')} = {em(Rth,'Ω',4)}$.\n\n{tail}")
    return make(stem, num_mcq(rng, ans, wr, fmt), sol, fig=fig)


@tpl("dc")
def norton(rng):
    Vs = rng.choice([10, 12, 15, 24])
    R1, R2, R3 = R(rng, 470, 4700), R(rng, 470, 4700), R(rng, 100, 2200)
    Vth = Vs * R2 / (R1 + R2)
    Rth = par(R1, R2) + R3
    IN = Vth / Rth
    stem = (f"A {Vs} V source in series with $R_1 = {em(R1,'Ω')}$ feeds a node; $R_2 = {em(R2,'Ω')}$ connects the node to the source's negative terminal, "
            f"and $R_3 = {em(R3,'Ω')}$ connects the node to output terminal a (terminal b is the source's negative terminal). "
            "What is the Norton current, i.e. the short-circuit current from a to b?")
    sol = (f"Short a–b. The source sees $R_1 + R_2\\parallel R_3$, or equivalently use $I_N = V_{{Th}}/R_{{Th}}$:\n\n"
           f"$V_{{Th}} = {em(Vth,'V',4)}$, $R_{{Th}} = R_1\\parallel R_2 + R_3 = {em(Rth,'Ω',4)}$\n\n"
           f"$$I_N = {frac(em(Vth,'V',4), em(Rth,'Ω',4))} = {em(IN,'A')}$$")
    wr = [Vs / R1, Vs / (R1 + R3), Vth / R3, Vs / (R1 + R2 + R3)]
    return make(stem, num_mcq(rng, IN, wr, lambda v: eng(v, "A")), sol)


@tpl("dc")
def max_power(rng):
    Vth = rng.choice([6, 10, 12, 20, 24, 50])
    Rth = R(rng, 8, 4700)
    P = Vth ** 2 / (4 * Rth)
    stem = (f"A source has a Thévenin equivalent of {Vth} V in series with {eng(Rth,'Ω')}. What is the maximum power it can deliver to a resistive load?")
    sol = (f"Maximum power transfer occurs when $R_L = R_{{Th}}$. The load then sees half the Thévenin voltage:\n\n"
           f"$$P_{{max}} = {frac('V_{Th}^2','4R_{Th}')} = {frac(f'{Vth}^2', f'4\\times {em(Rth,"Ω")}')} = {em(P,'W')}$$\n\n"
           "Efficiency at this point is only 50%, which is why power systems are never operated at maximum power transfer.")
    return make(stem, num_mcq(rng, P, [Vth ** 2 / Rth, Vth ** 2 / (2 * Rth), Vth ** 2 / (8 * Rth)], lambda v: eng(v, "W")), sol)


@tpl("dc")
def two_source(rng):
    V1, V2 = rng.choice([10, 12, 15, 20, 24]), rng.choice([5, 6, 9, 12, 18])
    R1, R2, R3 = R(rng, 1000, 6800), R(rng, 1000, 10000), R(rng, 1000, 6800)
    G = 1 / R1 + 1 / R2 + 1 / R3
    Vx = (V1 / R1 + V2 / R3) / G
    fig = qfig.two_source(V1, V2, R1, R2, R3)
    variant = rng.choice(["Vx", "IR2", "IR1", "super"])
    base = (f"Write KCL at node x, taking the bottom wire as reference:\n\n"
            f"$${frac('V_x - V_1','R_1')} + {frac('V_x','R_2')} + {frac('V_x - V_2','R_3')} = 0 \\;\\Rightarrow\\; "
            f"V_x = {frac('V_1/R_1 + V_2/R_3', '1/R_1 + 1/R_2 + 1/R_3')} = {em(Vx,'V',4)}$$\n\n")
    if variant == "Vx":
        stem = "In the circuit shown, what is the voltage at node x with respect to ground?"
        ans, wr, fmt = Vx, [(V1 + V2) / 2, (V1 / R1 - V2 / R3) / G, V1 * par(R2, R3) / (R1 + par(R2, R3))], lambda v: eng(v, "V")
        sol = base + "Writing one node equation is faster than two mesh equations here: one unknown instead of two."
    elif variant == "IR2":
        stem = "In the circuit shown, what current flows downward through $R_2$?"
        ans = Vx / R2
        wr, fmt = [(V1 + V2) / R2, V1 / (R1 + R2), (V1 - V2) / R2], lambda v: eng(v, "A")
        sol = base + f"$$I_{{R2}} = V_x/R_2 = {em(ans,'A')}$$"
    elif variant == "IR1":
        stem = "In the circuit shown, what current flows from $V_1$ through $R_1$ towards node x?"
        ans = (V1 - Vx) / R1
        if ans <= 0:
            ans = Vx / R2
            stem = "In the circuit shown, what current flows downward through $R_2$?"
            sol = base + f"$$I_{{R2}} = V_x/R_2 = {em(ans,'A')}$$"
        else:
            sol = base + f"$$I_{{R1}} = {frac('V_1 - V_x','R_1')} = {em(ans,'A')}$$\n\nA mesh analysis gives the same result with more algebra."
        wr, fmt = [V1 / R1, V1 / (R1 + R2), Vx / R1], lambda v: eng(v, "A")
    else:
        Rp = par(R2, R3)
        ans = V1 * Rp / (R1 + Rp)
        stem = "Using superposition, what component of the node-x voltage is due to $V_1$ acting alone?"
        wr, fmt = [V1 * R2 / (R1 + R2), Vx, V1 * R3 / (R1 + R3)], lambda v: eng(v, "V")
        sol = (f"Replace $V_2$ by a short circuit. $R_2$ and $R_3$ are then in parallel ($= {em(Rp,'Ω',4)}$), forming a divider with $R_1$:\n\n"
               f"$$V_x' = V_1{frac('R_2\\parallel R_3','R_1 + R_2\\parallel R_3')} = {em(ans,'V')}$$\n\n"
               f"Repeating with $V_1$ shorted and adding the two contributions recovers the full answer, $V_x = {em(Vx,'V',4)}$. A *voltage* source is turned off by shorting it; a *current* source by opening it.")
    return make(stem, num_mcq(rng, ans, wr, fmt), sol, fig=fig)


@tpl("dc")
def heater_voltage(rng):
    P, V = rng.choice([(2000, 240), (1500, 120), (3000, 230), (1000, 120), (2400, 240)])
    Vn = V * rng.choice([0.9, 0.92, 0.95, 1.05, 0.85])
    Pn = P * (Vn / V) ** 2
    stem = (f"A resistive heater is rated {P:,} W at {V} V. Assuming its resistance does not change, how much power does it draw at {fnum(Vn,4)} V?")
    sol = (f"First find the resistance: $R = V^2/P = {V}^2/{P} = {mnum(V*V/P,4)}\\ \\Omega$. Then\n\n"
           f"$$P' = {frac('V\'^2','R')} = P\\left({frac(mnum(Vn,4), V)}\\right)^2 = {mnum(Pn,4)}\\ \\text{{W}}$$\n\n"
           "Power scales with the *square* of voltage in a fixed resistance; scaling linearly is the trap.")
    return make(stem, num_mcq(rng, Pn, [P * Vn / V, float(P), P * (V / Vn) ** 2], lambda v: fu(v, "W", 4)), sol)


@tpl("dc")
def cap_network(rng):
    C1, C2, C3 = (rng.choice([2, 4, 6, 10, 12]) * 1e-6 for _ in range(3))
    V = rng.choice([10, 12, 24, 50, 100])
    Cp = C2 + C3
    Ceq = C1 * Cp / (C1 + Cp)
    W = 0.5 * Ceq * V ** 2
    stem = (f"Capacitor $C_1 = {em(C1,'F')}$ is connected in series with the parallel combination of $C_2 = {em(C2,'F')}$ and $C_3 = {em(C3,'F')}$. "
            f"The network is charged from {V} V. What total energy is stored?")
    sol = (f"Parallel capacitors add: $C_2 + C_3 = {em(Cp,'F')}$. Series capacitors combine like parallel resistors:\n\n"
           f"$$C_{{eq}} = {frac('C_1(C_2+C_3)','C_1 + C_2 + C_3')} = {em(Ceq,'F',4)}$$\n\n"
           f"$$W = \\tfrac{{1}}{{2}}C_{{eq}}V^2 = \\tfrac{{1}}{{2}}({em(Ceq,'F',4)})({V})^2 = {em(W,'J')}$$\n\n"
           "Capacitors combine in the opposite way to resistors—an easy reversal under time pressure.")
    wr = [0.5 * (C1 + C2 + C3) * V ** 2, Ceq * V ** 2, 0.5 * (C1 + par(C2, C3)) * V ** 2]
    return make(stem, num_mcq(rng, W, wr, lambda v: eng(v, "J")), sol)


@tpl("dc")
def delta_wye(rng):
    while True:
        Rab, Rbc, Rca = (rng.choice([10, 15, 20, 30, 40, 60, 90]) for _ in range(3))
        if len({Rab, Rbc, Rca}) == 3:
            break
    S = Rab + Rbc + Rca
    Ra = Rab * Rca / S
    stem = (f"A delta network has $R_{{ab}} = {Rab}\\ \\Omega$, $R_{{bc}} = {Rbc}\\ \\Omega$ and $R_{{ca}} = {Rca}\\ \\Omega$. "
            "In the equivalent wye, what is the resistance of the arm connected to node a?")
    sol = (f"Each wye arm equals the product of the two delta resistors touching that node divided by the sum of all three:\n\n"
           f"$$R_a = {frac('R_{ab}R_{ca}','R_{ab}+R_{bc}+R_{ca}')} = {frac(f'({Rab})({Rca})', S)} = {mnum(Ra,4)}\\ \\Omega$$\n\n"
           "Pick the two resistors that *meet at node a*; the opposite one appears only in the sum.")
    wr = [Rab * Rbc / S, Rbc * Rca / S, S / 3]
    return make(stem, num_mcq(rng, Ra, wr, lambda v: fu(v, "Ω", 4)), sol)


@tpl("dc")
def wheatstone(rng):
    R1, R2, R3 = R(rng, 100, 4700), R(rng, 100, 4700), R(rng, 100, 4700)
    Rx = R2 * R3 / R1
    stem = (f"A Wheatstone bridge has $R_1 = {em(R1,'Ω')}$ (a–c), $R_2 = {em(R2,'Ω')}$ (c–b), $R_3 = {em(R3,'Ω')}$ (a–d) and an unknown $R_x$ (d–b). "
            "The supply is connected across a–b and the galvanometer across c–d reads zero. What is $R_x$?")
    sol = (f"At balance the voltage ratios down each side are equal, so $R_1/R_2 = R_3/R_x$, giving\n\n"
           f"$$R_x = {frac('R_2R_3','R_1')} = {frac(f'({em(R2,"Ω")})({em(R3,"Ω")})', em(R1,'Ω'))} = {em(Rx,'Ω')}$$\n\n"
           "Check by cross-multiplication: opposite arms of a balanced bridge have equal products.")
    return make(stem, num_mcq(rng, Rx, [R1 * R3 / R2, R1 * R2 / R3, R2 + R3], lambda v: eng(v, "Ω")), sol)


@tpl("dc")
def internal_resistance(rng):
    E = rng.choice([12.6, 9.0, 6.0, 24.0, 48.0])
    RL = rng.choice([2, 4, 5, 10, 20])
    r = rng.choice([0.05, 0.1, 0.2, 0.5, 1.0])
    V = E * RL / (RL + r)
    I = V / RL
    stem = (f"A battery has an open-circuit voltage of {fnum(E)} V. With a {RL} Ω load connected, the terminal voltage falls to {fnum(V,4)} V. "
            "What is the battery's internal resistance?")
    sol = (f"Load current $I = V/R_L = {mnum(V,4)}/{RL} = {mnum(I,4)}$ A. The missing voltage is dropped inside the battery:\n\n"
           f"$$r = {frac('E - V','I')} = {frac(f'{fnum(E)} - {mnum(V,4)}', mnum(I,4))} = {mnum(r)}\\ \\Omega$$")
    return make(stem, num_mcq(rng, r, [(E - V) / E * RL * 2, E / I - r * 3, (E - V) / RL], lambda v: fu(v, "Ω")), sol)


@tpl("dc")
def inductor_energy(rng):
    L1, L2 = rng.choice([10, 20, 47, 100]) * 1e-3, rng.choice([5, 15, 33, 68]) * 1e-3
    I = rng.choice([0.5, 1, 2, 3, 5])
    mode = rng.choice(["series", "parallel"])
    Leq = L1 + L2 if mode == "series" else par(L1, L2)
    W = 0.5 * Leq * I ** 2
    other = par(L1, L2) if mode == "series" else L1 + L2
    stem = (f"Two uncoupled inductors, {eng(L1,'H')} and {eng(L2,'H')}, are connected in {mode}. The combination carries a total current of {fnum(I)} A. "
            "What is the total stored energy?")
    sol = (f"Uncoupled inductors combine like resistors: $L_{{eq}} = {em(Leq,'H',4)}$ ({mode}).\n\n"
           f"$$W = \\tfrac{{1}}{{2}}L_{{eq}}I^2 = \\tfrac{{1}}{{2}}({em(Leq,'H',4)})({fnum(I)})^2 = {em(W,'J')}$$")
    return make(stem, num_mcq(rng, W, [0.5 * other * I ** 2, Leq * I ** 2, 0.5 * Leq * I], lambda v: eng(v, "J")), sol)


# =============================================================== AC CIRCUITS


@tpl("ac")
def series_rl(rng):
    Rv = rng.choice([10, 20, 30, 47, 50, 100])
    L = rng.choice([10, 22, 47, 68, 100, 150]) * 1e-3
    f = rng.choice([50, 60, 400, 1000])
    XL = 2 * PI * f * L
    Z = math.hypot(Rv, XL)
    th = math.degrees(math.atan2(XL, Rv))
    if rng.random() < 0.6:
        stem = f"A {Rv} Ω resistor is in series with a {eng(L,'H')} inductor at {f} Hz. What is the magnitude of the impedance?"
        ans, wr, fmt = Z, [Rv + XL, math.hypot(Rv, f * L), XL], lambda v: eng(v, "Ω")
    else:
        stem = f"A {Rv} Ω resistor is in series with a {eng(L,'H')} inductor at {f} Hz. By what angle does the current lag the applied voltage?"
        ans, wr, fmt = th, [90 - th, math.degrees(math.atan(f * L / Rv)), math.degrees(math.atan(Rv / XL)) / 2], lambda v: deg(v)
    sol = (f"$X_L = 2\\pi fL = 2\\pi({f})({em(L,'H')}) = {em(XL,'Ω',4)}$.\n\n"
           f"$$|Z| = \\sqrt{{R^2 + X_L^2}} = {em(Z,'Ω',4)}, \\qquad \\theta = \\tan^{{-1}}{frac('X_L','R')} = {mnum(th)}^\\circ$$\n\n"
           "Resistance and reactance add as perpendicular phasors, never arithmetically. The current lags because the circuit is inductive.")
    return make(stem, num_mcq(rng, ans, wr, fmt), sol)


@tpl("ac")
def series_rc_current(rng):
    V = rng.choice([10, 24, 120, 230])
    Rv = R(rng, 100, 4700)
    C = rng.choice([0.1, 0.22, 0.47, 1.0, 2.2, 10]) * 1e-6
    f = rng.choice([60, 100, 500, 1000, 2000])
    XC = 1 / (2 * PI * f * C)
    I = V / math.hypot(Rv, XC)
    stem = (f"A {V} V (RMS), {f} Hz source drives a {eng(Rv,'Ω')} resistor in series with a {eng(C,'F')} capacitor. What is the RMS current?")
    sol = (f"$X_C = \\dfrac{{1}}{{2\\pi fC}} = {em(XC,'Ω',4)}$, so $|Z| = \\sqrt{{R^2 + X_C^2}} = {em(math.hypot(Rv,XC),'Ω',4)}$.\n\n"
           f"$$I = {frac('V','|Z|')} = {em(I,'A')}$$\n\n"
           "Adding $R + X_C$ directly is the most common error.")
    wr = [V / (Rv + XC), V / Rv, V / XC]
    return make(stem, num_mcq(rng, I, wr, lambda v: eng(v, "A")), sol)


@tpl("ac")
def resonance(rng):
    L = rng.choice([1, 2.2, 4.7, 10, 22, 100]) * 1e-3
    C = rng.choice([10, 22, 47, 100, 220, 470]) * 1e-9
    f0 = 1 / (2 * PI * math.sqrt(L * C))
    stem = f"What is the resonant frequency of a series circuit with $L = {em(L,'H')}$ and $C = {em(C,'F')}$?"
    sol = (f"$$f_0 = {frac(1, '2\\pi\\sqrt{LC}')} = {frac(1, f'2\\pi\\sqrt{{({mnum(L)})({mnum(C)})}}')} = {em(f0,'Hz')}$$\n\n"
           f"Quoting $1/\\sqrt{{LC}} = {em(2*PI*f0,'rad/s')}$ in hertz is a factor-of-$2\\pi$ error.")
    return make(stem, num_mcq(rng, f0, [2 * PI * f0, f0 / math.sqrt(2 * PI), 1 / (2 * PI * L * C) if 1 / (2 * PI * L * C) < 1e9 else f0 * 3], lambda v: eng(v, "Hz")), sol)


@tpl("ac")
def bandwidth(rng):
    Rv = rng.choice([5, 10, 20, 50, 100])
    L = rng.choice([1, 2, 5, 10, 20]) * 1e-3
    C = rng.choice([10, 47, 100, 220]) * 1e-9
    w0 = 1 / math.sqrt(L * C)
    f0 = w0 / (2 * PI)
    Qf = w0 * L / Rv
    BW = Rv / (2 * PI * L)
    if rng.random() < 0.5:
        stem = (f"A series RLC circuit has $R = {Rv}\\ \\Omega$, $L = {em(L,'H')}$ and $C = {em(C,'F')}$. What is its half-power bandwidth in hertz?")
        ans, wr, fmt = BW, [Rv / L, f0 * Qf, f0 / Qf * 2], lambda v: eng(v, "Hz")
    else:
        stem = (f"A series RLC circuit has $R = {Rv}\\ \\Omega$, $L = {em(L,'H')}$ and $C = {em(C,'F')}$. What is its quality factor $Q$?")
        ans, wr, fmt = Qf, [1 / Qf, Qf * 2 * PI, Rv * math.sqrt(C / L) * 100], lambda v: fnum(v)
    sol = (f"$\\omega_0 = 1/\\sqrt{{LC}} = {em(w0,'rad/s',4)}$ ($f_0 = {em(f0,'Hz',4)}$).\n\n"
           f"$$Q = {frac('\\omega_0 L','R')} = {mnum(Qf,4)}, \\qquad B = {frac('f_0','Q')} = {frac('R','2\\pi L')} = {em(BW,'Hz',4)}$$\n\n"
           "$R/L$ gives the bandwidth in rad/s; divide by $2\\pi$ for hertz.")
    return make(stem, num_mcq(rng, ans, wr, fmt), sol)


@tpl("ac")
def complex_power(rng):
    V = rng.choice([120, 230, 240, 480])
    I = rng.choice([2, 5, 8, 10, 15, 20])
    tv = rng.choice([0, 10, 20, 30])
    ti = tv - rng.choice([20, 25, 30, 36.87, 45, 53.13])
    phi = tv - ti
    P = V * I * math.cos(math.radians(phi))
    Qv = V * I * math.sin(math.radians(phi))
    which = rng.choice(["P", "Q"])
    stem = (f"A load has $\\mathbf{{V}} = {V}\\angle {mnum(tv,4)}^\\circ$ V (RMS) and $\\mathbf{{I}} = {I}\\angle {mnum(ti,4)}^\\circ$ A (RMS). "
            f"What {'real (average) power' if which=='P' else 'reactive power'} does it absorb?")
    sol = (f"The power-factor angle is the voltage angle minus the current angle: $\\phi = {mnum(tv,4)}^\\circ - ({mnum(ti,4)}^\\circ) = {mnum(phi,4)}^\\circ$.\n\n"
           f"$$\\mathbf{{S}} = \\mathbf{{V}}\\mathbf{{I}}^* = {V*I:,}\\angle {mnum(phi,4)}^\\circ = {mnum(P,4)} + j{mnum(Qv,4)}\\ \\text{{VA}}$$\n\n"
           f"So $P = {mnum(P,4)}$ W and $Q = {mnum(Qv,4)}$ var (positive: inductive, lagging). Using the conjugate of the current is what makes the angles subtract.")
    if which == "P":
        ans, wr, fmt = P, [V * I, Qv, V * I * math.cos(math.radians(tv + ti)) if abs(math.cos(math.radians(tv + ti))) > 0.05 else P / 2], lambda v: fu(v, "W", 4)
    else:
        ans, wr, fmt = Qv, [V * I, P, V * I * abs(math.sin(math.radians(tv + ti))) if abs(math.sin(math.radians(tv + ti))) > 0.05 else Qv / 2], lambda v: fu(v, "var", 4)
    return make(stem, num_mcq(rng, ans, wr, fmt), sol)


@tpl("ac")
def pf_correction(rng):
    P = rng.choice([10, 20, 50, 75, 100]) * 1e3
    pf1 = rng.choice([0.7, 0.75, 0.8])
    pf2 = rng.choice([0.9, 0.95, 1.0])
    V = rng.choice([240, 480, 4160])
    f = 60
    w = 2 * PI * f
    Qc = P * (math.tan(math.acos(pf1)) - math.tan(math.acos(pf2)))
    C = Qc / (w * V ** 2)
    stem = (f"A {P/1e3:g} kW single-phase load operates at {fnum(pf1)} power factor lagging from a {V} V, 60 Hz supply. "
            f"What parallel capacitance raises the power factor to {fnum(pf2)}{' lagging' if pf2<1 else ''}?")
    sol = (f"Reactive power to be cancelled: $Q_C = P(\\tan\\phi_1 - \\tan\\phi_2) = {P/1e3:g}\\text{{ k}}\\times({mnum(math.tan(math.acos(pf1)),4)} - {mnum(math.tan(math.acos(pf2)),4)}) = {em(Qc,'var',4)}$.\n\n"
           f"A capacitor supplies $Q_C = \\omega C V^2$, so\n\n$$C = {frac('Q_C','\\omega V^2')} = {frac(em(Qc,'var',4), f'(2\\pi\\cdot 60)({V})^2')} = {em(C,'F')}$$\n\n"
           "The real power $P$ is unchanged by the capacitor; only the reactive power and hence the current fall.")
    wr = [P * math.tan(math.acos(pf1)) / (w * V ** 2), Qc / (f * V ** 2), Qc / (w * 2 * V ** 2)]
    if pf2 == 1.0:
        wr[0] = Qc / (w * V ** 2) * pf1
    return make(stem, num_mcq(rng, C, wr, lambda v: eng(v, "F")), sol)


@tpl("ac")
def resistor_peak_power(rng):
    Vm = rng.choice([10, 20, 50, 100, 170, 325])
    Rv = rng.choice([8, 10, 50, 100, 1000])
    P = Vm ** 2 / (2 * Rv)
    stem = f"The voltage $v(t) = {Vm}\\cos(377t)$ V is applied to a {Rv} Ω resistor. What average power does the resistor dissipate?"
    sol = (f"Average power uses the RMS value, $V_{{rms}} = V_m/\\sqrt{{2}}$:\n\n$$P = {frac('V_{rms}^2','R')} = {frac('V_m^2','2R')} = {frac(f'{Vm}^2', f'2({Rv})')} = {em(P,'W')}$$\n\n"
           "Using the peak value directly doubles the answer. On the exam, always ask: *is this amplitude peak or RMS?*")
    return make(stem, num_mcq(rng, P, [Vm ** 2 / Rv, Vm ** 2 / (math.sqrt(2) * Rv), Vm ** 2 / (4 * Rv)], lambda v: eng(v, "W")), sol)


@tpl("ac")
def parallel_rc(rng):
    Rv = rng.choice([100, 200, 300, 500, 1000])
    XC = rng.choice([100, 150, 250, 400, 750, 1200])
    Z = Rv * XC / math.hypot(Rv, XC)
    stem = f"A {Rv} Ω resistor is in parallel with a capacitor whose reactance is {XC} Ω at the operating frequency. What is the magnitude of the combined impedance?"
    sol = (f"$$\\mathbf{{Z}} = {frac('R(-jX_C)','R - jX_C')} \\;\\Rightarrow\\; |Z| = {frac('RX_C','\\sqrt{R^2 + X_C^2}')} = {frac(f'({Rv})({XC})', mnum(math.hypot(Rv,XC),4))} = {mnum(Z,4)}\\ \\Omega$$\n\n"
           "The product-over-sum shortcut works only with complex numbers; using magnitudes in the denominator without the square root gives the wrong value.")
    return make(stem, num_mcq(rng, Z, [Rv * XC / (Rv + XC), math.hypot(Rv, XC), (Rv + XC) / 2], lambda v: fu(v, "Ω", 4)), sol)


@tpl("ac")
def ac_max_power(rng):
    Vth = rng.choice([10, 20, 50, 100, 120])
    Rt, Xt = rng.choice([4, 8, 10, 25, 50]), rng.choice([3, 6, 10, 20, -15, -8])
    P = Vth ** 2 / (4 * Rt)
    sign = "+" if Xt > 0 else "-"
    stem = (f"A source has a Thévenin equivalent of {Vth} V (RMS) in series with $\\mathbf{{Z}}_{{Th}} = {Rt} {sign} j{abs(Xt)}\\ \\Omega$. "
            "What is the maximum average power that can be delivered to a load of any impedance?")
    sol = (f"For maximum power the load is the complex conjugate, $\\mathbf{{Z}}_L = {Rt} {'-' if Xt>0 else '+'} j{abs(Xt)}\\ \\Omega$. The reactances cancel, the total impedance is $2R_{{Th}}$, and\n\n"
           f"$$P_{{max}} = {frac('|V_{Th}|^2','4R_{Th}')} = {frac(f'{Vth}^2', f'4({Rt})')} = {em(P,'W')}$$")
    return make(stem, num_mcq(rng, P, [Vth ** 2 / (4 * math.hypot(Rt, Xt)), Vth ** 2 / Rt, Vth ** 2 / (8 * Rt)], lambda v: eng(v, "W")), sol)


@tpl("ac")
def reactive_from_pf(rng):
    P = rng.choice([5, 12, 40, 80, 150, 500])
    pf = rng.choice([0.6, 0.7, 0.75, 0.8, 0.85, 0.9])
    phi = math.acos(pf)
    Qv = P * math.tan(phi)
    stem = f"A motor draws {P} kW at a power factor of {fnum(pf)} lagging. How much reactive power does it draw?"
    sol = (f"$\\phi = \\cos^{{-1}}({fnum(pf)}) = {mnum(math.degrees(phi))}^\\circ$, so\n\n$$Q = P\\tan\\phi = {P}\\tan({mnum(math.degrees(phi))}^\\circ) = {mnum(Qv,4)}\\ \\text{{kvar}}$$\n\n"
           f"Sketch the power triangle: $S = P/\\text{{pf}} = {mnum(P/pf,4)}$ kVA is the hypotenuse, not the reactive side.")
    return make(stem, num_mcq(rng, Qv, [P / pf, P * math.sin(phi), P * (1 - pf)], lambda v: fu(v, "kvar", 4)), sol)


@tpl("ac")
def phasor_sum(rng):
    A, B = rng.choice([10, 20, 30, 40]), rng.choice([10, 15, 25, 50])
    a, b = rng.choice([0, 30, 60]), rng.choice([-60, -90, 90, 120, -30])
    S = A * cmath.exp(1j * math.radians(a)) + B * cmath.exp(1j * math.radians(b))
    M = abs(S)
    stem = f"What is the amplitude of $v(t) = {A}\\cos(\\omega t {'+' if a>=0 else '-'} {abs(a)}^\\circ) + {B}\\cos(\\omega t {'+' if b>=0 else '-'} {abs(b)}^\\circ)$ V?"
    sol = (f"Add as phasors: ${A}\\angle {a}^\\circ + {B}\\angle {b}^\\circ = ({mnum(S.real,4)}) + j({mnum(S.imag,4)})$.\n\n"
           f"$$|V| = \\sqrt{{{mnum(S.real,4)}^2 + {mnum(S.imag,4)}^2}} = {mnum(M)}\\ \\text{{V}}$$\n\n"
           "Same-frequency sinusoids add as vectors; the amplitudes add arithmetically only when the phases are equal.")
    return make(stem, num_mcq(rng, M, [A + B, math.hypot(A, B), abs(A - B) if A != B else (A + B) / 3], lambda v: fu(v, "V")), sol)


@tpl("ac")
def vl_at_resonance(rng):
    V = rng.choice([1, 2, 5, 10])
    Rv = rng.choice([5, 10, 20])
    L = rng.choice([10, 20, 50]) * 1e-3
    C = rng.choice([100, 220, 470]) * 1e-9
    w0 = 1 / math.sqrt(L * C)
    XL = w0 * L
    VL = V / Rv * XL
    stem = (f"A {V} V (RMS) source drives a series circuit of $R = {Rv}\\ \\Omega$, $L = {em(L,'H')}$ and $C = {em(C,'F')}$ at its resonant frequency. "
            "What is the RMS voltage across the inductor?")
    sol = (f"At resonance $X_L = X_C$, so the source sees only $R$: $I = V/R = {mnum(V/Rv)}$ A.\n\n"
           f"$X_L = \\omega_0 L = L/\\sqrt{{LC}} = {mnum(XL,4)}\\ \\Omega$, hence $V_L = IX_L = QV = {mnum(VL,4)}$ V.\n\n"
           "The inductor and capacitor voltages can greatly exceed the supply—a real hazard in high-Q circuits.")
    return make(stem, num_mcq(rng, VL, [float(V), V * XL / (Rv + XL), V / (XL / Rv)], lambda v: fu(v, "V", 4)), sol)


@tpl("ac")
def z_from_measurement(rng):
    V = rng.choice([120, 230, 240])
    Rv, X = rng.choice([(6, 8), (12, 16), (9, 12), (15, 20), (24, 7), (5, 12)])
    Z = math.hypot(Rv, X)
    I = V / Z
    P = I * I * Rv
    stem = (f"Measurements on an inductive load give {V} V (RMS), {fnum(I,4)} A (RMS) and {fnum(P,4)} W. What is the load reactance?")
    sol = (f"$|Z| = V/I = {mnum(Z,4)}\\ \\Omega$ and the wattmeter sees only the resistance: $R = P/I^2 = {mnum(Rv,4)}\\ \\Omega$.\n\n"
           f"$$X = \\sqrt{{|Z|^2 - R^2}} = {mnum(X,4)}\\ \\Omega$$")
    return make(stem, num_mcq(rng, X, [Z, float(Rv), Z - Rv], lambda v: fu(v, "Ω", 3)), sol)


# =============================================================== LINEAR SYSTEMS / TRANSIENTS


@tpl("linsys")
def rc_step(rng):
    V = rng.choice([5, 10, 12, 15, 24])
    Rv = R(rng, 1000, 47000)
    C = rng.choice([0.1, 0.47, 1, 2.2, 10]) * 1e-6
    tau = Rv * C
    t = tau * rng.choice([0.5, 1, 1.5, 2, 3])
    mode = rng.choice(["charge", "discharge"])
    if mode == "charge":
        v = V * (1 - math.exp(-t / tau))
        stem = (f"An uncharged {eng(C,'F')} capacitor is connected through {eng(Rv,'Ω')} to a {V} V DC source at $t = 0$. What is the capacitor voltage at $t = {em(t,'s')}$?")
        expr = f"v_C(t) = V\\left(1 - e^{{-t/\\tau}}\\right) = {V}\\left(1 - e^{{-{mnum(t/tau)}}}\\right) = {em(v,'V')}"
        wr = [V * math.exp(-t / tau), V * t / tau if t / tau < 1 else V * 0.5, V * (1 - math.exp(-t / tau / 2))]
    else:
        v = V * math.exp(-t / tau)
        stem = (f"A {eng(C,'F')} capacitor charged to {V} V discharges through {eng(Rv,'Ω')} from $t = 0$. What is its voltage at $t = {em(t,'s')}$?")
        expr = f"v_C(t) = V_0e^{{-t/\\tau}} = {V}e^{{-{mnum(t/tau)}}} = {em(v,'V')}"
        wr = [V * (1 - math.exp(-t / tau)), V * math.exp(-t / (2 * tau)), V / (1 + t / tau)]
    sol = (f"Time constant $\\tau = RC = ({em(Rv,'Ω')})({em(C,'F')}) = {em(tau,'s')}$, so $t/\\tau = {mnum(t/tau)}$.\n\n$${expr}$$\n\n"
           "Useful landmarks: after one time constant a charging capacitor reaches 63.2% of its final value; a discharging one falls to 36.8%.")
    return make(stem, num_mcq(rng, v, wr, lambda x: eng(x, "V")), sol)


@tpl("linsys")
def rl_step(rng):
    V = rng.choice([12, 24, 48, 100])
    Rv = rng.choice([4, 6, 10, 20, 50])
    L = rng.choice([10, 50, 100, 200, 500]) * 1e-3
    tau = L / Rv
    t = tau * rng.choice([0.5, 1, 2, 3])
    i = V / Rv * (1 - math.exp(-t / tau))
    stem = (f"A {V} V DC source is switched at $t = 0$ onto a coil of resistance {Rv} Ω and inductance {eng(L,'H')}. What is the current at $t = {em(t,'s')}$?")
    sol = (f"$\\tau = L/R = {em(tau,'s')}$ and the final current is $V/R = {mnum(V/Rv)}$ A.\n\n"
           f"$$i(t) = {frac('V','R')}\\left(1 - e^{{-t/\\tau}}\\right) = {mnum(V/Rv)}\\left(1 - e^{{-{mnum(t/tau)}}}\\right) = {em(i,'A')}$$\n\n"
           "For RL circuits $\\tau = L/R$; writing $\\tau = RL$ is a common slip.")
    wr = [V / Rv, V / Rv * math.exp(-t / tau), V / Rv * (1 - math.exp(-t * Rv * L)) if (1 - math.exp(-t * Rv * L)) > 0.01 else i * 0.5]
    return make(stem, num_mcq(rng, i, wr, lambda x: eng(x, "A")), sol)


@tpl("linsys")
def time_to_percent(rng):
    tau = rng.choice([1, 2, 5, 10, 22, 47]) * 1e-3
    pct = rng.choice([50, 75, 90, 95, 99])
    t = tau * math.log(1 / (1 - pct / 100))
    stem = f"A first-order circuit has a time constant of {eng(tau,'s')}. How long after a step input does the response reach {pct}% of its final value?"
    sol = (f"$$1 - e^{{-t/\\tau}} = {mnum(pct/100)} \\;\\Rightarrow\\; t = \\tau\\ln{frac(1, f'1 - {mnum(pct/100)}')} = {em(tau,'s')}\\times{mnum(math.log(1/(1-pct/100)),4)} = {em(t,'s')}$$\n\n"
           "Handy multiples: 50% at 0.69τ, 90% at 2.3τ, 95% at 3τ, 99% at 4.6τ.")
    wr = [tau * math.log(1 / (pct / 100)) if pct != 50 else tau * 0.5, tau * pct / 100, tau * math.log(pct)]
    return make(stem, num_mcq(rng, t, wr, lambda x: eng(x, "s")), sol)


@tpl("linsys")
def inductor_switch(rng):
    Vs = rng.choice([12, 24, 48])
    R1 = rng.choice([4, 6, 8, 12])
    R2 = rng.choice([100, 220, 470, 1000])
    I0 = Vs / R1
    v0 = I0 * R2
    stem = (f"An inductor in series with $R_1 = {R1}\\ \\Omega$ has been connected to a {Vs} V DC source for a long time. "
            f"A {R2} Ω resistor is permanently connected across the inductor. At $t = 0$ the source and $R_1$ are disconnected. "
            "What is the magnitude of the voltage across the inductor immediately afterwards?")
    sol = (f"Before switching, the inductor is a short circuit in DC steady state, so it carries $I_0 = V_s/R_1 = {mnum(I0,4)}$ A "
           f"(the {R2} Ω resistor is shorted out by the inductor).\n\n"
           f"Inductor current cannot change instantaneously, so at $t = 0^+$ the same {mnum(I0,4)} A is forced through $R_2$:\n\n"
           f"$$|v_L(0^+)| = I_0R_2 = {mnum(I0,4)}\\times{R2} = {mnum(v0,4)}\\ \\text{{V}}$$\n\n"
           "This inductive kick—far above the supply voltage—is why relay coils need flyback diodes.")
    return make(stem, num_mcq(rng, v0, [float(Vs), Vs * R2 / (R1 + R2), 0.5 * v0], lambda x: fu(x, "V", 4)), sol)


@tpl("linsys")
def final_value(rng):
    K, a, b, c = rng.choice([5, 10, 20, 50]), rng.choice([1, 2, 3, 4]), rng.choice([1, 2, 5]), rng.choice([3, 4, 10])
    fv = K * a / (b * c)
    stem = f"What is the final value of $f(t)$ if $F(s) = \\dfrac{{{K}(s+{a})}}{{s(s+{b})(s+{c})}}$?"
    sol = (f"All poles of $sF(s)$ lie in the left half-plane, so the final value theorem applies:\n\n"
           f"$$\\lim_{{t\\to\\infty}} f(t) = \\lim_{{s\\to 0}} sF(s) = {frac(f'{K}({a})', f'({b})({c})')} = {mnum(fv,4)}$$\n\n"
           "Always check the pole condition first; the theorem gives nonsense for oscillating or growing signals.")
    return make(stem, num_mcq(rng, fv, [float(K), K / (b * c), K * a / (b + c)], lambda x: fnum(x, 4)), sol)


@tpl("linsys")
def initial_value(rng):
    A, B, c, d = rng.choice([2, 3, 4, 5, 7]), rng.choice([6, 8, 10, 12]), rng.choice([2, 3, 4]), rng.choice([5, 8, 13])
    stem = f"What is $f(0^+)$ if $F(s) = \\dfrac{{{A}s + {B}}}{{s^2 + {c}s + {d}}}$?"
    sol = (f"By the initial value theorem, $f(0^+) = \\lim_{{s\\to\\infty}} sF(s) = \\lim_{{s\\to\\infty}} \\dfrac{{{A}s^2 + {B}s}}{{s^2 + {c}s + {d}}} = {A}$.\n\n"
           f"Do not confuse it with $\\lim_{{s\\to 0}}$, which gives $F(0) = {mnum(B/d,4)}$ (not even the final value here, since there is no $1/s$).")
    return make(stem, num_mcq(rng, A, [B / d, float(B), 0.0 + A + c], lambda x: fnum(x, 3), positive=True), sol)


@tpl("linsys")
def inverse_laplace(rng):
    a, b = sorted(rng.sample([1, 2, 3, 4, 5, 6], 2))
    K = (b - a) * rng.choice([1, 2, 3, 5])
    k = K // (b - a)
    corr = f"${k}\\left(e^{{-{a}t}} - e^{{-{b}t}}\\right)u(t)$"
    wr = [f"${k}\\left(e^{{{a}t}} - e^{{{b}t}}\\right)u(t)$", f"${K}\\left(e^{{-{a}t}} + e^{{-{b}t}}\\right)u(t)$", f"${k}\\left(e^{{-{b}t}} - e^{{-{a}t}}\\right)u(t)$"]
    stem = f"What is the inverse Laplace transform of $F(s) = \\dfrac{{{K}}}{{(s+{a})(s+{b})}}$?"
    sol = (f"Partial fractions: $F(s) = \\dfrac{{A}}{{s+{a}}} + \\dfrac{{B}}{{s+{b}}}$. Cover-up gives $A = {K}/({b}-{a}) = {k}$ and $B = {K}/({a}-{b}) = -{k}$.\n\n"
           f"Since $\\mathcal{{L}}^{{-1}}\\{{1/(s+a)\\}} = e^{{-at}}u(t)$, the result is {corr}. Check: at $t = 0$ it is zero, as expected for a strictly proper transform with relative degree 2.")
    return make(stem, str_mcq(rng, corr, wr), sol)


@tpl("linsys")
def poles(rng):
    al, wd = rng.choice([1, 2, 3, 4]), rng.choice([1, 2, 3, 4, 5])
    b, c = 2 * al, al * al + wd * wd
    z = rng.choice([1, 2, 5, 10])
    corr = f"$s = -{al} \\pm j{wd}$"
    wr = [f"$s = {al} \\pm j{wd}$", f"$s = -{z}$ only", f"$s = -{b} \\pm j{c}$"]
    stem = f"Where are the poles of $H(s) = \\dfrac{{s + {z}}}{{s^2 + {b}s + {c}}}$, and is the system stable?"
    sol = (f"Poles are the roots of the denominator: $s = \\dfrac{{-{b} \\pm \\sqrt{{{b}^2 - 4({c})}}}}{{2}} = -{al} \\pm j{wd}$.\n\n"
           f"Both lie in the left half-plane, so the system is stable (with a damped oscillation at {wd} rad/s). $s = -{z}$ is a *zero*, not a pole.")
    return make(stem, str_mcq(rng, corr, wr), sol)


@tpl("linsys")
def rlc_zeta(rng):
    Rv = rng.choice([10, 20, 50, 100, 200, 400])
    L = rng.choice([10, 50, 100]) * 1e-3
    C = rng.choice([1, 2.2, 10]) * 1e-6
    zeta = Rv / 2 * math.sqrt(C / L)
    wn = 1 / math.sqrt(L * C)
    kind = "underdamped" if zeta < 0.98 else ("overdamped" if zeta > 1.02 else "critically damped")
    stem = (f"A series RLC circuit has $R = {Rv}\\ \\Omega$, $L = {em(L,'H')}$ and $C = {em(C,'F')}$. What is its damping ratio $\\zeta$?")
    sol = (f"For a series RLC circuit, $\\alpha = R/2L$ and $\\omega_0 = 1/\\sqrt{{LC}} = {em(wn,'rad/s',4)}$, so\n\n"
           f"$$\\zeta = {frac('\\alpha','\\omega_0')} = {frac('R','2')}\\sqrt{{{frac('C','L')}}} = {mnum(zeta)}$$\n\n"
           f"The response is therefore {kind}. (For a *parallel* RLC, $\\zeta = \\frac{{1}}{{2R}}\\sqrt{{L/C}}$—the resistor's role is inverted.)")
    wr = [1 / (2 * Rv) * math.sqrt(L / C), Rv * math.sqrt(C / L), Rv / (2 * L) / 1000]
    return make(stem, num_mcq(rng, zeta, wr, lambda x: fnum(x)), sol)


@tpl("linsys")
def discrete_conv(rng):
    x = [rng.randint(1, 4) for _ in range(3)]
    h = [rng.randint(-2, 3) or 1 for _ in range(2)]
    y = [0] * 4
    for n in range(4):
        for k in range(3):
            if 0 <= n - k < 2:
                y[n] += x[k] * h[n - k]
    n = rng.choice([1, 2])
    stem = (f"An LTI system has impulse response $h[n] = \\{{{h[0]}, {h[1]}\\}}$ (starting at $n = 0$). The input is $x[n] = \\{{{x[0]}, {x[1]}, {x[2]}\\}}$, also starting at $n = 0$. "
            f"What is the output $y[{n}]$?")
    terms = " + ".join(f"x[{k}]h[{n-k}]" for k in range(3) if 0 <= n - k < 2)
    nums = " + ".join(f"({x[k]})({h[n-k]})" for k in range(3) if 0 <= n - k < 2)
    sol = (f"Convolution: $y[n] = \\sum_k x[k]h[n-k]$. For $n = {n}$:\n\n$$y[{n}] = {terms} = {nums} = {y[n]}$$\n\n"
           f"The full output is $\\{{{', '.join(str(v) for v in y)}\\}}$, of length $3 + 2 - 1 = 4$.")
    wr = [x[n] * h[min(n, 1)], y[n - 1] if y[n - 1] != y[n] else y[n] + 2, sum(x) * sum(h) // 2 if sum(x) * sum(h) // 2 != y[n] else y[n] - 3]
    return make(stem, num_mcq(rng, y[n], wr, str, integer=True, positive=False), sol)


@tpl("linsys")
def first_order_step(rng):
    K = rng.choice([2, 4, 5, 10])
    tau = rng.choice([0.1, 0.5, 2, 5])
    A = rng.choice([1, 2, 3, 5])
    m = rng.choice([1, 2, 3])
    y = K * A * (1 - math.exp(-m))
    stem = (f"A system $G(s) = \\dfrac{{{K}}}{{{mnum(tau)}s + 1}}$ receives a step input of amplitude {A} at $t = 0$. What is the output at $t = {mnum(m*tau)}$ s?")
    sol = (f"Final value $KA = {K*A}$, time constant {mnum(tau)} s, so $t = {m}\\tau$:\n\n$$y = KA\\left(1 - e^{{-{m}}}\\right) = {K*A}\\times{mnum(1-math.exp(-m),4)} = {mnum(y,4)}$$")
    return make(stem, num_mcq(rng, y, [K * A * math.exp(-m), float(K * A), A * (1 - math.exp(-m))], lambda v: fnum(v, 3)), sol)
