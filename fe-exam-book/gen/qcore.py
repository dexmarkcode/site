"""Core helpers for the question engine: number formatting, option builders, registry."""
import math
import random
from dataclasses import dataclass, field

NBSP = " "
MINUS = "−"
PREF = {12: "T", 9: "G", 6: "M", 3: "k", 0: "", -3: "m", -6: "μ", -9: "n", -12: "p"}
E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]


@dataclass
class Q:
    stem: str
    options: list
    answer: int
    solution: str
    topic: str = ""
    fig: str = None
    tid: str = ""


REG = {}


def tpl(topic):
    def deco(f):
        REG.setdefault(topic, []).append(f)
        f.topic = topic
        return f
    return deco


# ---------------------------------------------------------------- numbers
def siground(x, sig=3):
    if x == 0 or not math.isfinite(x):
        return x
    return round(x, sig - 1 - int(math.floor(math.log10(abs(x)))))


def _plain(x, sig, ascii_minus=False, comma=True):
    if x == 0:
        return "0"
    x = siground(x, sig)
    ax = abs(x)
    mag = int(math.floor(math.log10(ax)))
    neg = ("-" if ascii_minus else MINUS) if x < 0 else ""
    if mag >= 7 or mag <= -4:
        m = siground(x / 10 ** mag, sig)
        if abs(m) >= 10:
            m /= 10
            mag += 1
        return None, neg, f"{abs(m):.{sig-1}f}", mag
    dec = max(sig - 1 - mag, 0)
    s = f"{ax:,.{dec}f}" if comma else f"{ax:.{dec}f}"
    return s, neg, None, None


def fnum(x, sig=3):
    """Plain number for running text (Unicode minus, thousands commas, sci for extremes)."""
    if x == 0:
        return "0"
    r = _plain(x, sig)
    if isinstance(r, str):
        return r
    s, neg, mant, mag = r
    if s is not None:
        return neg + s
    exp = str(mag).replace("-", MINUS)
    return f"{neg}{mant}{NBSP}×{NBSP}10^{exp}^"


def mnum(x, sig=3):
    """Number for use inside LaTeX math."""
    if x == 0:
        return "0"
    r = _plain(x, sig, ascii_minus=True)
    if isinstance(r, str):
        return r
    s, neg, mant, mag = r
    if s is not None:
        return neg + s.replace(",", "{,}")
    return f"{neg}{mant}\\times 10^{{{mag}}}"


def _engparts(x, sig=3):
    if x == 0:
        return "0", ""
    e = int(math.floor(math.log10(abs(x)) / 3)) * 3
    e = max(-12, min(12, e))
    m = siground(x / 10 ** e, sig)
    if abs(m) >= 1000 and e < 12:
        e += 3
        m = siground(x / 10 ** e, sig)
    mag = int(math.floor(math.log10(abs(m)))) if m != 0 else 0
    dec = max(sig - 1 - mag, 0)
    return (("-" if m < 0 else "") + f"{abs(m):.{dec}f}"), PREF[e]


def eng(x, unit, sig=3):
    n, p = _engparts(x, sig)
    return n.replace("-", MINUS) + NBSP + p + unit


def em(x, unit, sig=3):
    n, p = _engparts(x, sig)
    return n + "\\,\\text{" + p + unit + "}"


def fu(x, unit, sig=3):
    """plain number + unit (no prefix), text."""
    return fnum(x, sig) + (NBSP + unit if unit else "")


def mu(x, unit, sig=3):
    return mnum(x, sig) + ("\\,\\text{" + unit + "}" if unit else "")


def frac(a, b):
    return "\\frac{" + str(a) + "}{" + str(b) + "}"


def sq(a):
    return "\\sqrt{" + str(a) + "}"


def R(rng, lo=100, hi=10_000):
    vals = []
    d = 1
    while d <= hi * 10:
        for v in E12:
            x = round(v * d, 6)
            if lo <= x <= hi:
                vals.append(x)
        d *= 10
    return rng.choice(vals)


def pick(rng, seq):
    return rng.choice(list(seq))


# ---------------------------------------------------------------- options
def num_mcq(rng, correct, wrongs, fmt, integer=False, positive=True):
    """Return (options, answer_index). Options are sorted ascending, as on the real exam.
    Error-based distractors are preferred; the correct option's position is randomised."""
    cs = fmt(correct)
    seen = {cs}
    pool = []
    for w in wrongs:
        if w is None or not isinstance(w, (int, float)) or not math.isfinite(w):
            continue
        if positive and correct > 0 and w <= 0:
            continue
        s = fmt(w)
        if s in seen:
            continue
        seen.add(s)
        pool.append((w, s))
    below = [p for p in pool if p[0] < correct]
    above = [p for p in pool if p[0] > correct]
    p = rng.randrange(4)
    nb, na = p, 3 - p
    # if not enough natural distractors on one side, shift position before using fillers
    rng.shuffle(below)
    rng.shuffle(above)
    chosen = below[:nb] + above[:na]
    if integer:
        steps = [1, 2, 3, 4, 5, 6, 8, 10]
        fill_b = [correct - s for s in steps]
        fill_a = [correct + s for s in steps]
    else:
        a = abs(correct)
        fill_b = [correct - a * f for f in (0.25, 0.4, 0.5, 0.6, 0.15, 0.7)]
        fill_a = [correct + a * f for f in (0.33, 0.5, 1.0, 0.2, 1.5, 2.0)]
    bi = ai = 0
    nb_have = len([c for c in chosen if c[0] < correct])
    while nb_have < nb and bi < len(fill_b):
        w = fill_b[bi]
        bi += 1
        if positive and correct > 0 and w <= 0:
            continue
        s = fmt(w)
        if s in seen:
            continue
        seen.add(s)
        chosen.append((w, s))
        nb_have += 1
    while len(chosen) < 3:
        w = fill_a[ai % len(fill_a)] * (1 + 0.37 * (ai // len(fill_a)))
        ai += 1
        s = fmt(w)
        if s in seen:
            continue
        seen.add(s)
        chosen.append((w, s))
    allopts = chosen + [(correct, cs)]
    allopts.sort(key=lambda t: t[0])
    labels = [s for _, s in allopts]
    return labels, labels.index(cs)


def str_mcq(rng, correct, wrongs):
    opts = [correct]
    for w in wrongs:
        if w not in opts:
            opts.append(w)
    opts = opts[:4]
    assert len(opts) == 4, (correct, wrongs)
    rng.shuffle(opts)
    return opts, opts.index(correct)


def make(stem, opts_ans, sol, fig=None):
    opts, ans = opts_ans
    return Q(stem=stem, options=opts, answer=ans, solution=sol, fig=fig)


def poly(terms):
    """terms: list of (coef, varpart) -> LaTeX polynomial string."""
    out = ""
    for c, v in terms:
        if c == 0:
            continue
        sign = "-" if c < 0 else "+"
        a = abs(c)
        cstr = "" if (a == 1 and v) else (mnum(a, 4) if isinstance(a, float) else str(a))
        if not out:
            out = ("-" if c < 0 else "") + cstr + v
        else:
            out += f" {sign} " + cstr + v
    return out or "0"
