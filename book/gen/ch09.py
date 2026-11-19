"""Chapter 9 - Transfer functions, stability and frequency response."""
import math
import sympy as sp
from core import *
from lap import tp, ilt

CH = 9


def routh(coeffs):
    """Return Routh array rows (lists of sympy numbers) or None if a zero appears in the first column."""
    n = len(coeffs) - 1
    r1 = [sp.nsimplify(c) for c in coeffs[0::2]]
    r2 = [sp.nsimplify(c) for c in coeffs[1::2]]
    w = len(r1)
    r2 += [0] * (w - len(r2))
    rows = [r1, r2]
    for _ in range(n - 1):
        a, b = rows[-2], rows[-1]
        if b[0] == 0:
            return None
        new = []
        for i in range(w - 1):
            new.append(sp.nsimplify((b[0] * a[i + 1] - a[0] * b[i + 1]) / b[0]))
        new.append(0)
        rows.append(new)
    if any(r[0] == 0 for r in rows):
        return None
    return rows


def routh_tex(rows, n):
    lines = []
    for i, r in enumerate(rows):
        vals = [tex(v) for v in r if True]
        while len(vals) > 1 and vals[-1] == '0':
            vals.pop()
        lines.append(f"s^{{{n - i}}} & " + ' & '.join(vals))
    cols = 'c|' + 'c' * max(len(r) for r in rows)
    return f"$$\\begin{{array}}{{{cols}}} " + ' \\\\ '.join(lines) + " \\end{array}$$"


def h_from_ode(rng):
    p1, p2 = rng.sample([1, 2, 3, 4, 5, -1], 2)
    a1, a0 = p1 + p2, p1 * p2
    z = rng.choice([0, 1, 3, 6])
    b1, b0 = (1, z) if z else (0, rng.choice([2, 4, 10]))
    rhs = (f"\\dfrac{{dx}}{{dt}} + {cf(z)}x" if z else f"{b0}x")
    H = (b1 * s + b0) / (s ** 2 + a1 * s + a0)
    st = f"A system is described by $\\dfrac{{d^2y}}{{dt^2}} {'+' if a1 >= 0 else '-'} {abs(a1)}\\dfrac{{dy}}{{dt}} {'+' if a0 >= 0 else '-'} {abs(a0)}y = {rhs}$. Find $H(s)$, its poles and zeros, and decide whether the (causal) system is stable."
    stable = p1 > 0 and p2 > 0
    steps = [('Transform with zero initial conditions', f"$(s^2 {'+' if a1 >= 0 else '-'} {abs(a1)}s {'+' if a0 >= 0 else '-'} {abs(a0)})Y(s) = ({'s + ' + str(z) if z else str(b0)})X(s)$."),
             ('Transfer function', f"$H(s) = \\dfrac{{Y}}{{X}} = {tex(sp.factor(H))}$."),
             ('Poles and zeros', f"Poles at $s = {-p1}$ and $s = {-p2}$; " + (f"a zero at $s = {-z}$." if z else 'no finite zeros.')),
             ('Stability', 'Both poles are in the left half-plane, so the causal system is stable.' if stable else f"A pole at $s = {max(-p1, -p2)}$ lies in the right half-plane, so the causal system is unstable: its impulse response contains a growing exponential.")]
    return Prob('A', st, steps, f"$H(s) = {tex(sp.factor(H))}$; " + ('stable.' if stable else 'unstable.'), 'Transfer functions')


def pole_stability(rng):
    case = cyc(rng, 'ps', ['stable', 'marg', 'unst', 'cplx', 'margrep'])
    if case == 'stable':
        H = 1 / ((s + 1) * (s ** 2 + 2 * s + 5))
        verdict = 'Stable: all poles ($-1$, $-1 \\pm 2j$) are in the left half-plane.'
    elif case == 'marg':
        H = (s + 2) / (s * (s + 3))
        verdict = 'Not BIBO stable (marginally stable): the simple pole at $s = 0$ gives a step component in $h(t)$ that never decays; a step input produces a ramp.'
    elif case == 'unst':
        H = (s - 1) / ((s + 2) * (s - 3))
        verdict = 'Unstable: the pole at $s = 3$ is in the right half-plane. (The zero at $s = 1$ is irrelevant to stability.)'
    elif case == 'cplx':
        w0 = rng.choice([2, 3, 4])
        H = sp.Integer(1) / (s ** 2 + w0 ** 2)
        verdict = f'Not BIBO stable: poles at $\\pm j{w0}$ on the imaginary axis; an input at ${w0}$ rad/s causes resonance and an unbounded output.'
    else:
        H = sp.Integer(1) / (s ** 2 * (s + 1))
        verdict = 'Unstable: the double pole at $s = 0$ gives a ramp in $h(t)$.'
    st = f"Determine the stability of the causal LTI system $H(s) = {tex(H)}$."
    steps = [('Rule', 'A causal LTI system is BIBO stable if and only if every pole of $H(s)$ has a negative real part. Zeros play no part.'),
             ('Find the poles', 'Set the denominator to zero and solve.'),
             ('Verdict', verdict)]
    return Prob('A', st, steps, verdict, 'Stability from poles')


