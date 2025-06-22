from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple, Optional, Dict, Any

@dataclass
class TickerData:
    ticker: str
    price: float  # current price of stock
    volatility: float  # std of daily log returns
    dividend_schedule: Optional[Dict[str, Any]]  # dividend forecast data
    last_price_update: Optional[str] = None  # Changed to string for JSON serialization
    last_dividend_update: Optional[str] = None  # Changed to string for JSON serialization

@dataclass
class CacheConfig:
    price_cache_days: int = 1  # How many days to cache price data
    dividend_cache_days: int = 30  # How many days to cache dividend data
    volatility_cache_days: int = 7  # How many days to cache volatility data

@dataclass
class APILimits:
    alphavantage_daily_limit: int = 500
    twelve_data_daily_limit: int = 800
    current_alphavantage_usage: int = 0
    current_twelve_usage: int = 0

