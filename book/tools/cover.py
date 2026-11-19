"""Front cover, 6 x 9 in at 300 dpi."""
import os
import sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'gen'))
import figstyle as fs  # registers fonts
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

W, H = 6, 9
fig = plt.figure(figsize=(W, H), dpi=300)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis('off')
ax.add_patch(Rectangle((0, 0), W, H, color='#14243a'))
# gradient band
for i in range(60):
    ax.add_patch(Rectangle((0, 3.2 + i * 0.03), W, 0.03, color='#1d3557', alpha=0.02 * (60 - i) / 60 * 8, lw=0))

# faint grid like an s-plane
for x in np.arange(0, W + 0.01, 0.4):
    ax.plot([x, x], [0.9, 5.2], color='white', alpha=0.05, lw=0.6)
for y in np.arange(0.9, 5.21, 0.4):
    ax.plot([0, W], [y, y], color='white', alpha=0.05, lw=0.6)
ax.plot([3.6, 3.6], [0.9, 5.2], color='white', alpha=0.18, lw=0.8)
ax.plot([0, W], [3.05, 3.05], color='white', alpha=0.18, lw=0.8)

x = np.linspace(0, W, 2000)
# sinc
ax.plot(x, 3.05 + 1.25 * np.sinc((x - 3.6) * 1.35), color=fs.GOLD, lw=2.2, alpha=0.95)
# damped sinusoid
ax.plot(x, 3.05 + 0.9 * np.exp(-0.45 * x) * np.sin(7.5 * x), color='#5fb3c2', lw=1.4, alpha=0.85)
# square wave partial sums (Gibbs)
sq = sum(np.sin((2 * k + 1) * 2.4 * x) / (2 * k + 1) for k in range(9)) * 4 / np.pi
ax.plot(x, 1.55 + 0.35 * sq, color='white', lw=0.9, alpha=0.35)
# stems
for nn in np.arange(0.3, W, 0.3):
    v = 0.7 * np.cos(1.3 * nn) * np.exp(-0.12 * nn)
    ax.plot([nn, nn], [4.55, 4.55 + v], color=fs.RUST, lw=1.2, alpha=0.8)
    ax.add_patch(Circle((nn, 4.55 + v), 0.045, color=fs.RUST, alpha=0.9))
# poles and zeros
for (px, py) in [(2.9, 3.85), (2.9, 2.25)]:
    ax.plot([px - 0.1, px + 0.1], [py - 0.1, py + 0.1], color='white', lw=1.6)
    ax.plot([px - 0.1, px + 0.1], [py + 0.1, py - 0.1], color='white', lw=1.6)
ax.add_patch(Circle((4.4, 3.05), 0.1, fill=False, ec='white', lw=1.6))
ax.add_patch(Circle((3.6, 3.05), 1.15, fill=False, ec='white', lw=0.7, alpha=0.25, ls='--'))

# title block
ax.add_patch(Rectangle((0, 5.55), W, 3.45, color='#0f1c2e'))
ax.plot([0.55, 1.75], [7.05, 7.05], color=fs.GOLD, lw=2)
ax.text(0.55, 8.35, 'SIGNALS AND SYSTEMS', color='white', fontsize=27, family='Libertinus Serif Display', va='center')
ax.text(0.55, 7.55, 'WORKBOOK', color=fs.GOLD, fontsize=40, family='Libertinus Serif Display', va='center')
ax.text(0.55, 6.6, '600 Practice Problems on Fourier, Laplace,\nand Z-Transform With Step-by-Step Solutions',
        color='#dbe3ec', fontsize=12.5, family='Libertinus Serif', style='italic', va='center', linespacing=1.4)
# badge
ax.add_patch(Circle((4.95, 1.45), 0.62, color=fs.GOLD, zorder=5))
ax.add_patch(Circle((4.95, 1.45), 0.55, fill=False, ec='#14243a', lw=0.8, zorder=6))
ax.text(4.95, 1.58, '600', ha='center', va='center', fontsize=21, color='#14243a', family='Fira Sans', weight='bold', zorder=7)
ax.text(4.95, 1.2, 'PROBLEMS', ha='center', va='center', fontsize=7, color='#14243a', family='Fira Sans', weight='bold', zorder=7)
# author
ax.add_patch(Rectangle((0, 0), W, 0.85, color='#0f1c2e'))
ax.text(0.55, 0.43, 'MARCUS J. THORNTON PH.D', color='white', fontsize=15, family='Fira Sans', va='center')
os.makedirs('output', exist_ok=True)
fig.savefig('output/cover.jpg', dpi=300, pil_kwargs={'quality': 92})
print('cover written')
