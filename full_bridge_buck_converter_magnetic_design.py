# =============================================================================
# Magnetic Component Design for Full Bridge Buck Converter using the Geometrical Constant (Kg) Method
# =============================================================================
#
# Author: Carlos Franco (for CU Boulder Masters Project)
# Date: October 12, 2025
#
# Description:
# This script performs the preliminary design of a magnetic component (e.g., a
# transformer for a DC-DC converter) using the core geometrical constant (Kg)
# methodology. This approach links the electrical requirements of the application
# to the physical properties of the magnetic core and windings.
#
# Methodology:
# 1.  **Define Specifications:** Input voltage, output voltage, power, switching
#     frequency, and other key parameters are defined.
# 2.  **Calculate Electrical Stress:** The script calculates the RMS currents for
#     the primary and secondary windings and the volt-second product (lambda)
#     based on the converter topology.
# 3.  **Determine Required Core Geometry (Kfge_calc):** A required core
#     geometrical constant is calculated. This value encapsulates the core's
#     ability to handle the required power and is derived from the electrical
#     specifications and loss targets.
# 4.  **Core Selection:** The script selects the smallest suitable core from a
#     pre-defined table (`core_table`) that meets or exceeds the calculated
#     geometrical constant.
# 5.  **Calculate Flux Density and Turns:** Using the selected core's parameters,
#     the script calculates the peak AC flux density swing (deltaB) and the
#     required number of turns for the primary and secondary windings.
# 6.  **Winding Design:** The available winding area is allocated to the primary
#     and secondary windings. The script then calculates the required wire area
#     for each and selects the nearest appropriate American Wire Gauge (AWG)
#     from the `awg_table`.
# 7.  **Loss Verification:** Finally, the script calculates the actual copper
#     (Pcu) and core (Pfe) losses based on the selected core, turns, and wire
#     gauges to verify that the design meets the initial constraints.
#
# Assumptions:
# - Core loss is modeled using the Steinmetz equation (Pfe = Kfe * B^Beta).
# - Skin and proximity effects in the windings are not explicitly modeled in this
#   initial design stage but are implicitly managed by aiming for a low Pcu.
#
# =============================================================================

import numpy as np

# --- Data Tables ---

