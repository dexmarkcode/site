"""Shared helpers for the Electric Circuits Workbook build.

Formatting of engineering quantities, the Problem record, and circuit
diagram helpers built on schemdraw.  Every numerical answer in the book is
computed here rather than typed by hand, so solutions stay consistent with
the values printed in the questions.
"""
import math
import cmath
import os
import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

plt.rcParams["mathtext.fontset"] = "stix"
plt.rcParams["font.family"] = "STIXGeneral"
schemdraw.config(fontsize=12.5, font="STIXGeneral", lw=1.3)

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(HERE, "build", "figs")
os.makedirs(FIGDIR, exist_ok=True)

NBSP = " "
MINUS = "−"

PREFIX = {-15: "f", -12: "p", -9: "n", -6: "μ", -3: "m", 0: "", 3: "k", 6: "M", 9: "G"}


def _sig(x, sig):
    """Round to sig significant figures and return a tidy string."""
    if x == 0:
        return "0"
    r = round(x, sig - 1 - int(math.floor(math.log10(abs(x)))))
    s = f"{r:.{max(sig - 1 - int(math.floor(math.log10(abs(r)))), 0)}f}" if r != 0 else "0"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s.replace("-", MINUS)


def num(x, sig=4):
    """Plain number, sig figs, typographic minus."""
    if abs(x) < 1e-12:
        return "0"
    if abs(x) >= 1e6 or abs(x) < 1e-3:
        e = int(math.floor(math.log10(abs(x))))
        m = x / 10 ** e
        return f"{_sig(m, sig)} × 10<sup>{str(e).replace('-', MINUS)}</sup>"
    return _sig(x, sig)


def eng(x, unit="", sig=3, html=True):
    """Engineering notation with SI prefix, e.g. 4700 -> '4.7 kΩ'."""
    if abs(x) < 1e-15:
        return f"0{NBSP}{unit}".strip()
    e = int(math.floor(math.log10(abs(x)) / 3) * 3)
    e = max(-15, min(9, e))
    m = x / 10 ** e
    ms = _sig(m, sig)
    if ms.replace(MINUS, "") in ("1000",) and e < 9:
        e += 3
        ms = _sig(x / 10 ** e, sig)
    sp = NBSP if html else " "
    return f"{ms}{sp}{PREFIX[e]}{unit}"


def money(x):
    return f"£{x:,.2f}"


def ang(deg):
    return f"{_sig(deg, 4)}°"


def polar(z, unit="", sig=4):
    """Complex number in polar form: 12.5∠36.87° Ω"""
    mag = abs(z)
    a = math.degrees(cmath.phase(z)) if mag > 1e-12 else 0.0
    u = f"{NBSP}{unit}" if unit else ""
    return f"{_sig(mag, sig)}{u}∠{_sig(a, sig)}°" if unit == "" else f"{_sig(mag, sig)}∠{_sig(a, sig)}°{u}"


def rect(z, unit="", sig=4):
    re, im = z.real, z.imag
    sgn = "+" if im >= 0 else MINUS
    body = f"{_sig(re, sig)} {sgn} j{_sig(abs(im), sig)}"
    if unit:
        return f"({body}){NBSP}{unit}"
    return body


def var(name):
    """'V_1' -> <i>V</i><sub>1</sub>; 'R_Th' -> <i>R</i><sub>Th</sub>."""
    if "_" in name:
        a, b = name.split("_", 1)
        return f"<i>{a}</i><sub>{b}</sub>"
    return f"<i>{name}</i>"


def par(*rs):
    return 1.0 / sum(1.0 / r for r in rs)


# --------------------------------------------------------------------------
# Problem record
# --------------------------------------------------------------------------
class Problem:
    def __init__(self, text, steps, answer, level=1, fig=None, topic=""):
        self.text = text
        self.steps = steps
        self.answer = answer
        self.level = level
        self.fig = fig
        self.topic = topic
        self.number = None


def rng(seed):
    return random.Random(seed)


