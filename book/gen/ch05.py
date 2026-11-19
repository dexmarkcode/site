"""Chapter 5 - The continuous-time Fourier transform."""
import sympy as sp
from core import *

CH = 5
jw = r'j\omega'


def jwp(a):
    """(a + j omega) text."""
    return f"({tex(a)} + j\\omega)"


def basic_pairs(rng):
    case = cyc(rng, 'bp', ['exp', 'rect', 'dexp', 'delta', 'texp', 'dcos'])
    A = rng.choice([1, 2, 3, 4])
    a = rng.choice([1, 2, 3, 5])
    if case == 'exp':
        st = f"Find the Fourier transform of $x(t) = {cf(A)}{expo(a)}u(t)$ from the definition."
        steps = [('Definition', f"$X(j\\omega) = \\int_0^\\infty {A}{expo(a)}e^{{-j\\omega t}}dt = {A}\\int_0^\\infty e^{{-({a} + j\\omega)t}}dt$."),
                 ('Integrate', f"$= {A}\\left[\\dfrac{{e^{{-({a}+j\\omega)t}}}}{{-({a}+j\\omega)}}\\right]_0^\\infty = \\dfrac{{{A}}}{{{a} + j\\omega}}$, since the exponential vanishes at infinity because ${a} > 0$."),
                 ('Magnitude and phase', f"$|X| = {A}/\\sqrt{{{a*a} + \\omega^2}}$ and $\\angle X = -\\tan^{{-1}}(\\omega/{a})$.")]
        ans = f"$X(j\\omega) = \\dfrac{{{A}}}{{{a} + j\\omega}}$."
    elif case == 'rect':
        T = rng.choice([1, 2, 4])
        st = f"Find the Fourier transform of the pulse $x(t) = {A}$ for $|t| < {tex(Q(T, 2))}$, zero otherwise. Where are its first zeros?"
        steps = [('Definition', f"$X(j\\omega) = \\int_{{-{tex(Q(T,2))}}}^{{{tex(Q(T,2))}}} {A}e^{{-j\\omega t}}dt$."),
                 ('Integrate', f"$= {A}\\,\\dfrac{{e^{{-j\\omega {tex(Q(T,2))}}} - e^{{j\\omega {tex(Q(T,2))}}}}}{{-j\\omega}} = \\dfrac{{{2*A}\\sin({tex(Q(T,2))}\\omega)}}{{\\omega}}$."),
                 ('Sinc form', f"$X = {A*T}\\operatorname{{sinc}}\\!\\left(\\dfrac{{{T}\\omega}}{{2\\pi}}\\right)$, real and even because the pulse is real and even. $X(0) = {A*T}$, the area."),
                 ('Zeros', f"$\\sin({tex(Q(T,2))}\\omega) = 0$ first at $\\omega = \\pm 2\\pi/{T} = \\pm{tex(2*pi/T)}$ rad/s. Shorter pulses have wider spectra.")]
        ans = f"$X(j\\omega) = \\dfrac{{{2*A}\\sin({tex(Q(T,2))}\\omega)}}{{\\omega}}$; first zeros at $\\omega = \\pm{tex(2*pi/T)}$."
    elif case == 'dexp':
        st = f"Find the Fourier transform of $x(t) = {cf(A)}{expo(a, '|t|')}$."
        steps = [('Split at the origin', f"$X = {A}\\int_{{-\\infty}}^0 e^{{{a}t}}e^{{-j\\omega t}}dt + {A}\\int_0^\\infty e^{{-{a}t}}e^{{-j\\omega t}}dt$."),
                 ('Each half', f"$= \\dfrac{{{A}}}{{{a} - j\\omega}} + \\dfrac{{{A}}}{{{a} + j\\omega}}$."),
                 ('Combine', f"$= \\dfrac{{{2*a*A}}}{{{a*a} + \\omega^2}}$: real, even and positive, a Lorentzian shape.")]
        ans = f"$X(j\\omega) = \\dfrac{{{2*a*A}}}{{{a*a} + \\omega^2}}$."
    elif case == 'delta':
        t0 = rng.choice([1, 2, 3])
        st = f"Find the Fourier transform of $x(t) = {cf(A)}\\delta(t - {t0}) + \\delta(t + {t0})$ and write it in real form if possible."
        steps = [('Sifting', f"$\\int\\delta(t - t_0)e^{{-j\\omega t}}dt = e^{{-j\\omega t_0}}$."),
                 ('Apply', f"$X = {cf(A)}e^{{-j{cf(t0)}\\omega}} + e^{{j{cf(t0)}\\omega}}$."),
                 ('Real form', (f"With equal weights this is $2\\cos({cf(t0)}\\omega)$." if A == 1 else f"$X = {A+1}\\cos({cf(t0)}\\omega) - {cf(A-1)}j\\sin({cf(t0)}\\omega)$. Unequal weights break the symmetry, so the transform is complex."))]
        ans = f"$X(j\\omega) = {cf(A)}e^{{-j{cf(t0)}\\omega}} + e^{{j{cf(t0)}\\omega}}$" + ('$ = 2\\cos(' + str(t0) + '\\omega)$.' if A == 1 else '.')
        if A == 1:
            ans = f"$X(j\\omega) = 2\\cos({cf(t0)}\\omega)$."
    elif case == 'texp':
        st = f"Find the Fourier transform of $x(t) = {cf(A)}t{expo(a)}u(t)$."
        steps = [('Use a property', 'Rather than integrating by parts, use $t\\,x(t) \\leftrightarrow j\\dfrac{dX}{d\\omega}$.'),
                 ('Base pair', f"${expo(a)}u(t) \\leftrightarrow \\dfrac{{1}}{{{a} + j\\omega}}$."),
                 ('Differentiate', f"$j\\dfrac{{d}}{{d\\omega}}({a} + j\\omega)^{{-1}} = j\\cdot(-1)({a} + j\\omega)^{{-2}}\\cdot j = \\dfrac{{1}}{{({a} + j\\omega)^2}}$."),
                 ('Scale', f"$X(j\\omega) = \\dfrac{{{A}}}{{({a} + j\\omega)^2}}$.")]
        ans = f"$X(j\\omega) = \\dfrac{{{A}}}{{({a} + j\\omega)^2}}$."
    else:
        w0 = rng.choice([2, 3, 4, 10])
        st = f"Find the Fourier transform of the damped cosine $x(t) = {expo(a)}\\cos({w0}t)u(t)$."
        steps = [('Euler', f"$x(t) = \\tfrac12 e^{{-({a} - j{w0})t}}u(t) + \\tfrac12 e^{{-({a} + j{w0})t}}u(t)$."),
                 ('Transform each', f"$X = \\dfrac{{1/2}}{{{a} + j(\\omega - {w0})}} + \\dfrac{{1/2}}{{{a} + j(\\omega + {w0})}}$."),
                 ('Combine', f"$X(j\\omega) = \\dfrac{{{a} + j\\omega}}{{({a} + j\\omega)^2 + {w0*w0}}}$. The magnitude peaks near $\\omega = \\pm{w0}$ with width set by the decay rate ${a}$.")]
        ans = f"$X(j\\omega) = \\dfrac{{{a} + j\\omega}}{{({a} + j\\omega)^2 + {w0*w0}}}$."
    return Prob('A', st, steps, ans, 'Basic transform pairs')


