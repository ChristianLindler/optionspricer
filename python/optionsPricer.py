import blackScholes
import monteCarlo
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np

NUM_SIMS = 100
NUM_STEPS = 1000

def vol_dynamics(previousPrices, currentPrices, previousVol, vcr=-11):
    return

# Calculates historical volatility for a stock
# ticker: Stock ticker
# numDays: number of days incorporate for the calculation
def getHistoricalVolatility(ticker, numDays):
    stockData = yf.download(ticker)
    stockData = stockData.sort_values(by='Date', ascending=False).head(numDays)
    stockData['Daily_Returns'] = stockData['Adj Close'].pct_change()
    # Calculate annualized historical volatility
    return np.std(stockData['Daily_Returns']) * np.sqrt(252)


# Calculates the price of an option
# ticker: Stock ticker
# K: Strike Price
# T: Time to expiry
# r: risk free interest rate
# kappa: volatility mean reversion rate
def priceOption(callOrPut, ticker, K, T, r, kappa):
    stockData = yf.Ticker(ticker)
    initialPrice = stockData.history(period="1d")["Close"].iloc[0]
    print('initial price', initialPrice)
    
    # TEMP VALUES
    volatility = getHistoricalVolatility(ticker)
    theta = volatility ** 2
    volOfVol = 0.3

    # Drift set to risk free interest rate (risk neutral pricing)
    timePoints, paths = monteCarlo.generatePaths(NUM_SIMS, initialPrice, r, volatility, NUM_STEPS, T, kappa, volOfVol, theta)
    mcprice = monteCarlo.monteCarloPrice(callOrPut, paths, K, r, T)
    bcprice = blackScholes.blackScholes(callOrPut, initialPrice, K, T, volatility, r)
    print('MC:', mcprice)
    print('BS:', bcprice)

    for path in paths:
        plt.plot(timePoints, path)
    plt.show()
    

#priceOption('call', 'GOOG', 125, 3, 0.03, 3)
print(getHistoricalVolatility('GOOG', 30))