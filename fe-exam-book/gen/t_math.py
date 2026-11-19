"""Mathematics, probability & statistics, engineering economics templates."""
import math
from math import comb
from qcore import *

# =============================================================== MATHEMATICS


@tpl("math")
def quad_roots(rng):
    nz = [i for i in range(-9, 10) if i != 0]
    while True:
        p, q = rng.sample(nz, 2)
        if p + q != 0:
            break
    a = rng.choice([1, 2, 3])
    b, c = -a * (p + q), a * p * q
    hi, lo = max(p, q), min(p, q)
    eq = poly([(a, "x^2"), (b, "x"), (c, "")])
    D = b * b - 4 * a * c
    stem = f"What is the larger root of the equation ${eq} = 0$?"
    sol = (f"Use the quadratic formula with $a = {a}$, $b = {b}$, $c = {c}$. The discriminant is "
           f"$b^2 - 4ac = {b*b} - ({4*a*c}) = {D}$, so $\\sqrt{{D}} = {int(math.isqrt(D))}$.\n\n"
           f"$$x = {frac('-b \\pm \\sqrt{b^2-4ac}', '2a')} = {frac(f'{-b} \\pm {int(math.isqrt(D))}', 2*a)}$$\n\n"
           f"The two roots are ${hi}$ and ${lo}$, so the larger root is **{hi}**. A quick check: substituting "
           f"$x = {hi}$ makes the left-hand side zero. The commonest slip is reversing the sign of $-b$, which "
           f"produces the negated roots offered among the distractors.")
    return make(stem, num_mcq(rng, hi, [-lo, -hi, p + q, p * q], str, integer=True, positive=False), sol)


@tpl("math")
def log_solve(rng):
    V0 = rng.choice([10, 12, 15, 20, 24, 48])
    frac_left = rng.choice([0.5, 0.4, 0.25, 0.2, 0.1, 0.3])
    tau = rng.choice([2, 4, 5, 8, 10, 20, 50])
    Vt = V0 * frac_left
    t = tau * math.log(1 / frac_left)
    stem = (f"A capacitor voltage decays as $v(t) = {V0}\\,e^{{-t/{tau}}}$ V, with $t$ in milliseconds. "
            f"At what time does the voltage fall to {fnum(Vt)} V?")
    sol = (f"Set $v(t) = {mnum(Vt)}$ and take natural logarithms:\n\n"
           f"$${mnum(Vt)} = {V0}e^{{-t/{tau}}} \\;\\Rightarrow\\; t = {tau}\\ln\\left({frac(V0, mnum(Vt))}\\right) = {tau}\\ln({mnum(1/frac_left)}) = {mnum(t)}\\ \\text{{ms}}$$\n\n"
           f"Note that $\\ln$, not $\\log_{{10}}$, undoes the exponential; using $\\log_{{10}}$ gives {fnum(tau*math.log10(1/frac_left))} ms, a classic distractor.")
    wr = [tau * math.log10(1 / frac_left), tau * frac_left, tau * (1 - frac_left) * 2, tau / frac_left / 2]
    return make(stem, num_mcq(rng, t, wr, lambda v: fu(v, "ms")), sol)


@tpl("math")
def derivative_eval(rng):
    a, b, c, d = rng.choice([1, 2, 3, -2]), rng.randint(-5, 5), rng.randint(-8, 8), rng.randint(-9, 9)
    x0 = rng.choice([-2, -1, 1, 2, 3])
    f = poly([(a, "x^3"), (b, "x^2"), (c, "x"), (d, "")])
    fp = 3 * a * x0 ** 2 + 2 * b * x0 + c
    fval = a * x0 ** 3 + b * x0 ** 2 + c * x0 + d
    fpp = 6 * a * x0 + 2 * b
    naive = a * x0 ** 2 + b * x0 + c
    stem = f"Given $f(x) = {f}$, what is the value of $f'(x)$ at $x = {x0}$?"
    sol = (f"Differentiate term by term using $\\frac{{d}}{{dx}}x^n = nx^{{n-1}}$:\n\n"
           f"$$f'(x) = {poly([(3*a,'x^2'),(2*b,'x'),(c,'')])}$$\n\n"
           f"Substituting $x = {x0}$: $f'({x0}) = {3*a}({x0})^2 + ({2*b})({x0}) + ({c}) = {fp}$.\n\n"
           f"Watch out for evaluating $f({x0}) = {fval}$ instead of the derivative, or forgetting to bring the power down as a multiplier.")
    return make(stem, num_mcq(rng, fp, [fval, fpp, naive], str, integer=True, positive=False), sol)


@tpl("math")
def definite_integral(rng):
    a, b = rng.choice([3, 6, 9, 12]), rng.choice([2, 4, 6, 8, 10])
    T = rng.choice([1, 2, 3, 4])
    val = a * T ** 3 / 3 + b * T ** 2 / 2
    stem = (f"The current into a capacitor is $i(t) = {a}t^2 + {b}t$ A. What total charge, in coulombs, enters the "
            f"capacitor between $t = 0$ and $t = {T}$ s?")
    sol = (f"Charge is the time integral of current, $q = \\int i\\,dt$:\n\n"
           f"$$q = \\int_0^{{{T}}}({a}t^2 + {b}t)\\,dt = \\left[{frac(a,3)}t^3 + {frac(b,2)}t^2\\right]_0^{{{T}}} = {mnum(a*T**3/3)} + {mnum(b*T**2/2)} = {mnum(val)}\\ \\text{{C}}$$\n\n"
           "A frequent error is forgetting to divide by the new power after integrating.")
    wr = [a * T ** 3 + b * T ** 2, 2 * a * T + b, a * T ** 2 + b * T, a * T ** 3 / 3]
    return make(stem, num_mcq(rng, val, wr, lambda v: fu(v, "C")), sol)


@tpl("math")
def rms_offset(rng):
    V0 = rng.choice([2, 3, 4, 5, 6, 8, 10])
    Vm = rng.choice([4, 6, 8, 10, 12, 15, 20])
    rms = math.sqrt(V0 ** 2 + Vm ** 2 / 2)
    stem = (f"A voltage waveform is $v(t) = {V0} + {Vm}\\sin(\\omega t)$ V. What is its RMS value?")
    sol = (f"For a DC component plus a sinusoid, the RMS values combine in quadrature because the cross-term averages to zero over a period:\n\n"
           f"$$V_{{\\text{{rms}}}} = \\sqrt{{V_0^2 + \\left({frac('V_m', '\\sqrt{2}')}\\right)^2}} = \\sqrt{{{V0}^2 + {frac(f'{Vm}^2','2')}}} = {mnum(rms)}\\ \\text{{V}}$$\n\n"
           f"Simply adding $V_0 + V_m/\\sqrt{{2}} = {mnum(V0+Vm/math.sqrt(2))}$ V is wrong: RMS values add only in quadrature for components at different frequencies.")
    wr = [V0 + Vm / math.sqrt(2), math.sqrt(V0 ** 2 + Vm ** 2), Vm / math.sqrt(2), (V0 + Vm) / math.sqrt(2)]
    return make(stem, num_mcq(rng, rms, wr, lambda v: fu(v, "V")), sol)


