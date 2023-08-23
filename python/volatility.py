import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# rolling window: number of previous days to consider when calculating vol
def get_daily_historical_volatility(ticker, start_date, end_date, rolling_window):
    data = yf.download(ticker, start=start_date, end=end_date)

    # Calculate rolling volatility
    data['Daily_Return'] = data['Adj Close'].pct_change()
    data['Volatility'] = data['Daily_Return'].rolling(rolling_window).std()
    data['Annualized_Volatility'] = data['Volatility'] * np.sqrt(252)
    data = data.dropna() # Drop NaN values
    
    time_points = data.index
    annualized_volatilities = data['Annualized_Volatility'].values
    return time_points, annualized_volatilities

# rolling window: number of previous hours to consider when calculating vol
def get_hourly_volatility(stock_symbol, start_date, end_date, rolling_window):
    data = yf.download(stock_symbol, start=start_date, end=end_date, interval="1h")

    # Calculate rolling volatility for hours
    data['Hourly_Return'] = data['Adj Close'].pct_change()
    data['Volatility'] = data['Hourly_Return'].rolling(rolling_window).std()
    data = data.dropna() # Drop NaN values
    data['Annualized_Volatility'] = data['Volatility'] * np.sqrt(252 * 6.5) # 252 trading days 6.5 trading hours per day

    
    time_points = data.index
    annualized_volatilities = data['Annualized_Volatility'].values
    return time_points, annualized_volatilities

# calculates daily volatility using hours inside the day
def get_daily_volatility(stock_symbol, start_date, end_date):
    data = yf.download(stock_symbol, start=start_date, end=end_date, interval="1h")
    data['Hourly_Return'] = data['Adj Close'].pct_change()

    # Group data by date and calculate daily volatility for each trading day
    daily_volatility = data.groupby(data.index.date)['Hourly_Return'].std()
    annualized_volatility = daily_volatility * np.sqrt(252)

    return daily_volatility.index, annualized_volatility.values

time_points, annualized_volatilities = get_daily_volatility('GOOG', '2022-01-01', '2023-01-01')
plt.plot(time_points, annualized_volatilities)
plt.show()