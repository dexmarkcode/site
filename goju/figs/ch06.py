from figlib import *

@titled("Short strike to the face")
def r1(ax):
    a = stance(-0.42, 1, "A", lean=8); a.hands["near"] = (0.32, 1.72); a.draw(ax)
    b = stance(0.5, -1, "B", lean=-2); b.hands["near"] = (0.2, 1.45); b.hands["far"] = (0.25, 1.35); b.draw(ax)
    impact(ax, 0.4, 1.74)
@titled("Flinch: head back, hands up")
def r2(ax):
    a = stance(-0.42, 1, "A", lean=6); a.hands["near"] = (0.05, 1.55); a.draw(ax)
    b = stance(0.55, -1, "B", lean=-16); b.hands["near"] = (0.38, 1.78); b.hands["far"] = (0.42, 1.72); b.draw(ax)
    arrow(ax, (0.6, 1.95), (0.85, 1.85), dashed=True)
@titled("Pin the arms, strike the ribs")
def r3(ax):
    a = stance(-0.35, 1, "A", lean=12); a.hands["near"] = (0.38, 1.6); a.hands["far"] = (0.35, 1.2); a.open_hand = ("near",); a.draw(ax)
    b = stance(0.55, -1, "B", lean=-12); b.hands["near"] = (0.42, 1.68); b.hands["far"] = (0.45, 1.62); b.draw(ax)
    impact(ax, 0.42, 1.18)
sequence("fig6_1", [r1, r2, r3], cols=3)

@titled("Straight punch is blocked")
def s1(ax):
    a = stance(-0.45, 1, "A", lean=8); a.hands["far"] = (0.3, 1.68); a.draw(ax)
    b = stance(0.48, -1, "B"); b.hands["near"] = (0.2, 1.68); b.draw(ax)
@titled("Pass the arm, pivot outside")
def s2(ax):
    a = stance(-0.3, 1, "A", lean=6); a.hands["near"] = (0.12, 1.5); a.open_hand = ("near",); a.draw(ax)
    b = stance(0.5, -1, "B", lean=4); b.hands["near"] = (0.0, 1.45); b.draw(ax)
    arrow(ax, (-0.75, 0.3), (-0.4, 0.42), rad=-0.4)
@titled("Elbow from the outside")
def s3(ax):
    a = stance(-0.2, 1, "A", lean=14); a.hands["far"] = (0.18, 1.78); a.elbow["far"] = 1
    a.hands["near"] = (0.2, 1.42); a.open_hand = ("near",); a.draw(ax)
    b = stance(0.5, -1, "B", lean=-6); b.hands["near"] = (0.15, 1.38); b.draw(ax)
    impact(ax, 0.38, 1.8)
sequence("fig6_2", [s1, s2, s3], cols=3)

def strike(title, near, opener=None, elbow=-1, mark=None, b_mod=None):
    @titled(title)
    def p(ax):
        a = stance(-0.42, 1, "A", lean=8); a.hands["near"] = near; a.elbow["near"] = elbow
        if opener: opener(a)
        a.draw(ax)
        b = stance(0.48, -1, "B")
        if b_mod: b_mod(b)
        b.draw(ax)
        if mark: impact(ax, *mark)
    return p
def palm(a): a.open_hand = ("near",)
def hammer_b(b): b.lean = 22
sequence("fig6_3", [strike("Back fist", (0.33, 1.82), mark=(0.4, 1.82)),
                    strike("Palm heel", (0.3, 1.72), palm, mark=(0.38, 1.72)),
                    strike("Hammer fist", (0.15, 1.45), elbow=1, mark=(0.18, 1.42), b_mod=hammer_b),
                    strike("Short hook", (0.32, 1.8), elbow=1, mark=(0.4, 1.8))], cols=4, width=4.6)
