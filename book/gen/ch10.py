"""Chapter 10 - The Z-transform and its region of convergence."""
import numpy as np
import sympy as sp
from core import *
from zt import izt, series
import figstyle as fs
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

CH = 10
H_ = Q(1, 2)


def zden(p):
    return f"z - {par(p)}" if p >= 0 else f"z + {tex(-p)}"


def pz_plot(zeros, poles, name, rin=None, rout=None):
    fig, ax = plt.subplots(figsize=(2.8, 2.8))
    if rin is not None or rout is not None:
        R = 1.9
        ax.add_patch(Circle((0, 0), rout if rout else R, color=fs.TEAL, alpha=0.15, lw=0))
        if rin:
            ax.add_patch(Circle((0, 0), rin, color='white', lw=0))
    ax.add_patch(Circle((0, 0), 1, fill=False, ec=fs.GREY, ls='--', lw=0.9))
    for zz in zeros:
        ax.plot(float(sp.re(zz)), float(sp.im(zz)), 'o', mfc='white', mec=fs.NAVY, ms=8, mew=1.6)
    for pp in poles:
        ax.plot(float(sp.re(pp)), float(sp.im(pp)), 'x', color=fs.RUST, ms=9, mew=2)
    ax.axhline(0, color=fs.INK, lw=0.6); ax.axvline(0, color=fs.INK, lw=0.6)
    ax.set_xlim(-1.8, 1.8); ax.set_ylim(-1.8, 1.8); ax.set_aspect('equal')
    ax.set_xlabel('Re $z$', loc='right'); ax.set_title('Im $z$', loc='left', fontsize=8.5)
    return save_fig(fig, name)


def finite(rng):
    L = rng.choice([3, 4])
    st0 = rng.choice([0, 0, -1, 1])
    x = [rng.choice([-2, -1, 1, 2, 3]) for _ in range(L)]
    terms = combo([(v, '' if st0 + i == 0 else ('z' if st0 + i == -1 else f"z^{{{-(st0 + i)}}}")) for i, v in enumerate(x)])
    hasneg = st0 < 0
    haspos = st0 + L - 1 > 0
    roc = 'all $z$ except ' + (' and '.join((['$z = 0$'] if haspos else []) + (['$z = \\infty$'] if hasneg else [])) or 'none')
    if not haspos and not hasneg:
        roc = 'the entire $z$-plane'
    st = f"Find the Z-transform of $x[n] = {seq_tex(x, st0)}$ and its region of convergence."
    steps = [('Definition', '$X(z) = \\sum_n x[n]z^{-n}$: each sample contributes its value times $z^{-n}$.'),
             ('Write it out', f"$X(z) = {terms}$."),
             ('ROC', ('Positive powers of $z^{-1}$ blow up at $z = 0$. ' if haspos else '') + ('Positive powers of $z$ (from samples at negative $n$) blow up at $z = \\infty$. ' if hasneg else '') + f"So the ROC is {roc}.")]
    return Prob('A', st, steps, f"$X(z) = {terms}$; ROC: {roc}.", 'Finite sequences')


def basic(rng):
    a = cyc(rng, 'ba', [H_, Q(1, 3), Q(3, 4), -H_, Q(2, 3)])
    b = rng.choice([v for v in [Q(1, 4), 2, -Q(1, 3), Q(1, 5), 3] if v != a])
    A, B = rng.choice([1, 2, 3]), rng.choice([1, -1, 2])
    X = A * z / (z - a) + B * z / (z - b)
    roc = max(abs(a), abs(b))
    st = f"Find the Z-transform and ROC of $x[n] = {cf(A)}\\left({tex(a)}\\right)^n u[n] {'+' if B > 0 else '-'} {cf(abs(B))}\\left({tex(b)}\\right)^n u[n]$."
    steps = [('Standard pair', '$a^n u[n] \\leftrightarrow \\dfrac{1}{1 - az^{-1}} = \\dfrac{z}{z - a}$, ROC $|z| > |a|$.'),
             ('Each term', f"$\\dfrac{{{A}z}}{{{zden(a)}}}$ for $|z| > {tex(abs(a))}$ and $\\dfrac{{{B}z}}{{{zden(b)}}}$ for $|z| > {tex(abs(b))}$."),
             ('Combine', f"$X(z) = {tex(sp.factor(X))}$."),
             ('ROC', f"Intersection: $|z| > {tex(roc)}$, outside the outermost pole, as for every right-sided sequence." + (' It includes the unit circle, so the DTFT exists.' if roc < 1 else ' It excludes the unit circle, so the DTFT does not exist.'))]
    return Prob('A', st, steps, f"$X(z) = {tex(sp.factor(X))}$, ROC $|z| > {tex(roc)}$.", 'Right-sided sequences')


