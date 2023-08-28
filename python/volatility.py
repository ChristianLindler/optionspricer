# pylint: disable=C0114

import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

def get_daily_historical_volatility(ticker, start_date, end_date, rolling_window):
    """
    ticker: Stock ticker
    start_date: start date for historical volatility calculation
    end_date: end date for historical volatility calculation
    rolling_window: number of previous days to consider when calculating volatility
    Returns: time_points, annualized_volatilities
    """
    start_fetch_date = pd.Timestamp(start_date) - pd.DateOffset(days=2 * rolling_window) # Adjust bc not every day is a trading day
    data = yf.download(ticker, start=start_fetch_date, end=end_date)

    # Calculate rolling volatility
    data['Daily_Return'] = data['Adj Close'].pct_change()
    data['Log_Return'] = np.log(data['Adj Close'] / data['Adj Close'].shift(1))
    data['Volatility'] = data['Log_Return'].rolling(rolling_window).std()
    data['Annualized_Volatility'] = data['Volatility'] * np.sqrt(252)
    data = data.dropna() # Drop NaN values
    data = data[data.index >= pd.Timestamp(start_date)] # removes days before start_date that were downloaded for calculations
    time_points = data.index
    annualized_volatilities = data['Annualized_Volatility'].values
    print(data['Annualized_Volatility'])
    return time_points, annualized_volatilities

time_points, annualized_volatilities = get_daily_historical_volatility(
    'GOOG', '2023-08-01', '2023-08-23', 30)
plt.plot(time_points, annualized_volatilities)
plt.show()
