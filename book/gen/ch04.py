"""Chapter 4 - Continuous-time Fourier series."""
import sympy as sp
from core import *

CH = 4


def w0txt(w0):
    return tex(w0)


def ak_list(d):
    """d: {k: value} -> '$a_k = ...$' list."""
    return ', '.join(f"$a_{{{k}}} = {tex(sp.nsimplify(v))}$" for k, v in sorted(d.items()))


def inspection(rng):
    w0 = cyc(rng, 'iw', [pi, 2 * pi, 1, 2, 4 * pi, 100 * pi])
    A = rng.choice([0, 1, 2, 3, -1])
    B = rng.choice([2, 4, 6])
    C = rng.choice([2, 3, 4, -2])
    k1, k2 = rng.sample([1, 2, 3, 4], 2)
    phi = rng.choice([0, 0, pi / 4, pi / 3, -pi / 6])
    d = {}
    if A:
        d[0] = A
    d[k1] = B * sp.exp(j * phi) / 2
    d[-k1] = B * sp.exp(-j * phi) / 2
    d[k2] = d.get(k2, 0) + C / (2 * j)
    d[-k2] = d.get(-k2, 0) - C / (2 * j)
    arg1 = f"{cf(k1 * w0)}t" + ('' if phi == 0 else f" {'+' if phi > 0 else '-'} {tex(abs(phi))}")
    xs = (f"{A} + " if A else '') + f"{B}\\cos({arg1}) {'+' if C > 0 else '-'} {abs(C)}\\sin({cf(k2*w0)}t)"
    st = f"Find the Fourier series coefficients of $x(t) = {xs}$ by inspection, taking the fundamental frequency to be $\\omega_0 = {tex(w0)}$ rad/s."
    steps = [('Use Euler, not integrals', 'When a signal is already a sum of sinusoids, rewriting each one with Euler\'s formula gives the coefficients directly. No integration is needed.'),
             ('Cosine term', f"${B}\\cos(\\theta) = \\tfrac{{{B}}}{{2}}e^{{j\\theta}} + \\tfrac{{{B}}}{{2}}e^{{-j\\theta}}$ with $\\theta = {k1}\\omega_0 t" + ('' if phi == 0 else f" {'+' if phi > 0 else '-'} {tex(abs(phi))}") + "$" +
              (f", so the phase rides along as $e^{{\\pm j{tex(abs(phi))}}}$." if phi != 0 else '.') + f" This gives $a_{{\\pm{k1}}}$."),
             ('Sine term', f"${C}\\sin\\theta = \\dfrac{{{C}}}{{2j}}e^{{j\\theta}} - \\dfrac{{{C}}}{{2j}}e^{{-j\\theta}}$, and $\\dfrac{{1}}{{2j}} = -\\dfrac{{j}}{{2}}$. This gives $a_{{\\pm{k2}}}$."),
             ('Collect', ak_list(d) + '; all other coefficients are zero.'),
             ('Check symmetry', 'For a real signal $a_{-k} = a_k^*$. Every pair above satisfies this.')]
    return Prob('A', st, steps, ak_list(d) + '; all others zero.', 'Coefficients by inspection')


