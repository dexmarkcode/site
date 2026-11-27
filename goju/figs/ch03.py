from figlib import *

# 3.1 inside vs outside
@titled("Inside line: both hands reach you")
def a(ax):
    top_person(ax, 0, 0.55, 270, "B")
    top_person(ax, 0, -0.35, 90, "A", lhand=(-0.12, 0.12), rhand=(0.1, -0.02))
    arrow(ax, (0.18, 0.2), (0.05, -0.22), lw=1.1); arrow(ax, (-0.18, 0.2), (-0.05, -0.22), lw=1.1)
@titled("Outside line: their arm blocks their rear hand")
def b(ax):
    top_person(ax, 0, 0.55, 270, "B")
    top_person(ax, -0.62, -0.05, 45, "A", lhand=(-0.32, 0.12), rhand=(-0.3, 0.38))
    arrow(ax, (-0.18, 0.2), (-0.38, -0.0), lw=1.1, dashed=True)
    ax.text(0.35, -0.55, "rear hand\nhas no line", fontsize=6.5, ha="center")
plan_panels("fig3_1", [a, b], lim=1.0)

# 3.2 pivots
@titled("Front pivot (turn on the lead foot)")
def p1(ax):
    footprint(ax, 0.0, 0.25, 90, "L", s=1.6)
    footprint(ax, 0.25, -0.45, 90, "R", fill="white", label=True, s=1.6, ec="black")
    footprint(ax, -0.55, 0.15, 0, "R", s=1.6)
    arrow(ax, (0.2, -0.5), (-0.5, -0.05), rad=-0.5)
    ax.text(0, -0.85, "rear foot sweeps round", fontsize=6.5, ha="center")
    arrow(ax, (0.0, 0.95), (0.0, 0.62), lw=1.6); ax.text(0.06, 0.9, "push", fontsize=6.5)
@titled("Back pivot (turn on the rear foot)")
def p2(ax):
    footprint(ax, 0.2, -0.35, 90, "R", s=1.6)
    footprint(ax, -0.05, 0.4, 90, "L", fill="white", s=1.6)
    footprint(ax, -0.55, -0.35, 0, "L", s=1.6)
    arrow(ax, (-0.12, 0.35), (-0.55, -0.1), rad=0.45)
    ax.text(0, -0.85, "lead foot swings back", fontsize=6.5, ha="center")
    arrow(ax, (0.2, 0.95), (0.2, 0.55), lw=1.6, dashed=True); ax.text(0.26, 0.9, "push goes past", fontsize=6.5)
plan_panels("fig3_2", [p1, p2], lim=1.0)

# 3.3 cover entry
@titled("Punching range")
def c1(ax):
    stance(-0.75, 1, "A").draw(ax); stance(0.65, -1, "B").draw(ax)
@titled("Angled step, forearms up")
def c2(ax):
    a = stance(-0.45, 1, "A", lean=12); a.hands["near"] = (-0.05, 1.72); a.hands["far"] = (-0.1, 1.62); a.elbow["near"] = -1
    a.draw(ax)
    b = stance(0.6, -1, "B", lean=-6); b.hands["near"] = (0.15, 1.68); b.draw(ax)
    arrow(ax, (-0.95, 0.25), (-0.55, 0.25), dashed=True)
@titled("Contact made, off the line")
def c3(ax):
    a = stance(-0.25, 1, "A", lean=12); a.hands["near"] = (0.2, 1.68); a.hands["far"] = (0.05, 1.55); a.draw(ax)
    b = stance(0.55, -1, "B", lean=-8); b.hands["near"] = (0.12, 1.7); b.draw(ax)
    impact(ax, 0.2, 1.75, r=0.07)
sequence("fig3_3", [c1, c2, c3], cols=3)

# 3.4 angles vs problems (plan)
@titled("Two-handed push")
def q1(ax):
    top_person(ax, 0, 0.5, 270, "B", lhand=(0.15, 0.05), rhand=(-0.15, 0.05))
    top_person(ax, 0.42, -0.25, 160, "A")
    ax.add_patch(Circle((0, -0.25), 0.25, fc="none", ec="black", lw=0.7, ls=(0, (2, 2)), zorder=3))
    arrow(ax, (0.05, -0.3), (0.32, -0.3), rad=0.3)
    arrow(ax, (0, 0.2), (0, -0.75), dashed=True, lw=0.9)
@titled("Heavy hook")
def q2(ax):
    top_person(ax, 0, 0.45, 270, "B", rhand=(-0.45, 0.0))
    arrow(ax, (-0.55, 0.45), (-0.45, 0.05), rad=0.3, dashed=True)
    top_person(ax, -0.2, -0.15, 70, "A", lhand=(-0.25, 0.18), rhand=(-0.02, 0.22))
    arrow(ax, (-0.3, -0.7), (-0.22, -0.32))
@titled("Grab and punch")
def q3(ax):
    top_person(ax, 0, 0.45, 270, "B", lhand=(0.38, -0.05), rhand=(-0.2, 0.25))
    top_person(ax, 0.5, -0.22, 120, "A", lhand=(0.5, 0.15), rhand=(0.25, 0.12))
    arrow(ax, (0.05, -0.55), (0.42, -0.42), rad=0.2)
    ax.text(-0.5, -0.75, "grabbing arm now\nshields you", fontsize=6, ha="center")
plan_panels("fig3_4", [q1, q2, q3], lim=1.0)

# 3.5 triangle
@titled("Strong and weak lines of a fighting stance")
def t1(ax):
    footprint(ax, 0.25, 0.35, 70, "L", fill="white", s=1.5)
    footprint(ax, -0.25, -0.35, 70, "R", fill="white", s=1.5)
    ax.plot([0.25, -0.25], [0.35, -0.35], color="black", lw=1.6)
    for px, py in ((-0.5, 0.4), (0.5, -0.4)):
        ax.plot([0.25, px, -0.25], [0.35, py, -0.35], color="black", lw=0.8, ls=(0, (3, 2)))
        ax.add_patch(Circle((px, py), 0.06, fc="black", zorder=20))
    ax.text(-0.55, 0.52, "weak point", fontsize=6.5, ha="center")
    ax.text(0.58, -0.58, "weak point", fontsize=6.5, ha="center")
    ax.text(0.42, 0.18, "strong line", fontsize=6.5, rotation=55)
plan_panels("fig3_5", [t1], width=3.0, lim=0.85)