def dc_gain(rng):
    p1, p2 = rng.sample([1, 2, 4, 5], 2)
    K = rng.choice([2, 10, 20])
    z = rng.choice([1, 2, 3])
    A = rng.choice([2, 3, 5])
    H = K * (s + z) / ((s + p1) * (s + p2))
    G0 = H.subs(s, 0)
    st = f"The stable system $H(s) = {tex(H)}$ is driven by the step $x(t) = {A}u(t)$. What is the steady-state output?"
    steps = [('Final value theorem', f"$y(\\infty) = \\lim_{{s\\to0}} s\\cdot H(s)\\cdot\\dfrac{{{A}}}{{s}} = {A}H(0)$, valid because all poles are in the left half-plane."),
             ('DC gain', f"$H(0) = \\dfrac{{{K}\\cdot{z}}}{{{p1}\\cdot{p2}}} = {tex(G0)}$."),
             ('Result', f"$y(\\infty) = {tex(A * G0)}$.")]
    return Prob('A', st, steps, f"$y(\\infty) = {tex(A * G0)}$.", 'DC gain')


def routh_numeric(rng):
    for _ in range(200):
        deg = rng.choice([3, 3, 4])
        rts = []
        while len(rts) < deg:
            if deg - len(rts) >= 2 and rng.random() < 0.4:
                re = rng.choice([-2, -1, 1, 2, -3])
                im = rng.choice([1, 2])
                rts += [re + im * j, re - im * j]
            else:
                rts.append(rng.choice([-1, -2, -3, -4, 1, 2, -5]))
        poly = sp.Poly(sp.expand(sp.prod([s - r for r in rts])), s)
        co = poly.all_coeffs()
        if not all(c.is_integer for c in co) or any(c == 0 for c in co[1:]) and rng.random() < 0.7:
            continue
        rows = routh(co)
        if rows is None:
            continue
        rhp = sum(1 for r in rts if sp.re(r) > 0)
        break
    P = tex(poly.as_expr())
    signs = [r[0] for r in rows]
    changes = sum(1 for a, b in zip(signs, signs[1:]) if (a > 0) != (b > 0))
    st = f"Use the Routh–Hurwitz criterion to determine how many roots of $P(s) = {P}$ lie in the right half-plane."
    steps = [('Necessary condition', 'All coefficients must be positive for stability. ' + ('They are, so we must build the array.' if all(c > 0 for c in co) else 'They are not, so the polynomial certainly has roots in the right half-plane (or on the axis); the array tells us how many.')),
             ('First two rows', 'Fill the first row with alternate coefficients starting from the highest power, and the second row with the others.'),
             ('Remaining rows', 'Each new entry is $-\\dfrac{1}{b_1}\\begin{vmatrix} a_1 & a_{i+1} \\\\ b_1 & b_{i+1}\\end{vmatrix}$, using the two rows above.' + routh_tex(rows, deg)),
             ('Count sign changes', f"First column: ${', '.join(tex(v) for v in signs)}$. There {'is' if changes == 1 else 'are'} {changes} sign change{'s' if changes != 1 else ''}."),
             ('Conclusion', f"{changes} root{'s' if changes != 1 else ''} in the right half-plane" + ('; the polynomial is Hurwitz (stable).' if changes == 0 else '.') + ' (Factorising confirms it: the roots are ' + ', '.join(f"${tex(r)}$" for r in rts) + '.)')]
    assert changes == rhp
    return Prob('B', st, steps, f"{changes} right-half-plane root{'s' if changes != 1 else ''}" + (' (stable).' if changes == 0 else '.'), 'Routh–Hurwitz')