@tpl("math")
def complex_polar(rng):
    trip = rng.choice([(3, 4), (5, 12), (8, 6), (6, 8), (7, 24), (9, 12), (12, 5), (2, 2), (1, 3)])
    a, b = trip
    sa, sb = rng.choice([(1, 1), (-1, 1), (-1, -1), (1, -1)])
    a, b = sa * a, sb * b
    M = math.hypot(a, b)
    th = math.degrees(math.atan2(b, a))
    naive = math.degrees(math.atan(b / a))
    def P(m, t):
        return f"${mnum(m)}\\angle {mnum(t,4)}^\\circ$"
    corr = P(M, th)
    wr = [P(M, naive), P(abs(a) + abs(b), th), P(M, 90 - th if abs(90 - th) != abs(th) else th + 90), P(M, -th)]
    wr = [w for w in wr if w != corr]
    sgn = "+" if b > 0 else "-"
    stem = f"Express the complex number $z = {a} {sgn} j{abs(b)}$ in polar form."
    quad = {(1, 1): "first", (-1, 1): "second", (-1, -1): "third", (1, -1): "fourth"}[(sa, sb)]
    sol = (f"Magnitude: $|z| = \\sqrt{{({a})^2 + ({b})^2}} = {mnum(M)}$.\n\n"
           f"The point lies in the {quad} quadrant, so the angle must be taken with quadrant awareness (the calculator's two-argument or polar function does this automatically):\n\n"
           f"$$\\theta = \\operatorname{{atan2}}({b}, {a}) = {mnum(th,4)}^\\circ$$\n\n"
           f"Pressing $\\tan^{{-1}}(b/a)$ alone returns ${mnum(naive,4)}^\\circ$, which is only correct in the first and fourth quadrants. "
           "On the exam, always sketch the point before trusting the angle.")
    return make(stem, str_mcq(rng, corr, wr), sol)


@tpl("math")
def complex_divide(rng):
    A, B = rng.choice([10, 20, 50, 100, 120, 240]), rng.choice([2, 4, 5, 8, 10, 25])
    al, be = rng.choice([0, 30, 45, 60, -30, 90]), rng.choice([-60, -45, -30, 15, 20, 36.87, 53.13])
    def P(m, t):
        return f"${mnum(m)}\\angle {mnum(t,4)}^\\circ$"
    corr = P(A / B, al - be)
    wr = [P(A / B, al + be), P(A * B, al - be), P(B / A, al - be), P(A / B, be - al)]
    stem = (f"A voltage phasor $\\mathbf{{V}} = {A}\\angle {mnum(al,4)}^\\circ$ V is applied across an impedance "
            f"$\\mathbf{{Z}} = {B}\\angle {mnum(be,4)}^\\circ\\ \\Omega$. What is the current phasor $\\mathbf{{I}}$?")
    sol = (f"Ohm's law in phasor form, $\\mathbf{{I}} = \\mathbf{{V}}/\\mathbf{{Z}}$. In polar form, divide magnitudes and subtract angles:\n\n"
           f"$$\\mathbf{{I}} = {frac(A,B)}\\angle({mnum(al,4)}^\\circ - ({mnum(be,4)}^\\circ)) = {mnum(A/B)}\\angle {mnum(al-be,4)}^\\circ\\ \\text{{A}}$$\n\n"
           "Adding the angles (correct for multiplication) is the usual mistake.")
    return make(stem, str_mcq(rng, corr, wr), sol)


@tpl("math")
def det3(rng):
    while True:
        m = [[rng.randint(-4, 5) for _ in range(3)] for _ in range(3)]
        (a, b, c), (d, e, f), (g, h, i) = m
        det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
        bad = a * (e * i - f * h) + b * (d * i - f * g) + c * (d * h - e * g)
        diag = a * e * i + b * f * g + c * d * h
        if det != 0 and bad != det and abs(det) < 200:
            break
    mat = "\\begin{bmatrix} " + " \\\\ ".join(" & ".join(str(x) for x in row) for row in m) + " \\end{bmatrix}"
    stem = f"What is the determinant of the matrix $\\mathbf{{A}} = {mat}$?"
    sol = (f"Expand along the first row, remembering the alternating sign pattern $+,-,+$:\n\n"
           f"$$\\det \\mathbf{{A}} = {a}({e}\\cdot{i} - {f}\\cdot{h}) - ({b})({d}\\cdot{i} - {f}\\cdot{g}) + ({c})({d}\\cdot{h} - {e}\\cdot{g})$$\n\n"
           f"$$= {a}({e*i-f*h}) - ({b})({d*i-f*g}) + ({c})({d*h-e*g}) = {det}$$\n\n"
           f"Dropping the minus sign on the middle cofactor gives {bad}, which is why that value appears among the options. Most approved calculators "
           "will evaluate a $3\\times3$ determinant directly; use that as a check, not a substitute for understanding.")
    return make(stem, num_mcq(rng, det, [bad, diag, -det], str, integer=True, positive=False), sol)


@tpl("math")
def cramer2(rng):
    while True:
        x, y = rng.randint(-4, 6), rng.randint(-4, 6)
        a, b, c, d = rng.randint(2, 9), rng.randint(-5, 5), rng.randint(-5, 5), rng.randint(2, 9)
        D = a * d - b * c
        if D != 0 and x != 0 and x != y and b != 0 and c != 0:
            break
    e, f = a * x + b * y, c * x + d * y
    stem = (f"Two mesh currents satisfy ${poly([(a,'I_1'),(b,'I_2')])} = {e}$ and ${poly([(c,'I_1'),(d,'I_2')])} = {f}$ "
            "(currents in amperes). What is $I_1$?")
    sol = (f"By Cramer's rule, $\\Delta = ({a})({d}) - ({b})({c}) = {D}$ and\n\n"
           f"$$I_1 = {frac(f'({e})({d}) - ({b})({f})', D)} = {frac(e*d-b*f, D)} = {x}\\ \\text{{A}}$$\n\n"
           f"Substituting back gives $I_2 = {y}$ A, which satisfies both equations—always worth the ten-second check.")
    wr = [y, -x, (e * d + b * f) / D, D]
    return make(stem, num_mcq(rng, x, wr, lambda v: fu(v, "A", 3), positive=False), sol)


