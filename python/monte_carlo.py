# pylint: disable=C0114

import numpy as np
import tqdm
import matplotlib.pyplot as plt
from brownian_motion import generate_correlated_brownians

def generate_paths(num_sims, S0, mu, sigma, num_steps, T, kappa, vol_of_vol, theta, rho):
    '''
    Generates sample paths for a stock using the Heston Model
    dS(t) = mu*S*dt + sigma*S*dW(t)
    dV(t) = k(theta - V)dt + vol_of_vol*V*dW(t)
    The two brownian motions are correlated with rho
    num_sims: number of simulations
    S0: initial price
    mu: drift
    sigma: volatility
    num_steps: number of time steps
    T: time until expiry (years)
    kappa: mean reversion rate
    vol_of_vol: volatility of volatility
    theta: long term mean of variance
    rho: correlation for brownian motions
    Returns: time_points, paths
    '''
    time_points = np.linspace(0, T, num_steps)
    dt = time_points[1]
    paths = np.full((num_sims, num_steps), S0)
    theta = np.full(num_sims, theta)
    current_vol = np.full(num_sims, sigma)
    asset_brownian_motion, vol_brownian_motion = generate_correlated_brownians(
        dt, (num_sims, num_steps - 1), rho)
    for t in tqdm.trange(1, num_steps):
        current_prices = paths[:, t - 1]
        # The GBM Formula says dS(t) = mu*S*dt + sigma*S*dW(t)
        change_in_price = mu * paths[:, t - 1] * dt  \
            + current_vol * current_prices * asset_brownian_motion[:, t - 1]
        paths[:, t] = paths[:, t - 1] + change_in_price

        # The Heston model says dV(t) = k(theta - V)dt + vol_of_vol*V*dW(t)
        change_in_vol = kappa * (theta - current_vol ** 2) \
            * dt + vol_of_vol * current_vol * vol_brownian_motion[:, t - 1]
        current_vol += change_in_vol

    return time_points, paths

def visualize_paths(time_points, paths, strike_price=None):
    '''
    Visualizes monte carlo paths
    Include a strike price to include a line for in/out of money
    time_points: array of time points
    paths: [num_paths][num_steps]
    strike_price: strike price of option
    '''
    for path in paths:
        plt.plot(time_points, path)

    if strike_price is not None:
        plt.axhline(y=strike_price, color='r', linestyle='--',
                    label=f'Strike Price ({strike_price:.2f})')
        plt.legend()
    plt.xlabel('Time Steps (years)')
    plt.ylabel('Asset Price')
    plt.title('Monte Carlo Simulation for Asset Price')
    plt.grid(True)
    plt.show()
    