def left(rng):
    a = cyc(rng, 'la', [2, 3, H_, Q(3, 2)])
    A = rng.choice([1, 2])
    st = f"Find the Z-transform and ROC of $x[n] = -{cf(A)}\\left({tex(a)}\\right)^n u[-n-1]$."
    steps = [('Sum over negative $n$', f"$X(z) = -{A}\\sum_{{n=-\\infty}}^{{-1}}{tex(a)}^n z^{{-n}} = -{A}\\sum_{{m=1}}^{{\\infty}}\\left(\\dfrac{{z}}{{{tex(a)}}}\\right)^m$."),
             ('Geometric series', f"Converges for $|z| < {tex(a)}$ to $-{A}\\,\\dfrac{{z/{par(a)}}}{{1 - z/{par(a)}}} = \\dfrac{{{A}z}}{{z - {tex(a)}}}$."),
             ('Comment', 'Same formula as the right-sided sequence; only the ROC differs. A Z-transform without its ROC is incomplete.')]
    return Prob('A', st, steps, f"$X(z) = \\dfrac{{{A}z}}{{z - {tex(a)}}}$, ROC $|z| < {tex(a)}$.", 'Left-sided sequences')


def two_sided(rng):
    a = rng.choice([H_, Q(1, 3), Q(1, 4)])
    b = rng.choice([2, 3, Q(3, 2)])
    swap = cyc(rng, 'sw', [False, True, False, False, False])
    if swap:
        st = f"Find the Z-transform and ROC, if it exists, of $x[n] = \\left({tex(b)}\\right)^n u[n] - \\left({tex(a)}\\right)^n u[-n-1]$."
        steps = [('Right-sided part', f"$\\dfrac{{z}}{{z - {tex(b)}}}$, $|z| > {tex(b)}$."),
                 ('Left-sided part', f"$\\dfrac{{z}}{{z - {tex(a)}}}$, $|z| < {tex(a)}$."),
                 ('Intersect', f"We would need $|z| > {tex(b)}$ and $|z| < {tex(a)}$ at once; since ${tex(a)} < {tex(b)}$ this is impossible.")]
        return Prob('B', st, steps, 'No Z-transform: the ROCs do not overlap.', 'Two-sided sequences')
    X = z / (z - a) + z / (z - b)
    st = f"Find the Z-transform and ROC of $x[n] = \\left({tex(a)}\\right)^n u[n] - \\left({tex(b)}\\right)^n u[-n-1]$, and say whether its DTFT exists."
    steps = [('Right-sided part', f"$\\dfrac{{z}}{{z - {tex(a)}}}$, $|z| > {tex(a)}$."),
             ('Left-sided part', f"$-({tex(b)})^n u[-n-1] \\leftrightarrow \\dfrac{{z}}{{z - {tex(b)}}}$, $|z| < {tex(b)}$."),
             ('Combine', f"$X(z) = {tex(sp.factor(X))}$ on the ring ${tex(a)} < |z| < {tex(b)}$."),
             ('DTFT', 'The ring contains the unit circle, so the DTFT exists; the sequence decays in both directions.')]
    return Prob('B', st, steps, f"$X(z) = {tex(sp.factor(X))}$, ROC ${tex(a)} < |z| < {tex(b)}$; DTFT exists.", 'Two-sided sequences')


