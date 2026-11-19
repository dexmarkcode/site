"""Chapter 3 - Convolution in continuous and discrete time."""
import numpy as np
import sympy as sp
from core import *
import figstyle as fs
import matplotlib.pyplot as plt

CH = 3


def nz(rng, lo=-3, hi=4):
    return rng.choice([v for v in range(lo, hi + 1) if v != 0])


def dt_finite(rng):
    lx = rng.choice([3, 3, 4])
    lh = rng.choice([2, 3])
    x = [nz(rng) for _ in range(lx)]
    h = [nz(rng, -2, 3) for _ in range(lh)]
    sx = rng.choice([0, -1, 0, 1])
    sh = rng.choice([0, 0, -1, 1])
    y = [int(v) for v in np.convolve(x, h)]
    sy = sx + sh
    st = (f"Compute $y[n] = x[n] * h[n]$ for $x[n] = {seq_tex(x, sx)}$ and $h[n] = {seq_tex(h, sh)}$, where the arrow marks $n = 0$.")
    lines = []
    for m in range(len(y)):
        terms = []
        for kk in range(len(x)):
            hh = m - kk
            if 0 <= hh < len(h):
                terms.append(f"({x[kk]})({h[hh]})")
        lines.append(f"y[{m + sy}] &= " + ' + '.join(terms) + f" = {y[m]}")
    steps = [('Start and length', f"$x$ starts at $n = {sx}$ and $h$ at $n = {sh}$, so $y$ starts at $n = {sx} + ({sh}) = {sy}$. "
              f"The lengths are {lx} and {lh}, so $y$ has ${lx} + {lh} - 1 = {len(y)}$ samples."),
             ('Multiply and collect', "Each output sample is the sum of all products $x[k]h[m]$ whose indices add to the same $n$. "
              "This is exactly how you multiply two polynomials, and it is the quickest reliable way to do it by hand:"
              f"$$\\begin{{aligned}} {' \\\\ '.join(lines)} \\end{{aligned}}$$"),
             ('Check with the sum rule', f"The samples of a convolution sum to the product of the separate sums: $({sum(x)})({sum(h)}) = {sum(x) * sum(h)}$, and indeed ${' + '.join(f'({v})' for v in y)} = {sum(y)}$.")]
    return Prob('A', st, steps, f"$y[n] = {seq_tex(y, sy)}$.", 'Discrete convolution')


def conv_impulse(rng):
    kind = cyc(rng, 'ci', ['ct', 'dt', 'ct2', 'dt'])
    if kind == 'ct':
        a = rng.choice([1, 2, 3])
        t0 = rng.choice([-2, 1, 3])
        st = f"Simplify $y(t) = {expo(a)}u(t) * \\delta(t {'-' if t0 > 0 else '+'} {abs(t0)})$."
        ans = f"$y(t) = {expo(a, f'(t {chr(45) if t0 > 0 else chr(43)} {abs(t0)})')}u(t {'-' if t0 > 0 else '+'} {abs(t0)})$"
        steps = [('Shifting property', 'Convolving with $\\delta(t - t_0)$ simply shifts a signal by $t_0$: $x(t) * \\delta(t - t_0) = x(t - t_0)$.'),
                 ('Apply it', f"Replace every $t$ in $x(t)$ by $t {'-' if t0 > 0 else '+'} {abs(t0)}$, including the one inside the step. Forgetting to shift the step is the usual slip.")]
    elif kind == 'ct2':
        c = rng.choice([2, 3, -1])
        st = f"Simplify $y(t) = \\left[u(t) - u(t - 1)\\right] * \\left[\\delta(t + 1) {'+' if c > 0 else '-'} {abs(c)}\\delta(t - 2)\\right]$ and describe the result."
        ans = f"$y(t) = u(t + 1) - u(t) {'+' if c > 0 else '-'} {abs(c)}\\left[u(t - 2) - u(t - 3)\\right]$"
        steps = [('Distribute', 'Convolution distributes over addition, so treat each impulse separately.'),
                 ('Shift each copy', f"$\\delta(t + 1)$ moves the unit pulse to $[-1, 0)$; ${c}\\delta(t - 2)$ places a copy of height ${c}$ on $[2, 3)$."),
                 ('Describe', 'The output is two non-overlapping pulses, a reminder that convolving with a train of impulses places copies of the signal at each impulse.')]
    else:
        x = [nz(rng) for _ in range(3)]
        d = rng.choice([2, 3])
        c = rng.choice([2, -1, 3])
        y = x + [0] * d
        y = [0] * (len(x) + d)
        for i, v in enumerate(x):
            y[i] += v
            y[i + d] += c * v
        st = f"Find $y[n] = x[n] * (\\delta[n] {'+' if c > 0 else '-'} {abs(c)}\\delta[n - {d}])$ for $x[n] = {seq_tex(x, 0)}$."
        ans = f"$y[n] = {seq_tex(y, 0)}$"
        steps = [('Two copies', f"The output is $x[n] {'+' if c > 0 else '-'} {abs(c)}x[n - {d}]$: the original plus a scaled copy delayed by {d}."),
                 ('Add them up', 'Line the copies up sample by sample and add. Where they overlap, the values combine; this is a simple echo.')]
    return Prob('A', st, steps, ans + '.', 'Convolution with impulses')


