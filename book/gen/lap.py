"""Partial fractions and inverse Laplace transforms with readable working."""
import math
import sympy as sp
from core import *

tp = sp.Symbol('t', positive=True)


def roots_of(den):
    return sp.roots(sp.Poly(den, s))


def inv_term(T):
    """Invert one partial-fraction term. Returns (pairs for combo, sympy f, description)."""
    num, den = sp.fraction(sp.factor(T))
    if not den.has(s):
        c = sp.nsimplify(T)
        return [(c, '\\delta(t)')], c * sp.DiracDelta(tp), f"${tex(c)}$ is the transform of ${tex(c)}\\delta(t)$."
    P = sp.Poly(den, s)
    lc = P.LC()
    mon = sp.Poly(P.as_expr() / lc, s)
    rts = sp.roots(mon)
    numc = sp.Poly(num, s)
    if len(rts) == 1:
        r, kk = list(rts.items())[0]
        a = -r
        A = sp.nsimplify(numc.as_expr() / lc)
        body = expo(a) if a != 0 else ''
        if kk == 1:
            f = A * sp.exp(-a * tp)
            desc = f"$\\dfrac{{{tex(A)}}}{{{tex(s + a)}}} \\leftrightarrow {tex(A)}" + (f"{expo(a)}$" if a != 0 else '$ (a step).')
            return [(A, body)], f, desc
        coef = A / math.factorial(kk - 1)
        tpow = 't' if kk == 2 else f't^{{{kk-1}}}'
        f = coef * tp ** (kk - 1) * sp.exp(-a * tp)
        desc = (f"$\\dfrac{{{tex(A)}}}{{{tex((s + a))}^{{{kk}}}}} \\leftrightarrow {tex(A)}\\,\\dfrac{{t^{{{kk-1}}}}}{{{kk-1}!}}{expo(a) if a != 0 else ''}$, using $\\dfrac{{1}}{{(s+a)^n}} \\leftrightarrow \\dfrac{{t^{{n-1}}}}{{(n-1)!}}e^{{-at}}$.")
        return [(coef, tpow + body)], f, desc
    # irreducible quadratic
    p = mon.all_coeffs()
    _, p1, p0 = p
    al = sp.nsimplify(p1 / 2)
    be = sp.sqrt(sp.nsimplify(p0 - al ** 2))
    nc = numc.all_coeffs()
    if len(nc) == 1:
        B, C = 0, nc[0] / lc
    else:
        B, C = nc[0] / lc, nc[1] / lc
    B, C = sp.nsimplify(B), sp.nsimplify(C)
    K2 = sp.nsimplify((C - B * al) / be)
    ex = expo(al) if al != 0 else ''
    pairs = []
    if B != 0:
        pairs.append((B, f"{ex}\\cos({cf(be)}t)"))
    if K2 != 0:
        pairs.append((K2, f"{ex}\\sin({cf(be)}t)"))
    f = B * sp.exp(-al * tp) * sp.cos(be * tp) + K2 * sp.exp(-al * tp) * sp.sin(be * tp)
    sq = f"(s {'+' if al > 0 else '-'} {tex(abs(al))})^2 + {tex(be**2)}" if al != 0 else f"s^2 + {tex(be**2)}"
    shifted = (f"{tex(B)}(s {'+' if al > 0 else '-'} {tex(abs(al))}) {'+' if K2*be >= 0 else '-'} {tex(abs(K2*be))}" if al != 0 else f"{tex(B)}s + {tex(K2*be)}")
    desc = (f"Complete the square: ${tex(den / lc)} = {sq}$, and write the numerator as ${shifted}$. "
            f"Then use $\\dfrac{{s+\\alpha}}{{(s+\\alpha)^2+\\beta^2}} \\leftrightarrow e^{{-\\alpha t}}\\cos\\beta t$ and "
            f"$\\dfrac{{\\beta}}{{(s+\\alpha)^2+\\beta^2}} \\leftrightarrow e^{{-\\alpha t}}\\sin\\beta t$ with $\\alpha = {tex(al)}$, $\\beta = {tex(be)}$.")
    return pairs, f, desc


def ilt(F, delay=0):
    """Return dict with pf (latex), pairs, f (sympy), descs."""
    F = sp.together(sp.nsimplify(F))
    num, den = sp.fraction(F)
    q, r = sp.div(sp.Poly(num, s), sp.Poly(den, s))
    terms = []
    if not q.is_zero:
        terms += list(sp.Add.make_args(q.as_expr()))
    rem = sp.apart(r.as_expr() / den, s) if not r.is_zero else 0
    terms += list(sp.Add.make_args(rem)) if rem != 0 else []
    pairs, f, descs = [], 0, []
    for T in terms:
        p, ff, d = inv_term(T)
        pairs += p
        f += ff
        descs.append(d)
    pf = ' + '.join(tex(T) for T in terms).replace('+ -', '- ')
    return dict(pf=pf, pairs=pairs, f=sp.simplify(f), descs=descs, improper=not q.is_zero, terms=terms)


def time_tex(pairs, delay=0):
    """f(t) for t >= 0 as LaTeX, with u(t) or delayed form."""
    body = combo(pairs)
    if delay:
        body = body.replace('t)', f'(t - {delay}))').replace('t}', f'(t - {delay})}}')
    return body


def verify(F, f):
    """Check that L{f} == F (debug helper)."""
    G = sp.laplace_transform(f, tp, s, noconds=True)
    return sp.simplify(G - F) == 0
