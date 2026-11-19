"""Chapter 8 - Inverse Laplace transform and differential equations."""
import sympy as sp
from core import *
from lap import tp, ilt, combo as _c

CH = 8


def poly_s(expr):
    return tex(sp.expand(expr))


def inv_steps(F, intro=None):
    r = ilt(F)
    steps = []
    if intro:
        steps.append(intro)
    if r['improper']:
        steps.append(('Divide first', 'The numerator has the same degree as the denominator, so long division leaves a constant, which inverts to an impulse.'))
    steps.append(('Partial fractions', f"$F(s) = {r['pf']}$."))
    for i, d in enumerate(r['descs']):
        steps.append((f'Invert term {i+1}' if len(r['descs']) > 1 else 'Invert', d))
    ft = combo(r['pairs'])
    return r, steps, ft


def distinct(rng):
    k3 = rng.random() < 0.35
    ps = rng.sample([0, 1, 2, 3, 4, 5], 3 if k3 else 2)
    den = sp.prod([s + p for p in ps])
    deg = len(ps) - 1
    num = sp.Integer(rng.choice([1, 2, 3, 4, 6, 10])) if rng.random() < 0.5 else rng.choice([1, 2]) * s + rng.choice([1, 3, 5, 6])
    F = num / den
    if sp.simplify(sp.cancel(F) - F) != 0 or sp.degree(sp.cancel(F).as_numer_denom()[1], s) < len(ps):
        num = sp.Integer(rng.choice([2, 6]))
        F = num / den
    st = f"Find the inverse Laplace transform of $F(s) = \\dfrac{{{poly_s(num)}}}{{{tex(den)}}}$ (a causal signal)."
    r, steps, ft = inv_steps(F, ('Method', 'The poles are real and distinct, so each coefficient follows from the cover-up rule: cover the factor $(s + p)$ and evaluate the rest at $s = -p$.'))
    steps.append(('Check', f"$f(0^+) = {tex(sp.limit(s*F, s, sp.oo))}$ from the initial value theorem; the formula gives ${tex(sp.nsimplify(r['f'].subs(tp, 0)))}$."))
    return Prob('A', st, steps, f"$f(t) = \\left({ft}\\right)u(t)$.", 'Distinct real poles')


def delayed(rng):
    a, b = rng.sample([1, 2, 3, 4], 2)
    T = rng.choice([1, 2, 3])
    c = rng.choice([1, 2, 3, 6])
    F0 = c / ((s + a) * (s + b)) if rng.random() < 0.6 else sp.Integer(c) / (s * (s + a))
    r = ilt(F0)
    ft = combo(r['pairs'])
    shifted = combo([(cc, b_.replace('t}', f'(t - {T})}}').replace('(t)', f'(t - {T})').replace('cos(t', 'cos(t')) for cc, b_ in r['pairs']])
    shifted = shifted.replace('\\cos(', '\\cos(').replace('t)', f'(t - {T}))') if '\\cos' in shifted or '\\sin' in shifted else shifted
    st = f"Find the inverse Laplace transform of $F(s) = \\dfrac{{{c}e^{{-{cf(T)}s}}}}{{{tex(sp.factor(F0*1/c).as_numer_denom()[1])}}}$."
    steps = [('Separate the exponential', f"$F(s) = e^{{-{cf(T)}s}}G(s)$ with $G(s) = {tex(F0)}$. The exponential means 'delay by {T}'; deal with it last."),
             ('Invert $G$', f"$G(s) = {r['pf']}$, so $g(t) = \\left({ft}\\right)u(t)$."),
             ('Apply the delay', f"$f(t) = g(t - {T})$: replace every $t$ by $t - {T}$, including inside the step.")]
    return Prob('A', st, steps, f"$f(t) = \\left({shifted}\\right)u(t - {T})$.", 'Time delay')


def repeated(rng):
    a = rng.choice([1, 2, 3])
    b = rng.choice([v for v in [0, 1, 2, 4, 5] if v != a])
    c = rng.choice([1, 2, 4, 6])
    form = cyc(rng, 'rp', ['ab', 's', 'num'])
    if form == 'ab':
        F = sp.Integer(c) / ((s + a) ** 2 * (s + b))
    elif form == 's':
        F = sp.Integer(c) / (s * (s + a) ** 2)
    else:
        F = (s + rng.choice([v for v in [1, 3, 5, 6] if v not in (a, b)])) / (s + a) ** 2 / (s + b)
    st = f"Find the inverse Laplace transform of $F(s) = {tex(F)}$."
    r, steps, ft = inv_steps(F, ('Method', f"The factor $(s + {a})^2$ is a repeated pole, so the expansion needs both $\\dfrac{{A_1}}{{s + {a}}}$ and $\\dfrac{{A_2}}{{(s + {a})^2}}$. Find $A_2$ by cover-up, then $A_1$ by differentiating what remains (or by comparing coefficients)."))
    return Prob('B', st, steps, f"$f(t) = \\left({ft}\\right)u(t)$.", 'Repeated poles')


