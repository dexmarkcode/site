"""Schematics drawn for individual questions."""
import os
import figstyle  # noqa: F401
import schemdraw
import schemdraw.elements as elm
from qcore import eng

OUT = os.path.join(os.path.dirname(__file__), "..", "figures", "q")
os.makedirs(OUT, exist_ok=True)
_counter = [0]


def _path(tag):
    _counter[0] += 1
    return os.path.join(OUT, f"{tag}_{_counter[0]:03d}.png")


def _save(d, path):
    d.save(path, dpi=220)
    import matplotlib.pyplot as plt
    plt.close("all")
    return os.path.relpath(path, os.path.join(os.path.dirname(__file__), ".."))


def t_network(Vs, R1, R2, R3, load=None):
    path = _path("tnet")
    with schemdraw.Drawing(show=False) as d:
        d.config(unit=2.6)
        V = elm.SourceV().up().label(f"{Vs:g} V")
        elm.Resistor().right().label(f"R1 = {eng(R1,'Ω')}")
        elm.Dot()
        d.push()
        elm.Resistor().down().label(f"R2 = {eng(R2,'Ω')}", loc="bottom", ofst=0.15)
        elm.Dot()
        d.pop()
        elm.Resistor().right().label(f"R3 = {eng(R3,'Ω')}")
        a = elm.Dot(open=True).label("a", loc="right")
        if load:
            elm.Resistor().down().label(f"R_L = {eng(load,'Ω')}", loc="bottom", ofst=0.15)
        else:
            elm.Gap().down().label(["+", "$V_{ab}$", "−"])
        elm.Dot(open=True).label("b", loc="right")
        elm.Line().to(V.start)
    return _save(d, path)


def two_source(V1, V2, R1, R2, R3):
    path = _path("twosrc")
    with schemdraw.Drawing(show=False) as d:
        d.config(unit=2.6)
        S1 = elm.SourceV().up().label(f"$V_1$ = {V1:g} V")
        elm.Resistor().right().label(f"R1 = {eng(R1,'Ω')}")
        elm.Dot().label("x", loc="top")
        d.push()
        elm.Resistor().down().label(f"R2 = {eng(R2,'Ω')}", loc="bottom", ofst=0.15)
        elm.Dot()
        d.pop()
        elm.Line().right().length(1.2)
        elm.Resistor().right().label(f"R3 = {eng(R3,'Ω')}")
        elm.SourceV().down().reverse().label(f"$V_2$ = {V2:g} V", loc="bottom")
        elm.Line().to(S1.start)
    return _save(d, path)


def series_parallel(Vs, R1, R2, R3):
    path = _path("sp")
    with schemdraw.Drawing(show=False) as d:
        d.config(unit=2.6)
        S = elm.SourceV().up().label(f"{Vs:g} V")
        elm.Resistor().right().label(f"R1 = {eng(R1,'Ω')}")
        elm.Dot()
        d.push()
        elm.Resistor().down().label(f"R2 = {eng(R2,'Ω')}", loc="bottom", ofst=0.15)
        elm.Dot()
        d.pop()
        elm.Line().right()
        elm.Resistor().down().label(f"R3 = {eng(R3,'Ω')}", loc="bottom", ofst=0.15)
        elm.Line().to(S.start)
    return _save(d, path)
