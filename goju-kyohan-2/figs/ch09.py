import sys; sys.path.insert(0, '.')
from goju import *

big_embusen("fig9_1", [(0, -0.45), (0, 0.0), (0.0, 0.1), (0.4, 0.1), (-0.4, 0.13), (0.03, 0.13), (0.03, 0.5), (0.0, 0.3), (-0.02, -0.42)],
            [("1", (0.08, -0.35)), ("2", (0.08, -0.2)), ("3", (0.08, -0.05)), ("4", (0.45, 0.04)), ("5", (-0.45, 0.13)),
             ("6", (0.1, 0.5)), ("7", (-0.08, 0.28)), ("8", (0.08, -0.45))])

og = ((0.14, -0.01), -1, "open", 90)
plate("fig9_2", [
    P(S("sanchin", "hip", "hip")), P(S("sanchin", og, og)),
    P(S("sanchin", og, ((0.22, -0.05), -1, "nukite", 5))), P(S("sanchin", og, "nukite")),
    P(S("sanchin", og, ((0.30, -0.06), -1, "open", -60))), P(S("sanchin", og, ((0.17, -0.06), -1, "hook", 60))),
    P(S("sanchin", og, og, x=0.06)), P(S("sanchin", "nukite", og)),
], cols=4)

back = ((0.06, -0.06), -1, "palm", 90)
plate("fig9_3", [
    P(S("sanchin", back, back)), P(S("sanchin", back, "shotei")), P(S("sanchin", back, back)), P(S("sanchin", "shotei", back)),
    P(S("sanchin", back, back)), P(S("sanchin", "shotei", "shotei", drop=0.01)),
    P(S("sanchin", "shotei_low", ((0.28, 0.02), -1, "palm", 90))), P(S("sanchin", og, og)),
], cols=4)

plate("fig9_4", [
    P(F("sanchin", "kake_uke", "kake_uke")), P(F("heiko", "kake_uke", ((0.06, -0.12), (0.12, 0.0), "open", 80))),
    P(F("sanchin", "hip", ((0.08, -0.12), (0.18, -0.02), "open", 60))), P(F("sanchin", "hip", ((0.05, -0.15), (0.06, -0.24), "fist", -90))),
    P(F("shiko", "hikite", ((0.05, -0.15), (0.06, -0.24), "fist", -90), drop=-0.03)),
    P(F("shiko", ((0.16, -0.02), (0.20, 0.02), "fist", 160), "hikite")),
    P(F("shiko", "empi", "hikite", drop=0.02)), P(F("sanchin", "kake_uke", "kake_uke")),
], cols=4)

plate("fig9_5", [
    P(S("sagi", og, og, kick="chamber")), P(S("sagi", og, og, kick="mae")), P(S("sanchin", back, back)), P(S("sanchin", "shotei", "shotei", drop=0.01)),
    P(F("sanchin", "age_uke", "age_uke")), P(F("sanchin", "shotei_low", "shotei_low")),
    P(F("neko", mawashi_frames()[1][7], mawashi_frames()[0][7])), P(F("heiko", "yoi_open", "yoi_open")),
], cols=4)

plate("fig9_6", [
    P(D("sanchin", "hip", ((0.24, -0.02), -1, "open", 110)), A("sanchin", "hikite", ((0.3, -0.03), -1, "fist", 0), x=0.3)),
    P(D("sanchin", ((0.22, 0.0), -1, "open", 110), "nukite"), A("sanchin", "hikite", ((0.24, 0.06), -1, "fist", 60), x=0.3, lean=-0.03)),
    P(D("sanchin", og, ((0.22, -0.05), -1, "hook", 60)), A("sanchin", "hikite", ((0.24, -0.06), -1, "fist", 0), x=0.3)),
    P(D("sanchin", og, "grab_pull"), A("zenkutsu", "hikite", ((0.32, -0.12), -1, "fist", 0), x=0.26, lean=0.08)),
    P(D("sanchin", "hip", ((0.22, 0.0), -1, "open", 100)), A("zenkutsu", "hikite", ((0.32, -0.02), -1, "fist", 0), x=0.3)),
    P(D("sanchin", "hip", ((0.22, -0.02), -1, "claw", 0)), A("zenkutsu", "hikite", ((0.32, -0.03), -1, "fist", 0), x=0.3)),
    P(D("shiko", ((0.16, 0.02), -1, "fist", 90), ((0.06, -0.14), +1, "claw", 0)), A("zenkutsu", "hikite", ((0.34, -0.12), -1, "fist", 0), x=0.28, lean=0.06)),
    P(D("shiko", ((0.24, -0.06), -1, "fist", 90), ((0.04, -0.16), +1, "claw", 0), drop=0.02), A("zenkutsu", "hikite", ((0.36, -0.18), -1, "fist", -20), x=0.27, lean=0.1)),
], cols=4, panel_w=1.2)

pad = lambda ax, J: ax.add_patch(MPoly([(J["sh"][0] - 0.1 * 1, J["sh"][1] - 0.2), (J["sh"][0] - 0.06, J["sh"][1] - 0.2), (J["sh"][0] - 0.06, J["sh"][1] + 0.0), (J["sh"][0] - 0.1, J["sh"][1] + 0.0)], fc="white", ec="black", lw=0.9, zorder=7))
def padded(d, a):
    def fn(ax):
        d.draw(ax)
        J = a.draw(ax)
        floor(ax, -0.58, 0.58)
        x = J["sh"][0] - 0.085
        ax.add_patch(MPoly([(x - 0.035, J["sh"][1] - 0.2), (x + 0.0, J["sh"][1] - 0.2), (x + 0.0, J["sh"][1] + 0.0), (x - 0.035, J["sh"][1] + 0.0)], fc="white", ec="black", lw=0.9, zorder=7))
    return fn
plate("fig9_7", [
    P(D("sanchin", og, og), A("sanchin", ((0.2, -0.06), -1, "claw", 180), "guard", x=0.24)),
    P(D("sanchin", back, back, drop=0.01), A("sanchin", ((0.2, -0.06), -1, "claw", 180), "guard", x=0.24)),
    P(D("sanchin", ((0.2, -0.05), -1, "palm", 90), ((0.2, -0.05), -1, "palm", 90)), A("sanchin", "guard", "guard", x=0.26, lean=-0.03)),
    P(D("sanchin", "shotei", "shotei", drop=0.01), A("heiko", "guard", "guard", x=0.36, lean=-0.07)),
    padded(D("sanchin", back, back), A("sanchin", ((0.08, -0.12), -1, "open", 90), ((0.08, -0.12), -1, "open", 90), x=0.27)),
    padded(D("sanchin", "shotei", "shotei", drop=0.01), A("sanchin", ((0.08, -0.12), -1, "open", 90), ((0.08, -0.12), -1, "open", 90), x=0.3, lean=-0.03)),
    P(D("zenkutsu", "shotei", "shotei", lean=0.08, x=-0.28), A("sanchin", "guard", "guard", x=0.27)),
    P(D("sanchin", "shotei", "shotei", drop=0.01), A("sanchin", "guard", "guard", x=0.32, lean=-0.05)),
], cols=4, panel_w=1.2, caption_labels=["", "", "", "", "", "", "fault", "correct"])
print(COUNT)