def support(rng):
    if rng.random() < 0.5:
        a, b = sorted(rng.sample(range(-4, 6), 2))
        c, d = sorted(rng.sample(range(-3, 7), 2))
        st = f"A signal $x(t)$ is non-zero only on ${a} \\le t \\le {b}$ and $h(t)$ only on ${c} \\le t \\le {d}$. Over what interval can $y = x * h$ be non-zero, and how long is it?"
        steps = [('Rule for supports', 'The start of a convolution is the sum of the starts, and the end is the sum of the ends.'),
                 ('Apply', f"Start ${a} + ({c}) = {a + c}$, end ${b} + ({d}) = {b + d}$."),
                 ('Duration', f"Durations add: ${b - a} + {d - c} = {b + d - a - c}$.")]
        ans = f"${a + c} \\le t \\le {b + d}$, duration ${b + d - a - c}$."
    else:
        N1, N2 = rng.choice([4, 5, 8, 10, 16]), rng.choice([3, 6, 7, 12])
        s1, s2 = rng.choice([0, -2, 3]), rng.choice([0, 1, -1])
        st = f"$x[n]$ has {N1} samples starting at $n = {s1}$ and $h[n]$ has {N2} samples starting at $n = {s2}$. Find the first and last indices of $y = x * h$ and its length."
        first, last = s1 + s2, s1 + N1 - 1 + s2 + N2 - 1
        steps = [('Ends', f"$x$ ends at $n = {s1 + N1 - 1}$ and $h$ at $n = {s2 + N2 - 1}$."),
                 ('Add', f"First index ${s1} + ({s2}) = {first}$; last index ${s1 + N1 - 1} + {s2 + N2 - 1} = {last}$."),
                 ('Length', f"$N_1 + N_2 - 1 = {N1 + N2 - 1}$, which matches $last - first + 1$. The minus one is the bit people forget; it matters later when we use the DFT for convolution.")]
        ans = f"From $n = {first}$ to $n = {last}$, length ${N1 + N2 - 1}$."
    return Prob('A', st, steps, ans, 'Support of a convolution')


