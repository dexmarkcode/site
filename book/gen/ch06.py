"""Chapter 6 - DTFT, DFT and sampling."""
import numpy as np
import sympy as sp
from core import *

CH = 6


def nz(rng, lo=-2, hi=3):
    return rng.choice([v for v in range(lo, hi + 1) if v != 0])


def dtft_finite(rng):
    L = rng.choice([3, 4])
    x = [nz(rng) for _ in range(L)]
    st = f"Find the DTFT of $x[n] = {seq_tex(x, 0)}$ and evaluate it at $\\omega = 0$, $\\pi/2$ and $\\pi$."
    expr = combo([(v, '' if i == 0 else (f"e^{{-j\\omega}}" if i == 1 else f"e^{{-j{i}\\omega}}")) for i, v in enumerate(x)])
    vals = {}
    for name, wv in (('0', 0), ('\\pi/2', pi / 2), ('\\pi', pi)):
        vals[name] = sp.nsimplify(sp.expand_complex(sum(v * sp.exp(-j * wv * i) for i, v in enumerate(x))))
    steps = [('Definition', f"$X(e^{{j\\omega}}) = \\sum_n x[n]e^{{-j\\omega n}} = {expr}$."),
             ('At $\\omega = 0$', f"Every exponential is 1, so $X(e^{{j0}}) = \\sum x[n] = {tex(vals['0'])}$, the DC gain."),
             ('At $\\omega = \\pi/2$', f"$e^{{-j\\pi n/2}}$ cycles through $1, -j, -1, j$, giving $X = {tex(vals['\\pi/2'])}$."),
             ('At $\\omega = \\pi$', f"$e^{{-j\\pi n}} = (-1)^n$, so $X(e^{{j\\pi}}) = \\sum(-1)^n x[n] = {tex(vals['\\pi'])}$."),
             ('Periodicity', 'Being a polynomial in $e^{-j\\omega}$, $X$ repeats every $2\\pi$, as every DTFT must.')]
    ans = f"$X(e^{{j\\omega}}) = {expr}$; $X(e^{{j0}}) = {tex(vals['0'])}$, $X(e^{{j\\pi/2}}) = {tex(vals['\\pi/2'])}$, $X(e^{{j\\pi}}) = {tex(vals['\\pi'])}$."
    return Prob('A', st, steps, ans, 'DTFT of a finite sequence')


def dtft_geo(rng):
    a = cyc(rng, 'dg', [Q(1, 2), -Q(1, 2), Q(3, 4), Q(1, 3), -Q(4, 5)])
    A = rng.choice([1, 2])
    st = f"Find the DTFT of $x[n] = {cf(A)}\\left({tex(a)}\\right)^n u[n]$ and its magnitude at $\\omega = 0$ and $\\omega = \\pi$. Is the sequence low-pass or high-pass in character?"
    m0 = A / (1 - a)
    den = f"1 {'-' if a > 0 else '+'} {tex(abs(a))}e^{{-j\\omega}}"
    mpi = A / (1 + a)
    steps = [('Geometric series', f"$X = {A}\\sum_{{n\\ge0}}\\left({tex(a)}e^{{-j\\omega}}\\right)^n = \\dfrac{{{A}}}{{{den}}}$, valid because $|{tex(a)}| < 1$."),
             ('At $\\omega = 0$', f"$X = {A}/(1 - {par(a)}) = {tex(m0)}$."),
             ('At $\\omega = \\pi$', f"$e^{{-j\\pi}} = -1$, so $X = {A}/(1 + {par(a)}) = {tex(mpi)}$."),
             ('Character', 'A positive ratio gives a smooth sequence whose energy is concentrated at low frequencies; a negative ratio makes the samples alternate in sign, which pushes the energy towards $\\omega = \\pi$.')]
    kind = 'low-pass' if a > 0 else 'high-pass'
    return Prob('A', st, steps, f"$X = \\dfrac{{{A}}}{{{den}}}$; $|X(e^{{j0}})| = {tex(m0)}$, $|X(e^{{j\\pi}})| = {tex(mpi)}$; {kind}.", 'DTFT of a geometric sequence')


