# ===================================================================================
# Winding Loss Optimization using Dowell's Equation
# ===================================================================================
#
# ## Purpose ##
# This script is designed to calculate the winding power loss in a high-frequency
# magnetic component (like an inductor or transformer) and find the optimal
# conductor thickness (`h`) that minimizes this total loss.
#
# ## Methodology ##
# The script balances the trade-off between two types of power loss:
#
# 1.  **DC Loss (Conduction Loss):** This is the basic resistive loss (P = I²R).
#     Thinner conductors have higher DC resistance, leading to higher DC loss.
#
# 2.  **AC Loss (Eddy Current Loss):** At high frequencies, changing magnetic
#     fields induce circulating currents (eddy currents) within the conductors.
#     These currents cause additional power loss. This phenomenon is composed of:
#     - **Skin Effect:** Current crowds to the surface of the conductor.
#     - **Proximity Effect:** Eddy currents are induced by the magnetic fields
#       of *adjacent* conductors.
#     Thicker conductors are more susceptible to these effects, leading to higher AC loss.
#
# This script uses **Dowell's Equation** to model the AC resistance. It then
# iteratively tests different conductor thicknesses (`h`) to find the "sweet spot"
# where the combined DC and AC losses are at their lowest point.
#
# ===================================================================================

import numpy as np

def compute_G1(phi):
    """
    Computes the G1 auxiliary function used in Dowell's equation.
    This is an intermediate calculation based on the penetration ratio (phi).
    
    Args:
        phi (float): The penetration ratio (conductor height / skin depth).
    
    Returns:
        float: The result of the G1 function.
    """
    # Numerically stable calculation
    denominator = np.cosh(2 * phi) - np.cos(2 * phi)
    if denominator == 0:
        return 0
    numerator = np.sinh(2 * phi) + np.sin(2 * phi)
    return numerator / denominator

def compute_G2(phi):
    """
    Computes the G2 auxiliary function used in Dowell's equation.
    This is another intermediate calculation based on the penetration ratio (phi).

    Args:
        phi (float): The penetration ratio (conductor height / skin depth).

    Returns:
        float: The result of the G2 function.
    """
    # Numerically stable calculation
    denominator = np.cosh(2 * phi) - np.cos(2 * phi)
    if denominator == 0:
        return 0
    numerator = np.sinh(phi) * np.cos(phi) + np.cosh(phi) * np.sin(phi)
    return numerator / denominator

def compute_Q(phi, m):
    """
    Computes the Dowell Factor (Q) for a specific layer 'm'.
    The Q factor is the ratio of AC resistance to DC resistance (Rac/Rdc) for that layer.

    Args:
        phi (float): The penetration ratio.
        m (int): The layer number, starting from 1 for the layer in the lowest MMF region.

    Returns:
        float: The Dowell factor Q for the given layer.
    """
    G1 = compute_G1(phi)
    G2 = compute_G2(phi)
    # Dowell's formula for the Q factor of layer 'm'
    return (2 * m**2 - 2 * m + 1) * G1 - 4 * m * (m - 1) * G2

