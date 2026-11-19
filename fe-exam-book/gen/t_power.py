"""Power systems, control systems, communications templates."""
import math
from qcore import *

PI = math.pi
S3 = math.sqrt(3)


# =============================================================== POWER SYSTEMS


@tpl("power")
def delta_line_current(rng):
    VL = rng.choice([208, 240, 400, 480, 600])
    Z = rng.choice([10, 12, 20, 24, 30, 40])
    Iph = VL / Z
    IL = S3 * Iph
    stem = f"A balanced delta-connected load has an impedance of {Z} Ω per phase and is supplied at {VL} V line-to-line. What is the line current?"
    sol = (f"In delta, each phase sees the full line voltage: $I_{{ph}} = V_L/Z = {VL}/{Z} = {mnum(Iph,4)}$ A.\n\n"
           f"$$I_L = \\sqrt3\\,I_{{ph}} = {mnum(IL,4)}\\ \\text{{A}}$$\n\n"
           "Mnemonic: in **delta** the **currents** pick up the $\\sqrt3$; in **wye** the **voltages** do.")
    return make(stem, num_mcq(rng, IL, [Iph, Iph / S3, 3 * Iph], lambda v: fu(v, "A")), sol)


@tpl("power")
def three_phase_power(rng):
    VL = rng.choice([400, 480, 4160, 13800, 11000])
    IL = rng.choice([25, 50, 100, 150, 200])
    pf = rng.choice([0.8, 0.85, 0.9, 0.95])
    P = S3 * VL * IL * pf
    stem = f"A balanced three-phase load draws {IL} A at {fnum(VL,5)} V line-to-line and {fnum(pf)} power factor. What real power does it consume?"
    sol = f"$$P = \\sqrt3 V_LI_L\\cos\\theta = \\sqrt3({mnum(VL,5)})({IL})({fnum(pf)}) = {em(P,'W')}$$\n\nThis formula uses *line* quantities and holds for both wye and delta loads."
    return make(stem, num_mcq(rng, P, [3 * VL * IL * pf, S3 * VL * IL, VL * IL * pf], lambda v: eng(v, "W")), sol)


@tpl("power")
def wye_load_power(rng):
    VL = rng.choice([208, 400, 480])
    Rv, X = rng.choice([(8, 6), (12, 9), (16, 12), (6, 8), (20, 15)])
    Z = math.hypot(Rv, X)
    Vph = VL / S3
    I = Vph / Z
    P = 3 * I * I * Rv
    stem = f"A balanced wye load of $({Rv} + j{X})\\ \\Omega$ per phase is connected to a {VL} V (line-to-line) three-phase supply. What total real power is absorbed?"
    sol = (f"$V_{{ph}} = V_L/\\sqrt3 = {mnum(Vph,4)}$ V; $|Z| = {mnum(Z,4)}\\ \\Omega$; $I = V_{{ph}}/|Z| = {mnum(I,4)}$ A.\n\n"
           f"$$P = 3I^2R = 3({mnum(I,4)})^2({Rv}) = {em(P,'W')}$$\n\n"
           "Using the line voltage as if it were the phase voltage triples the answer.")
    return make(stem, num_mcq(rng, P, [3 * (VL / Z) ** 2 * Rv, I * I * Rv, 3 * Vph ** 2 / Z], lambda v: eng(v, "W")), sol)


@tpl("power")
def transformer_current(rng):
    a = rng.choice([2, 4, 5, 10, 20])
    V1 = rng.choice([480, 2400, 4800, 240 * 5])
    ZL = rng.choice([2, 4, 5, 8, 10])
    V2 = V1 / a
    I2 = V2 / ZL
    I1 = I2 / a
    stem = f"An ideal step-down transformer with turns ratio {a}:1 has {V1:,} V applied to its primary and a {ZL} Ω resistive load on its secondary. What is the primary current?"
    sol = (f"$V_2 = V_1/a = {mnum(V2,4)}$ V, so $I_2 = V_2/Z_L = {mnum(I2,4)}$ A. Current transforms inversely to voltage:\n\n"
           f"$$I_1 = {frac('I_2','a')} = {mnum(I1,4)}\\ \\text{{A}}$$\n\n"
           f"Check with power: $V_1I_1 = V_2I_2 = {mnum(V2*I2,4)}$ W.")
    return make(stem, num_mcq(rng, I1, [I2, I2 * a, V1 / ZL], lambda v: fu(v, "A")), sol)


@tpl("power")
def referred_impedance(rng):
    a = rng.choice([2, 3, 4, 5, 10])
    Z2 = rng.choice([2, 4, 8, 16, 0.5])
    Z1 = a * a * Z2
    stem = f"A {fnum(Z2)} Ω load is connected to the secondary of an ideal transformer with a {a}:1 (primary:secondary) turns ratio. What impedance is seen at the primary?"
    sol = f"$$Z_1' = a^2Z_2 = ({a})^2({fnum(Z2)}) = {mnum(Z1,4)}\\ \\Omega$$\n\nImpedance transforms by the *square* of the turns ratio—the basis of impedance matching with transformers."
    return make(stem, num_mcq(rng, Z1, [a * Z2, Z2 / a ** 2, Z2 / a], lambda v: fu(v, "Ω")), sol)


