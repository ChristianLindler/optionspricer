"""
Volatility estimation from historical price data.
Calculates annualized volatility using log returns from daily prices.
"""

import numpy as np

# Trading days per year for annualization
TRADING_DAYS_PER_YEAR = 252


def compute_std_of_log_returns(price_list):
    """
    Compute annualized volatility from daily log returns.
    
    Calculates the standard deviation of daily log returns and annualizes
    by multiplying by sqrt(252) to get the annualized volatility.
    
    Args:
        price_list: List of (date, price) tuples in chronological order
        
    Returns:
        float: Annualized volatility (standard deviation of log returns)
        
    Raises:
        ValueError: If insufficient price data or invalid prices
    """
    if len(price_list) < 2:
        raise ValueError("Need at least 2 price points to calculate volatility")
    
    prices = np.array([price for _, price in price_list])
    
    # Validate prices
    if np.any(prices <= 0):
        raise ValueError("All prices must be positive")
    
    # Calculate daily log returns
    log_returns = np.diff(np.log(prices))
    
    # Calculate daily volatility
    daily_vol = np.sqrt(np.var(log_returns, ddof=1))
    
    # Annualize: multiply by sqrt(252) for trading days
    annual_vol = daily_vol * np.sqrt(TRADING_DAYS_PER_YEAR)
    
    return annual_vol
