import sys; sys.path.insert(0, '.')
from goju import *

big_embusen("fig7_1", [(0, -0.45), (0.25, -0.22), (-0.25, -0.05), (0.25, 0.12), (0.03, 0.2), (0.03, 0.5), (0.0, 0.05), (0.35, 0.05), (-0.35, 0.08), (-0.02, -0.4)],
            [("1", (0.32, -0.25)), ("2", (-0.32, -0.05)), ("3", (0.32, 0.15)), ("4", (0.1, 0.5)), ("5", (-0.08, 0.25)),
             ("6", (0.42, 0.05)), ("7", (-0.42, 0.08)), ("8", (0.08, -0.4))])

cover = ((0.10, -0.15), (-0.10, -0.24), "fist", 200)
cover_l = ((-0.02, -0.15), (0.08, -0.25), "open", 0)
plate("fig7_2", [
    P(F("heiko", "yoi_open", "yoi_open")),
    P(F("heiko", "hikite", ((0.0, -0.14), (-0.06, -0.20), "fist", 200))),
    P(F("musubi", ((0.0, -0.13), (-0.04, -0.17), "open", 180), ((0.0, -0.14), (-0.08, -0.18), "fist", 200))),
    P(F("musubi", ((0.04, -0.14), (0.04, -0.24), "open", -90), ((0.04, -0.14), (-0.17, -0.24), "fist", 180))),
    P(F("shiko", ((0.0, -0.10), (-0.05, -0.12), "open", 180), ((0.06, -0.10), (-0.10, -0.08), "fist", 180), drop=-0.04)),
    P(F("shiko", ((-0.02, -0.12), (-0.03, -0.09), "open", 180), ((0.12, -0.04), (-0.07, -0.07), "fist", 180))),
    P(F("shiko", ((-0.02, -0.12), (-0.05, -0.08), "open", 180), ((0.13, -0.02), (-0.06, -0.06), "fist", 180), drop=0.02)),
    P(F("musubi", ((0.0, -0.14), (-0.08, -0.18), "fist", 200), ((0.0, -0.13), (-0.04, -0.17), "open", 180))),
], cols=4)

plate("fig7_3", [
    P(S("sagi", "guard", "chamber", kick="chamber")),
    P(S("sagi", "guard", "chamber", kick="mae")),
    P(S("seisan", ((0.25, -0.20), -1, "open", -40), "chamber")),
    P(S("seisan", "gedan_open", "uraken")),
    P(S("seisan", "chudan_tsuki", "hikite")),
    P(F("heiko", "hikite", "chamber_side")),
    P(S("sagi", "guard", "chamber", kick="chamber", facing=-1)),
    P(S("sagi", "guard", "chamber", kick="mae", facing=-1)),
], cols=4)

plate("fig7_4", [
    P(F("heiko", "hikite", ((-0.05, -0.08), (-0.18, -0.10), "open", 180))),
    P(F("heiko", "uraken", ((0.06, -0.15), (-0.02, -0.22), "fist", 200), drop=-0.02)),
    P(F("shiko", ((0.08, 0.0), (0.04, 0.10), "fist", 90), "hikite", drop=-0.05)),
    P(F("shiko", "kentsui", "hikite", drop=0.02)),
    P(F("shiko", "hikite", "hikite")),
    P(F("heiko", "hikite", "hikite", back=True)),
    P(F("heiko", ((-0.05, -0.08), (-0.18, -0.10), "open", 180), "uraken", drop=-0.02)),
    P(F("shiko", "hikite", "kentsui", drop=0.02)),
], cols=4)

