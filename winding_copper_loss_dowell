# =============================================================================
# Winding Loss Calculator using Dowell's Equation
# =============================================================================
#
# Description:
# This script calculates the total winding power loss (both DC and AC) for a
# multi-layer foil or rectangular wire winding in a magnetic component, such
# as an inductor or transformer. It is designed for windings where the magnetic
# field is predominantly parallel to the conductor layers.
#
# Methodology:
# 1.  **DC Loss:** Calculated using the standard formula for resistance based on
#     conductor geometry (height, width, Mean Length per Turn) and material
#     resistivity.
# 2.  **AC Loss (Proximity & Skin Effects):** Calculated using Dowell's
#     equation. This method models the increase in resistance due to high-
#     frequency eddy currents.
#     - The script first calculates the skin depth (δ) at the given switching
#       frequency.
#     - The penetration ratio (φ), which is the conductor height divided by the
#       skin depth, is determined.
#     - A unique Dowell's factor (Q) is computed for each layer 'm'. This factor
#       represents the ratio of that layer's AC resistance to its DC resistance.
#     - The AC power loss is then calculated for each layer using its Q factor
#       and the AC RMS current, and these losses are summed up.
#
# Assumptions:
# - The current waveform is triangular. The AC loss calculation is based on the
#   RMS value of the fundamental harmonic of this waveform.
# - The magnetic field is assumed to be uniform and parallel to the surface
#   of the conductors (a common 1D field assumption in transformer/inductor design).
# - End-turn effects on resistance are neglected.
#
# =============================================================================

import numpy as np

def compute_G1(phi):
    """Computes the G1 function for Dowell's equation."""
    numerator = np.sinh(2 * phi) + np.sin(2 * phi)
    denominator = np.cosh(2 * phi) - np.cos(2 * phi)
    return numerator / denominator if denominator != 0 else 0

def compute_G2(phi):
    """Computes the G2 function for Dowell's equation."""
    numerator = np.sinh(phi) * np.cos(phi) + np.cosh(phi) * np.sin(phi)
    denominator = np.cosh(2 * phi) - np.cos(2 * phi)
    return numerator / denominator if denominator != 0 else 0

def compute_Q(phi, m):
    """Computes the Dowell factor Q for a specific layer m."""
    G1 = compute_G1(phi)
    G2 = compute_G2(phi)
    return (2 * m**2 - 2 * m + 1) * G1 - 4 * m * (m - 1) * G2

# --- Input Parameters ---
h = 0.343e-3      # Conductor height (m)
W = 0.78e-2       # Conductor width (m)
MLT = 4.4e-2      # Mean Length per Turn (m)
n = 7             # Number of layers
rho = 2.3e-8      # Resistivity of conductor (Ohm-m)
fs = 300e3        # Switching frequency (Hz)
Ipk = 10          # Peak current of triangular wave (A)

# --- Calculations ---
skin_depth = np.sqrt(rho / (np.pi**2 * 4e-7 * fs))
phi = h / skin_depth

# DC Resistance Calculations
Rdc_total = n * rho * MLT / (h * W)
Rdc_layer = Rdc_total / n # DC resistance of a single layer

# Current Calculations
Idc = Ipk / 2
# RMS of the fundamental harmonic of a triangular wave
Iac_rms = (4 * Ipk / np.pi**2) / np.sqrt(2)

# Power Loss Calculations
Pdc_total = Rdc_total * (Idc**2)

Pac_total = 0
layer_results = [] # Store results for a summary table
for m in range(1, n + 1):
    Q_m = compute_Q(phi, m)
    Pm = Iac_rms**2 * Rdc_layer * Q_m
    Pac_total += Pm
    layer_results.append({"layer": m, "Q": Q_m, "loss_mW": Pm * 1000})

print("=" * 50)
print(" Winding Loss Analysis ".center(50, "="))
print("=" * 50)

print("\n--- Key Parameters ---")
print(f"Switching Frequency (fs): {fs/1e3:.1f} kHz")
print(f"Skin Depth (δ):           {skin_depth*1e6:.2f} µm")
print(f"Penetration Ratio (φ):    {phi:.3f}")

print("\n--- Resistance & Current ---")
print(f"Total DC Resistance:      {Rdc_total*1e3:.3f} mΩ")
print(f"DC Current (Idc):         {Idc:.2f} A")
print(f"AC RMS Current (Iac_rms): {Iac_rms:.3f} A")

print("\n--- Per-Layer AC Loss Breakdown ---")
print("-" * 52)
print(f"{'Layer (m)':<12} | {'Dowell Factor (Q)':<20} | {'AC Loss (mW)':<15}")
print("-" * 52)
for result in layer_results:
    print(f"{result['layer']:<12} | {result['Q']:<20.3f} | {result['loss_mW']:<15.2f}")
print("-" * 52)

print("\n--- Power Loss Summary ---")
# Note: Pdc_total is in Watts, so it's multiplied by 1000 for mW
print(f"Total DC Power Loss:      {Pdc_total * 1000:.5f} mW")
print(f"Total AC Power Loss:      {Pac_total * 1000:.5f} mW")
print("-" * 30)
# Note: Pac_total is already summed in Watts
print(f"TOTAL Winding Power Loss: {(Pdc_total + Pac_total) * 1000:.5f} mW ✨")
print("=" * 50)
