import math
import numpy as np
import tqdm

# Returns array of Wiener process increments
def getBrownianMotion(dt, size):
    return np.random.normal(0, math.sqrt(dt), size)

# Generates sample paths for a stock
# timePoints holds the array of sample times
# S0: initial price
# mu: drift
# sigma: volatility
# T: time until expiry (years)
# kappa: mean reversion rate
# volOfVol: volatility of volatility
# theta: long term mean of variance
def generatePaths(numSims, S0, mu, sigma, numSteps, T, kappa, volOfVol, theta):
    timePoints = np.linspace(0, T, numSteps)
    dt = timePoints[1]
    
    paths = np.full((numSims, numSteps), S0)
    assetBrownianMotion = getBrownianMotion(dt, (numSims, numSteps - 1))
    volBrownianMotion = getBrownianMotion(dt, (numSims, numSteps - 1))
    theta = np.full(numSims, theta)
    theta = currentVol = np.full(numSims, sigma)
    for t in tqdm.trange(1, numSteps):
        currentPrices = paths[:, t - 1]
        # The GBM Formula says dS(t) = mu*S*dt + sigma*S*dW(t) 
        changeInPrice = mu * paths[:, t - 1] * dt + currentVol * currentPrices * assetBrownianMotion[:, t - 1]
        paths[:, t] = paths[:, t - 1] + changeInPrice
        # The Heston model says dV(t) = k(theta - V)dt + volOfVol*V*dW(t) 
        changeInVol = kappa * (theta - currentVol) * dt + volOfVol * currentVol * volBrownianMotion[:, t - 1]
        currentVol += changeInVol
    return timePoints, paths

# Finds discounted payoff of option using final prices of random walks
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