def magphase(rng):
    A = rng.choice([1, 4, 10])
    a = cyc(rng, 'mp', [2, 5, 10, 100, 1000])
    wv = a * rng.choice([1, 2, Q(1, 2), 3])
    st = f"For $X(j\\omega) = \\dfrac{{{A}}}{{{a} + j\\omega}}$, find $|X|$ in decibels relative to $|X(0)|$ and the phase at $\\omega = {tex(wv)}$ rad/s. At what frequency is $|X|$ down by 3 dB?"
    r = wv / a
    dB = -10 * sp.log(1 + r ** 2, 10)
    ph = -sp.atan(r)
    steps = [('Normalise', f"$\\dfrac{{|X(j\\omega)|}}{{|X(0)|}} = \\dfrac{{{a}}}{{\\sqrt{{{a}^2 + \\omega^2}}}} = \\dfrac{{1}}{{\\sqrt{{1 + (\\omega/{a})^2}}}}$."),
             ('Evaluate', f"At $\\omega = {tex(wv)}$, $\\omega/{a} = {tex(r)}$, giving $-10\\log_{{10}}(1 + {tex(r**2)}) \\approx {dec(dB, 2)}$ dB."),
             ('Phase', f"$\\angle X = -\\tan^{{-1}}({tex(r)}) \\approx {dec(ph, 4)}$ rad $= {dec(ph*180/pi, 1)}^\\circ$."),
             ('Half-power point', f"$|X|^2$ halves when $(\\omega/{a})^2 = 1$, i.e. $\\omega = {a}$ rad/s, where the phase is $-45^\\circ$.")]
    return Prob('A', st, steps, f"${dec(dB, 2)}$ dB, phase ${dec(ph*180/pi, 1)}^\\circ$; 3 dB point at $\\omega = {a}$ rad/s.", 'Magnitude and phase')


