import blackScholes
import monteCarlo
import matplotlib.pyplot as plt
import yfinance as yf

NUM_SIMS = 100000
NUM_STEPS = 1000

def vol_dynamics(previousPrices, currentPrices, previousVol, vcr=-11):
    return


# Calculates the price of an option
# ticker: Stock ticker
# K: Strike Price
# T: Time to expiry
# r: risk free interest rate
def priceOption(callOrPut, ticker, K, T, r, vol_reversion):
    stockData = yf.Ticker(ticker)
    initialPrice = stockData.history(period="1d")["Close"].iloc[0]
    print('initial price', initialPrice)
    # TEMP VALUES:
    drift = r
    volatility = 0.2

    timePoints, paths = monteCarlo.generatePaths(NUM_SIMS, initialPrice, drift, volatility, NUM_STEPS, T, vol_reversion, 0)
    mcprice = monteCarlo.monteCarloPrice(callOrPut, paths, K, r, T)
    bcprice = blackScholes.blackScholesCall(initialPrice, K, T, volatility, r)
    print('MC:', mcprice)
    print('BS:', bcprice)

    #for path in paths:
        #plt.plot(timePoints, path)
    #plt.show()
    

priceOption('call', 'GOOG', 125, 3, 0.03, 1)