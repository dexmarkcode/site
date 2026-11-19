"""Chapter 2 - Systems and their properties."""
import numpy as np
import sympy as sp
from core import *

CH = 2

Y, N = 'Yes', 'No'
# expr, linear, TI, causal, memoryless, stable, reasons
LIB = [
    ('y(t) = t\\,x(t)', Y, N, Y, Y, N,
     ['Scaling and adding inputs scales and adds the products, so the system is linear.',
      'Delaying the input gives $t\\,x(t - t_0)$, but delaying the output gives $(t - t_0)x(t - t_0)$. The time-varying gain breaks time invariance.',
      'The output at $t$ uses only $x(t)$, so it is causal and memoryless.',
      'The bounded input $x(t) = 1$ produces $y(t) = t$, which grows without limit, so it is not BIBO stable.']),
    ('y(t) = x^2(t)', N, Y, Y, Y, Y,
     ['Doubling the input quadruples the output, so homogeneity fails: not linear.',
      'Shifting the input simply shifts $x^2$, so it is time-invariant.',
      'Only the present value is used: causal and memoryless.',
      'If $|x| \\le B$ then $|y| \\le B^2$, so it is stable.']),
    ('y(t) = x(t - 2)', Y, Y, Y, N, Y,
     ['A pure delay is linear.',
      'Delaying the input by $t_0$ delays the output by $t_0$: time-invariant.',
      'The output depends on the past value $x(t-2)$, so it is causal but has memory.',
      'The output is bounded by the same bound as the input: stable.']),
    ('y(t) = x(t + 1)', Y, Y, N, N, Y,
     ['A time advance is linear.',
      'An advance commutes with shifts, so it is time-invariant.',
      'The output at $t$ needs the input one second in the future: not causal, and it has memory.',
      'Bounded in, bounded out: stable.']),
    ('y(t) = x(2t)', Y, N, N, N, Y,
     ['Time compression is linear.',
      'Shifting the input by $t_0$ gives $x(2t - t_0)$, while shifting the output gives $x(2t - 2t_0)$. They differ, so it is time-varying.',
      'At $t = 1$ the output is $x(2)$, a future value: not causal, and not memoryless.',
      'Compression cannot make a bounded signal unbounded: stable.']),
    ('y(t) = x(-t)', Y, N, N, N, Y,
     ['Reversal is linear.',
      'Shifting the input gives $x(-t - t_0)$; shifting the output gives $x(-(t - t_0)) = x(-t + t_0)$. Not time-invariant.',
      'At $t = -1$ the output is $x(1)$, a future value: not causal, has memory.',
      'Stable, since the values are merely rearranged.']),
    ('y(t) = \\int_{-\\infty}^{t} x(\\tau)\\,d\\tau', Y, Y, Y, N, N,
     ['Integration is linear.',
      'The integrator commutes with shifts, so it is time-invariant.',
      'It uses all past values up to $t$: causal, with memory.',
      'A unit step input gives a ramp output, which is unbounded: not stable.']),
    ('y(t) = 3x(t) + 2', N, Y, Y, Y, Y,
     ['A zero input gives $y = 2$, not zero. Any linear system must map zero to zero, so this one is not linear; it is affine, sometimes called incrementally linear.',
      'The constant does not depend on time, so shifts commute: time-invariant.',
      'Only the present input is used: causal and memoryless.',
      '$|y| \\le 3B + 2$: stable.']),
    ('y(t) = x(t)\\cos(\\omega_c t)', Y, N, Y, Y, Y,
     ['A modulator is linear in $x$.',
      'Delaying the input gives $x(t - t_0)\\cos(\\omega_c t)$, not $x(t - t_0)\\cos(\\omega_c(t - t_0))$. Time-varying.',
      'Present value only: causal and memoryless.',
      '$|y| \\le |x| \\le B$: stable.']),
    ('y(t) = e^{x(t)}', N, Y, Y, Y, Y,
     ['$e^{x_1 + x_2} \\ne e^{x_1} + e^{x_2}$, so not linear.',
      'Time-invariant, since the rule is the same at every instant.',
      'Causal and memoryless.',
      'If $|x| \\le B$ then $y \\le e^B$: stable.']),
    ('y(t) = \\dfrac{dx(t)}{dt}', Y, Y, Y, N, N,
     ['Differentiation is linear.',
      'It commutes with shifts: time-invariant.',
      'The derivative depends on values in an arbitrarily small neighbourhood before $t$, so it is causal but conventionally regarded as having memory.',
      'A bounded step input produces an impulse, and $\\sin(t^2)$ is bounded while its derivative $2t\\cos(t^2)$ is not: unstable.']),
    ('y[n] = x[n] + x[n-1] + x[n-2]', Y, Y, Y, N, Y,
     ['A sum of delayed copies is linear.',
      'Every term is a fixed delay: time-invariant.',
      'Only present and past samples appear: causal, with memory.',
      '$|y| \\le 3B$: stable. Any FIR filter is stable.']),
    ('y[n] = n\\,x[n]', Y, N, Y, Y, N,
     ['Linear in $x$.',
      'The gain $n$ changes with time: time-varying.',
      'Causal and memoryless.',
      '$x[n] = 1$ gives $y[n] = n$, unbounded: not stable.']),
    ('y[n] = x[2n]', Y, N, N, N, Y,
     ['A down-sampler is linear.',
      'A one-sample delay of the input gives $x[2n - 1]$; a one-sample delay of the output gives $x[2n - 2]$. Time-varying.',
      'At $n = 1$ the output is $x[2]$: not causal, has memory.',
      'Stable, since it only discards samples.']),
    ('y[n] = \\sum_{k=-\\infty}^{n} x[k]', Y, Y, Y, N, N,
     ['The accumulator is linear.',
      'It commutes with shifts: time-invariant.',
      'Causal, with memory of the entire past.',
      'A unit step input gives $y[n] = (n + 1)u[n]$, unbounded: not stable.']),
    ('y[n] = x[n]\\,x[n-1]', N, Y, Y, N, Y,
     ['Doubling the input quadruples the output: not linear.',
      'Time-invariant.',
      'Causal, with memory of one sample.',
      '$|y| \\le B^2$: stable.']),
    ('y[n] = x[-n]', Y, N, N, N, Y,
     ['Linear.', 'Reversal does not commute with shifts: time-varying.',
      'At $n = -2$ the output is $x[2]$: not causal, has memory.', 'Stable.']),
    ('y[n] = \\tfrac12 y[n-1] + x[n] \\text{ (initially at rest)}', Y, Y, Y, N, Y,
     ['A linear constant-coefficient difference equation that starts at rest is linear.',
      'With constant coefficients and initial rest, it is time-invariant.',
      'Each output uses the present input and past outputs only: causal, with memory.',
      'Its impulse response is $(\\tfrac12)^n u[n]$, which is absolutely summable (the sum is 2): stable.']),
    ('y[n] = 2y[n-1] + x[n] \\text{ (initially at rest)}', Y, Y, Y, N, N,
     ['Linear, starting from rest.', 'Constant coefficients: time-invariant.', 'Causal, with memory.',
      'Its impulse response $2^n u[n]$ grows without bound, so it is not stable.']),
    ('y[n] = |x[n]|', N, Y, Y, Y, Y,
     ['$|{-x}| = |x|$, so scaling by $-1$ fails: not linear.', 'Time-invariant.', 'Causal and memoryless.', '$|y| \\le B$: stable.']),
    ('y(t) = x(t/2)', Y, N, N, N, Y,
     ['Linear.', 'Shifting the input gives $x(t/2 - t_0)$ but shifting the output gives $x((t - t_0)/2)$: time-varying.',
      'For $t = -2$ the output is $x(-1)$, a future value, so it is not causal; it has memory.', 'Stable.']),
]


