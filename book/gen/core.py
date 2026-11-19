"""Shared helpers for the problem generators.

Every problem is built from exact SymPy arithmetic so that the printed
answers are correct by construction.  The helpers here only deal with
presentation: LaTeX printing, phrasing variety and figure output.
"""
import os
import re
import random
import sympy as sp
from sympy.printing.latex import LatexPrinter

# ----------------------------------------------------------------- symbols
t = sp.Symbol('t', real=True)
tau = sp.Symbol('tau', real=True)
s = sp.Symbol('s')
z = sp.Symbol('z')
w = sp.Symbol('omega', real=True)
n = sp.Symbol('n', integer=True)
k = sp.Symbol('k', integer=True)
j = sp.I
pi = sp.pi
Q = sp.Rational


# Display-only function heads (never evaluated)
class u(sp.Function):      # u(t)
    pass


class ud(sp.Function):     # u[n]
    pass


class dl(sp.Function):     # delta(t)
    pass


class dd(sp.Function):     # delta[n]
    pass


class xf(sp.Function):
    pass


class Printer(LatexPrinter):
    def __init__(self, **kw):
        kw.setdefault('imaginary_unit', 'j')
        kw.setdefault('ln_notation', True)
        super().__init__(kw)

    def _print_Function(self, expr, exp=None):
        name = expr.func.__name__
        table = {'u': ('u', '()'), 'ud': ('u', '[]'), 'dl': (r'\delta', '()'),
                 'dd': (r'\delta', '[]'), 'xf': ('x', '()')}
        if name in table:
            head, br = table[name]
            args = ', '.join(self._print(a) for a in expr.args)
            out = f'{head}{br[0]}{args}{br[1]}'
            if exp is not None:
                out = f'{out}^{{{exp}}}'
            return out
        return super()._print_Function(expr, exp)

    def _print_Heaviside(self, expr, exp=None):
        out = f'u({self._print(expr.args[0])})'
        return out if exp is None else f'{out}^{{{exp}}}'

    def _print_DiracDelta(self, expr, exp=None):
        return rf'\delta({self._print(expr.args[0])})'


_P = Printer()


def tex(e):
    """LaTeX for a SymPy expression (j for the imaginary unit)."""
    if isinstance(e, str):
        return e
    out = _P.doprint(sp.sympify(e))
    out = out.replace(r'\left(t \right)', '(t)').replace(r'\left(n \right)', '(n)')
    if re.search(r'\\[a-zA-Z]+$', out):
        out += ' '
    return out


def num(e):
    """Pretty number: integers plain, rationals as fractions."""
    e = sp.nsimplify(e)
    return tex(e)


def dec(e, d=3):
    """Decimal approximation with d significant decimals, trimmed."""
    v = float(sp.N(e))
    txt = f'{v:.{d}f}'
    if '.' in txt:
        txt = txt.rstrip('0').rstrip('.')
    if txt == '-0':
        txt = '0'
    return txt


def cf(c):
    """Coefficient prefix: '' for 1, '-' for -1, else LaTeX of c."""
    c = sp.nsimplify(c)
    return '' if c == 1 else ('-' if c == -1 else tex(c))


def par(c):
    """LaTeX of c, bracketed if negative."""
    c = sp.nsimplify(c)
    return f'\\left({tex(c)}\\right)' if c < 0 else tex(c)


def expo(a, var='t'):
    """e^{-a t} written nicely for positive rational a."""
    a = sp.nsimplify(a)
    if a == 0:
        return '1'
    sign = '-' if a > 0 else ''
    a_abs = abs(a)
    coef = '' if a_abs == 1 else tex(a_abs)
    return f'e^{{{sign}{coef}{var}}}'


def term(c, body, first=False):
    """Format c*body with correct sign handling ('+ 3x', '- x', '2x')."""
    c = sp.nsimplify(c)
    if c == 0:
        return ''
    neg = c < 0
    a = -c if neg else c
    mag = '' if (a == 1 and body) else tex(a)
    if body and mag and not body.startswith('(') and not mag[-1].isdigit() and mag.startswith(r'\frac'):
        pass
    piece = f'{mag}{body}' if body else tex(a)
    if first:
        return ('-' if neg else '') + piece
    return (' - ' if neg else ' + ') + piece


