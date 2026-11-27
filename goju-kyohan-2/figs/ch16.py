import sys; sys.path.insert(0, '.')
from goju import *

def top(ax, me, opp, title=None, arrows_=None):
    # simple top view: defender as circle with nose line, partner as hollow square
    for (x, y, a), kind in ((me, "d"), (opp, "p")):
        if kind == "d":
            ax.add_patch(Circle((x, y + 0.35), 0.06, fc="black", ec="black", zorder=5))
        else:
            ax.add_patch(Circle((x, y + 0.35), 0.06, fc="white", ec="black", lw=1.0, zorder=5))
        r = math.radians(a)
        arrow(ax, (x, y + 0.35), (x + 0.14 * math.cos(r), y + 0.35 + 0.14 * math.sin(r)), lw=1.0)
    for a_, b_ in (arrows_ or []):
        arrow(ax, (a_[0], a_[1] + 0.35), (b_[0], b_[1] + 0.35), lw=0.7, ls=(0, (2, 2)))
    if title:
        label(ax, (0, -0.03), title, size=6.3)

plate("fig16_1", [
    lambda ax: top(ax, (0, -0.1, 0), (0.0, 0.25, -90), "kata: turn right", [((0.0, -0.1), (0.0, -0.1))]) if False else (embusen(ax, [(0, 0.15), (0, 0.4), (0.25, 0.4)], s=1.0), label(ax, (0, -0.03), "kata: turn right", size=6.3)),
    lambda ax: (top(ax, (0, -0.05, 0), (0.3, -0.05, 180), "misreading"), ax.add_patch(Circle((0, 0.6), 0.06, fc="white", ec="black", lw=1.0, ls=(0, (2, 2))))),
    lambda ax: top(ax, (-0.15, 0.0, 30), (0.1, 0.2, -110), "same opponent", [((0.0, -0.1), (-0.15, 0.0))]),
    P(D("sanchin", "guard", "guard"), A("zenkutsu", "hikite", ((0.3, -0.02), -1, "fist", 0), x=0.3)),
    P(D("heiko", "guard", "guard", x=-0.3), A("zenkutsu", "hikite", ((0.3, -0.02), -1, "fist", 0), x=0.3)),
    P(D("shiko", "guard", "guard", x=-0.28), A("zenkutsu", "hikite", ((0.3, -0.04), -1, "fist", 0), x=0.3)),
    P(D("shiko", ((0.2, -0.02), -1, "claw", 0), "guard", x=-0.26), A("zenkutsu", "hikite", ((0.32, -0.08), -1, "fist", 0), x=0.28, lean=0.05)),
    P(D("shiko", "hikite", ((0.22, -0.06), -1, "fist", 90), x=-0.24, drop=0.02), A("zenkutsu", "hikite", ((0.32, -0.16), -1, "fist", -20), x=0.28, lean=0.1)),
], cols=4, panel_w=1.2)

plate("fig16_2", [
    P(S("sanchin", "hikite", "chudan_tsuki")),
    P(D("sanchin", "hikite", ((0.27, 0.0), -1, "fist", 0)), A("zenkutsu", "hikite", ((0.3, -0.18), -1, "open", -40), x=0.27, lean=0.1)),
    P(S("sanchin", ((0.12, -0.06), -1, "open", 90), "chudan_tsuki")),
    P(D("sanchin", ((0.18, -0.08), -1, "open", 90), ((0.26, 0.0), -1, "fist", 0)), A("sanchin", ((0.08, -0.08), -1, "fist", 0), "hikite", x=0.28)),
    P(S("sanchin", ((0.0, 0.04), +1, "fist", 90), "chudan_tsuki")),
    P(D("sanchin", ((0.1, 0.02), +1, "claw", 90), ((0.24, -0.04), -1, "fist", 0)), A("zenkutsu", "guard", "hip", x=0.24, lean=0.1)),
    P(S("sanchin", "hikite", "hikite")),
    P(D("sanchin", ((0.04, -0.16), +1, "claw", 0), ((0.06, -0.16), +1, "claw", 0)), A("zenkutsu", "hikite", ((0.32, -0.16), -1, "open", -20), x=0.24, lean=0.12)),
], cols=4, panel_w=1.2)

