"""
Heston stochastic volatility model implementation.
Generates Monte Carlo paths for option pricing with stochastic volatility.
"""

import numpy as np
import tqdm

# Trading days per year
TRADING_DAYS_PER_YEAR = 252

def get_brownian_motion(dt, size):
    '''
    Generate increments of a Wiener process.
    Args:
        dt (float): Time step.
        size (int): Number of increments.
    Returns:
        np.ndarray: Array of Wiener process increments.
    '''
    return np.random.normal(0, np.sqrt(dt), size)

def generate_correlated_brownians(dt, size, correlation):
    """
    Generate correlated Wiener process increments for asset price and volatility.
    
    Args:
        dt: Time step size
        size: Number of increments (num_sims, num_steps)
        correlation: Correlation coefficient between asset and volatility processes
        
    Returns:
        Tuple of (asset_brownian, volatility_brownian) increments
    """
    corr_matrix = np.array([[1.0, correlation], [correlation, 1.0]])
    brownian_increments = np.random.multivariate_normal(
        np.array([0, 0]), cov=corr_matrix, size=size
    ) * np.sqrt(dt)
    return brownian_increments[:, :, 0], brownian_increments[:, :, 1]

def generate_paths(num_sims, initial_price, risk_free_rate, initial_volatility, 
                  time_to_expiry, mean_reversion_rate, vol_of_vol, long_term_variance, 
                  correlation, dividend_days=None):
    """
    Generate Monte Carlo paths using Heston stochastic volatility model.
    
    Implements risk-neutral pricing with discrete dividend adjustments and stochastic volatility.
    The Heston model allows volatility to follow its own stochastic process.
    
    Args:
        num_sims: Number of simulation paths
        initial_price: Initial stock price
        risk_free_rate: Risk-free interest rate
        initial_volatility: Initial volatility
        time_to_expiry: Time to expiry in years
        mean_reversion_rate: Speed of volatility mean reversion (kappa)
        vol_of_vol: Volatility of volatility parameter
        long_term_variance: Long-term variance level (theta)
        correlation: Correlation between asset and volatility processes
        dividend_days: Dividend payments on each trading day (discrete payments)
        
    Returns:
        Tuple of (time_points, price_paths)
    """
    num_steps = int(time_to_expiry * TRADING_DAYS_PER_YEAR)
    time_points = np.linspace(0, time_to_expiry, num_steps)
    dt = time_points[1]
    
    # Initialize paths and volatility
    paths = np.full((num_sims, num_steps), float(initial_price))
    variance = np.full(num_sims, float(initial_volatility ** 2))
    
    # Generate correlated Brownian motions
    asset_brownian, vol_brownian = generate_correlated_brownians(
        dt, (num_sims, num_steps - 1), float(correlation)
    )
    
    # Risk-neutral drift: mu = risk-free rate (no dividend yield adjustment for discrete dividends)
    risk_neutral_drift = risk_free_rate
    
    # Generate paths
    for t in tqdm.trange(1, num_steps, desc="Generating paths"):
        current_prices = paths[:, t - 1]
        current_vol = np.sqrt(np.maximum(variance, 0.01))  # Ensure positive volatility
        
        # Asset price evolution (risk-neutral SDE)
        drift_term = risk_neutral_drift * current_prices * dt
        diffusion_term = current_vol * current_prices * asset_brownian[:, t - 1]
        paths[:, t] = current_prices + drift_term + diffusion_term
        
        # Variance evolution (Heston volatility process)
        variance_drift = mean_reversion_rate * (long_term_variance - variance) * dt
        variance_diffusion = vol_of_vol * current_vol * vol_brownian[:, t - 1]
        variance += variance_drift + variance_diffusion
        
        # Ensure variance stays positive
        variance = np.maximum(variance, 0.01)
        
        # Apply discrete dividend if any on this day
        # The stock price drops by the dividend amount on the ex-dividend date
        if dividend_days is not None and t < len(dividend_days) and dividend_days[t] > 0:
            dividend_amount = dividend_days[t]
            # Subtract the dividend amount from the stock price
            paths[:, t] = np.maximum(paths[:, t] - dividend_amount, 0.01)
    
    return time_points, paths
    