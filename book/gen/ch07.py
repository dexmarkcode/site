"""Chapter 7 - The Laplace transform and its properties."""
import sympy as sp
from core import *
from lap import tp, ilt

CH = 7


def LT(f):
    return sp.simplify(sp.laplace_transform(f, tp, s, noconds=True))


def basic(rng):
    case = cyc(rng, 'b', ['expconst', 'poly', 'trig', 'mix', 'dtrig', 'expconst'])
    A, B = rng.choice([2, 3, 4, 5]), rng.choice([1, 2, 6])
    a, w0 = rng.choice([1, 2, 3, 4]), rng.choice([2, 3, 4, 5])
    if case == 'expconst':
        f = A * sp.exp(-a * tp) + B
        ft = f"{A}{expo(a)} + {B}"
        lines = [f"${A}{expo(a)} \\to \\dfrac{{{A}}}{{s + {a}}}$, ROC $\\operatorname{{Re}}(s) > -{a}$", f"${B} \\to \\dfrac{{{B}}}{{s}}$, ROC $\\operatorname{{Re}}(s) > 0$"]
        roc = '0'
    elif case == 'poly':
        f = A * tp ** 2 + B * tp
        ft = f"{A}t^2 + {cf(B)}t"
        lines = [f"$t^n \\to n!/s^{{n+1}}$, so ${A}t^2 \\to {2*A}/s^3$", f"${cf(B)}t \\to {B}/s^2$"]
        roc = '0'
    elif case == 'trig':
        f = A * sp.cos(w0 * tp) + B * sp.sin(w0 * tp)
        ft = f"{A}\\cos({w0}t) + {cf(B)}\\sin({w0}t)"
        lines = [f"$\\cos\\omega_0 t \\to \\dfrac{{s}}{{s^2 + \\omega_0^2}}$ and $\\sin\\omega_0 t \\to \\dfrac{{\\omega_0}}{{s^2 + \\omega_0^2}}$ with $\\omega_0 = {w0}$"]
        roc = '0'
    elif case == 'mix':
        f = A * tp * sp.exp(-a * tp) + B * sp.exp(-2 * a * tp)
        ft = f"{A}t{expo(a)} + {cf(B)}{expo(2*a)}"
        lines = [f"$t e^{{-at}} \\to \\dfrac{{1}}{{(s + a)^2}}$ gives $\\dfrac{{{A}}}{{(s + {a})^2}}$", f"${cf(B)}{expo(2*a)} \\to \\dfrac{{{B}}}{{s + {2*a}}}$"]
        roc = f'-{a}'
    else:
        f = A * sp.exp(-a * tp) * sp.cos(w0 * tp)
        ft = f"{A}{expo(a)}\\cos({w0}t)"
        lines = [f"Start from $\\cos({w0}t) \\to \\dfrac{{s}}{{s^2 + {w0*w0}}}$", f"Multiplying by ${expo(a)}$ replaces $s$ by $s + {a}$: $\\dfrac{{{A}(s + {a})}}{{(s + {a})^2 + {w0*w0}}}$"]
        roc = f'-{a}'
    F = LT(f)
    st = f"Find the Laplace transform of $x(t) = \\left({ft}\\right)u(t)$ and state its region of convergence."
    steps = [('Linearity', 'Transform each term separately using the standard table and add.')]
    steps += [(f'Term {i+1}' if len(lines) > 1 else 'Table entry', l + '.') for i, l in enumerate(lines)]
    steps.append(('Combine', f"$X(s) = {tex(sp.apart(F, s)) if case != 'dtrig' else tex(F)}$" + (f", which over a common denominator is ${tex(sp.factor(F))}$." if case in ('expconst', 'trig') else '.')))
    steps.append(('Region of convergence', f"The ROC is the intersection of the individual ROCs, i.e. to the right of the right-most pole: $\\operatorname{{Re}}(s) > {roc}$."))
    return Prob('A', st, steps, f"$X(s) = {tex(sp.factor(F))}$, ROC $\\operatorname{{Re}}(s) > {roc}$.", 'Standard transforms')


