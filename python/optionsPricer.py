import blackScholes
import monteCarlo
import matplotlib.pyplot as plt
import yfinance as yf

NUM_SIMS = 10000
NUM_STEPS = 252

#def vol_dynamics()

# Calculates the price of an option
# ticker: Stock ticker
# K: Strike Price
# T: Time to expiry
# r: risk free interest rate
def priceOption(callOrPut, ticker, K, T, r):
    stockData = yf.Ticker(ticker)
    initialPrice = stockData.history(period="1d")["Close"].iloc[0]
    print('initial price', initialPrice)
    # TEMP VALUES:
    drift = 0
    volatility = 0.2

    timePoints, paths = monteCarlo.generatePaths(NUM_SIMS, initialPrice, drift, volatility, NUM_STEPS, T, r)
    mcprice = monteCarlo.monteCarloPrice(callOrPut, paths, K, r, T)
    bcprice = blackScholes.blackScholesCall(initialPrice, K, T, volatility, r)
    for path in paths:
        plt.plot(timePoints, path)
    print('MC:', mcprice)
    print('BS:', bcprice)
    plt.show()

priceOption('call', 'GOOG', 125, 1, 0.03)