def standard(rng):
    case = cyc(rng, 'st', ['nan', 'cos', 'rsin', 'nan', 'rcos', 'step'])
    a = rng.choice([H_, Q(1, 3), Q(2, 3)])
    th = rng.choice([pi / 2, pi / 3, pi / 4])
    if case == 'nan':
        X = a * z / (z - a) ** 2
        st = f"Find the Z-transform of $x[n] = n\\left({tex(a)}\\right)^n u[n]$."
        steps = [('Differentiation property', '$n\\,x[n] \\leftrightarrow -z\\dfrac{dX}{dz}$.'), ('Apply', f"$-z\\dfrac{{d}}{{dz}}\\dfrac{{z}}{{z - {tex(a)}}} = -z\\cdot\\dfrac{{-{tex(a)}}}{{(z - {tex(a)})^2}}$."), ('Result', f"$X(z) = {tex(X)}$, ROC $|z| > {tex(a)}$, with a double pole at $z = {tex(a)}$.")]
        roc = tex(a)
    elif case == 'cos':
        X = z * (z - sp.cos(th)) / (z ** 2 - 2 * sp.cos(th) * z + 1)
        st = f"Find the Z-transform of $x[n] = \\cos\\left({tex(th)}n\\right)u[n]$."
        steps = [('Euler', f"$\\cos\\theta n = \\tfrac12(e^{{j\\theta n}} + e^{{-j\\theta n}})$, each a geometric sequence with ratio on the unit circle."),
                 ('Add', f"$\\tfrac12\\left[\\dfrac{{z}}{{z - e^{{j\\theta}}}} + \\dfrac{{z}}{{z - e^{{-j\\theta}}}}\\right] = \\dfrac{{z(z - \\cos\\theta)}}{{z^2 - 2z\\cos\\theta + 1}}$."),
                 ('Substitute', f"With $\\theta = {tex(th)}$: $X(z) = {tex(sp.simplify(X))}$, ROC $|z| > 1$. The poles sit on the unit circle at $e^{{\\pm j{tex(th)}}}$.")]
        roc = '1'
    elif case in ('rsin', 'rcos'):
        fn = 'sin' if case == 'rsin' else 'cos'
        X = (a * sp.sin(th) * z if fn == 'sin' else z * (z - a * sp.cos(th))) / (z ** 2 - 2 * a * sp.cos(th) * z + a ** 2)
        st = f"Find the Z-transform of $x[n] = \\left({tex(a)}\\right)^n\\{fn}\\left({tex(th)}n\\right)u[n]$."
        steps = [('Start from the undamped pair', f"$\\{fn}(\\theta n)u[n]$ has a standard transform with denominator $z^2 - 2z\\cos\\theta + 1$."),
                 ('Scaling in $z$', f"Multiplying by $a^n$ replaces $z$ by $z/a$, which moves the poles to radius $a = {tex(a)}$."),
                 ('Result', f"$X(z) = {tex(sp.simplify(X))}$, ROC $|z| > {tex(a)}$.")]
        roc = tex(a)
    else:
        X = z / (z - 1)
        st = "Find the Z-transform of the unit step and explain why its DTFT does not exist in the ordinary sense."
        steps = [('Sum', '$\\sum_{n\\ge0}z^{-n} = \\dfrac{1}{1 - z^{-1}} = \\dfrac{z}{z - 1}$ for $|z| > 1$.'), ('DTFT', 'The ROC $|z| > 1$ excludes the unit circle, where the pole sits; the DTFT exists only with impulses added.')]
        roc = '1'
    return Prob('B', st, steps, f"$X(z) = {tex(sp.simplify(X))}$, ROC $|z| > {roc}$.", 'Standard transforms')


