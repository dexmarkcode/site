# Appendix B: Useful Data, Constants and Conversions

The values below are those used in the worked examples and problems. Material properties vary with grade, temperature and supplier; treat them as typical values for estimation, not as design data.

## Physical constants

Table: **Table B.1** Physical constants.

| Quantity | Symbol | Value |
|:---|:---|:---|
| Acceleration due to gravity | *g* | 9.81 m/s^2^ |
| Universal gas constant | *R* | 8.314 J/(mol·K) |
| Boltzmann constant | *k* | 1.381 × 10^−23^ J/K (8.617 × 10^−5^ eV/K) |
| Faraday constant | *F* | 96 485 C/mol |
| Elementary charge | *e* | 1.602 × 10^−19^ C |
| Permeability of free space | *μ*~0~ | 4π × 10^−7^ H/m |
| Absolute zero | – | 0 K = −273.15 °C |

## Conversions

Table: **Table B.2** Common conversions.

| From | To | Multiply by |
|:---|:---|:---|
| km/h | m/s | 1/3.6 (0.2778) |
| mph | km/h | 1.609 |
| kWh | MJ | 3.6 |
| Wh/km | kWh/100 km | 0.1 |
| kWh/100 km | miles/kWh | 62.14 ÷ value |
| miles/kWh | km/kWh | 1.609 |
| rpm | rad/s | 2π/60 (0.1047) |
| hp (metric, PS) | kW | 0.7355 |
| hp (imperial) | kW | 0.7457 |
| lbf·ft | N·m | 1.356 |
| psi | kPa | 6.895 |
| Ah at nominal voltage *V* | Wh | *V* |
| Percentage gradient *G* | angle θ | θ = arctan(*G*/100) |

## Road-load data

Table: **Table B.3** Typical road-load parameters for passenger vehicles.

| Vehicle type | Test mass (kg) | *C*~rr~ | *C*~d~ | Frontal area (m^2^) | *C*~d~*A* (m^2^) |
|:---|:---|:---|:---|:---|:---|
| Small hatchback | 1 300–1 600 | 0.008–0.010 | 0.28–0.32 | 2.1–2.2 | 0.60–0.70 |
| Streamlined saloon | 1 800–2 200 | 0.007–0.009 | 0.21–0.25 | 2.2–2.3 | 0.46–0.57 |
| Mid-size crossover | 1 900–2 300 | 0.008–0.010 | 0.26–0.30 | 2.4–2.6 | 0.62–0.78 |
| Large SUV | 2 400–3 000 | 0.009–0.012 | 0.30–0.36 | 2.7–3.0 | 0.81–1.05 |
| Light van (3.5 t) | 2 500–3 500 | 0.009–0.012 | 0.33–0.40 | 3.8–4.5 | 1.25–1.80 |

Air density at sea level: 1.34 kg/m^3^ at −10 °C, 1.29 at 0 °C, 1.25 at 10 °C, 1.20 at 20 °C, 1.16 at 30 °C.

## Electrical and thermal properties of materials

Table: **Table B.4** Properties of conductors and common materials at about 20 °C.

| Material | Resistivity (Ω·m) | Temp. coeff. (1/K) | Density (kg/m^3^) | Specific heat (J/kg·K) | Thermal cond. (W/m·K) |
|:---|:---|:---|:---|:---|:---|
| Copper | 1.72 × 10^−8^ | 0.0039 | 8 960 | 385 | 400 |
| Aluminium | 2.82 × 10^−8^ | 0.0040 | 2 700 | 900 | 237 |
| Electrical steel (3 % Si) | ~4.8 × 10^−7^ | – | 7 650 | 460 | 25–30 |
| Sintered NdFeB magnet | ~1.5 × 10^−6^ | – | 7 500 | 440 | 7–9 |
| Aluminium nitride (ceramic) | insulator | – | 3 260 | 740 | 170–180 |
| Silicon nitride (ceramic) | insulator | – | 3 200 | 690 | 60–90 |
| Water-glycol 50/50 (at 20 °C) | – | – | 1 070 | 3 400 | 0.38 |
| Lithium-ion cell (average) | – | – | 2 200–2 700 | 900–1 100 | 1–30 (anisotropic) |

## Battery reference values

Table: **Table B.5** Indicative cell parameters used in this book.

| Parameter | NMC / graphite | LFP / graphite |
|:---|:---|:---|
| Nominal voltage | 3.6–3.7 V | 3.2–3.3 V |
| Voltage window | 2.8–4.2 V | 2.5–3.65 V |
| Cell energy density | 240–300 Wh/kg | 160–205 Wh/kg |
| Typical cycle life to 80 % | 1 500–3 000 cycles | 3 000–6 000 cycles |
| Preferred operating range | 15–35 °C | 15–35 °C |
| Approx. onset of thermal runaway | 150–200 °C | 200–250 °C |

## Formulae at a glance

- Road load: *F* = *C*~rr~*mg* cos θ + ½ρ*C*~d~*A v*^2^ + *mg* sin θ + δ*m* d*v*/d*t*
- Energy per km at constant speed on the level (kWh/100 km) = road-load force (N) ÷ 36
- Kinetic energy: *E* = ½δ*mv*^2^
- Three-phase power: *P* = √3 *V*~LL~ *I*~L~ cos φ
- Synchronous speed: *n*~s~ = 60*f*/*p*
- IPM torque: *T* = (3/2)*p*[ψ~m~*i*~q~ + (*L*~d~ − *L*~q~)*i*~d~*i*~q~]
- Rotor sizing: *T* = 2σ*V*~r~
- Copper loss: *P* = 3*I*~rms~^2^*R*; *R*~T~ = *R*~20~[1 + α(*T* − 20)]
- Iron loss (Steinmetz): *p* = *k*~h~*fB*^2^ + *k*~e~*f*^2^*B*^2^
- Pre-charge: *v*~C~ = *V*(1 − e^−*t*/*RC*^); energy in resistor = ½*CV*^2^
- Arrhenius ratio: *k*~2~/*k*~1~ = exp[(*E*~a~/*R*)(1/*T*~1~ − 1/*T*~2~)]
- Coolant flow: *ṁ* = *Q̇* / (*c*~p~Δ*T*)
- Boost converter: *V*~out~ = *V*~in~/(1 − *D*)
- Control pilot current: *I* = 0.6 × duty (%) for 10–85 %
- ASIL from S + E + C: 10 → D, 9 → C, 8 → B, 7 → A