def roc_type(rng):
    a, b = sorted(rng.sample([1, 2, 3, 4, 5], 2))
    case = cyc(rng, 'r', ['right', 'left', 'two', 'none'])
    if case == 'right':
        st = f"Find the bilateral Laplace transform and ROC of $x(t) = e^{{-{a}t}}u(t) + e^{{-{b}t}}u(t)$."
        ans = f"$X(s) = \\dfrac{{1}}{{s + {a}}} + \\dfrac{{1}}{{s + {b}}}$, ROC $\\operatorname{{Re}}(s) > -{a}$."
        steps = [('Right-sided terms', f"Each term converges to the right of its pole: $\\operatorname{{Re}}(s) > -{a}$ and $\\operatorname{{Re}}(s) > -{b}$."),
                 ('Intersect', f"Both hold when $\\operatorname{{Re}}(s) > -{a}$: a right half-plane to the right of the right-most pole.")]
    elif case == 'left':
        st = f"Find the bilateral Laplace transform and ROC of $x(t) = -e^{{{a}t}}u(-t)$."
        ans = f"$X(s) = \\dfrac{{1}}{{s - {a}}}$, ROC $\\operatorname{{Re}}(s) < {a}$."
        steps = [('Integrate over negative time', f"$X(s) = -\\int_{{-\\infty}}^0 e^{{{a}t}}e^{{-st}}dt = -\\left[\\dfrac{{e^{{({a} - s)t}}}}{{{a} - s}}\\right]_{{-\\infty}}^0$."),
                 ('Convergence', f"The lower limit vanishes only if $\\operatorname{{Re}}(s) < {a}$."),
                 ('Result', f"$X(s) = \\dfrac{{-1}}{{{a} - s}} = \\dfrac{{1}}{{s - {a}}}$. This is the same algebraic expression as for $e^{{{a}t}}u(t)$; only the ROC tells them apart.")]
    elif case == 'two':
        st = f"Find the bilateral Laplace transform and ROC of $x(t) = e^{{-{a}t}}u(t) + e^{{{b}t}}u(-t)$."
        ans = f"$X(s) = \\dfrac{{1}}{{s + {a}}} - \\dfrac{{1}}{{s - {b}}}$, ROC $-{a} < \\operatorname{{Re}}(s) < {b}$."
        steps = [('Right-sided part', f"$\\dfrac{{1}}{{s + {a}}}$ for $\\operatorname{{Re}}(s) > -{a}$."),
                 ('Left-sided part', f"$-\\dfrac{{1}}{{s - {b}}}$ for $\\operatorname{{Re}}(s) < {b}$."),
                 ('Intersect', f"A vertical strip $-{a} < \\operatorname{{Re}}(s) < {b}$, which contains the imaginary axis, so the Fourier transform also exists.")]
    else:
        st = f"Does $x(t) = e^{{-{b}t}}u(t) + e^{{-{a}t}}u(-t)$ have a bilateral Laplace transform? If so, does it have a Fourier transform?"
        ans = f"Yes: $X(s) = \\dfrac{{1}}{{s + {b}}} - \\dfrac{{1}}{{s + {a}}}$ with ROC $-{b} < \\operatorname{{Re}}(s) < -{a}$, a strip that excludes the $j\\omega$ axis."
        steps = [('Right-sided part', f"$e^{{-{b}t}}u(t) \\to \\dfrac{{1}}{{s + {b}}}$, needing $\\operatorname{{Re}}(s) > -{b}$."),
                 ('Left-sided part', f"$e^{{-{a}t}}u(-t) \\to -\\dfrac{{1}}{{s + {a}}}$, needing $\\operatorname{{Re}}(s) < -{a}$."),
                 ('Intersect', f"Because $-{b} < -{a}$, the strip $-{b} < \\operatorname{{Re}}(s) < -{a}$ is non-empty, so the transform exists there."),
                 ('Fourier transform?', 'The strip does not contain the imaginary axis, so the Fourier transform does not exist: the left-sided term grows as $t \\to -\\infty$.')]
    return Prob('A', st, steps, ans, 'Region of convergence')


