from figlib import *

def clinch_pair(ax, knee=False, alean=10):
    hx = -0.38
    feet = {"near": (hx + 0.25, 0.06), "far": (hx - 0.25, 0.06)}
    if knee:
        feet = {"near": (hx + 0.32, 0.55), "far": (hx - 0.1, 0.09)}
    a = Person(hip=(hx + (0.05 if knee else 0), 0.9), face=1, lean=alean,
               hands={"near": (0.12, 1.68), "far": (0.08, 1.62)}, feet=feet, toes={"near": -55 if knee else 0, "far": 0})
    a.draw(ax)
    b = Person(hip=(0.36, 0.88), face=-1, lean=16 if knee else 8, hands={"near": (-0.05, 1.42), "far": (-0.02, 1.36)},
               feet={"near": (0.12, 0.06), "far": (0.62, 0.06)}, style="B")
    b.draw(ax)
@titled("Hands behind the neck")
def k1(ax):
    clinch_pair(ax)
@titled("Hips drive, knee rises, pull")
def k2(ax):
    clinch_pair(ax, True, alean=4)
    impact(ax, 0.1, 1.0); arrow(ax, (-0.55, 0.45), (-0.15, 0.85), rad=-0.3)
    arrow(ax, (0.45, 1.9), (0.1, 1.85))
sequence("fig8_1", [k1, k2], cols=2)

def leg(title, foot, toes, knee=1, mark=None, lean=0, hip=(-0.4, 0.88), b_lean=4):
    @titled(title)
    def p(ax):
        a = Person(hip=hip, face=1, lean=lean, hands={"near": (hip[0] + 0.38, 1.6), "far": (hip[0] + 0.25, 1.52)},
                   feet={"near": foot, "far": (hip[0] - 0.22, 0.06)}, toes={"near": toes, "far": 0}, knee={"near": knee, "far": 1})
        a.draw(ax)
        stance(0.48, -1, "B", lean=b_lean).draw(ax)
        if mark: impact(ax, *mark)
    return p
sequence("fig8_2", [leg("Low front kick", (0.08, 0.35), 20, mark=(0.22, 0.38), lean=-8),
                    leg("Stamp to the knee", (0.1, 0.32), -10, mark=(0.25, 0.45), lean=-5),
                    leg("Shin kick to the thigh", (0.2, 0.62), 0, knee=1, mark=(0.28, 0.62), lean=-10),
                    leg("Stamp on the instep", (0.12, 0.1), 0, mark=(0.22, 0.12), lean=4)], cols=4, width=4.6)

@titled("Hip jam")
def d1(ax):
    a = stance(-0.45, 1, "A", lean=6); a.hands["near"] = (0.1, 0.98); a.open_hand = ("near",); a.draw(ax)
    b = Person(hip=(0.38, 0.9), face=-1, lean=4, hands={"near": (-0.05, 1.6), "far": (-0.02, 1.55)},
               feet={"near": (0.12, 0.3), "far": (0.6, 0.06)}, style="B"); b.draw(ax)
    arrow(ax, (-0.2, 0.8), (0.18, 0.92))
@titled("Elbow drop")
def d2(ax):
    a = stance(-0.42, 1, "A", lean=12); a.hands["near"] = (-0.1, 1.42); a.epos = {"near": (0.0, 0.95)}; a.draw(ax)
    b = Person(hip=(0.38, 0.9), face=-1, lean=4, hands={"near": (-0.08, 1.6), "far": (-0.02, 1.55)},
               feet={"near": (0.0, 0.45), "far": (0.62, 0.06)}, style="B"); b.draw(ax)
    impact(ax, -0.05, 0.98, r=0.07)
@titled("Leg check")
def d3(ax):
    a = Person(hip=(-0.42, 0.9), face=1, lean=2, hands={"near": (-0.05, 1.62), "far": (-0.1, 1.58)},
               feet={"near": (-0.12, 0.45), "far": (-0.6, 0.06)}); a.draw(ax)
    b = Person(hip=(0.42, 0.9), face=-1, lean=-6, hands={"near": (0.1, 1.6), "far": (0.15, 1.55)},
               feet={"near": (-0.1, 0.5), "far": (0.6, 0.06)}, style="B"); b.draw(ax)
    impact(ax, -0.08, 0.42, r=0.07)
sequence("fig8_3", [d1, d2, d3], cols=3)
