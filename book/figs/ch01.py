from common import *


def fig1_1():
    fig, axs = plt.subplots(1, 4, figsize=(W, 2.5))
    titles = ["Conventional", "Parallel hybrid", "Plug-in / series", "Battery electric"]
    for ax, t in zip(axs, titles):
        ax.set_xlim(0, 30); ax.set_ylim(0, 52); ax.axis("off"); ax.set_aspect("equal")
        ax.set_title(t, fontsize=7.2, color=NAVY, fontweight="semibold", pad=2)
        # wheels
        for x in (6, 24):
            ax.add_patch(Circle((x, 5), 3.2, fc=NAVY, ec="none"))
        line(ax, [6, 24], [5, 5], c=GREY, lw=2)
    # conventional
    a = axs[0]
    box(a, 8, 34, 14, 9, "Engine", fc=PALE, ec=AMBER, tc=NAVY, fs=6.5)
    box(a, 9, 20, 12, 7, "Gearbox", fs=6)
    box(a, 1, 44, 9, 6, "Fuel", fc="white", ec=GREY, tc=GREY, fs=6, bold=False)
    arrow(a, 15, 34, 15, 27, c=GREY); arrow(a, 15, 20, 15, 6, c=GREY)
    # parallel hybrid
    a = axs[1]
    box(a, 2, 34, 12, 9, "Engine", fc=PALE, ec=AMBER, fs=6.5)
    box(a, 16, 34, 12, 9, "Motor", fs=6.5)
    box(a, 16, 46, 12, 6, "Battery", fc="white", ec=TEAL, tc=TEAL, fs=6)
    box(a, 9, 20, 12, 7, "Gearbox", fs=6)
    arrow(a, 8, 34, 12, 27, c=GREY); arrow(a, 22, 34, 18, 27, c=GREY)
    arrow(a, 22, 46, 22, 43, c=TEAL, both=True, ms=5)
    arrow(a, 15, 20, 15, 6, c=GREY)
    # series / PHEV
    a = axs[2]
    box(a, 1, 40, 12, 8, "Engine", fc=PALE, ec=AMBER, fs=6.5)
    box(a, 1, 28, 12, 8, "Gen.", fs=6.5)
    box(a, 16, 34, 13, 9, "Battery", fc="white", ec=TEAL, tc=TEAL, fs=6.5)
    box(a, 9, 15, 13, 8, "Motor", fs=6.5)
    arrow(a, 7, 40, 7, 36, c=GREY); arrow(a, 13, 32, 16, 37, c=TEAL); arrow(a, 7, 28, 13, 23, c=TEAL)
    arrow(a, 22, 34, 18, 23, c=TEAL, both=True); arrow(a, 15.5, 15, 15.5, 6, c=GREY)
    label(a, 22.5, 47.5, "plug", fs=6, c=TEAL); arrow(a, 22.5, 46, 22.5, 43, c=TEAL, lw=1)
    # BEV
    a = axs[3]
    box(a, 4, 34, 22, 10, "Battery", fc="white", ec=TEAL, tc=TEAL, fs=7)
    box(a, 8, 22, 14, 7, "Inverter", fs=6)
    box(a, 8, 12, 14, 7, "Motor", fs=6.5)
    arrow(a, 15, 34, 15, 29, c=TEAL, both=True); arrow(a, 15, 22, 15, 19, c=TEAL, both=True)
    arrow(a, 15, 12, 15, 6, c=GREY)
    label(a, 15, 48.5, "plug", fs=6, c=TEAL); arrow(a, 15, 47, 15, 44, c=TEAL, lw=1)
    fig.subplots_adjust(wspace=0.08)
    save(fig, "fig1_1")


