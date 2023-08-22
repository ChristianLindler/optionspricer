import math
from scipy.stats import norm

# Returns price of put option
# callOrPut: whether option is call or put (string)
# S: Price of Stock
# K: Strike Price
# T: Time to expiry
# sigma: volatility
# r: risk free interest rate
def blackScholes(callOrPut, S, K, T, sigma, r):
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if callOrPut == 'call':
        return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    elif callOrPut == 'put':
        return K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    