def dt_geo(rng):
    pool = [Q(1, 2), Q(1, 3), Q(1, 4), Q(2, 3), Q(3, 4), -Q(1, 2), Q(1, 5)]
    if rng.random() < 0.17:
        a = rng.choice(pool)
        st = f"Find $y[n] = \\left({tex(a)}\\right)^n u[n] * \\left({tex(a)}\\right)^n u[n]$."
        steps = [('Write the sum', f"$y[n] = \\sum_k ({tex(a)})^k u[k]\\,({tex(a)})^{{n-k}}u[n-k]$. The steps restrict $0 \\le k \\le n$, so $y[n] = 0$ for $n<0$."),
                 ('Simplify', f"Each term is $({tex(a)})^k({tex(a)})^{{n-k}} = ({tex(a)})^n$, independent of $k$, and there are $n + 1$ of them."),
                 ('Result', f"$y[n] = (n + 1)\\left({tex(a)}\\right)^n u[n]$. The repeated ratio produces the factor $n + 1$, the discrete cousin of $t e^{{-at}}$.")]
        return Prob('B', st, steps, f"$y[n] = (n+1)({tex(a)})^n u[n]$.", 'Geometric sequences')
    a, b = sorted(rng.sample(pool, 2), reverse=True)
    if rng.random() < 0.5:
        a, b = b, a
    st = f"Find a closed form for $y[n] = \\left({tex(a)}\\right)^n u[n] * \\left({tex(b)}\\right)^n u[n]$ and evaluate $y[2]$."
    y2 = sum(a ** k * b ** (2 - k) for k in range(3))
    hi, lo = (a, b) if a > b else (b, a)
    steps = [('Limits from the steps', f"$y[n] = \\sum_{{k=0}}^{{n}} ({tex(a)})^k ({tex(b)})^{{n-k}}$ for $n \\ge 0$, and zero otherwise."),
             ('Factor out the $n$-dependence', f"$y[n] = ({tex(b)})^n \\sum_{{k=0}}^{{n}} \\left(\\dfrac{{{tex(a)}}}{{{tex(b)}}}\\right)^k$, a finite geometric series."),
             ('Sum it', f"$y[n] = ({tex(b)})^n\\,\\dfrac{{1 - (a/b)^{{n+1}}}}{{1 - a/b}} = \\dfrac{{a^{{n+1}} - b^{{n+1}}}}{{a - b}}$ with $a = {tex(a)}$, $b = {tex(b)}$."),
             ('Tidy', f"$y[n] = \\dfrac{{1}}{{{tex(abs(a - b))}}}\\left[\\left({tex(hi)}\\right)^{{n+1}} - \\left({tex(lo)}\\right)^{{n+1}}\\right]u[n]$, written so that the denominator is positive."),
             ('Check at $n = 2$', f"Directly: $b^2 + ab + a^2 = {tex(y2)}$; from the formula: $(a^3 - b^3)/(a - b) = {tex((a**3 - b**3)/(a - b))}$. They agree.")]
    return Prob('B', st, steps, f"$y[n] = \\dfrac{{({tex(hi)})^{{n+1}} - ({tex(lo)})^{{n+1}}}}{{{tex(abs(a - b))}}}u[n]$, $y[2] = {tex(y2)}$.", 'Geometric sequences')


def ct_exp(rng):
    pool = [1, 2, 3, 4, 5, Q(1, 2)]
    A, B = rng.choice([1, 2, 3]), rng.choice([1, 2, 4])
    if rng.random() < 0.17:
        a = rng.choice(pool)
        st = f"Find $y(t) = {cf(A)}{expo(a)}u(t) * {cf(B)}{expo(a)}u(t)$."
        steps = [('Set up', f"$y(t) = {A*B}\\int_0^t {expo(a, '\\tau')}{expo(a, '(t-\\tau)')}\\,d\\tau$ for $t \\ge 0$."),
                 ('Simplify the integrand', f"The exponents add to $-{tex(a)}t$, independent of $\\tau$, so the integral is ${expo(a)}\\int_0^t d\\tau = t{expo(a)}$."),
                 ('Result', f"$y(t) = {cf(A*B)}t{expo(a)}u(t)$: equal time constants produce a factor of $t$.")]
        return Prob('B', st, steps, f"$y(t) = {cf(A*B)}t{expo(a)}u(t)$.", 'Exponential convolution')
    a, b = rng.sample(pool, 2)
    K = sp.Rational(A * B) / (b - a)
    p1, p2 = (a, b) if K > 0 else (b, a)
    st = f"Find $y(t) = {cf(A)}{expo(a)}u(t) * {cf(B)}{expo(b)}u(t)$."
    steps = [('Overlap region', 'Both signals are zero for negative time, so for $t<0$ there is no overlap and $y = 0$. For $t \\ge 0$ the integrand is non-zero for $0 \\le \\tau \\le t$.'),
             ('Integral', f"$y(t) = {A*B}\\int_0^t {expo(a, '\\tau')}{expo(b, '(t - \\tau)')}\\,d\\tau = {A*B}{expo(b)}\\int_0^t e^{{({tex(b - a)})\\tau}}d\\tau$."),
             ('Evaluate', f"$= {A*B}{expo(b)}\\,\\dfrac{{e^{{({tex(b - a)})t}} - 1}}{{{tex(b - a)}}} = {cf(abs(K))}\\left({expo(p1)} - {expo(p2)}\\right)$, arranged so that the bracket is positive for $t>0$."),
             ('Check', 'At $t = 0$ the result is zero, as it must be for two signals that start with finite values; and it decays to zero as $t \\to \\infty$.')]
    return Prob('B', st, steps, f"$y(t) = {cf(abs(K))}\\left({expo(p1)} - {expo(p2)}\\right)u(t)$.", 'Exponential convolution')


