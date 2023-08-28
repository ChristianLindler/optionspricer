# pylint: disable=C0114
import math
from scipy.stats import norm

def black_scholes(call_or_put, S, K, T, sigma, r):
    """
    call_or_put: whether option is call or put (string)
    S: Price of Stock
    K: Strike Price
    T: Time to expiry
    sigma: volatility
    r: risk free interest rate
    Returns: price of option
    """
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if call_or_put == 'call':
        return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    elif call_or_put == 'put':
        return K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    