def nyquist(rng):
    case = cyc(rng, 'nq', ['sum', 'prod', 'sinc2', 'sum', 'mod'])
    f1, f2 = sorted(rng.sample([50, 100, 200, 300, 400, 500, 1000, 1500], 2))
    if case == 'sum':
        st = f"Find the Nyquist rate for $x(t) = 3\\cos(2\\pi\\cdot{f1}t) + \\sin(2\\pi\\cdot{f2}t)$."
        fm = f2
        steps = [('Highest frequency', f"The components are at ${f1}$ Hz and ${f2}$ Hz, so $f_{{\\max}} = {f2}$ Hz."),
                 ('Nyquist rate', f"$f_s > 2f_{{\\max}} = {2*f2}$ Hz.")]
    elif case == 'prod':
        st = f"Find the Nyquist rate for $x(t) = \\cos(2\\pi\\cdot{f1}t)\\cos(2\\pi\\cdot{f2}t)$."
        fm = f1 + f2
        steps = [('Product to sum', f"$\\cos A\\cos B = \\tfrac12[\\cos(A - B) + \\cos(A + B)]$, giving components at ${f2 - f1}$ Hz and ${f1 + f2}$ Hz."),
                 ('Nyquist rate', f"$2 \\times {f1 + f2} = {2*(f1+f2)}$ Hz. Multiplying signals adds their frequencies; it is easy to miss the sum term.")]
    elif case == 'sinc2':
        W = f1
        st = f"A signal $x(t)$ is band-limited to ${W}$ Hz. What is the Nyquist rate for $x^2(t)$?"
        fm = 2 * W
        steps = [('Squaring is self-convolution in frequency', f"$X * X$ has twice the width of $X$, so $x^2$ is band-limited to ${2*W}$ Hz."),
                 ('Nyquist rate', f"$2 \\times {2*W} = {4*W}$ Hz.")]
    else:
        W = f1
        fc = f2 * 10
        st = f"A message band-limited to ${W}$ Hz modulates a ${fc}$ Hz carrier: $x(t) = m(t)\\cos(2\\pi\\cdot{fc}t)$. What is the Nyquist rate for $x(t)$?"
        fm = fc + W
        steps = [('Spectrum', f"Modulation moves the message band to ${fc - W}$–${fc + W}$ Hz."),
                 ('Nyquist rate', f"Based on the highest frequency: $2({fc + W}) = {2*(fc+W)}$ Hz. (Band-pass sampling can do better, but that is beyond the simple theorem.)")]
    return Prob('A', st, steps, f"${2*fm}$ Hz.", 'Nyquist rate')


def alias(rng):
    fs_ = cyc(rng, 'al', [1000, 8000, 500, 44100, 2000, 100])
    f0 = int(fs_ * rng.choice([0.3, 0.7, 1.2, 1.45, 0.9, 2.15]))
    r = f0 % fs_
    fa = min(r, fs_ - r)
    st = f"A ${f0}$ Hz sinusoid is sampled at ${fs_}$ Hz without an anti-aliasing filter and then reconstructed by an ideal low-pass filter with cutoff ${fs_//2}$ Hz. What frequency is heard?"
    steps = [('Spectral copies', f"Sampling creates copies of the spectrum at $f_0 + k f_s$ for every integer $k$, i.e. at $\\pm{f0} + {fs_}k$ Hz."),
             ('Fold into the baseband', f"Reduce modulo $f_s$: ${f0} - {fs_}\\cdot{f0//fs_} = {r}$ Hz. " + (f"Since this exceeds $f_s/2 = {fs_//2}$, the image $f_s - {r} = {fa}$ Hz is the one that lands in the baseband." if r > fs_ / 2 else 'This already lies in $[0, f_s/2]$.')),
             ('Conclusion', f"The reconstructed tone is at ${fa}$ Hz." + (' No aliasing occurs because the signal satisfies the Nyquist condition.' if f0 < fs_ / 2 else ' This is aliasing: the original frequency cannot be recovered from the samples.'))]
    return Prob('B', st, steps, f"${fa}$ Hz.", 'Aliasing')