def step_conv(rng):
    a = cyc(rng, 'scv', [1, 2, 3, 4, Q(1, 2), 5])
    d = rng.choice([0, 1, 2, 3])
    A = rng.choice([1, 2, 3, 4])
    sh = f'(t - {d})' if d else 't'
    us = f'u(t - {d})' if d else 'u(t)'
    st = f"Find $y(t) = {cf(A)}{us} * {expo(a)}u(t)$."
    steps = [('Integrating effect of a step', 'Convolving with $u(t)$ integrates: $x(t) * u(t) = \\int_{-\\infty}^{t}x(\\tau)\\,d\\tau$.'),
             ('Integrate', f"$\\int_0^t {expo(a, '\\tau')}d\\tau = {tex(1/sp.nsimplify(a))}(1 - {expo(a)})$ for $t \\ge 0$."),
             ('Scale and shift', f"Multiply by ${A}$" + (f" and replace $t$ by $t - {d}$ because the step is delayed." if d else '.'))]
    ans = f"$y(t) = {cf(A / sp.nsimplify(a))}\\left(1 - {expo(a, sh)}\\right){us}$."
    return Prob('B', st, steps, ans, 'Convolution with a step')


def dt_value(rng):
    a = cyc(rng, 'dv', [Q(1, 2), Q(1, 3), Q(2, 3), -Q(1, 2)])
    N0 = rng.choice([3, 4, 5])
    n0 = rng.choice([2, 4, 6, 7])
    st = f"Let $x[n] = \\left({tex(a)}\\right)^n u[n]$ and $h[n] = u[n] - u[n - {N0}]$. Find $y[{n0}]$ where $y = x * h$, and give the general expression for $n \\ge {N0 - 1}$."
    lo = max(0, n0 - N0 + 1)
    val = sum(a ** kk for kk in range(lo, n0 + 1))
    steps = [('Interpret $h$', f"$h$ is a run of {N0} ones, so $y[n]$ is the sum of the latest {N0} samples of $x$: $y[n] = \\sum_{{k=n-{N0-1}}}^{{n}} x[k]$."),
             ('Evaluate at $n = ' + str(n0) + '$', f"Only $k \\ge 0$ contributes, so $y[{n0}] = \\sum_{{k={lo}}}^{{{n0}}}({tex(a)})^k = " + ' + '.join(tex(a ** kk) for kk in range(lo, n0 + 1)) + f" = {tex(val)}$."),
             ('General form', f"For $n \\ge {N0 - 1}$ the whole window lies in $k \\ge 0$: $y[n] = ({tex(a)})^{{n-{N0-1}}}\\,\\dfrac{{1 - ({tex(a)})^{{{N0}}}}}{{1 - {par(a)}}}$.")]
    return Prob('B', st, steps, f"$y[{n0}] = {tex(val)}$; for $n \\ge {N0-1}$, $y[n] = ({tex(a)})^{{n-{N0-1}}}\\,\\dfrac{{1 - ({tex(a)})^{{{N0}}}}}{{1 - {par(a)}}}$.", 'Moving sum')