def synthesis(rng):
    w0 = cyc(rng, 'sw', [pi, 2, 2 * pi, 3])
    a0 = rng.choice([0, 1, 2, -1])
    r1 = rng.choice([1, 2, 3])
    t1 = rng.choice([0, pi / 2, -pi / 2, pi / 4, pi / 3])
    r2 = rng.choice([Q(1, 2), 1, 2])
    t2 = rng.choice([0, pi, -pi / 3, pi / 2])
    a1 = sp.nsimplify(r1 * sp.exp(j * t1))
    a2 = sp.nsimplify(r2 * sp.exp(j * t2))
    st = (f"A real periodic signal with $\\omega_0 = {tex(w0)}$ rad/s has non-zero Fourier coefficients $a_0 = {a0}$, "
          f"$a_{{1}} = {tex(sp.expand_complex(a1))}$, $a_{{2}} = {tex(sp.expand_complex(a2))}$, together with $a_{{-1}}$ and $a_{{-2}}$. Write $x(t)$ as a sum of real cosines.")
    def piece(r, th, kk):
        ph = '' if th == 0 else (f" {'+' if th > 0 else '-'} {tex(abs(th))}")
        return f"{cf(2*r)}\\cos({cf(kk*w0)}t{ph})"
    xs = (f"{a0} + " if a0 else '') + piece(r1, t1, 1) + ' + ' + piece(r2, t2, 2)
    steps = [('Fill in the negative indices', f"A real signal has $a_{{-k}} = a_k^*$, so $a_{{-1}} = {tex(sp.expand_complex(sp.conjugate(a1)))}$ and $a_{{-2}} = {tex(sp.expand_complex(sp.conjugate(a2)))}$."),
             ('Pair the terms', 'Each pair combines as $a_k e^{jk\\omega_0 t} + a_k^* e^{-jk\\omega_0 t} = 2|a_k|\\cos(k\\omega_0 t + \\angle a_k)$.'),
             ('Polar form', f"$|a_1| = {tex(r1)}$, $\\angle a_1 = {tex(t1)}$; $|a_2| = {tex(r2)}$, $\\angle a_2 = {tex(t2)}$."),
             ('Assemble', f"$x(t) = {xs}$.")]
    return Prob('A', st, steps, f"$x(t) = {xs}$.", 'Synthesis')


def dc_value(rng):
    case = cyc(rng, 'dc', ['pulse', 'half', 'full', 'saw', 'pulse'])
    A = rng.choice([2, 3, 5, 10, 12])
    if case == 'pulse':
        d = rng.choice([Q(1, 4), Q(1, 3), Q(1, 5), Q(2, 5)])
        st = f"Find $a_0$ for a rectangular pulse train of height ${A}$ and duty cycle ${tex(d)}$."
        v = A * d
        steps = [('Meaning of $a_0$', '$a_0 = \\frac{1}{T}\\int_T x(t)\\,dt$ is simply the average value over a period.'),
                 ('Average', f"The signal is ${A}$ for a fraction ${tex(d)}$ of the period, so $a_0 = {tex(v)}$.")]
    elif case == 'half':
        st = f"Find the DC value $a_0$ of a half-wave rectified sine of peak ${A}$."
        v = A / pi
        steps = [('Average over a period', f"$a_0 = \\frac{{1}}{{T}}\\int_0^{{T/2}}{A}\\sin(\\omega_0 t)\\,dt$, and the positive half contributes area ${A}\\cdot 2/\\omega_0 = {A}T/\\pi$."),
                 ('Result', f"$a_0 = {A}/\\pi \\approx {dec(v)}$.")]
    elif case == 'full':
        st = f"Find the DC value $a_0$ of a full-wave rectified sine of peak ${A}$."
        v = 2 * A / pi
        steps = [('Average', f"Every half-cycle now contributes, so the average doubles compared with half-wave rectification: $a_0 = 2\\cdot{A}/\\pi$."),
                 ('Result', f"$a_0 \\approx {dec(v)}$. This is why full-wave rectifiers are preferred in power supplies.")]
    else:
        st = f"A sawtooth rises linearly from $0$ to ${A}$ in each period. Find $a_0$."
        v = Q(A, 2)
        steps = [('Average of a ramp', f"The average of a straight line over an interval is the mean of its end values: $(0 + {A})/2$."),
                 ('Result', f"$a_0 = {tex(v)}$.")]
    return Prob('A', st, steps, f"$a_0 = {tex(v)}" + ('' if sp.nsimplify(v).is_Rational else f" \\approx {dec(v)}") + '$.', 'DC value')


