"""Chapter 1 - Signals: classification, operations and elementary functions."""
import math
import sympy as sp
from core import *
import figstyle as fs
import matplotlib.pyplot as plt

CH = 1


# ---------------------------------------------------------------- A level
def sinusoid(rng):
    A = rng.choice([2, 3, 4, 5, 6, 8, 10, 12])
    f = cyc(rng, 'f1', [25, 50, 60, 100, 120, 250, 400, 500, 1000])
    phi = rng.choice([Q(1, 6), Q(1, 4), Q(1, 3), -Q(1, 4), -Q(1, 6), Q(1, 2), -Q(1, 3)]) * pi
    fn = rng.choice(['cos', 'sin'])
    w0 = 2 * f * pi
    st = (f"A signal is described by $x(t) = {A}\\{fn}\\left({tex(w0)} t {'+' if phi > 0 else '-'} {tex(abs(phi))}\\right)$, "
          f"with $t$ in seconds. State its amplitude, angular frequency, cyclic frequency and period, and evaluate $x(0)$.")
    x0 = A * (sp.cos(phi) if fn == 'cos' else sp.sin(phi))
    steps = [
        ('Match the standard form', f"Compare with $A\\{fn}(\\omega_0 t + \\phi)$. The amplitude is the multiplier in front, so $A = {A}$, "
         f"and the coefficient of $t$ inside the bracket is $\\omega_0 = {tex(w0)}$ rad/s. The phase is $\\phi = {tex(phi)}$ rad."),
        ('Convert to hertz', f"Cyclic frequency is $f_0 = \\omega_0 / 2\\pi = {tex(w0)}/2\\pi = {f}$ Hz."),
        ('Find the period', f"$T_0 = 1/f_0 = 1/{f}$ s $= {dec(sp.Rational(1000, f), 3)}$ ms."),
        ('Evaluate at $t = 0$', f"Only the phase survives: $x(0) = {A}\\{fn}\\left({tex(phi)}\\right) = {tex(sp.nsimplify(x0))}"
         + (f" \\approx {dec(x0)}$." if not sp.nsimplify(x0).is_Integer else '$.')),
    ]
    ans = (f"$A = {A}$, $\\omega_0 = {tex(w0)}$ rad/s, $f_0 = {f}$ Hz, $T_0 = 1/{f}$ s, $x(0) = {tex(sp.nsimplify(x0))}$.")
    return Prob('A', st, steps, ans, 'Sinusoid parameters')


def complex_polar(rng):
    a = rng.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
    b = rng.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
    zc = a + b * j
    mag = sp.sqrt(a * a + b * b)
    ang = sp.atan2(b, a)
    angd = float(ang) * 180 / math.pi
    quad = {(True, True): 'first', (False, True): 'second', (False, False): 'third', (True, False): 'fourth'}[(a > 0, b > 0)]
    naive = math.degrees(math.atan(b / a))
    steps = [
        ('Locate the point', f"The number $z = {tex(zc)}$ sits at $({a}, {b})$ in the complex plane, which is the {quad} quadrant. "
         "Knowing the quadrant first protects us from the most common slip with the arctangent."),
        ('Magnitude', f"$|z| = \\sqrt{{{a}^2 + ({b})^2}} = \\sqrt{{{a*a+b*b}}} = {tex(mag)}" + ('' if mag.is_Integer else f" \\approx {dec(mag)}") + '$.'),
        ('Angle', f"A calculator gives $\\tan^{{-1}}({b}/{a}) = {naive:.2f}^\\circ$. "
         + ("Because the point is in the first or fourth quadrant this is already correct" if a > 0 else
            "Because $a<0$ the point is in the left half-plane, so we must add or subtract $180^\\circ$")
         + f", giving $\\angle z = {angd:.2f}^\\circ = {dec(ang)}$ rad."),
        ('Write the polar and exponential forms', f"$z = {tex(mag)}\\angle {angd:.2f}^\\circ = {tex(mag)}\\,{eang(ang)}$."),
    ]
    st = (f"Express $z = {tex(zc)}$ in polar form and in exponential form, giving the angle in both degrees and radians. "
          f"Also write down $z z^*$.")
    steps.append(('The product with the conjugate', f"$z z^* = |z|^2 = {a*a+b*b}$, a real number, as it always is."))
    ans = f"$z = {tex(mag)}\\,{eang(ang)}$ (angle ${angd:.2f}^\\circ$), and $zz^* = {a*a+b*b}$."
    return Prob('A', st, steps, ans, 'Complex numbers')


