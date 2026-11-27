import sys; sys.path.insert(0, '.')
from goju import *

big_embusen("fig13_1", [(0, -0.45), (0, 0.1), (0.04, 0.1), (0.04, -0.15), (0.0, -0.12), (0.38, -0.12), (-0.38, -0.09), (0.0, -0.05), (0.0, 0.45), (-0.04, 0.4), (-0.04, -0.42)],
            [("1", (0.08, -0.35)), ("2", (-0.08, -0.15)), ("3", (-0.08, 0.08)), ("4", (0.1, -0.2)), ("5", (0.45, -0.12)),
             ("6", (-0.45, -0.09)), ("7", (0.08, 0.45)), ("8", (-0.1, -0.45))])

plate("fig13_2", [
    P(S("seisan", "sanchin", "sanchin")), P(S("seisan", "hikite", "chudan_uke")), P(S("seisan", "chudan_uke", "chudan_tsuki")),
    P(S("seisan", "chudan_tsuki", "hikite")), P(S("musubi", "sanchin", "sanchin")), P(S("seisan", "hikite", "chudan_uke", x=0.05)),
    P(S("seisan", "hikite", "kake_uke")), P(S("seisan", "kake_uke", "nukite")),
], cols=4)

plate("fig13_3", [
    P(S("sagi", "guard", "chamber", kick="chamber")), P(S("sagi", "guard", "chamber", kick="mae")), P(S("seisan", "guard", "chamber")),
    P(S("musubi", "guard", "chamber")), P(S("kosa", "hikite", ((0.24, -0.12), -1, "fist", -70))),
    P(S("kosa", ((0.22, -0.16), -1, "fist", -70), ((0.24, -0.12), -1, "fist", -70))), P(S("sanchin", "guard", "chamber")), P(S("seisan", "sanchin", "sanchin")),
], cols=4)

g = ((0.26, 0.02), -1, "claw", 0)
plate("fig13_4", [
    P(S("seisan", ((0.22, 0.0), -1, "open", 30), ((0.22, 0.0), -1, "open", 30))), P(S("seisan", g, g)),
    P(S("seisan", ((0.2, -0.16), -1, "claw", -60), ((0.2, -0.16), -1, "claw", -60))),
    P(S("sanchin", ((0.18, -0.2), -1, "claw", -70), ((0.18, -0.2), -1, "claw", -70), kick="chamber")),
    P(S("sanchin", ((0.16, -0.24), -1, "claw", -80), ((0.16, -0.24), -1, "claw", -80), kick="knee")),
    P(S("seisan", "guard", "guard")), P(S("seisan", "chudan_tsuki", "jodan_tsuki")), P(S("seisan", "sanchin", "sanchin")),
], cols=4)

plate("fig13_5", [
    P(F("shiko", "hikite", "gedan_open")), P(F("shiko", "hikite", ((0.08, -0.12), (0.12, -0.24), "shuto", -60), drop=0.02)),
    P(S("sanchin", "guard", "guard", kick="kansetsu")), P(F("shiko", "hikite", "gedan_tsuki")), P(F("heiko", "hip", "hip", back=True)),
    P(F("shiko", "gedan_open", "hikite")), P(F("neko", mawashi_frames()[1][7], mawashi_frames()[0][7])), P(F("heiko", "yoi_open", "yoi_open")),
], cols=4)

plate("fig13_6", [
    P(D("seisan", "sanchin", "sanchin"), A("zenkutsu", "hikite", ((0.3, -0.02), -1, "fist", 0), x=0.3)),
    P(D("seisan", "hikite", ((0.2, 0.0), -1, "fist", 90)), A("zenkutsu", "hikite", ((0.3, -0.02), -1, "fist", 0), x=0.3)),
    P(D("seisan", ((0.24, -0.06), -1, "fist", 0), ((0.2, 0.0), -1, "fist", 90)), A("zenkutsu", "hikite", ((0.3, -0.04), -1, "fist", 0), x=0.3, lean=-0.02)),
    P(D("seisan", ((0.2, 0.0), -1, "fist", 90), ((0.27, 0.02), -1, "fist", 0)), A("zenkutsu", "hikite", ((0.3, -0.06), -1, "fist", 0), x=0.3, lean=-0.04)),
    P(D("sagi", "guard", "guard", kick="mae"), A("sanchin", "guard", "guard", x=0.32)),
    P(D("seisan", "guard", "guard"), A("zenkutsu", "guard", "hip", x=0.3, lean=0.14)),
    P(D("kosa", "guard", "chamber", x=-0.14), A("zenkutsu", "guard", "hip", x=0.3, lean=0.16)),
    P(D("kosa", "hikite", ((0.24, -0.1), -1, "fist", -70), x=-0.12), A("zenkutsu", "guard", "hip", x=0.3, lean=0.2, drop=0.04)),
], cols=4, panel_w=1.25)

plate("fig13_7", [
    P(D("seisan", "guard", "guard"), A("zenkutsu", "guard", "hip", x=0.26, lean=0.14)),
    P(D("seisan", ((0.26, 0.0), -1, "claw", -30), ((0.26, 0.0), -1, "claw", -30)), A("zenkutsu", "guard", "hip", x=0.26, lean=0.14)),
    P(D("seisan", ((0.22, -0.12), -1, "claw", -60), ((0.22, -0.12), -1, "claw", -60)), A("zenkutsu", "guard", "hip", x=0.24, lean=0.18)),
    P(D("sanchin", ((0.2, -0.18), -1, "claw", -70), ((0.2, -0.18), -1, "claw", -70), kick="knee"), A("zenkutsu", "guard", "hip", x=0.24, lean=0.2)),
    P(D("sanchin", "guard", "guard"), A("zenkutsu", "hikite", ((0.32, -0.04), -1, "open", 0), x=0.3)),
    P(D("shiko", "guard", ((0.22, -0.12), -1, "shuto", -60)), A("zenkutsu", "hikite", ((0.34, -0.14), -1, "open", -20), x=0.3, lean=0.05)),
    P(D("sanchin", "guard", ((0.22, -0.14), -1, "claw", -60), kick="kansetsu"), A("zenkutsu", "hikite", ((0.34, -0.14), -1, "open", -20), x=0.3, lean=0.05)),
    P(D("sanchin", "hikite", "gedan_tsuki"), A("zenkutsu", "hikite", "hip", x=0.3, lean=0.1, drop=0.05)),
], cols=4, panel_w=1.25)
print(COUNT)
