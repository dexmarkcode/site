# Appendices and Tables {.part .unnumbered}

```{=latex}
\appendix
```

## Transform Tables

### Continuous-time Fourier transform

| $x(t)$ | $X(j\omega)$ |
|:--|:--|
| $\delta(t)$ | $1$ |
| $1$ | $2\pi\delta(\omega)$ |
| $u(t)$ | $\pi\delta(\omega) + \dfrac{1}{j\omega}$ |
| $e^{-at}u(t)$, $a > 0$ | $\dfrac{1}{a + j\omega}$ |
| $t\,e^{-at}u(t)$ | $\dfrac{1}{(a + j\omega)^2}$ |
| $e^{-a|t|}$ | $\dfrac{2a}{a^2 + \omega^2}$ |
| rectangle of height 1, width $T$, centred | $\dfrac{2\sin(\omega T/2)}{\omega}$ |
| triangle of height 1, base $2T$ | $T\,\dfrac{\sin^2(\omega T/2)}{(\omega T/2)^2}$ |
| $\dfrac{\sin Wt}{\pi t}$ | $1$ for $|\omega| < W$ |
| $e^{j\omega_0 t}$ | $2\pi\delta(\omega - \omega_0)$ |
| $\cos\omega_0 t$ | $\pi[\delta(\omega - \omega_0) + \delta(\omega + \omega_0)]$ |
| $\sin\omega_0 t$ | $\dfrac{\pi}{j}[\delta(\omega - \omega_0) - \delta(\omega + \omega_0)]$ |
| $\sum_n\delta(t - nT)$ | $\dfrac{2\pi}{T}\sum_k\delta\!\left(\omega - \dfrac{2\pi k}{T}\right)$ |

### Laplace transform (unilateral, $t \ge 0$)

| $x(t)$ | $X(s)$ |
|:--|:--|
| $\delta(t)$ | $1$ |
| $u(t)$ | $1/s$ |
| $t^n$ | $n!/s^{n+1}$ |
| $e^{-at}$ | $1/(s + a)$ |
| $t^ne^{-at}$ | $n!/(s + a)^{n+1}$ |
| $\cos\omega_0 t$ | $s/(s^2 + \omega_0^2)$ |
| $\sin\omega_0 t$ | $\omega_0/(s^2 + \omega_0^2)$ |
| $e^{-at}\cos\omega_0 t$ | $(s + a)/((s + a)^2 + \omega_0^2)$ |
| $e^{-at}\sin\omega_0 t$ | $\omega_0/((s + a)^2 + \omega_0^2)$ |
| $t\cos\omega_0 t$ | $(s^2 - \omega_0^2)/(s^2 + \omega_0^2)^2$ |
| $t\sin\omega_0 t$ | $2\omega_0 s/(s^2 + \omega_0^2)^2$ |

### Z-transform

| $x[n]$ | $X(z)$ | ROC |
|:--|:--|:--|
| $\delta[n]$ | $1$ | all $z$ |
| $\delta[n - k]$ | $z^{-k}$ | $z \ne 0$ |
| $u[n]$ | $z/(z - 1)$ | $|z| > 1$ |
| $a^nu[n]$ | $z/(z - a)$ | $|z| > |a|$ |
| $-a^nu[-n-1]$ | $z/(z - a)$ | $|z| < |a|$ |
| $na^nu[n]$ | $az/(z - a)^2$ | $|z| > |a|$ |
| $r^n\cos(\theta n)u[n]$ | $\dfrac{z(z - r\cos\theta)}{z^2 - 2rz\cos\theta + r^2}$ | $|z| > r$ |
| $r^n\sin(\theta n)u[n]$ | $\dfrac{zr\sin\theta}{z^2 - 2rz\cos\theta + r^2}$ | $|z| > r$ |

### Discrete-time Fourier transform

| $x[n]$ | $X(e^{j\omega})$ |
|:--|:--|
| $\delta[n]$ | $1$ |
| $a^nu[n]$, $|a| < 1$ | $\dfrac{1}{1 - ae^{-j\omega}}$ |
| $u[n] - u[n - N]$ | $e^{-j\omega(N-1)/2}\dfrac{\sin(N\omega/2)}{\sin(\omega/2)}$ |
| $\dfrac{\sin\omega_c n}{\pi n}$ | $1$ for $|\omega| < \omega_c$ |

## Properties at a Glance

| Property | Fourier ($j\omega$) | Laplace ($s$) | Z ($z$) |
|:--|:--|:--|:--|
| Delay | $e^{-j\omega t_0}X$ | $e^{-st_0}X$ | $z^{-k}X$ |
| Modulation | $X(j(\omega - \omega_0))$ | $X(s - s_0)$ | $X(z/a)$ |
| Differentiation / difference | $j\omega X$ | $sX - x(0^-)$ | $(1 - z^{-1})X$ |
| Multiplication by $t$ or $n$ | $j\,dX/d\omega$ | $-dX/ds$ | $-z\,dX/dz$ |
| Convolution | $XH$ | $XH$ | $XH$ |
| Initial value | | $\lim_{s\to\infty}sX$ | $\lim_{z\to\infty}X$ |
| Final value | | $\lim_{s\to0}sX$ | $\lim_{z\to1}(z - 1)X$ |
| Stability (causal) | | poles in $\operatorname{Re}(s) < 0$ | poles in $|z| < 1$ |

