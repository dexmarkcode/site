## Appendix A: Formula Summary

This appendix gathers the key results of every chapter on a few pages. It is meant for revision and quick reference, not as a substitute for understanding where each formula comes from. Before an examination, try writing out this list from memory; the gaps you find are the topics to revise.

### Fundamentals (Chapter 1)

| Quantity | Relationship | Unit |
|---|---|---|
| Current | <i>I</i> = <i>Q</i>/<i>t</i>, <i>i</i> = d<i>q</i>/d<i>t</i> | A |
| Ohm's law | <i>V</i> = <i>IR</i> | V |
| Conductance | <i>G</i> = 1/<i>R</i> | S |
| Power | <i>P</i> = <i>VI</i> = <i>I</i><sup>2</sup><i>R</i> = <i>V</i><sup>2</sup>/<i>R</i> | W |
| Energy | <i>W</i> = <i>Pt</i>; 1 kWh = 3.6 MJ | J |
| Resistivity | <i>R</i> = ρ<i>L</i>/<i>A</i> | Ω |
| Temperature | <i>R</i> = <i>R</i><sub>0</sub>(1 + αΔθ) | Ω |
| Efficiency | η = <i>P</i><sub>out</sub>/<i>P</i><sub>in</sub> | — |

### Resistive networks (Chapters 2 and 3)

| Result | Formula |
|---|---|
| Series | <i>R</i><sub>eq</sub> = <i>R</i><sub>1</sub> + <i>R</i><sub>2</sub> + … |
| Parallel | 1/<i>R</i><sub>eq</sub> = 1/<i>R</i><sub>1</sub> + 1/<i>R</i><sub>2</sub> + …; two resistors: <i>R</i><sub>1</sub><i>R</i><sub>2</sub>/(<i>R</i><sub>1</sub> + <i>R</i><sub>2</sub>) |
| Voltage divider | <i>V</i><sub>2</sub> = <i>V</i> <i>R</i><sub>2</sub>/(<i>R</i><sub>1</sub> + <i>R</i><sub>2</sub>) |
| Current divider | <i>I</i><sub>1</sub> = <i>I</i> <i>R</i><sub>2</sub>/(<i>R</i><sub>1</sub> + <i>R</i><sub>2</sub>) |
| Δ → Y | <i>R</i><sub>a</sub> = <i>R</i><sub>ab</sub><i>R</i><sub>ca</sub>/(<i>R</i><sub>ab</sub> + <i>R</i><sub>bc</sub> + <i>R</i><sub>ca</sub>), and similarly |
| Y → Δ | <i>R</i><sub>ab</sub> = (<i>R</i><sub>a</sub><i>R</i><sub>b</sub> + <i>R</i><sub>b</sub><i>R</i><sub>c</sub> + <i>R</i><sub>c</sub><i>R</i><sub>a</sub>)/<i>R</i><sub>c</sub>, and similarly |
| Bridge balance | <i>R</i><sub>1</sub>/<i>R</i><sub>3</sub> = <i>R</i><sub>2</sub>/<i>R</i><sub>4</sub> |
| KCL | Σ<i>i</i> = 0 at any node |
| KVL | Σ<i>v</i> = 0 round any closed loop |

### Systematic methods and theorems (Chapters 4 to 6)

| Result | Formula |
|---|---|
| Nodal (matrix form) | <b>G v</b> = <b>i</b>; <i>G</i><sub>kk</sub> = total conductance at node k, <i>G</i><sub>jk</sub> = −(conductance between j and k) |
| Mesh (matrix form) | <b>R i</b> = <b>v</b>; <i>R</i><sub>kk</sub> = total resistance of mesh k, <i>R</i><sub>jk</sub> = −(shared resistance) |
| Millman | <i>V</i> = Σ(<i>E</i><sub>k</sub>/<i>R</i><sub>k</sub>)/Σ(1/<i>R</i><sub>k</sub>) |
| Thévenin | <i>V</i><sub>Th</sub> = <i>V</i><sub>oc</sub>; <i>R</i><sub>Th</sub> = <i>V</i><sub>oc</sub>/<i>I</i><sub>sc</sub> |
| Norton | <i>I</i><sub>N</sub> = <i>I</i><sub>sc</sub>; <i>R</i><sub>N</sub> = <i>R</i><sub>Th</sub> |
| Maximum power | <i>R</i><sub>L</sub> = <i>R</i><sub>Th</sub>, <i>P</i><sub>max</sub> = <i>V</i><sub>Th</sub><sup>2</sup>/4<i>R</i><sub>Th</sub> |

### Energy storage and transients (Chapters 7 to 9)

