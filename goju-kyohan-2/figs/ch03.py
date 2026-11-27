import sys; sys.path.insert(0, '.')
from goju import *

U = 0.16  # one foot-length in panel units
plate("fig3_1", [
    feet_panel([(-0.04, 0, 75, "L"), (0.04, 0, 105, "R")], "musubi dachi"),
    feet_panel([(-0.09, 0, 90, "L"), (0.09, 0, 90, "R")], "heiko dachi"),
    feet_panel([(-0.09, -0.06, 90, "L"), (0.09, 0.1, 125, "R")], "sanchin dachi", lines=[((-0.25, -0.06), (0.25, -0.06))]),
    feet_panel([(-0.1, -0.12, 90, "L"), (0.1, 0.12, 110, "R")], "seisan dachi"),
    feet_panel([(-0.09, -0.2, 70, "L"), (0.09, 0.17, 95, "R")], "zenkutsu dachi"),
    feet_panel([(-0.25, 0, 135, "L"), (0.25, 0, 45, "R")], "shiko dachi", lines=[((-0.25, -0.12), (0.25, -0.12))]),
    feet_panel([(-0.03, -0.1, 55, "L"), (0.02, 0.12, 95, "R", "ghost")], "neko ashi dachi"),
    feet_panel([(0.04, 0.02, 80, "L"), (-0.05, -0.08, 80, "R", "ghost")], "kosa dachi"),
], cols=4, height=0.75)

plate("fig3_2", [
    P(F("sanchin", "sanchin", "sanchin")), P(S("sanchin", "sanchin", "sanchin")),
    P(F("sanchin", "sanchin", "sanchin", knee=-0.05)), P(S("sanchin", "sanchin", "sanchin", drop=-0.03)),
    P(S((0.43, None, (-0.25, 0.12)), "sanchin", "sanchin")), P(F("sanchin", "sanchin", "sanchin", knee=0.03)),
    P(S("sanchin", "sanchin", "sanchin", lean=0.06)), P(S("sanchin", ((0.14, 0.02), -1, "fist", 90), ((0.14, 0.02), -1, "fist", 90), lean=-0.03)),
], cols=4, caption_labels=["correct", "correct", "knees in", "knees locked", "too long", "foot out", "pelvis tipped", "shoulders up"])

def step(feet, arrows_=None, t=None):
    return feet_panel(feet, t, arrows_=arrows_, k=1.1, cy=0.3)
plate("fig3_3", [
    step([(-0.09, -0.08, 90, "L"), (0.09, 0.08, 125, "R")]),
    step([(-0.04, 0.0, 90, "L"), (0.09, 0.08, 125, "R"), (-0.09, -0.08, 90, "L", "ghost")], [((-0.09, -0.02), (-0.04, 0.05), -0.2)]),
    step([(-0.02, 0.12, 95, "L"), (0.09, 0.08, 125, "R"), (-0.04, 0.0, 90, "L", "ghost")], [((-0.04, 0.05), (-0.02, 0.15), 0)]),
    step([(-0.07, 0.22, 70, "L"), (0.09, 0.08, 125, "R"), (-0.02, 0.12, 95, "L", "ghost")], [((-0.02, 0.15), (-0.07, 0.25), 0.3)]),
    step([(-0.09, 0.24, 55, "L"), (0.09, 0.08, 90, "R")]),
    step([(-0.09, 0.24, 55, "L"), (0.09, 0.08, 125, "R"), (-0.24, 0.05, 90, "L", "ghost")], [((-0.09, -0.06), (-0.09, 0.2), 0.8)]),
], cols=3, height=0.82)

plate("fig3_4", [P(S("sanchin", "sanchin", "sanchin")), P(S("seisan", "hikite", "chudan_uke")),
                 P(S("zenkutsu", "hikite", "chudan_tsuki")), P(S((0.39, None, (-0.30, 0.10)), "hikite", "chudan_tsuki", lean=0.05))],
      cols=4, caption_labels=["sanchin dachi", "seisan dachi", "zenkutsu dachi", "knee too far"])

