from common import *

QE = 1.602e-19


def charge_time(r, tag):
    I = pick(r, [0.25, 0.5, 1.5, 2, 2.5, 3.2, 4, 6, 12.5])
    t_min = pick(r, [2, 5, 8, 10, 15, 20, 45, 90])
    ctx = pick(r, ["a car headlamp", "an electric drill", "a soldering iron", "a hair dryer element",
                   "a laboratory heater", "a cordless vacuum cleaner motor", "a toaster element"])
    t = t_min * 60
    Q = I * t
    return Problem(
        f"A steady current of {eng(I, 'A')} flows through {ctx} for {t_min} minutes. How much charge passes any cross-section of the circuit in that time?",
        [step("Convert the time to seconds", f"<i>t</i> = {t_min} × 60 = {num(t)} s."),
         step("Apply the definition of current", f"Since <i>I</i> = <i>Q</i>/<i>t</i>, the charge is <i>Q</i> = <i>It</i> = {num(I)} × {num(t)} = {num(Q)} C."),
         step("Sense-check", "A current of one ampere carries one coulomb every second, so the answer should be roughly the current multiplied by the number of seconds, which it is.")],
        f"<i>Q</i> = {eng(Q, 'C')}", level=1, topic="charge")


def electrons(r, tag):
    I = pick(r, [1e-3, 2.5e-3, 20e-3, 0.1, 0.5, 1, 3])
    t = pick(r, [1, 2, 10, 30, 60])
    Q = I * t
    n = Q / QE
    return Problem(
        f"A conductor carries a constant current of {eng(I, 'A')}. How many electrons pass a given point in {t} s? Take the electronic charge as 1.602 × 10<sup>−19</sup> C.",
        [step("Find the total charge", f"<i>Q</i> = <i>It</i> = {eng(I, 'A')} × {t} s = {eng(Q, 'C')}."),
         step("Divide by the charge on one electron", f"<i>n</i> = <i>Q</i>/<i>e</i> = {num(Q)} / (1.602 × 10<sup>−19</sup>) = {num(n)} electrons."),
         step("Comment", "Numbers this large are the reason we work in coulombs and amperes rather than counting electrons individually.")],
        f"<i>n</i> ≈ {num(n, 4)} electrons", level=1, topic="charge")


def current_from_charge(r, tag):
    Q = pick(r, [0.6, 1.8, 12, 45, 90, 240, 360])
    t = pick(r, [0.2, 3, 4, 15, 30, 120])
    I = Q / t
    return Problem(
        f"A charge of {eng(Q, 'C')} is transferred uniformly through a resistor in {eng(t, 's')}. Find the current.",
        [step("Recall the definition", "Current is the rate of flow of charge, <i>I</i> = <i>Q</i>/<i>t</i>."),
         step("Substitute", f"<i>I</i> = {num(Q)} / {num(t)} = {num(I)} A."),
         step("Express sensibly", f"<i>I</i> = {eng(I, 'A')}.")],
        f"<i>I</i> = {eng(I, 'A')}", level=1, topic="current")


def ohm_I(r, tag):
    V = pick(r, [5, 9, 12, 15, 24, 48, 230])
    R = R_ohms(r)
    I = V / R
    fig = ladder(tag, E("V", "V", f"{V} V"), [("S", E("W")), ("P", E("R", "R", eng(R, "Ω"), cur=None))])
    return Problem(
        f"A {V} V supply is connected across a {eng(R, 'Ω')} resistor, as shown. Find the current drawn from the supply.",
        [step("Identify what is known", f"The whole supply voltage appears across the resistor: <i>V</i> = {V} V, <i>R</i> = {eng(R, 'Ω')}."),
         step("Apply Ohm's law", f"<i>I</i> = <i>V</i>/<i>R</i> = {V} / {num(R)} = {num(I)} A."),
         step("Use a convenient prefix", f"<i>I</i> = {eng(I, 'A')}. (Volts divided by kilohms gives milliamperes directly, a useful shortcut.)")],
        f"<i>I</i> = {eng(I, 'A')}", level=1, fig=fig, topic="ohm")


def ohm_R(r, tag):
    V = pick(r, [1.5, 3.3, 5, 6, 12, 24, 110])
    I = pick(r, [0.002, 0.005, 0.015, 0.03, 0.25, 0.4, 1.2])
    R = V / I
    ctx = pick(r, ["an indicator lamp", "a heating element", "a sensor bridge arm", "a relay coil", "a strain gauge assembly"])
    return Problem(
        f"When {V} V is applied to {ctx}, the measured current is {eng(I, 'A')}. Assuming the device behaves as a linear resistor, what is its resistance?",
        [step("Rearrange Ohm's law", "<i>R</i> = <i>V</i>/<i>I</i>."),
         step("Substitute with consistent units", f"<i>R</i> = {num(V)} V / {num(I)} A = {num(R)} Ω."),
         step("State the result", f"<i>R</i> = {eng(R, 'Ω')}.")],
        f"<i>R</i> = {eng(R, 'Ω')}", level=1, topic="ohm")


