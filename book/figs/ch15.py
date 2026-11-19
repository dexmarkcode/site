from common import *


def fig15_1():
    fig, ax = canvas(h=2.7, ylim=(0, 60))
    layers = [("Fleet data", NAVY, "white"), ("Vehicle testing", "#244a66", "white"), ("Component benches", TEAL, "white"),
              ("Hardware-in-the-loop", "#4fa6b0", "white"), ("Simulation: MIL / SIL", "#a9d7dc", NAVY)]
    n = len(layers); top, bot = 56, 4; h = (top - bot) / n
    for i, (t, c, tc) in enumerate(layers):
        y1 = top - i * h; y0 = y1 - h
        w1 = 6 + i * 12; w0 = 6 + (i + 1) * 12
        ax.add_patch(Polygon([[50 - w0, y0], [50 + w0, y0], [50 + w1, y1], [50 - w1, y1]], fc=c, ec="white", lw=1.5))
        ax.text(50, (y0 + y1) / 2, t, ha="center", va="center", fontsize=6.6, color=tc, fontweight="semibold")
    arrow(ax, 94, 8, 94, 52, c=AMBER, lw=1.4, ms=7); ax.text(96, 30, "realism,\ncost per test,\ncost to fix", fontsize=6, color=AMBER, va="center")
    arrow(ax, 6, 52, 6, 8, c=TEAL, lw=1.4, ms=7); ax.text(4, 30, "speed,\nnumber of\ntest cases", fontsize=6, color=TEAL, va="center", ha="right")
    ax.set_xlim(-12, 112)
    save(fig, "fig15_1")


def fig15_2():
    fig, ax = canvas(h=2.9, ylim=(0, 64))
    box(ax, 34, 54, 32, 8, "Range lower than expected", fs=6.8, fc=NAVY, ec=NAVY, tc="white")
    mids = [(2, "Consumption\nhigher"), (36, "Usable energy\nlower"), (70, "Range estimate\nwrong")]
    for x, t in mids:
        box(ax, x, 38, 28, 9, t, fs=6.2, fc=PALE, ec=AMBER)
        line(ax, [50, x + 14], [54, 47], c=GREY, lw=0.8)
    leaves = {2: ["Speed / driving style", "Cold: heating, air", "Tyres, pressures", "Added drag, load", "Dragging brake", "Drivetrain fault"],
              36: ["Cold battery", "Cell imbalance", "Ageing (SoH)", "BMS limits / buffer"],
              70: ["Consumption forecast", "SoC estimate drift", "Display filtering"]}
    for x, items in leaves.items():
        for j, t in enumerate(items):
            yy = 30 - j * 5.0
            box(ax, x + 2, yy, 24, 4.2, t, fs=5.3, fc="white", ec="#b9c6cc", bold=False, r=0.6)
            line(ax, [x + 1, x + 1, x + 2], [38, yy + 2.1, yy + 2.1], c=GREY, lw=0.6)
    save(fig, "fig15_2")


if __name__ == "__main__":
    fig15_1(); fig15_2()