plate("fig7_5", [
    P(F("neko", "age_uke", "gedan_barai")),
    P(F("neko", "shotei_low", "shotei_low")),
    P(S("seisan", "guard", "chamber")),
    P(F("shiko", "uraken", ((0.04, -0.15), (-0.02, -0.25), "fist", -90), drop=0.02)),
    P(S("neko", "guard", "chamber")),
    P(F("neko", mawashi_frames()[1][2], mawashi_frames()[0][2])),
    P(F("neko", mawashi_frames()[1][7], mawashi_frames()[0][7])),
    P(F("heiko", "yoi_open", "yoi_open")),
], cols=4)

grab = ((0.26, -0.18), -1, "open", -10)
plate("fig7_6", [
    P(D("heiko", "hip", ((0.12, -0.18), -1, "fist", 0)), A("sanchin", "hikite", ((0.24, -0.19), -1, "claw", 180))),
    P(D("heiko", ((0.12, -0.17), -1, "open", 0), ((0.12, -0.18), -1, "fist", 0)), A("sanchin", "hikite", ((0.24, -0.19), -1, "claw", 180))),
    P(D("musubi", ((0.03, -0.24), +1, "open", 0), ((0.03, -0.24), +1, "fist", 0)), A("sanchin", "hikite", ((0.33, -0.24), -1, "claw", 180), lean=0.03)),
    P(D("musubi", ((0.0, -0.24), +1, "open", 0), ((0.0, -0.24), +1, "fist", 0)), A("zenkutsu", "hikite", ((0.32, -0.25), -1, "claw", 180), lean=0.06, x=0.25)),
    P(D("shiko", ((0.08, -0.1), +1, "open", 0), ((0.08, -0.08), +1, "fist", 0), drop=-0.03), A("zenkutsu", "hikite", ((0.32, -0.16), -1, "claw", 180), lean=0.05, x=0.25)),
    P(D("shiko", ((0.1, -0.06), +1, "open", 0), ((0.13, 0.0), +1, "fist", 90)), A("sanchin", "hikite", ((0.28, -0.08), -1, "open", 120), x=0.27)),
    P(D("shiko", ((0.1, -0.06), +1, "open", 0), ((0.22, 0.04), +1, "fist", 180), drop=0.02), A("sanchin", "hikite", "guard", x=0.27, lean=-0.05)),
    P(D("shiko", "hikite", "hikite"), A("heiko", "guard", "hip", x=0.32, lean=-0.06)),
], cols=4, panel_w=1.2)

plate("fig7_7", [
    P(D("neko", "guard", "chamber"), A("zenkutsu", "guard", "chamber", x=0.3)),
    P(D("sagi", "guard", "chamber", kick="mae"), A("zenkutsu", "guard", "chamber", x=0.3, lean=0.03)),
    P(D("seisan", ((0.26, -0.14), -1, "open", -20), "chamber"), A("zenkutsu", ((0.22, -0.16), -1, "fist", 0), "hikite", x=0.3, lean=0.06)),
    P(D("seisan", ((0.26, -0.16), -1, "open", -20), "uraken"), A("zenkutsu", ((0.22, -0.18), -1, "fist", 0), "hikite", x=0.3, lean=0.06)),
    P(D("heiko", "guard", "hip"), A("sanchin", "hikite", ((0.26, -0.02), -1, "claw", 180))),
    P(D("heiko", ((0.18, -0.02), -1, "claw", 0), ((0.05, 0.06), -1, "fist", 90)), A("sanchin", "hikite", ((0.28, -0.02), -1, "claw", 180), lean=0.03)),
    P(D("shiko", ((0.05, -0.14), +1, "fist", 0), ((0.08, 0.06), -1, "fist", 90), drop=-0.02), A("zenkutsu", "hikite", ((0.32, -0.14), -1, "open", 180), lean=0.08, x=0.26)),
    P(D("shiko", ((0.05, -0.14), +1, "fist", 0), ((0.22, -0.1), -1, "fist", -70), drop=0.02), A("zenkutsu", "hikite", ((0.32, -0.16), -1, "open", 180), lean=0.09, x=0.26)),
], cols=4, panel_w=1.2)
print(COUNT)