def classify(rng):
    e = cyc(rng, 'lib', LIB)
    expr, L, T, C, M, S, why = e
    st = (f"Classify the system ${expr}$. State, with a reason for each, whether it is linear, time-invariant, causal, memoryless and BIBO stable.")
    steps = [('Linearity', why[0] + ' The test is superposition: the response to $a x_1 + b x_2$ must equal $a y_1 + b y_2$.'),
             ('Time invariance', why[1]),
             ('Causality and memory', why[2]),
             ('Stability', why[3])]
    ans = f"Linear: {L}. Time-invariant: {T}. Causal: {C}. Memoryless: {M}. Stable: {S}."
    return Prob('B', st, steps, ans, 'Classifying systems')


def lti_numeric(rng):
    a = cyc(rng, 'ltia', [1, 2, 3, 4, Q(1, 2)])
    c1 = rng.choice([2, 3, 4, -2])
    c2 = rng.choice([-1, -2, 1, 3])
    t1 = rng.choice([1, 2])
    t2 = t1 + rng.choice([1, 2, 3])
    sresp = f"(1 - {expo(a)})u(t)"
    st = (f"An LTI system responds to the unit step $u(t)$ with $s(t) = {sresp}$. Find its response to "
          f"$x(t) = {combo([(c1, f'u(t - {t1})'), (c2, f'u(t - {t2})')])}$.")
    def shifted(T):
        return f"\\left(1 - {expo(a, f'(t - {T})')}\\right)u(t - {T})"
    yexpr = combo([(c1, shifted(t1)), (c2, shifted(t2))])
    steps = [('Express the input in terms of the known input', f"The input is a weighted sum of delayed unit steps: ${c1}$ times $u(t)$ delayed by ${t1}$, plus ${c2}$ times $u(t)$ delayed by ${t2}$."),
             ('Use linearity and time invariance', "Linearity lets us scale and add responses; time invariance says that a delayed input produces an equally delayed output. So each step produces a correspondingly scaled and delayed copy of $s(t)$."),
             ('Write the output', f"$y(t) = {c1}\\,s(t - {t1}) {'+' if c2 > 0 else '-'} {abs(c2)}\\,s(t - {t2})$, that is $$y(t) = {yexpr}.$$"),
             ('Sanity check', f"For large $t$ each bracket tends to one, so $y \\to {c1 + c2}$, which is the final value of the input multiplied by the DC gain of one. That is consistent.")]
    return Prob('A', st, steps, f"$y(t) = {yexpr}$.", 'Using LTI properties')