@tpl("power")
def per_unit_change(rng):
    Zold = rng.choice([0.05, 0.08, 0.1, 0.12])
    Sold, Snew = rng.choice([(50, 100), (25, 100), (100, 50), (20, 10)])
    Vold, Vnew = rng.choice([(13.8, 13.8), (13.8, 13.2), (11, 12), (138, 132)])
    Znew = Zold * (Snew / Sold) * (Vold / Vnew) ** 2
    stem = (f"A generator has a reactance of {fnum(Zold)} pu on its own rating of {Sold} MVA, {fnum(Vold)} kV. What is its reactance on a system base of {Snew} MVA, {fnum(Vnew)} kV?")
    sol = (f"$$Z_{{pu,new}} = Z_{{pu,old}}\\left({frac('S_{new}','S_{old}')}\\right)\\left({frac('V_{old}','V_{new}')}\\right)^2 = {fnum(Zold)}\\left({frac(Snew,Sold)}\\right)\\left({frac(fnum(Vold),fnum(Vnew))}\\right)^2 = {mnum(Znew,4)}\\ \\text{{pu}}$$\n\n"
           "Per-unit impedance rises with the MVA base and falls with the square of the kV base.")
    wr = [Zold * (Sold / Snew) * (Vold / Vnew) ** 2, Zold * (Snew / Sold), Zold * (Snew / Sold) * (Vnew / Vold) ** 2]
    return make(stem, num_mcq(rng, Znew, wr, lambda v: fnum(v, 4) + " pu"), sol)


@tpl("power")
def induction_slip(rng):
    f = rng.choice([60, 50])
    P = rng.choice([2, 4, 6, 8])
    ns = 120 * f / P
    s = rng.choice([0.02, 0.03, 0.04, 0.05])
    nr = ns * (1 - s)
    nr = round(nr)
    s = (ns - nr) / ns
    if rng.random() < 0.6:
        stem = f"A {P}-pole, {f} Hz induction motor runs at {nr:,} rpm. What is its slip?"
        sol = (f"$$n_s = {frac('120f','P')} = {frac(f'120({f})', P)} = {mnum(ns,4)}\\ \\text{{rpm}}, \\qquad s = {frac('n_s - n_r','n_s')} = {mnum(s*100,3)}\\%$$\n\n"
               "Note the factor 120, not 60, when $P$ counts poles rather than pole pairs.")
        return make(stem, num_mcq(rng, s * 100, [(60 * f / P - nr) / (60 * f / P) * 100 if 60 * f / P > nr else s * 50, (ns - nr) / nr * 100, s * 1000], lambda v: fnum(v) + "%"), sol)
    fr = s * f
    stem = f"A {P}-pole, {f} Hz induction motor runs at {nr:,} rpm. What is the frequency of the rotor currents?"
    sol = (f"$n_s = 120f/P = {mnum(ns,4)}$ rpm and $s = (n_s - n_r)/n_s = {mnum(s,4)}$.\n\n$$f_r = sf = {mnum(s,4)}\\times{f} = {em(fr,'Hz')}$$\n\nAt standstill ($s = 1$) the rotor frequency equals the supply frequency.")
    return make(stem, num_mcq(rng, fr, [float(f), f * (1 - s), nr / 60], lambda v: eng(v, "Hz")), sol)


@tpl("power")
def dc_motor(rng):
    V = rng.choice([120, 220, 240, 500])
    Ra = rng.choice([0.2, 0.25, 0.4, 0.5, 1.0])
    Ia = rng.choice([10, 20, 40, 50])
    n1 = rng.choice([1000, 1200, 1500, 1750])
    Ea = V - Ia * Ra
    if rng.random() < 0.5:
        stem = f"A separately excited DC motor takes {Ia} A from a {V} V supply; its armature resistance is {fnum(Ra)} Ω. What is the back EMF?"
        sol = f"$$E_a = V - I_aR_a = {V} - ({Ia})({fnum(Ra)}) = {mnum(Ea,4)}\\ \\text{{V}}$$\n\nIn a motor the back EMF is *less* than the terminal voltage; in a generator it is more."
        return make(stem, num_mcq(rng, Ea, [V + Ia * Ra, float(V), V - Ia / Ra if V - Ia / Ra > 0 else V - 2 * Ia * Ra], lambda v: fu(v, "V", 4)), sol)
    Ia2 = Ia * rng.choice([0.5, 1.5, 2])
    Ea2 = V - Ia2 * Ra
    n2 = n1 * Ea2 / Ea
    stem = (f"A separately excited DC motor ({V} V, $R_a = {fnum(Ra)}\\ \\Omega$) runs at {n1:,} rpm drawing {Ia} A. The load changes so that it draws {fnum(Ia2)} A, with field current unchanged. What is the new speed?")
    sol = (f"With constant flux, speed is proportional to back EMF.\n\n$E_{{a1}} = {V} - {Ia}({fnum(Ra)}) = {mnum(Ea,4)}$ V; $E_{{a2}} = {V} - {fnum(Ia2)}({fnum(Ra)}) = {mnum(Ea2,4)}$ V.\n\n"
           f"$$n_2 = n_1{frac('E_{a2}','E_{a1}')} = {n1}\\times{frac(mnum(Ea2,4), mnum(Ea,4))} = {mnum(n2,4)}\\ \\text{{rpm}}$$")
    return make(stem, num_mcq(rng, n2, [float(n1), n1 * Ia / Ia2, n1 * Ea / Ea2], lambda v: f"{v:,.0f} rpm"), sol)


