import sys; sys.path.insert(0, '.')
from goju import *
from goju import _poly
from matplotlib.patches import Ellipse as E

def tool_panel(fn, title):
    def p(ax):
        fn(ax)
        label(ax, (0, -0.03), title, size=6.3)
    return p
def tan(ax):
    _poly(ax, [(-0.3, 0.33), (0.3, 0.33), (0.3, 0.35), (-0.3, 0.35)])
    for x in (-0.3, 0.3):
        ax.add_patch(E((x, 0.34), 0.09, 0.2, fc="white", ec="black", lw=0.9, zorder=7))
def jari(ax):
    _poly(ax, [(-0.25, 0.15), (0.25, 0.15), (0.25, 0.35), (-0.25, 0.35)])
    _poly(ax, [(-0.25, 0.35), (0.25, 0.35), (0.32, 0.42), (-0.18, 0.42)])
    import random
    random.seed(3)
    for _ in range(40):
        ax.add_patch(Circle((random.uniform(-0.2, 0.28), random.uniform(0.36, 0.41)), 0.008, fc="black", zorder=8))
def geta(ax):
    for dx in (-0.12, 0.12):
        _poly(ax, [(dx - 0.07, 0.3), (dx + 0.07, 0.3), (dx + 0.06, 0.55), (dx - 0.06, 0.55)])
        _poly(ax, [(dx - 0.05, 0.22), (dx - 0.03, 0.22), (dx - 0.03, 0.3), (dx - 0.05, 0.3)])
        _poly(ax, [(dx + 0.03, 0.22), (dx + 0.05, 0.22), (dx + 0.05, 0.3), (dx + 0.03, 0.3)])
        ax.plot([dx - 0.05, dx, dx + 0.05], [0.42, 0.48, 0.42], c="black", lw=0.8, zorder=8)

plate("fig6_1", [
    tool_panel(lambda ax: chi_ishi(ax, (-0.25, 0.25), 25, L=0.42), "chi ishi"),
    tool_panel(lambda ax: (jar(ax, (-0.12, 0.5), s=1.6), jar(ax, (0.14, 0.5), s=1.6)), "nigiri game"),
    tool_panel(lambda ax: (ishi_sashi(ax, (-0.12, 0.5), s=1.6), ishi_sashi(ax, (0.14, 0.5), s=1.6)), "ishi sashi"),
    tool_panel(lambda ax: kongoken(ax, (0, 0.35), 0.62, 0.36), "kongoken"),
    tool_panel(tan, "tan"),
    tool_panel(lambda ax: makiwara(ax, 0.0, top=0.65), "makiwara"),
    tool_panel(jari, "jari bako"),
    tool_panel(geta, "tetsu geta"),
], cols=4, height=0.8)

ci = lambda key, ang, L=0.2: (lambda ax, J: chi_ishi(ax, J[key], ang, L))
up_front = ((0.03, -0.02), (-0.06, 0.0), "fist", 90)
plate("fig6_2", [
    with_tools(F("shiko", "hikite", ((0.02, -0.02), (-0.05, -0.02), "fist", 90)), [ci("handR", 90)]),
    with_tools(F("shiko", "hikite", ((0.02, -0.02), (-0.05, -0.02), "fist", 90)), [ci("handR", -80)]),
    with_tools(F("shiko", "hikite", "hira_side"), [ci("handR", 90)]),
    with_tools(F("shiko", "hikite", "hira_side"), [ci("handR", -90)]),
    with_tools(S("sanchin", "hikite", ((0.15, -0.16), -1, "fist", 90)), [ci("handF", -90, 0.14)]),
    with_tools(S("sanchin", "hikite", "chudan_uke"), [ci("handF", -90, 0.14)]),
    with_tools(S("sanchin", "hikite", "chudan_tsuki"), [ci("handF", -90, 0.14)]),
    with_tools(F("shiko", "hikite", ((0.05, 0.08), (0.10, 0.14), "fist", 90)), [ci("handR", 150)]),
], cols=4)

jr = lambda key, s=1.0: (lambda ax, J: jar(ax, J[key], s=s))
plate("fig6_3", [
    lambda ax: (jar(ax, (0.02, 0.62), s=2.2), _hand(ax)) if False else (jar(ax, (0.02, 0.6), s=2.6), label(ax, (0, -0.03), "grip on the rim", size=6.3)),
    with_tools(F("sanchin", "down", "down"), [jr("handL"), jr("handR")]),
    with_tools(S("sanchin", "down", "down"), [jr("handF")]),
    with_tools(S("sanchin", "down", "down", x=0.08), [jr("handF")]),
    with_tools(F("shiko", "down", "down"), [jr("handL"), jr("handR")]),
    with_tools(S("sanchin", ((0.30, -0.02), -1, "fist", 0), ((0.30, -0.02), -1, "fist", 0)), [jr("handF")]),
    with_tools(F("sanchin", "hira_side", "hira_side"), [jr("handL"), jr("handR")]),
    with_tools(F("sanchin", ((0.03, -0.12), (0.03, -0.27), "open", -90), ((0.03, -0.12), (0.03, -0.27), "open", -90), lean=0.0, drop=-0.01), [jr("handL"), jr("handR")]),
], cols=4)

ish = lambda key: (lambda ax, J: ishi_sashi(ax, J[key]))
def kg(dx, dy, w=0.3, h=0.16, ang=0):
    return lambda ax, J: kongoken(ax, (J["sh"][0] + dx, J["sh"][1] + dy), w, h, ang=ang) if "sh" in J else kongoken(ax, ((J["shL"][0] + J["shR"][0]) / 2 + dx, J["shL"][1] + dy), w, h, ang=ang)