plate("fig3_5", [
    P(F("shiko", "hip", "hip")), P(F("shiko", "hip", "hip", knee=-0.09)), P(F("shiko", "hip", "hip", drop=-0.06)),
    P(S("shiko", "hip", "hip", lean=0.08)), P(F("shiko", "hip", "hip", knee=0.05)),
    P(F((0.37, (-0.30, 0.20), None), "hip", "hip", lean=0.05)), P(F((0.4, (-0.15, 0.15), None), "hip", "hip")),
    P(F("shiko", "hip", "hip", drop=0.02)),
], cols=4, caption_labels=["correct", "knees in", "too high", "leaning (side)", "feet out", "weight on one leg", "too narrow", "the drop"])

plate("fig3_6", [
    P(S("neko", "tora_down", "tora_up")), P(S("neko", "guard", "chamber", kick="chamber")),
    P(S((0.42, None, (-0.12, 0.14)), "tora_down", "tora_up")), P(S("neko", "tora_down", "tora_up", drop=-0.04)),
    P(S("neko", "tora_down", "tora_up", lean=-0.05)), P(F("neko", "tensho_down", "tensho_up", knee=0.04)),
    P(S("sanchin", "tora_down", "tora_up")), P(S("neko", "tora_down", "tora_up")),
], cols=4, caption_labels=["correct", "kick ready", "weight even", "too high", "leaning back", "knee out", "step back...", "...settle"])

plate("fig3_7", [
    P(F("kosa", "hikite", "chudan_uke")), P(S("kosa", "hikite", "chudan_tsuki")),
    P(F("heiko", "hip", "hip")), P(F("kosa", "hip", "hip")),
    P(F("sagi", "hikite", "chudan_uke", kick="knee", front_leg="R")), P(S("sagi", "guard", "chamber", kick="knee")),
    P(S((0.47, None, (-0.01, 0.02)), "guard", "chamber", kick="knee")), P(S("sagi", "gedan_open", "guard", kick="knee")),
], cols=4, caption_labels=["kosa, front", "kosa, side", "start", "cross", "sagi, front", "sagi, side", "straight leg", "knee check"])

def headline(fig, y):
    def fn(ax):
        fig.draw(ax)
        floor(ax, -0.48, 0.48)
        ax.plot([-0.45, 0.45], [y, y], c="black", lw=0.6, ls=(0, (4, 3)))
    return fn
hy = STANCES["sanchin"][0] + TORSO + NECK + HEAD_R * 2
plate("fig3_8", [
    headline(S("sanchin", "hikite", "chudan_uke"), hy), headline(S("heiko", "hikite", "chudan_uke", drop=-0.03), hy),
    headline(S("sanchin", "hikite", "chudan_tsuki"), hy),
    headline(S("sanchin", "hikite", "chudan_uke"), hy), headline(S("musubi", "hikite", "chudan_uke", drop=0.025), hy),
    headline(S("sanchin", "hikite", "chudan_tsuki"), hy),
    P(S("musubi", "hikite", "chudan_tsuki", drop=0.02)), P(S("sanchin", "hikite", "chudan_tsuki")),
], cols=4)

plate("fig3_9", [
    step([(-0.09, -0.08, 90, "L"), (0.09, 0.08, 125, "R")], [((0.0, 0.18), (0.0, 0.3))]),
    step([(-0.09, -0.08, 90, "L"), (0.09, 0.08, 125, "R")], [((0.0, 0.18), (0.12, 0.26), -0.3)]),
    step([(0.0, -0.18, 30, "L"), (0.09, 0.08, 125, "R"), (-0.09, -0.08, 90, "L", "ghost")], [((-0.09, -0.12), (0.0, -0.22), 0.4)]),
    step([(0.06, -0.2, -60, "L"), (0.09, 0.08, -80, "R")]),
    step([(0.1, -0.22, -90, "L"), (-0.06, 0.02, -55, "R")], [((0.0, -0.02), (0.0, -0.15))]),
    step([(0.1, -0.22, -90, "L", "filled"), (-0.06, 0.02, -55, "R", "filled")]),
], cols=3, height=0.82, caption_labels=["start", "look", "step across", "pivot", "new stance", "fault: heels"])
print(COUNT)