def fig1_2():
    fig, ax = canvas(h=3.1, ylim=(0, 68))
    hv = dict(c=TEAL, lw=2.2)
    box(ax, 1, 4, 24, 16, "Traction battery\n+ BMS", fc="white", ec=TEAL, tc=NAVY, fs=7.5)
    box(ax, 31, 4, 24, 16, "HV junction box\ncontactors, fuses,\npre-charge", fs=6.2)
    box(ax, 61, 4, 16, 16, "Traction\ninverter", fs=7)
    box(ax, 83, 4, 16, 16, "Motor +\nreduction\ngear", fs=6.5)
    box(ax, 31, 30, 24, 11, "On-board\ncharger (AC)", fs=6.5)
    box(ax, 61, 30, 16, 11, "DC-DC\nconverter", fs=6.5)
    box(ax, 83, 30, 16, 11, "12 V net\n+ battery", fs=6.5, fc=PALE, ec=AMBER)
    box(ax, 1, 30, 24, 11, "Thermal system\npumps, chiller,\nheat pump", fs=5.8, fc="white", ec=GREY, tc=NAVY)
    box(ax, 36, 52, 40, 11, "Vehicle control unit (VCU)", fs=7.5, fc=NAVY, ec=NAVY, tc="white")
    box(ax, 1, 52, 24, 11, "Charge inlet\nAC / DC", fs=6.5, fc="white", ec=TEAL, tc=TEAL)
    arrow(ax, 25, 12, 31, 12, both=True, **hv); arrow(ax, 55, 12, 61, 12, both=True, **hv)
    arrow(ax, 77, 12, 83, 12, both=True, **hv)
    arrow(ax, 43, 30, 43, 20, **hv); arrow(ax, 55, 18, 64, 30, **hv)
    arrow(ax, 77, 35.5, 83, 35.5, c=AMBER, lw=1.6)
    arrow(ax, 25, 57.5, 30, 57.5, c=TEAL, lw=1.4); line(ax, [30, 30], [57.5, 42.5], c=TEAL, lw=1.4)
    arrow(ax, 30, 42.5, 36, 41.2, c=TEAL, lw=1.4)
    line(ax, [27.5, 27.5], [52, 24], c=TEAL, lw=1.4, ls=(0, (3, 2)))
    arrow(ax, 27.5, 24, 31, 19, c=TEAL, lw=1.4, ls="--")
    label(ax, 27, 47, "AC", fs=5.8, c=TEAL, ha="right")
    label(ax, 26.5, 26.5, "DC fast\ncharge", fs=5.4, c=TEAL, ha="right")
    for x in (13, 43, 69, 91):
        line(ax, [56, x], [52, 41], c=GREY, lw=0.6, ls=(0, (2, 2)))
    label(ax, 88, 49, "CAN / Ethernet", fs=5.5, c=GREY)
    save(fig, "fig1_2")


def fig1_3():
    stages = ["Grid", "On-board\ncharger", "Battery\n(charge)", "Battery\n(discharge)", "Inverter", "Motor", "Gear", "Wheels"]
    eff = [1, 0.93, 0.97, 0.97, 0.96, 0.92, 0.97]
    vals = [100]
    for e in eff[1:]:
        vals.append(vals[-1] * e)
    vals.append(vals[-1])
    fig, ax = plt.subplots(figsize=(W, 2.5))
    cols = [NAVY] + [TEAL] * 6 + [AMBER]
    ax.bar(range(len(vals)), vals, color=cols, width=0.62)
    for i, v in enumerate(vals):
        ax.text(i, v + 1.5, f"{v:.0f}", ha="center", fontsize=7.5, color=NAVY, fontweight="semibold")
        if 0 < i < 7:
            loss = vals[i - 1] - vals[i]
            ax.text(i, 5, f"−{loss:.1f}", ha="center", fontsize=6.3, color="white")
    ax.set_xticks(range(len(vals))); ax.set_xticklabels(stages, fontsize=6.5)
    ax.set_ylabel("Energy remaining (% of grid input)"); ax.set_ylim(0, 110)
    ax.grid(axis="x", visible=False)
    ax.axhline(25, color=RED, lw=0.8, ls="--")
    ax.text(7.45, 27, "typical petrol car\ntank-to-wheel ≈ 25 %", fontsize=6.2, color=RED, ha="right", va="bottom")
    save(fig, "fig1_3")


def fig1_4():
    fig, ax = canvas(h=2.6, ylim=(0, 58))
    left = [("Vehicle\nrequirements", 2, 44), ("System\nrequirements", 12, 32), ("Component\nrequirements", 22, 20)]
    right = [("Vehicle\nvalidation", 76, 44), ("System\nintegration test", 66, 32), ("Component\ntest", 56, 20)]
    for t, x, y in left:
        box(ax, x, y, 22, 9, t, fs=6.5)
    for t, x, y in right:
        box(ax, x, y, 22, 9, t, fs=6.5, fc=PALE, ec=AMBER)
    box(ax, 38, 5, 24, 9, "Design & build", fs=7, fc=NAVY, ec=NAVY, tc="white")
    arrow(ax, 13, 44, 20, 41, c=TEAL); arrow(ax, 23, 32, 30, 29, c=TEAL); arrow(ax, 33, 20, 40, 14, c=TEAL)
    arrow(ax, 60, 14, 66, 20, c=AMBER); arrow(ax, 70, 29, 75, 32, c=AMBER); arrow(ax, 80, 41, 85, 44, c=AMBER)
    for (t, x, y), (t2, x2, y2) in zip(left, right):
        line(ax, [x + 22, x2], [y + 4.5, y2 + 4.5], c=GREY, lw=0.6, ls=(0, (2, 2)))
    label(ax, 50, 52, "verification links", fs=6, c=GREY)
    label(ax, 9, 56, "Decompose & specify", fs=6.5, c=TEAL, fontweight="semibold")
    label(ax, 89, 56, "Integrate & verify", fs=6.5, c=AMBER, fontweight="semibold")
    save(fig, "fig1_4")


if __name__ == "__main__":
    fig1_1(); fig1_2(); fig1_3(); fig1_4()
