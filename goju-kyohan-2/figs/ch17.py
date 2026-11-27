import sys; sys.path.insert(0, '.')
from goju import *

w = ((0.22, -0.06), -1, "open", 70)
plate("fig17_1", [
    P(D("sanchin", "guard", w), A("sanchin", "guard", w)),
    P(D("sanchin", "guard", ((0.3, 0.0), -1, "palm", 90)), A("sanchin", "guard", ((0.14, -0.12), -1, "open", 40))),
    P(D("sanchin", "guard", ((0.18, -0.06), -1, "fist", 0)), A("sanchin", "guard", ((0.24, -0.06), -1, "claw", 180))),
    P(D("shiko", ((0.08, -0.06), +1, "open", 0), ((0.13, 0.0), +1, "fist", 90)), A("sanchin", "guard", ((0.3, -0.08), -1, "open", 120))),
    P(D("shiko", ((0.22, -0.06), -1, "fist", 90), ((0.06, -0.14), +1, "claw", 0), drop=0.02), A("zenkutsu", "guard", ((0.34, -0.16), -1, "open", -20), x=0.28, lean=0.08)),
    P(D("sanchin", "guard", ((0.24, -0.1), -1, "open", 0)), A("kokutsu", "guard", "guard", x=0.36)),
    P(D("sanchin", "guard", "guard"), A("zenkutsu", ((0.26, -0.06), -1, "claw", 180), ((0.3, -0.2), -1, "claw", 180), x=0.26, lean=0.1)),
    P(D("shiko", ((0.2, -0.06), -1, "claw", 0), ((0.16, -0.16), -1, "palm", 90), drop=0.03), A("zenkutsu", "guard", "guard", x=0.3, lean=-0.04)),
], cols=4, panel_w=1.2)

plate("fig17_2", [
    hand_panel("claw", 0, 0, "grip: outward turn"),
    P(D("sanchin", "guard", ((0.22, -0.06), -1, "claw", 60)), A("sanchin", "guard", ((0.2, -0.04), -1, "open", 150))),
    P(D("sanchin", "guard", ((0.22, -0.12), -1, "claw", 90)), A("kokutsu", "guard", ((0.22, -0.14), -1, "open", 200), lean=-0.06, x=0.3)),
    P(D("neko", "guard", ((0.22, -0.22), -1, "claw", 90), x=-0.3), A("shiko", "guard", ((0.2, -0.22), -1, "open", 220), lean=-0.1, x=0.26, drop=0.12)),
    hand_panel("hook", 60, 0, "grip: inward bend"),
    P(D("sanchin", "guard", ((0.2, -0.04), -1, "hook", -60)), A("sanchin", "guard", ((0.2, -0.06), -1, "hook", -90), x=0.26)),
    P(D("sanchin", ((0.22, -0.08), -1, "palm", -90), ((0.18, -0.12), -1, "hook", -60)), A("zenkutsu", "guard", ((0.24, -0.14), -1, "hook", -90), x=0.26, lean=0.08)),
    P(D("kokutsu", ((0.2, -0.16), -1, "palm", -90), ((0.16, -0.2), -1, "hook", -60), x=-0.3), A("zenkutsu", "guard", ((0.24, -0.22), -1, "hook", -90), x=0.2, lean=0.18, drop=0.04)),
], cols=4, panel_w=1.2)

plate("fig17_3", [
    P(D("sanchin", "guard", ((0.2, -0.04), -1, "claw", 0)), A("zenkutsu", "hikite", ((0.3, -0.04), -1, "open", 0), x=0.3)),
    P(D("sanchin", "guard", ((0.12, -0.12), +1, "claw", 0)), A("zenkutsu", "hikite", ((0.32, -0.1), -1, "open", 0), x=0.28, lean=0.04)),
    P(D("shiko", ((0.2, -0.06), -1, "fist", 90), ((0.08, -0.14), +1, "claw", 0)), A("zenkutsu", "hikite", ((0.34, -0.14), -1, "open", -20), x=0.28, lean=0.06)),
    P(D("shiko", ((0.22, -0.16), -1, "fist", 90), ((0.06, -0.2), +1, "claw", 0), drop=0.05), A("zenkutsu", "hikite", ((0.32, -0.26), -1, "open", -40), x=0.26, lean=0.2, drop=0.06)),
    P(Figure("sanchin", "side", ((0.18, -0.12), -1, "claw", 0), ((0.22, -0.02), -1, "claw", 0), x=-0.2, facing=1), Figure("heiko", "side", "guard", ((-0.04, -0.12), +1, "open", 0), x=0.12, facing=1, partner=True)),
    P(Figure("sanchin", "side", ((0.18, -0.06), -1, "claw", 0), ((0.24, 0.02), -1, "claw", 0), x=-0.2, facing=1), Figure("heiko", "side", "guard", ((-0.1, -0.04), +1, "open", 0), x=0.12, facing=1, partner=True, lean=0.05)),
    P(D("sanchin", ((0.2, -0.02), -1, "claw", 0), ((0.18, -0.12), -1, "claw", 0)), A("sanchin", "guard", ((0.12, -0.04), -1, "fist", 90), x=0.27)),
    P(D("sanchin", ((0.2, 0.0), -1, "claw", 30), ((0.16, -0.14), -1, "claw", 0), lean=-0.02), A("sanchin", "guard", ((0.1, -0.02), -1, "fist", 120), x=0.27, lean=-0.04)),
], cols=4, panel_w=1.2)

