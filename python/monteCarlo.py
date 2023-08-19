import math
import numpy as np


# Generates many sample paths of a stock
# timePoints holds the array of sample times
# S0: initial price
# mu: drift
# sigma: volatility
# T: time until expiry (years)
def generatePaths(numSims, S0, mu, sigma, numSteps, T, r):
    dt = float(T)/numSteps
    timePoints = np.arange(0, T+dt, dt)
    paths = []
    for i in range(numSims):
        path = [S0]
        currentPrice = S0
        for t in timePoints[1:]:
            brownianMotion =  np.random.normal(0, math.sqrt(dt))  # Wiener process increment
            #changeInPrice = np.exp(mu * dt + sigma * brownianMotion)
            changeInPrice = mu * S0 * dt + sigma * currentPrice * brownianMotion
            newPrice = currentPrice + changeInPrice
            #sigma = vol_dynamic_func(currentPrice, newPrice, sigma)
            currentPrice = newPrice
            path.append(currentPrice)
        paths.append(path)
    return timePoints, paths

# callOrPut: whether option is call or put (string)
# paths: [numPaths][numSteps]
# K: strike price
# r: risk free interest rate
# T: time until expiry (years)
def monteCarloPrice(callOrPut, paths, K, r, T):
    paths = np.array(paths)
    if callOrPut == 'call':
        payoffs = np.maximum(0, paths[:,-1] - K)
    elif callOrPut == 'put':
        payoffs = np.maximum(0, K - paths[:,-1])
    # Discount payoffs to present value using risk free interest rate
    return np.mean(payoffs)*np.exp(-r*T)