@tpl("math")
def vector_angle(rng):
    while True:
        A = [rng.randint(-4, 5) for _ in range(3)]
        B = [rng.randint(-4, 5) for _ in range(3)]
        na, nb = math.sqrt(sum(x * x for x in A)), math.sqrt(sum(x * x for x in B))
        if na == 0 or nb == 0:
            continue
        dot = sum(x * y for x, y in zip(A, B))
        th = math.degrees(math.acos(dot / (na * nb)))
        if 15 < th < 165 and abs(th - 90) > 5:
            break
    vec = lambda v: f"{v[0]}\\mathbf{{i}} {'+' if v[1]>=0 else '-'} {abs(v[1])}\\mathbf{{j}} {'+' if v[2]>=0 else '-'} {abs(v[2])}\\mathbf{{k}}"
    stem = f"What is the angle between the vectors $\\mathbf{{A}} = {vec(A)}$ and $\\mathbf{{B}} = {vec(B)}$?"
    sol = (f"Use $\\cos\\theta = \\dfrac{{\\mathbf{{A}}\\cdot\\mathbf{{B}}}}{{|\\mathbf{{A}}||\\mathbf{{B}}|}}$. "
           f"Here $\\mathbf{{A}}\\cdot\\mathbf{{B}} = {dot}$, $|\\mathbf{{A}}| = {mnum(na,4)}$ and $|\\mathbf{{B}}| = {mnum(nb,4)}$.\n\n"
           f"$$\\theta = \\cos^{{-1}}\\left({frac(dot, mnum(na*nb,4))}\\right) = {mnum(th)}^\\circ$$\n\n"
           "A negative dot product means the angle is obtuse; candidates who drop the sign get the supplement.")
    wr = [180 - th, 90 - th if th < 90 else th - 90, math.degrees(math.acos(max(-1, min(1, dot / (na * na))))) if abs(dot / (na * na)) <= 1 else th * 1.3]
    return make(stem, num_mcq(rng, th, wr, lambda v: fu(v, "°") .replace(NBSP + "°", "°")), sol)


@tpl("math")
def cross_mag(rng):
    while True:
        A = [rng.randint(-3, 4) for _ in range(3)]
        B = [rng.randint(-3, 4) for _ in range(3)]
        C = [A[1] * B[2] - A[2] * B[1], A[2] * B[0] - A[0] * B[2], A[0] * B[1] - A[1] * B[0]]
        mag = math.sqrt(sum(x * x for x in C))
        if mag > 0:
            break
    dot = sum(x * y for x, y in zip(A, B))
    vec = lambda v: f"({v[0]}, {v[1]}, {v[2]})"
    stem = (f"A force $\\mathbf{{F}} = {vec(B)}$ N acts at position $\\mathbf{{r}} = {vec(A)}$ m from a pivot. "
            "What is the magnitude of the moment $\\mathbf{r}\\times\\mathbf{F}$?")
    sol = (f"Compute the cross product by the determinant rule:\n\n"
           f"$$\\mathbf{{r}}\\times\\mathbf{{F}} = ({C[0]})\\mathbf{{i}} + ({C[1]})\\mathbf{{j}} + ({C[2]})\\mathbf{{k}}$$\n\n"
           f"$$|\\mathbf{{r}}\\times\\mathbf{{F}}| = \\sqrt{{{C[0]}^2 + {C[1]}^2 + {C[2]}^2}} = {mnum(mag)}\\ \\text{{N·m}}$$\n\n"
           f"The dot product ({dot}) is a scalar and measures alignment, not turning effect.")
    na, nb = math.sqrt(sum(x * x for x in A)), math.sqrt(sum(x * x for x in B))
    wr = [abs(dot), na * nb, abs(sum(C))]
    return make(stem, num_mcq(rng, mag, wr, lambda v: fu(v, "N·m")), sol)


@tpl("math")
def first_order_ode(rng):
    a = rng.choice([2, 4, 5, 10, 20])
    b = rng.choice([10, 20, 40, 50, 100])
    t = rng.choice([0.05, 0.1, 0.2, 0.25])
    y = b / a * (1 - math.exp(-a * t))
    stem = (f"The differential equation $\\dfrac{{dy}}{{dt}} + {a}y = {b}$ has initial condition $y(0) = 0$. "
            f"What is $y$ at $t = {mnum(t)}$ s?")
    sol = (f"For $y' + ay = b$ with $y(0)=0$ the solution is $y(t) = \\dfrac{{b}}{{a}}\\left(1 - e^{{-at}}\\right)$. "
           f"The steady-state value is $b/a = {mnum(b/a)}$ and the time constant is $1/a = {mnum(1/a)}$ s.\n\n"
           f"$$y({mnum(t)}) = {mnum(b/a)}\\left(1 - e^{{-{a}\\times{mnum(t)}}}\\right) = {mnum(y)}$$\n\n"
           "Recognising the standard first-order form saves you from solving it from scratch: the same shape describes RC and RL circuits.")
    wr = [b / a * math.exp(-a * t), b * (1 - math.exp(-a * t)), b / a * (1 - math.exp(-t / a)), b / a]
    return make(stem, num_mcq(rng, y, wr, lambda v: fnum(v)), sol)


