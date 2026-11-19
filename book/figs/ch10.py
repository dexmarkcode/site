from common import *
from matplotlib.patches import Ellipse


def fig10_1():
    fig, ax = plt.subplots(figsize=(W, 2.6))
    ax.set_xscale("log"); ax.set_yscale("log")
    regions = [("Si MOSFET", 3e4, 1e6, 15, 200, GREY), ("Si IGBT", 1e3, 3e4, 600, 6500, NAVY),
               ("SiC MOSFET", 5e3, 2e5, 600, 3300, TEAL), ("GaN HEMT", 5e4, 3e6, 80, 700, AMBER)]
    for name, f1, f2, v1, v2, c in regions:
        cx = np.sqrt(f1 * f2); cy = np.sqrt(v1 * v2)
        e = Ellipse((np.log10(cx), np.log10(cy)), np.log10(f2 / f1), np.log10(v2 / v1), transform=ax.transData, fc=c, alpha=0.18, ec=c, lw=1.2)
        ax.add_patch(Rectangle((f1, v1), f2 - f1, v2 - v1, fc=c, alpha=0.16, ec=c, lw=1.1))
        ax.text(cx, cy, name, ha="center", va="center", fontsize=7.5, color=c, fontweight="semibold")
    ax.set_xlim(5e2, 5e6); ax.set_ylim(10, 1e4)
    ax.set_xlabel("Switching frequency (Hz)"); ax.set_ylabel("Blocking voltage (V)")
    for v, t in [(48, "48 V systems"), (400, "400 V traction"), (800, "800 V traction")]:
        ax.axhline(v, color=RED, lw=0.6, ls=":"); ax.text(6e2, v * 1.08, t, fontsize=6.3, color=RED)
    save(fig, "fig10_1")


def fig10_2():
    t = np.linspace(0, 1, 800)
    fig, axs = plt.subplots(1, 2, figsize=(W, 2.2), sharey=True)
    # turn-on
    a = axs[0]
    i = np.clip((t - 0.2) / 0.2, 0, 1) + 0.35 * np.exp(-((t - 0.42) / 0.05) ** 2)
    v = np.where(t < 0.4, 1, np.clip(1 - (t - 0.4) / 0.2, 0, 1)) + 0.0
    p = i * v
    a.plot(t, v, color=NAVY, label="$v$"); a.plot(t, i, color=TEAL, label="$i$")
    a.fill_between(t, 0, p, color=AMBER, alpha=0.35, label="loss $v \\cdot i$")
    a.text(0.42, 1.42, "diode\nrecovery", fontsize=6.3, color=TEAL)
    a.set_title("Turn-on", fontsize=8, color=NAVY, fontweight="semibold")
    # turn-off
    a = axs[1]
    v2 = np.clip((t - 0.2) / 0.15, 0, 1) + 0.25 * np.exp(-((t - 0.42) / 0.04) ** 2)
    i2 = np.where(t < 0.35, 1, np.clip(1 - (t - 0.35) / 0.12, 0.18, 1))
    tail = np.where(t > 0.47, 0.18 * np.exp(-(t - 0.47) / 0.15), i2)
    i2 = np.where(t > 0.47, tail, i2)
    a.plot(t, v2, color=NAVY, label="$v$"); a.plot(t, i2, color=TEAL, label="$i$")
    a.fill_between(t, 0, v2 * i2, color=AMBER, alpha=0.35)
    a.annotate("IGBT tail", xy=(0.6, 0.08), xytext=(0.65, 0.5), fontsize=6.5, color=TEAL, arrowprops=dict(arrowstyle="->", color=TEAL, lw=0.6))
    a.text(0.45, 1.3, "overshoot\n$L\\,di/dt$", fontsize=6.3, color=NAVY)
    a.set_title("Turn-off", fontsize=8, color=NAVY, fontweight="semibold")
    for a in axs:
        a.set_xticks([]); a.set_xlabel("time"); a.set_ylim(0, 1.7)
    axs[0].set_ylabel("p.u."); axs[0].legend(loc="upper left", fontsize=6.5)
    fig.subplots_adjust(wspace=0.06)
    save(fig, "fig10_2")


def fig10_3():
    fig, ax = canvas(h=2.3, ylim=(0, 52))
    layers = [(6, 4, 88, 8, "#b87333", "copper baseplate"),
              (10, 12, 80, 3, "#d4a26a", "copper"),
              (10, 15, 80, 4, "#f3efe6", "ceramic (Si₃N₄ / AlN)"),
              (10, 19, 80, 3, "#d4a26a", "copper (patterned)")]
    for x, y, w, h, c, t in layers:
        ax.add_patch(Rectangle((x, y), w, h, fc=c, ec=NAVY, lw=0.5))
        ax.text(x + w + 6, y + h / 2, t, fontsize=6.2, color=NAVY, va="center")
    for x in range(10, 94, 5):
        ax.add_patch(Rectangle((x, 0), 2.5, 4, fc="#b87333", ec="none"))
    ax.text(100, 2, "pin fins in coolant", fontsize=6.2, color=TEAL, va="center", ha="left")
    ax.add_patch(Rectangle((6, -0.5), 88, 0.5, fc=TEAL, ec="none"))
    for x in (18, 44):
        ax.add_patch(Rectangle((x, 22), 14, 1, fc="#9aa8b0", ec="none"))
        ax.add_patch(Rectangle((x, 23), 14, 3, fc=NAVY, ec="none"))
        ax.text(x + 7, 24.5, "chip", fontsize=6, color="white", ha="center", va="center")
        for k in range(3):
            xs = np.linspace(x + 3 + k * 4, x + 22 + k * 3, 30)
            ys = 26 + 8 * np.sin(np.linspace(0, np.pi, 30))
            ax.plot(xs, ys, color="#8a9aa3", lw=0.9)
    ax.text(32, 37, "bond wires", fontsize=6.3, color=GREY, ha="center")
    ax.annotate("sintered die attach", xy=(30, 22.5), xytext=(96, 28), fontsize=6.2, color=NAVY, arrowprops=dict(arrowstyle="->", color=NAVY, lw=0.5))
    ax.add_patch(Rectangle((70, 22), 4, 18, fc="#d4a26a", ec=NAVY, lw=0.5)); ax.text(72, 42, "terminal", fontsize=6.2, color=NAVY, ha="center")
    ax.add_patch(Rectangle((6, 12), 88, 34, fc="none", ec=GREY, lw=0.6, ls="--")); ax.text(8, 43.5, "gel / mould compound", fontsize=6.2, color=GREY)
    ax.set_xlim(0, 135)
    save(fig, "fig10_3")


if __name__ == "__main__":
    fig10_1(); fig10_2(); fig10_3()
