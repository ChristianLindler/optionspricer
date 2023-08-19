import blackScholes
import monteCarlo
import matplotlib.pyplot as plt
import yfinance as yf

NUM_SIMS = 100
NUM_STEPS = 100

# Calculates the price of an option
# ticker: Stock ticker
# K: Strike Price
# T: Time to expiry
# r: risk free interest rate
def priceOption(ticker, K, T, r):
    stockData = yf.Ticker(ticker)
    initialPrice = stockData.history(period="1d")["Close"].iloc[0]

    # TEMP VALUES:
    drift = 0.05
    volatility = 0.2

    price = monteCarlo.monteCarloPrice(NUM_SIMS, initialPrice, K, drift, volatility, NUM_STEPS, T, r)
    print(price)




numPaths = 5
initialPrice = 1000
drift = .6
volatility = .2
T = 2
n = 10

paths = monteCarlo.generateSamplePaths(numPaths, initialPrice, drift, volatility, T, n)

for path in paths:
    plt.plot(path)
plt.show()