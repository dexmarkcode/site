from common import *


def fig14_1():
    fig, ax = canvas(h=2.8, ylim=(0, 62))
    # refrigerant circuit
    ax.add_patch(FancyBboxPatch((30, 34), 40, 24, boxstyle="round,pad=0,rounding_size=2", fc="none", ec=AMBER, lw=1.4, ls="-"))
    label(ax, 50, 59.5, "refrigerant circuit (heat pump)", fs=6.5, c=AMBER, fontweight="semibold")
    box(ax, 44, 52, 12, 6, "Compressor", fs=5.4, fc=PALE, ec=AMBER)
    box(ax, 53, 41, 14, 7, "Outdoor\nheat exch.", fs=5.4, fc="white", ec=AMBER)
    box(ax, 33, 41, 14, 7, "Cabin\ncondenser", fs=5.4, fc="white", ec=AMBER)
    box(ax, 34, 30, 12, 7, "Chiller", fs=5.8, fc=PALE, ec=AMBER)
    box(ax, 54, 30, 12, 7, "Water-cooled\ncondenser", fs=5.0, fc=PALE, ec=AMBER)
    # coolant loops
    box(ax, 2, 12, 22, 12, "Battery\ncold plates", fs=6.2, fc="white", ec=TEAL)
    box(ax, 76, 12, 22, 12, "Motor +\ninverter", fs=6.2, fc="white", ec=TEAL)
    box(ax, 39, 4, 22, 9, "Multi-way\ncoolant valve", fs=6.0, fc=NAVY, ec=NAVY, tc="white")
    box(ax, 76, 40, 22, 10, "Front-end\nradiator", fs=6.0, fc="white", ec=GREY)
    box(ax, 2, 40, 22, 10, "Cabin\n(HVAC module)", fs=6.0, fc="white", ec=GREY)
    for (x1, y1, x2, y2) in [(24, 18, 39, 9), (61, 9, 76, 18), (40, 30, 40, 13), (60, 30, 60, 13), (87, 24, 87, 40)]:
        line(ax, [x1, x2], [y1, y2], c=TEAL, lw=1.6)
    line(ax, [13, 13], [24, 33.5], c=TEAL, lw=1.6); line(ax, [13, 34], [33.5, 33.5], c=TEAL, lw=1.6)
    arrow(ax, 33, 44.5, 24, 44.5, c=RED, lw=1.2, ms=6); label(ax, 28.5, 47.5, "heat", fs=5.4, c=RED)
    label(ax, 50, 24, "coolant", fs=6, c=TEAL)
    label(ax, 15, 29, "battery loop", fs=5.5, c=TEAL, ha="left"); label(ax, 92, 30, "drive loop", fs=5.5, c=TEAL)
    save(fig, "fig14_1")


def fig14_2():
    T = np.linspace(-25, 15, 200)
    air = np.clip(1 + 2.2 / (1 + np.exp(-(T + 6) / 7)), 1.0, None)
    waste = air + 0.6 * (1 - (T + 25) / 50)
    fig, ax = plt.subplots(figsize=(W, 2.2))
    ax.plot(T, air, color=TEAL, lw=1.8, label="Air-source heat pump")
    ax.plot(T, waste, color=AMBER, lw=1.8, ls="--", label="With drive-unit waste heat")
    ax.axhline(1, color=RED, lw=1.0, ls=":"); ax.text(14, 1.07, "PTC heater (COP = 1)", fontsize=6.6, color=RED, ha="right")
    ax.set_xlabel("Ambient temperature (°C)"); ax.set_ylabel("COP")
    ax.set_xlim(-25, 15); ax.set_ylim(0.5, 3.8); ax.legend(loc="upper left")
    save(fig, "fig14_2")


def fig14_3():
    fig, ax = canvas(h=2.4, ylim=(0, 52))
    box(ax, 1, 34, 17, 12, "Item\ndefinition", fs=6.2)
    box(ax, 23, 34, 22, 12, "Hazard analysis\n& risk assessment", fs=6.0, fc=PALE, ec=AMBER)
    for i, (t, c) in enumerate([("Severity\nS0–S3", TEAL), ("Exposure\nE0–E4", TEAL), ("Control-\nlability\nC0–C3", TEAL)]):
        box(ax, 16 + i * 10.5, 17, 10, 11, t, fs=4.9, fc="white", ec=c)
    box(ax, 50, 34, 14, 12, "ASIL\nQM, A–D", fs=6.4, fc=NAVY, ec=NAVY, tc="white")
    box(ax, 69, 34, 14, 12, "Safety\ngoals", fs=6.4)
    box(ax, 50, 6, 48, 18, "", fc="white", ec=GREY)
    for i, t in enumerate(["Functional\nsafety\nrequirements", "Technical\nsafety\nrequirements", "Hardware &\nsoftware\nrequirements"]):
        box(ax, 52 + i * 15.5, 8.5, 14, 13, t, fs=4.9)
    for (x1, x2) in [(18, 23), (45, 50), (64, 69)]:
        arrow(ax, x1, 40, x2, 40, c=TEAL, lw=1.3, ms=6)
    arrow(ax, 34, 34, 34, 28, c=TEAL, lw=1.0, ms=5); arrow(ax, 45, 23, 55, 34, c=TEAL, lw=1.0, ms=5)
    arrow(ax, 76, 34, 76, 24, c=TEAL, lw=1.3, ms=6)
    label(ax, 28, 9, "ASIL from sum S+E+C:\n10→D, 9→C, 8→B, 7→A, ≤6→QM", fs=5.6, c=NAVY)
    save(fig, "fig14_3")


if __name__ == "__main__":
    fig14_1(); fig14_2(); fig14_3()