@tpl("power")
def torque(rng):
    P = rng.choice([5, 7.5, 15, 37, 75, 110]) * 1e3
    n = rng.choice([960, 1440, 1460, 1750, 2900, 3550])
    w = 2 * PI * n / 60
    T = P / w
    stem = f"A motor delivers {eng(P,'W')} of shaft power at {n:,} rpm. What is the shaft torque?"
    sol = f"Convert speed to rad/s: $\\omega = 2\\pi n/60 = {mnum(w,4)}$ rad/s.\n\n$$T = {frac('P','\\omega')} = {frac(mnum(P), mnum(w,4))} = {mnum(T,4)}\\ \\text{{N·m}}$$"
    return make(stem, num_mcq(rng, T, [P / n, P / (2 * PI * n), P * 60 / n], lambda v: fu(v, "N·m")), sol)


@tpl("power")
def transformer_eff(rng):
    S = rng.choice([25, 50, 100, 250]) * 1e3
    Pc = S * rng.choice([0.004, 0.005, 0.003])
    Pcu = S * rng.choice([0.01, 0.012, 0.015])
    x = rng.choice([0.5, 0.75, 1.0])
    pf = rng.choice([0.8, 0.85, 1.0])
    Po = x * S * pf
    eta = Po / (Po + Pc + x * x * Pcu)
    stem = (f"A {eng(S,'VA')} transformer has a core loss of {eng(Pc,'W')} and a full-load copper loss of {eng(Pcu,'W')}. What is its efficiency at {int(x*100)}% load and {fnum(pf)} power factor?")
    sol = (f"Output $P_o = xS\\cos\\theta = {em(Po,'W',4)}$. Core loss is constant; copper loss scales with $x^2$: ${em(x*x*Pcu,'W',4)}$.\n\n"
           f"$$\\eta = {frac('P_o','P_o + P_{core} + x^2P_{cu}')} = {mnum(eta*100,4)}\\%$$\n\n"
           "Maximum efficiency occurs at the load where copper loss equals core loss.")
    wr = [Po / (Po + Pc + x * Pcu), Po / (Po + x * x * Pcu), Po / (Po + Pc + Pcu)]
    if x == 1.0:
        wr[0] = Po / (Po + Pc / 2 + Pcu)
        wr[2] = (Po - Pc - Pcu) / Po
    return make(stem, num_mcq(rng, eta * 100, [w * 100 for w in wr], lambda v: fnum(v, 4) + "%"), sol)


@tpl("power")
def voltage_regulation(rng):
    VFL = rng.choice([220, 230, 240, 480])
    VNL = VFL * rng.choice([1.02, 1.03, 1.05, 1.04])
    VR = (VNL - VFL) / VFL * 100
    stem = f"A transformer secondary reads {fnum(VNL,4)} V at no load and {VFL} V at full load (same primary voltage). What is the voltage regulation?"
    sol = f"$$\\text{{VR}} = {frac('V_{NL} - V_{FL}','V_{FL}')}\\times100\\% = {frac(f'{mnum(VNL,4)} - {VFL}', VFL)}\\times100\\% = {mnum(VR,3)}\\%$$\n\nThe denominator is the *full-load* voltage."
    return make(stem, num_mcq(rng, VR, [(VNL - VFL) / VNL * 100, VNL / VFL, (VNL - VFL)], lambda v: fnum(v, 3) + "%"), sol)


@tpl("power")
def line_loss(rng):
    P = rng.choice([10, 20, 50, 100]) * 1e3
    V = rng.choice([480, 2400, 4160])
    pf = rng.choice([0.7, 0.8, 0.9])
    Rl = rng.choice([0.1, 0.2, 0.5, 1.0])
    I = P / (V * pf)
    loss = I * I * Rl
    stem = (f"A single-phase feeder of total loop resistance {fnum(Rl)} Ω delivers {eng(P,'W')} to a load at {V:,} V and {fnum(pf)} power factor. What power is lost in the feeder?")
    sol = (f"$$I = {frac('P','V\\cos\\theta')} = {frac(mnum(P), f'({V})({fnum(pf)})')} = {mnum(I,4)}\\ \\text{{A}}, \\qquad P_{{loss}} = I^2R = {em(loss,'W')}$$\n\n"
           f"At unity power factor the loss would fall to {eng((P/V)**2*Rl,'W')}: poor power factor costs real money in $I^2R$ losses.")
    return make(stem, num_mcq(rng, loss, [(P / V) ** 2 * Rl, I * Rl, loss / pf], lambda v: eng(v, "W")), sol)