def sifting(rng):
    kind = cyc(rng, 'sk', ['plain', 'scaled', 'outside', 'plain', 'scaled'])
    fchoice = cyc(rng, 'sf', ['poly', 'exp', 'cos'])
    if fchoice == 'poly':
        c = rng.choice([1, 2, 3, 5])
        f = t ** 2 + c
    elif fchoice == 'exp':
        a = rng.choice([1, 2, 3])
        f = sp.exp(-a * t)
    else:
        f = sp.cos(pi * t / rng.choice([2, 3, 4, 6]))
    if kind == 'plain':
        t0 = rng.choice([-2, -1, 1, 2, 3])
        st = f"Evaluate $\\displaystyle\\int_{{-\\infty}}^{{\\infty}} \\left({tex(f)}\\right)\\delta(t {'-' if t0 > 0 else '+'} {abs(t0)})\\,dt$."
        val = sp.nsimplify(f.subs(t, t0))
        steps = [('Find where the impulse fires', f"The argument $t {'-' if t0 > 0 else '+'} {abs(t0)}$ is zero at $t = {t0}$."),
                 ('Apply the sifting property', f"The integral simply picks out the value of the multiplying function at that instant: "
                  f"$f({t0}) = {tex(val)}$.")]
    elif kind == 'scaled':
        a_ = rng.choice([2, 3, 4, -2, -3])
        b_ = rng.choice([1, 2, 3, 4, 6]) * rng.choice([1, -1])
        t0 = sp.Rational(b_, a_)
        st = f"Evaluate $\\displaystyle\\int_{{-\\infty}}^{{\\infty}} \\left({tex(f)}\\right)\\delta({a_}t {'-' if b_ > 0 else '+'} {abs(b_)})\\,dt$."
        val = sp.nsimplify(f.subs(t, t0) / abs(a_))
        steps = [('Spot the scaling trap', "An impulse with a scaled argument is not the same as an ordinary impulse. "
                  "The rule is $\\delta(at - b) = \\dfrac{1}{|a|}\\,\\delta\\!\\left(t - \\dfrac{b}{a}\\right)$."),
                 ('Locate the impulse', f"The argument vanishes at $t = {b_}/{a_ if a_ > 0 else '(' + str(a_) + ')'} = {tex(t0)}$, and $|a| = {abs(a_)}$."),
                 ('Sift', f"The integral equals $\\dfrac{{1}}{{{abs(a_)}}} f\\!\\left({tex(t0)}\\right) = \\dfrac{{1}}{{{abs(a_)}}}\\left({tex(sp.nsimplify(f.subs(t, t0)))}\\right) = {tex(val)}$.")]
    else:
        t0 = rng.choice([3, 4, 5, -3, -4])
        lo, hi = (-2, 2)
        st = f"Evaluate $\\displaystyle\\int_{{{lo}}}^{{{hi}}} \\left({tex(f)}\\right)\\delta(t {'-' if t0 > 0 else '+'} {abs(t0)})\\,dt$."
        val = 0
        steps = [('Locate the impulse', f"The impulse sits at $t = {t0}$."),
                 ('Check the limits', f"The range of integration is $[{lo}, {hi}]$, which does not contain $t = {t0}$. "
                  "The integrand is therefore zero everywhere on the interval, and no amount of algebra on $f(t)$ changes that.")]
    ans = f"${tex(val)}" + ('$' if sp.nsimplify(val).is_Rational else f" \\approx {dec(val, 4)}$")
    return Prob('A', st, steps, ans, 'Impulse sifting')


def dt_energy_even(rng):
    vals = [rng.choice([-3, -2, -1, 1, 2, 3, 4]) for _ in range(4)]
    start = rng.choice([-1, 0, -2])
    nn = list(range(start, start + 4))
    x = dict(zip(nn, vals))
    E = sum(v * v for v in vals)
    M = max(abs(start), start + 3)
    rngn = list(range(-M, M + 1))
    xe = [sp.Rational(x.get(m, 0) + x.get(-m, 0), 2) for m in rngn]
    xo = [sp.Rational(x.get(m, 0) - x.get(-m, 0), 2) for m in rngn]
    st = (f"A discrete-time signal is $x[n] = {seq_tex(vals, start)}$, where the arrow marks $n = 0$ and all other samples are zero. "
          "Find its energy, and its even and odd parts.")
    steps = [
        ('Energy', f"$E = \\sum_n |x[n]|^2 = " + ' + '.join(f'{v*v}' for v in vals) + f" = {E}$."),
        ('Reflect the signal', f"Write $x[-n]$ by reading the samples backwards about $n=0$. Both $x[n]$ and $x[-n]$ then live on $-{M} \\le n \\le {M}$."),
        ('Even part', f"$x_e[n] = \\tfrac12(x[n] + x[-n]) = {seq_tex(xe, -M)}$."),
        ('Odd part', f"$x_o[n] = \\tfrac12(x[n] - x[-n]) = {seq_tex(xo, -M)}$. "
         "As a check, $x_e[n] + x_o[n]$ returns the original samples, and $x_o[0] = 0$ as it must."),
    ]
    ans = f"$E = {E}$; $x_e[n] = {seq_tex(xe, -M)}$; $x_o[n] = {seq_tex(xo, -M)}$."
    return Prob('A', st, steps, ans, 'Energy and symmetry')


