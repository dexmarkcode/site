"""Assemble all 800 questions into Markdown fragments in build/q/."""
import os
import random
import json
from collections import Counter, OrderedDict

import t_math, t_circuits, t_sig, t_power, t_digital  # noqa: F401  (registers templates)
from qcore import REG, Q, str_mcq
from concepts import C

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "build", "q")
os.makedirs(OUT, exist_ok=True)

NAMES = OrderedDict([
    ("math", "Mathematics"), ("prob", "Probability and Statistics"), ("ethics", "Ethics and Professional Practice"),
    ("econ", "Engineering Economics"), ("materials", "Properties of Electrical Materials"), ("dc", "Circuit Analysis (DC)"),
    ("ac", "Circuit Analysis (AC)"), ("linsys", "Linear Systems"), ("signal", "Signal Processing"), ("electronics", "Electronics"),
    ("power", "Power Systems"), ("em", "Electromagnetics"), ("control", "Control Systems"), ("comms", "Communications"),
    ("networks", "Computer Networks"), ("digital", "Digital Systems"), ("compsys", "Computer Systems"), ("software", "Software Engineering"),
])

RATIO = {"ethics": 1.0, "networks": 0.5, "software": 0.42, "compsys": 0.35, "materials": 0.35, "digital": 0.22,
         "em": 0.14, "signal": 0.14, "electronics": 0.12, "power": 0.14, "control": 0.14, "comms": 0.14, "prob": 0.1, "econ": 0.12}

MASTER = random.Random(20262027)


class Pool:
    def __init__(self, topic):
        self.topic = topic
        self.tpls = list(REG.get(topic, []))
        MASTER.shuffle(self.tpls)
        self.ti = 0
        self.concepts = list(C.get(topic, []))
        MASTER.shuffle(self.concepts)

    def draw(self):
        use_c = self.concepts and (not self.tpls or MASTER.random() < RATIO.get(self.topic, 0))
        if use_c:
            stem, corr, wr, expl = self.concepts.pop()
            opts, ans = str_mcq(MASTER, corr, wr)
            return Q(stem=stem, options=opts, answer=ans, solution=expl, topic=self.topic, tid="concept")
        if not self.tpls:
            raise RuntimeError(f"pool {self.topic} exhausted")
        f = self.tpls[self.ti % len(self.tpls)]
        self.ti += 1
        for attempt in range(25):
            try:
                q = f(random.Random(MASTER.randrange(10 ** 9)))
                if len(set(q.options)) == 4:
                    q.topic, q.tid = self.topic, f.__name__
                    return q
            except Exception:
                continue
        raise RuntimeError(f"template {f.__name__} failed repeatedly")


POOLS = {t: Pool(t) for t in NAMES}
LET = "ABCD"


def render(qs, prefix, title_q=None, grouped=False, sections=False):
    qmd, amd = [], []
    last = None
    for i, q in enumerate(qs, 1):
        num = f"{prefix}{i}"
        if sections and i in (1, 56):
            label = 'Section 1: Questions 1–55' if i == 1 else 'Section 2: Questions 56–110'
            qmd.append(f"\n## {label} {{.unnumbered}}\n")
            if i == 56:
                qmd.insert(len(qmd) - 1, '\n::: {.tip title="Scheduled Break"}\nYou have reached the end of Section 1. On the real exam you would now submit this section and could not return to it. Take a break of up to 25 minutes, then continue.\n:::\n')
        if grouped and q.topic != last:
            qmd.append(f"\n### {NAMES[q.topic]} {{.unnumbered .qgroup}}\n")
            last = q.topic
        block = [f"::: {{.question}}", f"**{num}** {q.stem}", ""]
        if q.fig:
            block += [f"![]({q.fig}){{width=62%}}", ""]
        for k, o in enumerate(q.options):
            block.append(f"({LET[k]}) {o}")
        block.append(":::")
        qmd.append("\n".join(block) + "\n")
        amd.append("\n".join([
            "::: {.solution}",
            f"**{num} Answer ({LET[q.answer]})** [{NAMES[q.topic]}]{{.qtopic}}",
            "",
            q.solution,
            ":::",
        ]) + "\n")
    return "\n".join(qmd), "\n".join(amd)