def props(rng):
    a = cyc(rng, 'pa', [1, 2, 3, 4])
    case = cyc(rng, 'pc', ['shift', 'scale', 'rev', 'tmul', 'deriv', 'exp', 'cos', 'conv'])
    X = f"\\dfrac{{1}}{{{a} + j\\omega}}"
    st0 = f"Given $x(t) = {expo(a)}u(t) \\leftrightarrow X(j\\omega) = {X}$, use properties (not integration) to find the transform of "
    if case == 'shift':
        t0 = rng.choice([1, 2, 3])
        st = st0 + f"$y(t) = x(t - {t0})$."
        ans = f"Y(j\\omega) = \\dfrac{{e^{{-j{t0}\\omega}}}}{{{a} + j\\omega}}"
        steps = [('Time-shift property', '$x(t - t_0) \\leftrightarrow e^{-j\\omega t_0}X(j\\omega)$.'), ('Apply', f"${ans}$. The magnitude is unchanged; the phase gains a linear term $-{t0}\\omega$.")]
    elif case == 'scale':
        c = rng.choice([2, 3])
        st = st0 + f"$y(t) = x({c}t)$."
        ans = f"Y(j\\omega) = \\dfrac{{1}}{{{c}}}\\cdot\\dfrac{{1}}{{{a} + j\\omega/{c}}} = \\dfrac{{1}}{{{a*c} + j\\omega}}"
        steps = [('Scaling property', '$x(ct) \\leftrightarrow \\dfrac{1}{|c|}X\\!\\left(\\dfrac{j\\omega}{c}\\right)$.'), ('Apply and simplify', f"${ans}$."),
                 ('Check directly', f"$x({c}t) = {expo(a*c)}u(t)$, whose transform is indeed $1/({a*c} + j\\omega)$.")]
    elif case == 'rev':
        st = st0 + "$y(t) = x(-t)$."
        ans = f"Y(j\\omega) = \\dfrac{{1}}{{{a} - j\\omega}}"
        steps = [('Reversal', '$x(-t) \\leftrightarrow X(-j\\omega)$.'), ('Apply', f"${ans}$, the transform of the left-sided exponential ${expo(-a)}u(-t)$.")]
    elif case == 'tmul':
        st = st0 + "$y(t) = t\\,x(t)$."
        ans = f"Y(j\\omega) = \\dfrac{{1}}{{({a} + j\\omega)^2}}"
        steps = [('Multiplication by $t$', '$t\\,x(t) \\leftrightarrow j\\,dX/d\\omega$.'), ('Differentiate', f"$j\\cdot\\dfrac{{-j}}{{({a}+j\\omega)^2}} = \\dfrac{{1}}{{({a}+j\\omega)^2}}$.")]
    elif case == 'deriv':
        st = st0 + "$y(t) = dx/dt$, and check your answer by differentiating $x$ directly."
        ans = f"Y(j\\omega) = \\dfrac{{j\\omega}}{{{a} + j\\omega}}"
        steps = [('Differentiation property', '$\\dfrac{dx}{dt} \\leftrightarrow j\\omega X(j\\omega)$.'), ('Apply', f"${ans}$."),
                 ('Direct check', f"$\\dfrac{{dx}}{{dt}} = \\delta(t) - {a}{expo(a)}u(t)$ (the jump at $t=0$ gives the impulse), with transform $1 - \\dfrac{{{a}}}{{{a}+j\\omega}} = \\dfrac{{j\\omega}}{{{a}+j\\omega}}$. Agreed.")]
    elif case == 'exp':
        w0 = rng.choice([2, 5, 10])
        st = st0 + f"$y(t) = x(t)e^{{j{w0}t}}$."
        ans = f"Y(j\\omega) = \\dfrac{{1}}{{{a} + j(\\omega - {w0})}}"
        steps = [('Frequency shift', '$x(t)e^{j\\omega_0 t} \\leftrightarrow X(j(\\omega - \\omega_0))$.'), ('Apply', f"${ans}$: the whole spectrum slides up by ${w0}$ rad/s.")]
    elif case == 'cos':
        w0 = rng.choice([5, 10, 20])
        st = st0 + f"$y(t) = x(t)\\cos({w0}t)$."
        ans = f"Y(j\\omega) = \\dfrac{{1/2}}{{{a} + j(\\omega - {w0})}} + \\dfrac{{1/2}}{{{a} + j(\\omega + {w0})}}"
        steps = [('Modulation', '$x(t)\\cos\\omega_0 t \\leftrightarrow \\tfrac12 X(j(\\omega - \\omega_0)) + \\tfrac12 X(j(\\omega + \\omega_0))$.'), ('Apply', f"${ans}$.")]
    else:
        st = st0 + "$y(t) = x(t) * x(t)$, and identify $y(t)$."
        ans = f"Y(j\\omega) = \\dfrac{{1}}{{({a} + j\\omega)^2}}"
        steps = [('Convolution property', 'Convolution in time is multiplication in frequency.'), ('Apply', f"$Y = X^2 = \\dfrac{{1}}{{({a}+j\\omega)^2}}$."),
                 ('Identify', f"This is the transform of $t{expo(a)}u(t)$, agreeing with the direct convolution result of Chapter 3.")]
    return Prob('B', st, steps, f"${ans}$.", 'Fourier transform properties')


