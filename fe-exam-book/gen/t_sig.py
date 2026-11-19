"""Signal processing, electronics and electromagnetics templates."""
import math
from qcore import *

PI = math.pi
EPS0 = 8.854e-12
MU0 = 4 * PI * 1e-7
C0 = 3e8
K_E = 8.99e9


def deg(v, sig=3):
    return fnum(v, sig) + "°"


def par(a, b):
    return a * b / (a + b)


# =============================================================== SIGNAL PROCESSING


@tpl("signal")
def nyquist_rate(rng):
    f1, f2 = rng.choice([(1, 3), (2, 5), (4, 10), (3, 8), (6, 15)])
    kind = rng.choice(["sum", "product"])
    if kind == "sum":
        expr = f"x(t) = 3\\cos(2\\pi\\cdot{f1}000\\,t) + \\sin(2\\pi\\cdot{f2}000\\,t)"
        fmax = f2 * 1000
        why = f"The highest frequency present is {f2} kHz."
        wr = [2 * f1 * 1000, f2 * 1000, 2 * (f1 + f2) * 1000]
    else:
        expr = f"x(t) = \\cos(2\\pi\\cdot{f1}000\\,t)\\,\\cos(2\\pi\\cdot{f2}000\\,t)"
        fmax = (f1 + f2) * 1000
        why = (f"A product of cosines contains sum and difference frequencies: "
               f"$\\cos A\\cos B = \\tfrac12[\\cos(A-B) + \\cos(A+B)]$, giving {f2-f1} kHz and {f1+f2} kHz. The highest is {f1+f2} kHz.")
        wr = [2 * f2 * 1000, (f1 + f2) * 1000, 2 * (f2 - f1) * 1000]
    fs = 2 * fmax
    stem = f"What is the minimum (Nyquist) sampling rate for the signal ${expr}$?"
    sol = (f"{why} The Nyquist rate is twice the highest frequency:\n\n$$f_s = 2f_{{max}} = {em(fs,'Hz')}$$\n\n"
           "In practice you sample comfortably above this, because real anti-aliasing filters are not brick walls.")
    return make(stem, num_mcq(rng, fs, wr, lambda v: eng(v, "Hz")), sol)


@tpl("signal")
def aliasing(rng):
    fs = rng.choice([8000, 10000, 20000, 44100, 1000])
    f = fs * rng.choice([0.6, 0.7, 0.85, 1.2, 1.35, 0.9])
    f = round(f / 10) * 10
    k = round(f / fs)
    fa = abs(f - k * fs)
    stem = f"A {eng(f,'Hz')} sinusoid is sampled at {eng(fs,'Hz')} with no anti-aliasing filter. At what frequency does it appear after reconstruction?"
    sol = (f"The Nyquist frequency is $f_s/2 = {em(fs/2,'Hz')}$, which the signal exceeds, so it aliases. The apparent frequency is the distance to the nearest multiple of $f_s$:\n\n"
           f"$$f_a = |f - kf_s| = |{mnum(f,5)} - {k}({mnum(fs,5)})| = {em(fa,'Hz')}$$\n\n"
           "Visualise the spectrum folding back about $f_s/2$ like a concertina.")
    wr = [float(f), f + fs, fs / 2, 2 * f - fs if 2 * f - fs > 0 else fs - f / 2]
    return make(stem, num_mcq(rng, fa, wr, lambda v: eng(v, "Hz")), sol)


