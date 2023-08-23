import math
import numpy as np
import tqdm

# Returns array of Wiener process increments
def get_brownian_motion(dt, size):
    return np.random.normal(0, math.sqrt(dt), size)

# Generates sample paths for a stock
# time_points holds the array of sample times
# S0: initial price
# mu: drift
# sigma: volatility
# T: time until expiry (years)
# kappa: mean reversion rate
# vol_of_vol: volatility of volatility
# theta: long term mean of variance
def generate_paths(num_sims, S0, mu, sigma, num_steps, T, kappa, vol_of_vol, theta):
    time_points = np.linspace(0, T, num_steps)
    dt = time_points[1]
    
    paths = np.full((num_sims, num_steps), S0)
    asset_brownian_motion = get_brownian_motion(dt, (num_sims, num_steps - 1))
    vol_brownian_motion = get_brownian_motion(dt, (num_sims, num_steps - 1))
    theta = np.full(num_sims, theta)
    theta = current_vol = np.full(num_sims, sigma)
    for t in tqdm.trange(1, num_steps):
        current_prices = paths[:, t - 1]
        # The GBM Formula says dS(t) = mu*S*dt + sigma*S*dW(t) 
        change_in_price = mu * paths[:, t - 1] * dt + current_vol * current_prices * asset_brownian_motion[:, t - 1]
        paths[:, t] = paths[:, t - 1] + change_in_price
        # The Heston model says dV(t) = k(theta - V)dt + vol_of_vol*V*dW(t) 
        change_in_vol = kappa * (theta - current_vol) * dt + vol_of_vol * current_vol * vol_brownian_motion[:, t - 1]
        current_vol += change_in_vol
    return time_points, paths

# Finds discounted payoff of option using final prices of random walks
# call_or_put: whether option is call or put (string)
# paths: [num_paths][num_steps]
# K: strike price
# r: risk free interest rate
# T: time until expiry (years)
def monte_carlo_price(call_or_put, paths, K, r, T):
    paths = np.array(paths)
    if call_or_put == 'call':
        payoffs = np.maximum(0, paths[:,-1] - K)
    elif call_or_put == 'put':
        payoffs = np.maximum(0, K - paths[:,-1])
    # Discount payoffs to present value using risk free interest rate
    return np.mean(payoffs)*np.exp(-r*T)