def bibo(rng):
    case = cyc(rng, 'bibo', ['dgeo', 'cexp', 'dgrow', 'cexpgrow', 'dstep', 'calt', 'dpoly'])
    if case == 'dgeo':
        a = rng.choice([Q(1, 2), Q(-1, 3), Q(3, 4), Q(-4, 5)])
        st = f"Is the LTI system with impulse response $h[n] = \\left({tex(a)}\\right)^n u[n]$ BIBO stable?"
        S = 1 / (1 - abs(a))
        steps = [('Criterion', 'An LTI system is BIBO stable exactly when its impulse response is absolutely summable.'),
                 ('Sum', f"$\\sum_n |h[n]| = \\sum_{{n\\ge0}} \\left({tex(abs(a))}\\right)^n = \\dfrac{{1}}{{1 - {tex(abs(a))}}} = {tex(S)}$."),
                 ('Conclusion', 'The sum is finite, so the system is stable.')]
        ans = f"Stable; $\\sum|h[n]| = {tex(S)}$."
    elif case == 'dgrow':
        a = rng.choice([Q(3, 2), -2, Q(5, 4)])
        st = f"Is the LTI system with impulse response $h[n] = \\left({tex(a)}\\right)^n u[n]$ BIBO stable?"
        steps = [('Criterion', 'Stable if and only if $\\sum|h[n]| < \\infty$.'),
                 ('Test', f"$|h[n]| = \\left({tex(abs(a))}\\right)^n$ grows with $n$, so the terms do not even tend to zero and the sum diverges.")]
        ans = 'Not stable.'
    elif case == 'cexp':
        a = rng.choice([1, 2, 3, 5])
        b = rng.choice([1, 2, 4])
        st = f"Is the system with $h(t) = {b}{expo(a)}u(t)$ BIBO stable? What is the largest possible output if $|x(t)| \\le 1$?"
        I = Q(b, a)
        steps = [('Criterion', 'Stable if and only if $\\int|h(t)|\\,dt < \\infty$.'),
                 ('Integrate', f"$\\int_0^\\infty {b}{expo(a)}\\,dt = {tex(I)}$, which is finite, so the system is stable."),
                 ('Worst case', f"$|y(t)| \\le \\int |h(\\tau)||x(t - \\tau)|\\,d\\tau \\le {tex(I)}$, with equality for $x = 1$. The integral of $|h|$ is precisely the worst-case gain.")]
        ans = f"Stable, and $|y| \\le {tex(I)}$."
    elif case == 'cexpgrow':
        a = rng.choice([1, 2, Q(1, 2)])
        st = f"Is the system with $h(t) = {expo(-a)}u(t)$ BIBO stable?"
        steps = [('Criterion', 'Stable if and only if $h$ is absolutely integrable.'),
                 ('Test', f"${expo(-a)}$ grows exponentially, so $\\int_0^\\infty {expo(-a)}\\,dt$ diverges. Not stable.")]
        ans = 'Not stable.'
    elif case == 'dstep':
        N0 = rng.choice([4, 5, 8])
        st = f"Is the system with $h[n] = u[n] - u[n - {N0}]$ stable? Is it FIR or IIR?"
        steps = [('Shape of $h$', f"$h[n]$ is a run of ${N0}$ ones starting at $n = 0$: a moving sum."),
                 ('Sum', f"$\\sum|h[n]| = {N0} < \\infty$, so stable. With finitely many non-zero samples it is an FIR system, and every FIR system is stable.")]
        ans = f"Stable (FIR), $\\sum|h| = {N0}$."
    elif case == 'calt':
        w0 = rng.choice([2, 3, 5])
        st = f"Is the system with $h(t) = \\cos({w0}t)u(t)$ BIBO stable?"
        steps = [('Test', f"$\\int_0^\\infty |\\cos({w0}t)|\\,dt$ adds a fixed positive area $2/{w0}$ every half period and so diverges."),
                 ('Physical picture', f"This is an undamped resonator; driving it with $\\cos({w0}t)$, a bounded input, makes the output grow like $t$.")]
        ans = 'Not stable.'
    else:
        st = "Is the system with $h[n] = \\dfrac{1}{n}u[n-1]$ BIBO stable?"
        steps = [('Test', 'The sum $\\sum_{n\\ge1} 1/n$ is the harmonic series, which diverges.'),
                 ('Comment', 'The impulse response decays to zero, yet the system is still unstable. Decay alone is not enough; it must decay fast enough to be summable.')]
        ans = 'Not stable.'
    return Prob('A', st, steps, ans, 'BIBO stability')


