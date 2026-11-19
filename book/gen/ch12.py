"""Chapter 12 - Discrete-time systems and digital filters."""
import math
import sympy as sp
from core import *
from zt import izt

CH = 12
H_ = Q(1, 2)


def de_tex(b, a):
    """Difference equation y[n] + a1 y[n-1] + ... = b0 x[n] + ..."""
    lhs = combo([(c, 'y[n]' if i == 0 else f'y[n-{i}]') for i, c in enumerate(a) if c != 0])
    rhs = combo([(c, 'x[n]' if i == 0 else f'x[n-{i}]') for i, c in enumerate(b) if c != 0])
    return f"{lhs} = {rhs}"


def h_from_de(rng):
    p1 = rng.choice([H_, Q(1, 3), -H_, Q(3, 4), Q(5, 4), 2])
    p2 = rng.choice([v for v in [Q(1, 4), -Q(1, 3), Q(2, 3), H_, -Q(3, 2)] if v != p1])
    b = [1, rng.choice([0, 1, -1, 2])]
    a = [1, -(p1 + p2), p1 * p2]
    H = (b[0] * z ** 2 + b[1] * z) / ((z - p1) * (z - p2))
    stable = abs(p1) < 1 and abs(p2) < 1
    st = f"A causal system obeys ${de_tex(b, a)}$. Find $H(z)$, its poles and zeros, and decide whether it is stable."
    steps = [('Transform with zero initial conditions', f"$Y(z)({zpoly_tex(a)}) = X(z)({zpoly_tex(b)})$."),
             ('System function', f"$H(z) = \\dfrac{{{zpoly_tex(b)}}}{{{zpoly_tex(a)}}} = {tex(sp.factor(H))}$ after multiplying through by $z^2$."),
             ('Poles and zeros', f"Poles at $z = {tex(p1)}$ and $z = {tex(p2)}$; zeros at $z = 0$" + (f" and $z = {tex(-b[1])}$." if b[1] else ' (double).')),
             ('Stability', 'A causal system is stable when every pole lies strictly inside the unit circle. ' + ('Both do, so it is stable.' if stable else 'At least one does not, so it is unstable.'))]
    return Prob('A', st, steps, f"$H(z) = {tex(sp.factor(H))}$; " + ('stable.' if stable else 'unstable.'), 'System function')


def dc_nyq(rng):
    case = cyc(rng, 'dn', ['fir', 'iir', 'iir', 'fir'])
    if case == 'fir':
        b = rng.choice([[1, 2, 1], [1, -2, 1], [1, 1, 1, 1], [1, -1], [2, 0, -2], [1, 3, 3, 1]])
        H = sum(c * z ** (-i) for i, c in enumerate(b))
        st = f"Find the gain at DC and at the Nyquist frequency of the FIR filter $y[n] = {combo([(c, 'x[n]' if i == 0 else f'x[n-{i}]') for i, c in enumerate(b) if c])}$, and classify it."
    else:
        a1 = rng.choice([H_, -H_, Q(9, 10), -Q(9, 10), Q(1, 4)])
        H = 1 / (1 - a1 / z)
        st = f"Find the gain at DC and at the Nyquist frequency of $y[n] = {tex(a1)}y[n-1] + x[n]$, and classify it."
    g0, gpi = sp.nsimplify(H.subs(z, 1)), sp.nsimplify(H.subs(z, -1))
    kind = 'low-pass' if abs(g0) > abs(gpi) else ('high-pass' if abs(gpi) > abs(g0) else 'neither (equal gains)')
    if g0 == 0 and gpi == 0:
        kind = 'band-pass'
    steps = [('Where to evaluate', 'DC is $\\omega = 0$, i.e. $z = 1$; the Nyquist frequency is $\\omega = \\pi$, i.e. $z = -1$.'),
             ('DC gain', f"$H(1) = {tex(g0)}$."),
             ('Nyquist gain', f"$H(-1) = {tex(gpi)}$."),
             ('Classify', f"The filter is {kind}.")]
    return Prob('A', st, steps, f"$H(1) = {tex(g0)}$, $H(-1) = {tex(gpi)}$; {kind}.", 'DC and Nyquist gain')


