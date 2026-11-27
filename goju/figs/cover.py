from figlib import *
from matplotlib import font_manager as fm
import os
F = os.path.join(HERE, "..", "fonts")
for f in os.listdir(F):
    fm.fontManager.addfont(os.path.join(F, f))
fig = plt.figure(figsize=(6, 9))
bg = fig.add_axes([0, 0, 1, 1]); bg.set_xlim(0, 6); bg.set_ylim(0, 9); bg.axis("off")
bg.add_patch(Rectangle((0, 0), 6, 9, fc="black"))
bg.text(3, 8.25, "GOJU-RYU KARATE", ha="center", color="white", fontsize=19, family="Source Sans 3", fontweight="bold")
bg.plot([2.2, 3.8], [7.98, 7.98], color="white", lw=1.2)
bg.text(3, 7.2, "CLOSE-COMBAT", ha="center", color="white", fontsize=40, family="EB Garamond", fontweight="bold")
bg.text(3, 6.5, "MASTERCLASS", ha="center", color="white", fontsize=40, family="EB Garamond", fontweight="bold")
sub = ("Diagrams for Trapping, Elbows, Knees, Throws,\nJoint Controls, and Counter-Attacks\nfor Sparring and Real-World Encounters")
bg.text(3, 5.75, sub, ha="center", va="top", color="white", fontsize=12.5, family="EB Garamond", style="italic", linespacing=1.35)
# figure panel in white
ax = fig.add_axes([0.1, 0.15, 0.8, 0.32]); ax.set_xlim(-1.4, 1.4); ax.set_ylim(-0.1, 2.0); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(Rectangle((-1.4, -0.1), 2.8, 2.1, fc="white", ec="white"))
ax.plot([-1.3, 1.3], [0, 0], color="black", lw=1.2)
a = stance(-0.25, 1, "A", lean=14); a.hands["far"] = (-0.05, 1.68); a.epos = {"far": (0.4, 1.62)}; a.hands["near"] = (0.22, 1.42); a.open_hand = ("near",); a.draw(ax)
b = stance(0.5, -1, "B", lean=-8); b.hands["near"] = (0.18, 1.4); b.draw(ax)
impact(ax, 0.42, 1.72, r=0.1)
bg.text(3, 0.6, "DR BEVERLY J. STIVERS", ha="center", color="white", fontsize=18, family="Source Sans 3", fontweight="bold")
fig.savefig(os.path.join(OUTDIR, "cover.png"), dpi=300, facecolor="black")
from PIL import Image
im = Image.open(os.path.join(OUTDIR, "cover.png")).convert("L").convert("RGB")
im = im.resize((1800, 2700)); im.save(os.path.join(OUTDIR, "cover.jpg"), quality=92, dpi=(300, 300))
im.save(os.path.join(OUTDIR, "cover.png"))
