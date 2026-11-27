"""Sequence strips and embusen maps for every kata."""
import math, sys, textwrap
from lib import *
from kata_data import KATA

COLS, ROWS = 2, 4


def cell(ax, x, y, w, h, mv):
    st = mv["st"]
    ax.add_patch(Rectangle((x, y), w, h, fc=WHITE, ec=INK, lw=0.6, zorder=1))
    # number badge
    n = str(mv["n"])
    bw = 7 if len(n) > 2 else 5.2
    ax.add_patch(Rectangle((x, y + h - 5.2), bw, 5.2, fc=INK, ec=INK, zorder=3))
    label(ax, x + bw / 2, y + h - 2.6, n, fs=7.2, c=WHITE, fontweight="bold", zorder=4)
    direction_icon(ax, x + w - 3.6, y + h - 3.6, mv["d"], r=2.4)
    label(ax, x + w - 3.6, y + h - 8.0, mv["d"], fs=5.4, c=DARK)
    if mv["k"]:
        ax.add_patch(Rectangle((x + bw + 1, y + h - 5.0), 9, 4.8, fc=WHITE, ec=INK, lw=0.6, zorder=3))
        label(ax, x + bw + 5.5, y + h - 2.6, "KIAI", fs=5.6, fontweight="bold", zorder=4)
    gy = y + 13.2
    ground(ax, x + 4, x + w - 4, gy)
    figure(ax, x + w / 2 - (3 if STANCES[st]["view"] == "side" else 0), gy, st, L=mv["L"], R=mv["R"], s=2.55)
    txt = mv["txt"]
    lines = textwrap.wrap(txt, 36)[:2]
    label(ax, x + w / 2, y + 7.6 if len(lines) > 1 else y + 6.4, "\n".join(lines), fs=6.7, linespacing=1.08)
    if mv["note"]:
        label(ax, x + w / 2, y + 1.9, mv["note"], fs=5.9, c=DARK, style="italic")


def strips(key):
    name, moves = KATA[key]
    per = COLS * ROWS
    pages = [moves[i:i + per] for i in range(0, len(moves), per)]
    out = []
    for pi, chunk in enumerate(pages, 1):
        rows = math.ceil(len(chunk) / COLS)
        cw, ch = 50, 40
        H = rows * ch
        fig, ax = canvas(w=4.5, h=4.5 * H / 100, xlim=(0, 100), ylim=(0, H))
        for i, mv in enumerate(chunk):
            r, c = divmod(i, COLS)
            cell(ax, c * cw + 0.4, H - (r + 1) * ch + 0.4, cw - 0.8, ch - 0.8, mv)
        fn = f"seq_{key}_{pi}"
        save(fig, fn)
        out.append((fn, chunk[0]["n"], chunk[-1]["n"]))
    return out


def embusen(key):
    name, moves = KATA[key]
    pts, order = {}, []
    def snap(q):
        for o in order:
            if abs(o[0] - q[0]) < 0.3 and abs(o[1] - q[1]) < 0.3:
                return o
        return q
    for mv in moves:
        p = snap((round(mv["pos"][0], 2), round(mv["pos"][1], 2)))
        mv["_st"] = p
        if p not in pts:
            pts[p] = []; order.append(p)
        pts[p].append(mv)
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    x0, x1 = min(xs) - 0.8, max(xs) + 0.8
    y0, y1 = min(ys) - 0.8, max(ys) + 0.8
    MW = 58.0                       # map panel width
    n_leg = len(order)
    H = max(n_leg * 5.2 + 14, 62)
    Sy = (H - 14) / (y1 - y0)
    Sx = min(MW / (x1 - x0), Sy * 1.3)
    S = Sy
    mh = (y1 - y0) * Sy
    fig, ax = canvas(w=4.5, h=4.5 * H / 100, xlim=(0, 100), ylim=(0, H))
    ox = MW / 2 - (x0 + x1) / 2 * Sx + 1
    oy = (H - mh) / 2 - y0 * Sy
    X = lambda p: (ox + p[0] * Sx, oy + p[1] * Sy)
    ax.add_patch(Rectangle((0.5, 0.5), MW + 1.5, H - 1, fc=WHITE, ec=INK, lw=0.6))
    # dojo floor grid
    g = 1.0
    gx = math.floor(x0)
    while gx <= x1:
        ax.plot([X((gx, 0))[0]] * 2, [1, H - 1], color=PALE, lw=0.5, zorder=0); gx += g
    gy = math.floor(y0)
    while gy <= y1:
        ax.plot([1.0, MW + 1.5], [X((0, gy))[1]] * 2, color=PALE, lw=0.5, zorder=0); gy += g
    seqp = [m["_st"] for m in moves]
    segs = set()
    for a, b in zip(seqp, seqp[1:]):
        if a != b and (a, b) not in segs and (b, a) not in segs:
            segs.add((a, b))
            ax.plot(*zip(X(a), X(b)), color=INK, lw=1.4, solid_capstyle="round", zorder=3)
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i, p in enumerate(order):
        px, py = X(p)
        start = i == 0
        ax.add_patch(Circle((px, py), 1.9, fc=INK if start else WHITE, ec=INK, lw=0.9, zorder=8))
        label(ax, px, py, letters[i], fs=5.6, c=WHITE if start else INK, fontweight="bold", zorder=9)
        # facing tick for first move at this station
        ang = math.radians(DIRS[pts[p][0]["d"]])
    compass(ax, MW - 3.5, H - 7, r=2.6)
    label(ax, MW / 2 + 1, 3.2, "Shomen (front) is at the top", fs=5.6, c=DARK)
    # legend
    lx = MW + 5
    label(ax, lx, H - 4, "Station    Counts performed there", fs=6.4, ha="left", fontweight="bold")
    ax.plot([lx, 99.5], [H - 6.3, H - 6.3], color=INK, lw=0.6)
    for i, p in enumerate(order):
        yy = H - 10 - i * 5.2
        ax.add_patch(Circle((lx + 2.2, yy), 1.9, fc=INK if i == 0 else WHITE, ec=INK, lw=0.7))
        label(ax, lx + 2.2, yy, letters[i], fs=5.6, c=WHITE if i == 0 else INK, fontweight="bold")
        nums = [str(m["n"]) for m in pts[p]]
        s = ", ".join(nums)
        if len(s) > 26:
            s = textwrap.shorten(s, 26, placeholder="…")
        label(ax, lx + 6.5, yy, s, fs=6.0, ha="left")
    save(fig, f"map_{key}")


if __name__ == "__main__":
    keys = sys.argv[1:] or list(KATA)
    import json
    info = {}
    for k in keys:
        info[k] = strips(k)
        embusen(k)
        print(k, info[k])
    json.dump(info, open(ROOT / "build" / "seqinfo.json", "w"))