@tpl("math")
def ode_damping(rng):
    kind = rng.choice(["over", "crit", "under", "under", "none"])
    if kind == "over":
        r1, r2 = rng.sample([1, 2, 3, 4, 5, 6], 2)
        b, c = r1 + r2, r1 * r2
    elif kind == "crit":
        r = rng.choice([2, 3, 4, 5, 6])
        b, c = 2 * r, r * r
    elif kind == "under":
        al, wd = rng.choice([1, 2, 3]), rng.choice([2, 3, 4, 5])
        b, c = 2 * al, al * al + wd * wd
    else:
        b, c = 0, rng.choice([4, 9, 16, 25])
    names = {"over": "Overdamped: two distinct real negative roots",
             "crit": "Critically damped: a repeated real root",
             "under": "Underdamped: complex-conjugate roots with negative real part",
             "none": "Undamped: purely imaginary roots, sustained oscillation"}
    corr = names[kind]
    wr = [v for k, v in names.items() if k != kind]
    D = b * b - 4 * c
    eqs = poly([(1, "\\ddot{y}"), (b, "\\dot{y}"), (c, "y")])
    stem = f"How would you describe the natural response of the system governed by ${eqs} = 0$?"
    sol = (f"The characteristic equation is $s^2 + {b}s + {c} = 0$, with discriminant $b^2 - 4c = {b*b} - {4*c} = {D}$.\n\n"
           "A positive discriminant gives two real roots (overdamped), zero gives a repeated root (critically damped), and a negative "
           "discriminant gives complex roots (underdamped, or undamped if the $\\dot{y}$ term is absent).\n\n"
           f"Equivalently, $\\omega_n = \\sqrt{{{c}}} = {mnum(math.sqrt(c))}$ rad/s and $\\zeta = {frac(b, '2\\omega_n')} = {mnum(b/(2*math.sqrt(c)))}$. Hence: **{corr.split(':')[0]}**.")
    return make(stem, str_mcq(rng, corr, wr), sol)


@tpl("math")
def newton_raphson(rng):
    k = rng.choice([2, 3, 5, 7, 10, 20, 30])
    x0 = rng.choice([1, 2, 3])
    f0 = x0 ** 3 - k
    fp = 3 * x0 ** 2
    x1 = x0 - f0 / fp
    stem = (f"Newton's method is used to find a root of $f(x) = x^3 - {k}$ starting from $x_0 = {x0}$. "
            "What is $x_1$ after one iteration?")
    sol = (f"Newton's iteration is $x_{{n+1}} = x_n - \\dfrac{{f(x_n)}}{{f'(x_n)}}$ with $f'(x) = 3x^2$.\n\n"
           f"$$x_1 = {x0} - {frac(f0, fp)} = {mnum(x1,4)}$$\n\n"
           f"The true root is $\\sqrt[3]{{{k}}} = {mnum(k**(1/3),4)}$; one step already moves you most of the way there, which is why the method appears so often.")
    wr = [x0 + f0 / fp, x0 - fp / f0 if f0 != 0 else 9, k ** (1 / 3)]
    return make(stem, num_mcq(rng, x1, wr, lambda v: fnum(v, 4), positive=False), sol)


@tpl("math")
def trapezoid(rng):
    c = rng.choice([1, 2, 3, 4])
    h = 0.5
    xs = [0, 0.5, 1.0, 1.5, 2.0]
    fs = [x * x + c for x in xs]
    T = h / 2 * (fs[0] + 2 * sum(fs[1:-1]) + fs[-1])
    exact = 8 / 3 + 2 * c
    left = h * sum(fs[:-1])
    stem = (f"Using the trapezoidal rule with step $h = 0.5$, estimate $\\displaystyle\\int_0^2 (x^2 + {c})\\,dx$.")
    sol = (f"Tabulate $f(x)$ at $x = 0, 0.5, 1, 1.5, 2$: ${', '.join(mnum(v,4) for v in fs)}$.\n\n"
           f"$$T = \\frac{{h}}{{2}}\\left[f_0 + 2(f_1+f_2+f_3) + f_4\\right] = 0.25\\left[{mnum(fs[0],4)} + 2({mnum(sum(fs[1:-1]),4)}) + {mnum(fs[-1],4)}\\right] = {mnum(T,4)}$$\n\n"
           f"The exact value is ${mnum(exact,4)}$; the trapezoidal rule slightly over-estimates a function that curves upwards.")
    return make(stem, num_mcq(rng, T, [exact, left, h * sum(fs)], lambda v: fnum(v, 4)), sol)


@tpl("math")
def lhopital(rng):
    a, b = rng.sample([2, 3, 4, 5, 6, 8], 2)
    kind = rng.choice(["sin", "exp", "cos"])
    if kind == "sin":
        expr, val = f"\\dfrac{{\\sin({a}x)}}{{{b}x}}", a / b
        how = f"Differentiate top and bottom: $\\dfrac{{{a}\\cos({a}x)}}{{{b}}} \\to {frac(a,b)}$ as $x\\to0$."
    elif kind == "exp":
        expr, val = f"\\dfrac{{e^{{{a}x}} - 1}}{{{b}x}}", a / b
        how = f"Differentiate top and bottom: $\\dfrac{{{a}e^{{{a}x}}}}{{{b}}} \\to {frac(a,b)}$ as $x\\to0$."
    else:
        expr, val = f"\\dfrac{{1 - \\cos({a}x)}}{{{b}x^2}}", a * a / (2 * b)
        how = (f"Apply the rule twice: $\\dfrac{{{a}\\sin({a}x)}}{{{2*b}x}} \\to \\dfrac{{{a*a}\\cos({a}x)}}{{{2*b}}} \\to {frac(a*a, 2*b)}$.")
    stem = f"Evaluate $\\displaystyle\\lim_{{x\\to 0}} {expr}$."
    sol = (f"Direct substitution gives the indeterminate form $0/0$, so L'Hôpital's rule applies. {how}\n\n"
           f"The limit is **{fnum(val)}**.")
    wr = [b / a, 1.0, a * a / b, 0.5 * a / b]
    return make(stem, num_mcq(rng, val, wr, lambda v: fnum(v)), sol)


