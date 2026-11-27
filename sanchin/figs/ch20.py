import importlib.util, sys
from common import *
spec = importlib.util.spec_from_file_location("ch19", str(Path(__file__).parent / "ch19.py"))
# reuse flowchart without re-rendering ch19: copy minimal function
from matplotlib.patches import FancyBboxPatch


def rbox(ax, x, y, w, h, text, fs=5.8, fill=WH, lw=0.8, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2", fc=fill, ec=K, lw=lw, zorder=3))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, zorder=4, linespacing=1.1,
            fontweight="bold" if bold else "normal")


def flowchart(name, symptoms, faults, links, h=3.0):
    fig, ax = canvas(W, h, xlim=(0, 150), ylim=(0, 100 * h / 3.0))
    top = 100 * h / 3.0
    ns, nf = len(symptoms), len(faults)
    ys = [top - 8 - i * (top - 12) / ns for i in range(ns)]
    yf = [top - 6 - i * (top - 8) / nf for i in range(nf)]
    for y, s in zip(ys, symptoms):
        rbox(ax, 2, y - 5, 50, 10, s, fill=G1, bold=True)
    for y, f in zip(yf, faults):
        rbox(ax, 92, y - 3.3, 56, 6.6, f, fs=5.5)
    for a, bs in links.items():
        for b in bs:
            ax.plot([52, 92], [ys[a], yf[b]], color=K, lw=0.5, zorder=1)
    ax.text(27, top - 1, "SYMPTOM", ha="center", fontsize=5.6, fontweight="bold")
    ax.text(120, top + 1.5, "LIKELY FAULT", ha="center", fontsize=5.6, fontweight="bold")
    save(fig, name)


if __name__ == "__main__":
    flowchart("fig20_1",
              ["Shoulder press\ngives way", "Punch push-back\ngives way", "Lower back aches", "Neck and shoulders\nache",
               "Block drifts when\nstepping", "One side always\nweaker"],
              ["20.1 Pelvis tilted forward", "20.2 Pelvis over-tucked", "20.3 Hips twisting", "20.4 Hips rising/falling",
               "20.5 Leaning forward", "20.6 Leaning back", "20.7 Ribs flaring", "20.8 Rounded upper back",
               "20.9 Shoulders raised", "20.10 Shoulders forward", "20.11 Blades winging", "20.12 Elbows flaring",
               "20.13 Arms drifting", "20.14 Asymmetry"],
              {0: [8, 0, 3], 1: [9, 4, 2, 11], 2: [0, 6, 1], 3: [8, 7, 6], 4: [12, 11, 2], 5: [13]})


def twist(p, deg):
    a = math.radians(deg)
    R = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]])
    for k in ("lsh", "rsh", "lel", "rel", "lwr", "rwr", "lhd", "rhd", "neck", "head"):
        p.j[k] = R @ p.j[k]
    return p


if __name__ == "__main__":
    fig, ax = canvas(W, 2.1, xlim=(0, 200), ylim=(-12, 104))
    floor(ax, 2, 198)
    cfg = [(Pose("uke", "uke", "sanchin", "R", lean=7, hipshift=-3), "Leaning forward", False),
           (Pose("uke", "uke", "sanchin", "R", hipshift=5, lean=-5), "Leaning back", False),
           (Pose("uke", "uke", "sanchin", "R", lean=3, chin=5, shrug=1), "Rounded upper back", False),
           (Pose("uke", "uke", "sanchin", "R"), "Correct", True)]
    for i, (pp, cap, ok) in enumerate(cfg):
        x = 25 + i * 50
        Figure(ax, pp, ox=x, th=-90, sc=0.95)
        (tick_mark if ok else cross_mark)(ax, x - 20, 96, r=3.2)
        sub_label(ax, x, -3, cap, fs=6.2)
    save(fig, "fig20_2")

    fig, ax = canvas(W, 2.5, xlim=(0, 165), ylim=(-12, 104))
    floor(ax, 2, 163)
    tw = twist(Pose("tsuki", "uke", "sanchin", "R"), -18)
    asym = Pose("uke", "uke", "sanchin", "R")
    asym.j["rsh"] = asym.j["rsh"] + v(0, 0, 4)
    for k in ("rel", "rwr", "rhd"):
        asym.j[k] = asym.j[k] + v(-5, 0, 4)
    cfg = [(tw, "Hips and shoulders twisting", False), (asym, "Asymmetry", False), (Pose("uke", "uke", "sanchin", "R"), "Square and symmetrical", True)]
    for i, (pp, cap, ok) in enumerate(cfg):
        x = 28 + i * 55
        Figure(ax, pp, ox=x, th=0)
        (tick_mark if ok else cross_mark)(ax, x - 22, 96, r=3.2)
        sub_label(ax, x, -3, cap, fs=6.2)
    save(fig, "fig20_3")