@tpl("power")
def fault_current(rng):
    Sb = rng.choice([10, 50, 100]) * 1e6
    Vb = rng.choice([13.8, 11, 4.16, 34.5]) * 1e3
    X = rng.choice([0.08, 0.1, 0.12, 0.15, 0.2])
    Ib = Sb / (S3 * Vb)
    If = Ib / X
    stem = (f"A bolted three-phase fault occurs at a {fnum(Vb/1e3)} kV bus. The Thévenin reactance at the bus is {fnum(X)} pu on a {Sb/1e6:g} MVA base, and the prefault voltage is 1.0 pu. What is the fault current?")
    sol = (f"$$I_{{base}} = {frac('S_b','\\sqrt3 V_b')} = {frac(mnum(Sb), f'\\sqrt3({mnum(Vb,4)})')} = {em(Ib,'A',4)}$$\n\n"
           f"$$I_f = {frac('1.0','X_{pu}')}I_{{base}} = {frac(1, fnum(X))}\\times{em(Ib,'A',4)} = {em(If,'A')}$$")
    return make(stem, num_mcq(rng, If, [Sb / Vb / X, Ib * X, Ib / X / S3], lambda v: eng(v, "A")), sol)


@tpl("power")
def sync_speed(rng):
    f = rng.choice([50, 60, 400])
    P = rng.choice([2, 4, 6, 8, 12])
    ns = 120 * f / P
    stem = f"At what speed does a {P}-pole synchronous motor run when supplied at {f} Hz?"
    sol = f"$$n_s = {frac('120f','P')} = {frac(f'120({f})', P)} = {mnum(ns,5)}\\ \\text{{rpm}}$$\n\nA synchronous machine runs at exactly this speed at any load (until it pulls out of step)."
    return make(stem, num_mcq(rng, ns, [60 * f / P, 120 * f / (P / 2), 120 * f / P * 0.96], lambda v: f"{v:,.0f} rpm"), sol)


# =============================================================== CONTROL SYSTEMS


@tpl("control")
def closed_loop_pole(rng):
    K, a = rng.choice([2, 5, 10, 20]), rng.choice([1, 2, 4, 5])
    p = -(a + K)
    stem = f"A plant $G(s) = \\dfrac{{{K}}}{{s + {a}}}$ is placed in a unity negative-feedback loop. Where is the closed-loop pole?"
    sol = (f"$$T(s) = {frac('G','1 + G')} = {frac(K, f's + {a} + {K}')} \\;\\Rightarrow\\; s = -{a+K}$$\n\n"
           f"Feedback moves the pole from $-{a}$ to $-{a+K}$: the response becomes faster, with time constant $1/{a+K}$ s. The DC gain becomes ${K}/{a+K} = {mnum(K/(a+K),3)}$.")
    return make(stem, num_mcq(rng, p, [-a, -K, -(a - K) if a != K else -(a + 2 * K)], lambda v: f"s = {fnum(v)}", integer=True, positive=False), sol)


@tpl("control")
def ess_step(rng):
    K, a, b = rng.choice([5, 10, 20, 40]), rng.choice([1, 2, 4]), rng.choice([2, 5, 10])
    Kp = K / (a * b)
    e = 1 / (1 + Kp)
    stem = f"A unity-feedback system has $G(s) = \\dfrac{{{K}}}{{(s+{a})(s+{b})}}$. What is the steady-state error to a unit step input?"
    sol = (f"The system is type 0 (no free integrator). The position constant is $K_p = \\lim_{{s\\to0}}G(s) = {K}/({a}\\cdot{b}) = {mnum(Kp,4)}$.\n\n"
           f"$$e_{{ss}} = {frac(1,'1 + K_p')} = {mnum(e,4)}$$\n\nAdding an integrator (making it type 1) would drive this error to zero.")
    return make(stem, num_mcq(rng, e, [1 / Kp, Kp / (1 + Kp), 1 / (1 + K)], lambda v: fnum(v, 3)), sol)


@tpl("control")
def ess_ramp(rng):
    K, a = rng.choice([10, 20, 50, 100]), rng.choice([2, 4, 5, 10])
    Kv = K / a
    e = 1 / Kv
    stem = f"A unity-feedback system has $G(s) = \\dfrac{{{K}}}{{s(s+{a})}}$. What is the steady-state error to a unit ramp input?"
    sol = (f"Type 1 system: $K_v = \\lim_{{s\\to0}} sG(s) = {K}/{a} = {mnum(Kv,4)}$.\n\n$$e_{{ss}} = 1/K_v = {mnum(e,4)}$$\n\n"
           "A type 1 system tracks a step with zero error but a ramp with finite error.")
    return make(stem, num_mcq(rng, e, [Kv, 1 / (1 + Kv), a / (K + a)], lambda v: fnum(v, 3)), sol)


