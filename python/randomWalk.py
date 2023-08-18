import numpy as np
import math
import matplotlib.pyplot as plt
#from scipy.stats import norm

paths = 100
initialPrice = 1000
drift = .6
volatility = .2
dt = 1/365
T = 1

# Returns an expected path of a stock
# initial price of stock, drift (expected return), volatility (over time period T), change in time, time remaining
def geometricBrownianMotion(initialPrice, drift, volatility, dt, T):
    currentPrice = initialPrice
    prices = [currentPrice]
    while dt < T:
        brownianMotion = np.random.normal(0, math.sqrt(dt))
        changeInPrice = drift * dt + volatility * brownianMotion
        currentPrice += changeInPrice
        prices.append(currentPrice)
        T -= dt
    return prices

# Generates many sample paths of a stock
def generateSamplePaths(numPaths, initialPrice, drift, volatility, dt, T):
    paths = []
    for i in range(numPaths):
        paths.append(geometricBrownianMotion(initialPrice, drift, volatility, dt, T))
    return paths

paths = generateSamplePaths(100, initialPrice, drift, volatility, dt, T)

for path in paths:
    plt.plot(path)
plt.show()