@tpl("math")
def eigen2(rng):
    for _ in range(500):
        l1, l2 = rng.sample([-4, -3, -2, -1, 1, 2, 3, 4, 5, 6], 2)
        T, D = l1 + l2, l1 * l2
        a = rng.randint(-3, 6)
        d = T - a
        prod = a * d - D
        if prod == 0:
            continue
        divs = [x for x in range(-6, 7) if x != 0 and prod % x == 0 and abs(prod // x) <= 9]
        if not divs:
            continue
        b = rng.choice(divs)
        c = prod // b
        if {a, d} == {l1, l2}:
            continue
        break
    mat = f"\\begin{{bmatrix}} {a} & {b} \\\\ {c} & {d} \\end{{bmatrix}}"
    lo, hi = sorted([l1, l2])
    corr = f"${lo}$ and ${hi}$"
    wr = [f"${min(a,d)}$ and ${max(a,d)}$", f"${-hi}$ and ${-lo}$", f"${min(T,D)}$ and ${max(T,D)}$" if T != D else f"${lo}$ and ${hi+1}$"]
    wr += [f"${lo-1}$ and ${hi+1}$", f"${lo+1}$ and ${hi+2}$", f"${lo}$ and ${-hi}$" if hi != 0 else f"${lo}$ and $3$"]
    uniq = []
    for w in wr:
        if w != corr and w not in uniq:
            uniq.append(w)
    wr = uniq[:3]
    stem = f"What are the eigenvalues of $\\mathbf{{A}} = {mat}$?"
    sol = (f"Solve $\\det(\\mathbf{{A}} - \\lambda\\mathbf{{I}}) = 0$:\n\n"
           f"$$({a}-\\lambda)({d}-\\lambda) - ({b})({c}) = \\lambda^2 - ({T})\\lambda + ({D}) = 0$$\n\n"
           f"which factors as $(\\lambda - ({l1}))(\\lambda - ({l2})) = 0$. A useful check: the eigenvalues sum to the trace ({T}) and multiply to the determinant ({D}). "
           "The diagonal entries are the eigenvalues only for triangular matrices.")
    return make(stem, str_mcq(rng, corr, wr), sol)


@tpl("math")
def partial_deriv(rng):
    a, b = rng.choice([2, 3, 4, 5]), rng.choice([1, 2, 3, -1, -2])
    x0, y0 = rng.choice([1, 2, -1, 3]), rng.choice([1, 2, -2, 3])
    fy = a * x0 ** 2 + 3 * b * y0 ** 2
    fx = 2 * a * x0 * y0
    fv = a * x0 ** 2 * y0 + b * y0 ** 3
    stem = f"For $f(x,y) = {a}x^2y {'+' if b>0 else '-'} {abs(b)}y^3$, what is $\\partial f/\\partial y$ at $(x,y) = ({x0}, {y0})$?"
    sol = (f"Treat $x$ as a constant when differentiating with respect to $y$:\n\n"
           f"$$\\frac{{\\partial f}}{{\\partial y}} = {a}x^2 + {3*b}y^2 \\;\\Rightarrow\\; {a}({x0})^2 + {3*b}({y0})^2 = {fy}$$\n\n"
           f"$\\partial f/\\partial x = {fx}$ at the same point is a common mix-up.")
    return make(stem, num_mcq(rng, fy, [fx, fv, a * x0 ** 2 + b * y0 ** 2], str, integer=True, positive=False), sol)


@tpl("math")
def line_intercept(rng):
    while True:
        x1, y1, x2, y2 = rng.randint(-5, 5), rng.randint(-6, 8), rng.randint(-5, 6), rng.randint(-6, 9)
        if x2 != x1 and (y2 - y1) != 0:
            m = (y2 - y1) / (x2 - x1)
            c = y1 - m * x1
            if abs(c - m) > 0.01 and abs(c) > 0.01:
                break
    stem = f"A straight line passes through the points $({x1}, {y1})$ and $({x2}, {y2})$. Where does it cross the $y$-axis?"
    sol = (f"Slope $m = \\dfrac{{{y2} - ({y1})}}{{{x2} - ({x1})}} = {mnum(m,4)}$. Then $c = y_1 - m x_1 = {y1} - ({mnum(m,4)})({x1}) = {mnum(c,4)}$.\n\n"
           f"So $y = {mnum(m,4)}x {'+' if c>=0 else '-'} {mnum(abs(c),4)}$, which crosses the $y$-axis at $y = {mnum(c,4)}$. "
           "Do not confuse the intercept with the slope or with the $x$-intercept $-c/m$.")
    wr = [m, -c, -c / m, y1 + m * x1]
    return make(stem, num_mcq(rng, c, wr, lambda v: "y = " + fnum(v, 3), positive=False), sol)


# =============================================================== PROBABILITY


@tpl("prob")
def sample_sd(rng):
    data = [rng.randint(10, 30) for _ in range(6)]
    n = len(data)
    mean = sum(data) / n
    ss = sum((x - mean) ** 2 for x in data)
    s = math.sqrt(ss / (n - 1))
    pop = math.sqrt(ss / n)
    stem = (f"Six resistors from a batch measure {', '.join(str(d) for d in data)} Ω above their nominal value. "
            "What is the sample standard deviation of these deviations?")
    sol = (f"The sample mean is $\\bar{{x}} = {mnum(mean,4)}$ Ω. The sum of squared deviations is ${mnum(ss,4)}$ Ω².\n\n"
           f"$$s = \\sqrt{{{frac('\\sum (x_i - \\bar{x})^2', 'n - 1')}}} = \\sqrt{{{frac(mnum(ss,4), n-1)}}} = {mnum(s)}\\ \\Omega$$\n\n"
           f"Dividing by $n$ instead of $n-1$ gives the population value ({fnum(pop)} Ω). The Reference Handbook gives both; the word *sample* tells you which one to use.")
    return make(stem, num_mcq(rng, s, [pop, ss / (n - 1), sum(abs(x - mean) for x in data) / n], lambda v: fu(v, "Ω")), sol)


@tpl("prob")
def binomial(rng):
    n = rng.choice([5, 6, 8, 10, 12])
    p = rng.choice([0.05, 0.1, 0.15, 0.2])
    k = rng.choice([1, 2])
    P = comb(n, k) * p ** k * (1 - p) ** (n - k)
    stem = (f"Each chip from a production line is defective with probability {fnum(p)}, independently. "
            f"In a sample of {n} chips, what is the probability that exactly {k} {'is' if k==1 else 'are'} defective?")
    sol = (f"This is a binomial experiment with $n = {n}$, $p = {fnum(p)}$:\n\n"
           f"$$P(X = {k}) = \\binom{{{n}}}{{{k}}}p^{k}(1-p)^{{{n-k}}} = {comb(n,k)}({fnum(p)})^{k}({mnum(1-p)})^{{{n-k}}} = {mnum(P)}$$\n\n"
           "Leaving out the $(1-p)^{n-k}$ factor ignores the requirement that the other chips are good.")
    cum = sum(comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k + 1))
    wr = [comb(n, k) * p ** k, p ** k * (1 - p) ** (n - k), cum, 1 - cum]
    return make(stem, num_mcq(rng, P, wr, lambda v: fnum(v, 3)), sol)


@tpl("prob")
def poisson(rng):
    lam = rng.choice([1.5, 2, 2.5, 3, 4])
    k = rng.choice([0, 1, 2, 3])
    P = lam ** k * math.exp(-lam) / math.factorial(k)
    stem = (f"Packets arrive at a router at an average rate of {fnum(lam)} per millisecond (Poisson process). "
            f"What is the probability that exactly {k} packet{'s' if k!=1 else ''} arrive in a given millisecond?")
    sol = (f"$$P(X = {k}) = {frac(f'\\lambda^{k} e^{{-\\lambda}}', f'{k}!')} = {frac(f'{mnum(lam)}^{k} e^{{-{mnum(lam)}}}', math.factorial(k))} = {mnum(P)}$$\n\n"
           "The factorial in the denominator is easy to forget when $k \\ge 2$.")
    wr = [lam ** k * math.exp(-lam), 1 - P, math.exp(-lam) if k else lam * math.exp(-lam), lam ** k * math.exp(-lam) / (k + 1)]
    return make(stem, num_mcq(rng, P, wr, lambda v: fnum(v, 3)), sol)


def Phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


@tpl("prob")
def normal_tail(rng):
    mu = rng.choice([100, 50, 220, 1000, 5])
    sigma = {100: 2, 50: 1.5, 220: 4, 1000: 20, 5: 0.1}[mu]
    z = rng.choice([1.0, 1.5, 2.0, 1.2, 0.8, 2.5])
    x = mu + z * sigma
    P = 1 - Phi(z)
    unit = {100: "Ω", 50: "Ω", 220: "V", 1000: "Ω", 5: "V"}[mu]
    stem = (f"A quantity is normally distributed with mean {fnum(mu,4)} {unit} and standard deviation {fnum(sigma)} {unit}. "
            f"What fraction of units exceed {fnum(x,4)} {unit}?")
    sol = (f"Standardise: $z = \\dfrac{{x - \\mu}}{{\\sigma}} = \\dfrac{{{mnum(x,4)} - {mnum(mu,4)}}}{{{mnum(sigma)}}} = {mnum(z)}$.\n\n"
           f"From the unit normal table, $F({mnum(z)}) = {mnum(Phi(z),4)}$, so the upper tail is $R(z) = 1 - F(z) = {mnum(P)}$.\n\n"
           "Read the table heading carefully: the Handbook tabulates $F(x)$, $R(x)$ and two-tailed values side by side, and picking the wrong column is the main source of error.")
    wr = [Phi(z), 2 * P, 1 - Phi((x - mu) / sigma ** 2) if sigma != 1 else P * 1.5, 0.5 - P]
    return make(stem, num_mcq(rng, P, wr, lambda v: fnum(v, 3)), sol)


@tpl("prob")
def combos(rng):
    n, k = rng.choice([(8, 3), (10, 4), (12, 3), (9, 2), (7, 3), (15, 2), (10, 3)])
    C = comb(n, k)
    Pm = math.perm(n, k)
    stem = (f"A design review panel of {k} engineers is chosen from a team of {n}. How many different panels are possible?")
    sol = (f"Order does not matter in a panel, so count combinations:\n\n$$\\binom{{{n}}}{{{k}}} = {frac(f'{n}!', f'{k}!\\,{n-k}!')} = {C}$$\n\n"
           f"Permutations (${Pm}$) would count the same people in different orders as different panels.")
    return make(stem, num_mcq(rng, C, [Pm, comb(n, k - 1), n * k], lambda v: fnum(v, 4), integer=True), sol)


@tpl("prob")
def bayes(rng):
    prev = rng.choice([0.01, 0.02, 0.05])
    sens = rng.choice([0.95, 0.98, 0.9])
    fpr = rng.choice([0.02, 0.05, 0.03])
    pos = sens * prev + fpr * (1 - prev)
    post = sens * prev / pos
    stem = (f"{fnum(prev*100)}% of boards from a supplier carry a latent fault. An automated test flags {fnum(sens*100)}% of faulty boards "
            f"but also flags {fnum(fpr*100)}% of good boards. If a board is flagged, what is the probability that it is actually faulty?")
    sol = (f"Apply Bayes' theorem. The total probability of a flag is\n\n$$P(+) = ({fnum(sens)})({fnum(prev)}) + ({fnum(fpr)})({mnum(1-prev)}) = {mnum(pos,4)}$$\n\n"
           f"$$P(\\text{{fault}}\\mid +) = {frac(f'({fnum(sens)})({fnum(prev)})', mnum(pos,4))} = {mnum(post)}$$\n\n"
           "When the fault is rare, most flags are false alarms. Quoting the test's detection rate as the answer is the classic base-rate error.")
    return make(stem, num_mcq(rng, post, [sens, pos, sens * prev, 1 - fpr], lambda v: fnum(v, 3)), sol)


@tpl("prob")
def expected_value(rng):
    vals = sorted(rng.sample([0, 500, 1000, 2000, 5000, 10000, 20000], 4))
    while True:
        ps = [rng.choice([0.1, 0.2, 0.3, 0.4, 0.5]) for _ in range(3)]
        if sum(ps) < 0.95:
            break
    ps.append(round(1 - sum(ps), 2))
    EV = sum(v * p for v, p in zip(vals, ps))
    rows = "; ".join(f"\\${v:,} with probability {fnum(p)}" for v, p in zip(vals, ps))
    stem = f"The annual repair cost of a substation transformer is estimated as: {rows}. What is the expected annual repair cost?"
    sol = (f"$$E[C] = \\sum c_i p_i = " + " + ".join(f"({v})({p})" for v, p in zip(vals, ps)) + f" = {mnum(EV,4)}$$\n\n"
           f"The expected cost is \\${EV:,.0f}. A simple average of the outcomes (\\${sum(vals)/4:,.0f}) ignores how likely each one is.")
    wr = [sum(vals) / 4, vals[ps.index(max(ps))], max(vals) * max(ps)]
    return make(stem, num_mcq(rng, EV, wr, lambda v: "\\$" + f"{v:,.0f}"), sol)


@tpl("prob")
def reliability(rng):
    R1 = rng.choice([0.9, 0.85, 0.8, 0.95])
    R2 = rng.choice([0.98, 0.95, 0.99, 0.97])
    sysR = (1 - (1 - R1) ** 2) * R2
    stem = (f"A system consists of two identical pumps in parallel (each with reliability {fnum(R1)}), followed in series by a controller "
            f"with reliability {fnum(R2)}. The system works if at least one pump and the controller work. What is the system reliability?")
    sol = (f"Parallel block: $R_p = 1 - (1 - {fnum(R1)})^2 = {mnum(1-(1-R1)**2,4)}$. Series with the controller:\n\n"
           f"$$R_{{sys}} = R_p R_c = {mnum(1-(1-R1)**2,4)}\\times{fnum(R2)} = {mnum(sysR,4)}$$\n\n"
           "Redundancy lifts the weaker stage; the series controller now limits the system.")
    wr = [R1 * R1 * R2, R1 * R2, 1 - (1 - R1) ** 2 * (1 - R2), 2 * R1 * R2 / 2 * 0.9]
    return make(stem, num_mcq(rng, sysR, wr, lambda v: fnum(v, 4)), sol)


@tpl("prob")
def exp_reliability(rng):
    mtbf = rng.choice([5000, 10000, 20000, 50000])
    t = rng.choice([1000, 2000, 5000, 8760])
    lam = 1 / mtbf
    Rt = math.exp(-lam * t)
    stem = (f"A power supply has a constant failure rate and a mean time between failures of {mtbf:,} h. "
            f"What is the probability that it operates without failure for {t:,} h?")
    sol = (f"With a constant failure rate, $\\lambda = 1/\\text{{MTBF}} = {mnum(lam)}$ per hour and $R(t) = e^{{-\\lambda t}}$:\n\n"
           f"$$R({t}) = e^{{-{t}/{mtbf}}} = {mnum(Rt)}$$\n\n"
           "$1 - e^{-\\lambda t}$ is the probability of failure, not survival.")
    return make(stem, num_mcq(rng, Rt, [1 - Rt, 1 - lam * t if lam * t < 1 else 0.3, lam * t], lambda v: fnum(v, 3)), sol)


@tpl("prob")
def conf_interval(rng):
    n = rng.choice([16, 25, 36, 49, 64, 100])
    xbar = rng.choice([4.98, 5.02, 12.1, 3.31, 49.8])
    sigma = rng.choice([0.2, 0.3, 0.4, 0.6])
    lvl, z = rng.choice([(95, 1.96), (90, 1.645), (99, 2.576)])
    upper = xbar + z * sigma / math.sqrt(n)
    stem = (f"A sample of {n} measurements of a reference voltage has mean {fnum(xbar,4)} V. The population standard deviation is known to be "
            f"{fnum(sigma)} V. What is the upper limit of the two-sided {lvl}% confidence interval for the true mean?")
    sol = (f"With $\\sigma$ known, $\\bar{{x}} \\pm z_{{\\alpha/2}}\\sigma/\\sqrt{{n}}$, and $z_{{\\alpha/2}} = {z}$ for {lvl}%.\n\n"
           f"$$\\text{{upper}} = {mnum(xbar,4)} + {z}\\times{frac(mnum(sigma), sq(n))} = {mnum(upper,4)}\\ \\text{{V}}$$\n\n"
           "Forgetting the $\\sqrt{n}$ makes the interval far too wide.")
    wr = [xbar + z * sigma, xbar + z * sigma / n, xbar + 1.645 * sigma / math.sqrt(n) if z != 1.645 else xbar + 1.96 * sigma / math.sqrt(n)]
    return make(stem, num_mcq(rng, upper, wr, lambda v: fu(v, "V", 4)), sol)


@tpl("prob")
def union_prob(rng):
    pa, pb = rng.choice([0.1, 0.2, 0.05, 0.15]), rng.choice([0.1, 0.3, 0.25, 0.08])
    P = pa + pb - pa * pb
    stem = (f"Two independent protection relays fail to operate with probabilities {fnum(pa)} and {fnum(pb)}. "
            "What is the probability that at least one of them fails?")
    sol = (f"For independent events, $P(A\\cup B) = P(A) + P(B) - P(A)P(B) = {fnum(pa)} + {fnum(pb)} - {mnum(pa*pb)} = {mnum(P,4)}$.\n\n"
           "Adding the probabilities double-counts the case where both fail.")
    return make(stem, num_mcq(rng, P, [pa + pb, pa * pb, 1 - pa * pb], lambda v: fnum(v, 4)), sol)


# =============================================================== ECONOMICS


def PF(i, n):
    return (1 + i) ** -n


def PA(i, n):
    return ((1 + i) ** n - 1) / (i * (1 + i) ** n)


def FA(i, n):
    return ((1 + i) ** n - 1) / i


def AP(i, n):
    return 1 / PA(i, n)


def AF(i, n):
    return i / ((1 + i) ** n - 1)


def money(v):
    return "\\$" + f"{v:,.0f}"


@tpl("econ")
def pw_single(rng):
    F = rng.choice([10000, 25000, 50000, 100000, 80000])
    i = rng.choice([0.05, 0.06, 0.08, 0.1, 0.12])
    n = rng.choice([5, 8, 10, 12, 15])
    P = F * PF(i, n)
    stem = (f"A utility expects to receive {money(F)} in {n} years when a contract matures. At an interest rate of {fnum(i*100)}% per year, "
            "what is the present worth of that receipt?")
    sol = (f"$$P = F(P/F, i, n) = F(1+i)^{{-n}} = {F:,}\\,(1.{int(round(i*100)):02d})^{{-{n}}} = {mnum(P,5)}$$\n\n"
           f"Present worth ≈ {money(P)}. Simple-interest discounting, $F/(1+in)$, gives {money(F/(1+i*n))} and is wrong for compound interest.")
    wr = [F / (1 + i * n), F * (1 - i) ** n, F * (1 + i) ** -(n - 1)]
    return make(stem, num_mcq(rng, P, wr, money), sol)


@tpl("econ")
def pw_annuity(rng):
    A = rng.choice([2000, 5000, 8000, 12000, 15000])
    i = rng.choice([0.05, 0.06, 0.08, 0.1])
    n = rng.choice([5, 8, 10, 15, 20])
    P = A * PA(i, n)
    stem = (f"An energy-efficient motor saves {money(A)} per year for {n} years. At {fnum(i*100)}% interest, what is the present worth of the savings?")
    sol = (f"$$P = A(P/A, i, n) = A\\,{frac('(1+i)^n - 1', 'i(1+i)^n')} = {A:,}\\times{mnum(PA(i,n),5)} = {mnum(P,5)}$$\n\n"
           f"Present worth ≈ {money(P)}. Multiplying $A \\times n$ ({money(A*n)}) ignores the time value of money.")
    wr = [A * n, A * FA(i, n), A * n * PF(i, n)]
    return make(stem, num_mcq(rng, P, wr, money), sol)


@tpl("econ")
def fw_annuity(rng):
    A = rng.choice([1000, 2500, 4000, 6000])
    i = rng.choice([0.04, 0.05, 0.06, 0.08])
    n = rng.choice([10, 15, 20, 25])
    F = A * FA(i, n)
    stem = (f"A firm deposits {money(A)} at the end of each year into a replacement fund earning {fnum(i*100)}% per year. "
            f"How much is in the fund immediately after the {n}th deposit?")
    sol = (f"$$F = A(F/A, i, n) = A\\,{frac('(1+i)^n - 1', 'i')} = {A:,}\\times{mnum(FA(i,n),5)} = {mnum(F,5)}$$\n\n"
           f"Fund value ≈ {money(F)}.")
    wr = [A * n, A * PA(i, n), A * n * (1 + i) ** n]
    return make(stem, num_mcq(rng, F, wr, money), sol)


@tpl("econ")
def capital_recovery(rng):
    P = rng.choice([50000, 120000, 200000, 75000])
    i = rng.choice([0.06, 0.08, 0.1, 0.12])
    n = rng.choice([5, 7, 10, 15])
    A = P * AP(i, n)
    stem = (f"A {money(P)} test rig is financed over {n} years at {fnum(i*100)}% interest with equal end-of-year payments. What is the annual payment?")
    sol = (f"$$A = P(A/P, i, n) = P\\,{frac('i(1+i)^n', '(1+i)^n - 1')} = {P:,}\\times{mnum(AP(i,n),5)} = {mnum(A,5)}$$\n\n"
           f"Payment ≈ {money(A)}. $P/n$ ({money(P/n)}) leaves out interest entirely.")
    wr = [P / n, P * i, P * (1 + i) ** n / n]
    return make(stem, num_mcq(rng, A, wr, money), sol)


@tpl("econ")
def effective_rate(rng):
    r = rng.choice([0.06, 0.08, 0.1, 0.12, 0.18])
    m, mname = rng.choice([(12, "monthly"), (4, "quarterly"), (365, "daily")])
    ie = (1 + r / m) ** m - 1
    stem = f"A loan carries a nominal annual rate of {fnum(r*100)}% compounded {mname}. What is the effective annual interest rate?"
    sol = (f"$$i_e = \\left(1 + {frac('r','m')}\\right)^m - 1 = \\left(1 + {frac(r, m)}\\right)^{{{m}}} - 1 = {mnum(ie*100,4)}\\%$$\n\n"
           "The effective rate always exceeds the nominal rate when compounding is more frequent than annual.")
    wr = [r, r / m * 12 if m != 12 else r * 1.02, math.exp(r) - 1 if m != 365 else (1 + r / 12) ** 12 - 1]
    return make(stem, num_mcq(rng, ie * 100, [w * 100 for w in wr], lambda v: fnum(v, 4) + "%"), sol)


@tpl("econ")
def sl_depreciation(rng):
    C = rng.choice([60000, 90000, 150000, 45000])
    S = rng.choice([5000, 10000, 15000])
    n = rng.choice([5, 8, 10])
    k = rng.randint(2, n - 1)
    D = (C - S) / n
    BV = C - k * D
    stem = (f"Equipment costs {money(C)}, has a {n}-year life and a salvage value of {money(S)}. Using straight-line depreciation, "
            f"what is its book value at the end of year {k}?")
    sol = (f"Annual depreciation $D = (C - S)/n = ({C:,} - {S:,})/{n} = {mnum(D,5)}$.\n\n"
           f"$$BV_{k} = C - kD = {C:,} - {k}({mnum(D,5)}) = {mnum(BV,5)}$$\n\n"
           f"Book value ≈ {money(BV)}. Ignoring the salvage value overstates the annual depreciation.")
    wr = [C - k * C / n, D, S + k * D]
    return make(stem, num_mcq(rng, BV, wr, money), sol)


@tpl("econ")
def breakeven(rng):
    F = rng.choice([40000, 60000, 90000, 120000])
    p = rng.choice([25, 40, 60, 80])
    v = rng.choice([10, 15, 20])
    Q = F / (p - v)
    stem = (f"A small electronics product has fixed costs of {money(F)} per year, sells for \\${p} per unit and costs \\${v} per unit to make. "
            "How many units per year must be sold to break even?")
    sol = (f"At break-even, revenue equals total cost: $pQ = F + vQ$, so\n\n$$Q = {frac('F','p - v')} = {frac(f'{F:,}', p-v)} = {mnum(Q,4)}\\ \\text{{units}}$$\n\n"
           "Round up in practice, since a fraction of a unit cannot be sold.")
    wr = [F / p, F / v, F / (p + v)]
    return make(stem, num_mcq(rng, Q, wr, lambda x: f"{x:,.0f} units"), sol)


@tpl("econ")
def euac(rng):
    P = rng.choice([30000, 50000, 80000])
    O = rng.choice([4000, 6000, 9000])
    S = rng.choice([3000, 5000, 8000])
    n = rng.choice([5, 8, 10])
    i = rng.choice([0.08, 0.1, 0.12])
    E = P * AP(i, n) + O - S * AF(i, n)
    stem = (f"A machine costs {money(P)}, has annual operating costs of {money(O)}, a life of {n} years and a salvage value of {money(S)}. "
            f"At {fnum(i*100)}% interest, what is its equivalent uniform annual cost (EUAC)?")
    sol = (f"$$\\text{{EUAC}} = P(A/P) + O - S(A/F) = {P:,}({mnum(AP(i,n),4)}) + {O:,} - {S:,}({mnum(AF(i,n),4)}) = {mnum(E,5)}$$\n\n"
           f"EUAC ≈ {money(E)}. The salvage term reduces cost; adding it is a frequent sign error.")
    wr = [P * AP(i, n) + O, P / n + O, P * AP(i, n) + O + S * AF(i, n)]
    return make(stem, num_mcq(rng, E, wr, money), sol)


@tpl("econ")
def payback(rng):
    P = rng.choice([24000, 36000, 50000, 18000])
    sav = rng.choice([6000, 8000, 10000, 4500])
    oc = rng.choice([1000, 1500, 2000])
    pb = P / (sav - oc)
    stem = (f"An LED retrofit costs {money(P)}. It saves {money(sav)} per year in energy but adds {money(oc)} per year in maintenance. "
            "What is the simple payback period?")
    sol = (f"Use the net annual saving: $\\text{{payback}} = {frac('P', '\\text{net saving}')} = {frac(f'{P:,}', f'{sav-oc:,}')} = {mnum(pb)}$ years.\n\n"
           "Simple payback ignores interest and benefits after the payback point, so it is a screening tool rather than a decision rule.")
    wr = [P / sav, P / (sav + oc), sav / P * 10]
    return make(stem, num_mcq(rng, pb, wr, lambda x: fnum(x) + " years"), sol)
