import sys; sys.path.insert(0, '.')
from goju import *

big_embusen("fig8_1", [(0, -0.45), (0.25, -0.25), (-0.25, -0.05), (0.25, 0.15), (0.03, 0.2), (0.03, 0.5), (0.0, 0.25), (0.35, 0.25), (-0.35, 0.28), (-0.02, -0.4)],
            [("1", (0.32, -0.28)), ("2", (-0.32, -0.05)), ("3", (0.32, 0.18)), ("4", (0.1, 0.32)), ("5", (0.1, 0.5)),
             ("6", (0.42, 0.25)), ("7", (-0.42, 0.28)), ("8", (0.08, -0.4))])

cross_low = ((0.0, -0.15), (-0.08, -0.24), "open", 200)
plate("fig8_2", [
    P(F("shiko", cross_low, cross_low)),
    P(F("shiko", ((0.0, -0.14), (-0.07, -0.12), "open", 120), ((0.0, -0.14), (-0.07, -0.12), "open", 120))),
    P(F("shiko", ((0.0, -0.12), (-0.06, -0.02), "open", 100), ((0.0, -0.12), (-0.06, -0.02), "open", 100))),
    P(F("shiko", ((0.08, -0.12), (0.08, 0.0), "open", 90), ((0.08, -0.12), (0.08, 0.0), "open", 90))),
    P(F("shiko", "gedan_open", "hikite")),
    P(F("shiko", ((0.0, -0.14), (0.0, -0.15), "open", 180), ((-0.02, -0.13), (-0.08, -0.2), "nukite", 230))),
    P(F("shiko", ((0.02, -0.13), (-0.06, -0.16), "fist", 200), ((0.02, -0.13), (-0.06, -0.16), "fist", 200), drop=0.01)),
    P(F("shiko", "hikite", "hikite", drop=0.02)),
], cols=4)

plate("fig8_3", [
    P(F("shiko", ((-0.05, -0.06), (-0.16, -0.04), "open", 180), "hikite")),
    P(F("shiko", ((-0.05, -0.06), (-0.16, -0.04), "open", 180), ((0.12, -0.04), (0.20, 0.0), "fist", 90))),
    P(F("shiko", ((-0.05, -0.06), (-0.17, -0.04), "open", 180), ((-0.1, -0.02), (0.0, -0.01), "fist", 180), drop=0.02)),
    P(F("shiko", "hikite", "uraken", drop=0.02)),
    P(F("shiko", "hikite", "gedan_barai")),
    P(F("heiko", "hikite", "hikite", back=True)),
    P(F("shiko", ((-0.1, -0.02), (0.0, -0.01), "fist", 180), ((-0.05, -0.06), (-0.17, -0.04), "open", 180), drop=0.02)),
    P(F("shiko", "uraken", "hikite", drop=0.02)),
], cols=4)

plate("fig8_4", [
    P(S("sanchin", "hikite", ((0.28, -0.04), -1, "hook", 80))),
    P(S("seisan", "hikite", "grab_pull")),
    P(S("seisan", "chudan_tsuki", "grab_pull")),
    P(F("shiko", ((0.08, 0.05), (0.02, 0.16), "open", 120), ((-0.02, -0.17), (-0.10, -0.30), "open", 230), drop=0.02)),
    P(F("heiko", ((0.08, 0.05), (0.02, 0.16), "open", 120), ((-0.02, -0.15), (-0.08, -0.18), "open", 150))),
    P(F("heiko", ((0.12, -0.06), (0.2, -0.17), "fist", -60), ((0.1, 0.02), (0.08, 0.16), "open", 90), lean=0.03)),
    P(F("shiko", "hikite", "hikite", drop=0.03)),
    P(F("shiko", "hikite", "gedan_tsuki")),
], cols=4)

plate("fig8_5", [
    P(F("shiko", "gedan_tsuki", "gedan_tsuki")),
    P(F("shiko", "gedan_barai", "gedan_barai")),
    P(F("shiko", "hira_side", "hira_side", drop=-0.02)),
    P(F("shiko", "hikite", "hikite", drop=0.04)),
    P(S("neko", "guard", "chamber")),
    P(F("neko", mawashi_frames()[1][3], mawashi_frames()[0][3])),
    P(F("neko", mawashi_frames()[1][7], mawashi_frames()[0][7])),
    P(F("heiko", "yoi_open", "yoi_open")),
], cols=4)