def evaluate_loss(h, W, ada, MLT, n, rho, fs, Ipk):
    """
    Calculates the total DC and AC power loss for a given set of winding parameters.

    Args:
        h (float): Conductor height/thickness (m).
        W (float): Conductor width (m).
        ada (float): Porosity factor (not used in this version but kept for signature consistency).
        MLT (float): Mean Length per Turn (m).
        n (int): Number of layers.
        rho (float): Electrical resistivity of the conductor material (Ohm-m).
        fs (float): Switching frequency (Hz).
        Ipk (float): Peak of the triangular current waveform (A).

    Returns:
        tuple: A tuple containing (Pdc, Pac, phi).
    """
    # --- Step 1: Calculate Skin Depth and Penetration Ratio ---
    # Skin depth (δ) is how deep an AC current tends to flow in a conductor.
    skin_depth = np.sqrt(rho / (np.pi**2 * 4e-7 * fs))
    # Penetration ratio (φ) compares conductor thickness to skin depth. A high phi (>1) indicates severe AC effects.
    phi = h / skin_depth

    # --- Step 2: Calculate DC Resistance ---
    # Total DC resistance of all n layers combined.
    Rdc_total = n * rho * MLT / (h * W)
    # DC resistance of a single layer.
    Rdc = Rdc_total / n

    # --- Step 3: Calculate Current Components ---
    # For a triangular wave, the DC component is half the peak.
    Idc = Ipk / 2
    # RMS value of the *fundamental harmonic* of a triangular wave. This is a key assumption for AC loss calculation.
    Iac_rms = (4 * Ipk / np.pi**2) / np.sqrt(2)

    # --- Step 4: Calculate Power Losses ---
    # DC power loss for the entire winding.
    Pdc = Rdc_total * (Idc**2)

    # AC power loss is calculated layer by layer and summed.
    Pac = 0
    for m in range(1, n + 1):
        # Get the AC resistance factor for this specific layer.
        Qm = compute_Q(phi, m)
        # AC loss for this layer is I_ac^2 * R_ac, where R_ac = Rdc * Qm
        Pac += Iac_rms**2 * Rdc * Qm

    return Pdc, Pac, phi


def find_optimal_h(initial_h, W, ada, MLT, n, rho, fs, Ipk, steps=1000):
    """
    Finds the optimal conductor height 'h' that minimizes total winding loss.
    It iterates through a range of 'h' values and returns the parameters
    corresponding to the minimum total loss found.

    Args:
        initial_h (float): The starting/maximum conductor height to test (m).
        steps (int): The number of steps to iterate through for 'h'.

    Returns:
        tuple: A tuple containing (best_h, best_phi, best_Pdc, best_Pac, best_total_loss).
    """
    # Create a search space for 'h', from 10% of the initial value up to the initial value.
    # We test smaller values because AC losses decrease with thinner conductors.
    h_values = np.linspace(initial_h * 0.1, initial_h, steps)
    
    # Initialize variables to store the best results found so far.
    best_h = None
    best_total_loss = float("inf")  # Start with infinity to ensure the first result is always "better".
    best_phi = None
    best_Pdc = None
    best_Pac = None

    # Iterate through all candidate 'h' values.
    for h in h_values:
        # Calculate the losses for the current 'h'.
        Pdc, Pac, phi = evaluate_loss(h, W, ada, MLT, n, rho, fs, Ipk)
        total_loss = Pdc + Pac
        
        # If the current total loss is lower than the best one we've seen, update our records.
        if total_loss < best_total_loss:
            best_total_loss = total_loss
            best_h = h
            best_phi = phi
            best_Pdc = Pdc
            best_Pac = Pac

    return best_h, best_phi, best_Pdc, best_Pac, best_total_loss


# ===================================================================================
# Example Usage: Define Parameters and Run Optimization
# ===================================================================================

# --- Input Parameters ---
h = 0.343e-3     # Initial conductor height (m) - from a component like a 3F46 PQ32/30 core
W = 0.78e-2      # Conductor width (m)
ada = 1          # Porosity factor (e.g., for litz wire, not used here)
MLT = 4.4e-2     # Mean Length per Turn (m)
n = 7            # Number of winding layers
rho = 2.3e-8     # Resistivity of copper at operating temperature (~100°C) (Ohm-m)
fs = 300e3       # Switching frequency (Hz)
Ipk = 10         # Peak current of the triangular waveform (A)

# --- Run the Optimization ---
# Call the function to find the best conductor height and the associated losses.
opt_h, opt_phi, opt_Pdc, opt_Pac, opt_loss = find_optimal_h(h, W, ada, MLT, n, rho, fs, Ipk)

# --- Print the Results ---
print("--- Optimization Results ---")
print(f"Optimal Conductor Height (h): {opt_h * 1e3:.4f} mm")
print(f"Optimal Penetration Ratio (φ): {opt_phi:.4f}")
print("--- Power Loss at Optimal Point ---")
print(f"DC Power Loss (Pdc): {opt_Pdc:.4f} W")
print(f"AC Power Loss (Pac): {opt_Pac:.4f} W")
print(f"Total Minimized Loss (Pdc + Pac): {opt_loss:.4f} W ✨")