def pulse_train(rng):
    A = rng.choice([1, 2, 3, 4])
    T, tw = cyc(rng, 'pt', [(2, 1), (4, 1), (3, 1), (6, 1), (4, 3), (3, 2), (8, 2), (6, 4)])
    st = (f"A periodic pulse train has period $T = {T}$ s and, in the period centred on the origin, $x(t) = {A}$ for $|t| < {tex(Q(tw, 2))}$ and $0$ elsewhere. "
          "Find a general expression for $a_k$ and evaluate $a_0$, $a_1$, $a_2$ and $a_3$.")
    w0 = 2 * pi / T
    def ak(kk):
        if kk == 0:
            return Q(A * tw, T)
        return sp.nsimplify(A * sp.sin(kk * pi * Q(tw, T)) / (kk * pi))
    vals = {kk: ak(kk) for kk in range(4)}
    steps = [('Fundamental frequency', f"$\\omega_0 = 2\\pi/{T} = {tex(w0)}$ rad/s."),
             ('Set up the integral', f"$a_k = \\dfrac{{1}}{{{T}}}\\int_{{-{tex(Q(tw,2))}}}^{{{tex(Q(tw,2))}}} {A}e^{{-jk\\omega_0 t}}dt$."),
             ('Integrate', f"$a_k = \\dfrac{{{A}}}{{{T}}}\\cdot\\dfrac{{2\\sin(k\\omega_0 \\cdot {tex(Q(tw,2))})}}{{k\\omega_0}} = \\dfrac{{{cf(A)}\\sin(k\\pi\\cdot {tex(Q(tw, T))})}}{{k\\pi}}$ for $k \\ne 0$. Being real and even, the signal has real, even coefficients."),
             ('DC term separately', f"$a_0 = {A}\\times{tw}/{T} = {tex(vals[0])}$, the average value. (It is also the limit of the general formula as $k \\to 0$.)"),
             ('Evaluate', ', '.join(f"$a_{kk} = {tex(vals[kk])}" + ('' if vals[kk].is_Rational else f" \\approx {dec(vals[kk])}") + '$' for kk in range(1, 4)) + '.'),
             ('Sinc form', f"Equivalently $a_k = {tex(vals[0])}\\,\\operatorname{{sinc}}(k\\cdot{tex(Q(tw, T))})$ with $\\operatorname{{sinc}}(x) = \\sin(\\pi x)/(\\pi x)$. Coefficients vanish whenever $k\\,{tex(Q(tw, T))}$ is a non-zero integer.")]
    ans = f"$a_k = \\dfrac{{{cf(A)}\\sin(k\\pi\\cdot {tex(Q(tw, T))})}}{{k\\pi}}$; " + ', '.join(f"$a_{kk} = {tex(vals[kk])}$" for kk in range(4)) + '.'
    return Prob('B', st, steps, ans, 'Pulse train')


def sawtooth(rng):
    A = rng.choice([1, 2, 3, 4, 5])
    T = cyc(rng, 'sT', [2, 1, 4, 2 * pi])
    st = (f"The periodic sawtooth $x(t) = {tex(sp.nsimplify(2*A/T))}t$ for $-{tex(sp.nsimplify(T/2))} < t < {tex(sp.nsimplify(T/2))}$, repeated with period ${tex(T)}$, swings between $-{A}$ and ${A}$. Find its Fourier coefficients.")
    steps = [('Observations first', 'The signal is real and odd, so its coefficients are purely imaginary and odd, and $a_0 = 0$.'),
             ('Set up', f"$a_k = \\dfrac{{1}}{{T}}\\int_{{-T/2}}^{{T/2}}\\dfrac{{{2*A}t}}{{T}}e^{{-jk\\omega_0 t}}dt$ with $\\omega_0 T = 2\\pi$."),
             ('Integrate by parts', "With $u = t$ and $dv = e^{-jk\\omega_0 t}dt$, the remaining integral of the exponential over a full period is zero, leaving only the boundary term $\\left[\\dfrac{t\\,e^{-jk\\omega_0 t}}{-jk\\omega_0}\\right]_{-T/2}^{T/2} = \\dfrac{T(-1)^k}{-jk\\omega_0}$, because $e^{\\mp jk\\pi} = (-1)^k$."),
             ('Simplify', f"$a_k = \\dfrac{{{2*A}}}{{T^2}}\\cdot\\dfrac{{jT(-1)^k}}{{k\\omega_0}} = \\dfrac{{{cf(A)}j(-1)^k}}{{\\pi k}}$, independent of the period."),
             ('Trigonometric form', f"Pairing $\\pm k$: $x(t) = \\dfrac{{{2*A}}}{{\\pi}}\\sum_{{k=1}}^{{\\infty}}\\dfrac{{(-1)^{{k+1}}}}{{k}}\\sin(k\\omega_0 t)$. The $1/k$ decay reflects the jump discontinuity.")]
    return Prob('B', st, steps, f"$a_0 = 0$, $a_k = \\dfrac{{{cf(A)}j(-1)^k}}{{\\pi k}}$ for $k \\ne 0$.", 'Sawtooth wave')


