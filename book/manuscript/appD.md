This appendix collects the key equations of the book in one place, chapter by chapter, for revision and quick reference.

## Part One: Foundations

::: {.table-wrap}
| Relationship | Equation | Chapter |
|:--|:--|:--:|
| Current | I = Q / t | 1 |
| Voltage | V = W / Q | 1 |
| Resistance of a conductor | R = ρL / A | 2 |
| Temperature effect | R~T~ = R~0~(1 + αΔT) | 2 |
| Conductance | G = 1 / R | 2 |
| Power | P = W / t = VI | 2 |
| Energy | W = Pt; 1 kWh = 3.6 MJ | 2 |
| Efficiency | η = P~out~ / P~in~ | 2 |
| Ohm's law | V = IR | 3 |
| Power in a resistor | P = I²R = V²/R | 3 |
| Real source | V = E − Ir | 3 |

: Table D.1 — Foundations.
:::

## Part Two: Laws and Basic Circuits

::: {.table-wrap}
| Relationship | Equation | Chapter |
|:--|:--|:--:|
| Meshes, branches and nodes | m = b − n + 1 | 4 |
| Double subscripts | V~AB~ = V~A~ − V~B~ | 4 |
| Passive sign convention | P = VI absorbed when I enters at + | 4 |
| Kirchhoff's current law | Σ I~in~ = Σ I~out~ | 5 |
| Kirchhoff's voltage law | Σ V = 0 round any loop | 5 |
| Series resistance | R~T~ = R~1~ + R~2~ + … | 6 |
| Parallel resistance | 1/R~T~ = 1/R~1~ + 1/R~2~ + … | 6 |
| Two in parallel | R~T~ = R~1~R~2~ / (R~1~ + R~2~) | 6 |
| Voltage divider | V~x~ = V~S~R~x~ / R~T~ | 6 |
| Current divider | I~1~ = I~T~R~2~ / (R~1~ + R~2~); I~x~ = I~T~G~x~ / G~T~ | 6 |

: Table D.2 — Laws and basic circuits.
:::

## Part Three: Simplifying Networks

::: {.table-wrap}
| Relationship | Equation | Chapter |
|:--|:--|:--:|
| Loaded divider | V~out~ = V~S~(R~2~ ∥ R~L~) / [R~1~ + (R~2~ ∥ R~L~)] | 8 |
| Ammeter shunt | R~sh~ = I~fs~R~m~ / (I − I~fs~) | 8 |
| Voltmeter multiplier | R~mult~ = V~fs~ / I~fs~ − R~m~ | 8 |
| Wheatstone bridge balance | R~1~R~4~ = R~2~R~3~ | 8 |
| Delta to star | R~a~ = R~ab~R~ca~ / (R~ab~ + R~bc~ + R~ca~) | 9 |
| Star to delta | R~ab~ = (R~a~R~b~ + R~b~R~c~ + R~c~R~a~) / R~c~ | 9 |
| Equal resistors | R~Y~ = R~Δ~ / 3 | 9 |

: Table D.3 — Simplifying networks.
:::

## Part Four: Systematic Methods

::: {.table-wrap}
| Relationship | Equation | Chapter |
|:--|:--|:--:|
| Branch current from node voltages | I~x→y~ = (V~x~ − V~y~) / R | 10 |
| Nodal equations | [G][V] = [I] | 10 |
| Shared mesh branch | I = I~1~ − I~2~ | 11 |
| Mesh equations | [R][I] = [V] | 11 |
| Supernode constraint | V~+~ − V~−~ = E | 12 |
| Supermesh constraint | difference of mesh currents = source current | 12 |
| Nodal unknowns | (n − 1) − (voltage sources) | 17 |
| Mesh unknowns | m − (current sources) | 17 |

: Table D.4 — Systematic methods.
:::

## Parts Five and Six: Theorems and Applications

::: {.table-wrap}
| Relationship | Equation | Chapter |
|:--|:--|:--:|
| Superposition | response = Σ responses to each independent source | 13 |
| Switching off sources | V source → short; I source → open; dependent sources stay | 13 |
| Thévenin | V~Th~ = V~oc~; R~Th~ = V~oc~ / I~sc~ | 14 |
| Load current | I~L~ = V~Th~ / (R~Th~ + R~L~) | 14 |
| Norton | I~N~ = I~sc~ = V~Th~ / R~Th~; R~N~ = R~Th~ | 15 |
| Source transformation | E in series with R ⟷ E/R in parallel with R | 15 |
| Millman | V = (Σ E~k~/R~k~) / (Σ 1/R~k~) | 15 |
| Maximum power transfer | R~L~ = R~Th~; P~max~ = V~Th~² / (4R~Th~) | 16 |
| Efficiency of transfer | η = R~L~ / (R~Th~ + R~L~) | 16 |
| RC time constant | τ = RC | 18 |

: Table D.5 — Theorems and applications.
:::