def inverse_pf(rng):
    a, b = rng.sample([1, 2, 3, 4, 5], 2)
    c = rng.choice([0, 1, 2])
    d = rng.choice([1, 2, 3, 4, 6])
    s_ = sp.Symbol('s')
    Xs = (c * s_ + d) / ((s_ + a) * (s_ + b))
    A = sp.simplify(((c * s_ + d) / (s_ + b)).subs(s_, -a))
    B = sp.simplify(((c * s_ + d) / (s_ + a)).subs(s_, -b))
    num = f"{c if c != 1 else ''}j\\omega + {d}" if c else str(d)
    st = f"Find the inverse Fourier transform of $X(j\\omega) = \\dfrac{{{num}}}{{(j\\omega + {a})(j\\omega + {b})}}$."
    steps = [('Treat $j\\omega$ as a single variable', 'Write $v = j\\omega$ and expand $X$ in partial fractions in $v$, exactly as for a rational function.'),
             ('Cover-up', f"$\\dfrac{{{num.replace('j\\omega', 'v')}}}{{(v + {a})(v + {b})}} = \\dfrac{{A}}{{v + {a}}} + \\dfrac{{B}}{{v + {b}}}$ with $A = \\left.\\dfrac{{{num.replace('j\\omega', 'v')}}}{{v + {b}}}\\right|_{{v=-{a}}} = {tex(A)}$ and $B = \\left.\\dfrac{{{num.replace('j\\omega', 'v')}}}{{v + {a}}}\\right|_{{v=-{b}}} = {tex(B)}$."),
             ('Invert each term', 'Each term $\\dfrac{1}{j\\omega + a}$ comes from $e^{-at}u(t)$.'),
             ('Check', f"At $t = 0^+$, $x = {tex(A + B)}$, which equals $\\lim_{{\\omega\\to\\infty}} j\\omega X(j\\omega) = {c}$ as the initial-value relation requires.")]
    ans = f"$x(t) = \\left({combo([(A, expo(a)), (B, expo(b))])}\\right)u(t)$"
    return Prob('B', st, steps, ans + '.', 'Inverse transform')