def definition(rng):
    case = cyc(rng, 'd', ['exp', 'pulse', 'ramp'])
    if case == 'exp':
        a = rng.choice([2, 3, 5])
        st = f"Using the definition, find the Laplace transform of $x(t) = {expo(a)}u(t)$ and its ROC."
        steps = [('Definition', f"$X(s) = \\int_0^\\infty {expo(a)}e^{{-st}}dt = \\int_0^\\infty e^{{-(s + {a})t}}dt$."),
                 ('Evaluate', f"$= \\left[\\dfrac{{e^{{-(s+{a})t}}}}{{-(s+{a})}}\\right]_0^\\infty = \\dfrac{{1}}{{s + {a}}}$, provided the upper limit vanishes, i.e. $\\operatorname{{Re}}(s + {a}) > 0$.")]
        ans = f"$\\dfrac{{1}}{{s + {a}}}$, ROC $\\operatorname{{Re}}(s) > -{a}$."
    elif case == 'pulse':
        A, T = rng.choice([2, 3, 5]), rng.choice([1, 2, 4])
        st = f"Using the definition, find the Laplace transform of the pulse $x(t) = {A}$ for $0 \\le t < {T}$, zero elsewhere."
        steps = [('Definition', f"$X(s) = \\int_0^{{{T}}} {A}e^{{-st}}dt = {A}\\left[\\dfrac{{e^{{-st}}}}{{-s}}\\right]_0^{{{T}}}$."),
                 ('Evaluate', f"$= \\dfrac{{{A}(1 - e^{{-{cf(T)}s}})}}{{s}}$."),
                 ('ROC', 'The integral is over a finite interval of a bounded function, so it converges for every $s$: the ROC is the whole plane. The apparent pole at $s = 0$ is cancelled by a zero of the numerator.')]
        ans = f"$\\dfrac{{{A}(1 - e^{{-{cf(T)}s}})}}{{s}}$, ROC: all $s$."
    else:
        st = "Using the definition and integration by parts, show that the ramp $t\\,u(t)$ has Laplace transform $1/s^2$."
        steps = [('Definition', '$X(s) = \\int_0^\\infty t e^{-st}dt$.'),
                 ('By parts', 'With $u = t$, $dv = e^{-st}dt$: $X = \\left[-\\dfrac{te^{-st}}{s}\\right]_0^\\infty + \\dfrac{1}{s}\\int_0^\\infty e^{-st}dt$.'),
                 ('Evaluate', 'For $\\operatorname{Re}(s) > 0$ the boundary term vanishes and the remaining integral is $1/s$, so $X = 1/s^2$.')]
        ans = '$1/s^2$, ROC $\\operatorname{Re}(s) > 0$.'
    return Prob('A', st, steps, ans, 'Transform from the definition')


