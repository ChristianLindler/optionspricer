from bs4 import BeautifulSoup
import numpy as np
import requests

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




# https://www.youtube.com/watch?v=--Il6rgtVjM
# https://github.com/cantaro86/Financial-Models-Numerical-Methods/blob/master/2.3%20American%20Options.ipynb
# https://people.math.ethz.ch/~hjfurrer/teaching/LongstaffSchwartzAmericanOptionsLeastSquareMonteCarlo.pdf
def longstaff_schwartz(S, K, r, T, option_type='call'):
    """
    Longstaff-Schwartz American option pricing method for call or put options.
    
    Args:
    S (np.ndarray): Price matrix, where each row represents a price path.
    K (float): Strike price of the option.
    r (float): Risk-free interest rate.
    T (float): Time to maturity.
    option_type (str): 'call' for call option or 'put' for put option.
    
    Returns:dt = T / (N - 1)
    float: American option price.
    """

    num_sims, num_steps = S.shape
    dt = T / (num_steps - 1)  # time interval
    df = np.exp(-r * dt)  # discount factor per time interval
    
    if option_type == 'put':
        exercise_value = np.maximum(K - S, 0)  # intrinsic values for put option
    elif option_type == 'call':
        exercise_value = np.maximum(S - K, 0)  # intrinsic values for call option
    else:
        raise ValueError("Invalid option_type. Use 'put' or 'call'.")

    cashflow = np.zeros_like(exercise_value)
    cashflow[:, -1] = exercise_value[:, -1] # No continuation value on final day, so set it equal to exercise value

    # Valuation by LS Method
    for t in range(num_steps - 2, -1, -1):
        itm = exercise_value[:, t] > 0 # matrix set to true where it is in the money
        exercise = np.zeros(len(itm), dtype=bool) # array initially set to false for where we wille exercise

        if np.count_nonzero(itm) > 0:
            regression = np.polyfit(S[itm, t], cashflow[itm, t + 1] * df, 2)
            continuation_value = np.polyval(regression, S[itm, t])
        else:
            continuation_value = np.zeros(S[itm, t])
        
        # paths where it is optimal to exercise
        exercise[itm] = exercise_value[itm, t] > continuation_value

        cashflow[exercise, t] = exercise_value[exercise, t]  # set V equal to H where it is optimal to exercise
        cashflow[exercise, t + 1 :] = 0  # set future cash flows, for that path, equal to zero
        discount_path = cashflow[:, t] == 0  # paths where we didn't exercise
        cashflow[discount_path, t] = cashflow[discount_path, t + 1] * df  # set V[t] in continuation region

    
    # discounted expectation of V[t=0]
    option_price = np.mean(cashflow[:, 0])
    price_std = np.std(cashflow[:, 0], ddof=1)

    return option_price, price_std