def triangle(rng):
    A = rng.choice([1, 2, 3, 5, 8])
    T = cyc(rng, 'tT', [2, 4, 1, 2 * pi])
    st = (f"A symmetric triangular wave has period ${tex(T)}$ s, value ${A}$ at $t = 0$ and $-{A}$ at $t = \\pm {tex(sp.nsimplify(T/2))}$, varying linearly in between. Find its Fourier coefficients and the first three non-zero terms of the cosine series.")
    steps = [('Symmetry', 'The wave is real and even, so the coefficients are real and even. It has zero mean, so $a_0 = 0$.'),
             ('A short cut via the derivative', f"The derivative is a square wave of amplitude $4\\cdot{A}/T$ (slope ${tex(sp.nsimplify(-4*A/T))}$ for $0<t<T/2$). Differentiation multiplies coefficients by $jk\\omega_0$, so if the square wave's coefficients are known, divide by $jk\\omega_0$."),
             ('Carry it out', f"An odd square wave of amplitude $B$ has $b_k = \\dfrac{{2B}}{{j\\pi k}}$ for odd $k$. Here $B = 4\\cdot{A}/T$ with a sign flip, and dividing by $jk\\omega_0 = jk\\,2\\pi/T$ gives $a_k = \\dfrac{{4\\cdot{A}}}{{\\pi^2 k^2}} = \\dfrac{{{4*A}}}{{\\pi^2k^2}}$ for odd $k$, zero for even $k$."),
             ('Cosine series', f"$x(t) = \\dfrac{{{8*A}}}{{\\pi^2}}\\left[\\cos\\omega_0 t + \\tfrac19\\cos 3\\omega_0 t + \\tfrac{{1}}{{25}}\\cos 5\\omega_0 t + \\cdots\\right]$ with $\\omega_0 = {tex(2*pi/T)}$."),
             ('Check', f"At $t = 0$ the series gives $\\dfrac{{{8*A}}}{{\\pi^2}}\\cdot\\dfrac{{\\pi^2}}{{8}} = {A}$, using $\\sum_{{k \\text{{ odd}}}} 1/k^2 = \\pi^2/8$. Correct.")]
    return Prob('B', st, steps, f"$a_k = \\dfrac{{{4*A}}}{{\\pi^2k^2}}$ for odd $k$, $0$ for even $k$ (including $k=0$).", 'Triangle wave')


