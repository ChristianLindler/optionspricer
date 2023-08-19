import math
import numpy as np

# Returns an expected path of a stock
# sigma: volatility
# mu: drift coefficient (expected return)
# T: time until expiry (years)
# n: number of steps
def generateRandomWalk(initialPrice, mu, sigma, T, n):
    dt = T/n
    currentPrice = initialPrice
    prices = [currentPrice]
    while dt < T:
        brownianMotion = np.random.normal(0, math.sqrt(dt))
        changeInPrice = mu * dt + sigma * brownianMotion
        currentPrice += changeInPrice
        prices.append(currentPrice)
        T -= dt
    return prices

# Generates many sample paths of a stock
# mu: drift
# sigma: volatility
# T: time until expiry (years)
def generatePaths(numSimulations, initialPrice, mu, sigma, numSteps, T):
    paths = []
    for i in range(numSimulations):
        paths.append(generateRandomWalk(initialPrice, mu, sigma, numSteps, T))
    return paths

# callOrPut: whether option is call or put (string)
# paths: [numPaths][numSteps]
# K: strike price
# r: risk free interest rate
# T: time until expiry (years)
def monteCarloPrice(callOrPut, paths, K, r, T):
    if callOrPut == 'call':
        payoffs = max(0, paths[-1] - K)
    elif callOrPut == 'put':
        payoffs = max(0, K - paths[-1])
    # Discount payoffs to present value using risk free interest rate
    return np.mean(payoffs)*np.exp(-r*T)
