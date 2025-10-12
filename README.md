# Power-Electronics Design and Analysis

Code and simulations for the Master of Science in Electrical and Computer Engineering program at the University of Colorado Boulder. This repository contains Python scripts for designing high-frequency magnetic components and MATLAB code for analyzing the control loops of switched-mode power converters.

---

## Scripts in this Repository

The projects are divided into two main categories: high-frequency magnetics design and converter control simulation.

### 1. High-Frequency Magnetics Design (Python)

* **`magnetic_design.py`**
    * Designs a high-frequency transformer for a Full-Bridge Buck Converter using the **Core Geometrical Constant ($K_g$)** method. It selects a suitable core from a library, calculates turns and wire gauges (AWG), and verifies copper and core losses.

* **`winding_loss_calculator.py`**
    * Calculates the total winding power loss (DC and AC) for multi-layer rectangular conductors. It uses Dowell's equation to model high-frequency skin and proximity effects.

* **`winding_thickness_optimizer.py`**
    * Performs an optimization to find the conductor thickness (`h`) that minimizes the total combined DC conduction and AC eddy current losses.

### 2. Converter Control and Simulation (MATLAB)

* **`buck_converter_analysis.m`**
    * Analyzes the frequency response of a synchronous buck converter. The script derives the plant's duty-cycle-to-output-voltage transfer function $G_{vd}(s)$, models a Type II compensator $G_c(s)$, and evaluates system stability and performance by analyzing the total loop gain $T(s)$ and the closed-loop output impedance $Z_o$.

---

## Methodology

The design and analysis scripts are based on several industry-standard methods.

### Magnetics

1.  **Core Geometrical Constant ($K_g$) Method**: Used in `magnetic_design.py`, this technique links electrical requirements (voltage, power) and loss targets to a core's physical properties, providing a systematic way to select the right core for an application.

2.  **Steinmetz Equation**: This model is used to estimate core losses due to the alternating magnetic flux. The general form is $P_{core} = K_{fe} \cdot (\Delta B)^{\beta}$, where the coefficients are specific to the core material.

3.  **Dowell's 1-D Analysis**: This method estimates AC winding resistance by modeling two primary high-frequency phenomena which cause current to flow non-uniformly through a conductor. 
    * **Skin Effect**: The tendency of AC current to concentrate near the surface of a conductor.
    * **Proximity Effect**: Eddy currents induced in a conductor by the magnetic fields of adjacent conductors, which further increases power loss.

### Control Systems


1.  **Small-Signal Perturbation**: The plant transfer function, $G_{vd}(s)$, is derived using small-signal perturbation to model the dynamic behavior of the buck converter's L-C filter around its DC operating point.

2.  **Frequency Domain Analysis**: A Type II compensator is designed with specific pole-zero placement to shape the loop gain. The goal is to ensure adequate phase margin for stability and high bandwidth for a fast transient response. 

3.  **Output Impedance ($Z_o$)**: The closed-loop output impedance is analyzed to predict the output voltage deviation in response to dynamic load changes. A lower output impedance peak indicates better load transient performance. The relationship is given by: $Z_o(s) = \frac{Z_{out}(s)}{1 + T(s)}$, where $Z_{out}$ is the open-loop impedance and $T(s)$ is the loop gain.

---

## Requirements

* **Python 3.x**
    * `numpy` library
* **MATLAB**
    * Control System Toolbox
