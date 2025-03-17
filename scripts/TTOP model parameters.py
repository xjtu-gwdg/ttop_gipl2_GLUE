import numpy as np
from pyDOE2 import lhs
from ultils.TTOP_Para_Test import plot
import warnings

# Suppress UserWarnings to avoid unnecessary messages
warnings.simplefilter("ignore", category=UserWarning)

# Define the TTOP model function
# This model estimates the mean annual ground temperature (MAGT) based on empirical parameters
def ttop_model(nf, nt, rk, FDD, TDD):

    return (nf * FDD + nt * TDD + rk) / 365

# Observed data for Borehole No.66
# These values represent climate-driven ground temperature variations
FDD_obs = -3160.36  # Observed Freezing Degree Days
TDD_obs = 378.67  # Observed Thawing Degree Days
MAGT_obs = -1.63   # Observed Mean Annual Ground Temperature (MAGT)

# Number of parameter samples for Latin Hypercube Sampling (LHS)
n_samples = 10000

# Define parameter ranges for LHS sampling
# All parameters (rk, nt, nf) are constrained between 0 and 1
param_bounds = {
    'rk': [0.0, 1.0],  # The ratio of soil thermal conductivity in frozen and thawed states
    'nt': [0.0, 1.0],  # The ratio between ground surface temperatures and air temperatures during thawing days
    'nf': [0.0, 1.0]   # The ratio between ground surface temperatures and air temperatures during freezing days
}

# Generate Latin Hypercube Samples (LHS) for parameter space exploration
lhs_samples = lhs(len(param_bounds), samples=n_samples, criterion="center")

# Scale sampled values to match the defined parameter ranges
param_samples = {
    name: (bounds[0] + lhs_samples[:, i] * (bounds[1] - bounds[0]))
    for i, (name, bounds) in enumerate(param_bounds.items())
}

# Simulate MAGT for each parameter set using the TTOP model
MAGT_sim_all = []
for i in range(n_samples):
    MAGT_sim = ttop_model(
        param_samples['nf'][i],
        param_samples['nt'][i],
        param_samples['rk'][i],
        FDD_obs,
        TDD_obs
    )
    MAGT_sim_all.append(MAGT_sim)
MAGT_sim_all = np.array(MAGT_sim_all)

# Plot the results
plot(param_samples, MAGT_obs, MAGT_sim_all)