# Wire gauge table containing properties for different AWG sizes.
# This data is essential for selecting the physical wire for the windings.
awg_table = [
    {"AWG": "0000", "area_cm2": 1072.3e-3, "resistance_uohm_per_cm": 1.608, "diameter_cm": 1.168},
    {"AWG": "000", "area_cm2": 850.3e-3, "resistance_uohm_per_cm": 2.027, "diameter_cm": 1.040},
    {"AWG": "00", "area_cm2": 674.2e-3, "resistance_uohm_per_cm": 2.557, "diameter_cm": 0.927},
    {"AWG": "0", "area_cm2": 534.8e-3, "resistance_uohm_per_cm": 3.224, "diameter_cm": 0.825},
    {"AWG": "1", "area_cm2": 424.1e-3, "resistance_uohm_per_cm": 4.065, "diameter_cm": 0.735},
    {"AWG": "2", "area_cm2": 336.3e-3, "resistance_uohm_per_cm": 5.128, "diameter_cm": 0.654},
    {"AWG": "3", "area_cm2": 266.7e-3, "resistance_uohm_per_cm": 6.463, "diameter_cm": 0.583},
    {"AWG": "4", "area_cm2": 211.5e-3, "resistance_uohm_per_cm": 8.153, "diameter_cm": 0.519},
    {"AWG": "5", "area_cm2": 167.7e-3, "resistance_uohm_per_cm": 10.28, "diameter_cm": 0.462},
    {"AWG": "6", "area_cm2": 133.0e-3, "resistance_uohm_per_cm": 13.0, "diameter_cm": 0.411},
    {"AWG": "7", "area_cm2": 105.5e-3, "resistance_uohm_per_cm": 16.3, "diameter_cm": 0.366},
    {"AWG": "8", "area_cm2": 83.67e-3, "resistance_uohm_per_cm": 20.6, "diameter_cm": 0.326},
    {"AWG": "9", "area_cm2": 66.32e-3, "resistance_uohm_per_cm": 26.0, "diameter_cm": 0.291},
    {"AWG": "10", "area_cm2": 52.41e-3, "resistance_uohm_per_cm": 32.9, "diameter_cm": 0.267},
    {"AWG": "11", "area_cm2": 41.60e-3, "resistance_uohm_per_cm": 41.37, "diameter_cm": 0.238},
    {"AWG": "12", "area_cm2": 33.08e-3, "resistance_uohm_per_cm": 52.09, "diameter_cm": 0.213},
    {"AWG": "13", "area_cm2": 26.26e-3, "resistance_uohm_per_cm": 69.64, "diameter_cm": 0.190},
    {"AWG": "14", "area_cm2": 20.02e-3, "resistance_uohm_per_cm": 82.80, "diameter_cm": 0.171},
    {"AWG": "15", "area_cm2": 16.51e-3, "resistance_uohm_per_cm": 104.3, "diameter_cm": 0.153},
    {"AWG": "16", "area_cm2": 13.07e-3, "resistance_uohm_per_cm": 131.8, "diameter_cm": 0.137},
    {"AWG": "17", "area_cm2": 10.39e-3, "resistance_uohm_per_cm": 165.8, "diameter_cm": 0.122},
    {"AWG": "18", "area_cm2": 8.228e-3, "resistance_uohm_per_cm": 209.5, "diameter_cm": 0.109},
    {"AWG": "19", "area_cm2": 6.531e-3, "resistance_uohm_per_cm": 263.9, "diameter_cm": 0.0948},
    {"AWG": "20", "area_cm2": 5.188e-3, "resistance_uohm_per_cm": 332.3, "diameter_cm": 0.0874},
    {"AWG": "21", "area_cm2": 4.116e-3, "resistance_uohm_per_cm": 418.9, "diameter_cm": 0.0785},
    {"AWG": "22", "area_cm2": 3.243e-3, "resistance_uohm_per_cm": 531.4, "diameter_cm": 0.0701},
    {"AWG": "23", "area_cm2": 2.508e-3, "resistance_uohm_per_cm": 666.0, "diameter_cm": 0.0632},
    {"AWG": "24", "area_cm2": 2.047e-3, "resistance_uohm_per_cm": 842.1, "diameter_cm": 0.0566},
    {"AWG": "25", "area_cm2": 1.623e-3, "resistance_uohm_per_cm": 1062.0, "diameter_cm": 0.0505},
    {"AWG": "26", "area_cm2": 1.280e-3, "resistance_uohm_per_cm": 1345.0, "diameter_cm": 0.0452},
    {"AWG": "27", "area_cm2": 1.021e-3, "resistance_uohm_per_cm": 1687.6, "diameter_cm": 0.0409},
    {"AWG": "28", "area_cm2": 0.8046e-3, "resistance_uohm_per_cm": 2142.7, "diameter_cm": 0.0366},
    {"AWG": "29", "area_cm2": 0.6470e-3, "resistance_uohm_per_cm": 2664.3, "diameter_cm": 0.0330},
    {"AWG": "30", "area_cm2": 0.5067e-3, "resistance_uohm_per_cm": 3402.2, "diameter_cm": 0.0294},
    {"AWG": "31", "area_cm2": 0.4013e-3, "resistance_uohm_per_cm": 4294.6, "diameter_cm": 0.0267},
    {"AWG": "32", "area_cm2": 0.3242e-3, "resistance_uohm_per_cm": 5314.9, "diameter_cm": 0.0241},
    {"AWG": "33", "area_cm2": 0.2554e-3, "resistance_uohm_per_cm": 6748.6, "diameter_cm": 0.0236},
    {"AWG": "34", "area_cm2": 0.2011e-3, "resistance_uohm_per_cm": 8572.8, "diameter_cm": 0.0191},
    {"AWG": "35", "area_cm2": 0.1589e-3, "resistance_uohm_per_cm": 10849, "diameter_cm": 0.0170},
    {"AWG": "36", "area_cm2": 0.1266e-3, "resistance_uohm_per_cm": 13608, "diameter_cm": 0.0152},
    {"AWG": "37", "area_cm2": 0.1026e-3, "resistance_uohm_per_cm": 16801, "diameter_cm": 0.0140},
    {"AWG": "38", "area_cm2": 0.08107e-3, "resistance_uohm_per_cm": 21266, "diameter_cm": 0.0124},
    {"AWG": "39", "area_cm2": 0.06207e-3, "resistance_uohm_per_cm": 27775, "diameter_cm": 0.0109},
    {"AWG": "40", "area_cm2": 0.04869e-3, "resistance_uohm_per_cm": 35400, "diameter_cm": 0.0096},
    {"AWG": "41", "area_cm2": 0.03972e-3, "resistance_uohm_per_cm": 43405, "diameter_cm": 0.00863},
    {"AWG": "42", "area_cm2": 0.03166e-3, "resistance_uohm_per_cm": 54429, "diameter_cm": 0.00762},
    {"AWG": "43", "area_cm2": 0.02452e-3, "resistance_uohm_per_cm": 70308, "diameter_cm": 0.00685},
    {"AWG": "44", "area_cm2": 0.0202e-3, "resistance_uohm_per_cm": 85072, "diameter_cm": 0.00635}
]

