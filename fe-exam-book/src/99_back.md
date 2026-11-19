```{=latex}
\backmatter
```

# Appendix A: Formula Summary {.unnumbered}

This summary gathers the relationships used most often on the exam. Most also appear, sometimes in a different form, in the *FE Reference Handbook*; those marked † are ones you should know cold, because they are absent from the Handbook or slow to find there. Review this appendix in the last few days before your exam.

## Mathematics {.unnumbered}

| Topic | Relationship |
|:--|:--|
| Quadratic roots | $x = \dfrac{-b \pm \sqrt{b^2 - 4ac}}{2a}$ |
| Polar form | $M = \sqrt{a^2 + b^2}$, $\theta = \tan^{-1}(b/a)$ (check quadrant) |
| Complex product/quotient | Multiply magnitudes, add angles / divide magnitudes, subtract angles |
| Euler | $e^{j\theta} = \cos\theta + j\sin\theta$ |
| $2\times2$ determinant / inverse | $ad - bc$; swap diagonal, negate off-diagonal, divide by determinant |
| Eigenvalues ($2\times2$) | $\lambda^2 - (\text{trace})\lambda + \det = 0$ |
| Dot / cross product | $\mathbf{A}\cdot\mathbf{B} = AB\cos\theta$; $|\mathbf{A}\times\mathbf{B}| = AB\sin\theta$ |
| RMS of DC + sinusoid † | $\sqrt{V_0^2 + V_m^2/2}$ |
| First-order ODE | $y = y_\infty + (y_0 - y_\infty)e^{-t/\tau}$ |
| Second-order | $\omega_n = \sqrt{c}$, $\zeta = b/(2\omega_n)$ for $\ddot{y} + b\dot{y} + cy$ |
| Newton's method | $x_{n+1} = x_n - f(x_n)/f'(x_n)$ |
| Trapezoidal rule | $\frac{h}{2}[f_0 + 2f_1 + \cdots + 2f_{n-1} + f_n]$ |

## Probability, Statistics and Economics {.unnumbered}

| Topic | Relationship |
|:--|:--|
| Sample standard deviation | $s = \sqrt{\sum(x_i - \bar{x})^2/(n - 1)}$ |
| Binomial | $P(k) = \binom{n}{k}p^k(1-p)^{n-k}$ |
| Poisson | $P(k) = \lambda^ke^{-\lambda}/k!$ |
| Normal | $z = (x - \mu)/\sigma$ |
| Exponential reliability | $R(t) = e^{-\lambda t}$, MTBF $= 1/\lambda$ |
| Series / parallel reliability | $\prod R_i$; $1 - \prod(1 - R_i)$ |
| Confidence interval ($\sigma$ known) | $\bar{x} \pm z_{\alpha/2}\sigma/\sqrt{n}$ |
| Present worth | $P = F(1+i)^{-n}$; $P = A\dfrac{(1+i)^n - 1}{i(1+i)^n}$ |
| Capital recovery | $A = P\dfrac{i(1+i)^n}{(1+i)^n - 1}$ |
| Effective rate | $i_e = (1 + r/m)^m - 1$ |
| EUAC | $P(A/P) + O - S(A/F)$ |
| Straight-line depreciation | $D = (C - S)/n$ |
| Break-even | $Q = F/(p - v)$ |

## Circuits {.unnumbered}