def ideal_lpf(rng):
    W = cyc(rng, 'lw', [1, 2, 4, 10 * pi, 100])
    G = rng.choice([1, 2])
    st = f"Find the impulse response of an ideal low-pass filter with $H(j\\omega) = {G}$ for $|\\omega| < {tex(W)}$ and $0$ otherwise. Is the filter causal?"
    steps = [('Inverse transform', f"$h(t) = \\dfrac{{1}}{{2\\pi}}\\int_{{-{tex(W)}}}^{{{tex(W)}}} {G}e^{{j\\omega t}}d\\omega = \\dfrac{{{G}}}{{2\\pi}}\\cdot\\dfrac{{2\\sin({cf(W)}t)}}{{t}}$."),
             ('Simplify', f"$h(t) = \\dfrac{{{cf(G)}\\sin({cf(W)}t)}}{{\\pi t}}$, with peak value $h(0) = {tex(G*W/pi)}$ and zeros at multiples of $\\pi/{tex(W)}$."),
             ('Causality', '$h(t)$ is non-zero for negative $t$, so the ideal filter is not causal. Real filters approximate it with a delay and a truncated, tapered response.')]
    return Prob('B', st, steps, f"$h(t) = \\dfrac{{{cf(G)}\\sin({cf(W)}t)}}{{\\pi t}}$; not causal.", 'Ideal filters')


def parseval(rng):
    a = cyc(rng, 'pva', [1, 2, 3, 5])
    A = rng.choice([1, 2, 3])
    Wm = rng.choice([1, 2, sp.sqrt(3)])
    W = a * Wm
    frac = 2 * sp.atan(Wm) / pi
    st = f"For $x(t) = {cf(A)}{expo(a)}u(t)$, find the total energy using Parseval's theorem, and the fraction of the energy in $|\\omega| < {tex(W)}$ rad/s."
    E = sp.Rational(A * A, 2 * a)
    steps = [('Energy spectrum', f"$|X|^2 = \\dfrac{{{A*A}}}{{{a*a} + \\omega^2}}$."),
             ("Parseval", f"$E = \\dfrac{{1}}{{2\\pi}}\\int_{{-\\infty}}^{{\\infty}}\\dfrac{{{A*A}}}{{{a*a} + \\omega^2}}d\\omega = \\dfrac{{{A*A}}}{{2\\pi}}\\cdot\\dfrac{{\\pi}}{{{a}}} = {tex(E)}$, matching the time-domain integral."),
             ('Band-limited part', f"$\\dfrac{{1}}{{2\\pi}}\\int_{{-W}}^{{W}}\\dfrac{{{A*A}d\\omega}}{{{a*a} + \\omega^2}} = \\dfrac{{{A*A}}}{{\\pi {a}}}\\tan^{{-1}}\\!\\left(\\dfrac{{W}}{{{a}}}\\right)$."),
             ('Fraction', f"Dividing by $E$: $\\dfrac{{2}}{{\\pi}}\\tan^{{-1}}({tex(Wm)}) = {tex(frac)} \\approx {dec(frac, 4)}$.")]
    return Prob('B', st, steps, f"$E = {tex(E)}$; fraction ${tex(frac)} \\approx {dec(frac, 3)}$.", "Parseval's theorem")


