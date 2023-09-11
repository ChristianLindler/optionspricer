# pylint: disable=C0114

from black_scholes import black_scholes
from monte_carlo import generate_paths
from options import longstaff_schwartz, get_implied_vol, price_european_option
import yfinance as yf
import numpy as np

NUM_STEPS = 100

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
    
    volatility = get_implied_vol(ticker)
    theta = volatility ** 2 # long term mean of variance

    # TEMP VALUES
    vol_of_vol = 0.3
    rho = -0.7 # brownian motion correlations
    r = 0.041 # risk free interest rate
    kappa = 5 # variance reversion rate
    dt = T/NUM_STEPS

    # Drift set to risk free interest rate (risk neutral pricing)
    time_points, heston_paths = generate_paths(n, initial_price, r, volatility, NUM_STEPS, T, kappa, vol_of_vol, theta, rho)
    us_price, us_price_std = longstaff_schwartz(heston_paths, K, r, T, call_or_put)
    eu_price, eu_price_std, discounted_payoff_std = price_european_option(call_or_put, heston_paths, K, r, T)
    
    return us_price, eu_price, heston_paths.tolist(), us_price_std, discounted_payoff_std

    
# price_option('call', 'GOOG', 125, 3, 10000)
