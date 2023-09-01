from bs4 import BeautifulSoup
import numpy as np
import requests
import yfinance

# https://github.com/jknaudt21/Option-Scraper-BlackScholes/blob/master/Option%20Scraper.ipynb
def get_tickers():
    """Returns the tickers for all the S&P500 companies using the Wikipedia page
    Outputs: 
        tickers - list of tickers for every company in the S&P500
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find("table") # tickers are contained in a table
    tickers = []
    for row in table.find_all('tr'):
            cols = row.find_all('td')
            if cols:
                tickers.append(cols[0].text.strip())
    return tickers

# https://github.com/jknaudt21/Option-Scraper-BlackScholes/blob/master/Option%20Scraper.ipynb
def get_implied_vol(ticker):
    """Returns a stock's 30-day implied volatility from alphaqueries
    Inputs:
        ticker     - a string representing a stock's ticker
    Outputs: 
        volatility - implied volatility for the stock 
    """
    url = "https://www.alphaquery.com/stock/"+ ticker+ "/volatility-option-statistics/30-day/iv-mean"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find("table")
    rows = table.find_all('tr') 
    volatility = float(rows[5].find_all('td')[1].text.strip())
    return volatility

def get_historical_vol(ticker):
    """Returns a stock's 30-day historical volatility from alphaqueries
    Inputs:
        ticker     - a string representing a stock's ticker
    Outputs: 
        volatility - implied volatility for the stock 
    """
    url = "https://www.alphaquery.com/stock/"+ ticker+ "/volatility-option-statistics/30-day/historical-volatility"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find("table")
    rows = table.find_all('tr') 
    volatility = float(rows[5].find_all('td')[1].text.strip())
    return volatility

def price_european_option(call_or_put, paths, K, r, T):
    '''
    Finds discounted payoff of option using final prices of random walks
    call_or_put: whether option is call or put (string)
    paths: [num_paths][num_steps]
    K: strike price
    r: risk free interest rate
    T: time until expiry (years)
    Returns: mean payoff, mean payoff sample std, payoff sample std
    '''
    paths = np.array(paths)
    N = len(paths)
    if call_or_put == 'call':
        payoffs = np.maximum(0, paths[:,-1] - K)
    elif call_or_put == 'put':
        payoffs = np.maximum(0, K - paths[:,-1])
    else:
        print(f'Unusable value for call_or_put: {call_or_put}')
        return None, None, None
    # Discount payoffs to present value using risk free interest rate
    discounted_payoffs = payoffs * np.exp(-r*T)
    mean_payoff = np.mean(discounted_payoffs)
    payoff_sample_std = np.std(discounted_payoffs, ddof=1)
    mean_payoff_sample_std = payoff_sample_std / np.sqrt(N)
    return mean_payoff, mean_payoff_sample_std, payoff_sample_std

def longstaff_schwartz(paths, call_or_put, strike_price, r, T):
    """
    Longstaff-Schwartz American option pricing method.
    
    Args:
    paths (np.ndarray): Array of price paths. Each path should be an array of prices.
    call_or_put (str): 'call' for call option, 'put' for put option.
    strike_price (float): Strike price of the option.
    r (float): Risk-free interest rate.
    T (float): Time to maturity.

    Returns:
    float: American option price.
    """
    
    # Payoff given no continuation value
    if call_or_put == 'call':
        cashflow = np.maximum(paths[:, -1] - strike_price, 0)
    elif call_or_put == 'put':
        cashflow = np.maximum(strike_price - paths[:, -1], 0)

    # Iterate backwards through time steps
    for t in reversed(range(paths.shape[1] - 1)):
        prices = paths[:, t]
        if call_or_put == 'call':
            exercise_value = np.maximum(prices - strike_price, 0)
        elif call_or_put == 'put':
            exercise_value = np.maximum(strike_price - prices, 0)
      
        # Look at only in the money paths
        itm = exercise_value > 0
        if np.any(itm):
            # Fit a polynomial to estimate continuation value
            coefficients = np.polyfit(prices[itm], cashflow[itm] * np.exp(-r * (T - t)), 2)
            continuation_value = np.polyval(coefficients, prices)
            
            # Indices where it is optimal to exercise the option
            exercise_idx = itm & (exercise_value > continuation_value)
            
            # Update cashflows with early exercise
            cashflow[exercise_idx] = exercise_value[exercise_idx] * np.exp(-r * (T - t))
    
    # Calculate the present value of cashflows at time 0
    option_price = np.mean(cashflow) * np.exp(-r * T)
    
    return option_price