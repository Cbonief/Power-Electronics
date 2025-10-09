# Power-Electronics

Code and simulations related to power electronic courses for the Master of Science in Electrical and Computer Engineering program at the University of Colorado Boulder. The primary focus of these scripts is the analysis and design of high-frequency magnetic components.

---

## Scripts in this Repository

This repository contains the following Python scripts:

* **`winding_loss_calculator.py`** (from first file)
    * This script calculates the total winding power loss, including both DC and AC components, for a multi-layer rectangular conductor winding. It uses Dowell's equation to accurately model the increase in resistance due to high-frequency skin and proximity effects. The output provides a detailed breakdown of key parameters and losses per layer.

* **`winding_thickness_optimizer.py`** (from second file)
    * This script extends the loss analysis to perform an optimization. It iteratively searches for the optimal conductor thickness (`h`) that minimizes the total combined power loss. This tool is useful for balancing the trade-off between DC conduction losses (which increase with thinner conductors) and AC eddy current losses (which increase with thicker conductors).

---

## Methodology

The calculations are based on **Dowell's one-dimensional analysis** for AC winding resistance. This industry-standard method is used to estimate the impact of two primary high-frequency phenomena in magnetic component windings:

1.  **Skin Effect:** The tendency of alternating current (AC) to become distributed within a conductor such that the current density is largest near the surface.
2.  **Proximity Effect:** The phenomenon where eddy currents are induced in a conductor by the magnetic field of adjacent conductors, resulting in a non-uniform current distribution and increased power loss.

The scripts assume a triangular current waveform and calculate AC losses based on its fundamental harmonic.

---

## Usage

To use a script, modify the input parameters defined in the "Example Usage" or main section at the bottom of the file. These include physical dimensions (conductor height, width, MLT), material properties (resistivity), and electrical conditions (frequency, peak current). Running the script will print the analysis or optimization results directly to the console.