@tpl("control")
def second_order(rng):
    wn = rng.choice([2, 3, 4, 5, 10])
    z = rng.choice([0.2, 0.3, 0.4, 0.5, 0.6, 0.7])
    b, c = 2 * z * wn, wn * wn
    q = rng.choice(["zeta", "wn", "os", "ts"])
    TF = f"T(s) = \\dfrac{{{mnum(c)}}}{{s^2 + {mnum(b)}s + {mnum(c)}}}"
    base = (f"Match to $\\dfrac{{\\omega_n^2}}{{s^2 + 2\\zeta\\omega_n s + \\omega_n^2}}$: $\\omega_n = \\sqrt{{{mnum(c)}}} = {wn}$ rad/s and $\\zeta = {frac(mnum(b), f'2({wn})')} = {mnum(z)}$.\n\n")
    if q == "zeta":
        stem = f"What is the damping ratio of ${TF}$?"
        return make(stem, num_mcq(rng, z, [b / c, b / 2, 1 / (2 * z)], lambda v: fnum(v)), base + "Damping ratio below 1 means an underdamped, overshooting step response.")
    if q == "wn":
        stem = f"What is the undamped natural frequency of ${TF}$?"
        return make(stem, num_mcq(rng, wn, [c, wn * math.sqrt(1 - z * z), b], lambda v: fu(v, "rad/s")), base + f"The *damped* frequency $\\omega_d = \\omega_n\\sqrt{{1-\\zeta^2}} = {mnum(wn*math.sqrt(1-z*z))}$ rad/s is a different quantity.")
    if q == "os":
        OS = 100 * math.exp(-z * PI / math.sqrt(1 - z * z))
        stem = f"What percentage overshoot does ${TF}$ show in response to a step input?"
        sol = base + f"$$\\%OS = 100\\,e^{{-\\zeta\\pi/\\sqrt{{1-\\zeta^2}}}} = 100\\,e^{{-{mnum(z)}\\pi/\\sqrt{{1-{mnum(z*z)}}}}} = {mnum(OS,3)}\\%$$\n\nOvershoot depends on $\\zeta$ alone, not on $\\omega_n$."
        return make(stem, num_mcq(rng, OS, [100 * math.exp(-z * PI), 100 * (1 - z), 100 * math.exp(-PI / math.sqrt(1 - z * z)) * 2], lambda v: fnum(v) + "%"), sol)
    Ts = 4 / (z * wn)
    stem = f"Using the 2% criterion, estimate the settling time of ${TF}$."
    sol = base + f"$$T_s \\approx {frac(4,'\\zeta\\omega_n')} = {frac(4, f'({mnum(z)})({wn})')} = {mnum(Ts,3)}\\ \\text{{s}}$$"
    return make(stem, num_mcq(rng, Ts, [4 / wn, PI / (wn * math.sqrt(1 - z * z)), 4 * z / wn], lambda v: fu(v, "s")), sol)


@tpl("control")
def routh(rng):
    a, b = rng.choice([(2, 3), (3, 4), (4, 5), (5, 6), (6, 2), (10, 2)])
    Kmax = a * b
    stem = f"For what range of $K$ is the closed-loop system with characteristic equation $s^3 + {a}s^2 + {b}s + K = 0$ stable?"
    sol = (f"Routh array:\n\n| | | |\n|:--|:--|:--|\n| $s^3$ | 1 | {b} |\n| $s^2$ | {a} | $K$ |\n| $s^1$ | ${frac(f'{a}({b}) - K', a)}$ | 0 |\n| $s^0$ | $K$ | |\n\n"
           f"For no sign changes in the first column we need $K > 0$ and ${a*b} - K > 0$, so **$0 < K < {Kmax}$**. At $K = {Kmax}$ the system oscillates at $\\omega = \\sqrt{{{b}}}$ rad/s.")
    corr = f"$0 < K < {Kmax}$"
    wr = [f"$0 < K < {a+b}$", f"$K > {Kmax}$", f"$0 < K < {mnum(b/a,3)}$"]
    return make(stem, str_mcq(rng, corr, wr), sol)


@tpl("control")
def dc_gain_db(rng):
    K, a, b = rng.choice([10, 50, 100, 200, 1000]), rng.choice([1, 2, 5]), rng.choice([10, 20, 50])
    g = K / (a * b)
    db = 20 * math.log10(g)
    stem = f"What is the low-frequency (DC) magnitude of $G(s) = \\dfrac{{{K}}}{{(s+{a})(s+{b})}}$ in decibels?"
    sol = (f"At DC, $s = 0$: $G(0) = {K}/({a}\\times{b}) = {mnum(g,4)}$.\n\n$$|G(0)|_{{dB}} = 20\\log_{{10}}({mnum(g,4)}) = {mnum(db,3)}\\ \\text{{dB}}$$\n\n"
           "The Bode magnitude starts flat at this value, bends down at 20 dB/decade after $\\omega = " + str(a) + "$ rad/s, and at 40 dB/decade after $\\omega = " + str(b) + "$ rad/s.")
    return make(stem, num_mcq(rng, db, [10 * math.log10(g), 20 * math.log10(K), g], lambda v: fu(v, "dB"), positive=False), sol)


