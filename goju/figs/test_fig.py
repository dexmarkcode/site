from figlib import *
@titled("Guard and distance")
def p1(ax):
    stance(-0.55,1,"A").draw(ax); stance(0.55,-1,"B").draw(ax)
@titled("Rising elbow")
def p2(ax):
    a=stance(-0.3,1,"A",lean=12)
    a.hands["near"]=(0.12,1.78); a.elbow["near"]=1
    a.draw(ax)
    b=stance(0.45,-1,"B",lean=-8); b.draw(ax)
    impact(ax,0.2,1.72)
@titled("Knee to the thigh")
def p3(ax):
    a=stance(-0.3,1,"A",lean=-5)
    a.feet["near"]=(0.05,0.55); a.toes["near"]=-60
    a.hands["near"]=(0.25,1.6); a.hands["far"]=(0.3,1.55)
    a.draw(ax)
    stance(0.4,-1,"B").draw(ax)
    arrow(ax,(-0.25,0.35),(0.05,0.62),rad=-0.3)
sequence("test", [p1,p2,p3])