def complex_poles(rng):
    al = rng.choice([0, 1, 2, 3])
    be = rng.choice([1, 2, 3, 4])
    quad = (s + al) ** 2 + be ** 2
    form = cyc(rng, 'cp', ['plain', 'plain', 'withreal', 'withs'])
    if form == 'plain':
        B, C = rng.choice([0, 1, 2]), rng.choice([1, 3, 5, 8])
        F = (B * s + C) / sp.expand(quad)
    elif form == 'withs':
        F = sp.Integer(rng.choice([5, 10, 13, 20])) / (s * sp.expand(quad))
    else:
        p = rng.choice([v for v in [1, 2, 4, 5] if v != al])
        F = (s + rng.choice([1, 2, 3])) / ((s + p) * sp.expand(quad))
    st = f"Find the inverse Laplace transform of $F(s) = {tex(F)}$."
    r, steps, ft = inv_steps(F, ('Method', 'Complex poles come in conjugate pairs. Keep the quadratic intact, complete the square, and match to the damped cosine and sine pairs; there is no need for complex arithmetic.'))
    return Prob('B', st, steps, f"$f(t) = \\left({ft}\\right)u(t)$.", 'Complex poles')


def improper(rng):
    a, b = rng.sample([1, 2, 3, 4], 2)
    n1, n0 = rng.choice([1, 3, 5, 6]), rng.choice([1, 2, 4, 7])
    F = (s ** 2 + n1 * s + n0) / ((s + a) * (s + b))
    if sp.cancel(F) != F:
        n0 += 1
        F = (s ** 2 + n1 * s + n0) / ((s + a) * (s + b))
    st = f"Find the inverse Laplace transform of $F(s) = \\dfrac{{{poly_s(s**2 + n1*s + n0)}}}{{{tex((s+a)*(s+b))}}}$."
    r, steps, ft = inv_steps(F)
    rest = combo([p for p in r['pairs'] if p[1] != '\\delta(t)'])
    imp = [p for p in r['pairs'] if p[1] == '\\delta(t)'][0][0]
    return Prob('B', st, steps, f"$f(t) = {cf(imp)}\\delta(t) + \\left({rest}\\right)u(t)$.", 'Improper functions')


def first_order(rng):
    a = cyc(rng, 'fa', [1, 2, 3, 4, 5])
    y0 = rng.choice([-1, 1, 2, 3, 0])
    case = rng.choice(['step', 'exp'])
    K = rng.choice([1, 2, 4, 6])
    if case == 'step':
        X = sp.Integer(K) / s
        xin = f"{cf(K)}u(t)"
    else:
        c = rng.choice([v for v in [1, 2, 3, 6] if v != a])
        X = sp.Integer(K) / (s + c)
        xin = f"{cf(K)}{expo(c)}u(t)"
    Y = sp.together((X + y0) / (s + a))
    st = f"Solve $\\dfrac{{dy}}{{dt}} + {cf(a)}y = {xin}$ with $y(0^-) = {y0}$ using the Laplace transform."
    r = ilt(Y)
    ft = combo(r['pairs'])
    steps = [('Transform', f"$sY - y(0^-) + {a}Y = X(s)$, with $X(s) = {tex(X)}$."),
             ('Solve for $Y$', f"$Y(s) = \\dfrac{{X(s) + {y0}}}{{s + {a}}} = {tex(sp.factor(Y))}$."),
             ('Partial fractions', f"$Y(s) = {r['pf']}$.")]
    steps += [('Invert', ' '.join(r['descs']))]
    steps.append(('Check', f"At $t = 0$: $y = {tex(sp.nsimplify(r['f'].subs(tp, 0)))}$, matching the initial condition. As $t \\to \\infty$: $y \\to {tex(sp.limit(r['f'], tp, sp.oo))}$."))
    return Prob('B', st, steps, f"$y(t) = {ft}$ for $t \\ge 0$.", 'First-order equations')