def moving_avg(rng):
    N = cyc(rng, 'ma', [3, 4, 5])
    st = f"For the {N}-point moving average $y[n] = \\tfrac{{1}}{{{N}}}\\sum_{{k=0}}^{{{N-1}}}x[n-k]$, find $H(z)$, its zeros, and $|H(e^{{j\\omega}})|$."
    zs = ', '.join(f"$e^{{\\pm j2\\pi\\cdot{k_}/{N}}}$" if 2 * k_ != N else '$-1$' for k_ in range(1, N // 2 + 1))
    steps = [('System function', f"$H(z) = \\dfrac{{1}}{{{N}}}\\sum_{{k=0}}^{{{N-1}}}z^{{-k}} = \\dfrac{{1}}{{{N}}}\\cdot\\dfrac{{1 - z^{{-{N}}}}}{{1 - z^{{-1}}}}$."),
             ('Zeros', f"The numerator vanishes at the {N}th roots of unity; the root $z = 1$ cancels the denominator, leaving zeros at {zs}."),
             ('Magnitude', f"$|H(e^{{j\\omega}})| = \\dfrac{{1}}{{{N}}}\\left|\\dfrac{{\\sin({N}\\omega/2)}}{{\\sin(\\omega/2)}}\\right|$, a Dirichlet kernel: unity at DC, with nulls at $\\omega = 2\\pi k/{N}$."),
             ('Use', 'A simple low-pass smoother that completely removes components at those null frequencies, such as mains hum when the sample rate is chosen accordingly.')]
    return Prob('A', st, steps, f"$H(z) = \\dfrac{{1 - z^{{-{N}}}}}{{{N}(1 - z^{{-1}})}}$; zeros at the non-unit {N}th roots of unity; $|H| = \\left|\\dfrac{{\\sin({N}\\omega/2)}}{{{N}\\sin(\\omega/2)}}\\right|$.", 'Moving average')


def stab_triangle(rng):
    a1 = rng.choice([-Q(3, 2), -1, -H_, H_, 1, Q(6, 5), -Q(9, 5), Q(1, 4)])
    a2 = rng.choice([Q(1, 4), H_, Q(9, 10), -H_, Q(11, 10), Q(4, 5)])
    stable = abs(a2) < 1 and abs(a1) < 1 + a2
    st = f"Is the causal system $y[n] {'+' if a1 >= 0 else '-'} {tex(abs(a1))}y[n-1] {'+' if a2 >= 0 else '-'} {tex(abs(a2))}y[n-2] = x[n]$ stable? Use the stability triangle, then confirm with the pole locations."
    rts = sp.roots(z ** 2 + a1 * z + a2)
    mags = [float(abs(sp.N(r))) for r in rts for _ in range(rts[r])]
    steps = [('The triangle', 'For $z^2 + a_1z + a_2$ both roots lie inside the unit circle exactly when $|a_2| < 1$ and $|a_1| < 1 + a_2$.'),
             ('Check', f"$|a_2| = {tex(abs(a2))}$ " + ('$< 1$' if abs(a2) < 1 else '$\\ge 1$') + f"; $|a_1| = {tex(abs(a1))}$ and $1 + a_2 = {tex(1 + a2)}$, so the second condition " + ('holds.' if abs(a1) < 1 + a2 else 'fails.')),
             ('Poles', f"Roots of $z^2 {'+' if a1 >= 0 else '-'} {tex(abs(a1))}z {'+' if a2 >= 0 else '-'} {tex(abs(a2))}$: " + ', '.join(f"${tex(r)}$" for r in rts) + f", with magnitudes " + ', '.join(f"{m:.3f}" for m in mags) + '.'),
             ('Conclusion', 'Stable.' if stable else 'Unstable.')]
    assert stable == all(m < 1 - 1e-12 for m in mags)
    return Prob('B', st, steps, 'Stable.' if stable else 'Unstable.', 'Stability triangle')


def ss_sin(rng):
    a = cyc(rng, 'ss', [H_, Q(3, 4), -H_, Q(9, 10)])
    w0 = rng.choice([pi / 2, pi / 3, pi / 4, pi])
    A = rng.choice([1, 2, 4])
    H = 1 / (1 - a * sp.exp(-j * w0))
    Hs = sp.nsimplify(sp.simplify(sp.expand_complex(H)))
    m = float(abs(sp.N(H)))
    ph = float(sp.arg(sp.N(H)))
    st = f"Find the steady-state response of $y[n] = {tex(a)}y[n-1] + x[n]$ to $x[n] = {cf(A)}\\cos\\left({tex(w0)}n\\right)$."
    steps = [('Frequency response', f"$H(e^{{j\\omega}}) = \\dfrac{{1}}{{1 - {par(a)}e^{{-j\\omega}}}}$."),
             ('Evaluate', f"At $\\omega = {tex(w0)}$: $H = {tex(Hs)}$, with $|H| \\approx {m:.4f}$ and $\\angle H \\approx {ph:.4f}$ rad."),
             ('Output', 'A sinusoid passes through scaled by $|H|$ and shifted by $\\angle H$, exactly as in continuous time.')]
    phs = '' if abs(ph) < 1e-12 else (f" + {ph:.4f}" if ph > 0 else f" - {abs(ph):.4f}")
    return Prob('B', st, steps, f"$y_{{ss}}[n] \\approx {A*m:.4f}\\cos\\left({tex(w0)}n{phs}\\right)$.", 'Sinusoidal steady state')


def linear_phase(rng):
    case = cyc(rng, 'lp', ['sym_odd', 'sym_even', 'anti', 'sym_odd', 'sym_even'])
    if case == 'sym_odd':
        c = [rng.choice([1, 2]), rng.choice([2, 3, 4]), rng.choice([3, 5, 6])]
        h = c + c[-2::-1]
    elif case == 'sym_even':
        c = [rng.choice([1, 2]), rng.choice([3, 4])]
        h = c + c[::-1]
    else:
        c = [1, rng.choice([2, 3])]
        h = c + [0] + [-v for v in c[::-1]]
    N = len(h)
    D = sp.Rational(N - 1, 2)
    st = f"An FIR filter has $h[n] = {seq_tex(h, 0)}$. Show that it has linear phase, find its group delay, and say whether it can be used as a low-pass filter."
    ftype = {'sym_odd': 'Type I (symmetric, odd length)', 'sym_even': 'Type II (symmetric, even length)', 'anti': 'Type III (antisymmetric, odd length)'}[case]
    use = {'sym_odd': 'Yes: Type I filters can realise any of the standard responses.',
           'sym_even': 'Yes for low-pass, but it has a forced zero at $\\omega = \\pi$, so it cannot be high-pass.',
           'anti': 'No: it has forced zeros at both $\\omega = 0$ and $\\omega = \\pi$, so it suits differentiators and Hilbert transformers, not low-pass filters.'}[case]
    steps = [('Symmetry', f"$h[n] = {'' if case != 'anti' else '-'}h[{N-1} - n]$: the coefficients are {'symmetric' if case != 'anti' else 'antisymmetric'} about $n = {tex(D)}$. This is {ftype}."),
             ('Factor out the centre', f"Pairing $h[k]$ with $h[{N-1}-k]$ gives $H(e^{{j\\omega}}) = e^{{-j{tex(D)}\\omega}}\\,A(\\omega)$ with $A$ real" + (' (times $j$ for the antisymmetric case)' if case == 'anti' else '') + '.'),
             ('Group delay', f"The phase is $-{tex(D)}\\omega$ plus a constant, so every frequency is delayed by the same ${tex(D)}$ samples. The waveform is not distorted."),
             ('Low-pass?', use)]
    return Prob('B', st, steps, f"{ftype}; group delay ${tex(D)}$ samples. {use}", 'Linear phase FIR')


def bilinear(rng):
    a = cyc(rng, 'bl', [1, 2, 10, 100, 1000])
    T = rng.choice([sp.Rational(1, 10), sp.Rational(1, 100), sp.Rational(1, 1000), sp.Rational(1, 8000)])
    if a * T > 2:
        T = sp.Rational(1, 1000)
    k_ = 2 / T
    H = sp.simplify((a / (s + a)).subs(s, k_ * (z - 1) / (z + 1)))
    num = a * (z + 1)
    den = (k_ + a) * z + (a - k_)
    b0 = sp.nsimplify(a / (k_ + a))
    pole = sp.nsimplify((k_ - a) / (k_ + a))
    wd = 2 * math.atan(float(a * T / 2))
    st = f"Convert $H(s) = \\dfrac{{{a}}}{{s + {a}}}$ to a digital filter using the bilinear transform with $T = {tex(T)}$ s. Where does the analogue 3 dB frequency land in the digital domain?"
    steps = [('Substitute', f"$s = \\dfrac{{2}}{{T}}\\cdot\\dfrac{{z - 1}}{{z + 1}} = {tex(k_)}\\,\\dfrac{{z - 1}}{{z + 1}}$."),
             ('Simplify', f"$H(z) = \\dfrac{{{a}(z + 1)}}{{{tex(k_)}(z - 1) + {a}(z + 1)}} = \\dfrac{{{tex(b0)}(1 + z^{{-1}})}}{{1 - {par(pole)}z^{{-1}}}}$."),
             ('Difference equation', f"$y[n] = {tex(pole)}y[n-1] + {tex(b0)}(x[n] + x[n-1])$."),
             ('Frequency warping', f"The bilinear map sends $\\Omega$ to $\\omega = 2\\tan^{{-1}}(\\Omega T/2)$. With $\\Omega = {a}$: $\\omega \\approx {wd:.4f}$ rad/sample. Prewarping ($\\Omega' = \\tfrac{{2}}{{T}}\\tan(\\omega_c/2)$) is used when the digital cutoff must be exact.")]
    return Prob('B', st, steps, f"$H(z) = \\dfrac{{{tex(b0)}(1 + z^{{-1}})}}{{1 - {par(pole)}z^{{-1}}}}$; cutoff at $\\omega \\approx {wd:.4f}$ rad/sample.", 'Bilinear transform')


def impulse_inv(rng):
    a = cyc(rng, 'ii', [1, 2, 5, 10])
    T = rng.choice([Q(1, 10), Q(1, 2), Q(1, 100)])
    two = rng.random() < 0.4
    if not two:
        st = f"Use impulse invariance with $T = {tex(T)}$ s to convert $H(s) = \\dfrac{{1}}{{s + {a}}}$ to a digital filter. Compare the DC gains."
        p = sp.exp(-a * T)
        steps = [('Sample the impulse response', f"$h(t) = {expo(a)}u(t)$, so $h[n] = T\\,h(nT) = {tex(T)}\\,e^{{-{tex(a*T)}n}}u[n]$ (the factor $T$ keeps the gain comparable)."),
                 ('Transform', f"$H(z) = \\dfrac{{{tex(T)}}}{{1 - e^{{-{tex(a*T)}}}z^{{-1}}}}$, a pole at $e^{{-{tex(a*T)}}} \\approx {float(p):.4f}$."),
                 ('DC gains', f"Analogue: $H(0) = 1/{a}$. Digital: $H(1) = {tex(T)}/(1 - e^{{-{tex(a*T)}}}) \\approx {float(T/(1 - p)):.4f}$, close to ${float(Q(1, a)):.4f}$ when $aT$ is small.")]
        ans = f"$H(z) = \\dfrac{{{tex(T)}}}{{1 - e^{{-{tex(a*T)}}}z^{{-1}}}}$."
    else:
        b = a * 2
        st = f"Use impulse invariance with $T = {tex(T)}$ s to convert $H(s) = \\dfrac{{1}}{{(s + {a})(s + {b})}}$."
        A = Q(1, b - a)
        steps = [('Partial fractions', f"$H(s) = {tex(A)}\\left[\\dfrac{{1}}{{s + {a}}} - \\dfrac{{1}}{{s + {b}}}\\right]$."),
                 ('Map each pole', 'Each $\\dfrac{1}{s + p}$ becomes $\\dfrac{T}{1 - e^{-pT}z^{-1}}$: poles map as $z = e^{sT}$.'),
                 ('Result', f"$H(z) = {tex(A*T)}\\left[\\dfrac{{1}}{{1 - e^{{-{tex(a*T)}}}z^{{-1}}}} - \\dfrac{{1}}{{1 - e^{{-{tex(b*T)}}}z^{{-1}}}}\\right]$.")]
        ans = f"$H(z) = {tex(A*T)}\\left[\\dfrac{{1}}{{1 - e^{{-{tex(a*T)}}}z^{{-1}}}} - \\dfrac{{1}}{{1 - e^{{-{tex(b*T)}}}z^{{-1}}}}\\right]$."
    steps.append(('Caution', 'Impulse invariance aliases: it suits low-pass and band-pass prototypes, never high-pass ones.'))
    return Prob('B', st, steps, ans, 'Impulse invariance')


def notch(rng):
    fs_ = cyc(rng, 'nf', [500, 1000, 2000, 400])
    f0 = rng.choice([50, 60])
    r = rng.choice([Q(9, 10), Q(19, 20), Q(49, 50)])
    w0 = 2 * pi * f0 / fs_
    c = sp.cos(w0)
    st = f"Design a second-order IIR notch filter to remove ${f0}$ Hz interference from a signal sampled at ${fs_}$ Hz, using pole radius $r = {tex(r)}$. Give the difference equation."
    cn = float(c)
    steps = [('Digital notch frequency', f"$\\omega_0 = 2\\pi\\cdot{f0}/{fs_} = {tex(w0)}$ rad/sample, $\\cos\\omega_0 \\approx {cn:.5f}$."),
             ('Zeros on the unit circle', f"Place zeros at $e^{{\\pm j\\omega_0}}$: numerator $1 - 2\\cos\\omega_0\\,z^{{-1}} + z^{{-2}}$, which blocks $\\omega_0$ completely."),
             ('Poles just inside', f"Place poles at $re^{{\\pm j\\omega_0}}$: denominator $1 - 2r\\cos\\omega_0\\,z^{{-1}} + r^2z^{{-2}}$. The closer $r$ is to 1, the narrower the notch; the 3 dB width is roughly $2(1 - r) = {tex(2*(1 - r))}$ rad/sample."),
             ('Difference equation', f"$y[n] = {2*float(r)*cn:.5f}y[n-1] - {float(r*r):.4f}y[n-2] + x[n] - {2*cn:.5f}x[n-1] + x[n-2]$.")]
    return Prob('C', st, steps, f"$H(z) = \\dfrac{{1 - {2*cn:.5f}z^{{-1}} + z^{{-2}}}}{{1 - {2*float(r)*cn:.5f}z^{{-1}} + {float(r*r):.4f}z^{{-2}}}}$.", 'Notch filters')


def realisation(rng):
    p1, p2 = rng.sample([H_, Q(1, 4), -Q(1, 3), Q(3, 4), -H_], 2)
    z1 = rng.choice([-1, 1, H_, 0])
    H = (1 - z1 / z) / ((1 - p1 / z) * (1 - p2 / z))
    a = [1, -(p1 + p2), p1 * p2]
    b = [1, -z1]
    st = f"Give the direct-form II and cascade realisations of $H(z) = \\dfrac{{{zpoly_tex(b)}}}{{({zpoly_tex([1, -p1])})({zpoly_tex([1, -p2])})}}$, and count delays and multipliers."
    steps = [('Expand the denominator', f"$({zpoly_tex([1, -p1])})({zpoly_tex([1, -p2])}) = {zpoly_tex(a)}$."),
             ('Direct form II', f"Use one internal state $w[n] = x[n] - ({tex(a[1])})w[n-1] - ({tex(a[2])})w[n-2]$, then $y[n] = w[n] {'-' if z1 > 0 else '+'} {tex(abs(z1))}w[n-1]$." if z1 else
              f"Internal state $w[n] = x[n] - ({tex(a[1])})w[n-1] - ({tex(a[2])})w[n-2]$, and $y[n] = w[n]$."),
             ('Cascade form', f"Section 1: $H_1 = \\dfrac{{{zpoly_tex(b)}}}{{{zpoly_tex([1, -p1])}}}$; section 2: $H_2 = \\dfrac{{1}}{{{zpoly_tex([1, -p2])}}}$."),
             ('Cost', 'Direct form II needs only two delays (the minimum, so it is canonical). The cascade uses the same number of delays but keeps each pole in its own section, which is far less sensitive to coefficient rounding in fixed-point hardware.')]
    return Prob('C', st, steps, f"DF-II: $w[n] = x[n] - ({tex(a[1])})w[n-1] - ({tex(a[2])})w[n-2]$, $y[n] = w[n] {'-' if z1 >= 0 else '+'} {tex(abs(z1))}w[n-1]$; cascade of two first-order sections.", 'Realisations')


def ewma(rng):
    case = cyc(rng, 'ew', ['alpha', 'design', 'alpha', 'design', 'alpha'])
    if case == 'alpha':
        al = rng.choice([Q(9, 10), Q(4, 5), Q(1, 2), Q(19, 20), Q(99, 100)])
        cw = 1 - (1 - al) ** 2 / (2 * al)
        wc = math.acos(float(cw))
        st = f"The smoother $y[n] = {tex(al)}y[n-1] + {tex(1 - al)}x[n]$ is used to clean up a sensor reading. Find its DC gain, its 3 dB frequency and its time constant in samples."
        steps = [('System function', f"$H(z) = \\dfrac{{{tex(1-al)}}}{{1 - {tex(al)}z^{{-1}}}}$; $H(1) = 1$, so the long-run average is preserved."),
                 ('3 dB point', f"Setting $|H|^2 = \\tfrac12$ gives $\\cos\\omega_c = 1 - \\dfrac{{(1 - \\alpha)^2}}{{2\\alpha}} = {tex(cw)}$, so $\\omega_c \\approx {wc:.4f}$ rad/sample."),
                 ('Time constant', f"The step response is $1 - \\alpha^{{n+1}}$; it reaches $1 - e^{{-1}}$ after about $-1/\\ln\\alpha \\approx {-1/math.log(float(al)):.1f}$ samples.")]
        ans = f"DC gain 1; $\\omega_c \\approx {wc:.4f}$ rad/sample; time constant $\\approx {-1/math.log(float(al)):.1f}$ samples."
    else:
        fs_ = rng.choice([100, 1000])
        tau = rng.choice([Q(1, 10), Q(1, 2), 1])
        al = math.exp(-1 / (float(tau) * fs_))
        st = f"Choose $\\alpha$ in $y[n] = \\alpha y[n-1] + (1 - \\alpha)x[n]$ so that, at ${fs_}$ Hz sampling, it mimics an RC filter with time constant ${tex(tau)}$ s."
        steps = [('Match the decay', 'The RC step response decays as $e^{-t/\\tau}$; the digital one as $\\alpha^n$ with $t = n/f_s$.'),
                 ('Solve', f"$\\alpha = e^{{-1/(\\tau f_s)}} = e^{{-1/{tex(tau*fs_)}}} \\approx {al:.5f}$."),
                 ('Comment', 'When $\\tau f_s$ is large, $\\alpha \\approx 1 - 1/(\\tau f_s)$, the familiar rule of thumb.')]
        ans = f"$\\alpha \\approx {al:.5f}$."
    return Prob('C', st, steps, ans, 'First-order smoothing')


TEMPLATES = [(h_from_de, 6), (dc_nyq, 4), (moving_avg, 3),
             (stab_triangle, 5), (ss_sin, 5), (linear_phase, 5), (bilinear, 5), (impulse_inv, 4),
             (notch, 4), (realisation, 4), (ewma, 5)]


def generate():
    return build_set(TEMPLATES, seed=1212)


if __name__ == '__main__':
    for i, p in enumerate(generate(), 1):
        print(f'--- 12.{i} [{p.level}] {p.topic}\n{p.statement}\n  ANS: {p.answer}')
