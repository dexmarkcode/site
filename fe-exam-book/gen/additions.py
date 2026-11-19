"""One-off insertion of additional teaching sections before a marker heading in each chapter."""
import os

SRC = os.path.join(os.path.dirname(__file__), "..", "src")

ADD = {
"ch06.md": ("## Practice Questions", r"""
## Common Traps in Transients and Linear Systems

Transient questions punish carelessness more than ignorance. Almost every wrong answer I see in this area comes from one of the following habits, and each has a simple antidote.

**Assuming the capacitor starts at zero.** Many candidates reach for $V(1 - e^{-t/\tau})$ by reflex, because it is the first formula they learned. But the capacitor may already be charged, perhaps to a voltage *higher* than the new source, in which case it discharges towards the new final value. The antidote is to write the general form, $x(\infty) + [x(0^+) - x(\infty)]e^{-t/\tau}$, every time, and fill in the two values deliberately.

**Using the wrong resistance in the time constant.** The time constant uses the Thévenin resistance seen by the capacitor or inductor *in the circuit as it is after the switching event*. If a switch has removed a resistor, or the energy-storage element now discharges through a different path, the time constant changes. Draw the post-switching circuit, kill the sources, and look back from the terminals of the storage element.

**Forgetting continuity.** Only capacitor voltage and inductor current are continuous. The current through a capacitor can jump from zero to its maximum in an instant, and the voltage across an inductor can leap to many times the supply voltage. If a question asks for the capacitor *current* at $t = 0^+$, find the capacitor *voltage* first, then use the circuit to find the current.

**Confusing $\omega_0$, $\omega_d$ and $\alpha$.** In second-order circuits, $\omega_0 = 1/\sqrt{LC}$ is the undamped natural frequency, $\alpha$ is the decay rate, and $\omega_d = \sqrt{\omega_0^2 - \alpha^2}$ is the frequency at which the response actually rings. A question asking for the frequency of oscillation wants $\omega_d$; one asking whether the circuit oscillates wants a comparison of $\alpha$ with $\omega_0$.

**Applying the final value theorem blindly.** Before using $\lim_{s\to0}sF(s)$, check that the poles of $sF(s)$ lie in the left half-plane. If $F(s)$ contains $\omega/(s^2 + \omega^2)$, the signal oscillates forever and has no final value, whatever the theorem appears to give.

**Mixing up poles and zeros.** Poles come from the denominator and decide stability; zeros come from the numerator and do not. A transfer function with a zero in the right half-plane is still stable if its poles are in the left half-plane—it simply has an unusual, initially reversed step response.

**Discrete convolution indices.** When convolving short sequences by hand, misaligning the indices by one place is the commonest error. Use the grid method, and check that the output length is $N + M - 1$.

None of these traps involves difficult mathematics. They involve reading the circuit carefully before writing anything down. A useful discipline is to say aloud, or at least in your head, three things before you calculate: *what is continuous here, what is the final state, and what resistance does the storage element see?* With those three answered, the rest is arithmetic.

### A note on units and magnitudes

Transient questions often involve microfarads, millihenries, kilohms and milliseconds in the same problem. The time constant $RC$ with $R$ in kilohms and $C$ in microfarads comes out directly in milliseconds, a handy shortcut: 4.7 kΩ × 10 μF = 47 ms. Similarly, $L/R$ with $L$ in millihenries and $R$ in ohms gives milliseconds. Use these pairings to check the magnitude of every time constant you calculate. A time constant of 47 seconds for a small electronic circuit, or 47 microseconds for a large motor winding, should make you stop and look again.
"""),
"ch07.md": ("## Practice Questions", r"""
## Common Traps in Signal Processing

**Nyquist rate versus Nyquist frequency.** The Nyquist *rate* is the minimum sampling rate, $2f_{max}$. The Nyquist *frequency* is half the actual sampling rate, $f_s/2$, the highest frequency that can be represented. Read carefully which one a question asks for.

**Voltage and power decibels.** Use $20\log$ for voltage, current and field ratios, and $10\log$ for power ratios. A filter that halves the voltage attenuates by 6 dB, not 3 dB.

**FIR versus IIR.** If the output appears on the right-hand side of the difference equation, the filter is recursive (IIR) and could be unstable. If only inputs appear, it is FIR and is always stable.

**Resolution of an FFT.** Increasing the sampling rate with a fixed number of points makes the resolution *worse*, not better, because $\Delta f = f_s/N$. To resolve closer frequencies you must observe the signal for longer.
"""),
"ch08.md": ("## Practice Questions", r"""
## Common Traps in Electronics

**Forgetting the region check.** Every transistor calculation rests on an assumption about its operating region. Finish every BJT bias problem by checking that $V_{CE}$ exceeds about 0.2 V, and every MOSFET problem by checking $v_{DS} \ge v_{GS} - V_t$. If the check fails, the answer you have is wrong, and the correct one comes from the other region's equations. The exam occasionally builds a question precisely so that the transistor saturates.

**Using $\beta$ where it does not belong.** With voltage-divider bias and an emitter resistor, the collector current is set by the divider and $R_E$, almost independently of $\beta$. If a question gives you $\beta$ and also says it is "large", you are being told to ignore it. If it gives a specific $\beta$ without that phrase, use the Thévenin base-loop method for a more accurate answer.

**Diode drops in bridges.** A bridge rectifier always has two diodes in the conduction path, so it loses about 1.4 V, not 0.7 V. A centre-tapped full-wave rectifier, by contrast, has one diode conducting at a time.

**RMS transformer ratings.** Transformer secondary voltages are quoted in RMS. Multiply by $\sqrt2$ to find the peak before subtracting diode drops.

**Op-amp saturation.** The golden rules hold only while the op-amp is in its linear region with negative feedback. If the calculated output exceeds the supply rails, the real output saturates near the rail, and the golden rule of equal input voltages no longer applies. Without negative feedback—in a comparator, for example—the op-amp simply saturates in the direction of the larger input.

**Gain–bandwidth and the right gain.** For a non-inverting amplifier the closed-loop bandwidth is GBW divided by the closed-loop gain. For an inverting amplifier it is GBW divided by the *noise gain*, $1 + R_f/R_{in}$, which is one more than the magnitude of the signal gain. For high gains the difference is negligible; for an inverting gain of $-1$ the bandwidth is half the GBW, not equal to it.

**Small-signal versus DC.** Small-signal parameters ($g_m$, $r_\pi$) describe how the transistor responds to small changes about the bias point; they do not replace the DC analysis. Always do the DC bias first, then use the bias current to find $g_m$, and only then analyse the small-signal circuit, in which DC sources are set to zero and large capacitors are treated as short circuits.

A final word of encouragement. Electronics questions often look intimidating because of the circuit diagram, but once the right model is in place most of them reduce to a single loop or node equation. Practise redrawing each circuit with its simplified device models before you start, and the intimidation fades quickly.
"""),
"ch09.md": ("## Practice Questions", r"""
## Common Traps in Electromagnetics and Materials

**Square roots of permittivity.** Wave speed, wavelength and intrinsic impedance all scale with $1/\sqrt{\varepsilon_r}$, but capacitance scales with $\varepsilon_r$ itself. Keep the two straight and many distractors disappear.

**Radius or diameter, centimetres or metres.** Geometry questions are designed to catch unit slips. Write every dimension in metres, with its exponent, before substituting.

**$B$ and $H$.** Ampère's law gives $H$ from the currents; multiply by $\mu$ to get $B$. In a ferromagnetic core, forgetting $\mu_r$ underestimates the flux density by a factor of hundreds or thousands.
"""),
"ch10.md": ("## Practice Questions", r"""
## Common Traps in Power Systems

**Which voltage?** System voltages are line-to-line unless stated otherwise. For wye loads, divide by $\sqrt3$ to get the phase voltage across each impedance; for delta loads, use the line voltage directly.

**Efficiency in motor problems.** A motor's rating is its *output* (shaft) power. To find the electrical input, and hence the current, divide by the efficiency. Forgetting this understates the current by several per cent—and the exam's options are usually spaced to catch exactly that.

**Horsepower conversion.** One horsepower is 746 W. Questions using US motor ratings expect the conversion.

**Per-unit base changes.** The impedance scales *up* with the new MVA base and *down* with the square of the new kV base. If you are unsure which way round the ratios go, sanity-check: a bigger MVA base means a given ohmic impedance is a larger fraction of the (smaller) base impedance.

**Slip in percent or per unit.** Slip is often quoted as a percentage but must be used as a decimal in $f_r = sf$ and $P_{mech} = (1 - s)P_{ag}$.

**Transformer test results.** The open-circuit test gives core loss; the short-circuit test gives copper loss at rated current. To find copper loss at another load, scale by the square of the load fraction, never linearly.
"""),
"ch11.md": ("## Practice Questions", r"""
## Common Traps in Control Systems

**Open-loop versus closed-loop.** Steady-state error constants, system type, gain margin and phase margin are all read from the *open-loop* transfer function $G(s)H(s)$. Overshoot, settling time, natural frequency and damping ratio describe the *closed-loop* response. Many wrong answers come from computing the right quantity from the wrong transfer function.

**System type.** Count only the poles exactly at $s = 0$ in the open-loop function. A pole at $s = -0.01$ is not an integrator, however close to the origin it lies.

**Positive and negative feedback.** The standard formula $G/(1 + GH)$ assumes negative feedback. If a block diagram shows a plus sign at the summing junction for the feedback signal, the denominator becomes $1 - GH$.

**Settling-time criteria.** The approximation $T_s \approx 4/(\zeta\omega_n)$ uses a 2% band; a 5% band gives roughly $3/(\zeta\omega_n)$. If a question specifies the band, use the matching constant.

**Margins with signs.** A negative gain margin or phase margin indicates an unstable closed loop. Read the Bode plot carefully at the correct crossover frequency: gain margin at the phase crossover ($-180°$), phase margin at the gain crossover (0 dB).

**Routh arrays with a zero in the first column.** If a zero appears in the first column but the rest of that row is not zero, replace it with a small positive number $\varepsilon$ and continue. If the entire row is zero, the system has roots symmetric about the origin—often a pair on the imaginary axis—and you form an auxiliary polynomial from the row above. On the FE exam, a whole row of zeros almost always marks the boundary of stability, which is the value of $K$ the question is looking for.
"""),
"ch12.md": ("## Practice Questions", r"""
## Common Traps in Communications

**Decibels in formulae that need ratios.** Shannon's formula, Friis's formula and the noise-factor definition all use *linear* ratios. Convert dB to a ratio first ($10^{x/10}$ for power ratios), do the calculation, and convert back at the end if the answer is wanted in dB.

**dB and dBm.** A dBm value is an absolute power; a dB value is a ratio. You can add a gain in dB to a power in dBm to get a power in dBm, but adding two powers in dBm is meaningless. To combine two signals' powers, convert both to milliwatts, add, and convert back.

**AM bandwidth and power.** AM bandwidth is twice the *highest* message frequency, not twice the carrier frequency. Total AM power depends on $m^2/2$, so at 50% modulation the sidebands add only 12.5% to the carrier power.

**Carson's rule terms.** Carson's rule uses the peak deviation and the *maximum* modulating frequency. Using the carrier frequency, or the RMS deviation, gives a wildly wrong answer.

**Bits and symbols.** Baud is symbols per second. Bit rate equals baud multiplied by bits per symbol, $\log_2M$. A 16-QAM link at 1 Mbaud carries 4 Mbit/s, not 16.

**Noise bandwidth.** Thermal noise power is proportional to bandwidth, so a receiver with ten times the bandwidth has a noise floor 10 dB higher. When a question changes the bandwidth, adjust the noise floor before calculating SNR.

**Path loss and frequency.** In the free-space formula, loss increases with frequency only because the formula assumes antennas of fixed gain, whose effective area shrinks as frequency rises. For fixed-*area* antennas the frequency dependence cancels. The exam rarely goes into this subtlety, but it occasionally appears as a conceptual question, and it is worth knowing why the formula looks the way it does.

### Working a link budget step by step

Link-budget questions can look long, but they reward an orderly approach. List every term in a column with its sign: transmitter power (dBm, positive), transmit antenna gain (dBi, positive), cable and connector losses (dB, negative), path loss (dB, negative), receive antenna gain (dBi, positive), receive cable loss (dB, negative). Add the column. Then, separately, calculate the noise floor from the bandwidth and the receiver's noise figure. The SNR is simply the received power minus the noise floor, both in dBm. Finally, compare that SNR with the requirement of the modulation scheme to obtain the margin. Working in a column like this makes it almost impossible to drop a term or flip a sign, and it mirrors exactly how practising radio engineers lay out their calculations.

### Choosing a modulation scheme

Conceptual questions sometimes ask which modulation suits a situation. Constant-envelope schemes (FM, FSK, PSK) tolerate non-linear, efficient power amplifiers and amplitude fading, which is why they suit battery-powered and mobile transmitters. Higher-order QAM achieves the best spectral efficiency but needs a high SNR and a linear amplifier, so it suits cable, fibre and short-range wireless links with strong signals. Spread-spectrum and OFDM schemes resist narrowband interference and multipath fading. Matching the scheme to the channel is the essential judgement of communications engineering.
"""),
"ch13.md": ("## Practice Questions", r"""
## Common Traps in Digital Systems

**Gray-code order on K-maps.** Columns must run 00, 01, 11, 10. Labelling them in binary order (00, 01, 10, 11) breaks the adjacency on which the method depends.

**Carry versus overflow.** A carry out of the most significant bit signals unsigned overflow. Signed (two's-complement) overflow is detected separately, by the sign rule. They are different flags.

**Address lines and capacity.** Address lines are set by the number of *words*, not the number of bits. A 64K × 16 memory needs 16 address lines, not 20.
"""),
"ch15.md": ("## Practice Questions", r"""
## Common Traps in Software Engineering

**Inclusive loop bounds.** In the exam's pseudocode, `for i = 1 to n` normally includes both 1 and $n$. Count the iterations carefully when the step is not 1; the loop stops at the last value that does not pass the limit.

**Big-O of sequential code.** Two loops of $n$ one after the other are $O(n)$, not $O(n^2)$. Only nesting multiplies.

**Best, average and worst cases.** When a question asks about an algorithm's complexity without qualification, it usually means the worst case. Quicksort is the classic example: $O(n\log n)$ on average, $O(n^2)$ in the worst case.

**Verification and validation.** Verification checks the product against its specification; validation checks it against the user's real needs. The exam may describe a scenario and ask which one is taking place.

**Black-box versus white-box.** If the tester designs tests from the requirements without seeing the code, it is black-box testing. If the tests are designed to exercise particular branches or paths in the code, it is white-box testing.
"""),
"ch16.md": ("## The Timed Drill", r"""
## A Personal Exam-Day Card

Before the exam, write your own one-page card of reminders—not formulae, which are in the Handbook, but the habits that protect you from your own typical mistakes, drawn from your error log. On exam day you cannot take the card in, but you can reproduce it from memory on the first page of your writing booklet during the tutorial minutes. Writing it out settles the nerves, and having it in front of you for six hours is surprisingly powerful.
"""),
"ch17.md": ("## Mock Exam One: Questions", r"""
## What Each Knowledge Area Will Test

Before you begin, it helps to know what to expect from each part of the paper. The notes below summarise the kinds of question you will meet in this mock exam—and on the real one—and point you to the chapter that covers each area. Read them now, then set them aside: during the exam itself you should rely on the Handbook and your own preparation.

**Mathematics (Chapter 2).** Expect quick algebra, logarithms, complex-number conversions, determinants and simultaneous equations, derivatives and integrals, eigenvalues, vectors, first- and second-order differential equations and simple numerical methods. These questions are mostly short; aim to average two minutes or less.

**Probability and statistics (Chapter 3).** Descriptive statistics, the binomial, Poisson, normal and exponential distributions, Bayes' theorem, reliability block diagrams and confidence intervals. Identifying the right distribution is usually the key step.

**Ethics and professional practice (Chapter 3).** Scenarios about public safety, competence, conflicts of interest, seals, confidentiality, licensure and intellectual property. Read every option; the best answer is usually the one that protects the public honestly and within the engineer's competence.

**Engineering economics (Chapter 3).** Present and future worth, annuities, capital recovery, effective interest, depreciation, break-even and comparison of alternatives. Draw a cash-flow diagram and pick the right factor.

**Properties of electrical materials (Chapters 4 and 9).** Resistivity and temperature coefficients, semiconductor doping and conductivity, dielectrics, magnetic materials and band gaps. Watch your units.

**Circuit analysis (Chapters 4 and 5).** The largest area: series–parallel reduction, dividers, nodal and mesh analysis, superposition, Thévenin and Norton equivalents, maximum power, impedance, resonance, AC power and power-factor correction. Speed here buys time everywhere else.

**Linear systems (Chapter 6).** RC and RL transients, second-order damping, Laplace transforms, transfer functions and poles, initial and final values, and convolution.

**Signal processing (Chapter 7).** Sampling and aliasing, ADC resolution, Fourier series, digital filters, z-transform stability, the DFT and decibels.

**Electronics (Chapter 8).** Diode circuits, rectifiers and ripple, Zener regulators, BJT and MOSFET biasing, small-signal gain and op-amp circuits.

**Power systems (Chapter 10).** Three-phase relationships and power, transformers, per-unit calculations, fault currents and rotating machines.

**Electromagnetics (Chapter 9).** Point charges, capacitance, magnetic fields around conductors, induction, wave propagation, skin depth and transmission lines.

**Control systems (Chapter 11).** Block diagrams, second-order response specifications, steady-state error, Routh stability and Bode margins.

**Communications (Chapter 12).** AM and FM, channel capacity, digital modulation, noise and link budgets.

**Computer networks (Chapter 14).** The OSI model, protocols, IPv4 subnetting, devices and delays.

**Digital systems (Chapter 13).** Number systems and two's complement, Boolean algebra and K-maps, flip-flops, counters, timing and memory.

**Computer systems (Chapter 14).** Performance equations, Amdahl's law, pipelining, caches, virtual memory and I/O.

**Software engineering (Chapter 15).** Code tracing, complexity, data structures, object-oriented concepts, development life cycles and testing.

The questions in this mock exam appear grouped broadly in the order above, as they often are on the computer-based exam. Do not let that lull you into treating each group as a separate test; keep your pace steady across the whole section, and remember that a question you find hard is often followed by several you find easy.

## A Word on Mindset

A mock exam can be an emotional experience. Somewhere around question forty you may feel that it is going badly. Nearly every candidate has that feeling at some point, and it is almost always wrong: the questions you struggle with stick in the mind, while the ones you answered smoothly fade. Keep going. Finish both sections, mark them honestly, and let the numbers—not your feelings during the exam—tell you where you stand.

And whatever the result, remember what it is for. A low mock score now, followed by targeted repair, is far better than a comfortable feeling followed by a disappointing real exam. Every wrong answer in this chapter is a mark you can still win on the day.
"""),
"ch18.md": ("## Mock Exam Two: Questions", r"""
## A Final Look Across the Knowledge Areas

Before you sit this last mock exam, here is a final pass across the specification: for each area, the single idea most worth carrying into the exam room. Think of it as the distilled version of the whole book.

**Mathematics.** Add complex numbers in rectangular form, multiply them in polar form, and always check the quadrant of an angle.

**Probability and statistics.** Decide first which distribution the question describes; the formula follows from that choice.

**Ethics.** Public safety, health and welfare come first, always.

**Engineering economics.** Draw the cash-flow diagram, then let the interest factor convert what you have into what you need.

**Materials.** Metals' resistance rises with temperature; semiconductors' falls. Donors make n-type, acceptors make p-type.

**DC circuits.** Look for the shortcut—divider, Millman, Thévenin—before writing a system of equations.

**AC circuits.** Peak or RMS? $\omega$ or $f$? Never add $R$ and $X$ arithmetically.

**Linear systems.** Capacitor voltage and inductor current are continuous; find them first.

**Signal processing.** Sample above twice the highest frequency present, remembering that products of sinusoids create sum frequencies.

**Electronics.** Model the device, solve, then check the operating region.

**Power systems.** In wye the voltages differ by $\sqrt3$; in delta the currents do. Quoted voltages are line-to-line.

**Electromagnetics.** Convert everything to base SI units before substituting.

**Control systems.** Read $\omega_n$ and $\zeta$ from the denominator in seconds; error constants come from the open loop.

**Communications.** Convert dB to ratios inside Shannon's and Friis's formulae.

**Computer networks.** Usable hosts are $2^h - 2$; know the seven OSI layers in order.

**Digital systems.** Gray-code order on K-maps; overflow only when same-sign operands give a different-sign result.

**Computer systems.** AMAT is hit time plus miss rate times miss penalty; Amdahl limits every speed-up.

**Software engineering.** Trace code in a table; nested loops multiply, sequential loops add.

If each of those eighteen sentences makes immediate sense to you, you are well prepared. If one or two still feel uncertain, turn back to the relevant chapter's summary box for ten minutes before you begin.

## How to Use This Second Mock

Use exactly the same conditions and the same scoring method as for Mock Exam One, so that the comparison between them is fair. Record your answers on a fresh sheet, mark your confidence against each one, and keep to the timing strictly. When you have finished, carry out the full post-mortem described in Chapter 17. The habit of analysing every error is what turns practice into progress, and it is the same habit that will serve you through the PE exam and throughout your professional life.
"""),
}

for fn, (marker, text) in ADD.items():
    p = os.path.join(SRC, fn)
    s = open(p, encoding="utf-8").read()
    if "## Common Traps" in s and fn not in ("ch17.md", "ch18.md", "ch16.md"):
        continue
    if text.strip()[:40] in s:
        continue
    assert marker in s, (fn, marker)
    s = s.replace(marker, text.strip() + "\n\n" + marker, 1)
    open(p, "w", encoding="utf-8").write(s)
    print("added to", fn)