# Core table with geometric and thermal properties for various standard core sizes.
core_table = [
    {
        "type": "EC35",
        "kg_cm5": 9.9e-3,       # Core geometrical constant [cm^5]
        "area_core": 0.843,     # Effective core cross-sectional area (Ac) [cm^2]
        "area_winding": 0.975,  # Available winding area (Wa) [cm^2]
        "length_path": 5.30,    # Effective magnetic path length (lm) [cm]
        "length_mlt": 18.5,     # Mean Length per Turn (MLT) [cm]
    },
    {
        "type": "EC41",
        "kg_cm5": 19.5e-3,
        "area_core": 1.21,
        "area_winding": 1.35,
        "length_path": 5.30,
        "length_mlt": 16.5,
    },
    {
        "type": "EC52",
        "kg_cm5": 31.7e-3,
        "area_core": 1.80,
        "area_winding": 2.12,
        "length_path":  10.5,
        "length_mlt": 7.50,
    },
    {
        "type": "EC70",
        "kg_cm5": 56.2e-3,
        "area_core": 2.79,
        "area_winding": 4.71,
        "length_path": 12.9,
        "length_mlt": 7.5,
    }
]

# --- Helper Functions ---

# Selects the largest wire from the awg_table that fits within the required area.
def get_awg_for_area(area_cm2):
    # Filter for all wires that are smaller than or equal to the required area.
    candidates = [wire for wire in awg_table if wire["area_cm2"] <= area_cm2]
    if not candidates:
        return None # No suitable wire found.
    # From the candidates, select the one with the largest area to minimize resistance.
    best_wire = max(candidates, key=lambda wire: wire["area_cm2"])
    return best_wire

# Selects the smallest core from the core_table that meets the calculated Kg value.
def get_core_for_kfe(kfe):
    # Filter for all cores with a geometric constant greater than or equal to the requirement.
    candidates = [core for core in core_table if core["kg_cm5"] >= kfe]
    if not candidates:
        return None # No suitable core found.
    # From the candidates, select the one with the smallest Kg to optimize for size and cost.
    best_core = min(candidates, key=lambda core: core["kg_cm5"])
    return best_core

# --- Input Parameters and Specifications ---
Vi = 400.0      # Input voltage [V]
Vo = 48.0       # Output voltage [V]
Po = 750.0      # Output power [W]
Io = Po/Vo      # Output current [A]
Ro = Vo/Io      # Equivalent load resistance [Ohms]
n = 1.0/6.0     # Transformer turns ratio (N_secondary / N_primary)
fs = 200.0*1e3  # Switching frequency [Hz]
p = 2.3*1e-6    # Resistivity of copper (rho) [ohm-cm]
Pcu = 2.0       # Target total copper loss [W]
Ku = 0.3        # Winding fill factor (ratio of copper area to total winding area)
Beta = 2.70     # Steinmetz exponent for the core material (e.g., for ferrite 3F3)
uo = 4e-7*np.pi # Permeability of free space [H/m]
Kfe = 10        # Steinmetz coefficient for the core material

# --- Core Design Calculations ---

# Calculate duty cycle for the 
D = Vo/(n*Vi)

# Calculate RMS currents for primary and secondary windings
Ip_rms = n*(Po/Vo)*np.sqrt(D)
Is_rms = np.sqrt(0.5)*np.sqrt(Io**2*(D)+2*(Io/2)**2*(1-D)) # Assuming two secondary windings
Itot_rms = Ip_rms + n*Is_rms + n*Is_rms # Weighted total RMS current for loss calculation

# Calculate the Volt-second product (Lambda) applied to the magnetizing inductance
lambd = Vi*D/(fs)

