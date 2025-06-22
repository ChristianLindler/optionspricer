"""
Dividend forecasting and scheduling for options pricing.
Parses dividend data from AlphaVantage and forecasts future payments.
"""

from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Any
import numpy as np


def forecast_dividend_schedule(dividend_data, years=3):
    """
    Parse AlphaVantage dividend data and forecast future payments.
    
    Extracts the last 4 dividend payments and forecasts future dividends
    based on historical patterns. Calculates present value and yield metrics.
    
    Args:
        dividend_data: Raw dividend data from AlphaVantage API
        years: Forecast horizon in years (default: 3)
        
    Returns:
        Dictionary containing:
        - schedule: List of (date, amount) tuples (most recent first)
        - present_value: Present value of future dividends
        - annual_yield: Estimated annual dividend yield
        - next_dividend_date: Predicted next dividend date
        - next_dividend_amount: Predicted next dividend amount
        - forecast_method: Method used for forecasting
    """
    schedule = []
    
    # Parse AlphaVantage DIVIDENDS endpoint format
    if 'data' in dividend_data and isinstance(dividend_data['data'], list):
        # Filter valid dividends (no None dates, positive amounts)
        valid_dividends = [
            (div.get('payment_date'), float(div.get('amount', 0.0)))
            for div in dividend_data['data']
            if div.get('payment_date') and div.get('amount') and div.get('payment_date') != 'None'
        ]
        # Sort by date descending (most recent first)
        valid_dividends.sort(key=lambda x: x[0], reverse=True)
        # Keep only the last 4
        schedule = valid_dividends[:4]
    
    # Calculate forecast metrics
    present_value = 0.0
    annual_yield = 0.0
    next_dividend_date = None
    next_dividend_amount = 0.0
    
    if schedule:
        # Calculate average dividend amount
        avg_dividend = sum(amount for _, amount in schedule) / len(schedule)
        
        # Estimate dividend frequency from historical data
        if len(schedule) >= 2:
            # Calculate average time between dividends
            dates = [datetime.strptime(date, '%Y-%m-%d') for date, _ in schedule]
            intervals = []
            for i in range(len(dates) - 1):
                interval = (dates[i] - dates[i + 1]).days
                intervals.append(interval)
            avg_interval = sum(intervals) / len(intervals)
            
            # Predict next dividend date
            last_date = datetime.strptime(schedule[0][0], '%Y-%m-%d')
            next_date = last_date + timedelta(days=avg_interval)
            next_dividend_date = next_date.strftime('%Y-%m-%d')
            next_dividend_amount = avg_dividend
            
            # Calculate annual yield (rough estimate)
            estimated_price = 100.0  # Placeholder for actual stock price
            annual_yield = (avg_dividend * (365 / avg_interval)) / estimated_price
            
            # Calculate present value of next dividend
            risk_free_rate = 0.0438  # Current risk-free rate
            time_to_next = avg_interval / 365.0
            present_value = avg_dividend * np.exp(-risk_free_rate * time_to_next)
    
    return {
        'schedule': schedule,
        'present_value': present_value,
        'annual_yield': annual_yield,
        'next_dividend_date': next_dividend_date,
        'next_dividend_amount': next_dividend_amount,
        'forecast_method': 'alphavantage_last4_forecast'
    }


def calculate_dividend_present_value(dividend_schedule, risk_free_rate):
    """
    Calculate present value of dividend schedule.
    
    Args:
        dividend_schedule: List of (date, amount) tuples
        risk_free_rate: Risk-free interest rate for discounting
        
    Returns:
        float: Present value of all future dividends
    """
    if not dividend_schedule:
        return 0.0
    
    present_value = 0.0
    for date_str, amount in dividend_schedule:
        try:
            dividend_date = datetime.strptime(date_str, '%Y-%m-%d')
            current_date = datetime.now()
            time_to_dividend = (dividend_date - current_date).days / 365.0
            
            if time_to_dividend > 0:
                present_value += amount * np.exp(-risk_free_rate * time_to_dividend)
        except ValueError:
            continue
    
    return present_value


def is_trading_day(date):
    """
    Simple check if a date is a trading day (Monday-Friday).
    In a production system, this would use a proper calendar.
    
    Args:
        date: datetime object
        
    Returns:
        bool: True if it's a trading day
    """
    return date.weekday() < 5  # Monday = 0, Friday = 4


