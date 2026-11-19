"""Inverse Z-transform helpers (partial fractions on X(z)/z)."""
import sympy as sp
from core import *


def izt(X, causal=True):
    """X rational in z. Returns dict: pf (X/z expansion), pairs [(coef, body)], descs, seq(nn) evaluator."""
    X = sp.together(sp.nsimplify(X))
    Y = sp.apart(sp.together(X / z), z)
    terms = list(sp.Add.make_args(Y))
    pairs, descs, funcs = [], [], []
    for T in terms:
        num, den = sp.fraction(sp.factor(T))
        P = sp.Poly(den, z)
        lc = P.LC()
        mon = sp.Poly(P.as_expr() / lc, z)
        rts = sp.roots(mon)
        numc = sp.Poly(num, z)
        if len(rts) == 1:
            p, kk = list(rts.items())[0]
            A = sp.nsimplify(numc.as_expr() / lc)
            if p == 0 and kk == 1:
                pairs.append((A, '\\delta[n]'))
                descs.append(f"$\\dfrac{{{tex(A)}}}{{z}}$ in $X(z)/z$ gives the constant ${tex(A)}$ in $X(z)$, i.e. ${tex(A)}\\delta[n]$.")
                funcs.append(lambda m, A=A: A if m == 0 else 0)
                continue
            if p == 0:
                d = kk - 1
                pairs.append((A, f'\\delta[n - {d}]'))
                descs.append(f"${tex(A)}z^{{-{d}}} \\leftrightarrow {tex(A)}\\delta[n - {d}]$.")
                funcs.append(lambda m, A=A, d=d: A if m == d else 0)
                continue
            if kk == 1:
                body = f"\\left({tex(p)}\\right)^n" if p != 1 else ''
                if causal:
                    pairs.append((A, body + ('u[n]' if False else '')))
                    descs.append(f"$\\dfrac{{{tex(A)}z}}{{z - {par(p)}}} \\leftrightarrow {tex(A)}\\left({tex(p)}\\right)^n u[n]$ (right-sided).")
                    funcs.append(lambda m, A=A, p=p: A * p ** m if m >= 0 else 0)
                else:
                    pairs.append((-A, body))
                    descs.append(f"$\\dfrac{{{tex(A)}z}}{{z - {par(p)}}} \\leftrightarrow -{par(A)}\\left({tex(p)}\\right)^n u[-n-1]$ (left-sided).")
                    funcs.append(lambda m, A=A, p=p: -A * p ** m if m < 0 else 0)
            elif kk == 2:
                # A z/(z-p)^2 <-> A n p^{n-1}
                coef = A / p
                pairs.append((coef, f"n\\left({tex(p)}\\right)^n"))
                descs.append(f"$\\dfrac{{{tex(A)}z}}{{(z - {par(p)})^2}} \\leftrightarrow {tex(A)}\\,n\\left({tex(p)}\\right)^{{n-1}}u[n] = {tex(coef)}\\,n\\left({tex(p)}\\right)^n u[n]$.")
                funcs.append(lambda m, A=A, p=p: A * m * p ** (m - 1) if m >= 0 else 0)
            else:
                raise ValueError('triple pole')
        else:
            _, a1, a0 = mon.all_coeffs()
            r = sp.sqrt(a0)
            c = sp.nsimplify(-a1 / (2 * r))
            th = sp.acos(c)
            sn = sp.sqrt(1 - c ** 2)
            nc = numc.all_coeffs()
            B, C = (0, nc[0] / lc) if len(nc) == 1 else (nc[0] / lc, nc[1] / lc)
            B, C = sp.nsimplify(B), sp.nsimplify(C)
            K = sp.nsimplify((C + B * r * c) / (r * sn))
            rb = '' if r == 1 else f"\\left({tex(r)}\\right)^n"
            if B != 0:
                pairs.append((B, f"{rb}\\cos\\left({tex(th)}n\\right)"))
            if K != 0:
                pairs.append((K, f"{rb}\\sin\\left({tex(th)}n\\right)"))
            descs.append(f"The quadratic $z^2 {'+' if a1 >= 0 else '-'} {tex(abs(a1))}z + {tex(a0)}$ has complex roots $r e^{{\\pm j\\theta}}$ with $r = {tex(r)}$ and $\\cos\\theta = {tex(c)}$, so $\\theta = {tex(th)}$. "
                         f"Write $z({tex(B)}z + {tex(C)})$ as ${tex(B)}\\,z(z - r\\cos\\theta) + {tex(K)}\\,z\\,r\\sin\\theta$ and use $\\dfrac{{z(z - r\\cos\\theta)}}{{z^2 - 2r\\cos\\theta\\,z + r^2}} \\leftrightarrow r^n\\cos\\theta n$, $\\dfrac{{z\\,r\\sin\\theta}}{{z^2 - 2r\\cos\\theta\\,z + r^2}} \\leftrightarrow r^n\\sin\\theta n$.")
            funcs.append(lambda m, B=B, K=K, r=r, th=th: (B * r ** m * sp.cos(th * m) + K * r ** m * sp.sin(th * m)) if m >= 0 else 0)
    pf = ' + '.join(tex(T) for T in terms).replace('+ -', '- ')
    seq = lambda m: sp.nsimplify(sp.simplify(sum(f(m) for f in funcs)))
    return dict(pf=pf, pairs=pairs, descs=descs, seq=seq, terms=terms)


def series(X, N=5):
    """First N samples of a causal sequence from X(z) by expansion in w = 1/z."""
    wv = sp.Symbol('w')
    ser = sp.series(sp.together(X).subs(z, 1 / wv), wv, 0, N).removeO()
    return [sp.nsimplify(ser.coeff(wv, m)) for m in range(N)]
