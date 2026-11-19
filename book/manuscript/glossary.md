# Glossary

Active short circuit (ASC)
:   A safe state in which the inverter turns on all three upper or all three lower switches, shorting the motor terminals so that back-EMF cannot drive current into the DC link.

ASIL
:   Automotive Safety Integrity Level. A classification from A (lowest) to D (highest) under ISO 26262, set by the severity, exposure and controllability of a hazardous event.

Back-EMF
:   The voltage induced in a motor's windings by its own rotation, proportional to speed. It opposes the supply voltage and limits speed without field weakening.

Balancing (cell)
:   Equalising the state of charge of series-connected cells, either by bleeding charge from high cells (passive) or transferring it between cells (active).

Base speed
:   The motor speed above which the available voltage limits torque and the drive enters the constant-power region.

Battery disconnect unit (BDU)
:   The assembly inside a pack containing main contactors, pre-charge circuit, fuse and current sensor.

BEV
:   Battery electric vehicle: a vehicle powered solely by a rechargeable traction battery.

C-rate
:   Current expressed relative to cell capacity: 1C fully charges or discharges the cell in about one hour.

CCS
:   Combined Charging System. A connector family adding two DC pins to a Type 1 (CCS1) or Type 2 (CCS2) AC inlet.

Cell-to-pack (CTP)
:   A pack architecture in which cells are mounted directly in the pack structure without intermediate modules.

Clarke transformation
:   A mathematical transformation of three phase quantities into two components on fixed orthogonal axes (α and β).

Coefficient of performance (COP)
:   Heat delivered by a heat pump divided by the electrical energy it consumes.

Contactor
:   An electromechanical switch designed to make and break high DC currents in the high-voltage circuit.

Control pilot (CP)
:   The signal wire used in Mode 3 and DC charging to indicate connection state and permitted current, and to carry power-line communication.

Coulomb counting
:   Estimating state of charge by integrating measured current over time.

Dead time
:   A brief interval in which both switches of an inverter leg are off, preventing shoot-through.

DC link
:   The DC bus feeding an inverter or converter, supported by the DC-link capacitor.

Drive cycle
:   A standard speed-time profile used to measure vehicle energy consumption and emissions, such as WLTC or CLTC.

Dual active bridge (DAB)
:   An isolated, bidirectional DC-DC converter with active bridges on both sides of a transformer, controlled by phase shift.

Efficiency map
:   A plot of motor or drive efficiency across the torque–speed plane.

Equivalent circuit model (ECM)
:   A model of a cell as an OCV source with series resistance and RC elements.

Field-oriented control (FOC)
:   Control of an AC machine in a reference frame rotating with the rotor or flux, in which currents become steady quantities.

Field weakening
:   Applying negative d-axis current (or reducing excitation) above base speed so that the motor can operate within the available voltage.

FIT
:   Failures in time: one failure per 10^9^ device-hours.

Freeze frame
:   A snapshot of key variables stored with a diagnostic trouble code.

FTTI
:   Fault tolerant time interval: the time between a fault and a possible hazardous event, within which a safety mechanism must act.

GaN
:   Gallium nitride, a wide-bandgap semiconductor used for very fast switching devices.

Hairpin winding
:   A stator winding made of rectangular copper bars bent into U shapes, giving high copper fill.

Heat pump
:   A refrigeration circuit run to move heat from outside air or waste heat sources into the cabin or battery.

HPPC
:   Hybrid pulse power characterisation, a pulse test used to measure cell resistance and power capability.

HVIL
:   High-voltage interlock loop: a low-voltage signal loop through high-voltage connectors that opens the contactors if any connector is disconnected.

IGBT
:   Insulated-gate bipolar transistor, a high-voltage power switch using conductivity modulation.

Integration efficiency
:   The ratio of pack-level to cell-level energy density (gravimetric or volumetric).

Intercalation
:   The reversible insertion of lithium ions into the crystal structure of an electrode material.

IPM
:   Interior permanent-magnet machine, with magnets buried inside the rotor, producing both magnet and reluctance torque.

Isolation monitoring
:   Continuous measurement of the insulation resistance between the high-voltage system and the vehicle chassis.

Lithium plating
:   Deposition of metallic lithium on the anode surface instead of intercalation, typically during fast or cold charging.

LFP
:   Lithium iron phosphate, a safe, long-lived, lower-cost cathode material with a flat voltage curve.

LLC converter
:   A resonant isolated DC-DC converter regulated by switching frequency.

MCS
:   Megawatt Charging System, a DC charging standard for heavy vehicles.

MTPA
:   Maximum torque per ampere: choosing d- and q-axis currents to produce each torque with the minimum current magnitude.

NMC
:   Lithium nickel manganese cobalt oxide, a layered cathode family with high energy density.

OCV
:   Open-circuit voltage: the terminal voltage of a cell at rest, a function mainly of state of charge.

On-board charger (OBC)
:   The vehicle's AC-to-DC converter for charging from AC supplies.

Park transformation
:   A transformation from stationary α–β axes to the d–q axes rotating with the rotor.

Partial discharge
:   Small electrical discharges in voids or air gaps within insulation, which erode it over time.

PFC
:   Power factor correction: a converter stage that draws sinusoidal current in phase with the supply voltage.

PHEV
:   Plug-in hybrid electric vehicle, with an engine and a battery that can be charged from the grid.

Plug & Charge
:   Automatic authorisation and billing for charging using digital certificates under ISO 15118.

Pre-charge
:   Charging the DC-link capacitors through a resistor before closing the main contactors.

Pyrofuse
:   A pyrotechnically triggered disconnect that cuts a busbar within milliseconds.

Reluctance torque
:   Torque produced by a rotor's tendency to align its lowest-reluctance path with the stator field.

Resolver
:   A rotary transformer sensor that measures rotor angle.

SEI
:   Solid electrolyte interphase: a passivating film on the anode that permits ion transport but blocks electrons.

Shear stress (air-gap)
:   Tangential magnetic force per unit area acting at the air gap of a motor; torque equals twice the shear stress times rotor volume.

SiC
:   Silicon carbide, a wide-bandgap semiconductor allowing fast, low-loss switching at 1 200 V and above.

Slip
:   In an induction motor, the fractional difference between synchronous speed and rotor speed.

SLAC
:   Signal Level Attenuation Characterisation, the process by which a vehicle and charger find each other over power-line communication.

SoC
:   State of charge: the fraction of usable charge remaining in a cell or battery.

SoH
:   State of health: a measure of ageing, usually present capacity relative to new, or resistance increase.

SOTIF
:   Safety of the intended functionality (ISO 21448): hazards from functional insufficiencies rather than faults.

SVPWM
:   Space-vector pulse-width modulation, which uses the inverter's switching-state vectors to maximise usable DC-link voltage.

Thermal runaway
:   A self-sustaining chain of exothermic reactions in a cell leading to very high temperatures and venting.

Uncontrolled generator mode
:   Operation in which a motor's back-EMF exceeds the DC-link voltage and drives current through the inverter's diodes.

V2G, V2H, V2L
:   Vehicle-to-grid, vehicle-to-home and vehicle-to-load: supplying power from the vehicle's battery to the grid, a building or appliances.

WLTP
:   Worldwide harmonised Light vehicles Test Procedure, the laboratory test used for consumption and range in many markets.

Zero-voltage switching (ZVS)
:   Turning a switch on when the voltage across it has already fallen to zero, eliminating turn-on loss.
