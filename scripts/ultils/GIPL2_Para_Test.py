import numpy as np
import os
import shutil
import subprocess
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import Polynomial


def process_point(point, VWC, a, b, TVHC, FVHC, THC, FHC, tas, pr, TTOP):

    try:
        # Define base directory and source directory for running the model
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        src = os.path.join(BASE_DIR, '../../data/GIPL_GLUE')

        # Create a unique directory for the model run
        dir_name = os.path.join(BASE_DIR, '../../temp/run_GIPL_GLUE/gipl_{}'.format(point))
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        shutil.copytree(src, dir_name)

        # Write temperature boundary conditions to input file
        with open(os.path.join(dir_name, 'in/bound.txt'), 'w') as f:
            f.write('600\n')
            for i in range(600):
                f.write(f"{i + 1}\t{tas[i].round(2)}\n")

        # Write initial soil temperature profile
        with open(os.path.join(dir_name, 'in/initial.txt'), 'w') as f:
            f.write('1\t4\nDEPTH\tTEMP\n')
            f.write('-1.5\t0\n')
            f.write(f'5\t{TTOP}\n')
            f.write(f'80\t{TTOP}\n')
            f.write('120\t0\n')

        # Write soil property parameters
        with open(os.path.join(dir_name, 'in/mineral.txt'), 'w') as f:
            f.write('1\n1\t1\n')
            f.write(f"{VWC.round(2)}\t{a.round(2)}\t{b.round(2)}\t{TVHC.round(2)}\t"
                    f"{FVHC.round(2)}\t{THC.round(2)}\t{FHC.round(2)}\t120\n")

        # Compute and write snow accumulation data based on precipitation and temperature
        snow = np.full(600, 0.0)
        for year in range(1960, 2010):
            for mon in range(12):
                index = 12 * (year - 1960) + mon
                if tas[index] > 2:
                    snow[index] = 0
                else:
                    if tas[index] > -2:
                        pr[index] *= (0.5 - 0.25 * tas[index])
                    snow[index] = pr[index] if index == 0 or snow[index - 1] == 0 else pr[index] + snow[index - 1]

        snow = np.maximum(snow / 0.138 / 1000, 0.0)  # Convert snow depth and ensure non-negative values

        with open(os.path.join(dir_name, 'in/snow.txt'), 'w') as f:
            f.write('600\n')
            for i in range(600):
                f.write(f"{i + 1}\t{snow[i].round(2)}\n")

        # Run the GIPL model
        os.chdir(dir_name)
        subprocess.run('./gipl.exe', check=True)

        # Extract model output and compute the mean annual ground temperature (MAGT)
        outdata = np.loadtxt(os.path.join(dir_name, 'out/result.txt'), usecols=(4, 5, 6, 7, 8, 9))
        out = np.array([np.nanmean(outdata[12 * year: 12 * (year + 1), 5]) for year in range(50)])

        print(f"Processing completed for sample {point}.")
        return np.nan if np.isnan(out[49]) else out[49]
    except Exception as e:
        print(f"Error processing point {point}: {e}")
        return np.nan


def plot(param_samples, MAGT_obs, MAGT_sim_all, MAGT_sim_all2):

    def mbe(y_obs, y_sim):
              return np.mean(y_sim - y_obs)

    # Compute MBE for each simulation
    likelihood_values = np.array([mbe(MAGT_obs, MAGT_sim) for MAGT_sim in MAGT_sim_all])

    def calculate_grouped_mean(param_samples, likelihood_values, param_name):

        param_samples[param_name] = np.delete(param_samples[param_name], np.isnan(MAGT_sim_all2), axis=0)
        unique_param_values = np.unique(param_samples[param_name])

        mean_likelihood = [np.mean(likelihood_values[param_samples[param_name] == value]) for value in
                           unique_param_values]
        return unique_param_values, np.array(mean_likelihood)

    # Compute mean likelihood values for each parameter
    param_names = ['VWC', 'a', 'b', 'TVHC', 'FVHC', 'THC', 'FHC']
    grouped_means = {name: calculate_grouped_mean(param_samples, likelihood_values, name) for name in param_names}

    # Create subplots for visualization
    fig, axs = plt.subplots(2, 4, figsize=(20, 10))

    # Fit a cubic polynomial to the data
    fitted_polynomials = {name: Polynomial.fit(grouped_means[name][0], grouped_means[name][1], 3) for name in
                          param_names}

    # Scatter plot each parameter against likelihood values
    for i, (name, ax) in enumerate(zip(param_names, axs.flatten()[:-1])):
        ax.scatter(param_samples[name], likelihood_values, c=likelihood_values, cmap='Greens', alpha=0.5, s=10)
        ax.set_xlabel(name, fontsize=20)
        ax.set_ylabel('Mean bias (°C)', fontsize=20)
        ax.set_ylim(-10, 4)
        ax.plot(grouped_means[name][0], fitted_polynomials[name](grouped_means[name][0]), color='red', lw=3,
                label='Polynomial Fit')

    axs[1, 3].axis('off')  # Hide the last unused subplot

    # Set x-axis limits for each parameter
    x_limits = [(0.05, 0.6), (0.05, 0.5), (-2, 2), (1500000, 4000000), (1500000, 4000000), (0.05, 3), (0.05, 3)]
    for ax, xlim in zip(axs.flatten()[:-1], x_limits):
        ax.set_xlim(xlim)

    # Adjust tick size
    for ax in axs.flatten():
        ax.tick_params(axis='both', which='major', labelsize=20)

    # Add colorbar
    sc = axs[0, 0].scatter(grouped_means['VWC'][0], grouped_means['VWC'][1], c=grouped_means['VWC'][1], cmap='Greens',
                           alpha=0.5, s=10)
    sc.set_clim(-10, 4)
    cbar = fig.colorbar(sc, ax=axs, orientation='vertical', fraction=0.02, pad=0.04)
    cbar.set_label('Mean bias (°C)', fontsize=20)
    cbar.ax.tick_params(labelsize=20 * 0.85)

    # Adjust colorbar position
    pos = cbar.ax.get_position()
    cbar.ax.set_position([pos.x0, pos.y0 - 0.08, pos.width * 1.5, pos.height * 0.6])

    plt.tight_layout()
    plt.show()