def props(rng):
    a = cyc(rng, 'pa', [H_, Q(1, 3), Q(1, 4)])
    case = cyc(rng, 'pc', ['delay', 'adv', 'scale', 'rev', 'conv', 'acc'])
    base = f"x[n] = \\left({tex(a)}\\right)^n u[n] \\leftrightarrow X(z) = \\dfrac{{z}}{{z - {tex(a)}}}"
    if case == 'delay':
        k_ = rng.choice([2, 3])
        st = f"Given ${base}$, find the transform of $x[n - {k_}]$."
        ans = f"z^{{-{k_}}}\\cdot\\dfrac{{z}}{{z - {tex(a)}}} = \\dfrac{{1}}{{{'z' if k_ == 2 else f'z^{{{k_-1}}}'}(z - {tex(a)})}}"
        steps = [('Delay property', '$x[n - k] \\leftrightarrow z^{-k}X(z)$ for a sequence that starts at $n = 0$.'), ('Apply', f"${ans}$.")]
    elif case == 'adv':
        st = f"Given ${base}$, find the unilateral transform of $x[n + 1]$."
        ans = f"zX(z) - zx[0] = \\dfrac{{z^2}}{{z - {tex(a)}}} - z = \\dfrac{{{tex(a)}z}}{{z - {tex(a)}}}"
        steps = [('Advance property (unilateral)', '$x[n + 1] \\leftrightarrow zX(z) - zx[0]$: the sample that moves to negative time must be removed.'), ('Apply', f"$x[0] = 1$, so ${ans}$."),
                 ('Check', f"$x[n + 1] = {tex(a)}\\cdot({tex(a)})^n u[n]$ for $n \\ge 0$, whose transform is indeed ${tex(a)}z/(z - {tex(a)})$.")]
    elif case == 'scale':
        c = rng.choice([2, 3])
        st = f"Given ${base}$, find the transform of ${c}^n x[n]$."
        ans = f"\\dfrac{{z/{c}}}{{z/{c} - {tex(a)}}} = \\dfrac{{z}}{{z - {tex(c*a)}}}"
        steps = [('Scaling in $z$', '$c^n x[n] \\leftrightarrow X(z/c)$, with the ROC scaled by $|c|$.'), ('Apply', f"${ans}$, ROC $|z| > {tex(c*a)}$.")]
    elif case == 'rev':
        st = f"Given ${base}$, find the transform of $x[-n]$ and its ROC."
        ans = f"\\dfrac{{z^{{-1}}}}{{z^{{-1}} - {tex(a)}}} = \\dfrac{{1}}{{1 - {tex(a)}z}},\\ |z| < {tex(1/a)}"
        steps = [('Reversal', '$x[-n] \\leftrightarrow X(1/z)$, and the ROC is inverted.'), ('Apply', f"${ans}$.")]
    elif case == 'conv':
        st = f"Given ${base}$, find the transform of $x[n] * u[n]$ and hence the sequence."
        ans = f"\\dfrac{{z^2}}{{(z - {tex(a)})(z - 1)}}"
        r = izt(z ** 2 / ((z - a) * (z - 1)))
        steps = [('Convolution becomes multiplication', f"$X(z)\\cdot\\dfrac{{z}}{{z - 1}} = {ans}$."), ('Partial fractions on $Y/z$', f"${r['pf']}$."), ('Sequence', f"$y[n] = \\left({combo(r['pairs'])}\\right)u[n]$, the running sum of $x$.")]
    else:
        st = f"Given ${base}$, find the transform of the accumulated sequence $y[n] = \\sum_{{k=0}}^{{n}} x[k]$ and its final value."
        ans = f"\\dfrac{{z^2}}{{(z - 1)(z - {tex(a)})}}"
        steps = [('Accumulation', 'Summing up to $n$ is convolution with $u[n]$, i.e. multiplication by $z/(z - 1)$.'), ('Apply', f"$Y(z) = {ans}$."),
                 ('Final value', f"$\\lim_{{z\\to1}}(z - 1)Y(z) = \\dfrac{{1}}{{1 - {tex(a)}}} = {tex(1/(1-a))}$, the sum of the geometric series.")]
    return Prob('B', st, steps, f"${ans}$.", 'Z-transform properties')