def parseval(rng):
    case = cyc(rng, 'pv', ['list', 'square', 'list', 'saw', 'list'])
    if case == 'list':
        a0 = rng.choice([0, 1, 2])
        c = [rng.choice([1, 2, 3]) * rng.choice([1, j, -j, (1 + j)]) for _ in range(2)]
        P = a0 ** 2 + 2 * sum(sp.Abs(v) ** 2 for v in c)
        st = f"A real periodic signal has $a_0 = {a0}$, $a_{{\\pm1}} = {tex(c[0])}$ and its conjugate, $a_{{\\pm3}} = {tex(c[1])}$ and its conjugate, and no other coefficients. Find its average power."
        steps = [("Parseval's relation", 'The average power equals the sum of the squared magnitudes of all the coefficients: $P = \\sum_k |a_k|^2$.'),
                 ('Magnitudes', f"$|a_0|^2 = {a0**2}$, $|a_{{\\pm1}}|^2 = {tex(sp.Abs(c[0])**2)}$ each, $|a_{{\\pm3}}|^2 = {tex(sp.Abs(c[1])**2)}$ each."),
                 ('Add, counting both signs', f"$P = {a0**2} + 2({tex(sp.Abs(c[0])**2)}) + 2({tex(sp.Abs(c[1])**2)}) = {tex(P)}$.")]
        ans = f"$P = {tex(P)}$."
    elif case == 'square':
        A = rng.choice([1, 2, 5])
        Nh = rng.choice([1, 3, 5])
        frac = sum(sp.Rational(8, 1) / (pi ** 2 * kk ** 2) for kk in range(1, Nh + 1, 2))
        st = f"An odd square wave switches between $+{A}$ and $-{A}$. What fraction of its power lies in harmonics up to and including the {['', 'first', '', 'third', '', 'fifth'][Nh]}?"
        steps = [('Total power', f"$|x|^2 = {A*A}$ at every instant, so $P = {A*A}$."),
                 ('Coefficients', f"$a_k = \\dfrac{{2\\cdot{A}}}{{j\\pi k}}$ for odd $k$, so $|a_k|^2 = \\dfrac{{4\\cdot{A*A}}}{{\\pi^2k^2}}$."),
                 ('Partial power', f"Counting $\\pm k$, the power in harmonics up to $k = {Nh}$ is $\\sum_{{k \\text{{ odd}} \\le {Nh}}} \\dfrac{{8\\cdot{A*A}}}{{\\pi^2k^2}}$."),
                 ('Fraction', f"Dividing by ${A*A}$: $\\dfrac{{8}}{{\\pi^2}}\\sum 1/k^2 = {dec(frac, 4)}$, i.e. about ${dec(100*frac, 1)}\\%$. The amplitude cancels.")]
        ans = f"About ${dec(100*frac, 1)}\\%$."
    else:
        A = rng.choice([1, 2, 3])
        st = f"Use Parseval's relation with the sawtooth coefficients $a_k = j{A}(-1)^k/(\\pi k)$ to evaluate $\\sum_{{k=1}}^\\infty 1/k^2$, given that the sawtooth's power is ${tex(Q(A*A, 3))}$."
        steps = [('Power from the coefficients', f"$\\sum_{{k \\ne 0}}|a_k|^2 = 2\\sum_{{k=1}}^\\infty \\dfrac{{{A*A}}}{{\\pi^2k^2}}$."),
                 ('Equate', f"$2\\cdot\\dfrac{{{A*A}}}{{\\pi^2}}\\sum 1/k^2 = {tex(Q(A*A, 3))}$, so $\\sum 1/k^2 = \\pi^2/6$."),
                 ('Comment', 'A signals problem has just evaluated a famous sum of pure mathematics. Parseval\'s relation is often used this way.')]
        ans = '$\\sum 1/k^2 = \\pi^2/6$.'
    return Prob('B', st, steps, ans, "Parseval's relation")


def lti_periodic(rng):
    a = cyc(rng, 'lp', [1, 2, 4, 5, 10])
    w0 = rng.choice([1, 2, 3])
    A0 = rng.choice([0, 1, 2])
    B = rng.choice([2, 4])
    C = rng.choice([1, 2, 3])
    st = (f"The signal $x(t) = {str(A0) + ' + ' if A0 else ''}{B}\\cos({cf(w0)}t) + {C}\\cos({3*w0}t)$ is applied to an LTI system with "
          f"$H(j\\omega) = \\dfrac{{{a}}}{{{a} + j\\omega}}$. Find the steady-state output.")
    terms = []
    lines = []
    if A0:
        terms.append(str(A0))
        lines.append(f"DC: $H(0) = 1$, so the constant ${A0}$ passes unchanged.")
    for amp, wk in ((B, w0), (C, 3 * w0)):
        H = sp.Integer(a) / (a + j * wk)
        m = sp.Abs(H)
        ph = sp.arg(H)
        lines.append(f"$\\omega = {wk}$: $H = \\dfrac{{{a}}}{{{a} + j{wk}}}$, $|H| = \\dfrac{{{a}}}{{\\sqrt{{{a*a + wk*wk}}}}} \\approx {dec(m, 4)}$, $\\angle H = -\\tan^{{-1}}({wk}/{a}) \\approx {dec(ph, 4)}$ rad.")
        terms.append(f"{dec(amp*m, 4)}\\cos({cf(wk)}t - {dec(-ph, 4)})")
    steps = [('Each harmonic passes independently', 'An LTI system multiplies each coefficient by $H(jk\\omega_0)$. For real cosines this means scaling by $|H|$ and shifting by $\\angle H$ at that frequency.')]
    steps += [(f'Harmonic {i+1}', l) for i, l in enumerate(lines)]
    steps.append(('Assemble', f"$y(t) \\approx {' + '.join(terms)}$."))
    steps.append(('Interpretation', 'This is a low-pass filter: the higher harmonic is attenuated more and delayed by a larger phase, so the waveform shape changes even though no new frequencies appear.'))
    return Prob('B', st, steps, f"$y(t) \\approx {' + '.join(terms)}$.", 'Periodic input to an LTI system')


