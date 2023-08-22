import math
import numpy as np
import tqdm

# Returns Wiener process increment
def getBrownianMotion(dt, size):
    return np.random.normal(0, math.sqrt(dt), size)

# Generates many sample paths of a stock
# timePoints holds the array of sample times
# S0: initial price
# mu: drift
# sigma: volatility
# T: time until expiry (years)
def generatePaths(numSims, S0, mu, sigma, numSteps, T, k, volOfVol):
    timePoints = np.linspace(0, T, numSteps)
    dt = timePoints[1]
    # paths = []
    # for i in range(numSims):
    #     path = [S0]
    #     currentPrice = S0
    #     currentVol = sigma
    #     for t in timePoints[1:]:
    #         #changeInPrice = np.exp(mu * dt + sigma * brownianMotion)
    #         changeInPrice = mu * S0 * dt + currentVol * currentPrice * brownianMotion(dt)
    #         currentPrice += changeInPrice
    #         #changeInVol = k * (sigma - currentVol) * dt + volOfVol * currentVol * brownianMotion(dt)
    #         #currentVol += changeInVol
    #         #sigma = vol_dynamic_func(currentPrice, newPrice, sigma)
    #         path.append(currentPrice)
    #     paths.append(path)

    paths = np.full((numSims, numSteps), S0)
    assetBrownianMotion = getBrownianMotion(dt, (numSims, numSteps - 1))
    volBrownianMotion = getBrownianMotion(dt, (numSims, numSteps - 1))
    longTermVol = currentVol = np.full(numSims, sigma)
    for t in tqdm.trange(1, numSteps):
        #changeInPrice = np.exp(mu * dt + sigma * brownianMotion)
        currentPrices = paths[:, t - 1]
        changeInPrice = mu * paths[:, t - 1] * dt + currentVol * currentPrices * assetBrownianMotion[:, t - 1]
        paths[:, t] = paths[:, t - 1] + changeInPrice
        changeInVol = k * (longTermVol - currentVol) * dt + volOfVol * currentVol * volBrownianMotion[:, t - 1]
        currentVol += changeInVol
        #sigma = vol_dynamic_func(currentPrice, newPrice, sigma)
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