def dft4(rng):
    N = 4
    x = [rng.choice([-2, -1, 0, 1, 2, 3]) for _ in range(N)]
    if all(v == 0 for v in x):
        x[0] = 1
    X = [sp.nsimplify(sp.expand_complex(sum(x[m] * sp.exp(-2 * pi * j * kk * m / N) for m in range(N)))) for kk in range(N)]
    st = f"Compute the 4-point DFT of $x[n] = {seq_tex(x, 0)}$."
    steps = [('Twiddle factors', 'With $N = 4$, $W = e^{-j2\\pi/4} = -j$, so the powers $W^{kn}$ are only $1, -j, -1, j$. No trigonometry is needed.'),
             ('The DFT matrix', '$$\\begin{bmatrix} X[0]\\\\X[1]\\\\X[2]\\\\X[3]\\end{bmatrix} = \\begin{bmatrix}1&1&1&1\\\\1&-j&-1&j\\\\1&-1&1&-1\\\\1&j&-1&-j\\end{bmatrix}\\begin{bmatrix}' + '\\\\'.join(map(str, x)) + '\\end{bmatrix}$$'),
             ('Multiply out', f"$X[0] = {tex(X[0])}$, $X[1] = {tex(X[1])}$, $X[2] = {tex(X[2])}$, $X[3] = {tex(X[3])}$."),
             ('Checks', f"$X[0]$ is the sum of the samples. For real $x$, $X[3] = X[1]^*$. Parseval: $\\sum|x|^2 = {sum(v*v for v in x)}$ and $\\tfrac14\\sum|X|^2 = {tex(sp.nsimplify(sum(sp.Abs(v)**2 for v in X) / 4))}$.")]
    return Prob('B', st, steps, f"$X[k] = \\{{{tex(X[0])},\\ {tex(X[1])},\\ {tex(X[2])},\\ {tex(X[3])}\\}}$.", 'DFT')


def circ_conv(rng):
    N = 4
    x = [rng.choice([-1, 1, 2, 3]) for _ in range(N)]
    h = [rng.choice([1, 2, -1]), rng.choice([1, -1, 2]), 0, 0]
    lin = [int(v) for v in np.convolve(x, h[:2])]
    circ = [0] * N
    for m in range(N):
        for kk in range(N):
            circ[m] += x[kk] * h[(m - kk) % N]
    st = f"Find the 4-point circular convolution of $x[n] = {seq_tex(x, 0)}$ and $h[n] = {seq_tex(h, 0)}$, and compare it with the linear convolution."
    steps = [('Linear convolution first', f"$x * h = {seq_tex(lin, 0)}$, which has 5 samples."),
             ('Wrap around', f"Circular convolution with $N = 4$ adds the sample at $n = 4$ back onto $n = 0$: ${lin[0]} + ({lin[4]}) = {circ[0]}$."),
             ('Result', f"$x \\circledast h = {seq_tex(circ, 0)}$."),
             ('Lesson', 'The two agree only when $N \\ge$ the linear length (here 5). Otherwise the tail wraps round, an effect called time-domain aliasing.')]
    return Prob('B', st, steps, f"$x \\circledast h = {seq_tex(circ, 0)}$; linear: ${seq_tex(lin, 0)}$.", 'Circular convolution')


def fir_resp(rng):
    b = rng.choice([[1, 1], [1, -1], [1, 2, 1], [1, -2, 1], [1, 0, -1], [1, 1, 1], [1, 0, 1]])
    g = rng.choice([1, Q(1, 2), Q(1, 4), 2])
    bb = [g * v for v in b]
    terms = combo([(c, 'x[n]' if i == 0 else f'x[n-{i}]') for i, c in enumerate(bb) if c != 0])
    H = lambda wv: sp.nsimplify(sp.expand_complex(sum(c * sp.exp(-j * wv * i) for i, c in enumerate(bb))))
    H0, H2, Hp = H(0), H(pi / 2), H(pi)
    if sp.Abs(H0) > sp.Abs(Hp) and sp.Abs(H0) >= sp.Abs(H2):
        kind = 'low-pass'
    elif sp.Abs(Hp) > sp.Abs(H0) and sp.Abs(Hp) >= sp.Abs(H2):
        kind = 'high-pass'
    elif sp.Abs(H2) > sp.Abs(H0) and sp.Abs(H2) > sp.Abs(Hp):
        kind = 'band-pass'
    else:
        kind = 'band-stop (notch at $\\pi/2$)' if H2 == 0 else 'all-round'
    st = f"For the FIR filter $y[n] = {terms}$, find $H(e^{{j\\omega}})$, evaluate it at $\\omega = 0, \\pi/2, \\pi$, and describe the filter."
    Hexpr = combo([(c, '' if i == 0 else ('e^{-j\\omega}' if i == 1 else f'e^{{-j{i}\\omega}}')) for i, c in enumerate(bb) if c != 0])
    steps = [('Frequency response', f"The impulse response is the coefficient list, so $H(e^{{j\\omega}}) = {Hexpr}$."),
             ('Evaluate', f"$H(e^{{j0}}) = {tex(H0)}$, $H(e^{{j\\pi/2}}) = {tex(H2)}$, $H(e^{{j\\pi}}) = {tex(Hp)}$."),
             ('Magnitudes', f"$|H| = {tex(sp.Abs(H0))},\\ {tex(sp.Abs(H2))},\\ {tex(sp.Abs(Hp))}$ respectively."),
             ('Describe', f"The filter is {kind}." + (' Its symmetric (or antisymmetric) coefficients give it linear phase.' if bb == bb[::-1] or bb == [-v for v in bb[::-1]] else ''))]
    return Prob('B', st, steps, f"$H(e^{{j\\omega}}) = {Hexpr}$; values ${tex(H0)}$, ${tex(H2)}$, ${tex(Hp)}$; {kind}.", 'FIR frequency response')