def causal_mem(rng):
    a = rng.choice([1, 2, 3])
    t0 = rng.choice([-2, -1, 1, 2, 3])
    K = rng.choice([2, 3, 5])
    kind = cyc(rng, 'cm', ['exp', 'delta', 'exp', 'dt'])
    if kind == 'exp':
        st = f"An LTI system has $h(t) = {expo(a, f'(t {'-' if t0 > 0 else '+'} {abs(t0)})')}u(t {'-' if t0 > 0 else '+'} {abs(t0)})$. Is it causal? Is it memoryless?"
        caus = t0 >= 0
        steps = [('Causality test for LTI systems', 'An LTI system is causal exactly when $h(t) = 0$ for $t < 0$.'),
                 ('Apply it', f"$h(t)$ switches on at $t = {t0}$. " + ('This is after the origin, so $h$ is zero for negative time: causal.' if caus else 'This is before the origin, so $h$ is non-zero for some negative times: not causal.')),
                 ('Memory', 'An LTI system is memoryless only if $h(t) = K\\delta(t)$. This $h$ is spread over time, so the system has memory.')]
        ans = ('Causal' if caus else 'Not causal') + '; has memory.'
    elif kind == 'delta':
        st = f"An LTI system has $h(t) = {K}\\delta(t {'-' if t0 > 0 else '+'} {abs(t0)})$. Describe what it does, and state whether it is causal and memoryless."
        steps = [('Interpret', f"Convolving with a shifted impulse shifts: $y(t) = {K}x(t {'-' if t0 > 0 else '+'} {abs(t0)})$, " + ('a scaled delay.' if t0 > 0 else 'a scaled advance.')),
                 ('Causality', 'Causal.' if t0 > 0 else 'Not causal, because the output needs future input.'),
                 ('Memory', 'Not memoryless, because the output depends on the input at a different time. Only $K\\delta(t)$ itself is memoryless.')]
        ans = ('Causal' if t0 > 0 else 'Not causal') + '; has memory.'
    else:
        b = rng.choice([Q(1, 2), Q(1, 3)])
        st = f"An LTI system has $h[n] = \\left({tex(b)}\\right)^n u[n {'-' if t0 > 0 else '+'} {abs(t0)}]$. Is it causal? Is it stable?"
        caus = t0 >= 0
        steps = [('Causality', f"The response starts at $n = {t0}$. " + ('Nothing before $n = 0$: causal.' if caus else 'There are non-zero samples at negative $n$: not causal.')),
                 ('Stability', f"$\\sum |h[n]| = \\sum_{{n\\ge{t0}}} ({tex(b)})^n = ({tex(b)})^{{{t0}}}/(1 - {tex(b)}) = {tex(b**t0/(1-b))}$, which is finite: stable.")]
        ans = ('Causal' if caus else 'Not causal') + ' and stable.'
    return Prob('A', st, steps, ans, 'Causality and memory')


