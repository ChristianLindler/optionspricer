"""
Black-Scholes option pricing model implementation.
Provides both analytical pricing and Monte Carlo simulation for European options.
"""

import math
import numpy as np


def normal_cdf(x):
    """
    Cumulative normal distribution function using error function approximation.
    
    Args:
        x: Input value
        
    Returns:
        Cumulative probability P(X <= x) for standard normal distribution
    """
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def black_scholes(call_or_put, stock_price, strike_price, time_to_expiry, volatility, risk_free_rate, dividend_yield=0.0):
    """
    Calculate European option price using Black-Scholes analytical formula.
    
    Args:
        call_or_put: Option type ('call' or 'put')
        stock_price: Current stock price
        strike_price: Option strike price
        time_to_expiry: Time to expiry in years
        volatility: Annualized volatility
        risk_free_rate: Risk-free interest rate
        dividend_yield: Continuous dividend yield (annualized, as a decimal)
        
    Returns:
        European option price
    """
    d1 = (math.log(stock_price / strike_price) + (risk_free_rate - dividend_yield + 0.5 * volatility ** 2) * time_to_expiry) / (volatility * math.sqrt(time_to_expiry))
    d2 = d1 - volatility * math.sqrt(time_to_expiry)
    
    if call_or_put == 'call':
        return stock_price * math.exp(-dividend_yield * time_to_expiry) * normal_cdf(d1) - strike_price * math.exp(-risk_free_rate * time_to_expiry) * normal_cdf(d2)
    elif call_or_put == 'put':
        return strike_price * math.exp(-risk_free_rate * time_to_expiry) * normal_cdf(-d2) - stock_price * math.exp(-dividend_yield * time_to_expiry) * normal_cdf(-d1)
    else:
        raise ValueError(f'Invalid option type: {call_or_put}. Must be "call" or "put"')


def price_european_option(call_or_put, paths, strike_price, risk_free_rate, time_to_expiry):
    """
    Price European option using Monte Carlo simulation on final path values.
    
    Calculates discounted payoffs using the terminal stock prices from simulated paths.
    This is equivalent to Black-Scholes for European options but uses simulation.
    
    Args:
        call_or_put: Option type ('call' or 'put')
        paths: Array of simulated stock price paths [num_paths][num_steps]
        strike_price: Option strike price
        risk_free_rate: Risk-free interest rate
        time_to_expiry: Time to expiry in years
        
    Returns:
        Tuple of (option_price, standard_error)
    """
    paths = np.array(paths)
    
    # Calculate payoffs at expiry
    if call_or_put == 'call':
        payoffs = np.maximum(0, paths[:, -1] - strike_price)
    elif call_or_put == 'put':
        payoffs = np.maximum(0, strike_price - paths[:, -1])
    else:
        raise ValueError(f'Invalid option type: {call_or_put}. Must be "call" or "put"')
    
    # Discount payoffs to present value
    discounted_payoffs = payoffs * np.exp(-risk_free_rate * time_to_expiry)
    
    # Calculate statistics
    option_price = np.mean(discounted_payoffs)
    standard_error = np.std(discounted_payoffs, ddof=1) / np.sqrt(len(discounted_payoffs))
    
    return option_price, standard_error