def ohm_V(r, tag):
    R = R_ohms(r)
    I = pick(r, [0.5e-3, 1.2e-3, 4e-3, 25e-3, 0.15, 0.8, 2.5])
    V = I * R
    return Problem(
        f"A current of {eng(I, 'A')} flows through a {eng(R, 'Ω')} resistor. What voltage is developed across it, and which terminal is at the higher potential?",
        [step("Apply Ohm's law", f"<i>V</i> = <i>IR</i> = {num(I)} × {num(R)} = {num(V)} V."),
         step("Polarity", "In a resistor, current always flows from the higher potential to the lower one. The terminal where the current enters is therefore positive."),
         step("Result", f"<i>V</i> = {eng(V, 'V')}, positive where the current enters.")],
        f"<i>V</i> = {eng(V, 'V')}", level=1, topic="ohm")


def power_forms(r, tag):
    R = pick(r, [8, 12, 22, 47, 100, 150, 220, 470, 1000])
    mode = r.randrange(3)
    if mode == 0:
        V = pick(r, [5, 9, 12, 24])
        I = V / R
        P = V * V / R
        txt = f"A {eng(R, 'Ω')} resistor has {V} V across it. Calculate the current, the power dissipated, and state whether a 0.25 W resistor would be adequate."
        steps = [step("Current", f"<i>I</i> = <i>V</i>/<i>R</i> = {V}/{R} = {eng(I, 'A')}."),
                 step("Power", f"<i>P</i> = <i>V</i><sup>2</sup>/<i>R</i> = {V}<sup>2</sup>/{R} = {eng(P, 'W')}. Check: <i>P</i> = <i>VI</i> = {V} × {num(I)} = {num(V * I)} W."),
                 step("Rating", f"A 0.25 W part {'is adequate, though a margin of at least two is good practice' if P < 0.125 else ('would be working uncomfortably close to its limit; choose 0.5 W or more' if P < 0.25 else 'would overheat; a higher rating is required')}.")]
        ans = f"<i>I</i> = {eng(I, 'A')}, <i>P</i> = {eng(P, 'W')}"
    elif mode == 1:
        I = pick(r, [0.01, 0.02, 0.05, 0.1, 0.3])
        P = I * I * R
        txt = f"A current of {eng(I, 'A')} passes through a {eng(R, 'Ω')} resistor. Find the power dissipated and the voltage across the resistor."
        steps = [step("Power from current", f"<i>P</i> = <i>I</i><sup>2</sup><i>R</i> = ({num(I)})<sup>2</sup> × {R} = {eng(P, 'W')}."),
                 step("Voltage", f"<i>V</i> = <i>IR</i> = {num(I)} × {R} = {eng(I * R, 'V')}."),
                 step("Check", f"<i>VI</i> = {num(I * R)} × {num(I)} = {num(I * I * R)} W, which agrees.")]
        ans = f"<i>P</i> = {eng(P, 'W')}, <i>V</i> = {eng(I * R, 'V')}"
    else:
        P = pick(r, [0.25, 0.5, 1, 2, 5])
        Vmax = math.sqrt(P * R)
        Imax = math.sqrt(P / R)
        txt = f"A {eng(R, 'Ω')} resistor is rated at {P} W. What is the largest voltage that may be applied continuously, and what current flows at that voltage?"
        steps = [step("Rearrange the power equation", "<i>P</i> = <i>V</i><sup>2</sup>/<i>R</i>, so <i>V</i> = √(<i>PR</i>)."),
                 step("Substitute", f"<i>V</i><sub>max</sub> = √({P} × {R}) = {eng(Vmax, 'V')}."),
                 step("Current", f"<i>I</i><sub>max</sub> = √(<i>P</i>/<i>R</i>) = √({P}/{R}) = {eng(Imax, 'A')}. Check: <i>V</i>/<i>R</i> = {num(Vmax / R)} A.")]
        ans = f"<i>V</i><sub>max</sub> = {eng(Vmax, 'V')}, <i>I</i> = {eng(Imax, 'A')}"
    return Problem(txt, steps, ans, level=1 if mode < 2 else 2, topic="power")


