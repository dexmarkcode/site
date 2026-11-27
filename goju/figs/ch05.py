from figlib import *

@titled("Contact on the forearm")
def a1(ax):
    a = stance(-0.45, 1, "A", lean=6); a.hands["near"] = (0.05, 1.5); a.open_hand = ("near",); a.draw(ax)
    b = stance(0.45, -1, "B"); b.hands["near"] = (0.02, 1.48); b.draw(ax)
@titled("Press the arm into their body")
def a2(ax):
    a = stance(-0.4, 1, "A", lean=10); a.hands["near"] = (0.3, 1.32); a.open_hand = ("near",); a.draw(ax)
    b = stance(0.48, -1, "B", lean=-4); b.hands["near"] = (0.32, 1.38); b.hands["far"] = (0.3, 1.58); b.draw(ax)
    arrow(ax, (-0.05, 1.1), (0.28, 1.2))
@titled("Strike over the pin")
def a3(ax):
    a = stance(-0.32, 1, "A", lean=12); a.hands["near"] = (0.32, 1.3); a.hands["far"] = (0.4, 1.75); a.open_hand = ("near",); a.draw(ax)
    b = stance(0.52, -1, "B", lean=-10); b.hands["near"] = (0.38, 1.38); b.hands["far"] = (0.36, 1.55); b.draw(ax)
    impact(ax, 0.45, 1.8)
sequence("fig5_1", [a1, a2, a3], cols=3)

@titled("Hook the wrist and pull to the hip")
def h1(ax):
    a = stance(-0.5, 1, "A", lean=2)
    a.hands["near"] = (-0.32, 1.08); a.hands["far"] = (0.15, 1.62); a.draw(ax)
    b = Person(hip=(0.3, 0.88), face=-1, lean=22, hands={"near": (-0.28, 1.1), "far": (0.0, 1.5)},
               feet={"near": (0.0, 0.06), "far": (0.65, 0.06)}, style="B")
    b.draw(ax)
    arrow(ax, (0.05, 0.85), (-0.35, 0.85))
    ax.text(-0.15, 0.72, "hikite", fontsize=6.5, ha="center", style="italic")
    impact(ax, 0.2, 1.62)
    arrow(ax, (0.75, 1.3), (0.45, 1.3), dashed=True)
    ax.text(0.85, 1.2, "drawn\nforward", fontsize=6, ha="center")
sequence("fig5_2", [h1], cols=1, width=3.6)

@titled("Cross trap from the outside line")
def x1(ax):
    top_person(ax, 0, 0.45, 270, "B", lhand=(-0.2, 0.18), rhand=(-0.1, 0.12))
    top_person(ax, 0.42, -0.12, 135, "A", lhand=(0.22, 0.22), rhand=(0.12, 0.08))
    arrow(ax, (0.42, 0.22), (-0.05, 0.2), rad=0.2)
    ax.text(-0.55, -0.5, "lead arm lies over\nrear arm: both tied up", fontsize=6.5, ha="center")
    arrow(ax, (-0.45, -0.35), (-0.18, 0.08), lw=0.8, dashed=True)
plan_panels("fig5_3", [x1], width=3.0, lim=0.85)
