"""Chapter 11 - Inverse Z-transform and difference equations."""
import sympy as sp
from core import *
from zt import izt, series

CH = 11
H_ = Q(1, 2)
POOL = [H_, Q(1, 3), Q(1, 4), -H_, Q(3, 4), -Q(1, 3), Q(2, 3), Q(1, 5)]


def zfrac(X):
    return tex(sp.factor(X))


def seq_check(X, r, N=4):
    a = series(X, N)
    b = [r['seq'](m) for m in range(N)]
    assert a == b, (X, a, b)
    return a


def by_inspection(rng):
    L = rng.choice([3, 4, 5])
    c = [rng.choice([-3, -2, -1, 0, 1, 2, 4]) for _ in range(L)]
    c[0] = c[0] or 1
    c[-1] = c[-1] or 2
    sh = rng.choice([0, 0, 1])
    X = zpoly_tex(c)
    if sh:
        X = f"z\\left({X}\\right)"
    st = f"Find the sequence whose Z-transform is $$X(z) = {X},$$ with ROC all $z$ except $0$" + (' and $\\infty$' if sh else '') + '.'
    vals = c
    start = -sh
    steps = [('Read off the coefficients', 'For a polynomial in $z^{-1}$ the coefficient of $z^{-n}$ is simply $x[n]$; no partial fractions are needed.')]
    if sh:
        steps.append(('Account for the factor $z$', 'Multiplying by $z$ advances the sequence by one sample, so every index decreases by one.'))
    steps.append(('Write the sequence', f"$x[n] = {seq_tex(vals, start)}$."))
    return Prob('A', st, steps, f"$x[n] = {seq_tex(vals, start)}$.", 'Inverse by inspection')


def distinct(rng):
    a, b = rng.sample(POOL, 2)
    A = rng.choice([1, 2, 3])
    form = cyc(rng, 'df', ['z2', 'z', 'zinv'])
    if form == 'z2':
        X = A * z ** 2 / ((z - a) * (z - b))
    elif form == 'z':
        X = A * z / ((z - a) * (z - b))
    else:
        X = (z ** 2 + rng.choice([1, -1, 2]) * z) / ((z - a) * (z - b))
    r = izt(X)
    first = seq_check(X, r)
    st = f"Find the causal sequence $x[n]$ with $X(z) = {zfrac(X)}$."
    steps = [('Divide by $z$ first', 'Expanding $X(z)/z$ rather than $X(z)$ leaves a factor $z$ on every term at the end, which matches the table entry $\\dfrac{z}{z - a} \\leftrightarrow a^n u[n]$.'),
             ('Partial fractions', f"$\\dfrac{{X(z)}}{{z}} = {r['pf']}$.")]
    steps += [(f'Term {i+1}', d) for i, d in enumerate(r['descs'])]
    steps.append(('Check', f"Long division gives $x[0..3] = {', '.join(tex(v) for v in first)}$, matching the formula."))
    return Prob('A', st, steps, f"$x[n] = \\left({combo(r['pairs'])}\\right)u[n]$.", 'Distinct poles')


def roc_dependent(rng):
    a, b = rng.choice([(H_, 2), (Q(1, 3), 3), (Q(1, 2), 3), (Q(1, 4), 2)])
    X = z ** 2 / ((z - a) * (z - b))
    which = cyc(rng, 'rd', ['ring', 'out', 'in'])
    rC = izt(X, causal=True)
    pf = rC['pf']
    A = sp.nsimplify(sp.limit((z - a) * X / z, z, a))
    B = sp.nsimplify(sp.limit((z - b) * X / z, z, b))
    roc = {'ring': f"{tex(a)} < |z| < {tex(b)}", 'out': f"|z| > {tex(b)}", 'in': f"|z| < {tex(a)}"}[which]
    st = f"Find $x[n]$ for $X(z) = {zfrac(X)}$ with ROC ${roc}$."
    rightA = which in ('ring', 'out')
    rightB = which == 'out'
    pairs = [(A if rightA else -A, f"\\left({tex(a)}\\right)^n u[{'n' if rightA else '-n-1'}]"),
             (B if rightB else -B, f"\\left({tex(b)}\\right)^n u[{'n' if rightB else '-n-1'}]")]
    xs = combo(pairs)
    steps = [('Partial fractions', f"$\\dfrac{{X(z)}}{{z}} = {pf}$, so $X(z) = \\dfrac{{{tex(A)}z}}{{z - {tex(a)}}} + \\dfrac{{{tex(B)}z}}{{z - {tex(b)}}}$."),
             ('Match each pole to the ROC', f"The ROC lies {'outside' if which in ('ring', 'out') else 'inside'} the pole at ${tex(a)}$, so that term is {'right' if which in ('ring', 'out') else 'left'}-sided; it lies {'outside' if which == 'out' else 'inside'} the pole at ${tex(b)}$, so that term is {'right' if which == 'out' else 'left'}-sided."),
             ('Assemble', f"$x[n] = {xs}$."),
             ('Stability', 'Stable' if which == 'ring' else 'Not stable', )]
    steps[-1] = ('Stability', 'This ROC contains the unit circle, so this is the only stable choice.' if which == 'ring' else 'This ROC does not contain the unit circle, so the sequence is not absolutely summable.')
    ans = f"$x[n] = {xs}$."
    return Prob('B', st, steps, ans, 'The role of the ROC')