plate("fig6_4", [
    with_tools(F("sanchin", "hikite", "hikite"), [ish("handL"), ish("handR")]),
    with_tools(S("sanchin", "hikite", "chudan_tsuki"), [ish("handF")]),
    with_tools(S("sanchin", "hikite", "age_uke"), [ish("handF")]),
    with_tools(F("shiko", "hikite", "chudan_tsuki"), [ish("handL"), ish("handR")]),
    with_tools(F("shiko", ((0.03, -0.17), (0.04, -0.31), "fist", -90), ((0.03, -0.17), (0.04, -0.31), "fist", -90), drop=0.04), [kg(0, -0.32, 0.36, 0.1)]),
    with_tools(F("heiko", ((0.08, -0.14), (0.14, -0.06), "fist", 90), ((0.08, -0.14), (0.14, -0.06), "fist", 90)), [kg(0, -0.06, 0.4, 0.14)]),
    with_tools(F("heiko", ((0.10, 0.10), (0.10, 0.20), "fist", 90), ((0.10, 0.10), (0.10, 0.20), "fist", 90)), [kg(0, 0.20, 0.34, 0.1)]),
    with_tools(Figure("sanchin", "side", ((0.22, -0.06), -1, "fist", 0), ((0.22, -0.06), -1, "fist", 0), x=-0.28, facing=1), [lambda ax, J: kongoken(ax, (J["handF"][0] + 0.06, J["handF"][1]), 0.12, 0.3)]),
], cols=4, panel_w=1.1)

def mk(fig, flex=0.0, x=0.13):
    def fn(ax):
        makiwara(ax, x, top=0.76, flex=flex)
        fig.draw(ax)
        floor(ax, -0.5, 0.5)
    return fn
plate("fig6_5", [
    mk(S("sanchin", "hikite", ((0.29, -0.06), -1, "fist", 0), x=-0.24)),
    mk(S("sanchin", "hikite", "chudan_tsuki", x=-0.22)),
    mk(S("sanchin", "hikite", "chudan_tsuki", x=-0.19), flex=0.04),
    mk(S("sanchin", "hikite", ((0.27, -0.06), -1, "fist", 0), x=-0.22), flex=0.02),
    mk(S("sanchin", "hikite", "shotei", x=-0.22)),
    mk(S("sanchin", "hikite", ((0.26, -0.03), -1, "fist", -70), x=-0.2)),
    mk(S("zenkutsu", "hikite", ((0.13, -0.04), +1, "fist", 180), x=0.0)),
    mk(S("sanchin", "hikite", ((0.31, -0.06), -1, "fist", -35), x=-0.22)),
], cols=4)

g1 = ((0.20, -0.20), -1, "fist", -60)
plate("fig6_6", [
    P(D("sanchin", "hikite", "sanchin"), A("sanchin", "hikite", "sanchin")),
    P(D("sanchin", "hikite", ((0.12, 0.05), -1, "fist", 90)), A("sanchin", "hikite", ((0.12, 0.05), -1, "fist", 90))),
    P(D("sanchin", "hikite", ((0.25, -0.18), -1, "fist", -50)), A("sanchin", "hikite", ((0.25, -0.18), -1, "fist", -50))),
    P(D("sanchin", "hikite", ((0.10, -0.22), -1, "fist", -90)), A("sanchin", "hikite", ((0.10, -0.22), -1, "fist", -90))),
    P(D("sanchin", "hikite", ((0.24, 0.0), -1, "fist", 80)), A("sanchin", "hikite", ((0.24, 0.0), -1, "fist", 80))),
    P(D("sanchin", "hikite", ((0.08, 0.06), +1, "fist", 160)), A("sanchin", "hikite", ((0.08, 0.06), +1, "fist", 160))),
    P(D("sanchin", "hikite", ((0.25, -0.06), -1, "fist", 90)), A("sanchin", "hikite", ((0.25, -0.06), -1, "fist", 90))),
    P(D("sanchin", "sanchin", "hikite"), A("sanchin", "sanchin", "hikite")),
], cols=4, panel_w=1.15)

def towel(fig, twist=False):
    def fn(ax):
        J = fig.draw(ax)
        floor(ax, -0.48, 0.48)
        a, b = J["handL"], J["handR"]
        ax.plot([a[0], b[0]], [a[1], b[1]], c="black", lw=3.2, zorder=4.5, solid_capstyle="round")
        ax.plot([a[0], b[0]], [a[1], b[1]], c="white", lw=1.8, zorder=4.6, solid_capstyle="round")
        if twist:
            for k in range(1, 6):
                t = k / 6
                x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
                ax.plot([x - 0.01, x + 0.01], [y - 0.012, y + 0.012], c="black", lw=0.5, zorder=4.7)
    return fn
plate("fig6_7", [
    P(S("sanchin", "sanchin", "sanchin")),
    P(D("sanchin", "shotei", "shotei"), A("sanchin", "shotei", "shotei")),
    P(D("sanchin", "sanchin", "sanchin"), A("sanchin", ((0.25, -0.02), -1, "open", 90), ((0.25, -0.02), -1, "open", 90))),
    P(D("sanchin", "chudan_tsuki", "chudan_tsuki", lean=-0.02), A("sanchin", ((0.28, -0.06), -1, "fist", 0), ((0.28, -0.06), -1, "fist", 0), lean=-0.03)),
    towel(F("shiko", "hira_side", "hira_side")),
    towel(F("shiko", ((0.03, -0.12), (0.05, -0.08), "fist", 0), ((0.03, -0.12), (-0.08, -0.08), "fist", 180)), twist=True),
    P(S("sanchin", "hikite", ((0.08, -0.1), -1, "fist", 90))), P(S("sanchin", "hikite", "chudan_uke")),
], cols=4, panel_w=1.15)
print(COUNT)