plate("fig16_3", [
    P(S("sanchin", "hikite", "gedan_barai")),
    P(D("sanchin", "hikite", "gedan_barai"), A("sagi", "guard", "guard", x=0.32, kick="mae")),
    P(D("sanchin", "hikite", ((0.24, -0.26), -1, "fist", -70)), A("sanchin", "guard", "guard", x=0.3)),
    P(D("sanchin", "hikite", ((0.24, -0.2), -1, "fist", -50)), A("sanchin", "hikite", ((0.24, -0.18), -1, "claw", 180), x=0.28)),
    P(D("shiko", "hikite", ((0.16, -0.24), -1, "claw", -80)), A("zenkutsu", "hikite", ((0.3, -0.22), -1, "open", -40), x=0.26, lean=0.1)),
    P(D("sanchin", ((0.2, -0.04), -1, "claw", 0), "guard"), A("zenkutsu", "hikite", ((0.32, -0.04), -1, "open", 0), x=0.3)),
    P(D("shiko", ((0.08, -0.14), +1, "claw", 0), ((0.22, -0.12), -1, "fist", -60)), A("zenkutsu", "hikite", ((0.34, -0.14), -1, "open", -20), x=0.28, lean=0.06)),
    P(D("shiko", ((0.06, -0.18), +1, "claw", 0), ((0.2, -0.2), -1, "fist", -70), drop=0.04), A("zenkutsu", "hikite", ((0.3, -0.26), -1, "open", -40), x=0.24, lean=0.2, drop=0.05)),
], cols=4, panel_w=1.2)

cover = ((0.04, -0.24), +1, "fist", 0)
plate("fig16_4", [
    P(F("shiko", ((-0.02, -0.12), (-0.05, -0.08), "open", 180), ((0.13, -0.02), (-0.06, -0.06), "fist", 180))),
    P(D("heiko", "hip", ((0.12, -0.18), -1, "fist", 0)), A("sanchin", "hikite", ((0.24, -0.19), -1, "claw", 180))),
    P(D("shiko", ((0.1, -0.06), +1, "open", 0), ((0.22, 0.04), +1, "fist", 180), drop=0.02), A("sanchin", "hikite", "guard", x=0.3, lean=-0.05)),
    P(D("heiko", "hip", ((0.12, -0.18), -1, "fist", 0)), A("sanchin", ((0.24, -0.19), -1, "claw", 180), ((0.24, -0.19), -1, "claw", 180))),
    P(D("shiko", ((0.08, -0.08), +1, "open", 0), ((0.13, 0.0), +1, "fist", 90)), A("sanchin", ((0.28, -0.1), -1, "open", 120), "guard", x=0.3)),
    P(D("heiko", "hip", "hip"), A("sanchin", "hikite", ((0.26, -0.02), -1, "claw", 180), x=0.26)),
    P(D("musubi", cover, cover), A("zenkutsu", "hikite", ((0.32, -0.12), -1, "claw", 180), x=0.24, lean=0.06)),
    P(D("shiko", ((0.08, -0.06), +1, "open", 0), ((0.2, 0.04), +1, "fist", 180), drop=0.02), A("zenkutsu", "hikite", ((0.3, -0.12), -1, "open", 120), x=0.24, lean=0.06)),
], cols=4, panel_w=1.2)

plate("fig16_5", [
    P(F("shiko", ((-0.05, -0.06), (-0.17, -0.04), "open", 180), ((-0.1, -0.02), (0.0, -0.01), "fist", 180), drop=0.02)),
    P(D("shiko", ((0.26, 0.06), -1, "open", 0), ((0.06, 0.06), +1, "fist", 180), x=-0.3), A("zenkutsu", "guard", "hip", x=0.3, lean=0.1)),
    P(D("shiko", ((0.24, -0.04), -1, "open", 0), ((0.14, -0.02), +1, "fist", 180)), A("zenkutsu", "hikite", ((0.3, -0.06), -1, "open", 0), x=0.28, lean=0.05)),
    P(D("shiko", ((0.08, -0.14), +1, "claw", 0), ((0.22, -0.08), -1, "fist", 90)), A("zenkutsu", "hikite", ((0.34, -0.14), -1, "open", -20), x=0.28, lean=0.06)),
    P(D("heiko", "hip", ((0.2, -0.04), -1, "claw", 0)), A("zenkutsu", "hikite", ((0.3, -0.04), -1, "open", 0), x=0.3)),
    P(D("shiko", ((0.16, 0.02), -1, "fist", 90), ((0.08, -0.12), +1, "claw", 0)), A("zenkutsu", "hikite", ((0.32, -0.1), -1, "open", 0), x=0.29, lean=0.03)),
    P(D("shiko", ((0.22, -0.08), -1, "fist", 90), ((0.06, -0.16), +1, "claw", 0), drop=0.03), A("zenkutsu", "hikite", ((0.34, -0.18), -1, "open", -20), x=0.28, lean=0.1)),
    P(D("shiko", ((0.22, -0.16), -1, "fist", 90), ((0.06, -0.2), +1, "claw", 0), drop=0.05), A("zenkutsu", "hikite", ((0.32, -0.26), -1, "open", -40), x=0.26, lean=0.2, drop=0.06)),
], cols=4, panel_w=1.2)
print(COUNT)