def polezero(rng):
    p1 = rng.choice([H_, -H_, Q(3, 4), Q(1, 3)])
    p2 = rng.choice([v for v in [-Q(1, 4), Q(2, 3), -Q(3, 4), Q(1, 5)] if v != p1])
    z1 = rng.choice([0, -1, 1, 2])
    X = (z - z1) * z / ((z - p1) * (z - p2))
    Xinv = sp.simplify(X)
    num_tex = tex(sp.expand((1 - z1 / z)))
    st = f"Find the poles and zeros of $X(z) = \\dfrac{{1 {'-' if z1 > 0 else '+'} {cf(abs(z1)) if z1 else ''}{'z^{-1}' if z1 else ''}}}{{{zpoly_tex([1, -(p1 + p2), p1 * p2])}}}$ and sketch the pole–zero plot. What ROC makes the sequence causal, and is it then stable?".replace('1 + z^{-1}', '1 + z^{-1}').replace('{1 + }', '{1}')
    if z1 == 0:
        st = f"Find the poles and zeros of $X(z) = \\dfrac{{1}}{{{zpoly_tex([1, -(p1 + p2), p1 * p2])}}}$ and sketch the pole–zero plot. What ROC makes the sequence causal, and is it then stable?"
    zeros = [0] + ([z1] if z1 != 0 else [0])
    poles = [p1, p2]
    path = pz_plot(zeros, poles, new_fig_name('ch10_pz'), rin=float(max(abs(p1), abs(p2))))
    steps = [('Multiply through by $z^2$', f"$X(z) = {tex(sp.factor(X))}$."),
             ('Zeros', f"Numerator roots: $z = 0$ and $z = {z1}$." if z1 != 0 else 'A double zero at $z = 0$.'),
             ('Poles', f"$z = {tex(p1)}$ and $z = {tex(p2)}$."),
             ('Causal ROC', f"Outside the outermost pole: $|z| > {tex(max(abs(p1), abs(p2)))}$. It contains the unit circle, so the causal sequence is also stable.")]
    return Prob('B', st, steps, f"Zeros: $0$, ${z1}$; poles: ${tex(p1)}$, ${tex(p2)}$; causal ROC $|z| > {tex(max(abs(p1), abs(p2)))}$, stable.", 'Poles and zeros', sol_fig=(path, 'Pole–zero plot; the shaded region is the causal ROC and the dashed circle is $|z| = 1$.'))


def truncated(rng):
    a = cyc(rng, 'tr', [H_, 2, Q(1, 3), 3])
    N = rng.choice([3, 4, 5, 8])
    st = f"Find the Z-transform of the truncated sequence $x[n] = \\left({tex(a)}\\right)^n$ for $0 \\le n \\le {N-1}$, zero otherwise. Where is its ROC, and what has happened to the apparent pole?"
    steps = [('Finite geometric sum', f"$X(z) = \\sum_{{n=0}}^{{{N-1}}}({tex(a)}z^{{-1}})^n = \\dfrac{{1 - {par(a)}^{{{N}}}z^{{-{N}}}}}{{1 - {tex(a)}z^{{-1}}}}$."),
             ('ROC', 'The sequence is finite and causal, so the ROC is all $z$ except $z = 0$.'),
             ('The pole cancels', f"The numerator vanishes at the ${N}$ points $z = {tex(a)}e^{{j2\\pi k/{N}}}$; the one with $k = 0$ cancels the apparent pole at $z = {tex(a)}$. The function is really a polynomial in $z^{{-1}}$.")]
    return Prob('B', st, steps, f"$X(z) = \\dfrac{{1 - {par(a)}^{{{N}}}z^{{-{N}}}}}{{1 - {tex(a)}z^{{-1}}}}$, ROC $z \\ne 0$; the pole at ${tex(a)}$ is cancelled.", 'Truncated sequences')