| Topic | Relationship |
|:--|:--|
| Resistance | $R = \rho L/A$; $R_T = R_0[1 + \alpha(T - T_0)]$ |
| Voltage divider † | $V_2 = V_sR_2/(R_1 + R_2)$ |
| Current divider † | $I_1 = IR_2/(R_1 + R_2)$ |
| Single-node voltage (Millman) † | $V = \dfrac{\sum V_k/R_k}{\sum 1/R_k}$ |
| Maximum power | $P_{max} = V_{Th}^2/(4R_{Th})$; AC: $\mathbf{Z}_L = \mathbf{Z}_{Th}^*$ |
| Δ to Y | $R_a = R_{ab}R_{ca}/(R_{ab} + R_{bc} + R_{ca})$; balanced $R_Y = R_\Delta/3$ |
| Stored energy | $\frac12CV^2$; $\frac12LI^2$ |
| Impedances | $j\omega L$; $1/(j\omega C)$ |
| Series resonance | $f_0 = 1/(2\pi\sqrt{LC})$; $Q = \omega_0L/R$; $B = R/(2\pi L)$ Hz |
| AC power | $\mathbf{S} = \mathbf{VI}^* = P + jQ$; $P = VI\cos\theta$ |
| PF correction | $Q_C = P(\tan\theta_1 - \tan\theta_2)$; $C = Q_C/(\omega V^2)$ |
| RC / RL time constants | $\tau = RC$; $\tau = L/R$ |
| Series RLC damping | $\alpha = R/2L$, $\zeta = \frac{R}{2}\sqrt{C/L}$ |
| Initial / final value | $f(0^+) = \lim_{s\to\infty}sF(s)$; $f(\infty) = \lim_{s\to0}sF(s)$ |

## Signals and Electronics {.unnumbered}

| Topic | Relationship |
|:--|:--|
| Nyquist | $f_s > 2f_{max}$; alias $f_a = |f - kf_s|$ |
| ADC | $\varepsilon = V_{FS}/2^N$; SQNR $\approx 6.02N + 1.76$ dB |
| DFT resolution | $\Delta f = f_s/N$ |
| Square-wave harmonics | $4A/(n\pi)$, odd $n$ |
| Decibels | $10\log(P_2/P_1)$; $20\log(V_2/V_1)$ |
| RC filter | $f_c = 1/(2\pi RC)$ |
| Rectifier average | $V_p/\pi$ (half); $2V_p/\pi$ (full) |
| Ripple | $I/(fC)$ (half); $I/(2fC)$ (full) |
| BJT | $I_C = \beta I_B$; $g_m = I_C/V_T$; $A_v \approx -g_mR_C$ |
| MOSFET (saturation) | $i_D = K(v_{GS} - V_t)^2$ |
| Op-amps † | Inverting $-R_f/R_{in}$; non-inverting $1 + R_f/R_1$ |

## Electromagnetics {.unnumbered}

| Topic | Relationship |
|:--|:--|
| Point charge | $F = kq_1q_2/r^2$; $E = kq/r^2$; $k = 8.99\times10^9$ |
| Parallel plates | $C = \varepsilon_r\varepsilon_0A/d$; $E = V/d$ |
| Long wire / solenoid | $B = \mu I/(2\pi r)$; $L = \mu N^2A/\ell$ |
| Force / induction | $F = BIL\sin\theta$; $\mathcal{E} = -N\,d\Phi/dt$ |
| Waves | $v = c/\sqrt{\varepsilon_r}$; $\eta = 377/\sqrt{\varepsilon_r}$ |
| Skin depth | $\delta = 1/\sqrt{\pi f\mu\sigma}$ |
| Transmission lines | $\Gamma = (Z_L - Z_0)/(Z_L + Z_0)$; VSWR $= (1 + |\Gamma|)/(1 - |\Gamma|)$ |
| Quarter-wave match | $Z_q = \sqrt{Z_1Z_2}$ |

## Power, Control and Communications {.unnumbered}

