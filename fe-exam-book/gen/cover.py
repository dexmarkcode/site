"""Front cover artwork (1600 x 2286 px, 7:10 trim ratio)."""
import os
import random
import numpy as np
import figstyle  # noqa: F401  registers fonts
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap

OUT = os.path.join(os.path.dirname(__file__), "..", "figures", "cover.png")
W, H = 7, 10
rng = random.Random(7)

fig = plt.figure(figsize=(W, H), dpi=228.6)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")

# background gradient
grad = np.linspace(0, 1, 512).reshape(-1, 1)
cmap = LinearSegmentedColormap.from_list("bg", ["#07142B", "#10264A", "#163563"])
ax.imshow(grad, extent=[0, W, 0, H], cmap=cmap, aspect="auto", origin="lower", zorder=0)

# circuit traces
COP = "#C9813A"
for _ in range(70):
    x, y = rng.uniform(0, W), rng.uniform(0, H)
    pts = [(x, y)]
    for _ in range(rng.randint(2, 5)):
        if rng.random() < 0.5:
            x += rng.choice([-1, 1]) * rng.uniform(0.3, 1.4)
        else:
            y += rng.choice([-1, 1]) * rng.uniform(0.3, 1.4)
        if rng.random() < 0.35:
            d = rng.uniform(0.2, 0.6)
            x += d * rng.choice([-1, 1])
            y += d * rng.choice([-1, 1])
        pts.append((x, y))
    xs, ys = zip(*pts)
    a = rng.uniform(0.06, 0.2)
    ax.plot(xs, ys, color=COP, lw=1.0, alpha=a, zorder=1, solid_capstyle="round")
    ax.add_patch(Circle(pts[-1], 0.045, fc="none", ec=COP, lw=1.0, alpha=a + 0.05, zorder=1))
    ax.add_patch(Circle(pts[0], 0.03, fc=COP, ec="none", alpha=a, zorder=1))

# sine waves motif across the middle
t = np.linspace(0, W, 800)
for k, (amp, ph, al) in enumerate([(0.32, 0, 0.9), (0.32, 2.094, 0.55), (0.32, 4.189, 0.35)]):
    ax.plot(t, 3.55 + amp * np.sin(2 * np.pi * t / 2.3 + ph), color=["#E6A15C", "#C9813A", "#8FA9D6"][k], lw=2.0, alpha=al, zorder=2)

# top band
ax.add_patch(Rectangle((0, 9.12), W, 0.88, fc="#B5651D", ec="none", zorder=3))
ax.text(W / 2, 9.56, "2026 – 2027  EDITION   ·   UPDATED FOR THE COMPUTER-BASED EXAM", ha="center", va="center",
        color="white", fontsize=11.5, fontweight="bold", zorder=4, family="TeX Gyre Pagella")

# title block
ax.text(W / 2, 8.42, "ELECTRICAL", ha="center", va="center", color="white", fontsize=50, fontweight="bold", zorder=4)
ax.text(W / 2, 7.62, "ENGINEERING", ha="center", va="center", color="white", fontsize=50, fontweight="bold", zorder=4)
ax.plot([1.2, 5.8], [7.08, 7.08], color="#E6A15C", lw=2.2, zorder=4)
ax.text(W / 2, 6.55, "FE EXAM PREP", ha="center", va="center", color="#E6A15C", fontsize=44, fontweight="bold", zorder=4)
ax.text(W / 2, 5.88, "2026 – 2027", ha="center", va="center", color="white", fontsize=30, zorder=4)
ax.text(W / 2, 5.12, "The Complete Study Guide", ha="center", va="center", color="white", fontsize=23, style="italic", zorder=4)

# feature badges
feat = [("800", "Practice\nQuestions"), ("2", "Full-Length\nMock Exams"), ("100%", "Worked\nSolutions")]
for i, (big, small) in enumerate(feat):
    cx = 1.35 + i * 2.15
    ax.add_patch(FancyBboxPatch((cx - 0.85, 1.95), 1.7, 1.15, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=(1, 1, 1, 0.07), ec="#E6A15C", lw=1.3, zorder=4))
    ax.text(cx, 2.78, big, ha="center", va="center", color="#E6A15C", fontsize=27, fontweight="bold", zorder=5)
    ax.text(cx, 2.27, small, ha="center", va="center", color="white", fontsize=11.5, zorder=5, linespacing=1.15)

ax.text(W / 2, 1.45, "Formulas  ·  Exam Strategy  ·  Reference Handbook Skills  ·  Pass First Time",
        ha="center", va="center", color="#D9DEE8", fontsize=12.5, zorder=4)

# author
ax.plot([2.3, 4.7], [0.98, 0.98], color="#E6A15C", lw=1.0, zorder=4)
ax.text(W / 2, 0.55, "MARCUS J. THORNTON, Ph.D.", ha="center", va="center", color="white", fontsize=21, fontweight="bold", zorder=4)

fig.savefig(OUT, dpi=228.6, bbox_inches=None, pad_inches=0, facecolor=fig.get_facecolor())
print("cover saved", OUT)