| Result | Capacitor | Inductor |
|---|---|---|
| Terminal law | <i>i</i> = <i>C</i> d<i>v</i>/d<i>t</i> | <i>v</i> = <i>L</i> d<i>i</i>/d<i>t</i> |
| Stored energy | ½<i>CV</i><sup>2</sup> | ½<i>LI</i><sup>2</sup> |
| Cannot change instantly | voltage | current |
| DC steady state | open circuit | short circuit |
| Series combination | 1/<i>C</i> = Σ1/<i>C</i><sub>k</sub> | <i>L</i> = Σ<i>L</i><sub>k</sub> |
| Parallel combination | <i>C</i> = Σ<i>C</i><sub>k</sub> | 1/<i>L</i> = Σ1/<i>L</i><sub>k</sub> |
| Time constant | τ = <i>R</i><sub>Th</sub><i>C</i> | τ = <i>L</i>/<i>R</i><sub>Th</sub> |

First-order response: <i>x</i>(<i>t</i>) = <i>x</i>(∞) + [<i>x</i>(0<sup>+</sup>) − <i>x</i>(∞)]e<sup>−<i>t</i>/τ</sup>.

Second-order: ω<sub>0</sub> = 1/√(<i>LC</i>); series α = <i>R</i>/2<i>L</i>; parallel α = 1/2<i>RC</i>; ζ = α/ω<sub>0</sub>; ω<sub>d</sub> = √(ω<sub>0</sub><sup>2</sup> − α<sup>2</sup>). Overdamped if α > ω<sub>0</sub>, critically damped if α = ω<sub>0</sub>, underdamped if α < ω<sub>0</sub>.

### AC circuits (Chapters 10 to 12)

| Result | Formula |
|---|---|
| RMS of sinusoid | <i>V</i><sub>rms</sub> = <i>V</i><sub>m</sub>/√2 |
| Impedances | <b>Z</b><sub>R</sub> = <i>R</i>; <b>Z</b><sub>L</sub> = jω<i>L</i>; <b>Z</b><sub>C</sub> = 1/(jω<i>C</i>) = −j/(ω<i>C</i>) |
| Resonance | ω<sub>0</sub> = 1/√(<i>LC</i>); series <i>Q</i> = ω<sub>0</sub><i>L</i>/<i>R</i>; parallel <i>Q</i> = ω<sub>0</sub><i>RC</i>; <i>B</i> = <i>f</i><sub>0</sub>/<i>Q</i> |
| Complex power | <b>S</b> = <b>V I</b>* = <i>P</i> + j<i>Q</i> |
| Real power | <i>P</i> = <i>V</i><sub>rms</sub><i>I</i><sub>rms</sub> cos θ |
| Reactive power | <i>Q</i> = <i>V</i><sub>rms</sub><i>I</i><sub>rms</sub> sin θ |
| pf correction | <i>Q</i><sub>C</sub> = <i>P</i>(tan θ<sub>1</sub> − tan θ<sub>2</sub>); <i>C</i> = <i>Q</i><sub>C</sub>/(ω<i>V</i><sup>2</sup>) |
| AC max power | <b>Z</b><sub>L</sub> = <b>Z</b><sub>Th</sub>* |
| Star | <i>V</i><sub>L</sub> = √3 <i>V</i><sub>ph</sub>, <i>I</i><sub>L</sub> = <i>I</i><sub>ph</sub> |
| Delta | <i>V</i><sub>L</sub> = <i>V</i><sub>ph</sub>, <i>I</i><sub>L</sub> = √3 <i>I</i><sub>ph</sub> |
| Three-phase power | <i>P</i> = √3 <i>V</i><sub>L</sub><i>I</i><sub>L</sub> cos φ |
| Two-wattmeter | <i>P</i> = <i>W</i><sub>1</sub> + <i>W</i><sub>2</sub>; tan φ = √3(<i>W</i><sub>1</sub> − <i>W</i><sub>2</sub>)/(<i>W</i><sub>1</sub> + <i>W</i><sub>2</sub>) |

## Appendix B: Units, Prefixes and Standard Values

### SI prefixes

| Prefix | Symbol | Multiplier | Typical use |
|---|---|---|---|
| giga | G | 10<sup>9</sup> | GHz radio frequencies, GW power stations |
| mega | M | 10<sup>6</sup> | MΩ insulation resistance, MW generators |
| kilo | k | 10<sup>3</sup> | kΩ resistors, kW loads, kV distribution |
| milli | m | 10<sup>−3</sup> | mA signal currents, mH inductors |
| micro | μ | 10<sup>−6</sup> | μF capacitors, μs time constants |
| nano | n | 10<sup>−9</sup> | nF capacitors, ns switching times |
| pico | p | 10<sup>−12</sup> | pF stray capacitance |

### Electrical quantities