plate("fig17_4", [
    P(D("sanchin", "guard", ((0.2, -0.06), -1, "claw", 0)), A("zenkutsu", "hikite", ((0.3, -0.08), -1, "open", 0), x=0.3)),
    P(D("shiko", "guard", ((0.06, -0.2), +1, "claw", 0), drop=0.04), A("zenkutsu", "hikite", ((0.32, -0.24), -1, "open", -40), x=0.24, lean=0.2, drop=0.04)),
    P(D("kosa", "guard", ((0.22, -0.02), -1, "palm", 90), x=-0.12), A("sanchin", "guard", "hikite", x=0.24)),
    P(D("zenkutsu", "guard", ((0.24, 0.04), -1, "palm", 90), x=-0.06), A("sagi", "guard", "guard", x=0.28, lean=-0.14, kick="mae")),
    P(D("heiko", ((0.22, 0.06), -1, "claw", 60), ((0.22, -0.06), -1, "claw", 0)), A("sanchin", "hikite", ((0.26, -0.02), -1, "claw", 180), x=0.26)),
    P(D("shiko", ((0.18, -0.02), -1, "claw", 0), ((0.14, -0.2), -1, "claw", -60), drop=0.04), A("zenkutsu", "guard", ((0.2, -0.2), -1, "open", -60), x=0.2, lean=0.2)),
    P(D("shiko", ((0.24, 0.02), -1, "open", 60), ((0.26, -0.28), -1, "open", -60), drop=0.04, x=-0.18), A("zenkutsu", "guard", ((0.22, -0.04), -1, "claw", 180), x=0.24, lean=0.05)),
    P(D("heiko", ((0.24, 0.06), -1, "open", 60), ((0.26, -0.2), -1, "open", -20), x=-0.16), A("sagi", "guard", "guard", x=0.18, lean=-0.08, kick="knee")),
], cols=4, panel_w=1.2)

plate("fig17_5", [
    P(D("heiko", "hip", ((0.12, -0.18), -1, "fist", 0)), A("sanchin", "hikite", ((0.24, -0.19), -1, "claw", 180))),
    P(D("shiko", ((0.1, -0.06), +1, "open", 0), ((0.22, 0.04), +1, "fist", 180), drop=0.02), A("sanchin", "hikite", "guard", x=0.3, lean=-0.05)),
    P(D("heiko", "hip", "hip"), A("sanchin", ((0.24, -0.02), -1, "claw", 180), ((0.24, -0.02), -1, "claw", 180), x=0.26)),
    P(D("shiko", ((0.16, 0.06), -1, "open", 60), ((0.14, 0.08), -1, "open", 60), drop=0.03), A("sanchin", ((0.2, 0.06), -1, "open", 120), ((0.24, -0.1), -1, "open", 180), x=0.27)),
    P(Figure("sanchin", "side", ((0.24, -0.06), -1, "claw", 0), ((0.24, -0.06), -1, "claw", 0), x=-0.18, facing=1, partner=True), S("heiko", "guard", "guard", x=0.1)),
    P(Figure("sanchin", "side", ((0.2, -0.1), -1, "open", 0), "guard", x=-0.24, facing=1, partner=True, lean=0.05), S("shiko", "guard", "empi_rear", x=0.1)),
    P(D("zenkutsu", "guard", ((0.34, -0.16), -1, "open", -20), x=-0.26, lean=0.08), A("shiko", ((0.22, -0.08), -1, "fist", 90), ((0.06, -0.16), +1, "claw", 0), x=0.28)),
    P(D("sanchin", "guard", ((0.14, -0.04), -1, "fist", 90), x=-0.14), A("sanchin", ((0.16, -0.04), -1, "fist", 90), ((0.06, -0.14), +1, "claw", 0), x=0.26, lean=-0.04)),
], cols=4, panel_w=1.2)
print(COUNT)