def routh_K(rng):
    a = rng.choice([2, 3, 4, 5, 6])
    b = rng.choice([2, 3, 5, 8])
    c = rng.choice([1, 2])
    Kmax = sp.Rational(a * b, c)
    st = f"A feedback system has characteristic equation $s^3 + {a}s^2 + {b}s + {cf(c)}K = 0$. Find the range of $K$ for stability and the frequency of oscillation at the limit."
    wosc = sp.sqrt(b)
    steps = [('Routh array', f"$$\\begin{{array}}{{c|cc}} s^3 & 1 & {b} \\\\ s^2 & {a} & {cf(c)}K \\\\ s^1 & \\dfrac{{{a*b} - {cf(c)}K}}{{{a}}} & 0 \\\\ s^0 & {cf(c)}K & \\end{{array}}$$"),
             ('Conditions', f"All first-column entries positive: ${a*b} - {cf(c)}K > 0$ and ${cf(c)}K > 0$."),
             ('Range', f"$0 < K < {tex(Kmax)}$."),
             ('Oscillation at the limit', f"At $K = {tex(Kmax)}$ the $s^1$ row vanishes. The auxiliary equation from the $s^2$ row is ${a}s^2 + {a*b} = 0$, so $s = \\pm j{tex(wosc)}$: the system oscillates at $\\omega = {tex(wosc)}$ rad/s.")]
    return Prob('B', st, steps, f"$0 < K < {tex(Kmax)}$; oscillation at $\\omega = {tex(wosc)}$ rad/s.", 'Stability range')


def second_order_specs(rng):
    wn = cyc(rng, 'wn', [2, 4, 5, 10, 3, 6])
    zeta = rng.choice([Q(1, 5), Q(3, 10), Q(2, 5), Q(1, 2), Q(3, 5), Q(7, 10)])
    a1 = 2 * zeta * wn
    a0 = wn * wn
    H = a0 / (s ** 2 + a1 * s + a0)
    zf = float(zeta)
    OS = math.exp(-math.pi * zf / math.sqrt(1 - zf * zf)) * 100
    wd = wn * math.sqrt(1 - zf * zf)
    Tp = math.pi / wd
    Ts = 4 / (zf * wn)
    st = f"For $H(s) = \\dfrac{{{a0}}}{{s^2 + {tex(a1)}s + {a0}}}$, find $\\omega_n$, $\\zeta$, the damped frequency, the percentage overshoot, the peak time and the 2% settling time of the step response."
    steps = [('Match the standard form', f"$\\dfrac{{\\omega_n^2}}{{s^2 + 2\\zeta\\omega_n s + \\omega_n^2}}$: $\\omega_n^2 = {a0}$ gives $\\omega_n = {wn}$ rad/s, and $2\\zeta\\omega_n = {tex(a1)}$ gives $\\zeta = {tex(zeta)}$."),
             ('Damped frequency', f"$\\omega_d = \\omega_n\\sqrt{{1 - \\zeta^2}} \\approx {wd:.3f}$ rad/s."),
             ('Overshoot', f"$M_p = e^{{-\\pi\\zeta/\\sqrt{{1-\\zeta^2}}}} \\approx {OS:.1f}\\%$."),
             ('Peak time', f"$T_p = \\pi/\\omega_d \\approx {Tp:.3f}$ s."),
             ('Settling time', f"$T_s \\approx 4/(\\zeta\\omega_n) = {Ts:.3f}$ s, from the envelope $e^{{-\\zeta\\omega_n t}}$ falling below 2%.")]
    return Prob('B', st, steps, f"$\\omega_n = {wn}$, $\\zeta = {tex(zeta)}$, $\\omega_d \\approx {wd:.3f}$, overshoot $\\approx {OS:.1f}\\%$, $T_p \\approx {Tp:.3f}$ s, $T_s \\approx {Ts:.3f}$ s.", 'Second-order response')