## Mathematical Toolkit

### Complex numbers

$e^{j\theta} = \cos\theta + j\sin\theta$. For $z = a + jb$: $|z| = \sqrt{a^2 + b^2}$, and $\angle z = \tan^{-1}(b/a)$ adjusted by $\pm\pi$ when $a < 0$. Multiplying complex numbers multiplies magnitudes and adds angles; $zz^* = |z|^2$; $1/j = -j$.

### Useful identities

$$\cos A\cos B = \tfrac12[\cos(A - B) + \cos(A + B)],$$
$$\sin^2\theta = \tfrac12(1 - \cos2\theta), \qquad \cos^2\theta = \tfrac12(1 + \cos2\theta).$$

### Geometric series

$$\sum_{n=0}^{N-1}a^n = \frac{1 - a^N}{1 - a}, \qquad \sum_{n=0}^{\infty}a^n = \frac{1}{1 - a}\ (|a| < 1),$$
$$\sum_{n=0}^{\infty}na^n = \frac{a}{(1 - a)^2}\ (|a| < 1).$$

### Partial fractions

For distinct poles, $A_i = (s + p_i)F(s)\big|_{s = -p_i}$ (cover-up). For a pole of order $m$ at $-a$, the coefficient of $(s + a)^{-k}$ is
$$\frac{1}{(m - k)!}\,\frac{d^{\,m-k}}{ds^{\,m-k}}\Big[(s + a)^mF(s)\Big]_{s = -a}.$$
For an irreducible quadratic, complete the square and match to the damped cosine and sine pairs. If the function is improper, divide first.

### Second-order systems

For $\dfrac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}$ with $0 < \zeta < 1$:
$$\omega_d = \omega_n\sqrt{1 - \zeta^2}, \qquad M_p = e^{-\pi\zeta/\sqrt{1 - \zeta^2}},$$
$$T_p = \frac{\pi}{\omega_d}, \qquad T_s \approx \frac{4}{\zeta\omega_n}.$$

## Glossary

**Aliasing.** The appearance of a high frequency as a lower one after sampling, caused by overlapping spectral copies.

**BIBO stability.** Every bounded input produces a bounded output. For LTI systems, equivalent to an absolutely integrable or summable impulse response.

**Causal.** The output never depends on future inputs. For LTI systems, $h = 0$ for negative time.

**Convolution.** The operation $\int x(\tau)h(t - \tau)\,d\tau$ or $\sum x[k]h[n - k]$ that gives the output of an LTI system.

**Damping ratio.** The parameter $\zeta$ of a second-order system that fixes the shape of its response: overdamped above one, underdamped below.

**DFT.** The discrete Fourier transform, $N$ samples of the DTFT of a finite sequence, computed in practice by the FFT.

**Eigenfunction.** A signal that passes through a system unchanged in shape, only scaled. Complex exponentials are eigenfunctions of every LTI system.

**FIR / IIR.** Finite or infinite impulse response; filters without or with feedback.

**Frequency response.** $H(j\omega)$ or $H(e^{j\omega})$: the complex gain of an LTI system at each frequency.

**Gibbs phenomenon.** The persistent overshoot of about 9% near a discontinuity in a truncated Fourier series.

**Linear phase.** A phase response proportional to frequency, giving the same time delay at every frequency.

**Nyquist rate.** Twice the highest frequency in a signal; the minimum sampling rate for exact reconstruction.

**Parseval's relation.** Energy or power is the same whether computed in time or in frequency.

**Pole / zero.** A root of the denominator / numerator of a rational transfer function.

**Region of convergence.** The set of $s$ or $z$ for which a Laplace or Z-transform converges. Together with the formula, it determines the signal uniquely.

**Routh–Hurwitz criterion.** A tabular test that counts right-half-plane roots of a polynomial without solving it.

**Transfer function.** $H(s)$ or $H(z)$: the ratio of output to input transforms for a system at rest.

## About the Author {.unnumbered}

Marcus J. Thornton holds a Ph.D. in electrical engineering and has taught signals and systems, control and digital signal processing to undergraduate and postgraduate students for many years. His teaching is known for its emphasis on method, intuition and careful checking, and for the conviction that anyone willing to practise can become fluent in the mathematics of engineering.

He has worked alongside industrial engineers on problems in instrumentation, filtering and control, and much of the practical advice in this book comes from that experience. He writes in the belief that a good problem, properly solved and properly explained, teaches more than many pages of theory.