def energy_cost(r, tag):
    app = pick(r, [("an electric kettle", 3000, 0.25), ("an immersion heater", 3000, 2.5), ("a fan heater", 2000, 4),
                   ("a desktop computer", 180, 8), ("a television", 95, 5), ("a dishwasher", 1800, 1.5),
                   ("a garage floodlight", 400, 6), ("an electric shower", 9500, 0.3)])
    name, Pw, hrs = app
    days = pick(r, [30, 31, 90, 365])
    price = pick(r, [24.5, 26.0, 27.3, 22.4, 28.6])
    E = Pw / 1000 * hrs * days
    cost = E * price / 100
    return Problem(
        f"{name[0].upper() + name[1:]} rated at {eng(Pw, 'W')} is used for {hrs} hours a day for {days} days. If electricity costs {price}p per kWh, find the energy used and the cost.",
        [step("Convert power to kilowatts", f"<i>P</i> = {Pw}/1000 = {num(Pw / 1000)} kW."),
         step("Total operating time", f"{hrs} h/day × {days} days = {num(hrs * days)} h."),
         step("Energy", f"<i>W</i> = <i>Pt</i> = {num(Pw / 1000)} × {num(hrs * days)} = {num(E)} kWh. (In joules this is {num(E * 3.6e6)} J, since 1 kWh = 3.6 MJ.)"),
         step("Cost", f"{num(E)} kWh × {price}p = {num(E * price)}p = {money(cost)}.")],
        f"{num(E)} kWh, costing {money(cost)}", level=2, topic="energy")


def resistivity(r, tag):
    mat = pick(r, [("copper", 1.72e-8), ("aluminium", 2.82e-8), ("nichrome", 1.10e-6), ("tungsten", 5.6e-8)])
    L = pick(r, [0.5, 2, 10, 25, 50, 100, 250])
    dmm = pick(r, [0.2, 0.5, 1.0, 1.5, 2.0, 2.5])
    A = math.pi * (dmm * 1e-3) ** 2 / 4
    R = mat[1] * L / A
    return Problem(
        f"Find the resistance of {L} m of {mat[0]} wire of circular cross-section and diameter {dmm} mm. Take the resistivity of {mat[0]} as {num(mat[1], 3)} Ω m.",
        [step("Cross-sectional area", f"<i>A</i> = π<i>d</i><sup>2</sup>/4 = π × ({num(dmm * 1e-3)})<sup>2</sup>/4 = {num(A)} m<sup>2</sup>. Keep everything in metres."),
         step("Apply R = ρL/A", f"<i>R</i> = ({num(mat[1], 3)} × {L}) / {num(A)} = {num(R)} Ω."),
         step("Interpretation", f"<i>R</i> ≈ {eng(R, 'Ω')}. Doubling the diameter would quarter the resistance, because area goes with the square of diameter.")],
        f"<i>R</i> = {eng(R, 'Ω')}", level=2, topic="resistivity")


def tempco(r, tag):
    R0 = pick(r, [10, 50, 100, 120, 500, 1000])
    a = pick(r, [0.00393, 0.0043, 0.0045, 0.00385])
    T1 = pick(r, [20, 0])
    T2 = pick(r, [60, 75, 85, 120, 150, 200])
    R = R0 * (1 + a * (T2 - T1))
    return Problem(
        f"A coil has a resistance of {eng(R0, 'Ω')} at {T1} °C. Its temperature coefficient of resistance referred to {T1} °C is {a} /°C. Find its resistance at {T2} °C.",
        [step("Write the linear model", f"<i>R</i><sub>θ</sub> = <i>R</i><sub>{T1}</sub>[1 + α(θ − {T1})]."),
         step("Temperature rise", f"Δθ = {T2} − {T1} = {T2 - T1} °C."),
         step("Substitute", f"<i>R</i> = {R0} × [1 + {a} × {T2 - T1}] = {R0} × {num(1 + a * (T2 - T1))} = {num(R)} Ω."),
         step("Comment", f"The resistance has risen by {num((R / R0 - 1) * 100, 3)} per cent. That is why motor windings are tested hot as well as cold.")],
        f"<i>R</i> = {eng(R, 'Ω', 4)}", level=2, topic="tempco")


def efficiency(r, tag):
    dev = pick(r, ["a DC motor", "a switch-mode power supply", "a battery charger", "a small transformer", "an LED driver"])
    Vin = pick(r, [12, 24, 48, 230])
    Iin = pick(r, [0.5, 1.2, 2, 3.5, 5])
    eta = pick(r, [0.72, 0.8, 0.85, 0.88, 0.92])
    Pin = Vin * Iin
    Pout = Pin * eta
    return Problem(
        f"{dev[0].upper() + dev[1:]} draws {eng(Iin, 'A')} from a {Vin} V supply and delivers {eng(Pout, 'W')} of useful output power. Find its efficiency and the power wasted as heat.",
        [step("Input power", f"<i>P</i><sub>in</sub> = <i>VI</i> = {Vin} × {num(Iin)} = {num(Pin)} W."),
         step("Efficiency", f"η = <i>P</i><sub>out</sub>/<i>P</i><sub>in</sub> = {num(Pout)}/{num(Pin)} = {num(eta, 3)}, or {num(eta * 100, 3)} %."),
         step("Losses", f"<i>P</i><sub>loss</sub> = {num(Pin)} − {num(Pout)} = {num(Pin - Pout)} W, which must be removed as heat.")],
        f"η = {num(eta * 100, 3)} %, losses {eng(Pin - Pout, 'W')}", level=2, topic="efficiency")