def ode_resp(rng):
    if rng.random() < 0.6:
        a, c = rng.sample([1, 2, 3, 4, 6], 2)
        b = rng.choice([1, 2, 3, 5])
        st = f"A system obeys $\\dfrac{{dy}}{{dt}} + {a}y = {b}x(t)$. Find $H(j\\omega)$ and use it to find the output when $x(t) = {expo(c)}u(t)$."
        K = sp.Rational(b, c - a)
        q1, q2 = (a, c) if K > 0 else (c, a)
        K = abs(K)
        steps = [('Transform the equation', f"$(j\\omega + {a})Y = {b}X$, so $H(j\\omega) = \\dfrac{{{b}}}{{j\\omega + {a}}}$."),
                 ('Output spectrum', f"$Y = \\dfrac{{{b}}}{{(j\\omega + {a})(j\\omega + {c})}}$."),
                 ('Partial fractions', f"$Y = {cf(K)}\\left[\\dfrac{{1}}{{j\\omega + {q1}}} - \\dfrac{{1}}{{j\\omega + {q2}}}\\right]$."),
                 ('Invert', f"$y(t) = {cf(K)}\\left({expo(q1)} - {expo(q2)}\\right)u(t)$, which is zero at $t = 0$ and positive afterwards.")]
        ans = f"$H = \\dfrac{{{b}}}{{j\\omega + {a}}}$, $y(t) = {cf(K)}({expo(q1)} - {expo(q2)})u(t)$."
    else:
        p1, p2 = sorted(rng.sample([1, 2, 3, 4], 2))
        s1, s2 = p1 + p2, p1 * p2
        st = f"A system obeys $y'' + {s1}y' + {s2}y = x(t)$. Find its frequency response and impulse response."
        A = sp.Rational(1, p2 - p1)
        steps = [('Transform', f"$((j\\omega)^2 + {s1}j\\omega + {s2})Y = X$."),
                 ('Factor', f"$H(j\\omega) = \\dfrac{{1}}{{(j\\omega + {p1})(j\\omega + {p2})}}$."),
                 ('Partial fractions', f"$H = {cf(A)}\\left[\\dfrac{{1}}{{j\\omega + {p1}}} - \\dfrac{{1}}{{j\\omega + {p2}}}\\right]$."),
                 ('Impulse response', f"$h(t) = {cf(A)}({expo(p1)} - {expo(p2)})u(t)$, causal and stable.")]
        ans = f"$H = \\dfrac{{1}}{{(j\\omega + {p1})(j\\omega + {p2})}}$, $h(t) = {cf(A)}({expo(p1)} - {expo(p2)})u(t)$."
    return Prob('B', st, steps, ans, 'Systems described by ODEs')


def am(rng):
    W = cyc(rng, 'amw', [5, 4, 10, 15])
    fc = rng.choice([100, 200, 500, 1000])
    st = (f"A message $m(t)$ is band-limited to ${W}$ kHz. It is transmitted as $x(t) = m(t)\\cos(2\\pi f_c t)$ with $f_c = {fc}$ kHz. "
          "Describe the spectrum of $x(t)$, its bandwidth, and how $m(t)$ can be recovered.")
    steps = [('Modulation property', '$X(j\\omega) = \\tfrac12 M(j(\\omega - \\omega_c)) + \\tfrac12 M(j(\\omega + \\omega_c))$: two half-height copies of the message spectrum centred on $\\pm\\omega_c$.'),
             ('Occupied band', f"The positive-frequency copy occupies ${fc - W}$ to ${fc + W}$ kHz."),
             ('Bandwidth', f"$2 \\times {W} = {2*W}$ kHz: double-sideband modulation doubles the bandwidth."),
             ('Recovery', f"Multiply again by $\\cos(2\\pi f_c t)$: $x(t)\\cos(\\omega_c t) = \\tfrac12 m(t) + \\tfrac12 m(t)\\cos(2\\omega_c t)$. A low-pass filter with cutoff between ${W}$ and ${2*fc - W}$ kHz and gain 2 returns $m(t)$.")]
    return Prob('C', st, steps, f"Copies at $\\pm{fc}$ kHz, band ${fc-W}$–${fc+W}$ kHz, bandwidth ${2*W}$ kHz; recover by coherent demodulation and low-pass filtering.", 'Modulation')


