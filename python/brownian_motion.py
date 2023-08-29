# pylint: disable=C0114

import numpy as np
import matplotlib.pyplot as plt

def get_brownian_motion(dt, size):
    '''
    dt: time step
    size: number of increments
    Returns: array of Wiener process increments
    '''
    return np.random.normal(0, np.sqrt(dt), size)

def generate_correlated_brownians(dt, size, rho):
    '''
    dt: time step
    size: number of increments
    rho: correlation
    Returns: array of correlated Wiener process increments
    '''
    corr_matrix = np.array([[1.0, rho], [rho, 1.0]])
    WT = np.random.multivariate_normal(np.array([0, 0]), cov=corr_matrix, size=size) * np.sqrt(dt)
    return WT[:, :, 0], WT[:, :, 1]

def visualize_correlated_brownians(dt, num_steps, rho, num_sims = 1):
    '''
    dt: time step
    num_steps: number of increments
    rho: correlation
    num_sims: number of simulations, default 1 for most clear visualization
    Visualizes the correlation between asset and volatility brownian motions
    '''
    asset_brownian_motion, vol_brownian_motion = generate_correlated_brownians(
        dt, (num_sims, num_steps), rho)
    plt.figure(figsize=(12, 6))
    time_steps = np.arange(num_steps) * dt
    for i in range(num_sims):
        plt.plot(time_steps, asset_brownian_motion[i], label=f'Asset Brownian Motion {i+1}')
        plt.plot(time_steps, vol_brownian_motion[i], label=f'Volatility Brownian Motion {i+1}')

    plt.xlabel('Time Steps')
    plt.ylabel('Brownian Motion Value')
    plt.title('Correlated Asset Price and Volatility Brownian Motions')
    plt.legend()
    plt.grid(True)
    plt.show()

dt = 1/252
num_steps = 100
rho = -0.7
#visualize_correlated_brownians(dt, num_steps, rho)