# ---------------------------------------------------------------- B level
def ct_period(rng):
    irr = rng.random() < 0.18
    fns = ['\\cos', '\\sin']
    if irr:
        a = rng.choice([1, 2, 3])
        b = rng.choice([1, 2, 3])
        st = f"Is $x(t) = \\cos({a if a > 1 else ''}t) + \\sin({b if b > 1 else ''}\\pi t)$ periodic? If so, find its fundamental period."
        steps = [('Individual periods', f"$T_1 = 2\\pi/{a}$ and $T_2 = 2/{b}$."),
                 ('Ratio test', f"The sum is periodic only if $T_1/T_2$ is rational. Here $T_1/T_2 = {b}\\pi/{a}$, which is irrational because $\\pi$ is."),
                 ('Conclusion', "No common period exists, so the sum never repeats exactly, even though each term does.")]
        return Prob('B', st, steps, "Not periodic: the ratio of periods involves $\\pi$.", 'Periodicity (CT)')
    pool = [Q(1), Q(2), Q(3), Q(4), Q(5), Q(6), Q(8), Q(1, 2), Q(3, 2), Q(2, 3), Q(4, 3), Q(5, 2), Q(10), Q(12), Q(9), Q(15)]
    cpi = cyc(rng, 'cpi', [pi, pi, 1, pi, 1])
    r1, r2 = rng.sample(pool, 2)
    three = rng.random() < 0.3
    rs = [r1, r2] + ([rng.choice([r for r in pool if r not in (r1, r2)])] if three else [])
    names = [rng.choice(fns) for _ in rs]
    amps = [rng.choice([1, 2, 3, 4]) for _ in rs]
    terms = [f"{a if a > 1 else ''}{nm}({tex(r*cpi) if r*cpi != 1 else ''} t)" for a, nm, r in zip(amps, names, rs)]
    st = f"Determine whether $x(t) = {' + '.join(terms)}$ is periodic and, if it is, find its fundamental period $T_0$ and fundamental frequency $\\omega_0$."
    Ts = [2 * pi / (r * cpi) for r in rs]
    # gcd of rationals for omegas
    from math import gcd
    from functools import reduce
    nums = [r.p for r in rs]
    dens = [r.q for r in rs]
    gnum = reduce(gcd, nums)
    lden = reduce(lambda a, b: a * b // gcd(a, b), dens)
    w0 = Q(gnum, lden)  # times pi
    T0 = 2 * pi / (w0 * cpi)
    steps = [('Individual periods', 'For a term $\\cos(\\omega t)$ or $\\sin(\\omega t)$ the period is $2\\pi/\\omega$. So ' +
              ', '.join(f"$T_{i+1} = 2\\pi/{tex(r*cpi)} = {tex(T)}$" for i, (r, T) in enumerate(zip(rs, Ts))) + '.'),
             ('Check the ratios', 'Every ratio of these periods is a ratio of rational numbers, so a common period exists and the sum is periodic.'),
             ('Fundamental frequency', f"The frequencies are integer multiples of the largest frequency that divides them all. "
              f"Here that is $\\omega_0 = {tex(w0*cpi)}$ rad/s: " + ', '.join(f"${tex(r*cpi)} = {r/w0}\\,\\omega_0$" for r in rs) + '.'),
             ('Fundamental period', f"$T_0 = 2\\pi/\\omega_0 = {tex(T0)}$ s. Check: $T_0$ is a whole number of each individual period ("
              + ', '.join(f"{T0/T}\\times" if False else f"${tex(T0/T)}$ periods of term {i+1}" for i, T in enumerate(Ts)) + ').')]
    ans = f"Periodic, with $T_0 = {tex(T0)}$ s and $\\omega_0 = {tex(w0*cpi)}$ rad/s."
    return Prob('B', st, steps, ans, 'Periodicity (CT)')


def dt_period(rng):
    if rng.random() < 0.2:
        a = rng.choice([2, 3, 4, 5])
        st = f"Is $x[n] = \\cos(n/{a})$ periodic? Explain."
        steps = [('Condition for discrete-time periodicity', "We need an integer $N$ with $\\omega_0 N = 2\\pi m$ for some integer $m$, i.e. $\\omega_0/2\\pi$ must be rational."),
                 ('Apply it', f"Here $\\omega_0/2\\pi = 1/({2*a}\\pi)$, which is irrational."),
                 ('Conclusion', "No integer $N$ works. The samples come from a periodic continuous cosine, yet the sequence itself never repeats, a genuinely discrete-time phenomenon.")]
        return Prob('B', st, steps, "Not periodic, because $\\omega_0/2\\pi$ is irrational.", 'Periodicity (DT)')

    def nper(r):  # omega = r*pi
        p, q = r.p, r.q
        from math import gcd
        return 2 * q // gcd(p, 2 * q)
    pool = [Q(1, 2), Q(1, 3), Q(2, 3), Q(1, 4), Q(3, 4), Q(1, 5), Q(2, 5), Q(1, 6), Q(5, 6), Q(3, 8), Q(1, 8), Q(4, 5), Q(3, 5), Q(5, 4), Q(7, 6)]
    two = rng.random() < 0.6
    rs = rng.sample(pool, 2 if two else 1)
    Ns = [nper(r) for r in rs]
    from math import lcm
    N = lcm(*Ns)
    names = [rng.choice(['\\cos', '\\sin']) for _ in rs]
    terms = [f"{nm}\\left({tex(r*pi)} n\\right)" for nm, r in zip(names, rs)]
    st = f"Find the fundamental period of $x[n] = {' + '.join(terms)}$."
    steps = [('Condition', "A discrete sinusoid $\\cos(\\omega_0 n)$ repeats after $N$ samples when $\\omega_0 N = 2\\pi m$ for integers $N, m$. "
              "The smallest such $N$ is the period, and $N = 2\\pi m/\\omega_0$ must be an integer.")]
    for i, (r, Nn) in enumerate(zip(rs, Ns)):
        steps.append((f'Term {i+1}', f"$\\omega_0/2\\pi = {tex(r)}/2 = {tex(r/2)}$. Writing this as $m/N$ in lowest terms gives $N_{i+1} = {Nn}$."))
    if two:
        steps.append(('Combine', f"The sum repeats when both terms do, so $N = \\operatorname{{lcm}}({Ns[0]}, {Ns[1]}) = {N}$."))
    steps.append(('Watch out', "Notice that $2\\pi/\\omega_0$ need not itself be an integer; the period is the smallest integer multiple of it that is."))
    return Prob('B', st, steps, f"$N_0 = {N}$ samples.", 'Periodicity (DT)')


def energy_power(rng):
    case = cyc(rng, 'ep', ['exp', 'cos', 'twocos', 'cexp', 'geo', 'rect', 'dexp'])
    A = rng.choice([2, 3, 4, 5])
    if case == 'exp':
        a = rng.choice([1, 2, 3, 4, Q(1, 2)])
        st = f"Classify $x(t) = {A}{expo(a)}u(t)$ as an energy signal, a power signal or neither, and find $E$ or $P$ as appropriate."
        E = sp.Rational(A * A) / (2 * a)
        steps = [('Set up the energy integral', f"$E = \\int_0^\\infty {A*A}{expo(2*a)}\\,dt$."),
                 ('Integrate', f"$E = {A*A}\\left[\\dfrac{{{expo(2*a)}}}{{-{tex(2*a)}}}\\right]_0^\\infty = \\dfrac{{{A*A}}}{{{tex(2*a)}}} = {tex(E)}$."),
                 ('Classify', "The energy is finite and non-zero, so this is an energy signal and its average power is zero.")]
        ans = f"Energy signal, $E = {tex(E)}$, $P = 0$."
    elif case == 'cos':
        wv = rng.choice([2, 5, 10, 100]) * pi
        st = f"Find the average power of $x(t) = {A}\\cos({tex(wv)}t + \\pi/{rng.choice([3, 4, 6])})$ and say whether it is an energy or a power signal."
        steps = [('Use one period', f"For a periodic signal the average power is the mean of $|x|^2$ over one period, $T_0 = 2\\pi/{tex(wv)}$."),
                 ('Square the cosine', f"$x^2(t) = {A*A}\\cos^2(\\cdot) = \\tfrac{{{A*A}}}{{2}}\\left[1 + \\cos(2\\cdot)\\right]$. The second term averages to zero over a period."),
                 ('Result', f"$P = {A*A}/2 = {tex(Q(A*A, 2))}$. Phase and frequency play no part."),
                 ('Classify', "Its energy over all time is infinite, so it is a power signal.")]
        ans = f"Power signal, $P = {tex(Q(A*A, 2))}$."
    elif case == 'twocos':
        B = rng.choice([1, 2, 3, 6])
        w1, w2 = rng.sample([1, 2, 3, 5, 7], 2)
        st = f"Find the average power of $x(t) = {A}\\cos({w1 if w1 > 1 else ''}t) + {B}\\sin({w2 if w2 > 1 else ''}t)$."
        P = Q(A * A + B * B, 2)
        steps = [('Expand the square', f"$x^2 = {A*A}\\cos^2({w1}t) + {B*B}\\sin^2({w2}t) + {2*A*B}\\cos({w1}t)\\sin({w2}t)$."),
                 ('Average term by term', "The squared terms average to half their peak value. The cross term is a sum of sinusoids at $\\omega_1 \\pm \\omega_2$, neither of which is zero because the frequencies differ, so it averages to zero."),
                 ('Add the powers', f"$P = \\tfrac{{{A*A}}}{{2}} + \\tfrac{{{B*B}}}{{2}} = {tex(P)}$. Powers of sinusoids at different frequencies simply add.")]
        ans = f"$P = {tex(P)}$."
    elif case == 'cexp':
        wv = rng.choice([3, 4, 10, 20])
        st = f"Show that $x(t) = {A}e^{{j{wv}t}}$ is a power signal and find its average power."
        steps = [('Magnitude', f"$|x(t)| = {A}|e^{{j{wv}t}}| = {A}$ for every $t$."),
                 ('Average', f"$P = \\lim_{{T\\to\\infty}}\\frac{{1}}{{2T}}\\int_{{-T}}^{{T}} {A*A}\\,dt = {A*A}$."),
                 ('Comment', "Unlike a real cosine of amplitude A, whose power is $A^2/2$, the complex exponential carries the full $A^2$ because its magnitude never dips.")]
        ans = f"$P = {A*A}$; infinite energy, so a power signal."
    elif case == 'geo':
        a = rng.choice([Q(1, 2), Q(1, 3), -Q(1, 2), Q(3, 4), -Q(2, 3), Q(2, 3)])
        st = f"Find the energy of $x[n] = {A}\\left({tex(a)}\\right)^n u[n]$."
        E = sp.Rational(A * A) / (1 - a * a)
        steps = [('Square the samples', f"$|x[n]|^2 = {A*A}\\left({tex(a*a)}\\right)^n$ for $n \\ge 0$; the sign of the ratio disappears on squaring."),
                 ('Sum the geometric series', f"$E = {A*A}\\sum_{{n=0}}^\\infty \\left({tex(a*a)}\\right)^n = \\dfrac{{{A*A}}}{{1 - {tex(a*a)}}} = {tex(E)}$."),
                 ('Classify', "Finite energy, so an energy signal with zero average power.")]
        ans = f"$E = {tex(E)}$" + ('' if E.is_Integer else f" $\\approx {dec(E)}$") + '.'
    elif case == 'rect':
        T = rng.choice([2, 3, 4, 5])
        st = f"Find the energy of the pulse $x(t) = {A}\\left[u(t) - u(t - {T})\\right]$."
        steps = [('Describe the pulse', f"The signal equals ${A}$ on $0 \\le t < {T}$ and zero elsewhere."),
                 ('Integrate', f"$E = \\int_0^{{{T}}} {A*A}\\,dt = {A*A*T}$.")]
        ans = f"$E = {A*A*T}$, an energy signal."
    elif case == 'dexp':
        a = rng.choice([1, 2, 3, 4])
        E = Q(A * A, a)
        st = f"Find the energy of the two-sided exponential $x(t) = {A}{expo(a, '|t|')}$."
        steps = [('Use symmetry', f"The signal is even, so $E = 2\\int_0^\\infty {A*A}{expo(2*a)}\\,dt$."),
                 ('Integrate', f"$E = 2 \\cdot \\dfrac{{{A*A}}}{{{2*a}}} = {tex(E)}$.")]
        ans = f"$E = {tex(E)}$."
    return Prob('B', st, steps, ans, 'Energy and power')


def even_odd_ct(rng):
    case = cyc(rng, 'eo', ['exp', 'poly', 'ramp', 'grow'])
    A = rng.choice([2, 3, 4, 6])
    if case == 'exp':
        a = rng.choice([1, 2, 3, 5])
        st = f"Find the even and odd parts of $x(t) = {A}{expo(a)}u(t)$."
        steps = [('Reflect', f"$x(-t) = {A}{expo(-a)}u(-t)$, which lives on $t<0$."),
                 ('Even part', f"$x_e(t) = \\tfrac12[x(t) + x(-t)] = {tex(Q(A, 2))}{expo(a, '|t|')}$, a symmetric double exponential."),
                 ('Odd part', f"$x_o(t) = \\tfrac12[x(t) - x(-t)] = {tex(Q(A, 2))}\\left[{expo(a)}u(t) - {expo(-a)}u(-t)\\right] = {tex(Q(A, 2))}\\operatorname{{sgn}}(t)\\,{expo(a, '|t|')}$."),
                 ('Check', "For $t>0$ the two parts add to $A e^{-at}$; for $t<0$ they cancel, as they should.")]
        ans = f"$x_e = {tex(Q(A, 2))}{expo(a, '|t|')}$, $x_o = {tex(Q(A, 2))}\\operatorname{{sgn}}(t){expo(a, '|t|')}$."
    elif case == 'poly':
        cs = [rng.choice([-3, -2, -1, 1, 2, 3, 4]) for _ in range(4)]
        wv = rng.choice([2, 3, 5])
        x = cs[0] * t ** 3 + cs[1] * t ** 2 + cs[2] * sp.sin(wv * t) + cs[3] * sp.cos(wv * t)
        xe = cs[1] * t ** 2 + cs[3] * sp.cos(wv * t)
        xo = cs[0] * t ** 3 + cs[2] * sp.sin(wv * t)
        st = f"Split $x(t) = {tex(x)}$ into its even and odd parts."
        steps = [('Know the building blocks', "Even powers of $t$ and cosines are even; odd powers and sines are odd."),
                 ('Reflect', f"$x(-t) = {tex(x.subs(t, -t))}$."),
                 ('Average and difference', f"$x_e = \\tfrac12[x(t)+x(-t)] = {tex(xe)}$ and $x_o = \\tfrac12[x(t)-x(-t)] = {tex(xo)}$.")]
        ans = f"$x_e(t) = {tex(xe)}$, $x_o(t) = {tex(xo)}$."
    elif case == 'ramp':
        st = f"Find the even and odd parts of the ramp $r(t) = {A}t\\,u(t)$ and sketch them mentally."
        steps = [('Reflect', f"$r(-t) = -{A}t\\,u(-t)$, which is positive for $t<0$."),
                 ('Even part', f"$r_e(t) = \\tfrac{{{A}}}{{2}}\\left[t u(t) - t u(-t)\\right] = {tex(Q(A, 2))}|t|$, a V shape."),
                 ('Odd part', f"$r_o(t) = \\tfrac{{{A}}}{{2}}\\left[t u(t) + t u(-t)\\right] = {tex(Q(A, 2))}t$, a straight line through the origin.")]
        ans = f"$r_e = {tex(Q(A, 2))}|t|$, $r_o = {tex(Q(A, 2))}t$."
    else:
        b = rng.choice([1, 2, 3])
        st = f"Find the even and odd parts of $x(t) = {A}e^{{{b if b > 1 else ''}t}}$ and identify them as hyperbolic functions."
        steps = [('Reflect', f"$x(-t) = {A}e^{{-{b if b > 1 else ''}t}}$."),
                 ('Even part', f"$x_e = \\tfrac{{{A}}}{{2}}(e^{{{b}t}} + e^{{-{b}t}}) = {A}\\cosh({b}t)$."),
                 ('Odd part', f"$x_o = \\tfrac{{{A}}}{{2}}(e^{{{b}t}} - e^{{-{b}t}}) = {A}\\sinh({b}t)$.")]
        ans = f"$x_e = {A}\\cosh({b}t)$, $x_o = {A}\\sinh({b}t)$."
    return Prob('B', st, steps, ans, 'Even and odd parts')


def plot_pw(points, name, title, xlabel='t', ylabel='x(t)', color=fs.NAVY, steps_style=False):
    fig, ax = plt.subplots(figsize=(4.2, 1.9))
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ax.plot(xs, ys, color=color)
    ax.set_xlabel(f'${xlabel}$', loc='right')
    ax.set_title(f'${ylabel}$', loc='left', fontsize=9)
    lo, hi = min(xs), max(xs)
    ax.set_xlim(lo - 0.3, hi + 0.3)
    ax.axhline(0, color=fs.INK, lw=0.7)
    ax.set_xticks(sorted(set([round(v, 3) for v in xs[1:-1]])))
    ymin = min(0, min(ys)) - 0.5
    ymax = max(ys) + 0.5
    ax.set_ylim(ymin, ymax)
    return save_fig(fig, name)


def step_repr(rng):
    t0 = rng.choice([-2, -1, 0, 1])
    widths = [rng.choice([1, 2]) for _ in range(3)]
    tb = [t0, t0 + widths[0], t0 + widths[0] + widths[1], t0 + sum(widths)]
    lv = rng.sample([-2, -1, 1, 2, 3, 4], 3)
    pts = [(tb[0] - 1.5, 0), (tb[0], 0)]
    for i in range(3):
        pts += [(tb[i], lv[i]), (tb[i + 1], lv[i])]
    pts += [(tb[3], 0), (tb[3] + 1.5, 0)]
    name = new_fig_name('ch01_step')
    path = plot_pw(pts, name, '')
    jumps = [lv[0], lv[1] - lv[0], lv[2] - lv[1], -lv[2]]
    expr = combo([(c, f"u(t {'-' if b > 0 else '+'} {abs(b)})" if b != 0 else 'u(t)') for c, b in zip(jumps, tb)])
    st = (f"The staircase signal in the figure takes the value ${lv[0]}$ on ${tb[0]} \\le t < {tb[1]}$, ${lv[1]}$ on ${tb[1]} \\le t < {tb[2]}$ "
          f"and ${lv[2]}$ on ${tb[2]} \\le t < {tb[3]}$, and is zero elsewhere. Write it as a sum of shifted unit steps.")
    steps = [('Read the jumps, not the levels', "Each unit step contributes a jump at its switch-on time, so the coefficient of each step is the size of the jump there, measured left to right."),
             ('List the jumps', ', '.join(f"at $t = {b}$ the signal jumps by ${c}$" for b, c in zip(tb, jumps)) + '.'),
             ('Assemble', f"$x(t) = {expr}$."),
             ('Check', "The coefficients sum to zero, which is exactly what we need for the signal to return to zero on the far right.")]
    return Prob('B', st, steps, f"$x(t) = {expr}$.", 'Step representation', fig=(path, 'The staircase signal.'))


# ---------------------------------------------------------------- C level
SHAPES = [
    [(-1, 0), (0, 2), (2, 2), (3, 0)],
    [(0, 0), (1, 2), (2, 0)],
    [(-2, 0), (-1, 1), (1, 1), (2, 0)],
    [(0, 0), (0, 1), (2, 1), (3, 0)],
    [(-1, 0), (1, 2), (1, 0)],
]


def time_transform(rng):
    shape = cyc(rng, 'sh', SHAPES)
    a = rng.choice([2, Q(1, 2), -1, -2, -Q(1, 2), 3])
    b = rng.choice([-3, -2, -1, 1, 2, 4])
    pts = [(Q(p[0]), Q(p[1])) for p in shape]
    full = [(pts[0][0] - 1, 0)] + pts + [(pts[-1][0] + 1, 0)]
    name = new_fig_name('ch01_tt')
    path = plot_pw([(float(x), float(y)) for x, y in full], name, '')
    newpts = sorted([((p[0] - b) / a, p[1]) for p in pts], key=lambda q: (q[0]))
    if a < 0:
        newpts = [((p[0] - b) / a, p[1]) for p in reversed(pts)]
    nfull = [(newpts[0][0] - 1, 0)] + newpts + [(newpts[-1][0] + 1, 0)]
    sname = new_fig_name('ch01_tts')
    spath = plot_pw([(float(x), float(y)) for x, y in nfull], sname, '', ylabel='y(t)', color=fs.RUST)
    arg = f"{tex(a) if a not in (1, -1) else ('-' if a == -1 else '')}t {'+' if b > 0 else '-'} {abs(b)}"
    st = (f"A piecewise-linear signal $x(t)$ is shown in the figure; its corners are at "
          + ', '.join(f"$({tex(p[0])}, {tex(p[1])})$" for p in pts)
          + f". Sketch $y(t) = x({arg})$ and list the corner points of $y(t)$.")
    rows = ' \\\\ '.join(f"{tex(p[0])} & {tex((p[0]-b)/a)} & {tex(p[1])}" for p in pts)
    steps = [('Use the corner-mapping method', f"A corner of $x$ at time $t_x$ appears in $y$ at the time $t_y$ where the argument equals $t_x$: "
              f"${arg} = t_x$, so $t_y = (t_x {'-' if b > 0 else '+'} {abs(b)})/{tex(a) if a > 0 else '(' + tex(a) + ')'}$. Heights are unchanged."),
             ('Tabulate', f"$$\\begin{{array}}{{ccc}} t_x & t_y & \\text{{height}} \\\\ \\hline {rows} \\end{{array}}$$"),
             ('Interpret', ("Because $a<0$ the signal is also flipped: the corner that was on the left of $x$ is now on the right of $y$. " if a < 0 else '')
              + ("The factor $|a|>1$ compresses the time axis. " if abs(a) > 1 else "The factor $|a|<1$ stretches the time axis. " if abs(a) < 1 else '')
              + "Join the mapped corners with straight lines to obtain the sketch in the solution figure."),
             ('A common mistake', f"Shifting by ${abs(b)}$ and then scaling the shift as well is the usual slip. Writing $y(t) = x\\big({tex(a)}(t {'+' if b/a > 0 else '-'} {tex(abs(b/a))})\\big)$ makes it clear that the true shift of the scaled signal is ${tex(abs(b/a))}$, not ${abs(b)}$.")]
    ans = "Corners of $y(t)$: " + ', '.join(f"$({tex(p[0])}, {tex(p[1])})$" for p in newpts) + '.'
    return Prob('C', st, steps, ans, 'Time transformation', fig=(path, 'The signal $x(t)$.'),
                sol_fig=(spath, f'The transformed signal $y(t) = x({arg})$.'))


def periodic_power(rng):
    case = cyc(rng, 'pp', ['saw', 'pulse', 'half', 'full', 'tri'])
    A = rng.choice([2, 3, 4, 5, 6, 10])
    if case == 'saw':
        T = rng.choice([1, 2, 4])
        st = f"A sawtooth wave rises linearly from $0$ to ${A}$ over each period of ${T}$ s, then drops back. Find its average power and RMS value."
        P = Q(A * A, 3)
        steps = [('One period', f"$x(t) = {tex(Q(A, T))}t$ on $0 \\le t < {T}$."),
                 ('Average the square', f"$P = \\dfrac{{1}}{{{T}}}\\int_0^{{{T}}} {tex(Q(A*A, T*T))}t^2\\,dt = \\dfrac{{1}}{{{T}}}\\cdot {tex(Q(A*A, T*T))}\\cdot\\dfrac{{{T}^3}}{{3}} = {tex(P)}$."),
                 ('RMS', f"$x_{{\\text{{rms}}}} = \\sqrt{{P}} = {tex(sp.sqrt(P))} \\approx {dec(sp.sqrt(P))}$. The period cancels, as you would expect.")]
    elif case == 'pulse':
        d = rng.choice([Q(1, 4), Q(1, 2), Q(1, 5), Q(1, 3)])
        st = f"A rectangular pulse train has amplitude ${A}$ and duty cycle ${tex(d)}$ (the pulse is high for a fraction ${tex(d)}$ of each period). Find its average power and RMS value."
        P = A * A * d
        steps = [('Average the square', f"Over one period $x^2$ equals ${A*A}$ for a fraction ${tex(d)}$ of the time and zero otherwise."),
                 ('Result', f"$P = {A*A}\\times{tex(d)} = {tex(P)}$, so $x_{{\\text{{rms}}}} = {tex(sp.sqrt(P))} \\approx {dec(sp.sqrt(P))}$.")]
    elif case == 'half':
        st = f"Find the average power of a half-wave rectified sine of peak value ${A}$."
        P = Q(A * A, 4)
        steps = [('Split the period', f"For half the period the signal is ${A}\\sin(\\omega_0 t)$; for the other half it is zero."),
                 ('Average', f"The mean of $\\sin^2$ over its positive half is $\\tfrac12$, and that half occupies half of the period, so $P = {A*A}\\cdot\\tfrac12\\cdot\\tfrac12 = {tex(P)}$."),
                 ('RMS', f"$x_{{\\text{{rms}}}} = {A}/2 = {tex(Q(A, 2))}$.")]
    elif case == 'full':
        st = f"Find the average power and RMS value of a full-wave rectified sine $x(t) = {A}|\\sin(\\omega_0 t)|$."
        P = Q(A * A, 2)
        steps = [('Key observation', f"$x^2(t) = {A*A}\\sin^2(\\omega_0 t)$: rectification does nothing to the square."),
                 ('Average', f"$P = {A*A}/2 = {tex(P)}$ and $x_{{\\text{{rms}}}} = {A}/\\sqrt2 \\approx {dec(A/sp.sqrt(2))}$, the same as the unrectified sine.")]
    else:
        st = f"A symmetric triangular wave swings between $-{A}$ and $+{A}$. Find its average power."
        P = Q(A * A, 3)
        steps = [('Quarter-period argument', f"Over a quarter period the wave is a straight line from $0$ to ${A}$, and by symmetry every quarter has the same mean square."),
                 ('Average', f"The mean of $({A}\\theta)^2$ for $\\theta$ uniform on $[0,1]$ is ${A*A}/3$, so $P = {tex(P)}$.")]
    return Prob('C', st, steps, f"$P = {tex(P)}$" + (f", RMS $\\approx {dec(sp.sqrt(P))}$." if True else '.'), 'Power of periodic waves')


TEMPLATES = [(sinusoid, 5), (complex_polar, 4), (sifting, 5), (dt_energy_even, 4),
             (ct_period, 6), (dt_period, 5), (energy_power, 6), (even_odd_ct, 4), (step_repr, 4),
             (time_transform, 4), (periodic_power, 3)]


def generate():
    return build_set(TEMPLATES, seed=101)


if __name__ == '__main__':
    for i, p in enumerate(generate(), 1):
        print(f'--- 1.{i} [{p.level}] {p.topic}\n{p.statement}\n  ANS: {p.answer}')