def shifting(rng):
    case = cyc(rng, 'sh', ['tshift', 'sshift', 'tshift2', 'sshift2', 'tsin', 'texp'])
    a, T, w0 = rng.choice([1, 2, 3]), rng.choice([1, 2, 3]), rng.choice([2, 3, 4])
    if case == 'tshift':
        st = f"Find the Laplace transform of $x(t) = (t - {T})u(t - {T})$."
        ans = f"\\dfrac{{e^{{-{cf(T)}s}}}}{{s^2}}"
        steps = [('Recognise a delayed ramp', f"The whole ramp $t\\,u(t)$ has been delayed by ${T}$."), ('Time-shift property', f"$x(t - T)u(t - T) \\leftrightarrow e^{{-sT}}X(s)$, so the answer is ${ans}$.")]
    elif case == 'tshift2':
        st = f"Find the Laplace transform of $x(t) = t\\,u(t - {T})$. (Careful: this is not a delayed ramp.)"
        ans = f"e^{{-{cf(T)}s}}\\left(\\dfrac{{1}}{{s^2}} + \\dfrac{{{T}}}{{s}}\\right)"
        steps = [('Rewrite in delayed form', f"$t = (t - {T}) + {T}$, so $x(t) = (t - {T})u(t - {T}) + {T}u(t - {T})$."),
                 ('Shift each piece', f"$\\to e^{{-{cf(T)}s}}\\cdot\\dfrac{{1}}{{s^2}} + {T}e^{{-{cf(T)}s}}\\cdot\\dfrac{{1}}{{s}}$."),
                 ('Lesson', 'The time-shift property needs the *whole* function shifted. Rewrite first, then apply.')]
    elif case == 'sshift':
        st = f"Find the Laplace transform of $x(t) = {expo(a)}\\sin({w0}t)u(t)$."
        ans = f"\\dfrac{{{w0}}}{{(s + {a})^2 + {w0*w0}}}"
        steps = [('Base transform', f"$\\sin({w0}t) \\to \\dfrac{{{w0}}}{{s^2 + {w0*w0}}}$."), ('Frequency shift', f"Multiplying by $e^{{-at}}$ replaces $s$ by $s + a$: ${ans}$."),
                 ('Poles', f"At $s = -{a} \\pm j{w0}$: the decay rate sets the real part and the oscillation frequency the imaginary part.")]
    elif case == 'sshift2':
        n_ = rng.choice([2, 3])
        st = f"Find the Laplace transform of $x(t) = t^{n_}{expo(a)}u(t)$."
        ans = f"\\dfrac{{{math_fact(n_)}}}{{(s + {a})^{{{n_+1}}}}}"
        steps = [('Base transform', f"$t^{n_} \\to {math_fact(n_)}/s^{n_+1}$."), ('Frequency shift', f"Replace $s$ by $s + {a}$: ${ans}$.")]
    elif case == 'tsin':
        st = f"Find the Laplace transform of $x(t) = \\sin({w0}(t - {T}))u(t - {T})$."
        ans = f"\\dfrac{{{w0}e^{{-{cf(T)}s}}}}{{s^2 + {w0*w0}}}"
        steps = [('A delayed sine', 'The sinusoid and the step are delayed together, so the time-shift property applies directly.'), ('Apply', f"${ans}$.")]
    else:
        st = f"Find the Laplace transform of $x(t) = {expo(a)}u(t - {T})$."
        ans = f"\\dfrac{{e^{{-{tex(a*T)}}}e^{{-{cf(T)}s}}}}{{s + {a}}}"
        steps = [('Rewrite', f"${expo(a)} = e^{{-{tex(a*T)}}}\\,{expo(a, f'(t - {T})')}$, so $x(t) = e^{{-{tex(a*T)}}}{expo(a, f'(t - {T})')}u(t - {T})$."),
                 ('Shift', f"$\\to e^{{-{tex(a*T)}}}\\cdot\\dfrac{{e^{{-{cf(T)}s}}}}{{s + {a}}}$."),
                 ('Equivalently', f"$X(s) = \\dfrac{{e^{{-{T}(s + {a})}}}}{{s + {a}}}$.")]
    return Prob('B', st, steps, f"${ans}$.", 'Shifting properties')


def math_fact(n_):
    import math
    return math.factorial(n_)


def piecewise(rng):
    case = cyc(rng, 'pw', ['pulse', 'stair', 'ramphold', 'tri', 'pulse'])
    A, T = rng.choice([1, 2, 3, 4]), rng.choice([1, 2, 3])
    if case == 'pulse':
        t1 = rng.choice([1, 2])
        st = f"Find the Laplace transform of a pulse of height ${A}$ that starts at $t = {t1}$ and ends at $t = {t1 + T}$."
        ans = f"\\dfrac{{{cf(A)}\\left(e^{{-{cf(t1)}s}} - e^{{-{cf(t1+T)}s}}\\right)}}{{s}}"
        steps = [('Steps', f"$x(t) = {A}[u(t - {t1}) - u(t - {t1+T})]$."), ('Transform', f"Each delayed step gives $e^{{-sT}}/s$: ${ans}$.")]
    elif case == 'stair':
        st = f"Find the Laplace transform of the staircase that equals ${A}$ on $0 \\le t < {T}$, ${2*A}$ on ${T} \\le t < {2*T}$, and zero afterwards."
        ans = f"\\dfrac{{{cf(A)}\\left(1 + e^{{-{cf(T)}s}} - 2e^{{-{cf(2*T)}s}}\\right)}}{{s}}"
        steps = [('Jumps', f"$+{A}$ at $0$, $+{A}$ at ${T}$, $-{2*A}$ at ${2*T}$, so $x(t) = {A}u(t) + {A}u(t - {T}) - {2*A}u(t - {2*T})$."), ('Transform', f"${ans}$.")]
    elif case == 'ramphold':
        st = f"Find the Laplace transform of the signal that rises linearly from $0$ to ${A}$ over $0 \\le t \\le {T}$ and stays at ${A}$ thereafter."
        ans = f"\\dfrac{{{cf(Q(A, T))}\\left(1 - e^{{-{cf(T)}s}}\\right)}}{{s^2}}"
        steps = [('Ramps', f"Slope ${tex(Q(A,T))}$ switches on at $0$ and off at ${T}$: $x(t) = {tex(Q(A,T))}[r(t) - r(t - {T})]$."), ('Transform', f"$r(t) \\to 1/s^2$ and a delay multiplies by $e^{{-{cf(T)}s}}$: ${ans}$."),
                 ('Check', f"Final value: $\\lim_{{s\\to0}} sX(s) = {tex(Q(A,T))}\\cdot{T} = {A}$, as expected.")]
    else:
        st = f"Find the Laplace transform of the triangular pulse that rises from $0$ to ${A}$ over $[0, {T}]$ and falls back to $0$ over $[{T}, {2*T}]$."
        ans = f"\\dfrac{{{cf(Q(A, T))}\\left(1 - e^{{-{cf(T)}s}}\\right)^2}}{{s^2}}"
        steps = [('Slope changes', f"$+{tex(Q(A,T))}$ at $0$, $-{tex(Q(2*A,T))}$ at ${T}$, $+{tex(Q(A,T))}$ at ${2*T}$: $x = {tex(Q(A,T))}[r(t) - 2r(t - {T}) + r(t - {2*T})]$."),
                 ('Transform and factor', f"${tex(Q(A,T))}\\dfrac{{1 - 2e^{{-{cf(T)}s}} + e^{{-{cf(2*T)}s}}}}{{s^2}} = {ans}$.")]
    return Prob('B', st, steps, f"${ans}$.", 'Piecewise signals')


