# pylint: disable=C0114
import math
from scipy.stats import norm
import numpy as np

def black_scholes(call_or_put, S, K, T, sigma, r):
    '''
    call_or_put: whether option is call or put (string)
    S: Price of Stock
    K: Strike Price
    T: Time to expiry
    sigma: volatility
    r: risk free interest rate
    Returns: price of European option
    '''
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if call_or_put == 'call':
        return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    elif call_or_put == 'put':
        return K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    

def price_european_option(call_or_put, paths, K, r, T):
    '''
    Finds discounted payoff of option using final prices of random walks
    call_or_put: whether option is call or put (string)
    paths: [num_paths][num_steps]
    K: strike price
    r: risk free interest rate
    T: time until expiry (years)
    Returns: mean payoff, mean payoff sample std, payoff sample std
    '''
    paths = np.array(paths)
    if call_or_put == 'call':
        payoffs = np.maximum(0, paths[:,-1] - K)
    elif call_or_put == 'put':
        payoffs = np.maximum(0, K - paths[:,-1])
    else:
        print(f'Unusable value for call_or_put: {call_or_put}')
        return None, None, None
    
    # Discount payoffs to present value using risk free interest rate
    discounted_payoffs = payoffs * np.exp(-r * T)
    mean_payoff = np.mean(discounted_payoffs)
    
    std_dev = np.std(discounted_payoffs, ddof=1)
    se = std_dev / np.sqrt(len(discounted_payoffs))
    return mean_payoff, se