| Topic | Relationship |
|:--|:--|
| Wye / delta † | Wye $V_L = \sqrt3V_p$; delta $I_L = \sqrt3I_p$ |
| Three-phase power | $P = \sqrt3V_LI_L\cos\theta$ |
| Transformer | $V_1/V_2 = a$; $Z' = a^2Z$ |
| Per-unit base change | $Z_{new} = Z_{old}(S_{new}/S_{old})(V_{old}/V_{new})^2$ |
| Fault current | $I_f = I_b/X_{pu}$; $I_b = S_b/(\sqrt3V_b)$ |
| Machines | $n_s = 120f/P$; $s = (n_s - n_r)/n_s$; $T = P/\omega$ |
| Closed loop | $T = G/(1 + GH)$ |
| Second-order specs | $\%OS = 100e^{-\zeta\pi/\sqrt{1-\zeta^2}}$; $T_s \approx 4/(\zeta\omega_n)$ |
| Steady-state error | Step $1/(1 + K_p)$; ramp $1/K_v$ |
| AM | $P_t = P_c(1 + m^2/2)$; $B = 2W$ |
| FM (Carson) | $B \approx 2(\Delta f + f_m)$ |
| Capacity | Shannon $B\log_2(1 + \text{SNR})$; Nyquist $2B\log_2M$ |
| Noise | $-174$ dBm/Hz $+ 10\log B$; Friis $F = F_1 + (F_2 - 1)/G_1$ |
| Free-space loss | $20\log d_{km} + 20\log f_{MHz} + 32.44$ |

## Digital and Computing {.unnumbered}

| Topic | Relationship |
|:--|:--|
| Two's-complement range | $-2^{n-1}$ to $2^{n-1} - 1$ |
| Maximum clock | $f_{max} = 1/(t_{CQ} + t_{logic} + t_{su})$ |
| Flip-flops for mod-$N$ | $\lceil\log_2N\rceil$ |
| CPU time | IC × CPI / $f$ |
| Amdahl | $S = 1/[(1-f) + f/k]$ |
| Pipeline speed-up | $nk/(k + n - 1)$ |
| AMAT | $t_{hit} + \text{miss rate}\times\text{penalty}$ |
| Cache fields | offset $\log_2B$; index $\log_2(\text{sets})$; tag = rest |
| Usable hosts † | $2^{32 - \text{prefix}} - 2$ |
| Delays | $L/R$ (bits); $d/v$ |
| Binary search | $\lfloor\log_2n\rfloor + 1$ comparisons |

# Appendix B: Constants and Conversions {.unnumbered}

| Constant | Symbol | Value |
|:--|:--|:--|
| Elementary charge | $q$ | $1.602\times10^{-19}$ C |
| Permittivity of free space | $\varepsilon_0$ | $8.854\times10^{-12}$ F/m |
| Permeability of free space | $\mu_0$ | $4\pi\times10^{-7}$ H/m |
| Speed of light | $c$ | $2.998\times10^8$ m/s |
| Coulomb constant | $1/(4\pi\varepsilon_0)$ | $8.99\times10^9$ N·m²/C² |
| Intrinsic impedance of free space | $\eta_0$ | $\approx 377$ Ω |
| Boltzmann constant | $k$ | $1.381\times10^{-23}$ J/K |
| Planck constant | $h$ | $6.626\times10^{-34}$ J·s |
| Thermal voltage at 300 K | $V_T$ | $\approx 25.9$ mV (26 mV used in this book) |
| $kT_0$ at 290 K | | $-174$ dBm/Hz |
| $hc$ | | $\approx 1240$ eV·nm |
| Resistivity of copper (20 °C) | $\rho$ | $1.72\times10^{-8}$ Ω·m |
| Conductivity of copper | $\sigma$ | $5.8\times10^7$ S/m |
| Temperature coefficient, copper (20 °C) | $\alpha$ | 0.00393 /°C |

Table: Physical constants.

| Quantity | Conversion |
|:--|:--|
| Power | 1 hp = 746 W |
| Energy | 1 kWh = 3.6 MJ; 1 eV = $1.602\times10^{-19}$ J; 1 Btu = 1055 J |
| Angular speed | $\omega$ (rad/s) $= 2\pi n/60$, with $n$ in rpm |
| Frequency | $\omega = 2\pi f$ |
| Length | 1 in = 25.4 mm; 1 ft = 0.3048 m; 1 mile = 1.609 km |
| Area | 1 cm² = $10^{-4}$ m²; 1 mm² = $10^{-6}$ m² |
| Magnetic flux density | 1 T = 1 Wb/m² = $10^4$ gauss |
| Decibel references | 0 dBm = 1 mW; 0 dBW = 1 W; 30 dBm = 0 dBW |
| Temperature | K = °C + 273.15; °F = 1.8 °C + 32 |
| Data | 1 byte = 8 bits; 1 KiB = 1024 bytes |