def get_next_trading_day(date):
    """
    Get the next trading day from a given date.
    
    Args:
        date: datetime object
        
    Returns:
        datetime: Next trading day
    """
    next_day = date + timedelta(days=1)
    while not is_trading_day(next_day):
        next_day += timedelta(days=1)
    return next_day


def get_dividend_array_for_pricing(dividend_schedule, time_to_expiry, trading_days_per_year=252):
    """
    Create dividend array for pricing models.
    
    Maps dividend schedule to trading days for use in Monte Carlo simulation.
    Dividends are applied on the ex-dividend date (typically 1-2 days before payment).
    
    Args:
        dividend_schedule: List of (date, amount) tuples (most recent first)
        time_to_expiry: Time to expiry in years
        trading_days_per_year: Number of trading days per year
        
    Returns:
        np.ndarray: Dividend amounts for each trading day
    """
    num_trading_days = int(time_to_expiry * trading_days_per_year)
    dividend_array = np.zeros(num_trading_days)
    
    if not dividend_schedule:
        return dividend_array
    
    current_date = datetime.now()
    
    # Get future dividends that fall within the option period
    future_dividends = []
    for date_str, amount in dividend_schedule:
        try:
            dividend_date = datetime.strptime(date_str, '%Y-%m-%d')
            # If dividend date is in the future and within option period
            if dividend_date > current_date:
                days_to_dividend = (dividend_date - current_date).days
                if days_to_dividend <= time_to_expiry * 365:  # Within option period
                    future_dividends.append((dividend_date, amount))
        except ValueError:
            continue
    
    # Sort by date (earliest first)
    future_dividends.sort(key=lambda x: x[0])
    
    # Map dividends to trading days
    for dividend_date, amount in future_dividends:
        # Calculate trading days from start
        days_from_start = (dividend_date - current_date).days
        trading_day_index = int(days_from_start * trading_days_per_year / 365)
        
        # Ensure the index is within bounds
        if 0 <= trading_day_index < num_trading_days:
            # Apply dividend on the ex-dividend date
            dividend_array[trading_day_index] = amount
    
    return dividend_array


def get_option_period_dividends(dividend_schedule, time_to_expiry):
    """
    Get dividend information specifically for the option period.
    
    For pricing purposes, we forecast dividends based on historical patterns
    throughout the entire option period, ignoring any scheduled dividends.
    
    Args:
        dividend_schedule: List of (date, amount) tuples (most recent first)
        time_to_expiry: Time to expiry in years
        
    Returns:
        Dictionary containing:
        - dividends_in_period: List of (date, amount) tuples for dividends during option period
        - total_dividends: Total dividend amount during option period
        - num_dividends: Number of dividends during option period
        - forecast_dividends: List of forecasted dividends (same as dividends_in_period)
    """
    if not dividend_schedule:
        return {
            'dividends_in_period': [],
            'total_dividends': 0.0,
            'num_dividends': 0,
            'forecast_dividends': []
        }
    
    current_date = datetime.now()
    option_end_date = current_date + timedelta(days=int(time_to_expiry * 365))
    
    # Always forecast dividends based on historical patterns, ignore scheduled dividends
    forecast_dividends = []
    
    if len(dividend_schedule) >= 2:
        # Calculate average dividend amount and frequency from historical data
        avg_amount = sum(amount for _, amount in dividend_schedule) / len(dividend_schedule)
        
        # Calculate average interval between dividends
        dates = [datetime.strptime(date, '%Y-%m-%d') for date, _ in dividend_schedule]
        intervals = []
        for i in range(len(dates) - 1):
            interval = (dates[i] - dates[i + 1]).days
            intervals.append(interval)
        avg_interval = sum(intervals) / len(intervals) if intervals else 90  # Default to quarterly
        
        # Start forecasting from the most recent dividend date
        last_known_date = max(dates)
        forecast_date = last_known_date
        
        # Generate dividends throughout the option period
        while forecast_date <= option_end_date:
            forecast_date += timedelta(days=avg_interval)
            if current_date < forecast_date <= option_end_date:
                forecast_dividends.append((forecast_date.strftime('%Y-%m-%d'), avg_amount))
    
    # Calculate totals
    total_dividends = sum(amount for _, amount in forecast_dividends)
    num_dividends = len(forecast_dividends)
    
    return {
        'dividends_in_period': forecast_dividends,  # Use forecasted dividends as the main list
        'total_dividends': total_dividends,
        'num_dividends': num_dividends,
        'forecast_dividends': forecast_dividends  # Keep for backward compatibility
    }