@tpl("control")
def rise_time(rng):
    tau = rng.choice([0.1, 0.2, 0.5, 1, 2, 5])
    tr = 2.2 * tau
    stem = f"A first-order system has a time constant of {fnum(tau)} s. What is its 10%–90% rise time?"
    sol = f"$t_{{90}} - t_{{10}} = \\tau(\\ln 10 - \\ln(10/9)) = \\tau\\ln 9 = 2.2\\tau = {mnum(tr,3)}$ s."
    return make(stem, num_mcq(rng, tr, [tau, 4 * tau, 0.69 * tau], lambda v: fu(v, "s")), sol)


@tpl("control")
def block_reduction(rng):
    G1, G2, H = rng.choice([2, 5, 10]), rng.choice([3, 4, 8]), rng.choice([0.1, 0.2, 0.5, 1])
    T = G1 * G2 / (1 + G1 * G2 * H)
    stem = f"Blocks $G_1 = {G1}$ and $G_2 = {G2}$ are in cascade in the forward path of a negative-feedback loop with feedback gain $H = {fnum(H)}$. What is the overall gain $C/R$?"
    sol = f"$$\\frac{{C}}{{R}} = {frac('G_1G_2','1 + G_1G_2H')} = {frac(G1*G2, f'1 + {G1*G2}({fnum(H)})')} = {mnum(T,4)}$$\n\nWhen $G_1G_2H \\gg 1$ the gain approaches $1/H = {mnum(1/H)}$: the feedback path sets the gain."
    wr = [G1 * G2 / (1 - G1 * G2 * H) if 1 - G1 * G2 * H != 0 else 2 * T, float(G1 * G2), 1 / H if abs(1 / H - T) > 0.01 else T * 1.5]
    return make(stem, num_mcq(rng, T, wr, lambda v: fnum(v, 3), positive=False), sol)


@tpl("control")
def gain_margin(rng):
    mag = rng.choice([0.1, 0.2, 0.25, 0.4, 0.5])
    GM = -20 * math.log10(mag)
    stem = f"At the frequency where the open-loop phase is −180°, the open-loop magnitude $|G(j\\omega)H(j\\omega)|$ is {fnum(mag)}. What is the gain margin?"
    sol = f"$$GM = 20\\log_{{10}}{frac(1,'|GH|')} = -20\\log_{{10}}({fnum(mag)}) = {mnum(GM,3)}\\ \\text{{dB}}$$\n\nThe loop gain could be increased by a factor of ${mnum(1/mag)}$ before the system reaches the edge of instability."
    return make(stem, num_mcq(rng, GM, [-10 * math.log10(mag), 1 / mag, 20 * math.log10(1 + 1 / mag)], lambda v: fu(v, "dB")), sol)


@tpl("control")
def phase_margin_zeta(rng):
    PM = rng.choice([30, 40, 45, 50, 60, 65])
    z = PM / 100
    stem = f"An open-loop transfer function gives a phase margin of {PM}°. Using the common approximation for a second-order closed loop, estimate the damping ratio."
    sol = f"For phase margins below about 70°, $\\zeta \\approx \\text{{PM}}/100$ with PM in degrees, so $\\zeta \\approx {mnum(z)}$. More margin means more damping and less overshoot."
    return make(stem, num_mcq(rng, z, [PM / 180, math.cos(math.radians(PM)), z / 2], lambda v: fnum(v, 2)), sol)


# =============================================================== COMMUNICATIONS


@tpl("comms")
def am_power(rng):
    Pc = rng.choice([100, 500, 1000, 10000, 50000])
    m = rng.choice([0.3, 0.5, 0.6, 0.8, 1.0])
    Pt = Pc * (1 + m * m / 2)
    if rng.random() < 0.6:
        stem = f"An AM transmitter has a carrier power of {eng(Pc,'W')} and a modulation index of {fnum(m)} (sinusoidal modulation). What is the total transmitted power?"
        sol = f"$$P_t = P_c\\left(1 + {frac('m^2','2')}\\right) = {mnum(Pc)}\\left(1 + {frac(mnum(m*m), 2)}\\right) = {em(Pt,'W')}$$\n\nEven at 100% modulation only one third of the power is in the sidebands, which carry the information."
        return make(stem, num_mcq(rng, Pt, [Pc * (1 + m * m), Pc * (1 + m / 2), Pc * m * m / 2], lambda v: eng(v, "W")), sol)
    Psb = Pc * m * m / 4
    stem = f"An AM transmitter has a carrier power of {eng(Pc,'W')} and a modulation index of {fnum(m)}. What power is carried in *each* sideband?"
    sol = f"Total sideband power is $P_cm^2/2$, split equally between upper and lower sidebands:\n\n$$P_{{USB}} = P_{{LSB}} = {frac('P_cm^2','4')} = {em(Psb,'W')}$$"
    return make(stem, num_mcq(rng, Psb, [Pc * m * m / 2, Pc * m / 4, Pc * m * m], lambda v: eng(v, "W")), sol)