def q_of_t(r, tag):
    a = pick(r, [2, 3, 4, 5, 6])
    b = pick(r, [1, 2, 5, 10])
    c = pick(r, [0, 1, 3])
    t0 = pick(r, [0.5, 1, 2, 3])
    i = 2 * a * t0 + b
    form = r.randrange(2)
    if form == 0:
        q = f"<i>q</i>(<i>t</i>) = {a}<i>t</i><sup>2</sup> + {b}<i>t</i> + {c}"
        steps = [step("Differentiate", f"<i>i</i>(<i>t</i>) = d<i>q</i>/d<i>t</i> = {2 * a}<i>t</i> + {b} A."),
                 step("Evaluate", f"At <i>t</i> = {t0} s: <i>i</i> = {2 * a} × {t0} + {b} = {num(i)} A."),
                 step("Charge transferred", f"Between 0 and {t0} s the charge delivered is <i>q</i>({t0}) − <i>q</i>(0) = {num(a * t0 ** 2 + b * t0)} C.")]
        ans = f"<i>i</i>({t0}) = {num(i)} A"
        txt = f"The charge entering a terminal is {q} coulombs, with <i>t</i> in seconds. Find the current at <i>t</i> = {t0} s and the charge delivered in the first {t0} s."
    else:
        w = pick(r, [50, 100, 120])
        Qm = pick(r, [2, 5, 10])
        tt = pick(r, [1, 2, 5])  # ms
        th = w * tt * 1e-3
        iv = Qm * w * math.cos(th) * 1e-3
        txt = f"The charge at a terminal is <i>q</i>(<i>t</i>) = {Qm} sin({w}<i>t</i>) mC. Find the current at <i>t</i> = {tt} ms."
        steps = [step("Differentiate", f"<i>i</i> = d<i>q</i>/d<i>t</i> = {Qm} × {w} cos({w}<i>t</i>) mA = {Qm * w} cos({w}<i>t</i>) mA."),
                 step("Evaluate the angle in radians", f"{w} × {tt} × 10<sup>−3</sup> = {num(th)} rad; cos({num(th)}) = {num(math.cos(th))}."),
                 step("Current", f"<i>i</i> = {Qm * w} × {num(math.cos(th))} = {num(iv * 1000)} mA.")]
        ans = f"<i>i</i> = {eng(iv, 'A')}"
    return Problem(txt, steps, ans, level=3, topic="calculus")


def battery(r, tag):
    cap = pick(r, [2000, 2600, 3000, 4500, 5000, 10000])
    V = pick(r, [3.7, 7.4, 11.1, 12])
    load = pick(r, [0.15, 0.25, 0.4, 0.75, 1.5])  # A
    usable = pick(r, [0.8, 0.85, 0.9])
    hrs = cap / 1000 * usable / load
    Wh = cap / 1000 * V
    return Problem(
        f"A {V} V battery pack is rated at {cap} mAh. Only {int(usable * 100)} % of its rated capacity is usable before the cut-off voltage is reached. Estimate how long it can supply a steady {eng(load, 'A')}, and the total stored energy in watt-hours.",
        [step("Usable charge", f"{cap} mAh × {usable} = {num(cap * usable)} mAh = {num(cap * usable / 1000)} Ah."),
         step("Running time", f"<i>t</i> = capacity / current = {num(cap * usable / 1000)} / {num(load)} = {num(hrs, 3)} h."),
         step("Stored energy", f"<i>W</i> = <i>V</i> × Ah = {V} × {num(cap / 1000)} = {num(Wh, 3)} Wh (rated), or {num(Wh * 3600, 3)} J."),
         step("Caution", "Real capacity falls at high discharge rates and low temperatures, so treat this as an upper estimate.")],
        f"about {num(hrs, 3)} h; {num(Wh, 3)} Wh rated", level=2, topic="battery")


def problems():
    plan = [(charge_time, 6), (electrons, 5), (current_from_charge, 5), (ohm_I, 6), (ohm_R, 5), (ohm_V, 5),
            (power_forms, 6), (energy_cost, 6), (resistivity, 5), (tempco, 5), (efficiency, 5), (q_of_t, 4), (battery, 4)]
    return build(1, plan, 101)
