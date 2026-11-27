import sys; sys.path.insert(0, '.')
from goju import *
og = ((0.14, -0.01), -1, "open", 90)
parts = {
 "part1": [P(F("heiko", "yoi_open", "yoi_open")), P(F("sanchin", "sanchin", "sanchin")), P(F("shiko", "gedan_barai", "age_uke"))],
 "part2": [P(S("sanchin", "sanchin", "sanchin")), P(S("sanchin", "kake_uke", "shotei")), with_tools(F("shiko", "hikite", "hira_side"), [lambda ax, J: chi_ishi(ax, J["handR"], 90, 0.2)])],
 "part3": [P(F("shiko", ((-0.02, -0.12), (-0.05, -0.08), "open", 180), ((0.13, -0.02), (-0.06, -0.06), "fist", 180))), P(F("shiko", "gedan_open", "hikite")), P(S("sanchin", og, "nukite"))],
 "part4": [P(S("sanchin", "guard", "guard", kick="kansetsu")), P(S("kosa", "hikite", "uraken")), P(S("neko", "shotei_low", "shotei"))],
 "part5": [P(S("sanchin", ((0.18, -0.24), -1, "claw", -80), ((0.18, -0.24), -1, "claw", -80), kick="knee")), P(S("sanchin", "nukite", "nukite")), P(F("neko", mawashi_frames()[1][7], mawashi_frames()[0][7]))],
}
for k, v in parts.items():
    plate(k, v, cols=3, numbered=False, width_in=3.6)
w = ((0.22, -0.06), -1, "open", 70)
plate("part6", [P(D("sanchin", "guard", w), A("sanchin", "guard", w)),
                P(D("shiko", ((0.22, -0.08), -1, "fist", 90), ((0.06, -0.16), +1, "claw", 0), drop=0.03), A("zenkutsu", "hikite", ((0.34, -0.18), -1, "open", -20), x=0.28, lean=0.1))],
      cols=2, numbered=False, width_in=3.6, panel_w=1.2)
plate("title_emblem", [P(F("neko", mawashi_frames()[1][7], mawashi_frames()[0][7]), ground=True)], cols=1, numbered=False, width_in=1.5)
print(COUNT)