def step_from_impulse(rng):
    if rng.random() < 0.5:
        a = cyc(rng, 'sfa', [1, 2, 3, 4, 5])
        A = rng.choice([2, 3, 6, 10])
        st = f"An LTI system has impulse response $h(t) = {A}{expo(a)}u(t)$. Find its step response $s(t)$ and its final value."
        fin = Q(A, a)
        steps = [('Link between the two', 'The step response is the running integral of the impulse response, $s(t) = \\int_{-\\infty}^{t} h(\\tau)\\,d\\tau$.'),
                 ('Integrate', f"For $t > 0$: $s(t) = \\int_0^t {A}{expo(a, '\\tau')}\\,d\\tau = {cf(fin)}\\left(1 - {expo(a)}\\right)$."),
                 ('Final value', f"As $t \\to \\infty$, $s(t) \\to {tex(fin)}$, which equals $\\int h$, the DC gain.")]
        ans = f"$s(t) = {cf(fin)}(1 - {expo(a)})u(t)$, final value ${tex(fin)}$."
    else:
        a = cyc(rng, 'sfd', [Q(1, 2), Q(1, 3), Q(-1, 2), Q(2, 3), Q(3, 4)])
        A = rng.choice([1, 2, 3])
        st = f"Find the step response of the LTI system with $h[n] = {A if A > 1 else ''}\\left({tex(a)}\\right)^n u[n]$, and evaluate $s[3]$."
        s3 = A * (1 - a ** 4) / (1 - a)
        steps = [('Running sum', 'In discrete time the step response is $s[n] = \\sum_{k=-\\infty}^{n} h[k]$.'),
                 ('Geometric series', f"For $n \\ge 0$: $s[n] = {A}\\sum_{{k=0}}^{{n}} ({tex(a)})^k = {A}\\,\\dfrac{{1 - ({tex(a)})^{{n+1}}}}{{1 - {tex(a)}}} = {tex(A/(1-a))}\\left[1 - \\left({tex(a)}\\right)^{{n+1}}\\right]$."),
                 ('Evaluate', f"$s[3] = {tex(A/(1-a))}\\left[1 - ({tex(a)})^4\\right] = {tex(s3)}$. Check by direct addition: $" + ' + '.join(par(A * a ** k) for k in range(4)) + f" = {tex(s3)}$.")]
        ans = f"$s[n] = {tex(A/(1-a))}[1 - ({tex(a)})^{{n+1}}]u[n]$, $s[3] = {tex(s3)}$."
    return Prob('B', st, steps, ans, 'Step response')