def rect_rect(rng):
    A, B = rng.choice([1, 2, 3]), rng.choice([1, 2, 4])
    T1, T2 = sorted([rng.choice([1, 2, 3]), rng.choice([2, 3, 4])])
    if rng.random() < 0.3:
        T2 = T1
    P = A * B
    st = (f"Let $x(t) = {cf(A)}[u(t) - u(t - {T1})]$ and $h(t) = {cf(B)}[u(t) - u(t - {T2})]$. Use the flip-and-slide method to find $y = x * h$ and sketch it.")
    if T1 == T2:
        pieces = f"y(t) = \\begin{{cases}} {P}t, & 0 \\le t < {T1} \\\\ {P}({2*T1} - t), & {T1} \\le t < {2*T1} \\\\ 0, & \\text{{otherwise}} \\end{{cases}}"
    else:
        pieces = (f"y(t) = \\begin{{cases}} {cf(P)}t, & 0 \\le t < {T1} \\\\ {P*T1}, & {T1} \\le t < {T2} \\\\ {cf(P)}({T1 + T2} - t), & {T2} \\le t < {T1 + T2} \\\\ 0, & \\text{{otherwise}} \\end{{cases}}")
    tt = np.linspace(-1, T1 + T2 + 1, 600)
    yy = np.convolve((tt >= 0) & (tt < T1), (tt >= 0) & (tt < T2))
    xs = np.array([-1, 0, T1, T2, T1 + T2, T1 + T2 + 1], float)
    ys = np.array([0, 0, P * T1, P * T1, 0, 0], float)
    fig, ax = plt.subplots(figsize=(4.2, 1.9))
    ax.plot(xs, ys, color=fs.RUST)
    ax.set_xticks([0, T1, T2, T1 + T2]); ax.set_title('$y(t)$', loc='left'); ax.set_xlabel('$t$', loc='right')
    ax.set_ylim(-0.4, P * T1 * 1.25)
    path = save_fig(fig, new_fig_name('ch03_rr'))
    steps = [('Flip and slide', f"Keep $h$ fixed and slide the reversed pulse $x(t - \\tau)$, which occupies $t - {T1} < \\tau \\le t$, across it. The output at each $t$ is ${P}$ times the length of the overlap."),
             ('No overlap', 'For $t < 0$ the sliding pulse has not reached $h$, so $y = 0$.'),
             ('Partial overlap (entry)', f"For $0 \\le t < {T1}$ the overlap is $[0, t]$, of length $t$, so $y = {P}t$."),
             ('Full overlap' if T1 != T2 else 'Partial overlap (exit)', (f"For ${T1} \\le t < {T2}$ the short pulse lies entirely inside the long one, so the overlap is ${T1}$ and $y = {P*T1}$." if T1 != T2 else
               f"For ${T1} \\le t < {2*T1}$ the overlap shrinks as $[t - {T1}, {T1}]$, of length ${2*T1} - t$.")),
             ('Assemble', f"$${pieces}$$ The result is a {'triangle' if T1 == T2 else 'trapezoid'}; its total area is $({A}\\cdot{T1})({B}\\cdot{T2}) = {A*T1*B*T2}$, the product of the areas, which is a good check.")]
    if T1 != T2:
        steps.insert(4, ('Exit', f"For ${T2} \\le t < {T1 + T2}$ the overlap is $[t - {T1}, {T2}]$, of length ${T1 + T2} - t$."))
    return Prob('C', st, steps, f"$${pieces}$$", 'Graphical convolution', sol_fig=(path, 'The convolution of the two pulses.'))