@tpl("comms")
def am_index(rng):
    Vmax = rng.choice([10, 12, 15, 20, 30])
    Vmin = Vmax * rng.choice([0.2, 0.25, 0.4, 0.5, 0.6])
    m = (Vmax - Vmin) / (Vmax + Vmin)
    stem = f"On an oscilloscope, an AM signal's envelope has a peak-to-peak maximum of {fnum(Vmax)} V and minimum of {fnum(Vmin)} V. What is the modulation index?"
    sol = f"$$m = {frac('V_{max} - V_{min}','V_{max} + V_{min}')} = {frac(f'{fnum(Vmax)} - {fnum(Vmin)}', f'{fnum(Vmax)} + {fnum(Vmin)}')} = {mnum(m,3)}$$"
    return make(stem, num_mcq(rng, m, [(Vmax - Vmin) / Vmax, Vmin / Vmax, (Vmax + Vmin) / (2 * Vmax)], lambda v: fnum(v, 3)), sol)


@tpl("comms")
def carson(rng):
    df = rng.choice([5, 25, 50, 75]) * 1e3
    fm = rng.choice([3, 5, 10, 15]) * 1e3
    B = 2 * (df + fm)
    stem = f"An FM signal has a peak frequency deviation of {eng(df,'Hz')} and a maximum modulating frequency of {eng(fm,'Hz')}. Estimate its bandwidth using Carson's rule."
    sol = f"$$B \\approx 2(\\Delta f + f_m) = 2({em(df,'Hz')} + {em(fm,'Hz')}) = {em(B,'Hz')}$$\n\nThe modulation index here is $\\beta = \\Delta f/f_m = {mnum(df/fm)}$."
    return make(stem, num_mcq(rng, B, [2 * df, df + fm, 2 * fm], lambda v: eng(v, "Hz")), sol)


@tpl("comms")
def shannon(rng):
    B = rng.choice([3e3, 1e6, 5e6, 20e6])
    snr_db = rng.choice([10, 20, 30, 15, 25])
    snr = 10 ** (snr_db / 10)
    Cc = B * math.log2(1 + snr)
    stem = f"A channel has a bandwidth of {eng(B,'Hz')} and a signal-to-noise ratio of {snr_db} dB. What is its Shannon capacity?"
    sol = (f"Convert dB to a ratio first: $\\text{{SNR}} = 10^{{{snr_db}/10}} = {mnum(snr,4)}$.\n\n$$C = B\\log_2(1 + \\text{{SNR}}) = {em(B,'Hz')}\\times\\log_2({mnum(1+snr,4)}) = {em(Cc,'bit/s')}$$\n\n"
           "Plugging the decibel figure straight into the formula is the classic error.")
    return make(stem, num_mcq(rng, Cc, [B * math.log2(1 + snr_db), B * math.log10(1 + snr), 2 * B * math.log2(1 + snr)], lambda v: eng(v, "bit/s")), sol)


@tpl("comms")
def nyquist_capacity(rng):
    B = rng.choice([3e3, 4e3, 10e3, 1e6])
    M = rng.choice([4, 8, 16, 64])
    Cc = 2 * B * math.log2(M)
    stem = f"What is the maximum data rate of a noiseless {eng(B,'Hz')} channel using {M} signal levels?"
    sol = f"Nyquist: $C = 2B\\log_2 M = 2({em(B,'Hz')})\\log_2 {M} = {em(Cc,'bit/s')}$."
    return make(stem, num_mcq(rng, Cc, [B * math.log2(M), 2 * B * M, 2 * B * math.log10(M)], lambda v: eng(v, "bit/s")), sol)


@tpl("comms")
def fspl(rng):
    d = rng.choice([1, 5, 10, 20, 50])
    f = rng.choice([100, 900, 2400, 5800])
    L = 20 * math.log10(d) + 20 * math.log10(f) + 32.44
    stem = f"What is the free-space path loss over {d} km at {fnum(f,4)} MHz?"
    sol = (f"$$L = 20\\log_{{10}}d_{{km}} + 20\\log_{{10}}f_{{MHz}} + 32.44 = {mnum(20*math.log10(d),4)} + {mnum(20*math.log10(f),4)} + 32.44 = {mnum(L,4)}\\ \\text{{dB}}$$\n\n"
           "This is just $20\\log_{10}(4\\pi d/\\lambda)$ with the unit conversions folded into the constant; doubling distance adds 6 dB.")
    return make(stem, num_mcq(rng, L, [10 * math.log10(d) + 10 * math.log10(f) + 32.44, 20 * math.log10(d) + 20 * math.log10(f), L + 6], lambda v: fu(v, "dB", 4)), sol)