Table: Useful conversions.

| Prefix | Symbol | Factor | Prefix | Symbol | Factor |
|:--|:--|:--|:--|:--|:--|
| tera | T | $10^{12}$ | milli | m | $10^{-3}$ |
| giga | G | $10^9$ | micro | μ | $10^{-6}$ |
| mega | M | $10^6$ | nano | n | $10^{-9}$ |
| kilo | k | $10^3$ | pico | p | $10^{-12}$ |

Table: SI prefixes.

# Glossary {.unnumbered}

**Admittance** — The reciprocal of impedance, $Y = G + jB$, in siemens.

**Aliasing** — The appearance of a frequency above half the sampling rate as a lower, false frequency after sampling.

**Amdahl's law** — The overall speed-up from improving part of a system is limited by the fraction that is not improved.

**Apparent power** — The product of RMS voltage and current, $|S| = VI$, in volt-amperes.

**Bandwidth** — The range of frequencies a signal occupies or a system passes; for a resonant circuit, the width between half-power points.

**Bode plot** — Graphs of a system's magnitude (in dB) and phase against logarithmic frequency.

**Cache** — A small, fast memory holding copies of recently used data from a larger, slower memory.

**Characteristic equation** — The equation whose roots are a system's natural frequencies (poles); for feedback systems, $1 + GH = 0$.

**CIDR** — Classless inter-domain routing; IP addressing with a prefix length such as /24.

**Comity** — Licensure in a second jurisdiction on the basis of a licence held in another.

**Complex power** — $\mathbf{S} = \mathbf{VI}^* = P + jQ$.

**Convolution** — The operation giving an LTI system's output from its input and impulse response.

**Critical damping** — The boundary between overdamped and underdamped responses, $\zeta = 1$.

**Damping ratio** ($\zeta$) — A dimensionless measure of how quickly oscillations in a second-order system decay.

**Decibel** — A logarithmic unit of ratio: $10\log$ for power, $20\log$ for voltage or current.

**Dielectric** — An insulating material that polarises in an electric field; characterised by its relative permittivity.

**DMA** — Direct memory access; block transfers between devices and memory without the CPU moving each word.

**Doping** — Adding impurities to a semiconductor to create n-type (donor) or p-type (acceptor) material.

**EIRP** — Effective isotropic radiated power; transmitter power plus antenna gain, less feeder loss.

**Encapsulation** — Bundling data with its methods and hiding internal state behind an interface.

**Engineer Intern (EI)** — The designation, also called Engineer-in-Training (EIT), typically granted after passing the FE exam.

**EUAC** — Equivalent uniform annual cost; a way of comparing alternatives as equal annual amounts.

**FIR filter** — A digital filter whose output depends only on present and past inputs; always stable.

**Flip-flop** — An edge-triggered one-bit memory element.

**Gain margin** — How much the loop gain can rise, at the phase-crossover frequency, before instability.

**Hysteresis** — Dependence of a magnetic material's flux density on its history; the loop area is the energy lost per cycle.

**IIR filter** — A digital filter with feedback, whose impulse response may continue indefinitely.

**Impedance** — The ratio of voltage phasor to current phasor, $Z = R + jX$.

**Inheritance** — An object-oriented mechanism by which a subclass acquires the members of a parent class.

**Intrinsic impedance** — The ratio of electric to magnetic field in a plane wave; about 377 Ω in free space.

**K-map** — Karnaugh map; a grid for simplifying Boolean expressions by grouping adjacent minterms.