def inverse_sys(rng):
    case = cyc(rng, 'inv', ['fir', 'iir', 'acc', 'delay', 'fir2'])
    a = rng.choice([Q(1, 2), Q(1, 4), 2, 3, Q(3, 4)])
    if case == 'fir':
        st = f"Find the inverse of the system $y[n] = x[n] - {tex(a)}x[n-1]$ and comment on its stability."
        steps = [('Solve for the input', f"Rearranging, $x[n] = y[n] + {tex(a)}x[n-1]$. The inverse system takes $y$ as its input and produces $w[n] = x[n]$."),
                 ('State the inverse', f"$w[n] = {tex(a)}w[n-1] + y[n]$, a recursive (IIR) system."),
                 ('Check by cascade', f"Its impulse response is $({tex(a)})^n u[n]$. Convolving with the original $\\delta[n] - {tex(a)}\\delta[n-1]$ gives $({tex(a)})^n u[n] - ({tex(a)})^n u[n-1] = \\delta[n]$, the identity."),
                 ('Stability', 'Stable, because the ratio is less than one.' if abs(a) < 1 else 'Not stable, because the ratio exceeds one: an inverse can exist mathematically yet be unusable in practice.')]
        ans = f"$w[n] = {tex(a)}w[n-1] + y[n]$; " + ('stable.' if abs(a) < 1 else 'unstable.')
    elif case == 'iir':
        st = f"The system $y[n] = {tex(a)}y[n-1] + x[n]$ is initially at rest. Find its inverse."
        steps = [('Rearrange', f"$x[n] = y[n] - {tex(a)}y[n-1]$."),
                 ('Interpret', f"The inverse is the FIR system $w[n] = v[n] - {tex(a)}v[n-1]$ driven by $v = y$, with impulse response $\\delta[n] - {tex(a)}\\delta[n-1]$."),
                 ('Note', 'An FIR inverse is always stable, even when the original recursive system is not.')]
        ans = f"$w[n] = v[n] - {tex(a)}v[n-1]$."
    elif case == 'acc':
        st = "Show that the first-difference system $w[n] = v[n] - v[n-1]$ is the inverse of the accumulator $y[n] = \\sum_{k=-\\infty}^{n}x[k]$."
        steps = [('Apply the difference to the accumulator output', '$y[n] - y[n-1] = \\sum_{k\\le n}x[k] - \\sum_{k\\le n-1}x[k] = x[n]$.'),
                 ('Conclusion', 'The cascade returns the input unchanged, so the first difference inverts the accumulator. In impulse-response terms, $u[n] * (\\delta[n] - \\delta[n-1]) = \\delta[n]$.')]
        ans = 'The cascade gives $x[n]$, so the two systems are inverses.'
    elif case == 'delay':
        T = rng.choice([2, 3, 5])
        K = rng.choice([2, 4, 5])
        st = f"Find the inverse of $y(t) = {K}x(t - {T})$. Is the inverse causal?"
        steps = [('Undo each operation', f"Undo the gain by dividing by ${K}$, and undo the delay by advancing by ${T}$."),
                 ('Inverse', f"$w(t) = \\tfrac{{1}}{{{K}}}\\,v(t + {T})$, with impulse response $\\tfrac{{1}}{{{K}}}\\delta(t + {T})$."),
                 ('Causality', 'The inverse needs future values, so it is not causal. A pure delay can only be undone if we are prepared to wait.')]
        ans = f"$w(t) = \\tfrac{{1}}{{{K}}}v(t + {T})$; not causal."
    else:
        b = rng.choice([2, 3])
        st = f"Is $y(t) = x^{b}(t)$ invertible? Justify your answer."
        if b == 2:
            steps = [('Test for one-to-one', 'The inputs $x(t) = 1$ and $x(t) = -1$ both give $y(t) = 1$.'),
                     ('Conclusion', 'Two different inputs give the same output, so no inverse can exist.')]
            ans = 'Not invertible.'
        else:
            steps = [('Test for one-to-one', 'The cube is strictly increasing on the reals, so distinct values of $x$ give distinct values of $y$.'),
                     ('Inverse', 'The inverse is $w(t) = \\sqrt[3]{v(t)}$, which is also memoryless and non-linear.')]
            ans = 'Invertible: $w(t) = v(t)^{1/3}$.'
    return Prob('B', st, steps, ans, 'Invertibility')