def repeated(rng):
    a = rng.choice([H_, Q(1, 3), -H_, Q(1, 4)])
    form = cyc(rng, 'rp', ['pure', 'step', 'mixed'])
    if form == 'pure':
        X = z ** 2 / (z - a) ** 2
    elif form == 'step':
        X = z ** 2 / ((z - a) ** 2) * 1 if False else z ** 2 / ((z - 1) * (z - a)) * z / (z - a) / z * z
        X = z ** 2 / ((z - 1) * (z - a)) if False else z / ((z - 1) * (z - a) ** 2) * z
    else:
        b = rng.choice([v for v in POOL if v != a])
        X = z ** 2 / ((z - a) ** 2 * (z - b)) * z
    X = sp.together(X)
    r = izt(X)
    first = seq_check(X, r)
    st = f"Find the causal sequence with $X(z) = {zfrac(X)}$."
    steps = [('Repeated pole', f"The factor $(z - {par(a)})^2$ needs terms in both $\\dfrac{{z}}{{z - a}}$ and $\\dfrac{{z}}{{(z - a)^2}}$; the second gives $n a^{{n-1}}u[n]$."),
             ('Partial fractions of $X/z$', f"${r['pf']}$.")]
    steps += [(f'Term {i+1}', d) for i, d in enumerate(r['descs'])]
    steps.append(('Check', f"First samples: ${', '.join(tex(v) for v in first)}$."))
    return Prob('B', st, steps, f"$x[n] = \\left({combo(r['pairs'])}\\right)u[n]$.", 'Repeated poles')


def long_div(rng):
    a, b = rng.sample(POOL[:5], 2)
    X = (z ** 2 + rng.choice([1, 2, -1]) * z) / ((z - a) * (z - b))
    vals = series(X, 5)
    st = f"Use long division to find the first five samples of the causal sequence with $X(z) = {zfrac(X)}$."
    den = sp.expand((z - a) * (z - b))
    steps = [('Write in powers of $z^{-1}$', f"Divide numerator and denominator by $z^2$: $X = \\dfrac{{{zpoly_tex(sp.Poly(sp.expand(sp.fraction(sp.together(X))[0]), z).all_coeffs())}}}{{{zpoly_tex(sp.Poly(den, z).all_coeffs())}}}$ (after dividing through)."),
             ('Divide', 'Divide as with ordinary polynomials, but in ascending powers of $z^{-1}$, so that the quotient is $x[0] + x[1]z^{-1} + x[2]z^{-2} + \\cdots$.'),
             ('Equivalently, recurse', f"The denominator corresponds to the recursion $x[n] = {combo([(a + b, 'x[n-1]'), (-a*b, 'x[n-2]')])} + (\\text{{input terms from the numerator}})$, which generates the same numbers."),
             ('Samples', ', '.join(f"$x[{m}] = {tex(v)}$" for m, v in enumerate(vals)) + '.')]
    return Prob('B', st, steps, ', '.join(f"$x[{m}] = {tex(v)}$" for m, v in enumerate(vals)) + '.', 'Long division')