def resolution(rng):
    fs_ = cyc(rng, 'rs', [1000, 8000, 48000, 2000])
    N = rng.choice([256, 512, 1024, 100, 200])
    df = sp.Rational(fs_, N)
    kk = rng.choice([5, 10, 20, 25])
    f = df * kk
    st = f"A signal is sampled at ${fs_}$ Hz and an ${N}$-point DFT is taken. What is the frequency spacing of the DFT bins, which bin holds a ${dec(f, 3)}$ Hz tone, and how long is the data record?"
    steps = [('Bin spacing', f"$\\Delta f = f_s/N = {fs_}/{N} = {dec(df, 4)}$ Hz."),
             ('Bin index', f"$k = f/\\Delta f = {dec(f, 3)}/{dec(df, 4)} = {kk}$ (and its mirror at $N - k = {N - kk}$)."),
             ('Record length', f"$T = N/f_s = {dec(sp.Rational(N, fs_), 4)}$ s. The spacing is $1/T$: to resolve finer detail you need a longer record, not just more zero-padding."),
             ('Zero-padding', 'Padding with zeros interpolates more points along the same underlying DTFT; it makes plots smoother but does not separate two tones closer than about $1/T$.')]
    return Prob('B', st, steps, f"$\\Delta f = {dec(df, 4)}$ Hz; bin ${kk}$; $T = {dec(sp.Rational(N, fs_), 4)}$ s.", 'DFT resolution')


def ideal_dt_lpf(rng):
    wc = cyc(rng, 'wc', [pi / 2, pi / 4, pi / 3])
    st = f"Find the impulse response of the ideal discrete-time low-pass filter with cutoff $\\omega_c = {tex(wc)}$, and give $h[0]$ to $h[3]$."
    hv = [wc / pi] + [sp.nsimplify(sp.sin(wc * m) / (pi * m)) for m in range(1, 4)]
    steps = [('Inverse DTFT', f"$h[n] = \\dfrac{{1}}{{2\\pi}}\\int_{{-\\omega_c}}^{{\\omega_c}} e^{{j\\omega n}}d\\omega = \\dfrac{{\\sin(\\omega_c n)}}{{\\pi n}}$."),
             ('$n = 0$', f"By the limit (or directly), $h[0] = \\omega_c/\\pi = {tex(hv[0])}$."),
             ('Values', ', '.join(f"$h[{m}] = {tex(v)}" + ('' if v == 0 else f" \\approx {dec(v, 4)}") + '$' for m, v in enumerate(hv)) + '.'),
             ('Comment', 'The response is infinite in both directions and therefore not causal. Practical FIR designs truncate and window it, then delay it to make it causal.')]
    return Prob('C', st, steps, f"$h[n] = \\dfrac{{\\sin({tex(wc)}n)}}{{\\pi n}}$; " + ', '.join(f"$h[{m}] = {tex(v)}$" for m, v in enumerate(hv)) + '.', 'Ideal filters')


def dft_conv_len(rng):
    L1 = rng.choice([50, 100, 200, 300, 1000])
    L2 = rng.choice([16, 31, 64, 101])
    Lr = L1 + L2 - 1
    p2 = 1 << (Lr - 1).bit_length()
    st = f"A record of {L1} samples is to be filtered by an FIR filter with {L2} taps using the DFT. What is the smallest DFT length that gives the linear convolution exactly, and the smallest power of two for an FFT?"
    steps = [('Length of the linear result', f"${L1} + {L2} - 1 = {Lr}$ samples."),
             ('Avoid wrap-around', f"Zero-pad both sequences to $N \\ge {Lr}$ before taking the DFT; then circular convolution equals linear convolution."),
             ('FFT size', f"The next power of two is ${p2}$."),
             ('If $N$ were too small', f"With, say, $N = {L1}$ the last {L2 - 1} output samples would wrap round and corrupt the first {L2 - 1}.")]
    return Prob('C', st, steps, f"$N \\ge {Lr}$; FFT size ${p2}$.", 'Fast convolution')