def triangle_ft(rng):
    A = rng.choice([1, 2, 3])
    T = cyc(rng, 'tt', [1, 2, 3])
    st = f"Find the Fourier transform of the triangular pulse $x(t) = {cf(A)}(1 - |t|/{T})$ for $|t| < {T}$, zero otherwise."
    steps = [('Spot a convolution', f"A unit-height pulse of width ${T}$ convolved with itself is a triangle of base ${2*T}$ and peak ${T}$. So $x(t) = \\dfrac{{{A}}}{{{T}}}\\,p(t) * p(t)$ with $p(t) = 1$ for $|t| < {tex(Q(T,2))}$."),
             ('Transform of the pulse', f"$P(j\\omega) = \\dfrac{{2\\sin({tex(Q(T,2))}\\omega)}}{{\\omega}}$."),
             ('Multiply', f"$X = \\dfrac{{{A}}}{{{T}}}P^2 = \\dfrac{{{tex(Q(4*A, T))}\\sin^2({cf(Q(T,2))}\\omega)}}{{\\omega^2}}$."),
             ('Checks', f"$X(0) = {A*T}$, the area of the triangle. $X \\ge 0$ everywhere, and it decays as $1/\\omega^2$ because the triangle is continuous with a discontinuous slope.")]
    return Prob('C', st, steps, f"$X(j\\omega) = \\dfrac{{{tex(Q(4*A, T))}\\sin^2({cf(Q(T,2))}\\omega)}}{{\\omega^2}} = {A*T}\\operatorname{{sinc}}^2\\!\\left(\\dfrac{{{cf(T)}\\omega}}{{2\\pi}}\\right)$.", 'Triangular pulse')


def bandwidth(rng):
    case = cyc(rng, 'bw', ['rc', 'pulse', 'rc'])
    if case == 'rc':
        R = rng.choice([1, 2, 10])
        C = rng.choice([1, 10, 100])
        tau = sp.Rational(R * C, 1000000) * 1000
        st = f"An RC low-pass filter has $R = {R}$ k$\\Omega$ and $C = {C}$ nF. Find its 3 dB bandwidth in hertz and its 10–90% rise time."
        RC = sp.Rational(R * 1000 * C, 10 ** 9)
        f3 = 1 / (2 * pi * RC)
        tr = sp.log(9) * RC
        steps = [('Frequency response', '$H(j\\omega) = \\dfrac{1}{1 + j\\omega RC}$, which is 3 dB down at $\\omega = 1/RC$.'),
                 ('Numbers', f"$RC = {R}\\times10^3 \\times {C}\\times10^{{-9}} = {dec(RC*1e6, 3)}\\ \\mu$s, so $f_{{3\\text{{dB}}}} = 1/(2\\pi RC) \\approx {dec(f3/1000, 3)}$ kHz."),
                 ('Rise time', f"The step response $1 - e^{{-t/RC}}$ reaches 10% at $RC\\ln(10/9)$ and 90% at $RC\\ln 10$, so $t_r = RC\\ln 9 \\approx 2.2RC \\approx {dec(tr*1e6, 3)}\\ \\mu$s."),
                 ('Rule of thumb', f"$t_r f_{{3\\text{{dB}}}} = \\ln 9/2\\pi \\approx 0.35$, a time–bandwidth product you will meet in oscilloscope specifications.")]
        ans = f"$f_{{3\\text{{dB}}}} \\approx {dec(f3/1000, 3)}$ kHz, $t_r \\approx {dec(tr*1e6, 3)}\\ \\mu$s."
    else:
        T = rng.choice([1, 2, 5, 10])
        st = f"A rectangular pulse lasts ${T}\\ \\mu$s. Estimate its bandwidth as the frequency of the first spectral null, and comment on the product of duration and bandwidth."
        steps = [('Spectrum', 'A pulse of width $T$ has $X \\propto \\sin(\\omega T/2)/\\omega$, whose first null is at $\\omega = 2\\pi/T$, i.e. $f = 1/T$.'),
                 ('Numbers', f"$f = 1/({T}\\times10^{{-6}}) = {tex(Q(1000, T))}$ kHz."),
                 ('Comment', 'Duration times bandwidth is one, whatever the pulse width: halving the duration doubles the bandwidth. This trade-off is fundamental to every pulsed system.')]
        ans = f"About ${tex(Q(1000, T))}$ kHz; duration $\\times$ bandwidth $= 1$."
    return Prob('C', st, steps, ans, 'Time and bandwidth')


