from figlib import *

# 11.1 outer reap
@titled("Push the head back")
def o1(ax):
    a = stance(-0.3, 1, "A", lean=12); a.hands["near"] = (0.52, 1.6); a.open_hand = ("near",); a.hands["far"] = (0.18, 1.22); a.draw(ax)
    b = Person(hip=(0.45, 0.88), face=-1, lean=-14, hands={"near": (0.15, 1.25), "far": (0.25, 1.45)},
               feet={"near": (0.25, 0.06), "far": (0.7, 0.06)}, style="B"); b.draw(ax)
    arrow(ax, (0.3, 1.88), (0.75, 1.92), rad=-0.2)
@titled("Step in beside the leg")
def o2(ax):
    a = Person(hip=(0.05, 0.88), face=1, lean=16, hands={"near": (0.62, 1.58), "far": (0.42, 1.2)},
               feet={"near": (0.22, 0.06), "far": (-0.3, 0.2)}, open_hand=("near",)); a.draw(ax)
    b = Person(hip=(0.5, 0.86), face=-1, lean=-18, hands={"near": (0.2, 1.25), "far": (0.32, 1.42)},
               feet={"near": (0.4, 0.06), "far": (0.75, 0.06)}, style="B"); b.draw(ax)
@titled("Reap the leg, drive down")
def o3(ax):
    b = Person(hip=(0.55, 0.62), face=-1, lean=-62, hands={"near": (0.45, 1.05), "far": (0.6, 1.1)},
               feet={"near": (0.05, 0.55), "far": (0.85, 0.06)}, style="B"); b.draw(ax)
    a = Person(hip=(0.1, 0.9), face=1, lean=34, hands={"near": (0.85, 1.12), "far": (0.6, 1.0)},
               feet={"near": (0.3, 0.06), "far": (0.42, 0.45)}, knee={"near": 1, "far": -1}, open_hand=("near",)); a.draw(ax)
    arrow(ax, (-0.3, 0.3), (0.3, 0.55), rad=0.3)
    arrow(ax, (0.9, 1.6), (1.1, 1.2), rad=-0.3)
sequence("fig11_1", [o1, o2, o3], cols=3, xlim=(-1.0, 1.25))

# 11.2 shoulder wheel
@titled("Pull the arm up")
def s1(ax):
    a = stance(-0.45, 1, "A", lean=4); a.hands["near"] = (-0.05, 1.7); a.draw(ax)
    b = Person(hip=(0.42, 0.9), face=-1, lean=12, hands={"near": (-0.05, 1.72), "far": (0.15, 1.45)},
               feet={"near": (0.2, 0.06), "far": (0.65, 0.06)}, style="B"); b.draw(ax)
    arrow(ax, (-0.2, 1.95), (-0.55, 1.95))
@titled("Drop under the body")
def s2(ax):
    b = Person(hip=(0.3, 0.92), face=-1, lean=30, hands={"near": (-0.35, 1.55), "far": (-0.1, 1.3)},
               feet={"near": (0.1, 0.06), "far": (0.6, 0.06)}, style="B"); b.draw(ax)
    a = Person(hip=(-0.1, 0.55), face=1, lean=28, hands={"near": (-0.3, 1.5), "far": (0.42, 0.65)},
               feet={"near": (0.3, 0.06), "far": (-0.45, 0.06)}); a.draw(ax)
@titled("Drive up and turn")
def s3(ax):
    a = Person(hip=(-0.05, 0.86), face=1, lean=10, hands={"near": (-0.45, 1.5), "far": (0.35, 1.55)},
               feet={"near": (0.2, 0.06), "far": (-0.3, 0.06)}); a.draw(ax, zbase=20)
    b = Person(hip=(0.3, 1.5), face=-1, lean=90, hands={"near": (-0.55, 1.35), "far": (-0.5, 1.2)},
               feet={"near": (0.8, 1.65), "far": (0.85, 1.4)}, style="B"); b.draw(ax, zbase=10)
    arrow(ax, (0.6, 1.95), (-0.5, 1.95), rad=0.3)
sequence("fig11_2", [s1, s2, s3], cols=3, xlim=(-1.1, 1.1))

# 11.3 arm bar
@titled("Take the wrist")
def a1(ax):
    a = stance(-0.45, 1, "A", lean=4); a.hands["near"] = (-0.05, 1.3); a.draw(ax)
    b = Person(hip=(0.4, 0.9), face=-1, lean=10, hands={"near": (-0.1, 1.32), "far": (0.15, 1.5)},
               feet={"near": (0.15, 0.06), "far": (0.65, 0.06)}, style="B"); b.draw(ax)
    arrow(ax, (-0.1, 1.05), (-0.5, 1.05))
@titled("Press above the elbow")
def a2(ax):
    b = Person(hip=(0.45, 0.88), face=-1, lean=40, hands={"near": (-0.32, 1.02), "far": (0.2, 1.0)},
               feet={"near": (0.25, 0.06), "far": (0.72, 0.06)}, style="B"); b.draw(ax, zbase=5)
    a = Person(hip=(-0.45, 0.88), face=1, lean=12, hands={"near": (-0.3, 1.02), "far": (-0.05, 1.2)},
               feet={"near": (-0.15, 0.06), "far": (-0.7, 0.06)}, epos={"far": (-0.1, 1.55)}, open_hand=("far",)); a.draw(ax)
    arrow(ax, (0.12, 1.55), (0.05, 1.25))
@titled("Press and circle: face down")
def a3(ax):
    b = Person(hip=(0.55, 0.45), face=-1, lean=72, hands={"near": (-0.35, 0.55), "far": (0.0, 0.08)},
               feet={"near": (0.75, 0.06), "far": (0.95, 0.06)}, knee={"near": 1, "far": 1}, style="B"); b.draw(ax, zbase=5)
    a = Person(hip=(-0.15, 0.82), face=1, lean=30, hands={"near": (-0.4, 0.7), "far": (0.15, 0.62)},
               feet={"near": (0.1, 0.06), "far": (-0.45, 0.06)}); a.draw(ax)
    arrow(ax, (0.25, 1.1), (0.2, 0.75))
sequence("fig11_3", [a1, a2, a3], cols=3, xlim=(-1.0, 1.2))

# 11.4 turning throw (plan)
@titled("Holding arm and shoulder")
def t1(ax):
    top_person(ax, 0, -0.3, 90, "A", lhand=(-0.12, 0.15), rhand=(0.18, 0.2))
    top_person(ax, 0, 0.35, 270, "B")
@titled("Pivot back as they push")
def t2(ax):
    top_person(ax, -0.15, -0.35, 45, "A", lhand=(0.0, 0.1), rhand=(0.18, -0.05))
    top_person(ax, 0.1, 0.2, 250, "B")
    arrow(ax, (-0.55, 0.05), (-0.55, -0.55), rad=0.4)
@titled("Swing them around and down")
def t3(ax):
    top_person(ax, -0.1, -0.2, 340, "A", lhand=(0.15, -0.5), rhand=(0.3, -0.25))
    top_person(ax, 0.45, -0.55, 160, "B")
    arrow(ax, (0.55, 0.45), (0.75, -0.35), rad=-0.4, lw=1.6)
plan_panels("fig11_4", [t1, t2, t3], lim=1.0)