def dtft_props(rng):
    a = cyc(rng, 'dpa', [Q(1, 2), Q(1, 3), Q(2, 3)])
    case = cyc(rng, 'dpc', ['nmul', 'shift', 'alt', 'rev', 'conv'])
    X = f"\\dfrac{{1}}{{1 - {tex(a)}e^{{-j\\omega}}}}"
    st0 = f"Given $({tex(a)})^n u[n] \\leftrightarrow {X}$, find the DTFT of "
    if case == 'nmul':
        st = st0 + f"$n({tex(a)})^n u[n]$."
        ans = f"\\dfrac{{{tex(a)}e^{{-j\\omega}}}}{{(1 - {tex(a)}e^{{-j\\omega}})^2}}"
        steps = [('Property', '$n\\,x[n] \\leftrightarrow j\\,\\dfrac{dX}{d\\omega}$.'), ('Differentiate', f"$\\dfrac{{dX}}{{d\\omega}} = \\dfrac{{-j{tex(a)}e^{{-j\\omega}}}}{{(1 - {tex(a)}e^{{-j\\omega}})^2}}$; multiplying by $j$ gives ${ans}$.")]
    elif case == 'shift':
        n0 = rng.choice([2, 3])
        st = st0 + f"$({tex(a)})^{{n-{n0}}}u[n-{n0}]$."
        ans = f"\\dfrac{{e^{{-j{n0}\\omega}}}}{{1 - {tex(a)}e^{{-j\\omega}}}}"
        steps = [('Property', '$x[n - n_0] \\leftrightarrow e^{-j\\omega n_0}X(e^{j\\omega})$.'), ('Apply', f"${ans}$.")]
    elif case == 'alt':
        st = st0 + f"$(-1)^n({tex(a)})^n u[n]$, and explain the effect on the spectrum."
        ans = f"\\dfrac{{1}}{{1 + {tex(a)}e^{{-j\\omega}}}}"
        steps = [('Write $(-1)^n = e^{j\\pi n}$', 'Multiplication by $e^{j\\pi n}$ shifts the spectrum by $\\pi$: $X(e^{j(\\omega - \\pi)})$.'), ('Apply', f"$e^{{-j(\\omega-\\pi)}} = -e^{{-j\\omega}}$, giving ${ans}$."),
                 ('Effect', 'Low frequencies and high frequencies swap places, turning a low-pass sequence into a high-pass one.')]
    elif case == 'rev':
        st = st0 + f"$({tex(a)})^{{-n}}u[-n]$."
        ans = f"\\dfrac{{1}}{{1 - {tex(a)}e^{{j\\omega}}}}"
        steps = [('Property', '$x[-n] \\leftrightarrow X(e^{-j\\omega})$.'), ('Apply', f"${ans}$.")]
    else:
        st = st0 + f"$({tex(a)})^n u[n] * ({tex(a)})^n u[n]$, and identify the sequence."
        ans = f"\\dfrac{{1}}{{(1 - {tex(a)}e^{{-j\\omega}})^2}}"
        steps = [('Convolution becomes multiplication', f"$Y = X^2 = {ans}$."), ('Identify', f"From Chapter 3 the sequence is $(n + 1)({tex(a)})^n u[n]$.")]
    return Prob('C', st, steps, f"${ans}$.", 'DTFT properties')


TEMPLATES = [(dtft_finite, 5), (dtft_geo, 4), (nyquist, 5),
             (alias, 6), (dft4, 6), (circ_conv, 4), (fir_resp, 5), (resolution, 4),
             (ideal_dt_lpf, 3), (dft_conv_len, 3), (dtft_props, 5)]


def generate():
    return build_set(TEMPLATES, seed=606)


if __name__ == '__main__':
    for i, p in enumerate(generate(), 1):
        print(f'--- 6.{i} [{p.level}] {p.topic}\n{p.statement}\n  ANS: {p.answer}')