@tpl("signal")
def dft_resolution(rng):
    fs = rng.choice([1000, 8000, 10240, 48000, 2048])
    N = rng.choice([256, 512, 1024, 2048, 4096])
    df = fs / N
    if rng.random() < 0.5:
        stem = f"A {N}-point DFT is computed from samples taken at {eng(fs,'Hz')}. What is the frequency spacing between DFT bins?"
        ans, wr, fmt = df, [fs / (2 * N), N / fs, 2 * fs / N], lambda v: eng(v, "Hz", 4)
        sol = (f"$$\\Delta f = {frac('f_s','N')} = {frac(fs, N)} = {em(df,'Hz',4)}$$\n\nThe record length is $T = N/f_s$, and resolution is its reciprocal: to resolve finer detail, record for longer.")
    else:
        k = rng.choice([5, 10, 20, 32, 50])
        f = k * df
        stem = f"A {N}-point DFT is computed from samples taken at {eng(fs,'Hz')}. In which bin index $k$ does a {eng(f,'Hz',4)} tone appear?"
        ans, wr, fmt = k, [k * 2, max(1, k // 2), k + 1], lambda v: f"k = {int(v)}"
        sol = (f"Bin $k$ corresponds to $f_k = k f_s/N$, so $k = fN/f_s = ({mnum(f,4)})({N})/{fs} = {k}$.")
        return make(stem, num_mcq(rng, ans, wr, fmt, integer=True), sol)
    return make(stem, num_mcq(rng, ans, wr, fmt), sol)


@tpl("signal")
def quant_snr(rng):
    N = rng.choice([8, 10, 12, 14, 16])
    snr = 6.02 * N + 1.76
    stem = f"What is the theoretical signal-to-quantisation-noise ratio of an ideal {N}-bit ADC driven by a full-scale sine wave?"
    sol = (f"$$\\text{{SQNR}} = 6.02N + 1.76\\ \\text{{dB}} = 6.02({N}) + 1.76 = {mnum(snr,4)}\\ \\text{{dB}}$$\n\n"
           "Each extra bit buys about 6 dB. The 1.76 dB term comes from the ratio of a sine wave's RMS value to the RMS of uniform quantisation noise.")
    return make(stem, num_mcq(rng, snr, [6.02 * N, 3.01 * N + 1.76, 6.02 * (N - 1) + 1.76], lambda v: fu(v, "dB", 4)), sol)


@tpl("signal")
def adc_lsb(rng):
    V = rng.choice([3.3, 5.0, 10.0, 2.5, 4.096])
    N = rng.choice([8, 10, 12, 16])
    q = V / 2 ** N
    stem = f"An {N}-bit ADC has a full-scale input range of 0 to {fnum(V,4)} V. What is its resolution (one LSB), using $\\varepsilon = V_{{FS}}/2^N$?"
    sol = (f"$$\\varepsilon = {frac('V_{FS}','2^N')} = {frac(fnum(V,4), f'2^{{{N}}}')} = {frac(fnum(V,4), 2**N)} = {em(q,'V',4)}$$\n\n"
           "The maximum quantisation error of a rounding converter is half of this.")
    return make(stem, num_mcq(rng, q, [V / 2 ** (N - 1), V / N, V / 2 ** (N + 1)], lambda v: eng(v, "V", 4)), sol)


@tpl("signal")
def fir_output(rng):
    b = [rng.choice([0.5, 1, 2, -1, 0.25]) for _ in range(3)]
    x = [rng.randint(-2, 4) for _ in range(4)]
    n = rng.choice([2, 3])
    y = sum(b[k] * x[n - k] for k in range(3) if 0 <= n - k < len(x))
    stem = (f"An FIR filter obeys $y[n] = {mnum(b[0])}x[n] {'+' if b[1]>=0 else '-'} {mnum(abs(b[1]))}x[n-1] {'+' if b[2]>=0 else '-'} {mnum(abs(b[2]))}x[n-2]$. "
            f"The input is $x[0..3] = \\{{{', '.join(str(v) for v in x)}\\}}$ and $x[n] = 0$ for $n < 0$. What is $y[{n}]$?")
    sol = (f"$$y[{n}] = {mnum(b[0])}x[{n}] + ({mnum(b[1])})x[{n-1}] + ({mnum(b[2])})x[{n-2}] = {mnum(b[0])}({x[n]}) + ({mnum(b[1])})({x[n-1]}) + ({mnum(b[2])})({x[n-2]}) = {mnum(y,4)}$$\n\n"
           "An FIR filter only ever looks at present and past *inputs*—no feedback—so it is always stable.")
    wr = [b[0] * x[n], sum(b) * x[n], sum(b[k] * x[n + k] for k in range(3) if n + k < len(x)) or y + 2]
    return make(stem, num_mcq(rng, y, wr, lambda v: fnum(v, 3), positive=False), sol)


@tpl("signal")
def iir_impulse(rng):
    a = rng.choice([0.5, 0.8, -0.5, 0.9, 0.6])
    n = rng.choice([2, 3, 4])
    kind = rng.choice(["impulse", "step"])
    if kind == "impulse":
        y = a ** n
        desc = "a unit impulse $\\delta[n]$"
        how = f"With an impulse input the response is $h[n] = a^n$ for $n\\ge0$, so $y[{n}] = ({mnum(a)})^{n} = {mnum(y,4)}$."
        wr = [a * n, a ** (n + 1), 1 - a ** n]
    else:
        y = sum(a ** k for k in range(n + 1))
        desc = "a unit step $u[n]$"
        how = (f"Iterate from $y[-1] = 0$: each output adds 1 to $a$ times the previous output, giving $y[{n}] = \\sum_{{k=0}}^{{{n}}} a^k = {mnum(y,4)}$.")
        wr = [a ** n, (n + 1) * a, 1 / (1 - a)]
    stem = f"A system obeys $y[n] = {mnum(a)}\\,y[n-1] + x[n]$ with zero initial conditions. For {desc} input, what is $y[{n}]$?"
    sol = how + f"\n\nThe single pole at $z = {mnum(a)}$ lies inside the unit circle, so the system is stable."
    return make(stem, num_mcq(rng, y, wr, lambda v: fnum(v, 4), positive=False), sol)


@tpl("signal")
def rc_lowpass(rng):
    Rv = R(rng, 1000, 22000)
    C = rng.choice([1, 2.2, 4.7, 10, 22, 100]) * 1e-9
    fc = 1 / (2 * PI * Rv * C)
    if rng.random() < 0.5:
        stem = f"A first-order RC low-pass filter uses $R = {em(Rv,'Ω')}$ and $C = {em(C,'F')}$. What is its −3 dB cut-off frequency?"
        sol = (f"$$f_c = {frac(1,'2\\pi RC')} = {em(fc,'Hz')}$$\n\nAt $f_c$ the output is $1/\\sqrt2$ of the input (half power) and lags by 45°.")
        return make(stem, num_mcq(rng, fc, [1 / (Rv * C), 2 * PI / (Rv * C) / 1000, fc / math.sqrt(2)], lambda v: eng(v, "Hz")), sol)
    m = rng.choice([2, 5, 10, 20])
    f = m * fc
    att = 10 * math.log10(1 + m * m)
    stem = (f"A first-order RC low-pass filter has a cut-off frequency of {eng(fc,'Hz')}. By how many decibels is a {eng(f,'Hz')} signal attenuated?")
    sol = (f"$|H| = 1/\\sqrt{{1 + (f/f_c)^2}}$ with $f/f_c = {m}$:\n\n$$\\text{{attenuation}} = 10\\log_{{10}}(1 + {m}^2) = {mnum(att,4)}\\ \\text{{dB}}$$\n\n"
           "Far above cut-off the roll-off approaches 20 dB per decade.")
    return make(stem, num_mcq(rng, att, [20 * math.log10(m * m), 10 * math.log10(m), 3.0 * m], lambda v: fu(v, "dB")), sol)


@tpl("signal")
def square_harmonic(rng):
    A = rng.choice([1, 2, 5, 10, 12])
    n = rng.choice([3, 5, 7])
    an = 4 * A / (n * PI)
    stem = (f"A symmetrical square wave alternates between $+{A}$ V and $-{A}$ V with zero mean. What is the amplitude of its {n}rd harmonic?" if n == 3 else
            f"A symmetrical square wave alternates between $+{A}$ V and $-{A}$ V with zero mean. What is the amplitude of its {n}th harmonic?")
    sol = (f"The Fourier series contains only odd harmonics: $x(t) = {frac('4A','\\pi')}\\sum_{{n\\,odd}} {frac(1,'n')}\\sin(n\\omega_0t)$.\n\n"
           f"$$a_{n} = {frac('4A',f'{n}\\pi')} = {frac(4*A, f'{n}\\pi')} = {em(an,'V')}$$\n\n"
           f"The fundamental is ${mnum(4*A/PI)}$ V—slightly larger than the square wave itself.")
    return make(stem, num_mcq(rng, an, [4 * A / PI, 2 * A / (n * PI), A / n], lambda v: eng(v, "V")), sol)


@tpl("signal")
def decibels(rng):
    kind = rng.choice(["v", "p"])
    r = rng.choice([2, 5, 10, 20, 50, 100, 0.5, 0.1])
    if kind == "v":
        db = 20 * math.log10(r)
        stem = f"An amplifier's output voltage is {fnum(r)} times its input voltage (equal input and load resistances). What is the gain in decibels?"
        sol = f"For voltage ratios, $G = 20\\log_{{10}}(V_o/V_i) = 20\\log_{{10}}({fnum(r)}) = {mnum(db,4)}$ dB. Using $10\\log$ (correct only for power) halves the answer."
        wr = [10 * math.log10(r), 20 * r / 10 if r > 1 else -3.0, 20 * math.log(r)]
    else:
        db = 10 * math.log10(r)
        stem = f"A filter passes {fnum(r)} times the input power to its output. What is the gain in decibels?"
        sol = f"For power ratios, $G = 10\\log_{{10}}(P_o/P_i) = 10\\log_{{10}}({fnum(r)}) = {mnum(db,4)}$ dB. A power ratio below 1 gives a negative gain (a loss)."
        wr = [20 * math.log10(r), 10 * math.log(r), -db]
    return make(stem, num_mcq(rng, db, wr, lambda v: fu(v, "dB", 3), positive=False), sol)


@tpl("signal")
def z_stability(rng):
    a = rng.choice([0.4, 0.5, 0.8, 1.2, 1.5, -0.6, -1.25, 0.95])
    stable = abs(a) < 1
    corr = (f"Pole at $z = {mnum(a)}$; stable, because $|z| < 1$" if stable else f"Pole at $z = {mnum(a)}$; unstable, because $|z| > 1$")
    wr = [f"Pole at $z = {mnum(-a)}$; {'stable' if abs(a)<1 else 'unstable'}, because the pole is real",
          (f"Pole at $z = {mnum(a)}$; unstable, because the pole is not at the origin" if stable else f"Pole at $z = {mnum(a)}$; stable, because the pole is real"),
          f"Pole at $z = {mnum(1/a)}$; {'unstable' if abs(1/a)>1 else 'stable'}, because of where it sits relative to the unit circle"]
    stem = f"A causal digital filter has $H(z) = \\dfrac{{1}}{{1 - {mnum(a)}z^{{-1}}}}$ if the sign is read literally. Where is its pole, and is the filter stable?" if a > 0 else \
        f"A causal digital filter has $H(z) = \\dfrac{{1}}{{1 + {mnum(-a)}z^{{-1}}}}$. Where is its pole, and is the filter stable?"
    stem = stem.replace(" if the sign is read literally", "")
    sol = (f"Multiply through by $z$: $H(z) = \\dfrac{{z}}{{z - ({mnum(a)})}}$, so the pole is at $z = {mnum(a)}$. "
           "A causal discrete-time system is stable when all poles lie strictly inside the unit circle. "
           f"Here $|{mnum(a)}| {'<' if stable else '>'} 1$, so the filter is {'stable' if stable else 'unstable'}.")
    return make(stem, str_mcq(rng, corr, wr), sol)


# =============================================================== ELECTRONICS


@tpl("electronics")
def diode_series(rng):
    Vs = rng.choice([5, 9, 12, 15, 24])
    Rv = R(rng, 220, 4700)
    nd = rng.choice([1, 2])
    I = (Vs - 0.7 * nd) / Rv
    stem = (f"A {Vs} V source drives {'a silicon diode' if nd==1 else 'two silicon diodes'} (forward-biased{'' if nd==1 else ', in series'}) in series with {eng(Rv,'Ω')}. "
            "Using the constant-voltage-drop model with 0.7 V per diode, what is the current?")
    sol = (f"$$I = {frac(f'V_s - {nd}(0.7)', 'R')} = {frac(f'{Vs} - {mnum(0.7*nd)}', em(Rv,'Ω'))} = {em(I,'A')}$$\n\n"
           "Each forward-biased silicon junction subtracts roughly 0.7 V from the loop.")
    wr = [Vs / Rv, (Vs - 0.3 * nd) / Rv, (Vs + 0.7 * nd) / Rv, (Vs - 0.7) / Rv if nd == 2 else (Vs - 1.4) / Rv]
    return make(stem, num_mcq(rng, I, wr, lambda v: eng(v, "A")), sol)


@tpl("electronics")
def zener(rng):
    Vz = rng.choice([5.1, 6.2, 9.1, 12])
    Vs = Vz + rng.choice([6, 8, 10, 12])
    Rs = rng.choice([100, 150, 220, 330])
    RL = rng.choice([470, 680, 1000, 2200])
    Is = (Vs - Vz) / Rs
    IL = Vz / RL
    Iz = Is - IL
    if Iz <= 0.001:
        RL = 4700
        IL = Vz / RL
        Iz = Is - IL
    stem = (f"A {fnum(Vz)} V Zener regulator is fed from {fnum(Vs)} V through a {Rs} Ω series resistor and supplies a {eng(RL,'Ω')} load. What current flows in the Zener?")
    sol = (f"With the Zener in breakdown, the load voltage is clamped at {fnum(Vz)} V.\n\n"
           f"Series-resistor current: $I_S = (V_s - V_Z)/R_S = ({fnum(Vs)} - {fnum(Vz)})/{Rs} = {em(Is,'A',4)}$\n\n"
           f"Load current: $I_L = V_Z/R_L = {em(IL,'A',4)}$\n\n$$I_Z = I_S - I_L = {em(Iz,'A')}$$\n\n"
           "Check that $I_Z$ is positive—if it were not, the Zener would drop out of regulation.")
    return make(stem, num_mcq(rng, Iz, [Is, IL, Vs / Rs - IL], lambda v: eng(v, "A")), sol)


@tpl("electronics")
def bjt_fixed_bias(rng):
    for _ in range(100):
        VCC = rng.choice([9, 12, 15, 20])
        RB = rng.choice([220, 330, 470, 680, 1000]) * 1e3
        RC = R(rng, 1000, 4700)
        beta = rng.choice([80, 100, 120, 150, 200])
        IB = (VCC - 0.7) / RB
        IC = beta * IB
        VCE = VCC - IC * RC
        if VCE > 1.0:
            break
    stem = (f"A fixed-bias NPN stage has $V_{{CC}} = {VCC}$ V, $R_B = {em(RB,'Ω')}$, $R_C = {em(RC,'Ω')}$, $\\beta = {beta}$ and $V_{{BE}} = 0.7$ V. What is $V_{{CE}}$?")
    sol = (f"$$I_B = {frac('V_{CC} - V_{BE}','R_B')} = {em(IB,'A',4)}, \\quad I_C = \\beta I_B = {em(IC,'A',4)}$$\n\n"
           f"$$V_{{CE}} = V_{{CC}} - I_CR_C = {VCC} - ({em(IC,'A',4)})({em(RC,'Ω')}) = {em(VCE,'V')}$$\n\n"
           "$V_{CE}$ is well above about 0.2 V, confirming the assumption that the transistor is in the active region.")
    wr = [VCC - beta * VCC / RB * RC, VCC - IB * RC, IC * RC]
    return make(stem, num_mcq(rng, VCE, wr, lambda v: eng(v, "V")), sol)


@tpl("electronics")
def bjt_divider_bias(rng):
    for _ in range(100):
        VCC = rng.choice([12, 15, 18, 20])
        R1, R2 = rng.choice([22, 33, 47, 56, 68]) * 1e3, rng.choice([4.7, 6.8, 8.2, 10, 12]) * 1e3
        RE = rng.choice([470, 680, 1000, 1200])
        RC = rng.choice([1500, 2200, 2700, 3300])
        VB = VCC * R2 / (R1 + R2)
        IE = (VB - 0.7) / RE
        VCE = VCC - IE * (RC + RE)
        if VB > 1.2 and VCE > 1.5:
            break
    if rng.random() < 0.5:
        stem = (f"A voltage-divider-biased NPN amplifier has $V_{{CC}} = {VCC}$ V, $R_1 = {em(R1,'Ω')}$, $R_2 = {em(R2,'Ω')}$, $R_E = {em(RE,'Ω')}$ and $R_C = {em(RC,'Ω')}$. "
                "Assuming $\\beta$ is large and $V_{BE} = 0.7$ V, what is the collector current?")
        ans, wr, fmt = IE, [VB / RE, (VCC - 0.7) / (RC + RE), VB / (RC + RE)], lambda v: eng(v, "A")
    else:
        stem = (f"A voltage-divider-biased NPN amplifier has $V_{{CC}} = {VCC}$ V, $R_1 = {em(R1,'Ω')}$, $R_2 = {em(R2,'Ω')}$, $R_E = {em(RE,'Ω')}$ and $R_C = {em(RC,'Ω')}$. "
                "Assuming $\\beta$ is large and $V_{BE} = 0.7$ V, what is $V_{CE}$?")
        ans, wr, fmt = VCE, [VCC - IE * RC, VCC - VB, VCC - VB / RE * (RC + RE)], lambda v: eng(v, "V")
    sol = (f"With large $\\beta$, base current is negligible and the divider sets the base voltage:\n\n"
           f"$$V_B = V_{{CC}}{frac('R_2','R_1+R_2')} = {em(VB,'V',4)}, \\quad V_E = V_B - 0.7 = {em(VB-0.7,'V',4)}$$\n\n"
           f"$$I_C \\approx I_E = V_E/R_E = {em(IE,'A',4)}, \\quad V_{{CE}} = V_{{CC}} - I_C(R_C + R_E) = {em(VCE,'V',4)}$$\n\n"
           "Forgetting to subtract $V_{BE}$ before dividing by $R_E$ is the commonest slip.")
    return make(stem, num_mcq(rng, ans, wr, fmt), sol)


@tpl("electronics")
def mosfet_sat(rng):
    K = rng.choice([0.5, 1, 2, 4]) * 1e-3
    Vt = rng.choice([0.7, 1.0, 1.5, 2.0])
    VGS = Vt + rng.choice([0.5, 1, 1.5, 2, 3])
    ID = K * (VGS - Vt) ** 2
    stem = (f"An n-channel enhancement MOSFET operating in saturation obeys $i_D = K(v_{{GS}} - V_t)^2$ with $K = {em(K,'A/V²')}$ and $V_t = {fnum(Vt)}$ V. "
            f"What drain current flows when $v_{{GS}} = {fnum(VGS)}$ V?")
    sol = (f"The overdrive is $v_{{GS}} - V_t = {mnum(VGS-Vt)}$ V.\n\n$$i_D = K(v_{{GS}} - V_t)^2 = ({em(K,'A/V²')})({mnum(VGS-Vt)})^2 = {em(ID,'A')}$$\n\n"
           "Confirm saturation by checking $v_{DS} \\ge v_{GS} - V_t$ in the actual circuit.")
    return make(stem, num_mcq(rng, ID, [K * (VGS - Vt), K * VGS ** 2, 0.5 * K * (VGS - Vt) ** 2], lambda v: eng(v, "A")), sol)


@tpl("electronics")
def opamp_inverting(rng):
    Rin = R(rng, 1000, 22000)
    Rf = Rin * rng.choice([2, 4.7, 10, 3.3, 5.6])
    Rf = siground(Rf, 2)
    Vin = rng.choice([0.1, 0.2, 0.5, -0.3, 1.0, 0.25])
    Vo = -Rf / Rin * Vin
    stem = f"An ideal inverting amplifier has $R_{{in}} = {em(Rin,'Ω')}$ and $R_f = {em(Rf,'Ω')}$. What is the output for an input of {fnum(Vin)} V (assume no saturation)?"
    sol = (f"The virtual earth at the inverting input forces $V_{{in}}/R_{{in}} = -V_o/R_f$:\n\n$$V_o = -{frac('R_f','R_{in}')}V_{{in}} = -{mnum(Rf/Rin,4)}\\times({mnum(Vin)}) = {em(Vo,'V')}$$")
    return make(stem, num_mcq(rng, Vo, [-Vo, (1 + Rf / Rin) * Vin, -Rin / Rf * Vin], lambda v: eng(v, "V"), positive=False), sol)


@tpl("electronics")
def opamp_noninv(rng):
    R1 = R(rng, 1000, 10000)
    Rf = siground(R1 * rng.choice([1, 2.2, 4.7, 9, 3.3]), 2)
    Vin = rng.choice([0.1, 0.25, 0.5, 1.2])
    G = 1 + Rf / R1
    stem = f"A non-inverting amplifier uses $R_1 = {em(R1,'Ω')}$ (to ground) and $R_f = {em(Rf,'Ω')}$. What is the output for {fnum(Vin)} V in?"
    sol = f"$$V_o = \\left(1 + {frac('R_f','R_1')}\\right)V_{{in}} = {mnum(G,4)}\\times{mnum(Vin)} = {em(G*Vin,'V')}$$\n\nThe gain of a non-inverting stage can never be less than 1."
    return make(stem, num_mcq(rng, G * Vin, [Rf / R1 * Vin, (1 + R1 / Rf) * Vin, Vin * (Rf / R1) * 1.5 if Rf != R1 else 3 * Vin], lambda v: eng(v, "V")), sol)


@tpl("electronics")
def summing_amp(rng):
    Rf = rng.choice([10, 20, 47, 100]) * 1e3
    R1, R2 = rng.choice([10, 20, 47]) * 1e3, rng.choice([5, 10, 22]) * 1e3
    V1, V2 = rng.choice([0.2, 0.5, 1.0, -0.4]), rng.choice([0.1, 0.3, -0.2, 0.6])
    Vo = -Rf * (V1 / R1 + V2 / R2)
    if abs(Vo) < 0.05:
        V2 = 0.5
        Vo = -Rf * (V1 / R1 + V2 / R2)
    stem = (f"An inverting summing amplifier has $R_f = {em(Rf,'Ω')}$, input $V_1 = {mnum(V1)}$ V through {eng(R1,'Ω')} and input $V_2 = {mnum(V2)}$ V through {eng(R2,'Ω')}. What is $V_o$?")
    sol = (f"Currents into the virtual earth add:\n\n$$V_o = -R_f\\left({frac('V_1','R_1')} + {frac('V_2','R_2')}\\right) = -{mnum(Rf/1e3)}\\text{{k}}\\left({frac(mnum(V1), mnum(R1/1e3)+'\\text{k}')} + {frac(mnum(V2), mnum(R2/1e3)+'\\text{k}')}\\right) = {em(Vo,'V')}$$")
    return make(stem, num_mcq(rng, Vo, [-Vo, -Rf / R1 * (V1 + V2), -(V1 + V2)], lambda v: eng(v, "V"), positive=False), sol)


@tpl("electronics")
def integrator(rng):
    Rv = rng.choice([10, 47, 100]) * 1e3
    C = rng.choice([0.1, 0.22, 1.0]) * 1e-6
    Vin = rng.choice([0.5, 1, 2, -1])
    t = rng.choice([1, 2, 5, 10]) * 1e-3
    Vo = -Vin * t / (Rv * C)
    if abs(Vo) > 12:
        t = t / 10
        Vo = -Vin * t / (Rv * C)
    stem = (f"An ideal op-amp integrator has $R = {em(Rv,'Ω')}$ and $C = {em(C,'F')}$, with the capacitor initially discharged. A constant {fnum(Vin)} V is applied at $t = 0$. "
            f"What is the output at $t = {em(t,'s')}$?")
    sol = (f"$$v_o(t) = -{frac(1,'RC')}\\int_0^t v_{{in}}\\,dt = -{frac(f'V_{{in}}t','RC')} = -{frac(f'({mnum(Vin)})({em(t,"s")})', f'({em(Rv*C,"s")})')} = {em(Vo,'V')}$$\n\n"
           "A constant input produces a linear ramp of the opposite sign until the op-amp saturates.")
    return make(stem, num_mcq(rng, Vo, [-Vo, -Vin * Rv * C / t, -Vin * t / (Rv * C) / 2], lambda v: eng(v, "V"), positive=False), sol)


@tpl("electronics")
def rectifier(rng):
    Vrms = rng.choice([6, 9, 12, 18, 24])
    full = rng.choice([False, True])
    Vp = Vrms * math.sqrt(2) - (1.4 if full else 0.7)
    Vdc = (2 * Vp / PI) if full else (Vp / PI)
    kind = "full-wave bridge" if full else "half-wave"
    stem = (f"A {kind} rectifier (no filter capacitor) is fed from a {Vrms} V RMS transformer secondary. "
            f"Allowing {'1.4 V for the two conducting diodes' if full else '0.7 V for the diode'}, what is the average (DC) load voltage?")
    sol = (f"Peak output $V_p = \\sqrt2({Vrms}) - {'1.4' if full else '0.7'} = {mnum(Vp,4)}$ V.\n\n"
           f"$$V_{{dc}} = {'\\frac{2V_p}{\\pi}' if full else '\\frac{V_p}{\\pi}'} = {mnum(Vdc,4)}\\ \\text{{V}}$$\n\n"
           "A half-wave output averages $V_p/\\pi$; full-wave doubles it. Don't use the RMS value as the peak.")
    wr = [Vrms / PI, Vp / 2, (Vp / PI) if full else (2 * Vp / PI), Vrms * 0.9]
    return make(stem, num_mcq(rng, Vdc, wr, lambda v: fu(v, "V")), sol)


@tpl("electronics")
def ripple(rng):
    I = rng.choice([0.1, 0.2, 0.5, 1.0])
    C = rng.choice([470, 1000, 2200, 4700]) * 1e-6
    f = 60
    full = rng.choice([True, False])
    dV = I / (2 * f * C) if full else I / (f * C)
    stem = (f"A {'full' if full else 'half'}-wave rectifier with a {eng(C,'F')} reservoir capacitor supplies {fnum(I)} A from a 60 Hz mains supply. Estimate the peak-to-peak ripple.")
    sol = (f"Between charging peaks the capacitor supplies the load current for roughly one ripple period, $T = 1/{'(2f)' if full else 'f'}$:\n\n"
           f"$$\\Delta V \\approx {frac('I', '2fC' if full else 'fC')} = {em(dV,'V')}$$\n\n"
           "Full-wave rectification halves the ripple because the capacitor is topped up twice per mains cycle.")
    wr = [I / (f * C) if full else I / (2 * f * C), I / (2 * PI * f * C), dV * 2 * PI]
    return make(stem, num_mcq(rng, dV, wr, lambda v: eng(v, "V")), sol)


@tpl("electronics")
def ce_gain(rng):
    IC = rng.choice([0.5, 1, 2, 2.6, 5]) * 1e-3
    RC = rng.choice([1, 2.2, 3.3, 4.7, 10]) * 1e3
    gm = IC / 0.026
    Av = gm * RC
    stem = (f"A common-emitter stage with a fully bypassed emitter resistor is biased at $I_C = {em(IC,'A')}$ with $R_C = {em(RC,'Ω')}$ (no external load). "
            "Taking $V_T = 26$ mV and neglecting $r_o$, what is the magnitude of the small-signal voltage gain?")
    sol = (f"$$g_m = {frac('I_C','V_T')} = {frac(em(IC,'A'), '26\\,\\text{mV}')} = {em(gm,'S',4)}$$\n\n$$|A_v| = g_mR_C = {mnum(Av,4)}$$\n\n"
           "Gain depends on bias current, not directly on $\\beta$—one reason the transconductance view is so useful.")
    return make(stem, num_mcq(rng, Av, [gm, RC / 26, Av / 2], lambda v: fnum(v)), sol)


@tpl("electronics")
def led_resistor(rng):
    Vs = rng.choice([5, 3.3, 12, 9])
    Vf, col = rng.choice([(2.0, "red"), (2.1, "yellow"), (3.1, "blue"), (2.2, "green")])
    If = rng.choice([10, 15, 20]) * 1e-3
    Rv = (Vs - Vf) / If
    stem = f"A {col} LED ($V_F = {fnum(Vf)}$ V) is to run at {eng(If,'A')} from a {fnum(Vs)} V supply. What series resistance is needed?"
    sol = f"$$R = {frac('V_s - V_F','I_F')} = {frac(f'{fnum(Vs)} - {fnum(Vf)}', em(If,'A'))} = {em(Rv,'Ω')}$$\n\nChoose the next standard value above to keep the current at or below the rating."
    return make(stem, num_mcq(rng, Rv, [Vs / If, Vf / If, (Vs + Vf) / If], lambda v: eng(v, "Ω")), sol)


@tpl("electronics")
def gbw(rng):
    GBW = rng.choice([1, 3, 10, 20]) * 1e6
    G = rng.choice([10, 20, 50, 100])
    B = GBW / G
    stem = f"An op-amp with a gain–bandwidth product of {eng(GBW,'Hz')} is used as a non-inverting amplifier with a gain of {G}. What is the approximate closed-loop bandwidth?"
    sol = f"For a single-pole op-amp the gain–bandwidth product is constant: $f_{{-3dB}} = \\text{{GBW}}/A_{{CL}} = {em(GBW,'Hz')}/{G} = {em(B,'Hz')}$."
    return make(stem, num_mcq(rng, B, [float(GBW), GBW / G ** 2, GBW / (G + 10)], lambda v: eng(v, "Hz")), sol)


# =============================================================== ELECTROMAGNETICS


@tpl("em")
def coulomb(rng):
    q1, q2 = rng.choice([1, 2, 3, 5]) * 1e-6, rng.choice([-2, 4, -5, 6]) * 1e-6
    r = rng.choice([0.05, 0.1, 0.2, 0.3, 0.5])
    F = K_E * abs(q1 * q2) / r ** 2
    stem = f"Point charges of {eng(q1,'C')} and {eng(q2,'C')} are {mnum(r*100)} cm apart in air. What is the magnitude of the force between them, and is it attractive or repulsive?"
    att = "attractive" if q2 < 0 else "repulsive"
    sol = (f"$$F = {frac('1','4\\pi\\varepsilon_0')}{frac('|q_1q_2|','r^2')} = (8.99\\times10^9){frac(f'({mnum(q1)})({mnum(abs(q2))})', f'({mnum(r)})^2')} = {mnum(F,4)}\\ \\text{{N}}$$\n\n"
           f"Opposite signs attract, like signs repel: here the force is **{att}**.")
    other = "repulsive" if att == "attractive" else "attractive"
    corr = f"{fnum(F)} N, {att}"
    wr = [f"{fnum(F)} N, {other}", f"{fnum(K_E*abs(q1*q2)/r)} N, {att}", f"{fnum(F/(4*PI))} N, {att}"]
    return make(stem, str_mcq(rng, corr, wr), sol)


@tpl("em")
def point_field(rng):
    q = rng.choice([1, 2, 5, 10]) * 1e-9
    r = rng.choice([0.1, 0.2, 0.5, 1.0])
    E = K_E * q / r ** 2
    stem = f"What is the electric field magnitude {mnum(r*100)} cm from an isolated point charge of {eng(q,'C')} in free space?"
    sol = f"$$E = {frac('q','4\\pi\\varepsilon_0 r^2')} = {frac(f'(8.99\\times10^9)({mnum(q)})', f'({mnum(r)})^2')} = {mnum(E,4)}\\ \\text{{V/m}}$$\n\nField falls with the square of distance; potential falls only with distance."
    return make(stem, num_mcq(rng, E, [K_E * q / r, E * r ** 2 * 10 if r < 1 else E / 3, K_E * q / (2 * r ** 2)], lambda v: fu(v, "V/m")), sol)


@tpl("em")
def capacitor_energy_field(rng):
    V = rng.choice([10, 50, 100, 500])
    d = rng.choice([0.1, 0.5, 1, 2]) * 1e-3
    if rng.random() < 0.5:
        E = V / d
        stem = f"A potential difference of {V} V is applied across parallel plates {mnum(d*1000)} mm apart. What is the electric field strength between them (ignoring fringing)?"
        sol = f"In a uniform field, $E = V/d = {V}/{mnum(d)} = {mnum(E,4)}$ V/m. Remember to convert millimetres to metres."
        return make(stem, num_mcq(rng, E, [V * d, V / (d * 1000), E / 1000 * 10], lambda v: fu(v, "V/m")), sol)
    C = rng.choice([1, 10, 47, 100, 470]) * 1e-6
    W = 0.5 * C * V ** 2
    stem = f"How much energy is stored in a {eng(C,'F')} capacitor charged to {V} V?"
    sol = f"$$W = \\tfrac12CV^2 = \\tfrac12({mnum(C)})({V})^2 = {em(W,'J')}$$"
    return make(stem, num_mcq(rng, W, [C * V ** 2, 0.5 * C * V, C * V], lambda v: eng(v, "J")), sol)


@tpl("em")
def solenoid_L(rng):
    N = rng.choice([100, 200, 500, 1000])
    dcm = rng.choice([1, 2, 4])
    lcm = rng.choice([5, 10, 20])
    mur = rng.choice([1, 200, 1000])
    A = PI * (dcm / 100) ** 2 / 4
    L = MU0 * mur * N * N * A / (lcm / 100)
    core = "an air core" if mur == 1 else f"a core of relative permeability {mur}"
    stem = f"A long solenoid of {N} turns, {lcm} cm long and {dcm} cm in diameter, has {core}. Estimate its inductance."
    sol = (f"$A = \\pi d^2/4 = {mnum(A)}\\ \\text{{m}}^2$.\n\n$$L = {frac('\\mu_0\\mu_r N^2 A','\\ell')} = {frac(f'(4\\pi\\times10^{{-7}})({mur})({N})^2({mnum(A)})', mnum(lcm/100))} = {em(L,'H')}$$\n\n"
           "Inductance scales with the *square* of the turns because each turn both creates and links the flux.")
    return make(stem, num_mcq(rng, L, [L / N, L * 4, L / mur if mur > 1 else L / 2], lambda v: eng(v, "H")), sol)


@tpl("em")
def wire_B(rng):
    I = rng.choice([1, 5, 10, 50, 100, 500])
    r = rng.choice([0.01, 0.02, 0.05, 0.1, 1.0])
    B = MU0 * I / (2 * PI * r)
    stem = f"What is the magnetic flux density {mnum(r*100)} cm from a long straight conductor carrying {I} A?"
    sol = f"By Ampère's law, $B = {frac('\\mu_0 I','2\\pi r')} = {frac(f'(4\\pi\\times10^{{-7}})({I})', f'2\\pi({mnum(r)})')} = {em(B,'T')}$."
    return make(stem, num_mcq(rng, B, [MU0 * I / (4 * PI * r), MU0 * I / (2 * r), MU0 * I / (2 * PI * r * r)], lambda v: eng(v, "T")), sol)


@tpl("em")
def wire_force(rng):
    B = rng.choice([0.1, 0.2, 0.5, 0.8, 1.2])
    I = rng.choice([2, 5, 10, 20])
    L = rng.choice([0.1, 0.2, 0.5])
    th = rng.choice([90, 30, 60, 45])
    F = B * I * L * math.sin(math.radians(th))
    stem = f"A {mnum(L*100)} cm conductor carrying {I} A lies at {th}° to a uniform {fnum(B)} T field. What force acts on it?"
    sol = f"$$F = BIL\\sin\\theta = ({fnum(B)})({I})({mnum(L)})\\sin {th}^\\circ = {mnum(F,4)}\\ \\text{{N}}$$\n\nOnly the current component perpendicular to $\\mathbf{{B}}$ experiences force."
    wr = [B * I * L * math.cos(math.radians(th)) if th != 90 else B * I * L / 2, B * I * L * (1 if th != 90 else 2), B * I / L]
    return make(stem, num_mcq(rng, F, wr, lambda v: fu(v, "N")), sol)


@tpl("em")
def faraday(rng):
    N = rng.choice([50, 100, 200, 500])
    B1, B2 = rng.choice([(0.1, 0.5), (0.8, 0.2), (0, 0.6), (1.0, 0.0)])
    A = rng.choice([10, 20, 50, 100]) * 1e-4
    dt = rng.choice([0.01, 0.05, 0.1, 0.2])
    emf = N * abs(B2 - B1) * A / dt
    stem = (f"A {N}-turn coil of area {mnum(A*1e4)} cm² lies perpendicular to a magnetic field that changes uniformly from {fnum(B1)} T to {fnum(B2)} T in {eng(dt,'s')}. "
            "What is the magnitude of the average induced EMF?")
    sol = (f"$$|\\mathcal{{E}}| = N{frac('\\Delta\\Phi','\\Delta t')} = N{frac('A\\,\\Delta B','\\Delta t')} = {N}{frac(f'({mnum(A)})({mnum(abs(B2-B1))})', mnum(dt))} = {em(emf,'V')}$$\n\n"
           "Lenz's law fixes the polarity: the induced current opposes the change in flux.")
    return make(stem, num_mcq(rng, emf, [emf / N, N * B2 * A / dt if B2 * A != abs(B2 - B1) * A else emf * 2, emf * 1e4 / 100], lambda v: eng(v, "V")), sol)


@tpl("em")
def wavelength_medium(rng):
    f = rng.choice([100e6, 300e6, 900e6, 2.4e9, 5e9])
    er = rng.choice([2.25, 4, 4.4, 9, 2.1])
    lam = C0 / (f * math.sqrt(er))
    stem = f"What is the wavelength of a {eng(f,'Hz')} wave in a lossless non-magnetic dielectric with $\\varepsilon_r = {fnum(er)}$?"
    sol = (f"Phase velocity $v = c/\\sqrt{{\\varepsilon_r}} = {mnum(C0/math.sqrt(er),4)}$ m/s, so\n\n$$\\lambda = {frac('v','f')} = {frac('c','f\\sqrt{\\varepsilon_r}')} = {em(lam,'m')}$$")
    return make(stem, num_mcq(rng, lam, [C0 / f, C0 / (f * er), C0 * math.sqrt(er) / f], lambda v: eng(v, "m")), sol)


@tpl("em")
def intrinsic_imp(rng):
    er = rng.choice([2.25, 4, 9, 16, 2.56])
    eta = 376.7 / math.sqrt(er)
    stem = f"What is the intrinsic impedance of a lossless non-magnetic medium with $\\varepsilon_r = {fnum(er)}$?"
    sol = f"$$\\eta = \\sqrt{{{frac('\\mu','\\varepsilon')}}} = {frac('\\eta_0','\\sqrt{\\varepsilon_r}')} = {frac('377', f'\\sqrt{{{fnum(er)}}}')} = {mnum(eta,4)}\\ \\Omega$$"
    return make(stem, num_mcq(rng, eta, [376.7 / er, 376.7 * math.sqrt(er), 376.7], lambda v: fu(v, "Ω")), sol)


@tpl("em")
def reflection(rng):
    Z0 = rng.choice([50, 75, 300])
    ZL = rng.choice([25, 100, 150, 200, 30, 600])
    if ZL == Z0:
        ZL = Z0 * 2
    G = (ZL - Z0) / (ZL + Z0)
    S = (1 + abs(G)) / (1 - abs(G))
    if rng.random() < 0.5:
        stem = f"A {Z0} Ω lossless line is terminated in a {ZL} Ω resistive load. What is the voltage reflection coefficient at the load?"
        sol = (f"$$\\Gamma = {frac('Z_L - Z_0','Z_L + Z_0')} = {frac(f'{ZL} - {Z0}', f'{ZL} + {Z0}')} = {mnum(G,4)}$$\n\n"
               "A negative $\\Gamma$ means the load is below $Z_0$ and the reflected voltage is inverted.")
        return make(stem, num_mcq(rng, G, [-G, (Z0 - ZL) / Z0, S], lambda v: fnum(v, 3), positive=False), sol)
    stem = f"A {Z0} Ω lossless line is terminated in a {ZL} Ω resistive load. What is the voltage standing-wave ratio (VSWR)?"
    sol = (f"$|\\Gamma| = |{ZL} - {Z0}|/({ZL} + {Z0}) = {mnum(abs(G),4)}$, and\n\n$$\\text{{VSWR}} = {frac('1 + |\\Gamma|','1 - |\\Gamma|')} = {mnum(S,4)}$$\n\n"
           "For a resistive load the shortcut $\\text{VSWR} = Z_L/Z_0$ or $Z_0/Z_L$ (whichever exceeds 1) gives the same result.")
    return make(stem, num_mcq(rng, S, [abs(G), 1 + abs(G), S * 2], lambda v: fnum(v, 3)), sol)


@tpl("em")
def skin_depth(rng):
    f = rng.choice([60, 1e3, 10e3, 1e6, 100e6])
    sigma = 5.8e7
    d = 1 / math.sqrt(PI * f * MU0 * sigma)
    stem = f"What is the skin depth in copper ($\\sigma = 5.8\\times10^7$ S/m, $\\mu_r = 1$) at {eng(f,'Hz')}?"
    sol = (f"$$\\delta = {frac(1,'\\sqrt{\\pi f\\mu\\sigma}')} = {frac(1, f'\\sqrt{{\\pi({mnum(f)})(4\\pi\\times10^{{-7}})(5.8\\times10^7)}}')} = {em(d,'m')}$$\n\n"
           "At mains frequency the skin depth is about 8.5 mm, which is why very large busbars are made hollow or laminated.")
    return make(stem, num_mcq(rng, d, [1 / (PI * f * MU0 * sigma) if 1 / (PI * f * MU0 * sigma) < 1 else d / 10, d / math.sqrt(2), d * math.sqrt(PI)], lambda v: eng(v, "m")), sol)


@tpl("em")
def quarter_wave(rng):
    Z1, Z2 = rng.choice([(50, 100), (50, 200), (75, 300), (50, 25), (300, 75), (50, 12.5)])
    Zq = math.sqrt(Z1 * Z2)
    stem = f"A quarter-wave transformer is to match a {fnum(Z2)} Ω load to a {Z1} Ω line at one frequency. What characteristic impedance must the quarter-wave section have?"
    sol = f"A $\\lambda/4$ line transforms $Z_L$ to $Z_{{in}} = Z_q^2/Z_L$. Setting $Z_{{in}} = {Z1}$ gives $Z_q = \\sqrt{{Z_1Z_L}} = \\sqrt{{({Z1})({fnum(Z2)})}} = {mnum(Zq,4)}\\ \\Omega$."
    return make(stem, num_mcq(rng, Zq, [(Z1 + Z2) / 2, Z1 * Z2 / (Z1 + Z2), abs(Z1 - Z2) if abs(Z1 - Z2) > 0 else 10], lambda v: fu(v, "Ω")), sol)
