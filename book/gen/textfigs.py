"""Illustrations used in the chapter narratives."""
import os
import sys
import numpy as np
import figstyle as fs
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle, FancyBboxPatch

OUT = os.path.join(os.path.dirname(__file__), '..', 'figures')


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + '.pdf'), bbox_inches='tight')
    fig.savefig(os.path.join(OUT, name + '.png'), dpi=200, bbox_inches='tight')
    plt.close(fig)


def label_axes(ax, xl='t', yl=None):
    ax.set_xlabel(f'${xl}$', loc='right', labelpad=0)
    if yl:
        ax.set_title(f'${yl}$', loc='left', fontsize=9)


# =============================================================== Chapter 1
def ch1():
    fig, axs = plt.subplots(2, 2, figsize=(6, 3.6))
    t = np.linspace(-2, 4, 1200)
    ax = axs[0, 0]
    ax.plot(t, (t >= 0).astype(float), color=fs.NAVY)
    ax.set_ylim(-0.3, 1.4); label_axes(ax, 't', 'u(t)\\;\\mathrm{unit\\ step}')
    ax = axs[0, 1]
    ax.plot(t, np.where(t >= 0, t, 0), color=fs.TEAL)
    ax.set_ylim(-0.3, 4.2); label_axes(ax, 't', 'r(t) = t\\,u(t)\\;\\mathrm{ramp}')
    ax = axs[1, 0]
    ax.axhline(0, color=fs.INK, lw=0.7)
    ax.annotate('', xy=(0, 1), xytext=(0, 0), arrowprops=dict(arrowstyle='-|>', color=fs.RUST, lw=1.8))
    ax.text(0.15, 0.9, '(1)', color=fs.RUST)
    ax.set_xlim(-2, 4); ax.set_ylim(-0.3, 1.4); label_axes(ax, 't', '\\delta(t)\\;\\mathrm{unit\\ impulse}')
    ax = axs[1, 1]
    for a, c in ((0.5, fs.NAVY), (1.0, fs.TEAL), (2.0, fs.RUST)):
        ax.plot(t, np.where(t >= 0, np.exp(-a * t), 0), color=c, label=f'$a={a:g}$')
    ax.legend(); ax.set_ylim(-0.3, 1.4); label_axes(ax, 't', 'e^{-at}u(t)')
    fig.tight_layout()
    save(fig, 'ch01_elementary')

    # time transformations
    def x(tt):
        return np.interp(tt, [-1, 0, 2, 3], [0, 2, 2, 0], left=0, right=0)
    fig, axs = plt.subplots(2, 2, figsize=(6, 3.4), sharey=True)
    t = np.linspace(-5, 5, 2000)
    for ax, f, ttl, c in [(axs[0, 0], x(t), 'x(t)', fs.NAVY), (axs[0, 1], x(t - 2), 'x(t-2)\\;\\mathrm{delay}', fs.TEAL),
                          (axs[1, 0], x(-t), 'x(-t)\\;\\mathrm{reversal}', fs.RUST), (axs[1, 1], x(2 * t), 'x(2t)\\;\\mathrm{compression}', fs.GOLD)]:
        ax.plot(t, f, color=c); ax.set_ylim(-0.3, 2.6); label_axes(ax, 't', ttl); ax.set_xticks(range(-4, 6, 1))
    fig.tight_layout()
    save(fig, 'ch01_transform')

    # even/odd
    t = np.linspace(-3, 3, 1200)
    xx = np.where(t >= 0, np.exp(-t), 0)
    fig, axs = plt.subplots(1, 3, figsize=(6.2, 1.9), sharey=True)
    for ax, f, ttl, c in [(axs[0], xx, 'x(t) = e^{-t}u(t)', fs.NAVY), (axs[1], 0.5 * np.exp(-abs(t)), 'x_e(t)', fs.TEAL),
                          (axs[2], 0.5 * np.sign(t) * np.exp(-abs(t)), 'x_o(t)', fs.RUST)]:
        ax.plot(t, f, color=c); label_axes(ax, 't', ttl); ax.set_ylim(-0.7, 1.15)
    fig.tight_layout()
    save(fig, 'ch01_evenodd')

    # DT sinusoids
    fig, axs = plt.subplots(2, 1, figsize=(6, 3.2), sharex=True)
    nn = np.arange(0, 33)
    fs.stem(axs[0], nn, np.cos(np.pi * nn / 8), fs.NAVY)
    axs[0].set_title('$\\cos(\\pi n/8)$: periodic, $N = 16$', loc='left')
    fs.stem(axs[1], nn, np.cos(nn / 2.5), fs.RUST)
    axs[1].set_title('$\\cos(n/2.5)$: samples of a periodic curve that never repeat', loc='left')
    axs[1].set_xlabel('$n$', loc='right')
    fig.tight_layout()
    save(fig, 'ch01_dtsin')


