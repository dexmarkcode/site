import sys; sys.path.insert(0, '.')
from goju import *

punch = ((0.3, -0.02), -1, "fist", 0)
plate("fig18_1", [
    P(D("sanchin", "guard", "guard", x=-0.36), A("zenkutsu", "hikite", punch, x=0.4)),
    P(D("sanchin", "guard", "guard"), A("zenkutsu", "hikite", punch, x=0.3)),
    P(D("sanchin", "guard", "guard"), A("zenkutsu", "hikite", ((0.28, 0.12), -1, "fist", 20), x=0.3)),
    P(D("sanchin", "guard", "guard"), A("zenkutsu", "hikite", ((0.3, -0.04), -1, "fist", 0), x=0.3)),
    P(D("sanchin", "guard", ((0.2, -0.04), -1, "claw", 0)), A("shiko", "guard", "guard", x=0.3, lean=-0.1, drop=0.1)),
    P(D("shiko", ((0.06, -0.18), +1, "claw", 0), ((0.2, -0.2), -1, "fist", -70), drop=0.04), A("zenkutsu", "hikite", ((0.3, -0.26), -1, "open", -40), x=0.24, lean=0.2, drop=0.05)),
    P(D("shiko", ((0.08, -0.14), +1, "claw", 0), ((0.22, -0.1), -1, "fist", 90)), A("shiko", "guard", ((0.3, -0.14), -1, "fist", 0), x=0.3, lean=-0.06)),
    P(D("shiko", ((0.08, -0.14), +1, "claw", 0), ((0.22, -0.1), -1, "fist", 90)), A("zenkutsu", "hikite", ((0.34, -0.14), -1, "open", -20), x=0.28, lean=0.05)),
], cols=4, panel_w=1.25, caption_labels=["fault", "correct", "fault", "correct", "fault", "correct", "fault", "correct"])

cover = ((0.04, -0.24), +1, "fist", 0)
plate("fig18_2", [
    P(D("heiko", "hip", ((0.12, -0.18), -1, "fist", 0)), A("sanchin", "hikite", ((0.24, -0.19), -1, "claw", 180))),
    P(D("musubi", cover, cover), A("zenkutsu", "hikite", ((0.32, -0.24), -1, "claw", 180), x=0.25, lean=0.05)),
    P(D("shiko", ((0.1, -0.06), +1, "open", 0), ((0.22, 0.04), +1, "fist", 180), drop=0.02), A("sanchin", "hikite", "guard", x=0.3, lean=-0.05)),
    P(D("sanchin", "guard", "guard"), A("zenkutsu", ((0.3, 0.0), -1, "fist", 0), "hikite", x=0.3)),
    P(D("seisan", ((0.26, -0.14), -1, "open", -20), "chamber"), A("zenkutsu", ((0.22, -0.16), -1, "fist", 0), "hikite", x=0.3, lean=0.06)),
    P(D("seisan", ((0.26, -0.16), -1, "open", -20), "uraken"), A("zenkutsu", ((0.22, -0.18), -1, "fist", 0), "hikite", x=0.3, lean=0.06)),
    P(D("heiko", ((0.18, -0.02), -1, "claw", 0), ((0.05, 0.06), -1, "fist", 90)), A("sanchin", "hikite", ((0.28, -0.02), -1, "claw", 180), lean=0.03)),
    P(D("shiko", ((0.05, -0.14), +1, "fist", 0), ((0.22, -0.1), -1, "fist", -70), drop=0.02), A("zenkutsu", "hikite", ((0.32, -0.16), -1, "open", 180), lean=0.09, x=0.26)),
], cols=4, panel_w=1.25)

og = ((0.14, -0.01), -1, "open", 90)
plate("fig18_3", [
    P(D("sanchin", og, og), A("sanchin", "hikite", punch, x=0.3)),
    P(D("sanchin", "hip", ((0.22, 0.0), -1, "open", 110)), A("sanchin", "hikite", punch, x=0.3)),
    P(D("sanchin", og, "grab_pull"), A("zenkutsu", "hikite", ((0.32, -0.1), -1, "fist", 0), x=0.28, lean=0.06)),
    P(D("sanchin", "nukite", "grab_pull"), A("zenkutsu", "guard", ((0.3, -0.1), -1, "fist", 0), x=0.3, lean=0.03)),
    P(D("sanchin", "nukite", og), A("sanchin", "hikite", ((0.22, 0.0), -1, "open", 110), x=0.3)),
    P(D("zenkutsu", ((0.32, -0.1), -1, "fist", 0), "hikite", lean=0.06, x=-0.28), A("sanchin", "grab_pull", og, x=0.3)),
    P(D("sanchin", "guard", og), A("sanchin", "grab_pull", "nukite", x=0.3)),
    P(D("sanchin", "hip", ((0.22, 0.0), -1, "open", 110)), A("sanchin", og, "nukite", x=0.3)),
], cols=4, panel_w=1.25)