def interconnect(rng):
    L = 3
    h1 = [rng.choice([-2, -1, 1, 2, 3]) for _ in range(rng.choice([2, 3]))]
    h2 = [rng.choice([-1, 1, 2]) for _ in range(2)]
    h3 = [rng.choice([-1, 1, 2, 3])]
    form = cyc(rng, 'ic', ['casc_par', 'par_casc'])
    if form == 'casc_par':
        c = np.convolve(h1, h2)
        tot = list(c)
        tot[0] += h3[0]
        desc = "The systems with impulse responses $h_1$ and $h_2$ are in cascade, and the pair is in parallel with $h_3$."
        steps = [('Cascade first', f"A cascade convolves: $h_1 * h_2 = {seq_tex(c, 0)}$."),
                 ('Then the parallel branch', f"Parallel branches add: $h = (h_1 * h_2) + h_3$. Since $h_3 = {h3[0]}\\delta[n]$, only the $n = 0$ sample changes."),
                 ('Result', f"$h[n] = {seq_tex(tot, 0)}$.")]
    else:
        s23 = list(h2)
        s23[0] += h3[0]
        tot = list(np.convolve(h1, s23))
        desc = "The system $h_1$ is in cascade with the parallel combination of $h_2$ and $h_3$."
        steps = [('Parallel pair', f"$h_2 + h_3 = {seq_tex(s23, 0)}$."),
                 ('Cascade', f"$h = h_1 * (h_2 + h_3)$. Multiply out sample by sample, as with polynomial multiplication."),
                 ('Result', f"$h[n] = {seq_tex(tot, 0)}$.")]
    st = (f"{desc} With $h_1[n] = {seq_tex(h1, 0)}$, $h_2[n] = {seq_tex(h2, 0)}$ and $h_3[n] = {h3[0]}\\delta[n]$, find the overall impulse response.")
    g1, g2, g3 = sum(h1), sum(h2), h3[0]
    gexp = f"({g1})({g2}) + ({g3})" if form == 'casc_par' else f"({g1})\\big(({g2}) + ({g3})\\big)"
    steps.append(('Check with DC gains', f"The samples of $h$ sum to ${sum(int(v) for v in tot)}$. The DC gains of the parts combine in the same way as the systems: ${gexp} = {sum(int(v) for v in tot)}$. They agree."))
    return Prob('C', st, steps, f"$h[n] = {seq_tex([int(v) for v in tot], 0)}$.", 'Interconnections')