**Laplace transform** — A transform converting differential equations in time into algebraic equations in $s$.

**Lenz's law** — An induced current opposes the change in flux that produces it.

**Linear system** — A system obeying superposition.

**Mealy machine** — A state machine whose outputs depend on the present state and inputs.

**Modulation index** — For AM, the ratio of message to carrier amplitude; for FM, $\Delta f/f_m$.

**Moore machine** — A state machine whose outputs depend only on the present state.

**NCEES** — The National Council of Examiners for Engineering and Surveying, which develops the FE and PE exams.

**Noise figure** — The degradation of signal-to-noise ratio through a device, in dB.

**Norton equivalent** — A current source in parallel with a resistance, equivalent to any linear two-terminal network.

**Nyquist rate** — Twice the highest frequency in a signal; the minimum sampling rate for perfect reconstruction.

**OSI model** — The seven-layer reference model for network communication.

**Overflow** — A result too large for the available bits; in two's complement, when same-sign operands give a different-sign result.

**Per unit** — Expression of a quantity as a fraction of a chosen base value.

**Phase margin** — Additional phase lag, at the gain-crossover frequency, that would cause instability.

**Phasor** — A complex number representing the amplitude and phase of a sinusoid.

**Pipeline** — Overlapping execution of instruction stages to raise throughput.

**Pole** — A root of a transfer function's denominator; poles determine the natural response and stability.

**Polymorphism** — One interface invoking different behaviour depending on an object's actual type.

**Power factor** — The ratio of real to apparent power, $\cos\theta$.

**Quality factor** ($Q$) — A measure of the sharpness of resonance; resonant frequency divided by bandwidth.

**Reactive power** — Power oscillating between source and reactive elements, $Q = VI\sin\theta$, in var.

**Reflection coefficient** — The ratio of reflected to incident voltage at a transmission-line discontinuity.

**RMS** — Root-mean-square; the effective value of a varying quantity, $V_m/\sqrt2$ for a sinusoid.

**Routh–Hurwitz criterion** — A test for the number of right-half-plane roots of a polynomial.

**Setup time** — The minimum time data must be stable before a clock edge.

**Skin depth** — The depth at which current density in a conductor falls to $1/e$ of its surface value.

**Slip** — The fractional difference between synchronous and rotor speed in an induction motor.

**Steady-state error** — The difference between reference and output after transients have died away.

**Subnet mask** — The bit pattern separating the network and host parts of an IP address.

**Superposition** — In a linear circuit, the total response equals the sum of responses to each source acting alone.

**Synchronous speed** — The speed of the rotating magnetic field in an AC machine, $120f/P$ rpm.

**Thévenin equivalent** — A voltage source in series with a resistance, equivalent to any linear two-terminal network.

**Time constant** — The characteristic time of a first-order response; $RC$ or $L/R$.

**TLB** — Translation lookaside buffer; a cache of virtual-to-physical page translations.

**Transfer function** — The ratio of output to input transforms of an LTI system with zero initial conditions.

**Two's complement** — The standard binary representation of signed integers.

**VSWR** — Voltage standing-wave ratio; the ratio of maximum to minimum voltage on a mismatched line.

**Zener diode** — A diode designed to operate in reverse breakdown at a well-defined voltage.

**z-transform** — The discrete-time counterpart of the Laplace transform; stability requires poles inside the unit circle.

# About the Author {.unnumbered .nodrop}

**Marcus J. Thornton, Ph.D.,** is an electrical engineer and educator with a lifelong interest in helping engineers through the licensure process. His teaching combines rigorous technical explanation with a practical focus on how examinations actually test knowledge—an approach shaped by years of working alongside students and early-career engineers as they prepared for the Fundamentals of Engineering exam.

He believes that passing the FE is less about talent than about method: understanding the exam as a system, practising deliberately, and learning from every mistake. This book distils that philosophy into a single, complete guide.

He writes in British English and welcomes feedback from readers on how the book helped them prepare.