def build(name, plan, prefix, grouped=False, shuffle=False, sections=False):
    qs = []
    for topic, n in plan:
        for _ in range(n):
            qs.append(POOLS[topic].draw())
    if shuffle:
        MASTER.shuffle(qs)
    qtext, atext = render(qs, prefix, grouped=grouped, sections=sections)
    open(os.path.join(OUT, f"{name}_q.md"), "w").write(qtext)
    open(os.path.join(OUT, f"{name}_a.md"), "w").write(atext)
    return qs


def answer_key(qs, name, prefix=""):
    rows = []
    per = (len(qs) + 1) // 2
    hdr = "| Q | Ans | Knowledge area | Q | Ans | Knowledge area |\n|:-:|:-:|:--------|:-:|:-:|:--------|\n"
    for r in range(per):
        cells = []
        for c in range(2):
            idx = c * per + r
            if idx < len(qs):
                q = qs[idx]
                cells += [f"{prefix}{idx+1}", LET[q.answer], NAMES[q.topic]]
            else:
                cells += ["", "", ""]
        rows.append("| " + " | ".join(cells) + " |")
    # score sheet by area
    cnt = Counter(q.topic for q in qs)
    sheet = "| Knowledge area | Questions | Your score | Percentage |\n|:--|:-:|:-:|:-:|\n"
    for t in NAMES:
        if cnt[t]:
            sheet += f"| {NAMES[t]} | {cnt[t]} | ___ | ___ % |\n"
    sheet += f"| **Total** | **{len(qs)}** | ___ | ___ % |\n"
    open(os.path.join(OUT, f"{name}_key.md"), "w").write(hdr + "\n".join(rows) + "\n")
    open(os.path.join(OUT, f"{name}_sheet.md"), "w").write(sheet)


DIAG = [("math", 2), ("prob", 1), ("ethics", 1), ("econ", 1), ("materials", 1), ("dc", 2), ("ac", 2), ("linsys", 1), ("signal", 1),
        ("electronics", 1), ("power", 1), ("em", 1), ("control", 1), ("comms", 1), ("networks", 1), ("digital", 1), ("compsys", 1)]
CHAPTERS = {
    "ch02": [("math", 36)],
    "ch03": [("prob", 13), ("econ", 13), ("ethics", 10)],
    "ch04": [("dc", 30), ("materials", 6)],
    "ch05": [("ac", 36)],
    "ch06": [("linsys", 36)],
    "ch07": [("signal", 36)],
    "ch08": [("electronics", 36)],
    "ch09": [("em", 24), ("materials", 12)],
    "ch10": [("power", 36)],
    "ch11": [("control", 36)],
    "ch12": [("comms", 36)],
    "ch13": [("digital", 36)],
    "ch14": [("compsys", 20), ("networks", 16)],
    "ch15": [("software", 36)],
}
DRILL = [("math", 6), ("prob", 3), ("ethics", 2), ("econ", 2), ("materials", 2), ("dc", 4), ("ac", 5), ("linsys", 3), ("signal", 3),
         ("electronics", 4), ("power", 4), ("em", 3), ("control", 3), ("comms", 3), ("networks", 2), ("digital", 4), ("compsys", 2), ("software", 1)]
MOCK = [("math", 12), ("prob", 5), ("ethics", 4), ("econ", 4), ("materials", 5), ("dc", 7), ("ac", 9), ("linsys", 5), ("signal", 5),
        ("electronics", 7), ("power", 8), ("em", 5), ("control", 6), ("comms", 5), ("networks", 4), ("digital", 8), ("compsys", 6), ("software", 5)]

if __name__ == "__main__":
    total = 0
    stats = {}
    qs = build("ch01", DIAG, "D", shuffle=False)
    total += len(qs)
    for ch, plan in CHAPTERS.items():
        n = int(ch[2:])
        qs = build(ch, plan, f"{n}.", grouped=len(plan) > 1)
        total += len(qs)
    qs = build("ch16", DRILL, "16.", shuffle=False)
    total += len(qs)
    for m in (1, 2):
        qs = build(f"mock{m}", MOCK, "", shuffle=False, sections=True)
        answer_key(qs, f"mock{m}")
        total += len(qs)
        stats[f"mock{m}"] = Counter(LET[q.answer] for q in qs)
    leftovers = {t: len(p.concepts) for t, p in POOLS.items() if p.concepts}
    print("TOTAL QUESTIONS:", total)
    print("unused concept items:", leftovers)
    print("mock answer letter spread:", stats)
