import sys; sys.path.insert(0, '.')
from goju import *

big_embusen("fig12_1", [(0, -0.45), (0.28, -0.25), (-0.28, -0.22), (0.0, -0.1), (0.0, 0.1), (0.4, 0.1), (-0.4, 0.13), (0.03, 0.13), (0.03, 0.45), (0.0, 0.25), (-0.02, -0.42)],
            [("1", (0.35, -0.27)), ("2", (-0.35, -0.22)), ("3", (0.08, 0.05)), ("4", (0.45, 0.04)), ("5", (-0.45, 0.13)),
             ("6", (0.1, 0.45)), ("7", (-0.08, 0.25)), ("8", (0.08, -0.45))])

og = ((0.18, -0.02), -1, "open", 80)
plate("fig12_2", [
    P(S("neko", "hip", "hip")), P(S("neko", "hip", "kake_uke")), P(S("neko", ((0.22, -0.1), -1, "palm", 90), "kake_uke")),
    P(S("neko", ((0.22, -0.1), -1, "palm", 90), ((0.2, -0.02), -1, "claw", 0))), P(S("neko", og, "grab_pull")),
    P(S("neko", "shotei", "grab_pull")), P(S("neko", og, ((0.24, -0.06), -1, "open", 70))), P(F("heiko", "hip", "hip", back=True)),
], cols=4)

plate("fig12_3", [
    P(S("neko", og, og)), P(S("sagi", og, og, kick="knee")), P(S("sagi", og, og, kick="mae")), P(S("sanchin", og, og)),
    P(S("sanchin", og, "shotei")), P(S("sanchin", "shotei", og)), P(S("sanchin", "shotei", "shotei", drop=0.01)), P(S("neko", og, og)),
], cols=4)

plate("fig12_4", [
    P(F("heiko", "kake_uke", "kake_uke")), P(F("heiko", "tensho_up", "tensho_up", drop=-0.01)), P(F("shiko", "tensho_up", "tensho_up", drop=-0.03)),
    P(F("shiko", "shotei_low", "shotei_high", drop=0.02)), P(F("shiko", "tensho_up", "tensho_up")), P(F("heiko", "hip", "hip", back=True)),
    P(F("shiko", "shotei_high", "shotei_low", drop=0.02)), P(F("neko", "kake_uke", "kake_uke")),
], cols=4)

plate("fig12_5", [
    P(S("neko", ((0.2, -0.12), -1, "open", 60), ((0.22, 0.08), -1, "open", 0))),
    P(S("sanchin", ((0.22, -0.08), -1, "claw", 60), ((0.24, 0.06), -1, "claw", -30))),
    P(S("sanchin", ((0.2, 0.02), -1, "claw", 120), ((0.24, -0.06), -1, "claw", -60), lean=-0.02)),
    P(S("kokutsu", ((0.18, 0.02), -1, "claw", 140), ((0.2, -0.12), -1, "claw", -80))),
    P(S("neko", ((0.15, -0.1), -1, "claw", -60), ((0.18, -0.2), -1, "claw", -80))), P(S("neko", "guard", "gedan_tsuki")),
    P(F("neko", mawashi_frames()[1][7], mawashi_frames()[0][7])), P(F("heiko", "yoi_open", "yoi_open")),
], cols=4)

plate("fig12_6", [
    P(D("neko", og, og), A("zenkutsu", "hikite", ((0.32, -0.02), -1, "fist", 0), x=0.32)),
    P(D("neko", og, ((0.2, 0.0), -1, "open", 110)), A("zenkutsu", "hikite", ((0.32, -0.02), -1, "fist", 0), x=0.32)),
    P(D("neko", ((0.24, -0.06), -1, "palm", 90), ((0.2, -0.02), -1, "claw", 0)), A("zenkutsu", "hikite", ((0.32, -0.04), -1, "fist", 0), x=0.32)),
    P(D("sanchin", ((0.26, 0.06), -1, "palm", 90), "grab_pull"), A("zenkutsu", "hikite", ((0.32, -0.12), -1, "fist", 0), x=0.3, lean=0.05)),
    P(D("neko", og, og), A("sanchin", "guard", "guard", x=0.32)),
    P(D("sagi", og, og, kick="mae"), A("sanchin", "guard", "guard", x=0.34)),
    P(D("sanchin", og, og), A("zenkutsu", "guard", "hip", x=0.28, lean=0.12)),
    P(D("sanchin", "shotei", "shotei"), A("zenkutsu", "guard", "hip", x=0.28, lean=0.1)),
], cols=4, panel_w=1.25)

plate("fig12_7", [
    P(D("heiko", "guard", "hip"), A("sanchin", ((0.24, -0.02), -1, "claw", 180), ((0.24, -0.02), -1, "claw", 180), x=0.26)),
    P(D("shiko", "guard", "guard", drop=0.02), A("sanchin", ((0.26, -0.06), -1, "claw", 180), ((0.26, -0.06), -1, "claw", 180), x=0.26, lean=0.03)),
    P(D("shiko", "shotei_low", "shotei", drop=0.02), A("sanchin", "guard", "guard", x=0.3, lean=-0.04)),
    P(D("shiko", "shotei_low", "shotei"), A("heiko", "guard", "guard", x=0.4, lean=-0.08)),
    P(D("heiko", "guard", "hip"), A("sanchin", "hikite", ((0.26, -0.02), -1, "claw", 180), x=0.26)),
    P(D("sanchin", ((0.22, 0.02), -1, "open", 0), ((0.2, -0.06), -1, "claw", 0)), A("sanchin", "hikite", ((0.26, -0.02), -1, "claw", 180), x=0.26)),
    P(D("kokutsu", ((0.2, -0.06), -1, "open", -30), ((0.12, -0.14), -1, "claw", 0), x=-0.3), A("zenkutsu", "hikite", ((0.32, -0.1), -1, "claw", 180), x=0.24, lean=0.12)),
    P(D("neko", ((0.18, -0.16), -1, "open", -60), ((0.1, -0.2), -1, "claw", 0), x=-0.32), A("zenkutsu", "guard", ((0.3, -0.2), -1, "open", -40), x=0.2, lean=0.2, drop=0.04)),
], cols=4, panel_w=1.25)
print(COUNT)