lapel = ((0.26, -0.02), -1, "claw", 180)
plate("fig8_6", [
    P(D("heiko", "hip", "hip"), A("sanchin", lapel, lapel, x=0.26)),
    P(D("shiko", ((0.08, -0.15), -1, "open", 90), ((0.08, -0.15), -1, "open", 90), drop=0.02), A("sanchin", ((0.27, -0.06), -1, "claw", 180), ((0.27, -0.06), -1, "claw", 180), x=0.26, lean=0.03)),
    P(D("shiko", ((0.13, -0.04), -1, "open", 90), ((0.13, -0.04), -1, "open", 90), drop=0.02), A("sanchin", ((0.27, -0.08), -1, "claw", 180), ((0.27, -0.08), -1, "claw", 180), x=0.26, lean=0.04)),
    P(D("shiko", ((0.16, 0.06), -1, "open", 60), ((0.14, 0.08), -1, "open", 60), drop=0.03), A("sanchin", ((0.2, 0.06), -1, "open", 120), ((0.24, -0.1), -1, "open", 180), x=0.27, lean=0.0)),
    P(D("shiko", ((0.22, -0.2), -1, "open", -40), "hikite", drop=0.02), A("sanchin", "guard", ((0.2, -0.2), -1, "fist", -60), x=0.27)),
    P(D("shiko", "hikite", ((0.28, -0.16), -1, "nukite", -20), drop=0.02), A("sanchin", "guard", "hip", x=0.27, lean=0.03)),
    P(D("shiko", ((0.25, -0.06), -1, "claw", 0), ((0.25, -0.08), -1, "claw", 0)), A("zenkutsu", "guard", ((0.2, -0.08), -1, "open", 0), x=0.25, lean=0.05)),
    P(D("shiko", ((0.08, -0.16), +1, "fist", 0), ((0.08, -0.16), +1, "fist", 0), drop=0.03), A("zenkutsu", ((0.2, -0.22), -1, "open", -40), ((0.2, -0.22), -1, "open", -40), x=0.22, lean=0.1)),
], cols=4, panel_w=1.2)

plate("fig8_7", [
    P(D("heiko", "guard", "hip"), A("zenkutsu", "hikite", ((0.3, -0.04), -1, "open", 0), x=0.3)),
    P(D("heiko", "hip", ((0.2, -0.04), -1, "claw", 0)), A("zenkutsu", "hikite", ((0.3, -0.04), -1, "open", 0), x=0.3)),
    P(D("shiko", ((0.18, -0.02), -1, "fist", 90), ((0.1, -0.12), +1, "claw", 0)), A("zenkutsu", "hikite", ((0.32, -0.1), -1, "open", 0), x=0.3, lean=0.03)),
    P(D("shiko", ((0.22, -0.08), -1, "fist", 90), ((0.06, -0.16), +1, "claw", 0), drop=0.03), A("zenkutsu", "hikite", ((0.34, -0.18), -1, "open", -20), x=0.28, lean=0.1)),
    P(D("heiko", "guard", "hip"), A("zenkutsu", "guard", ((0.26, -0.04), -1, "claw", 180), x=0.28, lean=0.05)),
    P(D("shiko", ((0.24, 0.02), -1, "open", 60), ((0.26, -0.28), -1, "open", -60), drop=0.04, x=-0.18), A("zenkutsu", "guard", ((0.22, -0.04), -1, "claw", 180), x=0.24, lean=0.05)),
    P(D("heiko", ((0.24, 0.06), -1, "open", 60), ((0.26, -0.2), -1, "open", -20), x=-0.16), A("sagi", "guard", "guard", x=0.18, lean=-0.08, kick="knee")),
    P(D("shiko", ((0.2, -0.16), -1, "fist", -40), ((0.24, 0.1), -1, "open", 90), x=-0.16), A("sagi", ((0.2, 0.1), -1, "open", 90), "guard", x=0.14, lean=-0.14, kick="mae")),
], cols=4, panel_w=1.2)
print(COUNT)