def ivt_fvt(rng):
    case = cyc(rng, 'iv', ['ok', 'ok', 'unstable', 'osc', 'ok', 'ok'])
    if case == 'ok':
        a, b = rng.sample([1, 2, 3, 4, 5], 2)
        c = rng.choice([1, 2, 3])
        d = rng.choice([2, 4, 6, 10])
        X = (c * s + d) / (s * (s + a) * (s + b))
        x0 = sp.limit(s * X, s, sp.oo)
        xinf = sp.limit(s * X, s, 0)
        st = f"Find $x(0^+)$ and $x(\\infty)$ for $X(s) = {tex(X)}$ without inverting the transform."
        steps = [('Initial value theorem', f"$x(0^+) = \\lim_{{s\\to\\infty}} sX(s) = \\lim \\dfrac{{{c}s + {d}}}{{(s + {a})(s + {b})}} = {tex(x0)}$."),
                 ('Is the final value theorem valid?', f"$sX(s)$ has poles at $-{a}$ and $-{b}$, both in the left half-plane, so yes."),
                 ('Final value theorem', f"$x(\\infty) = \\lim_{{s\\to0}} sX(s) = \\dfrac{{{d}}}{{{a*b}}} = {tex(xinf)}$.")]
        ans = f"$x(0^+) = {tex(x0)}$, $x(\\infty) = {tex(xinf)}$."
    elif case == 'unstable':
        a = rng.choice([1, 2, 3])
        X = 1 / (s * (s - a))
        st = f"A student applies the final value theorem to $X(s) = {tex(X)}$ and obtains $-{tex(Q(1, a))}$. Explain the error."
        steps = [('Check the conditions', f"$sX(s) = 1/(s - {a})$ has a pole at $s = {a}$, in the right half-plane."),
                 ('Consequence', f"The theorem does not apply. Inverting gives $x(t) = \\tfrac{{1}}{{{a}}}(e^{{{a}t}} - 1)$, which grows without bound; there is no final value.")]
        ans = 'The FVT is invalid (pole in the right half-plane); $x(t)$ grows without limit.'
    else:
        w0 = rng.choice([2, 3, 5])
        X = s / (s ** 2 + w0 ** 2)
        st = f"Can the final value theorem be applied to $X(s) = {tex(X)}$?"
        steps = [('Poles of $sX(s)$', f"At $s = \\pm j{w0}$, on the imaginary axis."),
                 ('Conclusion', f"Not valid. The signal is $\\cos({w0}t)$, which oscillates for ever and has no limit. The formula would wrongly give 0.")]
        ans = 'No: poles on the imaginary axis; $x(t) = \\cos(' + str(w0) + 't)$ has no final value.'
    return Prob('B', st, steps, ans, 'Initial and final value theorems')