@tpl("comms")
def link_budget(rng):
    Pt = rng.choice([20, 27, 30, 33, 40])
    Gt, Gr = rng.choice([3, 6, 10, 15]), rng.choice([0, 3, 6, 10])
    L = rng.choice([90, 100, 110, 120, 130])
    Pr = Pt + Gt + Gr - L
    stem = f"A transmitter outputs {Pt} dBm into an antenna of gain {Gt} dBi. The receiving antenna has a gain of {Gr} dBi and the path loss is {L} dB. What is the received power?"
    sol = f"Everything in decibels simply adds:\n\n$$P_r = P_t + G_t + G_r - L = {Pt} + {Gt} + {Gr} - {L} = {Pr}\\ \\text{{dBm}}$$"
    return make(stem, num_mcq(rng, Pr, [Pt - Gt - Gr - L, Pt + Gt + Gr + L - 2 * L - 10, Pt - L], lambda v: f"{fnum(v)} dBm", integer=True, positive=False), sol)


@tpl("comms")
def thermal_noise(rng):
    B = rng.choice([1e3, 10e3, 200e3, 1e6, 20e6])
    N = -174 + 10 * math.log10(B)
    stem = f"What is the thermal noise power, in dBm, in a {eng(B,'Hz')} bandwidth at room temperature (290 K)?"
    sol = (f"$N = kTB$; at 290 K, $kT = -174$ dBm/Hz. Therefore\n\n$$N = -174 + 10\\log_{{10}}({mnum(B)}) = {mnum(N,4)}\\ \\text{{dBm}}$$")
    return make(stem, num_mcq(rng, N, [-174 + 20 * math.log10(B), -204 + 10 * math.log10(B), -174 - 10 * math.log10(B)], lambda v: f"{fnum(v,4)} dBm", positive=False), sol)


@tpl("comms")
def friis(rng):
    NF1, G1, NF2 = rng.choice([1, 1.5, 2, 3]), rng.choice([10, 15, 20]), rng.choice([6, 8, 10, 12])
    F1, Gl, F2 = 10 ** (NF1 / 10), 10 ** (G1 / 10), 10 ** (NF2 / 10)
    F = F1 + (F2 - 1) / Gl
    NF = 10 * math.log10(F)
    stem = f"A receiver front end has an LNA (noise figure {fnum(NF1)} dB, gain {G1} dB) followed by a mixer with a noise figure of {NF2} dB. What is the overall noise figure?"
    sol = (f"Work in linear ratios: $F_1 = {mnum(F1,4)}$, $G_1 = {mnum(Gl,4)}$, $F_2 = {mnum(F2,4)}$.\n\n$$F = F_1 + {frac('F_2 - 1','G_1')} = {mnum(F,4)} \\;\\Rightarrow\\; NF = 10\\log_{{10}}F = {mnum(NF,3)}\\ \\text{{dB}}$$\n\n"
           "A high-gain, low-noise first stage dominates the noise figure of the whole chain.")
    return make(stem, num_mcq(rng, NF, [float(NF1 + NF2), 10 * math.log10(F1 + F2 - 1), NF1 + NF2 / G1], lambda v: fu(v, "dB")), sol)


@tpl("comms")
def pcm_rate(rng):
    fs = rng.choice([8e3, 16e3, 44.1e3, 48e3])
    n = rng.choice([8, 12, 16, 24])
    ch = rng.choice([1, 2, 24, 32])
    Rb = fs * n * ch
    stem = f"{ch} audio channel{'s are' if ch>1 else ' is'} digitised by PCM at {eng(fs,'Hz')} with {n} bits per sample. Ignoring framing overhead, what is the total bit rate?"
    sol = f"$$R_b = f_s\\times n\\times N_{{ch}} = {mnum(fs)}\\times{n}\\times{ch} = {em(Rb,'bit/s')}$$"
    return make(stem, num_mcq(rng, Rb, [fs * n, 2 * fs * n * ch, fs * ch * math.log2(n)], lambda v: eng(v, "bit/s")), sol)


@tpl("comms")
def qam_rate(rng):
    M = rng.choice([4, 16, 64, 256])
    Rs = rng.choice([1, 2.5, 5, 10]) * 1e6
    Rb = Rs * math.log2(M)
    stem = f"A {M}-QAM link transmits {eng(Rs,'baud')}. What is the bit rate?"
    sol = f"Each symbol carries $\\log_2 {M} = {int(math.log2(M))}$ bits, so $R_b = {em(Rs,'baud')}\\times{int(math.log2(M))} = {em(Rb,'bit/s')}$."
    return make(stem, num_mcq(rng, Rb, [Rs * M, Rs / math.log2(M), Rs * math.sqrt(M)], lambda v: eng(v, "bit/s")), sol)
