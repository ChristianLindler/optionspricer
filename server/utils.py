import numpy as np
import yfinance as yf
from datetime import datetime
from pytz import utc
import numpy as np
import matplotlib.pyplot as plt

NUM_TRADING_DAYS = 252

def get_dividend_days(dividend_data, T):
    '''
    Formats the dividend paid on each day

    dividends: yahoo finance dividend data for a stock
    T: time to expiry (years)
    Returns: divdend[] such that dividend[i] = dividend paid on ith trading day
    '''
    num_days = int(T * NUM_TRADING_DAYS) + 1

    if len(dividend_data) < 2:
        return [0] * num_days

    # Use the past two dividend payments to determine dividend rate and value
    today = datetime.now(utc)
    last_dividend_date = dividend_data.index[-1].replace(tzinfo=utc)
    second_last_dividend_date = dividend_data.index[-2].replace(tzinfo=utc)
    last_dividend = dividend_data.iloc[-1]
    second_last_dividend = dividend_data.iloc[-2]

    average_payment = (last_dividend + second_last_dividend) / 2.0
    days_between_payments = (last_dividend_date - second_last_dividend_date).days
    days_until_payment = days_between_payments - (today - last_dividend_date).days

    # Generates array 'dividends' which is the dividend payment on each day (usually 0)
    curr_day = days_until_payment
    dividends = [0] * num_days
    while curr_day < num_days:
        dividends[curr_day] = average_payment
        curr_day += days_between_payments
    
    return dividends

def get_dividend_present_val(dividend_days, T, r):
    '''
    Discounts the value of the future dividends to present value

    dividend_days[]: dividend_days[i] = dividend paid on ith trading day
    T: time to expiry (years)
    r: risk free interest rate
    Returns: discounted_price[] such that discounted_price[i] = present dollar value of future dividend payments
    '''
    num_days = int(T * NUM_TRADING_DAYS) + 1

    # Steps backwards through days, discounting the prior day's dividend payoff and adding the dividend payoff on that day
    discounted_payment = [0] * (num_days - 1)
    df = np.exp(-r * 1/NUM_TRADING_DAYS)
    discounted_payment[-1] = dividend_days[-1]
    for i in reversed(range(len(discounted_payment) - 2)):
        discounted_payment[i] = df * discounted_payment[i + 1] + dividend_days[i]
    
    '''
    plt.plot(range(len(discounted_payment)), discounted_payment, marker='o')
    plt.title("Discounted Dividend Payments Over Time")
    plt.xlabel("Time (days)")
    plt.ylabel("Discounted Payment")
    plt.grid(True)
    plt.show()
    '''
    
    return np.array(discounted_payment)

def get_historical_volatility(ticker, num_days):
    '''
    ticker: Stock ticker
    numDays: number of days incorporate for the calculation
    Returns: annualized historical volatility
    '''
    stock_data = yf.download(ticker)
    stock_data = stock_data.sort_values(by='Date', ascending=False).head(num_days)
    stock_data['Daily_Returns'] = stock_data['Adj Close'].pct_change()
    return np.std(stock_data['Daily_Returns']) * np.sqrt(252)