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
    Returns: American Options Price, European Options Price, List of Paths, Price Standard Errors
    '''
    stock_data = yf.Ticker(ticker)
    dividend_data = stock_data.dividends
    
    initial_price = stock_data.history(period='1d')['Close'].iloc[0]
    volatility = get_historical_volatility(ticker, 10)
    theta = volatility ** 2 # long term mean of variance

    # TEMP VALUES
    vol_of_vol = 0.2
    rho = -0.7 # brownian motion correlations
    r = 0.041 # risk free interest rate (drift for risk neutral pricing)
    kappa = 5 # variance reversion rate
    
    dividend_days = get_dividend_days(dividend_data, T)
    dividend_present_val = get_dividend_present_val(dividend_days, T, r)

    time_points, heston_paths = generate_paths(n, initial_price, r, volatility, T, kappa, vol_of_vol, theta, rho, dividend_days)
    us_price, us_se = longstaff_schwartz(heston_paths, K, r, T, call_or_put, dividend_present_val)
    eu_price, eu_se = price_european_option(call_or_put, heston_paths, K, r, T)
    return us_price, eu_price, heston_paths.tolist(), us_se, eu_se, volatility, dividend_days


'''
us_price, eu_price, heston_paths, us_se, eu_se, vol, div = price_option('call', 'VZ', 30, 1, 100000)

print(f'us_price={us_price}')
print(f'eu_price={eu_price}')
print(f'us standard error={eu_se}')
'''
