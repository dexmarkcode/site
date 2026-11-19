"""Digital systems, computer systems, computer networks, software engineering templates."""
import math
import itertools
import ipaddress
from qcore import *

# =============================================================== DIGITAL SYSTEMS


@tpl("digital")
def base_conversion(rng):
    kind = rng.choice(["d2b", "h2d", "b2h", "d2h"])
    v = rng.randint(37, 250)
    if kind == "d2b":
        stem = f"What is the decimal number {v} in 8-bit binary?"
        corr = f"{v:08b}"
        wr = [f"{(v ^ (1 << rng.randint(0,3))):08b}", f"{int(f'{v:08b}'[::-1],2):08b}", f"{(v+1):08b}"]
        sol = (f"Subtract descending powers of two (128, 64, 32, 16, 8, 4, 2, 1), or divide repeatedly by 2 and read the remainders upwards: "
               f"${v}_{{10}} = {corr}_2$. Check: " + " + ".join(str(1 << (7 - i)) for i, b in enumerate(corr) if b == "1") + f" = {v}.")
        corr, wr = f"`{corr}`", [f"`{w}`" for w in wr]
    elif kind == "h2d":
        stem = f"What is the hexadecimal value 0x{v:02X} in decimal?"
        corr = str(v)
        hi, lo = divmod(v, 16)
        wr = [str(hi * 10 + lo), str(lo * 16 + hi), str(v + 16)]
        sol = f"$\\text{{{v:02X}}}_{{16}} = {hi}\\times16 + {lo} = {v}$. Each hex digit is worth 16 times the digit to its right; reading it as a decimal number is a common slip."
    elif kind == "b2h":
        v = rng.randint(4096, 65535)
        b = f"{v:016b}"
        stem = f"What is the binary number `{b[:4]} {b[4:8]} {b[8:12]} {b[12:]}` in hexadecimal?"
        corr = f"0x{v:04X}"
        wr = [f"0x{int(b[::-1],2):04X}", f"0x{v ^ 0x0100:04X}", f"0x{(v >> 4) | ((v & 0xF) << 12):04X}"]
        sol = f"Group into nibbles from the right and convert each: " + ", ".join(f"`{b[i:i+4]}` = {int(b[i:i+4],2):X}" for i in range(0, 16, 4)) + f", giving **{corr}**."
    else:
        stem = f"What is the decimal number {v} in hexadecimal?"
        corr = f"0x{v:02X}"
        hi, lo = divmod(v, 16)
        wr = [f"0x{lo:X}{hi:X}", f"0x{v//10:X}{v%10:X}", f"0x{(v+10):02X}"]
        sol = f"${v} \\div 16 = {hi}$ remainder ${lo}$, so the hex digits are {hi:X} and {lo:X}: **{corr}**."
    wr = [w for w in wr if w != corr]
    return make(stem, str_mcq(rng, corr, wr[:3] + ["0x00"] * (3 - len(wr[:3]))), sol)


@tpl("digital")
def twos_complement(rng):
    if rng.random() < 0.5:
        v = rng.randint(-120, -3)
        pat = f"{v & 0xFF:08b}"
        stem = f"How is the decimal value {v} represented as an 8-bit two's-complement number?"
        corr = f"`{pat}`"
        mag = f"{abs(v):08b}"
        ones = "".join("1" if c == "0" else "0" for c in mag)
        signmag = "1" + mag[1:]
        wr = [f"`{ones}`", f"`{signmag}`", f"`{mag}`"]
        sol = (f"Write $|{v}| = {abs(v)}$ in binary (`{mag}`), invert every bit (`{ones}`), then add 1: **`{pat}`**. "
               "The inverted form alone is the one's complement; setting only the top bit gives sign-magnitude.")
    else:
        u = rng.randint(129, 250)
        pat = f"{u:08b}"
        val = u - 256
        stem = f"The 8-bit register holds `{pat}`. What decimal value does this represent if it is interpreted as a two's-complement number?"
        corr = str(val).replace("-", MINUS)
        wr = [str(u), str(-(u - 128)).replace("-", MINUS), str(-(255 - u)).replace("-", MINUS)]
        sol = (f"The MSB is 1, so the number is negative. Its weight is $-128$: value $= -128 + {u-128} = {val}$. "
               f"Unsigned, the same pattern would be {u}.")
    return make(stem, str_mcq(rng, corr, [w for w in wr if w != corr]), sol)


