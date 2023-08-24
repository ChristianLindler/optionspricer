import numpy as np
import matplotlib.pyplot as plt

# Returns array of Wiener process increments
def get_brownian_motion(dt, size):
    return np.random.normal(0, np.sqrt(dt), size)

# Function to generate correlated Brownian motions
def generate_correlated_brownians(dt, size, rho):
    corr_matrix = np.array([[1.0, rho], [rho, 1.0]])
    WT = np.random.multivariate_normal(np.array([0, 0]), cov=corr_matrix, size=size) * np.sqrt(dt)
    return WT[:, :, 0], WT[:, :, 1]

def visualize_correlated_brownians(dt, num_sims, num_steps, rho):
    asset_brownian_motion, vol_brownian_motion = generate_correlated_brownians(dt, (num_sims, num_steps), rho)
    plt.figure(figsize=(12, 6))
    time_steps = np.arange(num_steps) * dt 
    
    for i in range(num_sims):
        plt.plot(time_steps, asset_brownian_motion[i], label=f'Asset Path {i+1}')
        plt.plot(time_steps, vol_brownian_motion[i], label=f'Volatility Path {i+1}', linestyle='--')

    plt.xlabel('Time Steps')
    plt.ylabel('Brownian Motion Value')
    plt.title('Correlated Asset Price and Volatility Brownian Motions')
    plt.legend()
    plt.grid(True)
    plt.show()