def complex_z(rng):
    r0, th = rng.choice([(H_, pi / 3), (1, pi / 2), (H_, pi / 2), (1, pi / 3), (Q(1, 3), pi / 2), (sp.sqrt(2) / 2, pi / 4)])
    a1 = -2 * r0 * sp.cos(th)
    a0 = r0 ** 2
    den = z ** 2 + a1 * z + a0
    form = cyc(rng, 'cz', ['z2', 'z'])
    X = (z ** 2 if form == 'z2' else z) / den
    X = sp.nsimplify(X)
    r = izt(X)
    first = seq_check(X, r)
    st = f"Find the causal sequence with $X(z) = {tex(X)}$."
    steps = [('Poles', f"The denominator has complex roots $z = {tex(r0)}e^{{\\pm j{tex(th)}}}$, so expect a {'damped ' if r0 != 1 else ''}sinusoid."),
             ('Method', r['descs'][-1]),
             ('Check', f"First samples by long division: ${', '.join(tex(v) for v in first)}$.")]
    return Prob('B', st, steps, f"$x[n] = \\left({combo(r['pairs'])}\\right)u[n]$.", 'Complex poles')


def first_order(rng):
    a = cyc(rng, 'fa', [H_, Q(1, 3), -H_, Q(3, 4), Q(1, 4)])
    y0 = rng.choice([1, 2, 4, -2])
    inp = rng.choice(['step', 'delta', 'geo'])
    K = rng.choice([1, 2, 3])
    if inp == 'step':
        Xz, xin = K * z / (z - 1), f"{cf(K)}u[n]"
    elif inp == 'delta':
        Xz, xin = sp.Integer(K), f"{cf(K)}\\delta[n]"
    else:
        b = rng.choice([v for v in POOL if v != a])
        Xz, xin = K * z / (z - b), f"{cf(K)}\\left({tex(b)}\\right)^n u[n]"
    Y = sp.together((Xz + a * y0) / (1 - a / z))
    r = izt(Y)
    first = seq_check(Y, r)
    st = f"Solve $y[n] - {par(a)}y[n-1] = {xin}$ for $n \\ge 0$, given $y[-1] = {y0}$."
    steps = [('Unilateral shift rule', '$y[n-1] \\leftrightarrow z^{-1}Y(z) + y[-1]$.'),
             ('Transform', f"$Y - {par(a)}(z^{{-1}}Y + {y0}) = X(z)$, with $X(z) = {tex(Xz)}$."),
             ('Solve', f"$Y(z) = \\dfrac{{X(z) + {tex(a*y0)}}}{{1 - {par(a)}z^{{-1}}}} = {zfrac(Y)}$."),
             ('Partial fractions of $Y/z$', f"${r['pf']}$.")]
    steps += [('Invert', ' '.join(r['descs']))]
    steps.append(('Check by recursion', f"$y[0] = {tex(a)}\\cdot{y0} + x[0] = {tex(first[0])}$, $y[1] = {tex(first[1])}$, $y[2] = {tex(first[2])}$; the formula agrees."))
    return Prob('B', st, steps, f"$y[n] = {combo(r['pairs'])}$ for $n \\ge 0$.", 'First-order difference equations')


def second_order(rng):
    kind = cyc(rng, 'so', ['real', 'real', 'rep', 'real', 'rep', 'real', 'real', 'rep'])
    if kind == 'real':
        p1, p2 = rng.sample(POOL[:6], 2)
    else:
        p1 = p2 = rng.choice([H_, Q(1, 3), -H_])
    a1, a2 = -(p1 + p2), p1 * p2
    y1, y2 = rng.choice([0, 1, 2]), rng.choice([0, 1, -1])
    inp = rng.choice(['step', 'zero', 'step'])
    K = rng.choice([1, 2])
    Xz = K * z / (z - 1) if inp == 'step' else 0
    if inp == 'zero' and y1 == 0 and y2 == 0:
        y1 = 1
    # Y(1 + a1 z^-1 + a2 z^-2) = X - a1 y[-1] - a2 (z^-1 y[-1] + y[-2])
    Y = sp.together((Xz - a1 * y1 - a2 * (y1 / z + y2)) / (1 + a1 / z + a2 / z ** 2))
    r = izt(Y)
    first = seq_check(Y, r)
    xin = f"{cf(K)}u[n]" if inp == 'step' else '0'
    st = (f"Solve $y[n] {'+' if a1 >= 0 else '-'} {tex(abs(a1))}y[n-1] {'+' if a2 >= 0 else '-'} {tex(abs(a2))}y[n-2] = {xin}$ for $n \\ge 0$ with $y[-1] = {y1}$, $y[-2] = {y2}$.")
    steps = [('Shift rules', '$y[n-1] \\to z^{-1}Y + y[-1]$ and $y[n-2] \\to z^{-2}Y + z^{-1}y[-1] + y[-2]$.'),
             ('Transform and collect', f"$Y(z)\\left(1 {'+' if a1 >= 0 else '-'} {tex(abs(a1))}z^{{-1}} {'+' if a2 >= 0 else '-'} {tex(abs(a2))}z^{{-2}}\\right) = X(z) - ({tex(a1)})({y1}) - ({tex(a2)})\\left(z^{{-1}}({y1}) + {y2}\\right)$."),
             ('Solve', f"$Y(z) = {zfrac(Y)}$; the characteristic roots are ${tex(p1)}$ and ${tex(p2)}$" + (' (repeated).' if kind == 'rep' else '.')),
             ('Partial fractions of $Y/z$', f"${r['pf']}$.")]
    steps += [(f'Term {i+1}', d) for i, d in enumerate(r['descs'])]
    steps.append(('Check by recursion', f"Direct iteration gives $y[0..3] = {', '.join(tex(v) for v in first)}$, as does the formula."))
    return Prob('C', st, steps, f"$y[n] = {combo(r['pairs'])}$ for $n \\ge 0$.", 'Second-order difference equations')