@tpl("digital")
def overflow(rng):
    while True:
        a, b = rng.randint(-100, 120), rng.randint(-100, 120)
        if a != 0 and b != 0:
            break
    s = a + b
    ov = not (-128 <= s <= 127)
    res = (s & 0xFF)
    res_s = res - 256 if res > 127 else res
    stem = f"Two 8-bit two's-complement numbers, {a} and {b}, are added. What is the 8-bit result interpreted as signed, and is there overflow?"
    corr = f"{res_s}, {'overflow' if ov else 'no overflow'}".replace("-", MINUS)
    other = f"{res_s}, {'no overflow' if ov else 'overflow'}".replace("-", MINUS)
    wr = [other, f"{s}, {'overflow' if ov else 'no overflow'}".replace("-", MINUS) if s != res_s else f"{-res_s}, no overflow".replace("-", MINUS),
          f"{res}, no overflow" if res != res_s else f"{res_s + 1}, no overflow".replace("-", MINUS)]
    sol = (f"The true sum is {s}. An 8-bit signed register holds −128 to +127, so "
           + ("the sum does not fit and **overflow** occurs; the stored bits read as " + str(res_s) + "." if ov else "the sum fits: **no overflow**.")
           + " Overflow can occur only when both operands have the same sign and the result's sign differs from theirs.")
    return make(stem, str_mcq(rng, corr, [w for w in wr if w != corr]), sol)


