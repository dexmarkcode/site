import sys; sys.path.insert(0, '.')
from goju import *

big_embusen("fig10_1", [(0, -0.45), (0, 0.0), (0.0, 0.08), (0.4, 0.08), (-0.4, 0.11), (0.03, 0.11), (0.03, 0.45), (0.0, 0.2), (-0.02, -0.42)],
            [("1", (0.08, -0.35)), ("2", (0.08, -0.2)), ("3", (0.08, -0.05)), ("4", (0.45, 0.02)), ("5", (-0.45, 0.11)),
             ("6", (0.1, 0.45)), ("7", (-0.08, 0.2)), ("8", (0.08, -0.45))])

plate("fig10_2", [
    P(S("sanchin", "sanchin", "sanchin")), P(S("sanchin", "sanchin", "chudan_tsuki")), P(S("sanchin", "chudan_tsuki", "hikite")),
    P(S("sanchin", "sanchin", "sanchin")), P(S("musubi", "sanchin", "sanchin")), P(S("sanchin", "sanchin", "sanchin", x=0.05)),
    P(S("sanchin", "gedan_tsuki", "jodan_tsuki")), P(S("sanchin", "sanchin", "sanchin")),
], cols=4)

ctl = ((0.22, 0.0), -1, "claw", 0)
plate("fig10_3", [
    P(S("sanchin", "guard", "chudan_uke")), P(S("sanchin", ctl, ((0.22, -0.04), -1, "open", 90))),
    P(S("sanchin", ctl, ((0.22, -0.04), -1, "open", 90), kick="chamber")), P(S("sanchin", ctl, ((0.22, -0.04), -1, "open", 90), kick="kansetsu")),
    P(S("sanchin", ctl, ((0.22, -0.04), -1, "open", 90), kick="stamp")), P(S("sanchin", "hikite", ((0.14, 0.05), +1, "fist", 180))),
    P(S("sanchin", "guard", "chudan_uke", facing=-1)), P(S("sanchin", ctl, ((0.22, -0.04), -1, "open", 90), kick="kansetsu", facing=-1)),
], cols=4)

g = ((0.26, 0.04), -1, "claw", 0)
plate("fig10_4", [
    P(S("sanchin", ((0.22, 0.0), -1, "open", 30), ((0.22, 0.0), -1, "open", 30))), P(S("sanchin", g, g)),
    P(S("sanchin", ((0.24, -0.1), -1, "claw", -20), ((0.24, -0.1), -1, "claw", -20))),
    P(S("sanchin", ((0.2, -0.2), -1, "claw", -60), ((0.2, -0.2), -1, "claw", -60), kick="chamber")),
    P(S("sanchin", ((0.18, -0.24), -1, "claw", -80), ((0.18, -0.24), -1, "claw", -80), kick="knee")),
    P(S("sanchin", "guard", "guard")), P(S("sanchin", "shotei", "shotei")), P(S("sanchin", "sanchin", "sanchin")),
], cols=4)

plate("fig10_5", [
    P(F("shiko", "hikite", ((-0.06, 0.06), (-0.1, -0.02), "fist", 180))), P(F("shiko", "hikite", "uraken")),
    P(F("shiko", "hikite", "kentsui", drop=0.02)), P(F("shiko", "hikite", "gedan_barai")),
    P(S("neko", "guard", "chamber")), P(F("neko", mawashi_frames()[1][3], mawashi_frames()[0][3])),
    P(F("neko", mawashi_frames()[1][7], mawashi_frames()[0][7])), P(F("heiko", "yoi_open", "yoi_open")),
], cols=4)

guard = ((0.18, 0.0), -1, "fist", 80)
plate("fig10_6", [
    P(D("sanchin", "sanchin", "sanchin"), A("sanchin", guard, ((0.12, 0.02), -1, "fist", 80), x=0.28)),
    P(D("sanchin", "sanchin", ((0.27, -0.0), -1, "fist", 0)), A("sanchin", guard, ((0.12, 0.02), -1, "fist", 80), x=0.28, lean=-0.03)),
    P(D("sanchin", "chudan_tsuki", "hikite"), A("sanchin", guard, ((0.08, -0.05), -1, "fist", 80), x=0.28, lean=-0.04)),
    P(D("sanchin", "sanchin", "sanchin"), A("sanchin", ((0.24, -0.02), -1, "claw", 180), ((0.24, -0.02), -1, "claw", 180), x=0.26)),
    P(D("sanchin", ((0.2, -0.02), -1, "claw", 0), ((0.2, -0.02), -1, "claw", 0)), A("sanchin", ((0.24, -0.02), -1, "claw", 180), ((0.24, -0.02), -1, "claw", 180), x=0.26)),
    P(D("sanchin", ((0.2, -0.02), -1, "claw", 0), ((0.2, -0.02), -1, "claw", 0), kick="kansetsu"), A("sanchin", ((0.24, -0.02), -1, "claw", 180), ((0.24, -0.02), -1, "claw", 180), x=0.26)),
    P(D("sanchin", ((0.2, -0.06), -1, "claw", 0), ((0.2, -0.06), -1, "claw", 0), kick="stamp"), A("sanchin", ((0.24, -0.08), -1, "claw", 180), ((0.24, -0.08), -1, "claw", 180), x=0.26, drop=0.05)),
    P(D("sanchin", "hikite", ((0.16, 0.03), +1, "fist", 180)), A("sanchin", "guard", "guard", x=0.27, drop=0.06, lean=-0.03)),
], cols=4, panel_w=1.2)

plate("fig10_7", [
    P(D("sanchin", "guard", "guard"), A("zenkutsu", "guard", "hip", x=0.26, lean=0.12)),
    P(D("sanchin", ((0.26, 0.0), -1, "claw", -30), ((0.26, 0.0), -1, "claw", -30)), A("zenkutsu", "guard", "hip", x=0.26, lean=0.12)),
    P(D("sanchin", ((0.22, -0.12), -1, "claw", -60), ((0.22, -0.12), -1, "claw", -60)), A("zenkutsu", "guard", "hip", x=0.24, lean=0.16)),
    P(D("sanchin", ((0.2, -0.18), -1, "claw", -70), ((0.2, -0.18), -1, "claw", -70), kick="knee"), A("zenkutsu", "guard", "hip", x=0.24, lean=0.18)),
    P(D("sanchin", "guard", "guard"), A("zenkutsu", ((0.28, 0.0), -1, "palm", 90), "hip", x=0.28, lean=0.04)),
    P(D("shiko", "guard", "guard", drop=0.02), A("zenkutsu", ((0.28, 0.0), -1, "palm", 90), "hip", x=0.27, lean=0.06)),
    P(D("shiko", "guard", ((0.1, 0.14), +1, "fist", 180)), A("zenkutsu", "guard", "hip", x=0.24, lean=0.0)),
    P(D("shiko", "guard", ((0.2, -0.12), -1, "fist", -70), drop=0.02), A("zenkutsu", "guard", "hip", x=0.24, lean=0.16)),
], cols=4, panel_w=1.2)
print(COUNT)
