import sys; sys.path.insert(0, '.')
from goju import *

seq = [lerp_side("hikite", "chudan_tsuki", t) for t in (0.0, 0.3, 0.55, 0.75, 0.9, 1.0)]
plate("fig2_1", [P(S("sanchin", "hikite", a)) for a in seq] +
      [P(S("sanchin", "hikite", lerp_side("chudan_tsuki", "hikite", 0.4))), P(S("sanchin", "hikite", "hikite"))], cols=4)

def ground_path(fig, keys):
    def fn(ax):
        J = fig.draw(ax)
        floor(ax, -0.48, 0.48)
        pts = [J[k] for k in keys]
        for a, b in zip(pts, pts[1:]):
            arrow(ax, (a[0] + 0.0, a[1]), (b[0], b[1]), lw=1.1, ls=(0, (3, 1.5)))
    return fn

plate("fig2_2", [
    ground_path(S("sanchin", "hikite", "chudan_tsuki"), ["footB", "kneeB", "hip", "sh", "elbowF", "handF"]),
    ground_path(S("sanchin", "shotei", "shotei"), ["footB", "kneeB", "hip", "sh", "handF"]),
    ground_path(F("shiko", "hikite", "kentsui"), ["footR", "kneeR", "hipR", "shR", "elbowR", "handR"]),
    ground_path(S("zenkutsu", "hikite", ((0.12, 0.10), +1, "fist", 180)), ["footB", "kneeB", "hip", "sh", "elbowF"]),
], cols=4)

def withline(fig, y=None):
    def fn(ax):
        fig.draw(ax)
        floor(ax, -0.48, 0.48)
        if y is not None:
            ax.plot([-0.45, 0.45], [y, y], c="black", lw=0.6, ls=(0, (4, 3)))
    return fn

plate("fig2_3", [
    P(S("sanchin", "hip", "hip", lean=0.06)), P(S("sanchin", "hip", "hip", lean=-0.06)), P(S("sanchin", "hip", "hip")),
    P(S("sanchin", "hikite", "chudan_tsuki", lean=0.07)), P(S("sanchin", "hikite", "chudan_tsuki", lean=-0.06)), P(S("sanchin", "hikite", "chudan_tsuki")),
], cols=3, caption_labels=["arched", "tucked", "neutral", "arched", "tucked", "neutral"])

hh = STANCES["shiko"][0] + TORSO
plate("fig2_4", [
    withline(F("shiko", "hikite", "uraken"), hh + 0.0),
    withline(F("shiko", "hikite", ((0.07, -0.03), (0.04, -0.06), "fist", -90), drop=0.01), hh),
    withline(F("shiko", "hikite", ((0.05, -0.11), (0.01, -0.19), "fist", -90), drop=0.025), hh),
    withline(F("shiko", "hikite", "kentsui", drop=0.04), hh),
    withline(S("sanchin", "hikite", ((0.20, -0.06), -1, "fist", 0)), STANCES["sanchin"][0]),
    withline(S("sanchin", "hikite", ((0.25, -0.06), -1, "fist", 0), drop=0.008), STANCES["sanchin"][0]),
    withline(S("sanchin", "hikite", ((0.29, -0.06), -1, "fist", 0), drop=0.018), STANCES["sanchin"][0]),
    withline(S("sanchin", "hikite", "chudan_tsuki", drop=0.025), STANCES["sanchin"][0]),
], cols=4)

plate("fig2_5", [
    P(D("neko", "hip", "guard"), A("zenkutsu", "hikite", ((0.30, -0.02), -1, "fist", 0))),
    P(D("neko", "hip", ((0.20, -0.02), -1, "open", 70)), A("zenkutsu", "hikite", ((0.30, -0.04), -1, "fist", 0))),
    P(D("neko", "hip", ((0.20, -0.08), -1, "open", 40)), A("zenkutsu", "hikite", ((0.28, -0.08), -1, "fist", 0))),
    P(D("neko", "guard", ((0.18, -0.14), -1, "open", 0)), A("zenkutsu", "hikite", ((0.26, -0.16), -1, "fist", -10), lean=-0.02)),
    P(D("sanchin", ((0.20, -0.14), -1, "open", 0), ((0.10, -0.06), -1, "fist", 90)), A("zenkutsu", "hikite", ((0.26, -0.16), -1, "fist", -10), lean=-0.03)),
    P(D("sanchin", ((0.20, -0.16), -1, "open", 0), "jodan_tsuki"), A("zenkutsu", "hikite", ((0.24, -0.18), -1, "fist", -10), lean=-0.03)),
    P(D("neko", "hip", ((0.22, 0.04), -1, "open", 110)), A("zenkutsu", "hikite", ((0.30, -0.02), -1, "fist", 0))),
    P(D("neko", "hip", "hip", lean=-0.03), A("zenkutsu", ((0.32, 0.02), -1, "fist", 0), "hikite")),
], cols=4, panel_w=1.3)

def breath(fig, out=True):
    def fn(ax):
        J = fig.draw(ax)
        floor(ax, -0.48, 0.48)
        h = J["hip"]
        y = h[1] + 0.09
        x = h[0] + 0.09
        if out:
            arrow(ax, (x + 0.09, y), (x + 0.01, y), lw=1.0)
        else:
            arrow(ax, (x + 0.0, y), (x + 0.08, y), lw=1.0)
        hd = J["head"]
        if out:
            arrow(ax, (hd[0] + 0.06, hd[1] - 0.03), (hd[0] + 0.16, hd[1] - 0.05), lw=0.8, ls=(0, (2, 1.5)))
        else:
            arrow(ax, (hd[0] + 0.16, hd[1]), (hd[0] + 0.07, hd[1] - 0.005), lw=0.8, ls=(0, (2, 1.5)))
    return fn

plate("fig2_6", [breath(S("sanchin", "sanchin", "sanchin"), out=False), breath(S("sanchin", "sanchin", "sanchin", drop=0.01), out=True),
                 breath(S("sanchin", "tensho_up", "tensho_up"), out=False), breath(S("sanchin", "tensho_down", "tensho_up"), out=True)], cols=4,
      caption_labels=["ibuki: in", "ibuki: out", "nogare: in", "nogare: out"])
print(COUNT)