# --------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------
def save(d, name):
    """Save a schemdraw Drawing as SVG (print) and PNG (ebook)."""
    svg = os.path.join(FIGDIR, name + ".svg")
    png = os.path.join(FIGDIR, name + ".png")
    d.save(svg)
    d.save(png, dpi=170)
    plt.close("all")
    return name


def tex_name(n):
    if "_" in n:
        a, b = n.split("_", 1)
        return f"${a}_{{\\mathrm{{{b}}}}}$" if len(b) > 1 and b.isalpha() else f"${a}_{{{b}}}$"
    return f"${n}$"


def lab(name=None, value=None):
    parts = []
    if name:
        parts.append(tex_name(name))
    if value:
        parts.append(value.replace(NBSP, " ").replace(MINUS, "−"))
    return "\n".join(parts)


from schemdraw.elements.sources import Source as _Src
from schemdraw.segments import SegmentText as _ST


class MeterG(_Src):
    """Galvanometer: circle with G."""
    def __init__(self, **kw):
        super().__init__(**kw)
        self.segments.append(_ST((.5, 0), "G"))


_MAKE = {
    "G": lambda: MeterG(),
    "R": lambda: elm.Resistor(),
    "Z": lambda: elm.ResistorIEC(),
    "C": lambda: elm.Capacitor(),
    "L": lambda: elm.Inductor2(loops=3),
    "V": lambda: elm.SourceV(),
    "Vac": lambda: elm.SourceSin(),
    "I": lambda: elm.SourceI(),
    "DV": lambda: elm.SourceControlledV(),
    "DI": lambda: elm.SourceControlledI(),
    "W": lambda: elm.Line(),
    "SWo": lambda: elm.Switch(action="open"),
    "SWc": lambda: elm.Switch(action="close"),
    "Lamp": lambda: elm.Lamp(),
    "A": lambda: elm.MeterA(),
    "Vm": lambda: elm.MeterV(),
}


def E(kind, name=None, value=None, rev=False, node=None, cur=None):
    """Element spec for ladder(): kind, label name, value text, reversed?, node label, current label."""
    return dict(kind=kind, name=name, value=value, rev=rev, node=node, cur=cur)


def _place(d, spec, direction, length=None, at=None, vertical=False):
    e = _MAKE[spec["kind"]]()
    if at is not None:
        e = e.at(at)
    e = getattr(e, direction)()
    if length:
        e = e.length(length)
    if spec.get("rev"):
        e = e.reverse()
    text = lab(spec.get("name"), spec.get("value"))
    if spec["kind"] in ("SWo", "SWc") and not text:
        text = "$t = 0$"
    if text and spec["kind"] != "W":
        if vertical:
            e = e.label(text, loc="bottom", ofst=0.25)
        else:
            e = e.label(text, ofst=0.18)
    d += e
    if spec.get("cur"):
        d += elm.CurrentLabelInline(direction="in" if not spec.get("curback") else "out").at(e).label(
            tex_name(spec["cur"]), fontsize=12)
    return e


def ladder(name, source, items, H=3.0, gap=2.6, terminals=("a", "b")):
    """Draw a ladder network.

    source: spec drawn vertically at the left (+ / arrow upward unless rev),
            or None for open input terminals.
    items:  list of ('S', spec) series elements along the top rail and
            ('P', spec) shunt elements from top rail to bottom rail.
    If the list ends with a series element, output terminals are drawn.
    """
    with schemdraw.Drawing(show=False) as d:
        d.config(unit=3)
        x = 0.0
        if source is None:
            d += elm.Dot(open=True).at((0, H)).label(terminals[0], loc="left")
            d += elm.Dot(open=True).at((0, 0)).label(terminals[1], loc="left")
        else:
            _place(d, source, "up", length=H, at=(0, 0), vertical=False)
        prev = "src"
        for k, (kind, spec) in enumerate(items):
            if kind == "S":
                _place(d, spec, "right", at=(x, H))
                x += 3.0
                prev = "S"
                if spec.get("node"):
                    d += elm.Dot().at((x, H)).label(spec["node"], loc="top")
            else:
                if prev == "P" or (prev == "src"):
                    d += elm.Line().at((x, H)).right().length(gap)
                    x += gap
                more = any(t == "P" or t == "S" for t, _ in items[k + 1:])
                if more:
                    d += elm.Dot().at((x, H))
                    d += elm.Dot().at((x, 0))
                sp = dict(spec)
                sp["rev"] = not spec.get("rev")  # drawn downward, so + at top by default
                _place(d, sp, "down", length=H, at=(x, H), vertical=True)
                if spec.get("node"):
                    d += elm.Label().at((x, H + 0.35)).label(spec["node"])
                prev = "P"
        if prev == "S":
            d += elm.Line().at((x, H)).right().length(0.8)
            d += elm.Dot(open=True).at((x + 0.8, H)).label(terminals[0], loc="right")
            d += elm.Dot(open=True).at((x + 0.8, 0)).label(terminals[1], loc="right")
            x += 0.8
        d += elm.Line().at((0, 0)).to((x, 0))
        return save(d, name)


