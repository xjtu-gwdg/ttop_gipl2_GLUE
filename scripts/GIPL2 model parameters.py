import numpy as np
from pyDOE2 import lhs
import warnings
from ultils.GIPL2_Para_Test import process_point, plot

# Suppress RuntimeWarnings to prevent unnecessary warning messages
warnings.simplefilter("ignore", category=RuntimeWarning)
warnings.simplefilter("ignore", category=UserWarning)

# Set the number of Monte Carlo simulation samples
# For quick demonstration, we set n_samples to 100; in real tests, use 10,000.
n_samples = 100
# n_samples = 10000

# Set random seed for reproducibility
np.random.seed(42)

# In this demonstration, we use Borehole No.66 as the observed value
# In actual tests, all boreholes should be used
MAGT_obs = -1.63

# Define parameter ranges for Latin Hypercube Sampling (LHS)
param_bounds = {
    'VWC': [0.05, 0.6],  # The volumetric water content (fraction of 1)
    'a': [0.05, 0.5],  # The coefficient a of the unfrozen water curve
    'b': [-2, 2],  # The coefficient b of the unfrozen water curve
    'TVHC': [1500000, 4000000],  # Thawed volumetric heat capacities (J/(m³·K))
    'FVHC': [1500000, 4000000],  # Frozen volumetric heat capacities (J/(m³·K))
    'THC': [0.05, 3],  # Thawed heat conductivities (W/(m·K))
    'FHC': [0.05, 3],  # Frozen heat conductivities (W/(m·K))
}

# Generate LHS samples within the specified parameter bounds
lhs_samples = lhs(len(param_bounds), samples=n_samples)
param_samples = {
    name: (bounds[0] + lhs_samples[:, i] * (bounds[1] - bounds[0]))
    for i, (name, bounds) in enumerate(param_bounds.items())
}

# Load air temperature (tas) and precipitation (pr) data for Borehole No.66
# The dataset is located in the "data" folder
tas = np.loadtxt('../data/tas.csv')
pr = np.loadtxt('../data/pr.csv')

# Run model simulations for each parameter sample
results = []
for i in range(n_samples):
    results.append(process_point(i,
          param_samples['VWC'][i],
          param_samples['a'][i],
          param_samples['b'][i],
          param_samples['TVHC'][i],
          param_samples['FVHC'][i],
          param_samples['THC'][i],
          param_samples['FHC'][i], tas, pr, -2.19))

# Convert simulation results to a NumPy array
res = np.array(results)

# Remove NaN values from the simulation results
MAGT_sim_all2 = np.array(res)
MAGT_sim_all2 = [np.nan if value is None else value for value in MAGT_sim_all2]
MAGT_sim_all = np.delete(MAGT_sim_all2, np.isnan(MAGT_sim_all2), axis=0)

# Plot simulation results
plot(param_samples, MAGT_obs, MAGT_sim_all, MAGT_sim_all2)