# ------------------------------------------------------------ diagram helpers
def block(ax, x, y, text, w=1.3, h=0.7, color=None):
    color = color or fs.NAVY
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle='round,pad=0.02,rounding_size=0.08',
                                fc='#eef2f7', ec=color, lw=1.2))
    ax.text(x, y, text, ha='center', va='center', fontsize=10, color=fs.INK)


def arrow(ax, x1, y1, x2, y2, text=None, color=None, above=True):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='-|>', color=color or fs.INK, lw=1.1, shrinkA=0, shrinkB=0))
    if text:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + (0.15 if above else -0.25), text, ha='center', va='bottom', fontsize=9.5)


def summer(ax, x, y, r=0.18):
    ax.add_patch(Circle((x, y), r, fc='white', ec=fs.NAVY, lw=1.2))
    ax.text(x, y, '+', ha='center', va='center', fontsize=10)


def blank(ax, xl, yl):
    ax.set_xlim(*xl); ax.set_ylim(*yl); ax.axis('off'); ax.set_aspect('equal')


# =============================================================== Chapter 2
def ch2():
    fig, axs = plt.subplots(3, 1, figsize=(6, 4.2))
    ax = axs[0]; blank(ax, (0, 10), (-0.6, 0.8))
    arrow(ax, 0.6, 0, 2.4, 0, '$x(t)$'); block(ax, 3.1, 0, '$h_1$'); arrow(ax, 3.75, 0, 5.25, 0)
    block(ax, 5.9, 0, '$h_2$'); arrow(ax, 6.55, 0, 8.4, 0, '$y(t)$')
    ax.text(9.9, 0, 'cascade:\n$h = h_1 * h_2$', ha='right', va='center', fontsize=8.5, color=fs.RUST)
    ax = axs[1]; blank(ax, (0, 10), (-1.1, 1.1))
    arrow(ax, 0.6, 0, 1.6, 0, '$x$'); ax.plot([1.6, 1.6], [-0.65, 0.65], color=fs.INK, lw=1.1)
    arrow(ax, 1.6, 0.65, 2.6, 0.65); arrow(ax, 1.6, -0.65, 2.6, -0.65)
    block(ax, 3.25, 0.65, '$h_1$'); block(ax, 3.25, -0.65, '$h_2$')
    ax.plot([3.9, 4.8], [0.65, 0.65], color=fs.INK, lw=1.1); ax.plot([3.9, 4.8], [-0.65, -0.65], color=fs.INK, lw=1.1)
    arrow(ax, 4.8, 0.65, 4.8, 0.18); arrow(ax, 4.8, -0.65, 4.8, -0.18); summer(ax, 4.8, 0)
    arrow(ax, 4.98, 0, 6.6, 0, '$y$')
    ax.text(9.9, 0, 'parallel:\n$h = h_1 + h_2$', ha='right', va='center', fontsize=8.5, color=fs.RUST)
    ax = axs[2]; blank(ax, (0, 10), (-1.1, 0.8))
    arrow(ax, 0.6, 0, 1.62, 0, '$x$'); summer(ax, 1.8, 0); arrow(ax, 1.98, 0, 2.9, 0)
    block(ax, 3.55, 0, '$G$'); ax.plot([4.2, 5.4], [0, 0], color=fs.INK, lw=1.1); arrow(ax, 5.4, 0, 6.6, 0, '$y$')
    ax.plot([5.4, 5.4], [0, -0.75], color=fs.INK, lw=1.1); arrow(ax, 5.4, -0.75, 4.2, -0.75)
    block(ax, 3.55, -0.75, '$H$', h=0.5); ax.plot([2.9, 1.8], [-0.75, -0.75], color=fs.INK, lw=1.1)
    arrow(ax, 1.8, -0.75, 1.8, -0.18); ax.text(1.5, -0.45, '$-$', fontsize=11)
    ax.text(9.9, -0.2, 'feedback:\n$G/(1+GH)$ in\nthe transform domain', ha='right', va='center', fontsize=8.5, color=fs.RUST)
    fig.tight_layout(); save(fig, 'ch02_interconnect')

    fig, axs = plt.subplots(1, 2, figsize=(6.2, 2.0))
    nn = np.arange(0, 16)
    fs.stem(axs[0], nn, 0.8 ** nn, fs.TEAL); axs[0].set_title('$h[n] = (0.8)^n u[n]$: stable', loc='left'); axs[0].set_xlabel('$n$', loc='right')
    fs.stem(axs[1], nn, 1.15 ** nn, fs.RUST); axs[1].set_title('$h[n] = (1.15)^n u[n]$: unstable', loc='left'); axs[1].set_xlabel('$n$', loc='right')
    fig.tight_layout(); save(fig, 'ch02_stability')

    fig, ax = plt.subplots(figsize=(5.6, 2.1))
    t = np.linspace(0, 12, 1000)
    ax.plot(t, np.cos(1.2 * t), color=fs.NAVY, label='input $\\cos(1.2t)$')
    H = 1 / (0.6 + 1.2j)
    ax.plot(t, abs(H) * np.cos(1.2 * t + np.angle(H)) , color=fs.RUST, label='output: scaled and delayed')
    ax.legend(loc='upper right', ncol=2); ax.set_ylim(-1.3, 1.6); ax.set_xlabel('$t$', loc='right')
    fig.tight_layout(); save(fig, 'ch02_eigen')