def derivative_ic(rng):
    p1, p2 = rng.sample([1, 2, 3, 4], 2)
    y0, yd0 = rng.choice([0, 1, 2]), rng.choice([0, 1, -1])
    a1, a0 = p1 + p2, p1 * p2
    c = rng.choice([1, 2, 5])
    st = (f"Transform the equation $y'' + {a1}y' + {a0}y = {c}u(t)$ with $y(0^-) = {y0}$ and $y'(0^-) = {yd0}$, and solve for $Y(s)$. (Do not invert.)")
    Ys = (c / s + (s + a1) * y0 + yd0) / (s ** 2 + a1 * s + a0)
    steps = [('Derivative rules', "$\\mathcal{L}\\{y'\\} = sY - y(0^-)$ and $\\mathcal{L}\\{y''\\} = s^2Y - sy(0^-) - y'(0^-)$."),
             ('Substitute', f"$s^2Y - {y0}s - ({yd0}) + {a1}(sY - {y0}) + {a0}Y = \\dfrac{{{c}}}{{s}}$."),
             ('Collect', f"$(s^2 + {a1}s + {a0})Y = \\dfrac{{{c}}}{{s}} + {y0}s + {a1*y0 + yd0}$."),
             ('Solve', f"$Y(s) = {tex(sp.factor(sp.together(Ys)))}$. The initial conditions appear in the numerator; the characteristic polynomial ${tex(sp.factor(s**2 + a1*s + a0))}$ is the denominator.")]
    return Prob('B', st, steps, f"$Y(s) = {tex(sp.factor(sp.together(Ys)))}$.", 'Derivative property')


def periodic_lt(rng):
    case = cyc(rng, 'pl', ['square', 'saw', 'pulse', 'halfsine'])
    T = rng.choice([1, 2, 4])
    A = rng.choice([1, 2, 3])
    if case == 'square':
        st = f"Find the Laplace transform of the periodic square wave that equals ${A}$ for the first half of each period and $0$ for the second half, with period ${T}$."
        ans = f"\\dfrac{{{A}}}{{s\\left(1 + e^{{-{cf(Q(T,2))}s}}\\right)}}"
        steps = [('Periodic rule', '$X(s) = \\dfrac{X_1(s)}{1 - e^{-sT}}$, where $X_1$ is the transform of one period.'),
                 ('One period', f"$X_1 = \\dfrac{{{A}(1 - e^{{-{cf(Q(T,2))}s}})}}{{s}}$."),
                 ('Simplify', f"$1 - e^{{-{cf(T)}s}} = (1 - e^{{-{cf(Q(T,2))}s}})(1 + e^{{-{cf(Q(T,2))}s}})$, so $X(s) = {ans}$.")]
    elif case == 'saw':
        st = f"Find the Laplace transform of the sawtooth $x(t) = {tex(Q(A, T))}t$ for $0 \\le t < {T}$, repeated with period ${T}$."
        ans = f"{tex(Q(A, T) / s**2)} - \\dfrac{{{cf(A)}e^{{-{cf(T)}s}}}}{{s(1 - e^{{-{cf(T)}s}})}}"
        steps = [('One period', f"$x_1(t) = {tex(Q(A,T))}t[u(t) - u(t - {T})] = {tex(Q(A,T))}r(t) - {tex(Q(A,T))}r(t-{T}) - {A}u(t - {T})$, so $X_1 = {tex(Q(A,T))}\\dfrac{{1 - e^{{-{cf(T)}s}}}}{{s^2}} - \\dfrac{{{A}e^{{-{cf(T)}s}}}}{{s}}$."),
                 ('Periodic rule', f"Divide by $1 - e^{{-{cf(T)}s}}$: $X(s) = {ans}$.")]
    elif case == 'pulse':
        d = rng.choice([Q(1, 4), Q(1, 2)])
        w = T * d
        st = f"Find the Laplace transform of a train of pulses of height ${A}$ and width ${tex(w)}$ starting at $t = 0, {T}, {2*T}, \\dots$"
        ans = f"\\dfrac{{{cf(A)}(1 - e^{{-{cf(w)}s}})}}{{s(1 - e^{{-{cf(T)}s}})}}"
        steps = [('One period', f"$X_1 = {A}(1 - e^{{-{cf(w)}s}})/s$."), ('Periodic rule', f"$X = {ans}$.")]
    else:
        st = f"Find the Laplace transform of the half-wave rectified sine $x(t) = \\sin(\\pi t)$ on $0 \\le t < 1$, zero on $1 \\le t < 2$, repeated with period 2."
        ans = "\\dfrac{\\pi}{(s^2 + \\pi^2)(1 - e^{-s})}"
        steps = [('One period', 'The first half-cycle is $\\sin(\\pi t)u(t) + \\sin(\\pi(t - 1))u(t - 1)$, because the delayed sine cancels the original after $t = 1$. Its transform is $\\dfrac{\\pi(1 + e^{-s})}{s^2 + \\pi^2}$.'),
                 ('Periodic rule', 'Divide by $1 - e^{-2s} = (1 - e^{-s})(1 + e^{-s})$: $X = ' + ans + '$.')]
    return Prob('C', st, steps, f"${ans}$.", 'Periodic signals')