def properties(rng):
    case = cyc(rng, 'pr', ['shift', 'deriv', 'reverse', 'mod', 'scale'])
    st0 = "A periodic signal $x(t)$ with fundamental frequency $\\omega_0$ has Fourier coefficients $a_k$."
    if case == 'shift':
        t0 = rng.choice([1, 2, Q(1, 2)])
        st = st0 + f" Find the coefficients of $y(t) = x(t - {tex(t0)})$, and show that $|b_k| = |a_k|$."
        steps = [('Substitute', f"$y(t) = \\sum a_k e^{{jk\\omega_0(t - {tex(t0)})}} = \\sum \\left(a_k e^{{-jk\\omega_0 {tex(t0)}}}\\right)e^{{jk\\omega_0 t}}$."),
                 ('Read off', f"$b_k = a_k e^{{-j{tex(t0)}k\\omega_0}}$. The factor has unit magnitude, so a shift changes only the phases.")]
        ans = f"$b_k = a_k e^{{-j{tex(t0)}k\\omega_0}}$."
    elif case == 'deriv':
        st = st0 + " Find the coefficients of $y(t) = dx/dt$ and explain why $b_0 = 0$."
        steps = [('Differentiate term by term', '$\\dfrac{d}{dt}e^{jk\\omega_0 t} = jk\\omega_0 e^{jk\\omega_0 t}$.'),
                 ('Read off', '$b_k = jk\\omega_0 a_k$. In particular $b_0 = 0$: the derivative of a periodic signal has zero average, because $x$ returns to its starting value each period.')]
        ans = '$b_k = jk\\omega_0 a_k$.'
    elif case == 'reverse':
        st = st0 + " Find the coefficients of $y(t) = x(-t)$, and deduce what is true of $a_k$ when $x$ is real and even."
        steps = [('Substitute', '$y(t) = \\sum a_k e^{-jk\\omega_0 t} = \\sum a_{-m}e^{jm\\omega_0 t}$ with $m = -k$.'),
                 ('Read off', '$b_k = a_{-k}$.'),
                 ('Even real signals', 'If $x$ is even, $a_k = a_{-k}$; if it is also real, $a_{-k} = a_k^*$. Together these force $a_k$ to be real and even.')]
        ans = '$b_k = a_{-k}$; real and even signals have real, even coefficients.'
    elif case == 'mod':
        M = rng.choice([1, 2, 3])
        st = st0 + f" Find the coefficients of $y(t) = x(t)\\cos({M}\\omega_0 t)$."
        steps = [('Write the cosine with Euler', f"$\\cos({M}\\omega_0 t) = \\tfrac12 e^{{j{M}\\omega_0 t}} + \\tfrac12 e^{{-j{M}\\omega_0 t}}$."),
                 ('Multiplication by $e^{jM\\omega_0 t}$ shifts indices', f"$x(t)e^{{j{M}\\omega_0 t}}$ has coefficients $a_{{k-{M}}}$."),
                 ('Combine', f"$b_k = \\tfrac12\\left(a_{{k-{M}}} + a_{{k+{M}}}\\right)$. The spectrum is copied up and down by ${M}$ harmonics, the Fourier-series form of amplitude modulation.")]
        ans = f"$b_k = \\tfrac12(a_{{k-{M}}} + a_{{k+{M}}})$."
    else:
        c = rng.choice([2, 3])
        st = st0 + f" What are the coefficients and fundamental frequency of $y(t) = x({c}t)$?"
        steps = [('Substitute', f"$y(t) = \\sum a_k e^{{jk({c}\\omega_0)t}}$."),
                 ('Interpret', f"The coefficients are unchanged, $b_k = a_k$, but the fundamental frequency is now ${c}\\omega_0$. Compressing time stretches the spacing of the harmonics.")]
        ans = f"$b_k = a_k$, with fundamental ${c}\\omega_0$."
    return Prob('C', st, steps, ans, 'Fourier series properties')