def sss(rng):
    p = rng.choice([1, 2, 4, 5])
    K = rng.choice([2, 5, 10])
    w0 = rng.choice([1, 2, 3, 5])
    A = rng.choice([1, 2, 3])
    two = rng.random() < 0.4
    H = K / (s + p) if not two else K / ((s + p) * (s + 1))
    Hj = sp.simplify(H.subs(s, j * w0))
    m = float(sp.Abs(Hj))
    ph = float(sp.arg(Hj))
    st = f"Find the steady-state response of $H(s) = {tex(H)}$ to $x(t) = {cf(A)}\\cos({cf(w0)}t)$."
    steps = [('Evaluate on the imaginary axis', f"$H(j{w0}) = {tex(Hj)}$."),
             ('Magnitude and phase', f"$|H(j{w0})| \\approx {m:.4f}$, $\\angle H(j{w0}) \\approx {ph:.4f}$ rad $({math.degrees(ph):.1f}^\\circ)$."),
             ('Steady state', f"$y_{{ss}}(t) = {A}|H|\\cos({w0}t + \\angle H)$. The transient terms from the poles die away because the system is stable.")]
    return Prob('B', st, steps, f"$y_{{ss}}(t) \\approx {A*m:.4f}\\cos({cf(w0)}t - {abs(ph):.4f})$.", 'Sinusoidal steady state')


def bode(rng):
    z = rng.choice([1, 2, 5, 10])
    p1 = z * rng.choice([10, 20])
    p2 = p1 * rng.choice([5, 10])
    K = rng.choice([10, 100, 1000])
    w = rng.choice([z, p1, int(math.sqrt(z * p1))])
    H = K * (s + z) / ((s + p1) * (s + p2))
    G0 = K * z / (p1 * p2)
    Hj = H.subs(s, j * w)
    dB = 20 * math.log10(float(sp.Abs(Hj)))
    st = f"Sketch the asymptotic Bode magnitude plot of $H(s) = {tex(H)}$ and find the exact gain in dB at $\\omega = {w}$ rad/s."
    steps = [('Normalise', f"$H(s) = {tex(sp.Rational(K*z, p1*p2))}\\,\\dfrac{{1 + s/{z}}}{{(1 + s/{p1})(1 + s/{p2})}}$, so the low-frequency gain is ${tex(sp.Rational(K*z, p1*p2))}$, i.e. ${20*math.log10(G0):.1f}$ dB."),
             ('Corner frequencies', f"Zero at ${z}$ rad/s (slope $+20$ dB/decade from there), poles at ${p1}$ and ${p2}$ rad/s (each adds $-20$ dB/decade)."),
             ('Asymptotes', f"Flat up to ${z}$; rising at $+20$ dB/dec to ${p1}$; flat again to ${p2}$; then falling at $-20$ dB/dec."),
             ('Exact value', f"$|H(j{w})| = {float(sp.Abs(Hj)):.4f}$, i.e. ${dB:.2f}$ dB. At a single corner the exact curve sits about 3 dB from the asymptotes.")]
    return Prob('C', st, steps, f"Low-frequency gain ${20*math.log10(G0):.1f}$ dB; corners at {z}, {p1}, {p2} rad/s; $|H(j{w})| \\approx {dB:.2f}$ dB.", 'Bode plots')


def feedback_err(rng):
    a = rng.choice([1, 2, 4, 5])
    K = rng.choice([4, 10, 20, 50])
    typ = cyc(rng, 'ty', [1, 0, 1, 0, 1])
    if typ == 1:
        G = K / (s * (s + a))
        T = sp.factor(sp.simplify(G / (1 + G)))
        Kv = sp.Rational(K, a)
        st = f"A unity-feedback system has open-loop transfer function $G(s) = {tex(G)}$. Find the closed-loop transfer function and the steady-state errors for a unit step and a unit ramp."
        steps = [('Closed loop', f"$T(s) = \\dfrac{{G}}{{1 + G}} = \\dfrac{{{K}}}{{s^2 + {cf(a)}s + {K}}}$, stable for any positive gain."),
                 ('System type', 'One integrator in $G$: a type 1 system.'),
                 ('Step', '$K_p = \\lim_{s\\to0}G(s) = \\infty$, so $e_{ss} = 1/(1 + K_p) = 0$.'),
                 ('Ramp', f"$K_v = \\lim_{{s\\to0}} sG(s) = {K}/{a} = {tex(Kv)}$, so $e_{{ss}} = 1/K_v = {tex(1/Kv)}$.")]
        ans = f"$T(s) = \\dfrac{{{K}}}{{s^2 + {cf(a)}s + {K}}}$; step error $0$; ramp error ${tex(1/Kv)}$."
    else:
        b = rng.choice([v for v in [1, 3, 5] if v != a])
        G = K / ((s + a) * (s + b))
        Kp = sp.Rational(K, a * b)
        st = f"A unity-feedback system has $G(s) = {tex(G)}$. Find the closed-loop transfer function and the steady-state error to a unit step."
        steps = [('Closed loop', f"$T(s) = \\dfrac{{{K}}}{{s^2 + {a+b}s + {a*b + K}}}$."),
                 ('System type', 'No integrator: a type 0 system, which cannot track a step perfectly.'),
                 ('Position constant', f"$K_p = G(0) = {tex(Kp)}$."),
                 ('Error', f"$e_{{ss}} = \\dfrac{{1}}{{1 + K_p}} = {tex(1/(1 + Kp))}$. Raising $K$ reduces the error but, in higher-order systems, eventually costs stability.")]
        ans = f"$T(s) = \\dfrac{{{K}}}{{s^2 + {a+b}s + {a*b+K}}}$; $e_{{ss}} = {tex(1/(1+Kp))}$."
    return Prob('C', st, steps, ans, 'Feedback and steady-state error')


