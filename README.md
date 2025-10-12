# Power-Electronics

Code and simulations related to power electronic courses for the Master of Science in Electrical and Computer Engineering program at the University of Colorado Boulder. The primary focus of these scripts is the analysis and design of high-frequency magnetic components.

---

## Scripts in this Repository

This repository contains the following Python scripts:

* **`magnetic_design.py`**
    * This script designs a high-frequency transformer for a **Full-Bridge Buck Converter**. It uses the **Core Geometrical Constant ($K_g$)** method to select a suitable magnetic core from a component library based on electrical specifications. The script calculates the required turns, wire gauges (AWG), and verifies the final copper and core losses.

* **`winding_loss_calculator.py`**
    * This script calculates the total winding power loss, including both DC and AC components, for a multi-layer rectangular conductor winding. It uses Dowell's equation to accurately model the increase in resistance due to high-frequency skin and proximity effects. The output provides a detailed breakdown of key parameters and losses per layer.

* **`winding_thickness_optimizer.py`**
    * This script extends the loss analysis to perform an optimization. It iteratively searches for the optimal conductor thickness (`h`) that minimizes the total combined power loss. This tool is useful for balancing the trade-off between DC conduction losses and AC eddy current losses.

---

## Methodology

The design and analysis in these scripts are based on several industry-standard methods for power magnetics:

1.  **Core Geometrical Constant ($K_g$) Method:** Used in `magnetic_design.py`, this method links the electrical requirements (voltage, power, etc.) and loss targets to a core's physical properties. It provides a systematic way to select the right core for a specific application.

2.  **Steinmetz Equation:** Used to estimate core losses due to the alternating magnetic flux. The general form is $P_{core} = K_{fe} \cdot f^{\alpha} \cdot (\Delta B)^{\beta}$, where the coefficients are specific to the core material.

3.  **Dowell's 1-D Analysis:** This method, used in the winding loss scripts, estimates AC resistance by modeling two primary high-frequency phenomena:
    * **Skin Effect:** The tendency of AC current to flow near the surface of a conductor. 
    * **Proximity Effect:** Eddy currents induced in a conductor by the magnetic field of adjacent conductors, which increases power loss.
=

---

## Usage

To use a script, modify the **input parameters** defined in the main section at the bottom of the file. These include physical dimensions (conductor height, width, MLT), material properties (resistivity), and electrical conditions (voltage, power, frequency). Running the script will print the design and analysis results directly to the console.
