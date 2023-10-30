from black_scholes import black_scholes
from longstaff_schwartz import longstaff_schwartz
from utils import get_historical_volatility, get_dividend_days, get_dividend_present_val
from heston_model import generate_paths
from black_scholes import price_european_option
import yfinance as yf

def price_option(call_or_put, ticker, K, T, n):
    '''
    Prices an option for the specified ticker using multiple models

    call_or_put: whether option is call or put (string)
    ticker: Stock ticker
    K: Strike Price
    T: Time to expiry (years)
    n: num simulations
    Returns: American Options Price, European Options Price, List of Paths, Price Standard Deviations
    '''
    stock_data = yf.Ticker(ticker)
    dividend_data = stock_data.dividends
    
    initial_price = stock_data.history(period='1d')['Close'].iloc[0]
    volatility = get_historical_volatility(ticker, 10)
    theta = volatility ** 2 # long term mean of variance

    # TEMP VALUES
    vol_of_vol = 0.3
    rho = -0.7 # brownian motion correlations
    r = 0.041 # risk free interest rate
    kappa = 5 # variance reversion rate
    
    dividend_days = get_dividend_days(dividend_data, T)
    dividend_present_val = get_dividend_present_val(dividend_days, T, r)

    # Drift set to risk free interest rate (risk neutral pricing)
    time_points, heston_paths = generate_paths(n, initial_price, r, volatility, T, kappa, vol_of_vol, theta, rho, dividend_days)
    us_price, us_price_std = longstaff_schwartz(heston_paths, K, r, T, call_or_put, dividend_present_val)
    eu_price, eu_price_std = price_european_option(call_or_put, heston_paths, K, r, T)
    return us_price, eu_price, heston_paths.tolist(), us_price_std, eu_price_std, volatility, dividend_days

#us_price, eu_price, heston_paths, us_price_std, eu_price_std = price_option('call', 'msft', 120, 1, 100000)