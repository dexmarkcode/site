## A.1 Quantities, Symbols and Units

::: {.table-wrap}
| Quantity | Symbol | SI unit | Unit symbol | Defined in |
|:--|:--:|:--|:--:|:--|
| Charge | Q | coulomb | C | Chapter 1 |
| Current | I | ampere | A | Chapter 1 |
| Voltage (potential difference), EMF | V, E | volt | V | Chapter 1 |
| Energy, work | W | joule | J | Chapter 1 |
| Time | t | second | s | Chapter 1 |
| Resistance | R | ohm | Ω | Chapters 2–3 |
| Conductance | G | siemens | S | Chapter 2 |
| Resistivity | ρ | ohm metre | Ω m | Chapter 2 |
| Temperature coefficient | α | per degree Celsius | /°C | Chapter 2 |
| Power | P | watt | W | Chapter 2 |
| Efficiency | η | (ratio or %) | — | Chapter 2 |
| Capacitance | C | farad | F | Chapter 18 |
| Time constant | τ | second | s | Chapter 18 |
| Frequency | f | hertz | Hz | Chapter 1 |

: Table A.1 — Electrical quantities used in this book.
:::

Useful conversions:

- 1 kWh = 3.6 × 10^6^ J = 3.6 MJ
- 1 A h = 3600 C; 1 mA h = 3.6 C
- 1 W h = 3600 J
- 1 mm² = 10^−6^ m²
- charge on one electron, e = 1.602 × 10^−19^ C

## A.2 SI Prefixes

::: {.table-wrap}
| Prefix | Symbol | Multiplier | Prefix | Symbol | Multiplier |
|:--|:--:|:--|:--|:--:|:--|
| tera | T | 10^12^ | milli | m | 10^−3^ |
| giga | G | 10^9^ | micro | µ | 10^−6^ |
| mega | M | 10^6^ | nano | n | 10^−9^ |
| kilo | k | 10^3^ | pico | p | 10^−12^ |

: Table A.2 — SI prefixes in engineering notation.
:::

Remember that the case matters: m (milli) is 10^−3^, while M (mega) is 10^6^.

## A.3 The Resistor Colour Code

Four-band resistors carry two significant-figure bands, a multiplier band and a tolerance band. Five-band (precision) resistors carry three significant-figure bands, a multiplier and a tolerance. Read from the end with the bands closest together; the tolerance band is usually set slightly apart.

::: {.table-wrap}
| Colour | Digit | Multiplier | Tolerance |
|:--|:--:|:--|:--|
| Black | 0 | × 1 | — |
| Brown | 1 | × 10 | ± 1 % |
| Red | 2 | × 100 | ± 2 % |
| Orange | 3 | × 1 k | — |
| Yellow | 4 | × 10 k | — |
| Green | 5 | × 100 k | ± 0.5 % |
| Blue | 6 | × 1 M | ± 0.25 % |
| Violet | 7 | × 10 M | ± 0.1 % |
| Grey | 8 | — | ± 0.05 % |
| White | 9 | — | — |
| Gold | — | × 0.1 | ± 5 % |
| Silver | — | × 0.01 | ± 10 % |

: Table A.3 — The resistor colour code.
:::

A traditional memory aid for the order of the colours (black, brown, red, orange, yellow, green, blue, violet, grey, white) is "**B**ad **B**eer **R**ots **O**ur **Y**oung **G**uts, **B**ut **V**odka **G**oes **W**ell". You may prefer to invent your own.

**Examples.** Brown–black–red–gold: 1, 0, × 100, ± 5 % = 1000 Ω = 1 kΩ ± 5 %. Yellow–violet–orange–gold: 4, 7, × 1000 = 47 kΩ ± 5 %. Brown–black–black–red–brown (five-band): 1, 0, 0, × 100 = 10 kΩ ± 1 %.

### Surface-mount codes

Small surface-mount resistors often use a three- or four-digit code: the last digit is the number of zeros. So "472" is 4700 Ω = 4.7 kΩ, and "1002" is 10 000 Ω = 10 kΩ. The letter R marks a decimal point: "4R7" is 4.7 Ω.

## A.4 Preferred Values

::: {.table-wrap}
| Series | Tolerance | Values in each decade |
|:--|:--|:--|
| E6 | ± 20 % | 1.0, 1.5, 2.2, 3.3, 4.7, 6.8 |
| E12 | ± 10 % | 1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2 |
| E24 | ± 5 % | 1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1 |

: Table A.4 — The E6, E12 and E24 preferred-value series. Each value is available multiplied by 1, 10, 100, 1000 and so on.
:::

## A.5 Greek Letters Used in This Book

::: {.table-wrap}
| Letter | Name | Use in this book |
|:--:|:--|:--|
| Ω | omega (capital) | unit of resistance, the ohm |
| ρ | rho | resistivity |
| α | alpha | temperature coefficient of resistance |
| η | eta | efficiency |
| Δ | delta (capital) | a change in a quantity; the delta connection; a determinant |
| Σ | sigma (capital) | "the sum of" |
| µ | mu | prefix micro (10^−6^); voltage gain of a VCVS |
| β | beta | current gain of a CCCS |
| τ | tau | time constant |
| π | pi | 3.14159…; the π network |

: Table A.5 — Greek letters.
:::