# =============================================================== Chapter 3
def ch3():
    tau = np.linspace(-3, 5, 1600)
    h = np.where(tau >= 0, np.exp(-0.8 * tau), 0)
    fig, axs = plt.subplots(2, 2, figsize=(6.2, 3.6), sharey=True)
    for ax, tt in zip(axs.flat, [-1.0, 0.8, 2.0, 3.5]):
        x = np.where((tt - tau >= 0) & (tt - tau < 1.5), 1.0, 0)
        ax.plot(tau, h, color=fs.NAVY, label='$h(\\tau)$')
        ax.plot(tau, x, color=fs.RUST, label='$x(t-\\tau)$')
        ov = np.minimum(h, x)
        ax.fill_between(tau, 0, ov, color=fs.GOLD, alpha=0.45)
        ax.set_title(f'$t = {tt:g}$', loc='left'); ax.set_ylim(-0.1, 1.25); ax.set_xlabel('$\\tau$', loc='right')
    axs[0, 0].legend(loc='upper right')
    fig.tight_layout(); save(fig, 'ch03_flipslide')

    t = np.linspace(-1, 7, 1600)
    y = np.where(t < 0, 0, np.where(t < 1.5, (1 - np.exp(-0.8 * t)) / 0.8, (np.exp(0.8 * 1.5) - 1) * np.exp(-0.8 * t) / 0.8))
    fig, ax = plt.subplots(figsize=(5.6, 1.9))
    ax.plot(t, y, color=fs.TEAL); ax.set_title('$y(t) = x(t) * h(t)$', loc='left'); ax.set_xlabel('$t$', loc='right')
    for tt in [-1.0, 0.8, 2.0, 3.5]:
        yy = np.interp(tt, t, y); ax.plot([tt], [yy], 'o', color=fs.GOLD, ms=5)
    fig.tight_layout(); save(fig, 'ch03_result')

    fig, axs = plt.subplots(1, 3, figsize=(6.2, 1.8), sharey=True)
    xv = [1, 2, 1]; hv = [1, -1]
    fs.stem(axs[0], range(3), xv, fs.NAVY); axs[0].set_title('$x[n]$', loc='left')
    fs.stem(axs[1], range(2), hv, fs.TEAL); axs[1].set_title('$h[n]$', loc='left')
    fs.stem(axs[2], range(4), np.convolve(xv, hv), fs.RUST); axs[2].set_title('$y[n] = x*h$', loc='left')
    for ax in axs: ax.set_xlim(-0.8, 4.5); ax.set_xlabel('$n$', loc='right')
    fig.tight_layout(); save(fig, 'ch03_dtconv')


ALL = [ch1, ch2, ch3]

if __name__ == '__main__':
    which = sys.argv[1:] or [f.__name__ for f in ALL]
    for f in ALL:
        if f.__name__ in which:
            f()
            print('made', f.__name__)