def periodic_ft(rng):
    w0 = cyc(rng, 'pw', [2, 3, 5, 10])
    A = rng.choice([1, 2, 4])
    B = rng.choice([1, 3])
    if rng.random() < 0.6:
        st = f"Find the Fourier transform of $x(t) = {cf(A)}\\cos({w0}t) + {cf(B)}\\sin({2*w0}t)$."
        steps = [('Transform of a complex exponential', '$e^{j\\omega_0 t} \\leftrightarrow 2\\pi\\delta(\\omega - \\omega_0)$: a periodic signal has a spectrum made of impulses.'),
                 ('Cosine', f"${A}\\cos({w0}t) \\leftrightarrow {A}\\pi[\\delta(\\omega - {w0}) + \\delta(\\omega + {w0})]$."),
                 ('Sine', f"${B}\\sin({2*w0}t) \\leftrightarrow \\dfrac{{{B}\\pi}}{{j}}[\\delta(\\omega - {2*w0}) - \\delta(\\omega + {2*w0})]$."),
                 ('Relation to Fourier series', 'In general $X(j\\omega) = \\sum_k 2\\pi a_k\\,\\delta(\\omega - k\\omega_0)$: the series coefficients become impulse weights, multiplied by $2\\pi$.')]
        ans = f"$X = {cf(A)}\\pi[\\delta(\\omega - {w0}) + \\delta(\\omega + {w0})] - j{cf(B)}\\pi[\\delta(\\omega - {2*w0}) - \\delta(\\omega + {2*w0})]$."
    else:
        T = rng.choice([1, 2, 4])
        st = f"Find the Fourier transform of the impulse train $x(t) = \\sum_n \\delta(t - {T}n)$."
        steps = [('Fourier series first', f"Over one period the train is a single impulse, so $a_k = \\dfrac{{1}}{{{T}}}\\int\\delta(t)e^{{-jk\\omega_0 t}}dt = \\dfrac{{1}}{{{T}}}$ for every $k$, with $\\omega_0 = {tex(2*pi/T)}$."),
                 ('Convert to a transform', f"$X(j\\omega) = \\sum_k 2\\pi\\cdot\\dfrac{{1}}{{{T}}}\\,\\delta(\\omega - k\\omega_0) = {tex(2*pi/T)}\\sum_k \\delta(\\omega - {tex(2*pi/T)}k)$."),
                 ('Interpretation', 'An impulse train in time is an impulse train in frequency. This pair is the key to the sampling theorem in Chapter 6.')]
        ans = f"$X(j\\omega) = {tex(2*pi/T)}\\sum_k \\delta(\\omega - {tex(2*pi/T)}k)$."
    return Prob('C', st, steps, ans, 'Transforms of periodic signals')


TEMPLATES = [(basic_pairs, 6), (magphase, 4),
             (props, 8), (inverse_pf, 6), (ideal_lpf, 3), (parseval, 4), (ode_resp, 5),
             (am, 4), (triangle_ft, 3), (bandwidth, 3), (periodic_ft, 4)]


def generate():
    return build_set(TEMPLATES, seed=505)


if __name__ == '__main__':
    for i, p in enumerate(generate(), 1):
        print(f'--- 5.{i} [{p.level}] {p.topic}\n{p.statement}\n  ANS: {p.answer}')
