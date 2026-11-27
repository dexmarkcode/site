import sys; sys.path.insert(0, '.')
from goju import *

big_embusen("fig11_1", [(0, -0.45), (0.28, -0.2), (-0.28, -0.2), (0.0, -0.05), (0.0, 0.25), (0.4, 0.3), (-0.4, 0.33), (0.03, 0.33), (0.03, 0.5), (-0.02, -0.42)],
            [("1", (0.35, -0.22)), ("2", (-0.35, -0.2)), ("3", (0.08, -0.02)), ("4", (0.08, 0.2)), ("5", (0.45, 0.25)),
             ("6", (-0.45, 0.33)), ("7", (0.1, 0.5)), ("8", (0.08, -0.45))])

plate("fig11_2", [
    P(F("neko", "kake_uke", "hip")), P(F("neko", "hip", ((0.05, -0.12), (0.06, 0.0), "open", 100))),
    P(F("neko", "hip", ((0.1, -0.1), (0.18, -0.02), "open", 40))), P(F("neko", "hip", ((0.08, -0.12), (0.12, -0.1), "claw", -20))),
    P(F("sanchin", "hip", ((0.04, -0.15), (0.02, -0.24), "fist", -90))), P(F("sanchin", ((0.08, -0.02), (0.05, 0.08), "fist", 90), "hikite")),
    P(F("shiko", "uraken", "hikite", drop=0.02)), P(F("neko", "kake_uke", "kake_uke")),
], cols=4)

plate("fig11_3", [
    P(S("sanchin", "guard", "chudan_uke")), P(S("musubi", "guard", "chamber")), P(S("kosa", "hikite", "uraken")),
    P(S("kosa", "hikite", ((0.24, -0.08), -1, "fist", 0))), P(S("musubi", "hikite", "hikite")), P(S("sanchin", "hikite", "gedan_barai")),
    P(S("kosa", "guard", "chamber")), P(S("kosa", "hikite", "kentsui")),
], cols=4)

plate("fig11_4", [
    P(F("heiko", "gedan_open", ((0.06, 0.05), (0.04, 0.18), "open", 90))),
    P(F("heiko", "gedan_open", ((-0.06, 0.0), (-0.18, 0.04), "open", 180))),
    P(F("heiko", ((0.10, -0.06), (0.16, 0.06), "open", 90), ((-0.04, -0.12), (-0.16, -0.16), "open", 200))),
    P(F("heiko", "cross_high", "cross_low")),
    P(F("heiko", ((-0.03, 0.06), (-0.1, 0.18), "open", 120), "gedan_open", back=True)),
    P(F("shiko", "hikite", "gedan_open", drop=0.02)), P(F("shiko", "hikite", "kentsui", drop=0.03)), P(F("neko", "kake_uke", "kake_uke")),
], cols=4)

plate("fig11_5", [
    P(F("sanchin", "cross_high", "cross_high")), P(S("sanchin", "guard", "empi_rear")),
    P(F("heiko", "hikite", "hikite", back=True)), P(F("shiko", "hikite", "uraken")), P(F("shiko", "hikite", "kentsui", drop=0.02)),
    P(S("neko", "guard", "chamber")), P(F("neko", mawashi_frames()[1][7], mawashi_frames()[0][7])), P(F("heiko", "yoi_open", "yoi_open")),
], cols=4)

plate("fig11_6", [
    P(D("neko", "guard", "hip"), A("zenkutsu", "hikite", ((0.32, -0.02), -1, "fist", 0), x=0.3)),
    P(D("neko", "hip", ((0.22, 0.02), -1, "open", 120)), A("zenkutsu", "hikite", ((0.32, -0.02), -1, "fist", 0), x=0.3)),
    P(D("neko", "hip", ((0.22, -0.02), -1, "claw", 0)), A("zenkutsu", "hikite", ((0.32, -0.04), -1, "fist", 0), x=0.3)),
    P(D("sanchin", "chudan_tsuki", "grab_pull"), A("zenkutsu", "hikite", ((0.34, -0.12), -1, "fist", 0), x=0.26, lean=0.08)),
    P(D("kosa", "guard", "guard", x=-0.15), A("zenkutsu", "hikite", ((0.3, -0.02), -1, "fist", 0), x=0.3)),
    P(D("kosa", "guard", ((0.2, -0.05), -1, "claw", 0), x=-0.1), A("sanchin", "hikite", ((0.24, -0.02), -1, "fist", 0), x=0.24)),
    P(D("zenkutsu", "guard", ((0.22, 0.02), -1, "palm", 90), x=-0.05), A("sanchin", "guard", "hikite", x=0.24, lean=-0.06)),
    P(D("zenkutsu", "shotei", "shotei", x=-0.02), A("sagi", "guard", "guard", x=0.3, lean=-0.14, kick="mae")),
], cols=4, panel_w=1.2)

plate("fig11_7", [
    P(D("heiko", "guard", "hip"), A("sanchin", "hikite", ((0.26, -0.02), -1, "claw", 180), x=0.26)),
    P(D("heiko", ((0.22, 0.04), -1, "claw", 60), ((0.22, -0.06), -1, "claw", 0)), A("sanchin", "hikite", ((0.26, -0.02), -1, "claw", 180), x=0.26)),
    P(D("shiko", ((0.2, 0.08), -1, "claw", 60), ((0.2, -0.14), -1, "claw", -40), drop=0.02), A("zenkutsu", "hikite", ((0.26, -0.06), -1, "claw", 180), x=0.24, lean=0.08)),
    P(D("shiko", ((0.18, -0.02), -1, "claw", 0), ((0.14, -0.2), -1, "claw", -60), drop=0.04), A("zenkutsu", "guard", ((0.2, -0.2), -1, "open", -60), x=0.2, lean=0.2)),
    P(Figure("sanchin", "side", ((0.24, -0.06), -1, "claw", 0), ((0.24, -0.06), -1, "claw", 0), x=-0.18, facing=1, partner=True), S("heiko", "guard", "guard", x=0.1)),
    P(Figure("sanchin", "side", ((0.24, -0.1), -1, "claw", 0), ((0.24, -0.1), -1, "claw", 0), x=-0.2, facing=1, partner=True), S("shiko", "guard", "guard", x=0.1, drop=0.02)),
    P(Figure("sanchin", "side", ((0.2, -0.1), -1, "open", 0), "guard", x=-0.24, facing=1, partner=True, lean=0.05), S("shiko", "guard", "empi_rear", x=0.1)),
    P(Figure("sanchin", "side", "guard", "guard", x=-0.26, facing=1, partner=True, lean=0.08), S("sanchin", "hikite", ((0.26, 0.04), -1, "fist", 70), x=0.1, facing=-1)),
], cols=4, panel_w=1.2)
print(COUNT)
