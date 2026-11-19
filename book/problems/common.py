import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib import *  # noqa: F401,F403
from lib import rng


def build(chapter, plan, seed):
    """plan: list of (template_fn, count). Each fn(r, tag) -> Problem."""
    r = rng(seed)
    out = []
    seen = set()
    for fn, count in plan:
        for i in range(count):
            for _ in range(60):  # avoid printing the same question twice
                p = fn(r, f"c{chapter:02d}_{fn.__name__}_{i}")
                key = (p.text, p.answer)
                if key not in seen:
                    break
            seen.add(key)
            out.append(p)
    # stable order by level, keeping template grouping within a level
    out.sort(key=lambda p: p.level)
    for k, p in enumerate(out, 1):
        p.number = f"{chapter}.{k}"
    return out


def pick(r, seq):
    return seq[r.randrange(len(seq))]


RVALS = [1, 1.2, 1.5, 2, 2.2, 2.7, 3, 3.3, 3.9, 4, 4.7, 5, 5.6, 6, 6.8, 8, 8.2, 10, 12, 15, 18, 20, 22, 24, 27, 30, 33, 39, 40, 47, 50, 56, 60, 68, 82, 100]
RSMALL = [2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 24, 30, 40, 60]


def R_ohms(r, scale=None):
    base = pick(r, RSMALL)
    sc = scale if scale is not None else pick(r, [1, 1, 1000, 1000, 100])
    return base * sc


def step(head, body):
    return f"<b>{head}.</b> {body}"