def rc_circuit(rng):
    R = rng.choice([1, 2, 5, 10])
    C = rng.choice([100, 200, 500, 1000])
    V = rng.choice([5, 10, 12])
    v0 = rng.choice([0, 2, 3])
    tau = sp.Rational(R * 1000 * C, 10 ** 6)
    st = f"A series RC circuit with $R = {R}$ k$\\Omega$ and $C = {C}\\ \\mu$F has $v_C(0^-) = {v0}$ V. At $t = 0$ a ${V}$ V source is switched in. Find $v_C(t)$."
    a = 1 / tau
    Y = sp.together((V * a / s + v0) / (s + a))
    r = ilt(Y)
    steps = [('Circuit equation', f"$RC\\,\\dfrac{{dv_C}}{{dt}} + v_C = {V}u(t)$, with $RC = {tex(tau)}$ s."),
             ('Transform', f"$RC(sV_C - {v0}) + V_C = {V}/s$, so $V_C(s) = \\dfrac{{{V}/(RC\\,s) + {v0}}}{{s + 1/RC}} = {tex(sp.factor(Y))}$."),
             ('Partial fractions', f"$V_C = {r['pf']}$."),
             ('Invert', f"$v_C(t) = {V} - {V - v0}{expo(1/tau)}$ V for $t \\ge 0$."),
             ('Interpret', f"The capacitor moves from ${v0}$ V to ${V}$ V with time constant ${tex(tau)}$ s; it is within 1% of the final value after about $5RC = {tex(5*tau)}$ s.")]
    return Prob('B', st, steps, f"$v_C(t) = {V} - {V - v0}{expo(1/tau)}$ V, $t \\ge 0$.", 'RC circuits')


def second_order(rng):
    kind = cyc(rng, 'so', ['real', 'rep', 'cplx', 'real', 'cplx', 'rep', 'real', 'cplx'])
    if kind == 'real':
        p1, p2 = rng.sample([1, 2, 3, 4], 2)
        a1, a0 = p1 + p2, p1 * p2
    elif kind == 'rep':
        p = rng.choice([1, 2, 3])
        a1, a0 = 2 * p, p * p
    else:
        al, be = rng.choice([1, 2]), rng.choice([1, 2, 3])
        a1, a0 = 2 * al, al * al + be * be
    y0, yd0 = rng.choice([0, 1, 2]), rng.choice([0, 1, -1, 2])
    inp = rng.choice(['step', 'zero', 'step', 'exp'])
    K = rng.choice([1, 2, 4, 5, 10])
    if inp == 'step':
        X, xin = sp.Integer(K) / s, f"{cf(K)}u(t)"
    elif inp == 'zero':
        X, xin = 0, '0'
        if y0 == 0 and yd0 == 0:
            y0 = 1
    else:
        c = rng.choice([v for v in [1, 2, 3, 5] if v not in (a1, a0)])
        X, xin = sp.Integer(K) / (s + c), f"{cf(K)}{expo(c)}u(t)"
    Y = sp.together((X + (s + a1) * y0 + yd0) / (s ** 2 + a1 * s + a0))
    try:
        r = ilt(Y)
    except Exception:
        return second_order(rng)
    st = f"Solve $y'' + {cf(a1)}y' + {cf(a0)}y = {xin}$ with $y(0^-) = {y0}$, $y'(0^-) = {yd0}$."
    char = sp.factor(s ** 2 + a1 * s + a0)
    rts = sp.roots(s ** 2 + a1 * s + a0)
    steps = [('Transform with initial conditions', f"$[s^2Y - {y0}s - ({yd0})] + {a1}[sY - {y0}] + {a0}Y = X(s)$" + (f", with $X(s) = {tex(X)}$." if X != 0 else ' with no input.')),
             ('Solve for $Y$', f"$Y(s) = {tex(sp.factor(Y))}$."),
             ('Nature of the poles', f"$s^2 + {a1}s + {a0} = {tex(char)}$, with roots " + ', '.join(f"${tex(rr)}$" for rr in rts) + ' — ' +
              {'real': 'real and distinct (overdamped).', 'rep': 'repeated (critically damped).', 'cplx': 'complex (underdamped), so expect a decaying oscillation.'}[kind]),
             ('Partial fractions', f"$Y(s) = {r['pf']}$.")]
    steps += [(f'Invert term {i+1}', d) for i, d in enumerate(r['descs'])]
    f0 = sp.nsimplify(r['f'].subs(tp, 0))
    fd0 = sp.nsimplify(sp.diff(r['f'], tp).subs(tp, 0))
    assert f0 == y0, (f0, y0)
    if not (inp == 'zero' and False):
        pass
    steps.append(('Check the initial conditions', f"$y(0) = {tex(f0)}$ and $y'(0) = {tex(fd0)}$, as required."))
    return Prob('C', st, steps, f"$y(t) = {combo(r['pairs'])}$ for $t \\ge 0$.", 'Second-order equations')