def exp_pulse(rng):
    a = cyc(rng, 'ep', [1, 2, 3, Q(1, 2), 4])
    T = rng.choice([1, 2, 3])
    A = rng.choice([1, 2, 5])
    ia = 1 / sp.nsimplify(a)
    st = f"An RC-type system has $h(t) = {expo(a)}u(t)$. Find its response to the pulse $x(t) = {cf(A)}[u(t) - u(t - {T})]$."
    K = A * ia
    steps = [('Two regions', f"Because $x$ switches on at $0$ and off at ${T}$, we need separate expressions for $0 \\le t < {T}$ and $t \\ge {T}$."),
             ('While the pulse is on', f"$y(t) = {A}\\int_0^t {expo(a, '(t - \\tau)')}d\\tau = {cf(K)}(1 - {expo(a)})$."),
             ('After it switches off', f"The integral runs only up to ${T}$: $y(t) = {A}\\int_0^{{{T}}} {expo(a, '(t - \\tau)')}d\\tau = {cf(K)}\\left(e^{{{tex(a*T)}}} - 1\\right){expo(a)}$."),
             ('Alternative route', f"Write $x(t) = {A}u(t) - {A}u(t - {T})$ and subtract the delayed step response: $y(t) = {cf(K)}(1 - {expo(a)})u(t) - {cf(K)}(1 - {expo(a, f'(t - {T})')})u(t - {T})$, which reproduces both pieces."),
             ('Peak value', f"The output peaks when the pulse ends: $y({T}) = {tex(K)}(1 - e^{{-{tex(a*T)}}}) \\approx {dec(K * (1 - sp.exp(-a * T)))}$.")]
    ans = f"$y(t) = {cf(K)}(1 - {expo(a)})$ for $0 \\le t < {T}$, $y(t) = {cf(K)}(e^{{{tex(a*T)}}} - 1){expo(a)}$ for $t \\ge {T}$, and $0$ for $t < 0$."
    return Prob('C', st, steps, ans, 'Pulse response')


def deconv(rng):
    h = [1, rng.choice([-2, -1, 1, 2, 3])]
    if rng.random() < 0.5:
        h = [rng.choice([1, 2]), rng.choice([-1, 1, 3])]
    x = [nz(rng, -3, 3) for _ in range(3)]
    y = [int(v) for v in np.convolve(x, h)]
    st = (f"An LTI system with $h[n] = {seq_tex(h, 0)}$ produces the output $y[n] = {seq_tex(y, 0)}$. Find the input $x[n]$, assuming it starts at $n = 0$.")
    steps = [('Write the convolution as a recursion', f"$y[n] = {h[0]}x[n] {'+' if h[1] > 0 else '-'} {abs(h[1])}x[n - 1]$, so $x[n] = \\dfrac{{y[n] {'-' if h[1] > 0 else '+'} {abs(h[1])}x[n - 1]}}{{{h[0]}}}$.")]
    xs = []
    prev = 0
    for m in range(len(y)):
        val = sp.Rational(y[m] - h[1] * prev, h[0])
        if m < 3:
            steps.append((f'$n = {m}$', f"$x[{m}] = ({y[m]} - ({h[1]})({tex(prev)}))/{h[0]} = {tex(val)}$."))
        prev = val
        xs.append(val)
    steps.append(('Confirm the end', f"At $n = 3$ the recursion gives $x[3] = {tex(xs[3])}$, so the input really has stopped. Convolving the result with $h$ reproduces $y$."))
    return Prob('C', st, steps, f"$x[n] = {seq_tex(x, 0)}$.", 'Deconvolution')


TEMPLATES = [(dt_finite, 6), (conv_impulse, 4), (support, 4),
             (dt_geo, 6), (ct_exp, 6), (step_conv, 4), (dt_value, 4),
             (rect_rect, 5), (exp_pulse, 5), (deconv, 6)]


def generate():
    return build_set(TEMPLATES, seed=303)


if __name__ == '__main__':
    for i, p in enumerate(generate(), 1):
        print(f'--- 3.{i} [{p.level}] {p.topic}\n{p.statement}\n  ANS: {p.answer}')
