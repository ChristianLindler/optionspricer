import numpy as np
import tqdm
import matplotlib.pyplot as plt

NUM_TRADING_DAYS = 252

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
    rho: covariance
    Returns: array of correlated Wiener process increments
    '''
    corr_matrix = np.array([[1.0, rho], [rho, 1.0]])
    WT = np.random.multivariate_normal(np.array([0, 0]), cov=corr_matrix, size=size) * np.sqrt(dt)
    return WT[:, :, 0], WT[:, :, 1]

def visualize_correlated_brownians(dt, num_steps, rho, num_sims = 1):
    '''
    dt: time step
    num_steps: number of increments
    rho: covariance
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

def generate_paths(num_sims, S0, mu, sigma, T, kappa, vol_of_vol, theta, rho, dividend_days=[]):
    '''
    Generates sample paths for a stock using the Heston Model
    dS(t) = mu*S*dt + sigma*S*dW(t)
    dV(t) = k(theta - V)dt + vol_of_vol*sigma*dW(t)
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
    dividend_days ([]): ith element is 1/100 * percentage dividend on ith day
    Returns: time_points, paths
    '''

    num_steps = int(T * NUM_TRADING_DAYS)
    time_points = np.linspace(0, T, num_steps)
    dt = time_points[1]

    paths = np.full((num_sims, num_steps), float(S0))
    theta = np.full(num_sims, float(theta))

    current_vol = np.full(num_sims, float(sigma))

    # Generates two matrices of brownian motions such that A[i, j] has covariance rho with B[i, j]
    asset_brownian_motion, vol_brownian_motion = generate_correlated_brownians(
        dt, (num_sims, num_steps - 1), float(rho))
    
    for t in tqdm.trange(1, num_steps):
        current_prices = paths[:, t - 1]
        # The GBM Formula says dS(t) = mu*S*dt + sigma*S(t)*dW(t)
        change_in_price = mu * current_prices * dt  + current_vol * current_prices * asset_brownian_motion[:, t - 1]
        paths[:, t] = (current_prices + change_in_price) * (1 - dividend_days[t - 1])

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
    