def bridge(name, source, r1, r2, r3, r4, mid=None, terminals=("a", "b")):
    """Wheatstone bridge: source on the left; top node T, bottom node B,
    left arm junction a (R1 top-left, R3 bottom-left), right junction b
    (R2 top-right, R4 bottom-right).  mid: spec between a and b, or None
    for open terminals a, b."""
    with schemdraw.Drawing(show=False) as d:
        d.config(unit=3)
        T = (4.0, 6.0)
        B = (4.0, 0.0)
        A = (0.6, 3.0)
        Bn = (7.4, 3.0)
        _place(d, source, "up", length=6, at=(-2.5, 0))
        d += elm.Line().at((-2.5, 6)).to(T)
        d += elm.Line().at((-2.5, 0)).to(B)
        for spec, p0, p1, loc in ((r1, T, A, "top"), (r2, T, Bn, "top"), (r3, A, B, "bottom"), (r4, Bn, B, "bottom")):
            e = _MAKE[spec["kind"]]().endpoints(p0, p1)
            d += e.label(lab(spec.get("name"), spec.get("value")), loc=loc, ofst=0.15)
        d += elm.Dot().at(T)
        d += elm.Dot().at(B)
        if mid is None:
            d += elm.Dot(open=True).at(A).label(terminals[0], loc="left")
            d += elm.Dot(open=True).at(Bn).label(terminals[1], loc="right")
        else:
            d += elm.Dot().at(A).label("a", loc="left")
            d += elm.Dot().at(Bn).label("b", loc="right")
            e = _MAKE[mid["kind"]]().endpoints(A, Bn)
            d += e.label(lab(mid.get("name"), mid.get("value")), loc="top", ofst=0.15)
        return save(d, name)


def star_delta(name, kind, labels, star=True, supply=None):
    """Three-phase or Δ/Y network sketch.  labels: three label strings."""
    with schemdraw.Drawing(show=False) as d:
        d.config(unit=2.5)
        mk = _MAKE[kind]
        if star:
            c = (0, 0)
            pts = [(0, 3.2), (-2.8, -1.6), (2.8, -1.6)]
            names = ["a", "b", "c"] if supply is None else supply
            for p, l, n in zip(pts, labels, names):
                d += mk().endpoints(p, c).label(l, ofst=0.2)
                d += elm.Dot(open=True).at(p).label(n, loc="top")
            d += elm.Dot().at(c).label("n", loc="bottom", ofst=0.3)
        else:
            pts = [(0, 3.2), (-2.9, -1.8), (2.9, -1.8)]
            names = ["a", "b", "c"] if supply is None else supply
            for (p, q), l in zip(((pts[0], pts[1]), (pts[1], pts[2]), (pts[2], pts[0])), labels):
                d += mk().endpoints(p, q).label(l, ofst=0.2)
            for p, n in zip(pts, names):
                d += elm.Dot().at(p).label(n, loc="top")
        return save(d, name)


def opamp(name, kind, labels):
    """Small op-amp sketches used only in text figures (kept for completeness)."""
    raise NotImplementedError