| Quantity | Symbol | Unit | Unit symbol |
|---|---|---|---|
| Charge | <i>Q</i> | coulomb | C |
| Current | <i>I</i> | ampere | A |
| Voltage | <i>V</i> | volt | V |
| Resistance | <i>R</i> | ohm | Ω |
| Conductance | <i>G</i> | siemens | S |
| Capacitance | <i>C</i> | farad | F |
| Inductance | <i>L</i> | henry | H |
| Power (real) | <i>P</i> | watt | W |
| Reactive power | <i>Q</i> | volt-ampere reactive | var |
| Apparent power | <i>S</i> | volt-ampere | VA |
| Frequency | <i>f</i> | hertz | Hz |
| Angular frequency | ω | radian per second | rad/s |

### The E12 preferred values

Resistors and capacitors are manufactured in logarithmically spaced series so that, allowing for tolerance, every value is covered. The E12 series (10 % tolerance) is: 1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2, repeated in every decade. When a design calculation produces an awkward value, choose the nearest preferred value and check that the circuit still meets its specification.

### Resistor colour code

| Colour | Digit | Multiplier | Tolerance |
|---|---|---|---|
| Black | 0 | × 1 | — |
| Brown | 1 | × 10 | ±1 % |
| Red | 2 | × 100 | ±2 % |
| Orange | 3 | × 1 k | — |
| Yellow | 4 | × 10 k | — |
| Green | 5 | × 100 k | ±0.5 % |
| Blue | 6 | × 1 M | ±0.25 % |
| Violet | 7 | × 10 M | ±0.1 % |
| Grey | 8 | — | — |
| White | 9 | — | — |
| Gold | — | × 0.1 | ±5 % |
| Silver | — | × 0.01 | ±10 % |

### Useful constants

| Constant | Value |
|---|---|
| Electronic charge, <i>e</i> | 1.602 × 10<sup>−19</sup> C |
| Permittivity of free space, ε<sub>0</sub> | 8.854 × 10<sup>−12</sup> F/m |
| Permeability of free space, μ<sub>0</sub> | 4π × 10<sup>−7</sup> H/m |
| Resistivity of copper (20 °C) | 1.72 × 10<sup>−8</sup> Ω m |
| Temperature coefficient of copper (20 °C) | 0.0039 /°C |
| UK low-voltage supply | 230 V single-phase, 400 V three-phase, 50 Hz |

## Appendix C: Examination Technique for Circuit Problems

Over many years of marking scripts I have found that most lost marks are not lost through ignorance. They are lost through haste, untidiness and a failure to check. The following advice is unglamorous, but it is worth several grades.

**Read the whole question first.** Later parts often hint at the method expected in earlier ones. A question that asks you to "hence find" something is telling you to reuse a previous result.

**Redraw the circuit.** Copy it neatly, label every node, and mark every unknown current with an arrow. Many circuits become far simpler when redrawn: elements that looked tangled turn out to be in parallel, and a confusing bridge becomes an obvious ladder.

**Choose the method deliberately.** As a rough guide: count the essential nodes and the meshes. If there are fewer unknown node voltages than mesh currents, use nodal analysis, and vice versa. If you only need one quantity in a large circuit, consider Thévenin's theorem. If there are several independent sources and you need to understand the contribution of each, superposition is natural.

**Write the equations before substituting numbers.** This lets the examiner award method marks even if your arithmetic fails, and it makes your own errors far easier to find.

**Carry units.** An answer of "4.7" is worth less than "4.7 mA", and the habit of writing units catches kilohm-versus-ohm mistakes before they become disasters.

**Check.** Every circuit problem offers a cheap check: KCL at a node you did not use, KVL round a loop you did not use, a power balance, or a limiting case. Thirty seconds of checking is the best investment you can make in an examination.

**Present the answer clearly.** Underline or box it, give it to a sensible number of significant figures, and state the direction or polarity where that matters. "2.4 A" is incomplete if the question asked which way the current flows.

## About the Author

Marcus J. Thornton, PhD, is an electrical engineer and educator with a long career spanning industry, further education and university teaching. He has taught circuit theory, power systems and electronics to apprentices, undergraduates and practising engineers preparing for professional registration, and has set and marked examinations at every level from technician certificates to final-year degree papers.

His teaching is built on a simple conviction: that anyone willing to work steadily through well-chosen problems can master circuit analysis, and that the best help a teacher can give is a clear explanation followed by plenty of honest practice. This workbook is the distillation of the problem sheets, tutorial notes and examination questions he has developed over many years in the classroom and the laboratory.

When he is not writing problems, he can usually be found restoring old valve radios, an activity he recommends to any student who wants to see how much engineering can be packed into a wooden box.
