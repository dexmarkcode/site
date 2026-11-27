import sys; sys.path.insert(0, '.')
from goju import *

big_embusen("fig14_1", [(0, -0.45), (0, 0.0), (0.0, 0.08), (0.4, 0.08), (-0.4, 0.11), (0.02, 0.11), (0.02, -0.2), (0.05, -0.2), (0.05, 0.45), (0.0, 0.25), (-0.03, -0.42)],
            [("1", (0.08, -0.35)), ("2", (0.08, -0.2)), ("3", (0.08, -0.05)), ("4", (0.45, 0.02)), ("5", (-0.45, 0.11)),
             ("6", (-0.08, -0.22)), ("7", (0.12, 0.45)), ("8", (0.1, -0.45))])

og = ((0.14, -0.01), -1, "open", 90)
plate("fig14_2", [
    P(S("sanchin", "hip", "hip")), P(S("sanchin", og, og)), P(S("sanchin", ((0.22, -0.05), -1, "nukite", 5), ((0.22, -0.05), -1, "nukite", 5))),
    P(S("sanchin", "nukite", "nukite")), P(S("sanchin", ((0.3, -0.06), -1, "open", -60), ((0.3, -0.06), -1, "open", -60))),
    P(S("sanchin", ((0.17, -0.06), -1, "hook", 60), ((0.17, -0.06), -1, "hook", 60))), P(S("musubi", og, og)), P(S("sanchin", "nukite", "nukite", x=0.04)),
], cols=4)

plate("fig14_3", [
    P(F("sanchin", "hip", "kake_uke")), P(F("sanchin", "hip", ((0.08, -0.12), (0.12, -0.1), "claw", -20))),
    P(F("sanchin", "shotei", ((0.04, -0.15), (0.02, -0.24), "fist", -90))), P(F("sagi", "kake_uke", "hikite", kick="knee", front_leg="R")),
    P(S("sagi", "guard", "chamber", kick="mae")), P(S("seisan", "guard", ((0.12, 0.06), +1, "fist", 180))),
    P(S("seisan", "guard", "uraken")), P(F("heiko", "hip", "hip", back=True)),
], cols=4)

plate("fig14_4", [
    P(S("sanchin", "shotei", "shotei")), P(S("sagi", "tora_up", "tora_up", kick="knee")), P(S("sagi", ((0.12, 0.12), -1, "claw", 90), ((0.12, 0.12), -1, "claw", 90), kick="knee")),
    P(S("sagi", "guard", "guard", kick="mae")), P(S("zenkutsu", "tora_up", "tora_up")), P(S("zenkutsu", "tora_down", "tora_up")),
    P(S("seisan", og, og)), P(S("neko", og, og)),
], cols=4)

plate("fig14_5", [
    P(F("shiko", "kentsui", "kentsui", drop=0.03)), P(F("shiko", "hikite", "gedan_tsuki")), P(F("shiko", ((0.04, -0.15), (0.02, -0.24), "fist", -90), "chamber_side")),
    P(F("shiko", ((0.04, -0.15), (0.02, -0.24), "fist", -90), ((-0.08, -0.06), (-0.2, -0.08), "fist", 180))),
    P(F("shiko", "hikite", "empi", drop=0.02)), P(S("neko", "guard", "chamber")),
    P(F("neko", mawashi_frames()[1][7], mawashi_frames()[0][7])), P(F("heiko", "yoi_open", "yoi_open")),
], cols=4)

lapel = ((0.24, -0.02), -1, "claw", 180)
plate("fig14_6", [
    P(D("sanchin", "hip", "hip"), A("sanchin", lapel, lapel, x=0.26)),
    P(D("sanchin", ((0.2, -0.02), -1, "nukite", 5), ((0.2, -0.02), -1, "nukite", 5)), A("sanchin", lapel, lapel, x=0.26)),
    P(D("sanchin", ((0.22, 0.02), -1, "open", 50), ((0.22, 0.02), -1, "open", 50)), A("sanchin", ((0.18, 0.1), -1, "open", 120), ((0.16, -0.14), -1, "open", -60), x=0.28)),
    P(D("sanchin", og, "shotei"), A("sanchin", "guard", "hip", x=0.3, lean=-0.05)),
    P(D("sanchin", "hip", ((0.22, 0.02), -1, "open", 110)), A("zenkutsu", "hikite", ((0.32, -0.02), -1, "fist", 0), x=0.3)),
    P(D("sanchin", "hip", "grab_pull"), A("zenkutsu", "hikite", ((0.34, -0.12), -1, "fist", 0), x=0.27, lean=0.08)),
    P(D("sagi", "guard", "grab_pull", kick="mae"), A("zenkutsu", "hikite", ((0.34, -0.12), -1, "fist", 0), x=0.3, lean=0.06)),
    P(D("seisan", "guard", ((0.12, 0.05), +1, "fist", 180)), A("zenkutsu", "hikite", "hip", x=0.27, lean=0.12)),
], cols=4, panel_w=1.25)

plate("fig14_7", [
    P(D("neko", og, og), A("sagi", "guard", "guard", x=0.3, kick="kansetsu")),
    P(D("sagi", "tora_up", "tora_up", kick="knee"), A("sagi", "guard", "guard", x=0.3, kick="kansetsu")),
    P(D("zenkutsu", og, og, x=-0.28), A("sanchin", "guard", "guard", x=0.3)),
    P(D("zenkutsu", "tora_down", "tora_up", x=-0.28), A("sanchin", "guard", "guard", x=0.32, lean=-0.06)),
    P(D("heiko", "guard", "hip"), A("zenkutsu", "hikite", ((0.3, -0.04), -1, "open", 0), x=0.3)),
    P(D("heiko", "hip", ((0.2, -0.04), -1, "claw", 0)), A("zenkutsu", "hikite", ((0.3, -0.04), -1, "open", 0), x=0.3)),
    P(D("shiko", ((0.22, -0.08), -1, "fist", 90), ((0.06, -0.16), +1, "claw", 0), drop=0.03), A("zenkutsu", "hikite", ((0.34, -0.18), -1, "open", -20), x=0.28, lean=0.1)),
    P(D("shiko", ((0.22, -0.16), -1, "fist", 90), ((0.06, -0.2), +1, "claw", 0), drop=0.05), A("zenkutsu", "hikite", ((0.32, -0.26), -1, "open", -40), x=0.26, lean=0.2, drop=0.05)),
], cols=4, panel_w=1.25)
print(COUNT)