def bilateral(rng):
    a, b = rng.sample([1, 2, 3, 4], 2)
    A = rng.choice([1, 2, 3])
    case = cyc(rng, 'bl', ['dexp', 'mixed', 'mixednone', 'dexp', 'inv'])
    if case == 'dexp':
        st = f"Find the bilateral Laplace transform of $x(t) = {cf(A)}{expo(a, '|t|')}$ and its ROC."
        ans = f"\\dfrac{{{-2*a*A}}}{{(s + {a})(s - {a})}} = \\dfrac{{{2*a*A}}}{{{a*a} - s^2}},\\ -{a} < \\operatorname{{Re}}(s) < {a}"
        steps = [('Split', f"${A}{expo(a)}u(t) + {A}e^{{{a}t}}u(-t)$."), ('Each side', f"$\\dfrac{{{A}}}{{s + {a}}}$ for $\\operatorname{{Re}}(s) > -{a}$; $-\\dfrac{{{A}}}{{s - {a}}}$ for $\\operatorname{{Re}}(s) < {a}$."),
                 ('Combine', f"${ans}$. Setting $s = j\\omega$ recovers the Fourier transform $\\dfrac{{{2*a*A}}}{{{a*a} + \\omega^2}}$ of Chapter 5.")]
    elif case in ('mixed', 'mixednone'):
        a, b = (max(a, b), min(a, b)) if case == 'mixed' else (min(a, b), max(a, b))
        st = f"Find the bilateral Laplace transform and ROC of $x(t) = {cf(A)}{expo(a)}u(t) - e^{{-{b}t}}u(-t)$."
        lo, hi = -a, -b
        if lo < hi:
            ans = f"\\dfrac{{{A}}}{{s + {a}}} + \\dfrac{{1}}{{s + {b}}},\\ -{a} < \\operatorname{{Re}}(s) < -{b}"
            tail = f"The strip $-{a} < \\operatorname{{Re}}(s) < -{b}$ is non-empty, so the transform exists."
        else:
            ans = "\\text{no transform: the ROCs do not overlap}"
            tail = f"We would need $\\operatorname{{Re}}(s) > -{a}$ and $< -{b}$, but $-{a} \\ge -{b}$, so no $s$ works."
        steps = [('Right-sided part', f"$\\dfrac{{{A}}}{{s + {a}}}$, $\\operatorname{{Re}}(s) > -{a}$."), ('Left-sided part', f"$-e^{{-{b}t}}u(-t) \\to \\dfrac{{1}}{{s + {b}}}$, $\\operatorname{{Re}}(s) < -{b}$."), ('Intersect', tail)]
    else:
        st = f"$X(s) = \\dfrac{{1}}{{(s + {min(a,b)})(s - {max(a,b)})}}$. List every possible ROC and the corresponding signal type, and identify the one for which $x(t)$ has a Fourier transform."
        m, M = min(a, b), max(a, b)
        ans = f"$\\operatorname{{Re}}(s) > {M}$ (right-sided), $\\operatorname{{Re}}(s) < -{m}$ (left-sided), $-{m} < \\operatorname{{Re}}(s) < {M}$ (two-sided, the only one with a Fourier transform)"
        steps = [('Poles', f"$s = -{m}$ and $s = {M}$. ROCs are bounded by poles and contain none."),
                 ('Three choices', f"Right of $s = {M}$; left of $s = -{m}$; or the strip between."),
                 ('Fourier transform', 'Only the strip contains the $j\\omega$ axis. That choice gives a two-sided signal: a decaying exponential for $t>0$ and another for $t<0$.')]
    return Prob('C', st, steps, f"${ans}$." if not ans.startswith('$') else ans + '.', 'Bilateral transform')


