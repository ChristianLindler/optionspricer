import blackScholes
import monteCarlo
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np

NUM_SIMS = 100
NUM_STEPS = 1000

def vol_dynamics(previous_prices, current_prices, previous_vol, vcr=-11):
    return

# Calculates historical volatility for a stock
# ticker: Stock ticker
# numDays: number of days incorporate for the calculation
def get_historical_volatility(ticker, num_days):
    stock_data = yf.download(ticker)
    stock_data = stock_data.sort_values(by='Date', ascending=False).head(num_days)
    stock_data['Daily_Returns'] = stock_data['Adj Close'].pct_change()
    # Calculate annualized historical volatility
    return np.std(stock_data['Daily_Returns']) * np.sqrt(252)


# Calculates the price of an option
# ticker: Stock ticker
# K: Strike Price
# T: Time to expiry
# r: risk free interest rate
# kappa: volatility mean reversion rate
def price_option(call_or_put, ticker, K, T, r, kappa):
    stock_data = yf.Ticker(ticker)
    initial_price = stock_data.history(period="1d")["Close"].iloc[0]
    print('initial price', initial_price)
    
    # TEMP VALUES
    volatility = get_historical_volatility(ticker)
    theta = volatility ** 2
    vol_of_vol = 0.3

    # Drift set to risk free interest rate (risk neutral pricing)
    time_points, paths = monteCarlo.generate_paths(NUM_SIMS, initial_price, r, volatility, NUM_STEPS, T, kappa, vol_of_vol, theta)
    mc_price = monteCarlo.monte_carlo_price(call_or_put, paths, K, r, T)
    bc_price = blackScholes.black_scholes(call_or_put, initial_price, K, T, volatility, r)
    print('MC:', mc_price)
    print('BS:', bc_price)

    for path in paths:
        plt.plot(time_points, path)
    plt.show()
    

#priceOption('call', 'GOOG', 125, 3, 0.03, 3)
print(get_historical_volatility('GOOG', 30))