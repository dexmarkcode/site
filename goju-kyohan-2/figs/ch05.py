import sys; sys.path.insert(0, '.')
from goju import *

plate("fig5_1", [
    hand_panel("open", 90, -60, "kake uke"), hand_panel("palm", 0, 0, "shotei"), hand_panel("palm", 180, 180, "gedan shotei") if False else hand_panel("palm", -90, 10, "gedan shotei"),
    hand_panel("open", 120, -40, "tensho uke"), hand_panel("hook", 90, 10, "koken"), hand_panel("claw", 20, 20, "tora guchi"),
    hand_panel("nukite", 20, 20, "nukite"), hand_panel("open", 190, 190, "hiki te"),
], cols=4, height=0.85)

cyc = ["kake_uke", ((0.03, -0.14), (-0.03, -0.05), "open", 95), "shotei", ((0.03, -0.14), (0.0, -0.13), "open", -40),
       "shotei_low", "tensho_out", "koken", "kake_uke"]
plate("fig5_2", [P(F("sanchin", "hikite", a)) for a in cyc], cols=4)

plate("fig5_3", [
    P(S("sanchin", "kake_uke", "kake_uke")), P(S("sanchin", lerp_side("kake_uke", "shotei", 0.5), lerp_side("kake_uke", "shotei", 0.5))),
    P(S("sanchin", "shotei", "shotei")), P(S("sanchin", lerp_side("shotei", "shotei_low", 0.5), lerp_side("shotei", "shotei_low", 0.5))),
    P(S("sanchin", "shotei_low", "shotei_low")), P(S("sanchin", "tensho_up", "tensho_up")),
    P(S("sanchin", "kake_uke", "shotei")), P(S("neko", "tora_down", "tora_up")),
], cols=4)

plate("fig5_4", [
    P(S("sanchin", "hikite", ((0.29, -0.04), -1, "open", 20))), P(S("sanchin", "hikite", "shotei")),
    P(S("sanchin", "hikite", ((0.17, 0.02), +1, "open", 90))), P(S("sanchin", "hikite", "kake_uke")),
    P(F("sanchin", ((0.12, -0.12), (0.10, -0.02), "open", 80), ((0.12, -0.12), (0.10, -0.02), "open", 80))), P(F("sanchin", "kake_uke", "kake_uke")),
    P(S("sanchin", ((0.28, 0.0), -1, "palm", 90), ((0.28, 0.0), -1, "palm", 90), lean=-0.04)), P(S("sanchin", "shotei", "shotei")),
], cols=4, caption_labels=["fault", "correct", "fault", "correct", "fault", "correct", "fault", "correct"])

w = ((0.22, -0.06), -1, "open", 70)
plate("fig5_5", [
    P(D("sanchin", "guard", w), A("sanchin", "guard", w)),
    P(D("sanchin", "guard", ((0.29, -0.06), -1, "palm", 90)), A("sanchin", "guard", ((0.16, -0.06), -1, "open", 70))),
    P(D("sanchin", "guard", ((0.29, -0.06), -1, "palm", 90)), A("sanchin", "guard", ((0.13, -0.05), -1, "open", 70), lean=-0.02)),
    P(D("sanchin", "guard", ((0.25, 0.0), -1, "palm", 90)), A("sanchin", "guard", ((0.17, 0.01), -1, "open", 110))),
    P(D("sanchin", "guard", ((0.17, -0.05), -1, "open", 70)), A("sanchin", "guard", ((0.28, -0.06), -1, "palm", 90))),
    P(D("sanchin", "guard", ((0.13, -0.05), -1, "open", 70), lean=-0.02), A("sanchin", "guard", ((0.29, -0.06), -1, "palm", 90))),
    P(D("sanchin", "guard", ((0.17, 0.01), -1, "open", 110)), A("sanchin", "guard", ((0.25, 0.0), -1, "palm", 90))),
    P(D("sanchin", "guard", w), A("sanchin", "guard", w)),
], cols=4, panel_w=1.15)

plate("fig5_6", [
    P(D("zenkutsu", "guard", ((0.30, -0.04), -1, "palm", 90), lean=0.06, x=-0.2), A("zenkutsu", "guard", ((0.30, -0.04), -1, "palm", 90), lean=0.06, x=0.2)),
    P(D("sanchin", "guard", w), A("sanchin", "guard", w)),
    P(D("sanchin", "guard", ((0.12, -0.12), -1, "open", 60)), A("sanchin", "guard", ((0.24, 0.02), -1, "open", 70))),
    P(D("sanchin", "guard", ((0.22, -0.02), -1, "open", 100)), A("sanchin", "guard", ((0.22, -0.02), -1, "open", 80))),
    P(D("sanchin", "guard", ((0.29, -0.06), -1, "palm", 90)), A("heiko", "guard", ((0.10, -0.05), -1, "open", 70))),
    P(D("sanchin", "guard", ((0.29, -0.06), -1, "palm", 90)), A("sanchin", "guard", ((0.13, -0.05), -1, "open", 70), lean=-0.03)),
    P(D("heiko", "guard", w, drop=-0.02), A("heiko", "guard", w, drop=-0.02)),
    P(D("sanchin", "guard", w), A("sanchin", "guard", w)),
], cols=4, panel_w=1.15, caption_labels=["fault", "correct", "fault", "correct", "fault", "correct", "fault", "correct"])
print(COUNT)