def ivt_fvt(rng):
    a, b = rng.sample([H_, Q(1, 3), Q(1, 4), -H_], 2)
    c = rng.choice([1, 2, 3])
    X = c * z ** 2 / ((z - 1) * (z - a))
    if rng.random() < 0.5:
        X = c * z / ((z - 1) * (z - a))
    x0 = sp.limit(X, z, sp.oo)
    xf = sp.limit((z - 1) * X, z, 1)
    st = f"For the causal sequence with $X(z) = {tex(X)}$, find $x[0]$ and $\\lim_{{n\\to\\infty}}x[n]$ without inverting."
    vals = series(X, 4)
    steps = [('Initial value', f"$x[0] = \\lim_{{z\\to\\infty}}X(z) = {tex(x0)}$."),
             ('Final value conditions', f"$(z - 1)X(z)$ has its only pole at $z = {tex(a)}$, inside the unit circle, so the theorem applies."),
             ('Final value', f"$\\lim_{{z\\to1}}(z - 1)X(z) = \\dfrac{{{c}}}{{1 - {par(a)}}} = {tex(xf)}$."),
             ('Check by long division', f"The first samples are ${', '.join(tex(v) for v in vals)}, \\dots$, consistent with both results.")]
    return Prob('C', st, steps, f"$x[0] = {tex(x0)}$, $x[\\infty] = {tex(xf)}$.", 'Initial and final values')


def roc_choice(rng):
    p1, p2 = rng.choice([(H_, 2), (Q(1, 3), 3), (Q(3, 4), Q(3, 2)), (H_, 3)])
    X = z / ((z - p1) * (z - p2))
    st = f"$X(z) = {tex(X)}$. List the possible ROCs. For each, say whether $x[n]$ is right-sided, left-sided or two-sided, and whether it is stable (absolutely summable)."
    steps = [('Poles', f"$z = {tex(p1)}$ and $z = {tex(p2)}$; ROCs are rings bounded by poles."),
             ('$|z| > ' + tex(p2) + '$', 'Right-sided (causal). Excludes the unit circle: not stable.'),
             (f'${tex(p1)} < |z| < {tex(p2)}$', 'Two-sided. Contains the unit circle: stable, though not causal.'),
             ('$|z| < ' + tex(p1) + '$', 'Left-sided (anti-causal). Excludes the unit circle: not stable.'),
             ('Moral', 'A system with a pole outside the unit circle can be causal or stable, but not both.')]
    return Prob('C', st, steps, f"$|z| > {tex(p2)}$: causal, unstable; ${tex(p1)} < |z| < {tex(p2)}$: two-sided, stable; $|z| < {tex(p1)}$: anti-causal, unstable.", 'ROC, causality and stability')


def conv_z(rng):
    a, b = rng.sample([H_, Q(1, 3), Q(1, 4), -H_, Q(3, 4)], 2)
    X = z ** 2 / ((z - a) * (z - b))
    r = izt(X)
    st = f"Use the Z-transform to compute $\\left({tex(a)}\\right)^n u[n] * \\left({tex(b)}\\right)^n u[n]$."
    steps = [('Multiply transforms', f"$Y(z) = \\dfrac{{z}}{{{zden(a)}}}\\cdot\\dfrac{{z}}{{{zden(b)}}} = {tex(X)}$."),
             ('Expand $Y(z)/z$', f"$\\dfrac{{Y(z)}}{{z}} = {r['pf']}$.")]
    steps += [('Invert', ' '.join(r['descs']))]
    steps.append(('Compare', 'This agrees with the closed form $\\dfrac{a^{n+1} - b^{n+1}}{a - b}$ found by direct summation in Chapter 3.'))
    return Prob('C', st, steps, f"$y[n] = \\left({combo(r['pairs'])}\\right)u[n]$.", 'Convolution by Z-transform')


TEMPLATES = [(finite, 6), (basic, 5), (left, 3),
             (two_sided, 5), (standard, 6), (props, 6), (polezero, 4), (truncated, 3),
             (ivt_fvt, 5), (roc_choice, 4), (conv_z, 3)]


def generate():
    return build_set(TEMPLATES, seed=1010)


if __name__ == '__main__':
    for i, p in enumerate(generate(), 1):
        print(f'--- 10.{i} [{p.level}] {p.topic}\n{p.statement}\n  ANS: {p.answer}')
