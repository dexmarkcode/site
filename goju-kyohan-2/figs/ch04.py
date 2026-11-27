import sys; sys.path.insert(0, '.')
from goju import *

plate("fig4_1", [
    P(F("heiko", "yoi_open", "yoi_open")),
    P(F("sanchin", lerp_arm("yoi_open", "sanchin", 0.5), lerp_arm("yoi_open", "sanchin", 0.5))),
    P(F("sanchin", "sanchin", "sanchin")),
    P(F("sanchin", "hikite", "sanchin")),
    P(F("sanchin", lerp_arm("hikite", "chudan_tsuki", 0.5), "sanchin")),
    P(F("sanchin", "chudan_tsuki", "sanchin")),
    P(F("sanchin", "sanchin", "sanchin")),
    P(F("heiko", "sanchin", "sanchin", drop=0.01)),
], cols=4)

plate("fig4_2", [
    P(S("sanchin", "sanchin", "sanchin")),
    P(S("sanchin", "hikite", ((-0.02, -0.22), +1, "open", -90))),
    P(S("sanchin", "hikite", ((0.12, -0.12), -1, "nukite", 20))),
    P(S("sanchin", "nukite", "nukite")),
    P(S("sanchin", ((0.25, -0.02), -1, "open", 60), ((0.25, -0.02), -1, "open", 60))),
    P(S("sanchin", "hikite", "hikite")),
    P(S("sanchin", "shotei", "shotei")),
    P(S("neko", "tora_down", "tora_up")),
], cols=4)

plate("fig4_3", [
    marked(F("sanchin", "sanchin", "sanchin"), [("shL", (0.000, 0.180), (0, 0.03)), ("shR", (0.000, 0.180), (0, 0.03)),
           ("elbowL", (0.180, 0.075), (0.04, 0.05)), ("kneeR", (-0.210, 0.060), (-0.05, 0.02)), ("kneeL", (0.150, 0.150), (0.04, 0.03))]),
    marked(S("sanchin", "sanchin", "sanchin"), [("sh", (-0.240, -0.090), (-0.07, -0.06)), ("hip", (0.330, 0.120), (0.1, 0.08)),
           ("hip", (0.300, -0.015), (0.09, -0.01)), ("kneeF", (0.195, 0.045), (0.05, 0.02))]),
    marked(F("sanchin", "sanchin", "sanchin", back=True), [("shL", (0.000, 0.180), (0, 0.03)), ("shR", (0.000, 0.180), (0, 0.03)),
           ("hipL", (0.210, -0.060), (0.06, -0.04)), ("kneeR", (-0.210, 0.090), (-0.05, 0.04))]),
    marked(S("sanchin", "sanchin", "sanchin"), [("hip", (0.300, 0.000), (0.08, 0.0)), ("hip", (-0.330, 0.000), (-0.1, 0.0))]),
], cols=4, caption_labels=["front", "side", "rear", "stance"])

# tester stands behind (left) the performer, both facing right
def tester(right, left="hip", x=-0.27, stance="heiko", lean=0.0):
    return Figure(stance=stance, view="side", left=left, right=right, x=x, facing=1, partner=True, lean=lean)
perf = lambda: S("sanchin", "sanchin", "sanchin", x=0.08)
plate("fig4_4", [
    P(tester(((0.33, 0.01), -1, "open", -10), "guard"), perf()),
    P(tester(((0.30, -0.06), -1, "open", -80), ((0.30, -0.06), -1, "open", -80)), perf()),
    P(tester(((0.33, 0.03), -1, "open", -80), ((0.33, 0.03), -1, "open", -80), stance="sanchin", x=-0.3), perf()),
    P(Figure("sanchin", "side", ((0.18, -0.05), -1, "open", 90), ((0.18, -0.05), -1, "open", 90), x=0.36, facing=-1, partner=True), S("sanchin", "sanchin", "sanchin", x=-0.12)),
    P(tester(((0.24, 0.10), -1, "open", 120), "guard"), perf()),
    P(tester(((0.30, -0.06), -1, "open", -40), "guard", stance="sanchin"), perf()),
    P(Figure("sanchin", "side", "hikite", ((0.24, -0.02), -1, "fist", 90), x=0.36, facing=-1, partner=True), S("sanchin", "sanchin", "sanchin", x=-0.12)),
    P(Figure("sanchin", "side", "hikite", ((0.26, -0.24), -1, "fist", -40), x=0.36, facing=-1, partner=True, lean=-0.03), S("sanchin", "sanchin", "sanchin", x=-0.12)),
], cols=4, panel_w=1.2)

up = ((0.14, 0.03), -1, "fist", 90)
plate("fig4_5", [
    P(S("sanchin", up, up)), P(S("sanchin", "sanchin", "sanchin")),
    P(S("sanchin", "sanchin", "sanchin", lean=-0.05)), P(S("sanchin", "sanchin", "sanchin")),
    P(F("sanchin", ((0.09, -0.15), (-0.02, -0.03), "fist", 100), ((0.09, -0.15), (-0.02, -0.03), "fist", 100))), P(F("sanchin", "sanchin", "sanchin")),
    P(S("sanchin", "hikite", ((0.31, -0.06), -1, "fist", -25))),
    P(S("sanchin", "hikite", "chudan_tsuki")),
], cols=4, caption_labels=["shoulders up", "corrected", "chest out", "corrected", "elbows out", "corrected", "bent wrist", "straight"])

plate("fig4_6", [
    P(S("sanchin", "sanchin", "sanchin")), P(S("sanchin", "sanchin", "sanchin")),
    P(F("heiko", "sanchin", "sanchin", knee=-0.02)), P(F("musubi", "sanchin", "sanchin", back=True)),
    P(S("sanchin", "sanchin", "sanchin", facing=-1)),
    P(S("sanchin", up, ((0.2, 0.0), -1, "fist", 70), facing=-1)), P(S("sanchin", "sanchin", "sanchin", facing=-1, drop=-0.04)),
    P(S("sanchin", "sanchin", "sanchin", facing=-1, x=0.08), Figure("heiko", "side", ((0.30, 0.02), -1, "open", -80), ((0.30, 0.02), -1, "open", -80), x=0.38, facing=-1, partner=True)),
], cols=4, panel_w=1.1)

def wall(fig, xw):
    def fn(ax):
        fig.draw(ax)
        floor(ax, -0.5, 0.5)
        ax.plot([xw, xw], [0, 0.95], c="black", lw=1.6)
        for y in range(0, 95, 6):
            ax.plot([xw, xw - 0.03], [y / 100, y / 100 - 0.03], c="black", lw=0.5)
    return fn
def mirror(fig):
    def fn(ax):
        fig.draw(ax)
        floor(ax, -0.5, 0.5)
        ax.add_patch(MPoly([(0.32, 0.1), (0.42, 0.1), (0.42, 0.95), (0.32, 0.95)], fc="white", ec="black", lw=1.0))
        for k in range(3):
            ax.plot([0.34 + k * 0.025, 0.37 + k * 0.025], [0.6 + k * 0.05, 0.68 + k * 0.05], c="black", lw=0.5)
    return fn
plate("fig4_7", [
    mirror(S("sanchin", "sanchin", "sanchin", x=-0.1)),
    wall(S("sanchin", "hikite", "chudan_tsuki", x=-0.05), -0.2),
    wall(F("sanchin", ((0.16, -0.15), (0.17, -0.02), "fist", 90), ((0.16, -0.15), (0.17, -0.02), "fist", 90)), 0.33),
    P(S("sanchin", "sanchin", ((0.02, -0.08), +1, "open", 90))),
], cols=4)
print(COUNT)