def mitt(ax, J, key, dx=0.03):
    p = J[key]
    ax.add_patch(Ellipse((p[0] + dx, p[1]), 0.05, 0.1, fc="white", ec="black", lw=0.9, zorder=8))
def shield(ax, x, y0, y1, w=0.05):
    ax.add_patch(MPoly([(x, y0), (x + w, y0), (x + w, y1), (x, y1)], fc="white", ec="black", lw=0.9, zorder=8))
def holder(stance="sanchin", right=((0.12, 0.0), -1, "open", 90), left="guard", x=0.3, **kw):
    return Figure(stance, "side", left, right, x=x, facing=-1, partner=True, **kw)
def padpanel(d, a, tool):
    def fn(ax):
        J1 = d.draw(ax)
        J2 = a.draw(ax) if a else None
        floor(ax, -0.6, 0.6)
        tool(ax, J1, J2)
    return fn
plate("fig18_4", [
    padpanel(D("sanchin", "guard", "uraken"), holder(right=((0.16, 0.06), -1, "open", 90)), lambda ax, a, b: mitt(ax, b, "handF", -0.02)),
    padpanel(D("sanchin", "guard", "shotei"), holder(right=((0.16, -0.04), -1, "open", 90)), lambda ax, a, b: mitt(ax, b, "handF", -0.02)),
    padpanel(D("sanchin", "guard", "guard", kick="knee"), holder(right=((0.12, -0.18), -1, "open", 90), left=((0.12, -0.18), -1, "open", 90)), lambda ax, a, b: shield(ax, b["hip"][0] - 0.14, 0.32, 0.52)),
    padpanel(D("sanchin", "guard", "guard", kick="kansetsu"), holder(right=((0.12, -0.3), -1, "open", 90), left=((0.12, -0.3), -1, "open", 90), drop=0.02), lambda ax, a, b: shield(ax, b["hip"][0] - 0.14, 0.08, 0.3)),
    padpanel(D("shiko", "hikite", ((0.12, 0.0), +1, "fist", 180), x=-0.15), None, lambda ax, a, b: shield(ax, 0.08, 0.2, 0.85, w=0.14)),
    padpanel(D("shiko", "hikite", ((0.22, -0.14), -1, "fist", -70), x=-0.2), None, lambda ax, a, b: shield(ax, 0.08, 0.2, 0.85, w=0.14)),
    padpanel(D("sanchin", "shotei", "shotei"), holder(right=((0.08, -0.08), -1, "open", 90), left=((0.08, -0.08), -1, "open", 90)), lambda ax, a, b: shield(ax, b["sh"][0] - 0.13, b["sh"][1] - 0.22, b["sh"][1] + 0.02)),
    padpanel(D("sanchin", ((0.2, -0.04), -1, "claw", 0), ((0.26, 0.04), -1, "fist", 30)), holder(right=((0.2, -0.04), -1, "fist", 0), left=((0.14, 0.06), -1, "open", 90)), lambda ax, a, b: mitt(ax, b, "handB", -0.02)),
], cols=4, panel_w=1.25)

lapel = ((0.24, -0.02), -1, "claw", 180)
plate("fig18_5", [
    P(D("heiko", "guard", "guard"), A("sanchin", ((0.06, 0.06), -1, "fist", 90), lapel, x=0.26)),
    P(D("heiko", "guard", "guard", lean=-0.04), A("zenkutsu", lapel, lapel, x=0.24, lean=0.06)),
    P(D("heiko", "hip", ((0.12, -0.18), -1, "fist", 0)), A("kokutsu", "hikite", ((0.26, -0.2), -1, "claw", 180), x=0.3, lean=-0.04)),
    P(Figure("sanchin", "side", ((0.24, -0.06), -1, "claw", 0), ((0.24, -0.06), -1, "claw", 0), x=-0.18, facing=1, partner=True), S("heiko", "guard", "guard", x=0.1)),
    P(D("heiko", "guard", "guard", lean=0.06), A("sanchin", ((0.18, 0.12), -1, "claw", 150), ((0.22, 0.02), -1, "claw", 180), x=0.22)),
    P(lambda: None) if False else (lambda ax: (ax.plot([-0.42, -0.42], [0, 0.95], c="black", lw=1.6), D("heiko", "guard", "guard", x=-0.3, lean=-0.03).draw(ax), A("zenkutsu", "shotei", "shotei", x=0.2, lean=0.06).draw(ax), floor(ax, -0.6, 0.6))),
    P(D("sanchin", "guard", "guard"), A("zenkutsu", "hikite", ((0.2, 0.08), +1, "fist", 180), x=0.3)),
    P(D("sanchin", "guard", "guard"), A("zenkutsu", ((0.24, -0.16), -1, "open", -30), ((0.24, -0.16), -1, "open", -30), x=0.22, lean=0.2, drop=0.06)),
], cols=4, panel_w=1.25)
print(COUNT)