@tpl("digital")
def counter_ff(rng):
    N = rng.choice([5, 10, 12, 24, 60, 100, 1000])
    n = math.ceil(math.log2(N))
    stem = f"What is the minimum number of flip-flops needed to build a synchronous mod-{N} counter?"
    sol = f"$n$ flip-flops give $2^n$ states, so we need $2^n \\ge {N}$: $2^{{{n-1}}} = {2**(n-1)} < {N} \\le 2^{{{n}}} = {2**n}$. Hence **{n}** flip-flops (unused states should be made to lead back into the count sequence)."
    return make(stem, num_mcq(rng, n, [n - 1, N // 2 if N // 2 != n else n + 2, int(math.log10(N)) + 1 if int(math.log10(N)) + 1 != n else n + 1], str, integer=True), sol)


@tpl("digital")
def memory_lines(rng):
    words = rng.choice([1024, 2048, 4096, 8192, 65536, 1 << 20])
    width = rng.choice([4, 8, 16])
    if rng.random() < 0.5:
        n = int(math.log2(words))
        stem = f"A memory chip is organised as {words:,} × {width} bits. How many address lines does it need?"
        sol = f"Address lines select a word: $2^n = {words:,}$ gives $n = {n}$. The word width ({width} bits) sets the number of *data* lines, not address lines."
        return make(stem, num_mcq(rng, n, [n + int(math.log2(width)), width, n - 1], str, integer=True), sol)
    chip_w, chip_b = rng.choice([(1024, 4), (2048, 8), (4096, 4), (8192, 8)])
    tw, tb = chip_w * rng.choice([2, 4, 8]), chip_b * rng.choice([1, 2])
    chips = (tw // chip_w) * (tb // chip_b)
    stem = f"How many {chip_w:,} × {chip_b} memory chips are needed to build a {tw:,} × {tb} memory?"
    sol = f"Depth: ${tw}/{chip_w} = {tw//chip_w}$ rows of chips. Width: ${tb}/{chip_b} = {tb//chip_b}$ chips side by side. Total $= {tw//chip_w}\\times{tb//chip_b} = {chips}$."
    return make(stem, num_mcq(rng, chips, [tw // chip_w, tb // chip_b if tb // chip_b != chips else chips * 2, chips + 2], str, integer=True), sol)


@tpl("digital")
def max_clock(rng):
    tcq, tlog, tsu = rng.choice([1, 2, 3, 5]), rng.choice([5, 8, 10, 12, 15, 20]), rng.choice([1, 2, 3])
    T = (tcq + tlog + tsu) * 1e-9
    f = 1 / T
    stem = (f"In a synchronous circuit the flip-flops have a clock-to-Q delay of {tcq} ns and a setup time of {tsu} ns. The longest combinational path between flip-flops is {tlog} ns. What is the maximum clock frequency?")
    sol = f"The clock period must cover launch, propagation and capture: $T_{{min}} = t_{{CQ}} + t_{{logic}} + t_{{su}} = {tcq} + {tlog} + {tsu} = {tcq+tlog+tsu}$ ns, so $f_{{max}} = 1/T_{{min}} = {em(f,'Hz')}$."
    return make(stem, num_mcq(rng, f, [1 / ((tcq + tlog) * 1e-9), 1 / (tlog * 1e-9), 1 / ((tcq + tlog + 2 * tsu) * 1e-9)], lambda v: eng(v, "Hz")), sol)


@tpl("digital")
def dac(rng):
    N = rng.choice([4, 8, 10])
    Vref = rng.choice([5.0, 10.0, 2.56, 3.3])
    code = rng.randint(3, 2 ** N - 2)
    V = Vref * code / 2 ** N
    bits = f"{code:0{N}b}"
    stem = f"An {N}-bit DAC has $V_{{out}} = V_{{ref}}\\,D/2^N$ with $V_{{ref}} = {fnum(Vref)}$ V. What output does the input code `{bits}` produce?"
    sol = f"`{bits}` = $D = {code}$. $V_{{out}} = {fnum(Vref)}\\times{code}/{2**N} = {em(V,'V',4)}$. The LSB step is ${em(Vref/2**N,'V',4)}$."
    return make(stem, num_mcq(rng, V, [Vref * code / (2 ** N - 1) * 1.02, Vref * int(bits[::-1], 2) / 2 ** N, Vref * code / 2 ** (N - 1) if Vref * code / 2 ** (N - 1) < Vref * 2 else V / 2], lambda v: eng(v, "V", 4)), sol)


@tpl("digital")
def mux_lines(rng):
    n = rng.choice([4, 8, 16, 32, 64])
    s = int(math.log2(n))
    if rng.random() < 0.5:
        stem = f"How many select lines does a {n}-to-1 multiplexer need?"
        sol = f"Select lines form a binary index into the inputs: $2^s = {n}$ gives $s = {s}$."
        return make(stem, num_mcq(rng, s, [n, n // 2, s + 1], str, integer=True), sol)
    stem = f"A decoder has {s} input lines. How many output lines does it drive (one active at a time)?"
    sol = f"A full $n$-to-$2^n$ decoder has $2^{{{s}}} = {n}$ outputs, one for each input combination."
    return make(stem, num_mcq(rng, n, [s * 2, n // 2, n * 2], str, integer=True), sol)


@tpl("digital")
def gray(rng):
    v = rng.randint(5, 15)
    b = f"{v:04b}"
    g = v ^ (v >> 1)
    corr = f"`{g:04b}`"
    stem = f"What is the 4-bit Gray code for binary `{b}`?"
    sol = (f"Keep the MSB, then XOR each adjacent pair of binary bits: $G = B \\oplus (B \\gg 1)$ = `{b}` ⊕ `{v>>1:04b}` = **`{g:04b}`**. "
           "Adjacent Gray codes differ in exactly one bit, which avoids glitches in shaft encoders.")
    wr = [f"`{(v ^ (v << 1)) & 0xF:04b}`", f"`{(~v) & 0xF:04b}`", f"`{(g ^ 1):04b}`"]
    return make(stem, str_mcq(rng, corr, [w for w in wr if w != corr] + ["`0000`"]), sol)


def _lit(var, pos):
    return var if pos else f"\\overline{{{var}}}"


def _term_str(t):
    return "".join(_lit(v, p) for v, p in t) or "1"


def _expr(terms):
    return " + ".join(_term_str(t) for t in terms) if terms else "0"


def _term_eval(t, assign):
    return all(assign[v] == p for v, p in t)


def _truth(terms, vars_):
    out = []
    for bits in itertools.product([0, 1], repeat=len(vars_)):
        a = {v: bool(b) for v, b in zip(vars_, bits)}
        out.append(any(_term_eval(t, a) for t in terms))
    return tuple(out)


@tpl("digital")
def kmap_min(rng):
    V = ["A", "B", "C"]
    cands = []
    for spec in itertools.product([None, True, False], repeat=3):
        t = tuple((v, p) for v, p in zip(V, spec) if p is not None)
        if t:
            cands.append(t)
    while True:
        ones = sorted(rng.sample(range(8), rng.randint(3, 5)))
        target = tuple(i in ones for i in range(8))
        imps = [t for t in cands if all(target[i] for i in range(8) if _truth([t], V)[i])]
        best = None
        for k in range(1, 4):
            for combo in itertools.combinations(imps, k):
                if _truth(list(combo), V) == target:
                    cost = (k, sum(len(t) for t in combo))
                    if best is None or cost < best[0]:
                        best = (cost, combo)
            if best:
                break
        if best and best[0][1] >= 2:
            break
    sol_terms = list(best[1])
    corr = f"$F = {_expr(sol_terms)}$"
    wrongs = []
    tries = 0
    while len(wrongs) < 3 and tries < 200:
        tries += 1
        t2 = [list(t) for t in sol_terms]
        i = rng.randrange(len(t2))
        op = rng.choice(["flip", "drop", "add"])
        if op == "flip" and t2[i]:
            j = rng.randrange(len(t2[i]))
            v, p = t2[i][j]
            t2[i][j] = (v, not p)
        elif op == "drop" and len(t2) > 1:
            t2.pop(i)
        else:
            used = {v for v, _ in t2[i]}
            free = [v for v in V if v not in used]
            if not free:
                continue
            t2[i].append((rng.choice(free), rng.choice([True, False])))
            t2[i].sort()
        t2 = [tuple(x) for x in t2]
        if _truth(t2, V) == target:
            continue
        s = f"$F = {_expr(t2)}$"
        if s != corr and s not in wrongs:
            wrongs.append(s)
    stem = f"What is the minimal sum-of-products expression for $F(A,B,C) = \\sum m({', '.join(map(str, ones))})$?"
    grid = "| $A\\backslash BC$ | 00 | 01 | 11 | 10 |\n|:-:|:-:|:-:|:-:|:-:|\n"
    for a in (0, 1):
        row = [str(int(target[a * 4 + bc])) for bc in (0, 1, 3, 2)]
        grid += f"| {a} | " + " | ".join(row) + " |\n"
    sol = (f"Plot the minterms on a three-variable K-map (columns in Gray-code order 00, 01, 11, 10):\n\n{grid}\n"
           f"Group the 1s into the largest possible power-of-two rectangles (wrapping around the edges is allowed). The minimal cover is {corr}. "
           "Each distractor differs from the target function in at least one cell, which you can confirm by evaluating it at a single minterm.")
    return make(stem, str_mcq(rng, corr, wrongs), sol)


@tpl("digital")
def shift_register(rng):
    init = rng.randint(0, 15)
    seq = [rng.randint(0, 1) for _ in range(3)]
    state = f"{init:04b}"
    hist = [state]
    for b in seq:
        state = str(b) + state[:-1]
        hist.append(state)
    corr = f"`{state}`"
    left = f"{init:04b}"
    for b in seq:
        left = left[1:] + str(b)
    wr = [f"`{left}`", f"`{''.join(map(str, seq[::-1]))}{f'{init:04b}'[0]}`", f"`{''.join(map(str, seq))}{f'{init:04b}'[-1]}`"]
    stem = (f"A 4-bit serial-in shift register (Q3 Q2 Q1 Q0) shifts right on each clock, entering the serial input at Q3. It starts at `{init:04b}` and the serial input is "
            f"{seq[0]}, {seq[1]}, {seq[2]} on three successive clocks. What are the contents afterwards?")
    sol = "Track each clock, shifting every bit one place right and inserting the new bit at the left: " + " → ".join(f"`{h}`" for h in hist) + f". Final: **{corr}**."
    return make(stem, str_mcq(rng, corr, [w for w in wr if w != corr] + ["`1111`", "`0000`"]), sol)


@tpl("digital")
def boolean_count(rng):
    exprs = [
        ("A\\overline{B} + BC", lambda a, b, c: (a and not b) or (b and c)),
        ("(A + B)\\overline{C}", lambda a, b, c: (a or b) and not c),
        ("A \\oplus B \\oplus C", lambda a, b, c: (a ^ b ^ c)),
        ("\\overline{A + B} + AC", lambda a, b, c: (not (a or b)) or (a and c)),
        ("AB + \\overline{A}C + BC", lambda a, b, c: (a and b) or ((not a) and c) or (b and c)),
        ("\\overline{AB}\\,C", lambda a, b, c: (not (a and b)) and c),
    ]
    e, f = rng.choice(exprs)
    cnt = sum(1 for a, b, c in itertools.product([0, 1], repeat=3) if f(a, b, c))
    rows = [(a, b, c) for a, b, c in itertools.product([0, 1], repeat=3) if f(a, b, c)]
    stem = f"For how many of the eight input combinations of $A, B, C$ is $F = {e}$ equal to 1?"
    sol = f"Evaluate the expression for all eight rows of the truth table. $F = 1$ for $ABC$ = " + ", ".join(f"{a}{b}{c}" for a, b, c in rows) + f": **{cnt}** rows."
    if "BC" in e and "\\overline{A}C" in e:
        sol += " (The $BC$ term is the consensus of the other two and is redundant.)"
    return make(stem, num_mcq(rng, cnt, [8 - cnt, cnt + 1, cnt - 1 if cnt > 1 else cnt + 2], str, integer=True), sol)


# =============================================================== COMPUTER SYSTEMS


@tpl("compsys")
def amat(rng):
    hit = rng.choice([1, 2])
    mr = rng.choice([0.02, 0.03, 0.05, 0.1])
    pen = rng.choice([50, 80, 100, 200])
    A = hit + mr * pen
    stem = f"A cache has a hit time of {hit} ns, a miss rate of {fnum(mr*100)}% and a miss penalty of {pen} ns. What is the average memory access time?"
    sol = f"$$\\text{{AMAT}} = t_{{hit}} + (\\text{{miss rate}})(\\text{{miss penalty}}) = {hit} + ({mnum(mr)})({pen}) = {mnum(A,3)}\\ \\text{{ns}}$$\n\nEvery access pays the hit time; only misses pay the penalty."
    return make(stem, num_mcq(rng, A, [mr * pen, (1 - mr) * hit + mr * pen, hit + pen * (1 - mr)], lambda v: fu(v, "ns")), sol)


@tpl("compsys")
def cpu_time(rng):
    IC = rng.choice([2, 5, 10, 50]) * 1e6
    CPI = rng.choice([1.2, 1.5, 2.0, 2.5, 3.0])
    f = rng.choice([500e6, 1e9, 2e9, 2.5e9])
    T = IC * CPI / f
    stem = f"A program executes {eng(IC,'')} instructions with an average CPI of {fnum(CPI)} on a {eng(f,'Hz')} processor. What is the execution time?".replace(" instructions", " instructions").replace(NBSP + " instructions", " instructions")
    sol = f"$$T = {frac('IC\\times CPI','f')} = {frac(f'({mnum(IC)})({fnum(CPI)})', mnum(f))} = {em(T,'s')}$$"
    return make(stem, num_mcq(rng, T, [IC / f, IC * CPI * f / 1e18, IC / (CPI * f)], lambda v: eng(v, "s")), sol)


@tpl("compsys")
def amdahl(rng):
    fpar = rng.choice([0.4, 0.5, 0.6, 0.75, 0.8, 0.9])
    k = rng.choice([2, 4, 8, 10, 16])
    S = 1 / ((1 - fpar) + fpar / k)
    stem = f"{int(fpar*100)}% of a program's run time can be sped up by a factor of {k}; the rest is unchanged. What is the overall speed-up?"
    sol = f"Amdahl's law: $$S = {frac(1,'(1 - f) + f/k')} = {frac(1, f'{mnum(1-fpar)} + {mnum(fpar)}/{k}')} = {mnum(S,3)}$$\n\nThe untouched {int((1-fpar)*100)}% caps the speed-up at $1/(1-f) = {mnum(1/(1-fpar),3)}$ however large $k$ becomes."
    return make(stem, num_mcq(rng, S, [fpar * k, float(k), 1 / (1 - fpar)], lambda v: fnum(v, 3) + "×"), sol)


@tpl("compsys")
def pipeline(rng):
    k = rng.choice([4, 5, 6, 8])
    n = rng.choice([10, 20, 50, 100, 1000])
    S = n * k / (k + n - 1)
    stem = f"An ideal {k}-stage pipeline (equal stage delays, no hazards) executes {n} instructions. What speed-up does it achieve over the unpipelined design?"
    sol = f"Unpipelined time: $nk$ stage-times. Pipelined: $k + (n-1)$ stage-times.\n\n$$S = {frac('nk','k + n - 1')} = {frac(f'{n}({k})', k+n-1)} = {mnum(S,4)}$$\n\nAs $n\\to\\infty$, $S\\to k$."
    return make(stem, num_mcq(rng, S, [float(k), n / (k + n - 1), n * k / (n + 1)], lambda v: fnum(v, 4)), sol)


@tpl("compsys")
def cache_bits(rng):
    addr = 32
    size = rng.choice([8, 16, 32, 64]) * 1024
    block = rng.choice([16, 32, 64])
    ways = rng.choice([1, 2, 4])
    sets = size // (block * ways)
    off = int(math.log2(block))
    idx = int(math.log2(sets))
    tag = addr - idx - off
    q = rng.choice(["tag", "index"])
    org = "direct-mapped" if ways == 1 else f"{ways}-way set-associative"
    stem = f"A {size//1024} KiB {org} cache with {block}-byte blocks serves a 32-bit byte-addressed memory. How many bits are in the {q} field?"
    sol = (f"Offset bits: $\\log_2 {block} = {off}$. Number of sets: ${size}/({block}\\times{ways}) = {sets}$, so index bits $= {idx}$. "
           f"Tag bits $= 32 - {idx} - {off} = {tag}$.")
    ans = tag if q == "tag" else idx
    wr = [32 - off - int(math.log2(size // block)), off, idx + off if q == "index" else tag + 2, idx + 1]
    return make(stem, num_mcq(rng, ans, wr, str, integer=True), sol)


@tpl("compsys")
def page_table(rng):
    va = rng.choice([32, 36, 40])
    pg = rng.choice([4, 8, 16]) * 1024
    pbits = int(math.log2(pg))
    entries = 2 ** (va - pbits)
    stem = f"A system uses {va}-bit virtual addresses and {pg//1024} KiB pages. How many entries does a single-level page table need?"
    sol = f"Offset within a page: $\\log_2({pg}) = {pbits}$ bits. The remaining ${va} - {pbits} = {va-pbits}$ bits are the virtual page number, so the table has $2^{{{va-pbits}}} = {entries:,}$ entries."
    return make(stem, num_mcq(rng, entries, [2 ** pbits, 2 ** (va - pbits - 1), 2 ** va // 1024], lambda v: f"{int(v):,}"), sol)


@tpl("compsys")
def avg_cpi(rng):
    mix = [(rng.choice([0.4, 0.5]), 1), (rng.choice([0.2, 0.3]), rng.choice([2, 3])), (None, rng.choice([4, 5]))]
    f3 = round(1 - mix[0][0] - mix[1][0], 2)
    mix[2] = (f3, mix[2][1])
    cpi = sum(f * c for f, c in mix)
    stem = (f"An instruction mix is {int(mix[0][0]*100)}% ALU (CPI 1), {int(mix[1][0]*100)}% load/store (CPI {mix[1][1]}) and {int(f3*100)}% branch (CPI {mix[2][1]}). What is the average CPI?")
    sol = f"Weight each class's CPI by its frequency: $\\text{{CPI}} = " + " + ".join(f"({f})({c})" for f, c in mix) + f" = {mnum(cpi,3)}$."
    return make(stem, num_mcq(rng, cpi, [sum(c for _, c in mix) / 3, float(max(c for _, c in mix)), cpi - 0.5], lambda v: fnum(v, 3)), sol)


@tpl("compsys")
def disk_access(rng):
    rpm = rng.choice([5400, 7200, 10000, 15000])
    seek = rng.choice([3, 4, 6, 8, 9])
    xfer = rng.choice([0.1, 0.2, 0.5])
    rot = 0.5 * 60 / rpm * 1000
    T = seek + rot + xfer
    stem = f"A {rpm:,} rpm disk has an average seek time of {seek} ms and a transfer time of {fnum(xfer)} ms for one sector. What is the average time to read a sector?"
    sol = f"Average rotational latency is half a revolution: $0.5\\times60/{rpm} = {mnum(rot,3)}$ ms.\n\n$$T = {seek} + {mnum(rot,3)} + {fnum(xfer)} = {mnum(T,3)}\\ \\text{{ms}}$$"
    return make(stem, num_mcq(rng, T, [seek + 2 * rot + xfer, seek + xfer, seek + rot], lambda v: fu(v, "ms")), sol)


# =============================================================== COMPUTER NETWORKS


@tpl("networks")
def subnet_hosts(rng):
    p = rng.choice([22, 24, 25, 26, 27, 28, 29, 30])
    h = 2 ** (32 - p) - 2
    stem = f"How many usable host addresses are available on a /{p} IPv4 subnet?"
    sol = f"There are $32 - {p} = {32-p}$ host bits, giving $2^{{{32-p}}} = {2**(32-p)}$ addresses. Subtract two (the network and broadcast addresses): **{h}** usable hosts."
    return make(stem, num_mcq(rng, h, [2 ** (32 - p), 2 ** (32 - p) - 1, 2 ** (32 - p - 1)], lambda v: f"{int(v):,}", integer=True), sol)


@tpl("networks")
def network_address(rng):
    p = rng.choice([20, 22, 26, 27, 28])
    ip = ipaddress.IPv4Address(f"{rng.choice([10,172,192])}.{rng.randint(0,255)}.{rng.randint(0,255)}.{rng.randint(1,254)}")
    net = ipaddress.IPv4Network(f"{ip}/{p}", strict=False)
    q = rng.choice(["network", "broadcast"])
    corr = str(net.network_address if q == "network" else net.broadcast_address)
    octs = str(ip).split(".")
    wr = [str(net.broadcast_address if q == "network" else net.network_address), ".".join(octs[:3] + ["0"]), ".".join(octs[:3] + ["255"]),
          str(ipaddress.IPv4Network(f"{ip}/{p+2}", strict=False).network_address)]
    stem = f"A host has address {ip}/{p}. What is the {q} address of its subnet?"
    sol = (f"The /{p} mask is {net.netmask}. The network address is the host address AND the mask: {net.network_address}. "
           f"The broadcast address sets all host bits to 1: {net.broadcast_address}. Answer: **{corr}**.")
    return make(stem, str_mcq(rng, corr, [w for w in dict.fromkeys(wr) if w != corr][:3]), sol)


@tpl("networks")
def subnet_mask(rng):
    p = rng.choice([19, 21, 23, 25, 26, 27, 28, 29])
    m = str(ipaddress.IPv4Network(f"0.0.0.0/{p}").netmask)
    wr = [str(ipaddress.IPv4Network(f"0.0.0.0/{p+1}").netmask), str(ipaddress.IPv4Network(f"0.0.0.0/{p-1}").netmask), str(ipaddress.IPv4Network(f"0.0.0.0/{p+8 if p<=24 else p-8}").netmask)]
    stem = f"What dotted-decimal subnet mask corresponds to the prefix /{p}?"
    sol = f"Write {p} ones followed by {32-p} zeros and convert each octet: **{m}**."
    return make(stem, str_mcq(rng, m, wr), sol)


@tpl("networks")
def delay(rng):
    Lb = rng.choice([500, 1000, 1500, 12000])
    Rr = rng.choice([1e6, 10e6, 100e6])
    d = rng.choice([100, 1000, 2000, 5000]) * 1e3
    v = 2e8
    tx = Lb * 8 / Rr
    tp = d / v
    T = tx + tp
    stem = (f"A {Lb:,}-byte packet is sent over a {eng(Rr,'bit/s')} link {d/1e3:,.0f} km long (propagation speed $2\\times10^8$ m/s). "
            "Ignoring queueing and processing, how long from the first bit leaving the sender until the last bit arrives?")
    sol = f"Transmission delay $L/R = {Lb*8:,}\\ \\text{{bits}}/{mnum(Rr)} = {em(tx,'s',4)}$. Propagation delay $d/v = {em(tp,'s',4)}$. Total $= {em(T,'s')}$."
    return make(stem, num_mcq(rng, T, [Lb / Rr + tp, tx, tp], lambda v: eng(v, "s")), sol)


@tpl("networks")
def stop_wait(rng):
    Lb = rng.choice([1000, 1500, 4000])
    Rr = rng.choice([1e6, 10e6, 100e6])
    tp = rng.choice([1, 5, 10, 20]) * 1e-3
    tx = Lb * 8 / Rr
    U = tx / (tx + 2 * tp)
    stem = f"A stop-and-wait protocol sends {Lb:,}-byte frames over a {eng(Rr,'bit/s')} link with a one-way propagation delay of {eng(tp,'s')}. Ignoring ACK transmission time, what is the link utilisation?"
    sol = f"$t_{{tx}} = {em(tx,'s',4)}$. Each frame occupies one transmission time plus a round trip: $U = t_{{tx}}/(t_{{tx}} + 2t_p) = {mnum(U*100,3)}\\%$. Sliding-window protocols exist precisely to fill this idle pipe."
    return make(stem, num_mcq(rng, U * 100, [tx / (tx + tp) * 100, tx / (2 * tp) * 100 if tx < 2 * tp else U * 50, U * 200], lambda v: fnum(v, 3) + "%"), sol)


# =============================================================== SOFTWARE ENGINEERING


def code(lines):
    return "```\n" + "\n".join(lines) + "\n```"


@tpl("software")
def loop_trace(rng):
    kind = rng.choice(["sum", "nested", "halve", "prod"])
    if kind == "sum":
        a, b, s = rng.choice([1, 2, 3]), rng.choice([10, 12, 15, 20]), rng.choice([2, 3])
        vals = list(range(a, b + 1, s))
        out = sum(vals)
        src = code(["total = 0", f"for i = {a} to {b} step {s}", "    total = total + i", "end for", "print total"])
        how = f"$i$ takes the values {', '.join(map(str, vals))}; their sum is **{out}**."
        wr = [sum(range(a, b + 1)), out - vals[-1], out + b + s]
    elif kind == "nested":
        n, m = rng.choice([3, 4, 5]), rng.choice([2, 3, 4])
        out = sum(1 for i in range(1, n + 1) for j in range(i, m + 1))
        src = code(["count = 0", f"for i = 1 to {n}", f"    for j = i to {m}", "        count = count + 1", "    end for", "end for", "print count"])
        how = "For each $i$ the inner loop runs $\\max(0, " + str(m) + " - i + 1)$ times: " + " + ".join(str(max(0, m - i + 1)) for i in range(1, n + 1)) + f" = **{out}**. Note the inner loop does not execute at all once $i > {m}$."
        wr = [n * m, n * m // 2, out + 1]
    elif kind == "halve":
        n = rng.choice([100, 64, 1000, 37, 250])
        c, x = 0, n
        while x > 1:
            x //= 2
            c += 1
        out = c
        src = code([f"x = {n}", "c = 0", "while x > 1", "    x = x div 2      // integer division", "    c = c + 1", "end while", "print c"])
        how = f"Repeated halving of {n} reaches 1 after $\\lfloor\\log_2 {n}\\rfloor = {c}$ iterations. Loops like this are $O(\\log n)$."
        wr = [n // 2, c + 1, c - 1]
    else:
        n = rng.choice([4, 5, 6])
        out = 1
        for i in range(1, n + 1, 2):
            out *= i
        src = code(["p = 1", f"for k = 1 to {n} step 2", "    p = p * k", "end for", "print p"])
        how = f"$k$ = {', '.join(str(i) for i in range(1, n+1, 2))}; the product is **{out}**."
        wr = [math.factorial(n), out * 2, out + n]
    stem = "What does the following pseudocode print?\n\n" + src
    return make(stem, num_mcq(rng, out, wr, str, integer=True), how + " Trace loops with a small table of variable values; it is quicker and safer than doing it in your head.")


@tpl("software")
def binary_search(rng):
    n = rng.choice([100, 500, 1000, 1024, 5000, 10**6])
    c = math.floor(math.log2(n)) + 1
    stem = f"What is the maximum number of comparisons a binary search needs to find an item (or establish that it is absent) in a sorted array of {n:,} elements?"
    sol = f"Each comparison halves the search interval: the worst case is $\\lfloor\\log_2 {n:,}\\rfloor + 1 = {c}$ comparisons. A linear search could need {n:,}."
    return make(stem, num_mcq(rng, c, [n // 2, c - 1, c + 2], lambda v: f"{int(v):,}", integer=True), sol)


@tpl("software")
def stack_queue(rng):
    ops = []
    pushed = 0
    items = list("ABCDEFG")
    seq = []
    for _ in range(7):
        if pushed < len(items) and (not seq or rng.random() < 0.6):
            seq.append(("push", items[pushed]))
            pushed += 1
        else:
            seq.append(("pop", None))
    kind = rng.choice(["stack", "queue"])
    ds = []
    popped = []
    for op, x in seq:
        if op == "push":
            ds.append(x)
        elif ds:
            popped.append(ds.pop() if kind == "stack" else ds.pop(0))
    if not popped:
        return stack_queue(rng)
    verb = ("push", "pop") if kind == "stack" else ("enqueue", "dequeue")
    oplist = ", ".join(f"{verb[0]}({x})" if op == "push" else f"{verb[1]}()" for op, x in seq)
    stem = f"Starting with an empty {kind}, the operations {oplist} are performed. In what order are items removed?"
    corr = ", ".join(popped)
    # alternative behaviour as distractor
    ds2, alt = [], []
    for op, x in seq:
        if op == "push":
            ds2.append(x)
        elif ds2:
            alt.append(ds2.pop(0) if kind == "stack" else ds2.pop())
    wr = [", ".join(alt), ", ".join(popped[::-1]), ", ".join(sorted(popped, reverse=True))]
    if len(popped) == 1:
        wr = [items[0] if popped[0] != items[0] else items[1], items[2], items[3]]
    sol = f"A {kind} is {'LIFO (last in, first out)' if kind=='stack' else 'FIFO (first in, first out)'}. Tracing the operations, the removed items are **{corr}**."
    return make(stem, str_mcq(rng, corr, [w for w in dict.fromkeys(wr) if w != corr] + ["G", "F, G"]), sol)


@tpl("software")
def recursion(rng):
    a, b = rng.choice([1, 2]), rng.choice([1, 2, 3])
    f0, f1 = rng.choice([0, 1]), rng.choice([1, 2])
    n = rng.choice([5, 6])
    vals = [f0, f1]
    for i in range(2, n + 1):
        vals.append(a * vals[-1] + b * vals[-2])
    src = code([f"function f(n)", f"    if n == 0 return {f0}", f"    if n == 1 return {f1}", f"    return {a if a>1 else ''}{'*' if a>1 else ''}f(n-1) + {b if b>1 else ''}{'*' if b>1 else ''}f(n-2)", "end function"])
    stem = f"Given the recursive function below, what is f({n})?\n\n{src}"
    sol = "Build the values bottom-up rather than expanding the recursion tree: " + ", ".join(f"f({i}) = {v}" for i, v in enumerate(vals)) + f". So f({n}) = **{vals[n]}**."
    return make(stem, num_mcq(rng, vals[n], [vals[n - 1], vals[n] + vals[n - 2], vals[n - 1] * 2 + 1], str, integer=True), sol)


@tpl("software")
def array_address(rng):
    rows, cols = rng.choice([(10, 20), (8, 16), (50, 40), (5, 12)])
    es = rng.choice([2, 4, 8])
    base = rng.choice([1000, 2000, 4096, 0x1000])
    i, j = rng.randint(1, rows - 1), rng.randint(1, cols - 1)
    addr = base + (i * cols + j) * es
    stem = (f"A {rows} × {cols} array `A` of {es}-byte elements is stored in row-major order starting at address {base}, with zero-based indices. What is the address of `A[{i}][{j}]`?")
    sol = f"Row-major: $\\text{{addr}} = \\text{{base}} + (i\\cdot\\text{{cols}} + j)\\times\\text{{size}} = {base} + ({i}\\cdot{cols} + {j})\\times{es} = {addr}$."
    wr = [base + (j * rows + i) * es, base + (i * cols + j), base + ((i + 1) * cols + j + 1) * es]
    return make(stem, num_mcq(rng, addr, wr, lambda v: f"{int(v):,}", integer=True), sol)


@tpl("software")
def inversions(rng):
    arr = rng.sample(range(1, 10), 5)
    inv = sum(1 for i in range(5) for j in range(i + 1, 5) if arr[i] > arr[j])
    stem = f"How many swaps does a standard bubble sort perform to sort the list [{', '.join(map(str, arr))}] into ascending order?"
    sol = f"Each bubble-sort swap removes exactly one inversion (a pair out of order), so the count equals the number of inversions: **{inv}**. Listing pairs with the larger value first gives the same total."
    return make(stem, num_mcq(rng, inv, [10, inv + 2, max(inv - 1, 0) if inv > 1 else inv + 3], str, integer=True), sol)


@tpl("software")
def complexity(rng):
    pats = [
        (["for i = 1 to n", "    for j = 1 to n", "        x = x + 1"], "$O(n^2)$"),
        (["i = n", "while i > 1", "    i = i / 2"], "$O(\\log n)$"),
        (["for i = 1 to n", "    j = 1", "    while j < n", "        j = j * 2"], "$O(n\\log n)$"),
        (["for i = 1 to n", "    x = x + i", "for j = 1 to n", "    y = y + j"], "$O(n)$"),
        (["for i = 1 to n", "    for j = 1 to i", "        for k = 1 to 10", "            x = x + 1"], "$O(n^2)$"),
    ]
    lines, corr = rng.choice(pats)
    allc = ["$O(n)$", "$O(n^2)$", "$O(\\log n)$", "$O(n\\log n)$", "$O(n^3)$", "$O(2^n)$"]
    stem = "What is the time complexity of the following fragment as a function of $n$?\n\n" + code(lines)
    sol = {"$O(n^2)$": "The work grows with the product of two loop counts that each scale with $n$ (constant factors such as 10 are dropped).",
           "$O(\\log n)$": "The loop variable is halved each time, so the loop runs about $\\log_2 n$ times.",
           "$O(n\\log n)$": "An outer loop of $n$ iterations contains an inner loop that doubles its variable, running about $\\log_2 n$ times.",
           "$O(n)$": "Two loops in *sequence* add ($n + n = 2n$); only *nested* loops multiply."}[corr]
    return make(stem, str_mcq(rng, corr, [c for c in allc if c != corr][:4] and rng.sample([c for c in allc if c != corr], 3)), sol + f" Answer: {corr}.")