# Calculate the required core geometrical constant (Kg)
# This formula combines electrical specs and loss targets into a single parameter
# that defines the required physical size and shape of the core.
Kfge_calc = 1e8*(p*lambd**2*Itot_rms**2*(Kfe**(2/Beta)))/(4*Ku*Pcu**((Beta+2)/Beta))
print(f"\\Kfe_calculated: {Kfge_calc:.6f} cm^5")

# --- Component Selection and Detailed Design ---

# Select the best core based on the calculated Kg value
core = get_core_for_kfe(Kfge_calc)
MLT = core['length_mlt']     # Mean Length per Turn [cm]
Wa = core['area_winding']    # Winding Area [cm^2]
Ac = core['area_core']       # Core Area [cm^2]
lm = core['length_path']     # Magnetic Path Length [cm]

# Calculate the peak AC flux density swing (deltaB) in Tesla
# This is derived by relating copper and core loss equations to the core geometry.
term1 = p*lambd**2*Itot_rms**2/(2*Ku)
term2 = MLT/(Wa*lm*Ac**3)
term3 = 1/(Beta*Kfe)
deltaB = np.power((1e8*term1*term2*term3),(1/(Beta+2)))
print(f"Calculated Flux Density (deltaB): {deltaB:.4f} T")

# Set the number of turns for primary and secondary.
# NOTE: In a real design, these would be calculated from Faraday's law:
# n1 = np.round(lambd*10**4/(2*deltaB*Ac))
# n2 = np.round(n1*n)
# For this example, specific turn counts are chosen to meet an exact ratio.
n1= 30
n2=5

# --- Winding Design ---

# Allocate proportions of the winding area to primary and secondary windings
a1 = Ip_rms/Itot_rms
a21 = (n2/n1)*(Is_rms/Itot_rms)
a22 = (n2/n1)*(Is_rms/Itot_rms)

# Calculate the required wire cross-sectional area for each winding
Aw1_calc = a1*Ku*Wa/n1
Aw2_calc = a21*Ku*Wa/n2

# Select the best AWG wire gauge for each winding
WG1 = get_awg_for_area(Aw1_calc)
WG2 = get_awg_for_area(Aw2_calc)

# --- Loss Verification ---

# Recalculate the copper loss using the selected wire gauges
Pcu_p = Ip_rms**2 * (MLT*n1*p/(WG1["area_cm2"]))
Pcu_s = Is_rms**2 * (MLT*n2*p/(WG2["area_cm2"]))
Pcu_calc = Pcu_p + 2*Pcu_s # Total copper loss (assuming two secondaries)

# Recalculate the core loss using the Steinmetz equation
Pfe = Kfe*deltaB**Beta

# --- Output Results ---
print(f"\n--- Design Results for Core: {core['type']} ---")

print(f"\nPrimary RMS current (Ip_rms): {Ip_rms:.4f} A")
print(f"Secondary RMS current (Is_rms): {Is_rms:.4f} A")
print(f"Total RMS current for copper loss (Itot_rms): {Itot_rms:.4f} A")

print(f"\nNumber of turns (Primary): {n1:.0f}")
print(f"Number of turns (Secondary): {n2:.0f}")

print(f"\nProportion of area for Primary (a1): {a1:.4f}")
print(f"Proportion of area for Secondary (a2): {a21:.4f}")

print(f"\nRequired wire area for Primary (Aw1): {Aw1_calc*100:.4f} mm²")
print(f"Required wire area for Secondary (Aw2): {Aw2_calc*100:.4f} mm²")

if WG1:
    print(f"Selected AWG for Primary: AWG{WG1['AWG']} ({WG1['area_cm2']*100:.4f} mm²)")
else:
    print("No suitable AWG found for primary.")

if WG2:
    print(f"Selected AWG for Secondary: AWG{WG2['AWG']} ({WG2['area_cm2']*100:.4f} mm²)")
else:
    print("No suitable AWG found for secondary.")

print(f"\n--- Loss Analysis ---")
print(f"Copper loss (Primary winding): {Pcu_p:.4f} W")
print(f"Copper loss (Secondary winding): {Pcu_s:.4f} W")
print(f"Total Copper Loss (Pcu_calc): {Pcu_calc:.4f} W")
print(f"Total Core Loss (Pfe): {Pfe:.4f} W")
print(f"Total Estimated Loss: {Pcu_calc + Pfe:.4f} W")
print("\n----------------------")
