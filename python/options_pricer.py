# pylint: disable=C0114

from black_scholes import black_scholes
from monte_carlo import generate_paths, monte_carlo_price
import yfinance as yf
import numpy as np

NUM_STEPS = 100

def vol_dynamics(previous_prices, current_prices, previous_vol, vcr=-11):
    return

def get_historical_volatility(ticker, num_days):
    '''
    ticker: Stock ticker
    numDays: number of days incorporate for the calculation
    Returns: annualized historical volatility
    '''
    stock_data = yf.download(ticker)
    stock_data = stock_data.sort_values(by='Date', ascending=False).head(num_days)
    stock_data['Daily_Returns'] = stock_data['Adj Close'].pct_change()
    # Calculate annualized historical volatility
    return np.std(stock_data['Daily_Returns']) * np.sqrt(252)

def price_option(call_or_put, ticker, K, T, n):
    '''
    call_or_put: whether option is call or put (string)
    ticker: Stock ticker
    K: Strike Price
    T: Time to expiry
    n: num simulations
    Returns: price of option
    '''
    stock_data = yf.Ticker(ticker)
    initial_price = stock_data.history(period='1d')['Close'].iloc[0]
    print('initial price', initial_price)
    
    # TEMP VALUES
    volatility = get_historical_volatility(ticker, 30)
    theta = volatility ** 2 # long term mean of variance
    vol_of_vol = 0.3
    rho = -0.7 # brownian motion correlations
    r = 0.03 # risk free interest rate
    kappa = 50 # variance reversion rate

    # Drift set to risk free interest rate (risk neutral pricing)
    time_points, heston_paths = generate_paths(n, initial_price, r, volatility, NUM_STEPS, T, kappa, vol_of_vol, theta, rho)
    heston_price, heston_price_std, heston_payoff_std = monte_carlo_price(call_or_put, heston_paths, K, r, T)
    bs_price = black_scholes(call_or_put, initial_price, K, T, volatility, r)
    print(f'HS: {heston_price:.3f}, Price STD: {heston_price_std:.3f}, Payoff STD: {heston_payoff_std:.3f}')
    print('BS:', bs_price)

    return heston_price, heston_paths.tolist(), heston_price_std, heston_payoff_std, bs_price

    #visualize_paths(time_points, heston_paths, K)
    
#price_option('call', 'GOOG', 125, 3, 10000)
#print(get_historical_volatility('GOOG', 30))