def tmul(rng):
    case = cyc(rng, 'tm', ['tsin', 'tcos', 't2e', 'int', 'sin2', 'tsin', 'int'])
    w0, a = rng.choice([1, 2, 3, 4]), rng.choice([1, 2, 3])
    if case == 'tsin':
        st = f"Use the property $t\\,x(t) \\leftrightarrow -dX/ds$ to find the transform of $t\\sin({cf(w0)}t)u(t)$."
        ans = f"\\dfrac{{{2*w0}s}}{{(s^2 + {w0*w0})^2}}"
        steps = [('Base', f"$\\sin({w0}t) \\to {w0}(s^2 + {w0*w0})^{{-1}}$."), ('Differentiate', f"$-\\dfrac{{d}}{{ds}}\\left[{w0}(s^2 + {w0*w0})^{{-1}}\\right] = {w0}\\cdot 2s(s^2 + {w0*w0})^{{-2}}$."), ('Result', f"${ans}$. The double pole on the $j\\omega$ axis signals resonance: an amplitude growing like $t$.")]
    elif case == 'tcos':
        st = f"Find the Laplace transform of $t\\cos({cf(w0)}t)u(t)$."
        ans = f"\\dfrac{{s^2 - {w0*w0}}}{{(s^2 + {w0*w0})^2}}"
        steps = [('Base', f"$\\cos({w0}t) \\to s/(s^2 + {w0*w0})$."), ('Differentiate', f"$-\\dfrac{{d}}{{ds}}\\dfrac{{s}}{{s^2 + {w0*w0}}} = -\\dfrac{{(s^2 + {w0*w0}) - 2s^2}}{{(s^2 + {w0*w0})^2}}$."), ('Result', f"${ans}$.")]
    elif case == 't2e':
        st = f"Find the transform of $t^2{expo(a)}u(t)$ by differentiating twice."
        ans = f"\\dfrac{{2}}{{(s + {a})^3}}"
        steps = [('Base', f"${expo(a)} \\to (s + {a})^{{-1}}$."), ('Twice', f"$(-1)^2\\dfrac{{d^2}}{{ds^2}}(s+{a})^{{-1}} = 2(s+{a})^{{-3}}$."), ('Cross-check', 'This agrees with $t^n e^{-at} \\to n!/(s+a)^{n+1}$.')]
    elif case == 'int':
        st = f"Find the Laplace transform of $y(t) = \\int_0^t e^{{-{a}\\tau}}\\cos({w0}\\tau)\\,d\\tau$."
        ans = f"\\dfrac{{s + {a}}}{{s\\left[(s + {a})^2 + {w0*w0}\\right]}}"
        steps = [('Integration property', '$\\int_0^t x(\\tau)d\\tau \\leftrightarrow X(s)/s$.'), ('Integrand', f"$\\dfrac{{s + {a}}}{{(s + {a})^2 + {w0*w0}}}$."), ('Result', f"${ans}$.")]
    else:
        st = f"Find the Laplace transform of $\\sin^2({cf(w0)}t)u(t)$."
        ans = f"\\dfrac{{{2*w0*w0}}}{{s(s^2 + {4*w0*w0})}}"
        steps = [('Identity', f"$\\sin^2\\theta = \\tfrac12(1 - \\cos 2\\theta)$, so $x = \\tfrac12 - \\tfrac12\\cos({2*w0}t)$."), ('Transform', f"$\\dfrac{{1}}{{2s}} - \\dfrac{{s}}{{2(s^2 + {4*w0*w0})}}$."), ('Combine', f"${ans}$.")]
    return Prob('C', st, steps, f"${ans}$.", 'Multiplication and integration')


TEMPLATES = [(basic, 6), (roc_type, 4), (definition, 3),
             (shifting, 6), (piecewise, 5), (ivt_fvt, 6), (derivative_ic, 4),
             (periodic_lt, 4), (bilateral, 5), (tmul, 7)]


def generate():
    return build_set(TEMPLATES, seed=707)


if __name__ == '__main__':
    for i, p in enumerate(generate(), 1):
        print(f'--- 7.{i} [{p.level}] {p.topic}\n{p.statement}\n  ANS: {p.answer}')
