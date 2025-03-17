import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import Polynomial

def plot(param_samples, MAGT_obs, MAGT_sim_all):

    def mbe(y_obs, y_sim):
        return np.mean(y_sim - y_obs)

    # Compute MBE for each simulation result
    likelihood_values = np.array([mbe(MAGT_obs, MAGT_sim) for MAGT_sim in MAGT_sim_all])

    def calculate_grouped_mean(param_samples, likelihood_values, param_name):

        unique_param_values = np.unique(param_samples[param_name])
        mean_likelihood = []
        for value in unique_param_values:
            group_likelihood = likelihood_values[param_samples[param_name] == value]
            mean_likelihood.append(np.mean(group_likelihood))
        return unique_param_values, np.array(mean_likelihood)

    # Compute mean likelihood for each parameter
    mean_likelihood_rk_values, mean_likelihood_rk = calculate_grouped_mean(param_samples, likelihood_values, 'rk')
    mean_likelihood_nt_values, mean_likelihood_nt = calculate_grouped_mean(param_samples, likelihood_values, 'nt')
    mean_likelihood_nf_values, mean_likelihood_nf = calculate_grouped_mean(param_samples, likelihood_values, 'nf')

    # Create subplots for each parameter
    fig, axs = plt.subplots(1, 4, figsize=(20, 5))

    # Fit polynomial curves to model trends in MBE for each parameter
    poly_rk = Polynomial.fit(mean_likelihood_rk_values, mean_likelihood_rk, 3)
    poly_nt = Polynomial.fit(mean_likelihood_nt_values, mean_likelihood_nt, 3)
    poly_nf = Polynomial.fit(mean_likelihood_nf_values, mean_likelihood_nf, 5)

    # Plot rk vs likelihood (Mean Bias)
    sc = axs[2].scatter(param_samples['rk'], likelihood_values, c=likelihood_values, cmap='Blues', alpha=0.5, s=10)
    axs[2].plot(mean_likelihood_rk_values, poly_rk(mean_likelihood_rk_values), color='red', lw=3)

    axs[2].set_xlabel('$r_k$', fontsize=20)  # Thermal offset coefficient
    axs[2].set_ylabel('Mean bias (°C)', fontsize=20)
    axs[2].set_xlim(0, 1)
    axs[2].set_ylim(-10, 4)

    # Plot nt vs likelihood
    axs[1].scatter(param_samples['nt'], likelihood_values, c=likelihood_values, cmap='Blues', alpha=0.5, s=10)
    axs[1].plot(mean_likelihood_nt_values, poly_nt(mean_likelihood_nt_values), color='red', lw=3)

    axs[1].set_xlabel('$n_t$', fontsize=20)  # Thawing n-factor
    axs[1].set_ylabel('Mean bias (°C)', fontsize=20)
    axs[1].set_xlim(0, 1)
    axs[1].set_ylim(-10, 4)

    # Plot nf vs likelihood
    axs[0].scatter(param_samples['nf'], likelihood_values, c=likelihood_values, cmap='Blues', alpha=0.5, s=10)
    axs[0].plot(mean_likelihood_nf_values, poly_nf(mean_likelihood_nf_values), color='red', lw=3)

    axs[0].set_xlabel('$n_f$', fontsize=20)  # Freezing n-factor
    axs[0].set_ylabel('Mean bias (°C)', fontsize=20)
    axs[0].set_xlim(0, 1)
    axs[0].set_ylim(-10, 4)

    # Hide the fourth subplot
    axs[3].axis('off')

    # Adjust tick label sizes for readability
    for ax in axs:
        ax.tick_params(axis='both', which='major', labelsize=20)

    # Configure colorbar to represent MBE scale
    sc.set_clim(-10, 4)
    cbar = fig.colorbar(sc, ax=axs, orientation='vertical', fraction=0.02, pad=0.04)
    cbar.set_label('Mean bias (°C)', fontsize=20)
    cbar.ax.tick_params(labelsize=15)

    # Adjust layout for better visualization
    plt.tight_layout()
    plt.show()