def full_wave(rng):
    A = rng.choice([1, 2, 5, 10])
    w1 = cyc(rng, 'fw', [1, 2, 100 * pi, 120 * pi])
    st = f"Find the complex Fourier series of the full-wave rectified sine $x(t) = {cf(A)}|\\sin({cf(w1)}t)|$."
    T = pi / w1
    steps = [('Period and fundamental', f"Rectification halves the period: $T = \\pi/{tex(w1)} = {tex(T)}$, so $\\omega_0 = 2\\cdot{tex(w1)} = {tex(2*w1)}$ rad/s."),
             ('Set up', f"Over one period $x(t) = {A}\\sin({cf(w1)}t)$ for $0 < t < {tex(T)}$, so $a_k = \\dfrac{{1}}{{T}}\\int_0^T {A}\\sin(\\omega_1 t)e^{{-jk\\omega_0 t}}dt$ with $\\omega_1 = {tex(w1)}$."),
             ('Change variable', 'With $\\theta = \\omega_1 t$, $a_k = \\dfrac{A}{\\pi}\\int_0^\\pi \\sin\\theta\\, e^{-j2k\\theta}d\\theta$.'),
             ('Evaluate', 'Writing $\\sin\\theta = (e^{j\\theta} - e^{-j\\theta})/2j$ and integrating each exponential, using $e^{-j2k\\pi} = 1$ and $e^{\\pm j\\pi} = -1$, gives $\\int_0^\\pi \\sin\\theta\\,e^{-j2k\\theta}d\\theta = \\dfrac{2}{1 - 4k^2}$.'),
             ('Result', f"$a_k = \\dfrac{{{2*A}}}{{\\pi(1 - 4k^2)}}$, real and even. Check: $a_0 = {2*A}/\\pi$, the known DC value.")]
    return Prob('C', st, steps, f"$a_k = \\dfrac{{{2*A}}}{{\\pi(1 - 4k^2)}}$, with $\\omega_0 = {tex(2*w1)}$.", 'Rectified sine')


def filtered_square(rng):
    A = rng.choice([1, 2, 4])
    f0 = cyc(rng, 'fs', [50, 100, 1000, 200])
    fc = f0 * rng.choice([2, 4, 6])
    kept = [kk for kk in range(1, 20, 2) if kk * f0 < fc]
    terms = ' + '.join(f"\\tfrac{{1}}{{{kk}}}\\sin({2*kk*f0}\\pi t)" if kk > 1 else f"\\sin({2*f0}\\pi t)" for kk in kept)
    frac = sum(sp.Rational(8) / (pi ** 2 * kk ** 2) for kk in kept)
    st = (f"A square wave switching between $\\pm{A}$ at ${f0}$ Hz (odd symmetry) passes through an ideal low-pass filter with unity gain below ${fc}$ Hz and zero gain above. Write down the output and the fraction of the input power that survives.")
    steps = [('Spectrum of the square wave', f"$x(t) = \\dfrac{{{4*A}}}{{\\pi}}\\sum_{{k\\text{{ odd}}}}\\dfrac{{1}}{{k}}\\sin(2\\pi k\\cdot{f0}\\,t)$. Only odd harmonics are present."),
             ('Which harmonics pass', f"Harmonics lie at ${f0}k$ Hz. Those below ${fc}$ Hz are $k = {', '.join(map(str, kept))}$."),
             ('Output', f"$y(t) = \\dfrac{{{4*A}}}{{\\pi}}\\left[{terms}\\right]$."),
             ('Power', f"Input power ${A*A}$. Output power ${A*A}\\cdot\\dfrac{{8}}{{\\pi^2}}\\sum_{{k \\in \\{{{', '.join(map(str, kept))}\\}}}}\\dfrac{{1}}{{k^2}}$, a fraction $\\approx {dec(frac, 4)}$.")]
    return Prob('C', st, steps, f"$y(t) = \\dfrac{{{4*A}}}{{\\pi}}[{terms}]$; about ${dec(100*frac, 1)}\\%$ of the power.", 'Filtering a square wave')


TEMPLATES = [(inspection, 6), (synthesis, 4), (dc_value, 3),
             (pulse_train, 6), (sawtooth, 4), (triangle, 4), (parseval, 5), (lti_periodic, 6),
             (properties, 5), (full_wave, 3), (filtered_square, 4)]


def generate():
    return build_set(TEMPLATES, seed=404)


if __name__ == '__main__':
    for i, p in enumerate(generate(), 1):
        print(f'--- 4.{i} [{p.level}] {p.topic}\n{p.statement}\n  ANS: {p.answer}')
