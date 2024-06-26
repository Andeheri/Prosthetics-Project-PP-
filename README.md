# Simulation of the Hodkin-Huxley model

The project is based on the following articles:

* [Hodkin-Huxley model](https://en.wikipedia.org/wiki/Hodgkin%E2%80%93Huxley_model)

    - [Original article](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1392413/)

## Introduction

### Lipid Bilayer
Each cell in the body is incased in a thin polar membrane called the [*Lipid bilayer*](https://en.wikipedia.org/wiki/Lipid_bilayer). In the Hodkin-Huxley model, this is modeled as the capacitance: 
$$C_m [\text{F} / m^2]$$
The equation for the current through the lipid bilayer is given by: 
$$
I_m = C_m \frac{d V_m}{dt} \quad \text{(m denotes 'membrane')}
$$

### Voltage-gated ion channels
In excitable cells (such as in nervonal and muscle tissue) you crucially find [*Voltage-gated ion channels*](https://en.wikipedia.org/wiki/Voltage-gated_ion_channel). These make it possible for rapid and co-ordinated [*depolarization*](https://en.wikipedia.org/wiki/Depolarization). Depolarization is when there is a shift in the electric charge distrubution within a cell, where the inside becomes more positively charged compared to the outside. This is illustrated in the following image. 
![Image of depolarization](images/depolarization.jpg)

The voltage-gated ion channels are ion-specific, s.t. it only lets certain ions pass through, like ${\text{Na}}^+$, ${\text{K}}^+$, ${\text{Ca}}^{2+}$ and ${\text{Cl}}^-$. Whenever the potential difference over the lipid bilayer is high enough, the protein gets distorted the point where the gate opens, and ions flow through to depolarize, and equalize the potential. The electrical conductance through a channel n at a given time and voltage, is given as: 
$$g_i [1/Ω m^2] \quad \text{(i: specific ion channel)}$$
The current through a given ion channel is given by:
$$I_i = g_i (V_m - V_i) \quad (V_i: \text{Reversal potential})$$
The [*reversal potential*](https://en.wikipedia.org/wiki/Reversal_potential) is the membrane potential at which the direction of ionic current reverses. At the reversal potential, there is no net flow of ions from one side of the membrane to the other.

### Leak channel
In the cells, there are also so-called [*leak channels*](https://en.wikipedia.org/wiki/Two-pore-domain_potassium_channel) (I haven't quite understood these). They are modeled as the linear conductance: $$g_L [1/Ω m^2]$$
The current through the leak channel is therefore: $$I_l = g_L (V_m - V_L)$$

### Total current through membrane

The total current through the membrane for a cell with sodium and potassium channels is hence: 
$$I = C_m \frac{d V_m}{dt} + g_K (V_m - V_K)+ g_{Na} (V_m - V_{Na}) + g_L (V_m - V_L) \quad [A / m^2]$$

The variables $g_{Na}$, $g_K$ and $V_m$ are really time-dependant. So these needs to be modeled. After a set of experiments, Hodkin and Huxley came up with the following sets of ODE's to model the current more correctly.
$$I = C_m \frac{d V_m}{dt} + \bar{g_K} n^4 (V_m - V_K) + \bar{g_{Na}} m^3 h (V_m - V_{Na}) + \bar{g_L} (V_m - V_L) \quad [A / m^2]$$
$$\frac{dn}{dt} = \alpha_n (V_m) (1 - n) - \beta_n (V_m) n$$
$$\frac{dm}{dt} = \alpha_m (V_m) (1 - m) - \beta_m (V_m) m$$
$$\frac{dh}{dt} = \alpha_h (V_m) (1 - h) - \beta_h (V_m) h$$
The variable $\bar{g_n}$ is the maximal conductance for the given channel. The functions $\alpha_n$, $\alpha_m$ and $\alpha_h$ are given by:

$$\alpha_n(V_m) = $$

## Result (target)
![Animation of the action potential](images/action_potential_target.gif)