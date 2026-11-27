import sys; sys.path.insert(0, '.')
from goju import *

# 1.1 signature postures
plate("fig1_1", [
    P(F("shiko", (( -0.02, -0.12), (-0.11, -0.09), "fist", 180), ((0.02, -0.10), (0.02, -0.07), "open", 180))),
    P(F("shiko", "gedan_open", "chamber_side", drop=0.03)),
    P(S("sanchin", "hikite", "shotei")),
    P(S("neko", "guard", "chamber", kick="kansetsu")),
    P(F("kosa", "kentsui", "hikite")),
    P(S("neko", "shotei_low", "shotei")),
    P(S("sanchin", "grab_pull", "grab_pull", kick="knee")),
    P(S("sanchin", "nukite", "nukite")),
], cols=4, caption_labels=["Saifa", "Seiyunchin", "Shisochin", "Sanseru", "Sepai", "Kururunfa", "Seisan", "Suparinpei"])

# 1.2 opening and closing
plate("fig1_2", [
    P(F("musubi", "down", "down")),
    P(F("musubi", "down", "down", lean=0.0, drop=0.02)),
    P(F("musubi", "down", "down")),
    P(F("musubi", "cross_high", "cross_high")),
    P(F("heiko", "yoi_open", "yoi_open")),
    P(F("heiko", "down", "down")),
    P(F("musubi", "down", "down")),
    P(F("musubi", "down", "down", drop=0.02)),
], cols=4, caption_labels=["musubi dachi", "rei", "name of kata", "hands rise", "yoi", "hands lower", "musubi dachi", "rei"])

R, L = mawashi_frames()
plate("fig1_3", [P(F("neko", L[i], R[i])) for i in range(8)], cols=4)

# 1.4 four stages of learning (Saifa tearing release)
plate("fig1_4", [
    P(F("heiko", ((0.00, -0.12), (-0.10, -0.12), "fist", 180), ((0.02, -0.12), (0.05, -0.14), "open", 180))),
    P(F("heiko", "hikite", ((0.02, -0.10), (-0.08, -0.06), "fist", 180))),
    P(F("shiko", ((0.00, -0.12), (-0.10, -0.12), "fist", 180), ((0.02, -0.12), (0.05, -0.14), "open", 180))),
    P(F("shiko", "hikite", ((0.02, -0.10), (-0.08, -0.06), "fist", 180))),
    P(F("shiko", ((0.00, -0.12), (-0.10, -0.12), "fist", 180), ((0.02, -0.12), (0.05, -0.14), "open", 180), drop=0.02)),
    P(F("shiko", "hikite", ((-0.02, -0.06), (-0.12, -0.02), "fist", 180), drop=0.03)),
    P(D("sanchin", "hikite", ((0.26, -0.10), -1, "fist", 0)), A("sanchin", "guard", ((0.24, -0.14), -1, "open", -10))),
    P(D("shiko", "grab_pull", "empi"), A("sanchin", "hikite", ((0.22, -0.12), -1, "open", 0))),
], cols=4, panel_w=1.15)

# 1.5 three ways
plate("fig1_5", [
    P(S("sanchin", "hikite", lerp_side("hikite", "chudan_tsuki", 0.0))),
    P(S("sanchin", "hikite", lerp_side("hikite", "chudan_tsuki", 0.5))),
    P(S("sanchin", "hikite", "chudan_tsuki")),
    P(S("sanchin", "chudan_tsuki", "hikite")),
    P(S("sanchin", lerp_side("chudan_tsuki", "hikite", 0.5), lerp_side("hikite", "chudan_tsuki", 0.5))),
    P(S("sanchin", "hikite", "chudan_tsuki")),
    P(D("sanchin", "grab_pull", "chamber"), A("sanchin", "hikite", ((0.26, -0.12), -1, "fist", 0))),
    P(D("sanchin", "hikite", ((0.27, -0.06), -1, "fist", 0)), A("sanchin", "guard", "hikite", lean=-0.02)),
], cols=4, panel_w=1.15)

# 1.6 floor patterns
pats = [
    [(0, 0), (0.18, 0.15), (-0.18, 0.3), (0.18, 0.45), (0.03, 0.5), (0.03, 0.05)],
    [(0, 0), (0.2, 0.12), (-0.2, 0.26), (0.2, 0.4), (0.02, 0.45), (0.02, 0.05)],
    [(0, 0), (0, 0.45), (0.25, 0.45), (-0.25, 0.48), (0.04, 0.48), (0.04, 0.03)],
    [(0, 0), (0, 0.42), (0.25, 0.42), (-0.25, 0.45), (0.04, 0.45), (0.04, 0.03)],
    [(0, 0), (0.2, 0.18), (-0.2, 0.18), (0.0, 0.32), (0.24, 0.35), (-0.24, 0.38), (0.03, 0.05)],
    [(0, 0), (0.22, 0.1), (-0.22, 0.13), (0, 0.28), (0, 0.5), (0.04, 0.05)],
    [(0, 0), (0, 0.5), (0.04, 0.18), (0.26, 0.18), (-0.26, 0.21), (0.0, 0.03)],
    [(0, 0), (0, 0.45), (0.25, 0.45), (-0.25, 0.48), (0.04, 0.48), (0.2, 0.22), (-0.2, 0.22), (0.02, 0.03)],
]
names = ["Saifa", "Seiyunchin", "Shisochin", "Sanseru", "Sepai", "Kururunfa", "Seisan", "Suparinpei"]
plate("fig1_6", [panel_embusen(p, n, s=1.15) for p, n in zip(pats, names)], cols=4, height=0.85)
print(COUNT)