def eigen(rng):
    a = cyc(rng, 'eg', [1, 2, 3, 4, 5])
    w0 = rng.choice([1, 2, 3, 4, 5])
    A = rng.choice([1, 2, 4, 5])
    H = 1 / (a + j * w0)
    mag = sp.sqrt(sp.Integer(a * a + w0 * w0))
    ph = -sp.atan(sp.Rational(w0, a))
    st = (f"An LTI system has impulse response $h(t) = {expo(a)}u(t)$. Find its output when the input is $x(t) = {A if A > 1 else ''}\\cos({w0 if w0 > 1 else ''}t)$ for all $t$.")
    steps = [('Complex exponentials are eigenfunctions', 'For an LTI system the input $e^{j\\omega t}$ produces $H(j\\omega)e^{j\\omega t}$, where $H(j\\omega) = \\int h(\\tau)e^{-j\\omega\\tau}d\\tau$.'),
             ('Compute the gain', f"$H(j\\omega) = \\int_0^\\infty {expo(a, '\\tau')}e^{{-j\\omega\\tau}}d\\tau = \\dfrac{{1}}{{{a} + j\\omega}}$. At $\\omega = {w0}$: $H = \\dfrac{{1}}{{{a} + j{w0}}}$."),
             ('Polar form', f"$|H| = 1/\\sqrt{{{a*a + w0*w0}}} \\approx {dec(1/mag, 4)}$ and $\\angle H = -\\tan^{{-1}}({w0}/{a}) \\approx {dec(ph, 4)}$ rad."),
             ('Assemble the output', "A real system with a cosine input gives a cosine output scaled by $|H|$ and shifted by $\\angle H$.")]
    amp = A / mag
    ans = f"$y(t) = {tex(sp.nsimplify(amp))}\\cos({w0 if w0 > 1 else ''}t - {dec(-ph, 4)}) \\approx {dec(amp, 4)}\\cos({w0 if w0 > 1 else ''}t - {dec(-ph, 4)})$."
    return Prob('C', st, steps, ans, 'Eigenfunctions')


def diffeq_h(rng):
    a = cyc(rng, 'dh', [Q(1, 2), Q(-1, 2), Q(1, 3), Q(3, 4), Q(2, 3)])
    b = rng.choice([1, 2, 3])
    c = rng.choice([-1, 1, 2, -2])
    hv = [sp.Integer(b)] + [b * a ** m + c * a ** (m - 1) for m in range(1, 5)]
    st = f"Find the impulse response of the causal system $y[n] - {tex(a) if a > 0 else '(' + tex(a) + ')'}\\,y[n-1] = {b}x[n] {'+' if c > 0 else '-'} {abs(c)}x[n-1]$, initially at rest, both by recursion and in closed form."
    steps = [('Recursion', f"Set $x[n] = \\delta[n]$ and $h[n] = 0$ for $n < 0$. Then $h[n] = {tex(a)}h[n-1] + {b}\\delta[n] + ({c})\\delta[n-1]$."),
             ('First samples', ', '.join(f"$h[{m}] = {tex(v)}$" for m, v in enumerate(hv)) + '.'),
             ('Closed form', f"The recursive part alone has response $({tex(a)})^n u[n]$. By linearity and time invariance the right-hand side gives ${b}$ times that, plus ${c}$ times a one-sample delayed copy: $$h[n] = {b}\\left({tex(a)}\\right)^n u[n] {'+' if c > 0 else '-'} {cf(abs(c))}\\left({tex(a)}\\right)^{{n-1}}u[n-1].$$"),
             ('Cross-check', f"At $n = 2$ the formula gives ${tex(hv[2])}$, matching the recursion.")]
    return Prob('C', st, steps, f"$h[n] = {b}({tex(a)})^n u[n] {'+' if c > 0 else '-'} {cf(abs(c))}({tex(a)})^{{n-1}}u[n-1]$.", 'Impulse response from a difference equation')


TEMPLATES = [(lti_numeric, 5), (bibo, 5), (causal_mem, 4),
             (classify, 12), (step_from_impulse, 5), (inverse_sys, 5),
             (interconnect, 6), (eigen, 5), (diffeq_h, 3)]
PROBLEM_INTRO = "For classification problems, always give a reason: a bare yes or no earns nothing in an examination and teaches you nothing here."


def generate():
    return build_set(TEMPLATES, seed=202)


if __name__ == '__main__':
    for i, p in enumerate(generate(), 1):
        print(f'--- 2.{i} [{p.level}] {p.topic}\n{p.statement}\n  ANS: {p.answer}')