def combo(pairs):
    """Join [(coef, body), ...] into a signed sum string."""
    out = ''
    for c, b in pairs:
        piece = term(c, b, first=(out == ''))
        out += piece
    return out if out else '0'


def poly_tex(coeffs, var='s'):
    """Polynomial from highest power down, e.g. [1, 3, 2] -> s^2 + 3s + 2."""
    deg = len(coeffs) - 1
    pairs = []
    for i, c in enumerate(coeffs):
        p = deg - i
        body = '' if p == 0 else (var if p == 1 else f'{var}^{{{p}}}')
        pairs.append((c, body))
    return combo(pairs)


def zpoly_tex(coeffs):
    """Polynomial in z^{-1}: [1, -0.5] -> 1 - 0.5 z^{-1}."""
    pairs = []
    for i, c in enumerate(coeffs):
        body = '' if i == 0 else ('z^{-1}' if i == 1 else f'z^{{-{i}}}')
        pairs.append((c, body))
    return combo(pairs)


def seq_tex(vals, start=0):
    """Finite sequence with the n = 0 sample marked by an up-arrow."""
    parts = [num(v) for v in vals]
    idx0 = -start
    if 0 <= idx0 < len(vals):
        parts[idx0] = r'\underset{\uparrow}{' + parts[idx0] + '}'
    else:
        parts[0] = r'\underset{\scriptscriptstyle n=' + str(start) + '}{' + parts[0] + '}'
    return r'\{' + r',\ '.join(parts) + r'\}'


# ------------------------------------------------------------ problem object
LEVELS = {'A': 'Warm-up', 'B': 'Core', 'C': 'Challenge'}


class Prob:
    def __init__(self, level, statement, steps, answer, topic='', fig=None, sol_fig=None):
        self.level = level
        self.statement = statement.strip()
        self.steps = steps
        self.answer = answer.strip()
        self.topic = topic
        self.fig = fig  # (path_without_ext, caption)
        self.sol_fig = sol_fig


def build_set(templates, seed, total=50):
    """templates: list of (func, count). Each func(rng) -> Prob."""
    rng = random.Random(seed)
    seen = set()
    out = []
    for func, count in templates:
        made, tries = 0, 0
        while made < count:
            tries += 1
            if tries > 400:
                raise RuntimeError(f'could not make unique problems for {func.__name__}')
            p = func(rng)
            key = p.statement
            if key in seen:
                continue
            seen.add(key)
            out.append(p)
            made += 1
    assert len(out) == total, (len(out), total)
    order = {'A': 0, 'B': 1, 'C': 2}
    out.sort(key=lambda p: order[p.level])  # stable: template order kept inside levels
    return out


def pick(rng, *options):
    return rng.choice(options)


_queues = {}


def cyc(rng, key, options):
    """Draw from options without repetition until all have been used."""
    q = _queues.get(key)
    if not q:
        q = list(options)
        rng.shuffle(q)
        _queues[key] = q
    return q.pop()


def eang(x):
    """e^{j theta} exponent text with the sign placed correctly."""
    v = float(sp.N(x))
    return f'e^{{-j{abs(v):.3f}}}' if v < 0 else f'e^{{j{v:.3f}}}'


# ------------------------------------------------------------------ figures
FIG_DIR = os.path.join(os.path.dirname(__file__), '..', 'figures', 'gen')
_fig_counter = {}


def save_fig(fig, name):
    import matplotlib.pyplot as plt
    os.makedirs(FIG_DIR, exist_ok=True)
    base = os.path.join(FIG_DIR, name)
    fig.savefig(base + '.pdf', bbox_inches='tight')
    fig.savefig(base + '.png', dpi=200, bbox_inches='tight')
    plt.close(fig)
    return 'figures/gen/' + name


def new_fig_name(prefix):
    _fig_counter[prefix] = _fig_counter.get(prefix, 0) + 1
    return f'{prefix}_{_fig_counter[prefix]:02d}'
