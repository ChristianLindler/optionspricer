import os
from supabase.client import create_client, Client
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from .schema import TickerData, CacheConfig, APILimits
from .providers.alphavantage_provider import AlphaVantageProvider
from .providers.twelve_provider import TwelveProvider
from .volatility_estimator import compute_std_of_log_returns
from .dividend_forecaster import forecast_dividend_schedule

# Get configuration from environment variables
ALPHAVANTAGE_API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')
TWELVE_API_KEY = os.getenv('TWELVE_API_KEY')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Validate required API keys
if not ALPHAVANTAGE_API_KEY:
    raise ValueError("ALPHAVANTAGE_API_KEY is required. Set it as an environment variable.")
if not TWELVE_API_KEY:
    raise ValueError("TWELVE_API_KEY is required. Set it as an environment variable.")
if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL is required. Set it as an environment variable.")
if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY is required. Set it as an environment variable.")

# Initialize clients
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
twelve_provider = TwelveProvider(TWELVE_API_KEY)
alphavantage_provider = AlphaVantageProvider(ALPHAVANTAGE_API_KEY)

# Configuration
cache_config = CacheConfig()
api_limits = APILimits()

def get_stock_data(ticker: str) -> TickerData:
    """Get stock data with caching"""
    ticker = ticker.upper()
    now = datetime.now()
    
    print(f"Fetching data for {ticker}...")
    
    # Try to fetch from cache
    cached_data = _get_cached_data(ticker)
    if cached_data:
        print(f"Found cached data for {ticker}")
    else:
        print(f"No cached data found for {ticker}, will fetch fresh data")
    
    # Determine what needs updating
    needs_price_update = _is_price_stale(cached_data, now)
    needs_dividend_update = _is_dividend_stale(cached_data, now)
    
    print(f"Price update needed: {needs_price_update}")
    print(f"Dividend update needed: {needs_dividend_update}")
    
    # Check API limits
    if needs_price_update and api_limits.current_twelve_usage >= api_limits.twelve_data_daily_limit:
        needs_price_update = False
        print("Price update skipped due to API limit")
        
    if needs_dividend_update and api_limits.current_alphavantage_usage >= api_limits.alphavantage_daily_limit:
        needs_dividend_update = False
        print("Dividend update skipped due to API limit")
    
    # Get current data (from cache or fresh)
    current_price = cached_data.get("price") if cached_data and cached_data.get("price") is not None else 0.0
    volatility = cached_data.get("volatility") if cached_data and cached_data.get("volatility") is not None else 0.0
    dividend_schedule = cached_data.get("dividend_json") if cached_data else None
    
    # Fetch fresh data if needed
    if needs_price_update:
        try:
            print(f"Fetching price data for {ticker} from Twelve Data...")
            prices = twelve_provider.get_closing_prices(ticker)
            current_price = prices[-1][1]
            volatility = compute_std_of_log_returns(prices)
            api_limits.current_twelve_usage += 1
            print(f"Price data fetched: ${current_price:.2f}, Volatility: {volatility:.4f}")
        except Exception as e:
            print(f"Error fetching price data: {e}")
            if not cached_data:
                raise RuntimeError(f"No cached data available for {ticker}")
    
    if needs_dividend_update:
        try:
            print(f"Fetching dividend data for {ticker} from Alpha Vantage...")
            raw_divs = alphavantage_provider.get_dividend_data(ticker)
            dividend_schedule = forecast_dividend_schedule(raw_divs)
            api_limits.current_alphavantage_usage += 1
            print(f"Dividend data fetched: {len(dividend_schedule.get('schedule', []))} dividends with valid dates")
            if dividend_schedule.get('schedule'):
                print("Caching dividend schedule:")
                for i, (date, amount) in enumerate(dividend_schedule['schedule']):
                    print(f"  {i+1}. {date}: ${amount:.4f}")
        except Exception as e:
            print(f"Error fetching dividend data: {e}")
            if not cached_data:
                raise RuntimeError(f"No cached data available for {ticker}")
    
    # Update cache
    last_price_update = now.isoformat() if needs_price_update else (cached_data.get("last_price_update") if cached_data else None)
    last_dividend_update = now.isoformat() if needs_dividend_update else (cached_data.get("last_dividend_update") if cached_data else None)
    
    print(f"Updating cache for {ticker}...")
    _upsert_stock_data(
        ticker=ticker,
        price=float(current_price) if current_price is not None else 0.0,
        volatility=float(volatility) if volatility is not None else 0.0,
        dividend_schedule=dividend_schedule if isinstance(dividend_schedule, dict) else {},
        last_price_update=last_price_update,
        last_dividend_update=last_dividend_update
    )
    
    return TickerData(
        ticker=ticker,
        price=current_price if current_price is not None else 0.0,
        volatility=volatility if volatility is not None else 0.0,
        dividend_schedule=dividend_schedule if isinstance(dividend_schedule, dict) or dividend_schedule is None else {},
        last_price_update=last_price_update if isinstance(last_price_update, str) or last_price_update is None else str(last_price_update),
        last_dividend_update=last_dividend_update if isinstance(last_dividend_update, str) or last_dividend_update is None else str(last_dividend_update)
    )

def _get_cached_data(ticker: str) -> Optional[Dict[str, Any]]:
    """Fetch data from Supabase cache"""
    try:
        result = (supabase.table("stock_data")
                 .select("*")
                 .eq("ticker", ticker.lower())
                 .single()
                 .execute())
        return result.data
    except:
        return None

def _is_price_stale(cached_data: Optional[Dict[str, Any]], now: datetime) -> bool:
    """Check if price data is stale"""
    if not cached_data or not cached_data.get("last_price_update"):
        return True
    last_update = datetime.fromisoformat(cached_data["last_price_update"])
    return (now - last_update) > timedelta(days=cache_config.price_cache_days)

def _is_dividend_stale(cached_data: Optional[Dict[str, Any]], now: datetime) -> bool:
    """Check if dividend data is stale"""
    if not cached_data or not cached_data.get("dividend_json") or not cached_data.get("last_dividend_update"):
        return True
    last_update = datetime.fromisoformat(cached_data["last_dividend_update"])
    return (now - last_update) > timedelta(days=cache_config.dividend_cache_days)

def _upsert_stock_data(ticker: str, price: float, volatility: float, 
                      dividend_schedule: Dict[str, Any], last_price_update, 
                      last_dividend_update) -> Dict[str, Any]:
    """Upsert stock data to Supabase"""
    if isinstance(last_price_update, datetime):
        last_price_update = last_price_update.isoformat()
    if isinstance(last_dividend_update, datetime):
        last_dividend_update = last_dividend_update.isoformat()
    
    data = {
        "ticker": ticker.lower(),
        "price": price,
        "volatility": volatility,
        "dividend_json": dividend_schedule,
        "last_price_update": last_price_update,
        "last_dividend_update": last_dividend_update,
    }
    
    try:
        result = supabase.table("stock_data").upsert(data).execute()
        return result.data[0] if result.data else {}
    except Exception as e:
        raise

def get_api_usage_stats() -> Dict[str, int]:
    """Get current API usage statistics"""
    return {
        "alphavantage_used": api_limits.current_alphavantage_usage,
        "alphavantage_limit": api_limits.alphavantage_daily_limit,
        "twelve_data_used": api_limits.current_twelve_usage,
        "twelve_data_limit": api_limits.twelve_data_daily_limit
    }

def reset_daily_usage():
    """Reset daily API usage counters"""
    api_limits.current_alphavantage_usage = 0
    api_limits.current_twelve_usage = 0 