def zi_zs(rng):
    p1, p2 = rng.sample([1, 2, 3], 2)
    a1, a0 = p1 + p2, p1 * p2
    y0, yd0 = rng.choice([1, 2]), rng.choice([0, 1, -1])
    K = rng.choice([2, 6, 12])
    Yzi = ((s + a1) * y0 + yd0) / (s ** 2 + a1 * s + a0)
    Yzs = K / s / (s ** 2 + a1 * s + a0)
    rzi, rzs = ilt(Yzi), ilt(Yzs)
    st = f"For $y'' + {a1}y' + {a0}y = {K}u(t)$ with $y(0^-) = {y0}$, $y'(0^-) = {yd0}$, find the zero-input and zero-state responses separately, and hence the total response."
    steps = [('Split the transform', f"$Y(s) = \\underbrace{{\\dfrac{{{tex(sp.expand((s + a1)*y0 + yd0))}}}{{{tex(sp.factor(s**2 + a1*s + a0))}}}}}_{{\\text{{zero-input}}}} + \\underbrace{{\\dfrac{{{K}}}{{s{tex(sp.factor(s**2 + a1*s + a0))}}}}}_{{\\text{{zero-state}}}}$."),
             ('Zero-input response', f"${rzi['pf']}$, giving $y_{{zi}}(t) = {combo(rzi['pairs'])}$: what the system does on its own, starting from its initial state."),
             ('Zero-state response', f"${rzs['pf']}$, giving $y_{{zs}}(t) = {combo(rzs['pairs'])}$: the response to the input from rest."),
             ('Total', 'Add the two. The zero-state part is linear in the input; the zero-input part is linear in the initial state. The total is linear in neither alone, which is why the split is useful.')]
    tot = combo(rzi['pairs'] + rzs['pairs'])
    return Prob('C', st, steps, f"$y_{{zi}} = {combo(rzi['pairs'])}$, $y_{{zs}} = {combo(rzs['pairs'])}$; $y = y_{{zi}} + y_{{zs}}$.", 'Zero-input and zero-state')


def rlc(rng):
    case = cyc(rng, 'rl', ['under', 'over', 'crit', 'under'])
    L = 1
    if case == 'under':
        R, C = rng.choice([2, 4]), Q(1, rng.choice([5, 10, 13]))
    elif case == 'over':
        R, C = rng.choice([5, 6]), Q(1, rng.choice([4, 6]))
    else:
        R, C = 4, Q(1, 4)
    V = rng.choice([1, 5, 10])
    a1, a0 = sp.Integer(R) / L, 1 / (L * C)
    if case == 'over' and a1 ** 2 - 4 * a0 <= 0:
        R = 7
        a1 = sp.Integer(R)
    Y = V * a0 / (s * (s ** 2 + a1 * s + a0))
    r = ilt(Y)
    disc = a1 ** 2 - 4 * a0
    st = f"A series RLC circuit has $R = {R}\\ \\Omega$, $L = 1$ H and $C = {tex(C)}$ F, with no initial energy stored. A ${V}$ V step is applied at $t = 0$. Find the capacitor voltage $v_C(t)$."
    steps = [('Transfer function', f"$\\dfrac{{V_C}}{{V_{{in}}}} = \\dfrac{{1/LC}}{{s^2 + (R/L)s + 1/LC}} = \\dfrac{{{tex(a0)}}}{{s^2 + {tex(a1)}s + {tex(a0)}}}$."),
             ('Damping', f"Discriminant $(R/L)^2 - 4/LC = {tex(disc)}$: " + ('negative, so underdamped.' if disc < 0 else 'positive, so overdamped.' if disc > 0 else 'zero, so critically damped.')),
             ('Output transform', f"$V_C(s) = {tex(sp.factor(Y))} = {r['pf']}$.")]
    steps += [(f'Invert term {i+1}', d) for i, d in enumerate(r['descs'])]
    steps.append(('Check', f"$v_C(0) = 0$ and $v_C(\\infty) = {V}$ V, as the capacitor must charge to the source voltage."))
    return Prob('C', st, steps, f"$v_C(t) = {combo(r['pairs'])}$ V for $t \\ge 0$.", 'RLC circuits')


TEMPLATES = [(distinct, 7), (delayed, 4),
             (repeated, 6), (complex_poles, 6), (improper, 3), (first_order, 5), (rc_circuit, 3),
             (second_order, 8), (zi_zs, 4), (rlc, 4)]


def generate():
    return build_set(TEMPLATES, seed=808)


if __name__ == '__main__':
    from lap import verify
    for i, p in enumerate(generate(), 1):
        print(f'--- 8.{i} [{p.level}] {p.topic}\n{p.statement}\n  ANS: {p.answer}')