def zi_zs(rng):
    a = cyc(rng, 'zz', [H_, Q(1, 3), Q(3, 4), -H_])
    y0 = rng.choice([1, 2, 4])
    K = rng.choice([1, 2])
    Yzi = a * y0 / (1 - a / z)
    Yzs = (K * z / (z - 1)) / (1 - a / z)
    ri, rs = izt(Yzi), izt(Yzs)
    st = f"For $y[n] - {par(a)}y[n-1] = {cf(K)}u[n]$ with $y[-1] = {y0}$, find the zero-input and zero-state responses."
    steps = [('Split', f"$Y(z) = \\underbrace{{\\dfrac{{{tex(a*y0)}}}{{1 - {par(a)}z^{{-1}}}}}}_{{\\text{{zero-input}}}} + \\underbrace{{\\dfrac{{X(z)}}{{1 - {par(a)}z^{{-1}}}}}}_{{\\text{{zero-state}}}}$."),
             ('Zero-input', f"$y_{{zi}}[n] = {combo(ri['pairs'])}$: the stored initial condition decaying through the natural mode."),
             ('Zero-state', f"$\\dfrac{{Y_{{zs}}}}{{z}} = {rs['pf']}$, so $y_{{zs}}[n] = {combo(rs['pairs'])}$."),
             ('Steady state', f"As $n \\to \\infty$ only the step term survives: $y \\to {tex(sp.nsimplify(K/(1-a)))}$, the DC gain $1/(1 - {par(a)})$ times ${K}$.")]
    return Prob('C', st, steps, f"$y_{{zi}} = {combo(ri['pairs'])}$, $y_{{zs}} = {combo(rs['pairs'])}$ ($n \\ge 0$).", 'Zero-input and zero-state')


def step_resp(rng):
    a, b = rng.sample(POOL[:6], 2)
    c = rng.choice([1, 2])
    H = c * z ** 2 / ((z - a) * (z - b))
    Y = sp.together(H * z / (z - 1))
    r = izt(Y)
    first = seq_check(Y, r)
    st = f"A causal system has $H(z) = {zfrac(H)}$. Find its step response and its final value."
    steps = [('Output transform', f"$Y(z) = H(z)\\dfrac{{z}}{{z - 1}} = {zfrac(Y)}$."),
             ('Partial fractions of $Y/z$', f"${r['pf']}$.")]
    steps += [('Invert', ' '.join(r['descs']))]
    steps.append(('Final value', f"$H(1) = {tex(H.subs(z, 1))}$, the DC gain, which is the constant term above."))
    return Prob('C', st, steps, f"$s[n] = \\left({combo(r['pairs'])}\\right)u[n]$; final value ${tex(H.subs(z, 1))}$.", 'Step response')


TEMPLATES = [(by_inspection, 5), (distinct, 6),
             (roc_dependent, 5), (repeated, 5), (long_div, 4), (complex_z, 5), (first_order, 5),
             (second_order, 8), (zi_zs, 4), (step_resp, 3)]


def generate():
    return build_set(TEMPLATES, seed=1111)


if __name__ == '__main__':
    for i, p in enumerate(generate(), 1):
        print(f'--- 11.{i} [{p.level}] {p.topic}\n{p.statement}\n  ANS: {p.answer}')