def block(rng):
    a, b = rng.sample([1, 2, 3, 5], 2)
    k = rng.choice([1, 2, 4])
    case = cyc(rng, 'bk', ['fb', 'par', 'nested', 'fb'])
    G1 = sp.Integer(k) / (s + a)
    G2 = sp.Integer(1) / (s + b)
    if case == 'fb':
        H = sp.Integer(rng.choice([1, 2]))
        T = sp.factor(sp.simplify(G1 * G2 / (1 + G1 * G2 * H)))
        st = f"Blocks $G_1 = {tex(G1)}$ and $G_2 = {tex(G2)}$ are in cascade in the forward path, with negative feedback through $H = {tex(H)}$. Find the overall transfer function."
        steps = [('Forward path', f"$G_1G_2 = {tex(sp.factor(G1*G2))}$."), ('Feedback formula', '$T = \\dfrac{G_1G_2}{1 + G_1G_2H}$.'), ('Simplify', f"Multiply top and bottom by $(s + {a})(s + {b})$: $T(s) = {tex(T)}$.")]
    elif case == 'par':
        T = sp.factor(sp.together(G1 + G2))
        st = f"Blocks $G_1 = {tex(G1)}$ and $G_2 = {tex(G2)}$ are in parallel, their outputs added. Find the overall transfer function and its zero."
        zz = sp.solve(sp.fraction(T)[0], s)
        steps = [('Parallel blocks add', f"$T = G_1 + G_2 = {tex(T)}$."), ('Zero', f"The numerator vanishes at $s = {tex(zz[0])}$: parallel connections create zeros that neither block had alone.")]
    else:
        T = sp.factor(sp.simplify((G1 / (1 + G1)) * G2 / (1 + (G1 / (1 + G1)) * G2)))
        st = f"An inner loop consists of $G_1 = {tex(G1)}$ with unity negative feedback. Its output feeds $G_2 = {tex(G2)}$, and the whole is enclosed in an outer unity negative feedback loop. Find the overall transfer function."
        inner = sp.factor(sp.simplify(G1 / (1 + G1)))
        steps = [('Inner loop first', f"$G_i = \\dfrac{{G_1}}{{1 + G_1}} = {tex(inner)}$."), ('Forward path', f"$G_iG_2 = {tex(sp.factor(inner*G2))}$."), ('Outer loop', f"$T = \\dfrac{{G_iG_2}}{{1 + G_iG_2}} = {tex(T)}$.")]
    return Prob('C', st, steps, f"$T(s) = {tex(T)}$.", 'Block diagrams')


TEMPLATES = [(h_from_ode, 6), (pole_stability, 4), (dc_gain, 4),
             (routh_numeric, 7), (routh_K, 4), (second_order_specs, 6), (sss, 5),
             (bode, 5), (feedback_err, 5), (block, 4)]


def generate():
    return build_set(TEMPLATES, seed=909)


if __name__ == '__main__':
    for i, p in enumerate(generate(), 1):
        print(f'--- 9.{i} [{p.level}] {p.topic}\n{p.statement}\n  ANS: {p.answer}')
