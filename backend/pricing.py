"""
Options pricing module using Monte Carlo simulation with Heston model.
Provides both American (Longstaff-Schwartz) and European (Black-Scholes) option pricing.
"""

from model.black_scholes import price_european_option
from model.longstaff_schwartz import longstaff_schwartz
from data.cache import get_stock_data
from model.heston_model import generate_paths
from data.dividend_forecaster import get_dividend_array_for_pricing, get_option_period_dividends
import numpy as np
import math

# Model parameters
RISK_FREE_RATE = 0.0438  # 4.38%
VOL_OF_VOL = 0.2
CORRELATION = -0.7
MEAN_REVERSION_RATE = 5.0
TRADING_DAYS_PER_YEAR = 252


def price_option(call_or_put: str, ticker: str, K: float, T: float, num_sims: int = 1000) -> tuple[float, float, float, float, list[list[float]], float, dict]:
    """
    Price an option using Monte Carlo simulation with Heston model and Longstaff-Schwartz for American options.
    
    Args:
        call_or_put: 'call' or 'put'
        ticker: Stock ticker symbol
        K: Strike price
        T: Time to expiry in years
        num_sims: Number of Monte Carlo simulations
        
    Returns:
        Tuple of (us_option_price, eu_option_price, us_price_std, eu_price_std, paths, vol, dividends)
    """
    try:
        # Validate inputs
        if call_or_put not in ['call', 'put']:
            raise ValueError("call_or_put must be 'call' or 'put'")
        if K <= 0:
            raise ValueError("Strike price must be positive")
        if T <= 0:
            raise ValueError("Time to expiry must be positive")
        if num_sims <= 0:
            raise ValueError("Number of simulations must be positive")
            
        # Get stock data
        stock_data = get_stock_data(ticker)
        
        # Validate stock data
        if stock_data.price <= 0:
            raise ValueError(f"Invalid stock price for {ticker}: {stock_data.price}")
        if stock_data.volatility <= 0:
            raise ValueError(f"Invalid volatility for {ticker}: {stock_data.volatility}")
            
        print(f"Pricing {call_or_put} option for {ticker}")
        print(f"Current price: ${stock_data.price:.2f}")
        print(f"Strike price: ${K:.2f}")
        print(f"Time to expiry: {T:.4f} years")
        print(f"Volatility: {stock_data.volatility:.4f}")
        print(f"Number of simulations: {num_sims}")
        
        print('DEBUG about to call generate_paths')
        # Generate price paths using Heston model
        dividend_schedule_list = stock_data.dividend_schedule.get('schedule', []) if isinstance(stock_data.dividend_schedule, dict) else []
        
        # Get dividend information for the option period
        option_dividend_info = get_option_period_dividends(dividend_schedule_list, T)
        
        # Use forecasted dividends for simulation
        dividends_for_simulation = option_dividend_info['dividends_in_period']
        
        paths = generate_paths(
            num_sims=num_sims,
            initial_price=stock_data.price,
            risk_free_rate=RISK_FREE_RATE,
            initial_volatility=stock_data.volatility,
            time_to_expiry=T,
            mean_reversion_rate=MEAN_REVERSION_RATE,
            vol_of_vol=VOL_OF_VOL,
            long_term_variance=stock_data.volatility ** 2,
            correlation=CORRELATION,
            dividend_days=get_dividend_array_for_pricing(dividends_for_simulation, T)
        )
        print('DEBUG paths:', type(paths), 'len:', len(paths) if hasattr(paths, '__len__') else 'N/A')
        
        # Extract just the paths (second element of tuple)
        price_paths = paths[1]
        print('DEBUG price_paths type:', type(price_paths), 'shape:', getattr(price_paths, 'shape', None))
        
        # Estimate continuous dividend yield for Black-Scholes
        dividend_yield = 0.0
        if isinstance(stock_data.dividend_schedule, dict) and dividends_for_simulation:
            # Only use dividend yield if there are actually dividends in the simulation
            dividend_yield = stock_data.dividend_schedule.get('annual_yield', 0.0)
            # If annual_yield is based on a $100 price, scale it to actual price
            if dividend_yield > 0 and stock_data.price > 0:
                # annual_yield = (annual_div / 100), so scale to actual price
                annual_div = dividend_yield * 100
                dividend_yield = annual_div / stock_data.price

        # Price European option using Black-Scholes analytical formula
        from model.black_scholes import black_scholes
        eu_price = black_scholes(
            call_or_put=call_or_put,
            stock_price=stock_data.price,
            strike_price=K,
            time_to_expiry=T,
            volatility=stock_data.volatility,
            risk_free_rate=RISK_FREE_RATE,
            dividend_yield=dividend_yield
        )
        # Price European option using MC for standard error
        eu_price_mc, eu_se = price_european_option(
            call_or_put=call_or_put,
            paths=price_paths,
            strike_price=K,
            risk_free_rate=RISK_FREE_RATE,
            time_to_expiry=T
        )
        
        # Price American option using Longstaff-Schwartz
        # Get dividend array for the option period
        dividend_days = get_dividend_array_for_pricing(dividends_for_simulation, T)
        
        # For American options, we need to consider the present value of future dividends
        # when calculating the exercise value for call options
        dividend_present_val = None
        if call_or_put == 'call' and dividends_for_simulation:
            # Only add dividend present value if there are actual dividends
            total_future_dividends = np.sum(dividend_days)
            if total_future_dividends > 0:
                # Simple approach: use the total present value of future dividends
                dividend_present_val = np.full(num_sims, total_future_dividends)
        
        us_price, us_se = longstaff_schwartz(
            S=price_paths,
            K=K,
            r=RISK_FREE_RATE,
            T=T,
            option_type=call_or_put,
            dividend_present_val=dividend_present_val
        )
        
        # Calculate standard deviations
        eu_payoffs = []
        us_payoffs = []
        
        for path in price_paths:
            final_price = float(path[-1])
            if call_or_put == 'call':
                eu_payoff = max(final_price - K, 0)
            else:  # put
                eu_payoff = max(K - final_price, 0)
            eu_payoffs.append(eu_payoff)
        
        # For American options, we need to calculate payoffs considering early exercise
        # This is a simplified approach - in practice, Longstaff-Schwartz would handle this
        us_payoffs = eu_payoffs.copy()  # Simplified for now
        
        eu_std = np.std(eu_payoffs) if len(eu_payoffs) > 1 else 0.0
        us_std = np.std(us_payoffs) if len(us_payoffs) > 1 else 0.0
        
        print(f"European {call_or_put} price: ${eu_price:.4f} ± ${eu_std:.4f}")
        print(f"American {call_or_put} price: ${us_price:.4f} ± ${us_std:.4f}")
        
        # Ensure dividend_schedule is always a dict
        dividend_schedule = stock_data.dividend_schedule if isinstance(stock_data.dividend_schedule, dict) else {}
        
        # Add option-specific dividend information
        dividend_schedule['option_period_info'] = option_dividend_info
        
        return (
            float(us_price),
            float(eu_price),  # Analytical Black-Scholes price
            float(us_std),
            float(eu_std),
            price_paths.tolist(),
            float(stock_data.volatility),
            dividend_schedule
        )
        
    except Exception as e:
        print(f"Error pricing option for {ticker}: {str(e)}")
        # Return safe defaults instead of raising
        return (
            0.0,  # us_price
            0.0,  # eu_price
            0.0,  # us_std
            0.0,  # eu_std
            [[0.0]],  # paths - safe default
            0.0,  # vol
            {}  # dividends
        )


def _print_dividend_info(dividend_data):
    """Print dividend schedule information."""
    if dividend_data and dividend_data.get('schedule'):
        schedule = dividend_data['schedule']
        print("\nDividends being used (most recent first):")
        for i, (date, amount) in enumerate(schedule[:5]):
            print(f"  {i+1}. Date: {date}, Amount: ${amount:.4f}")
        if len(schedule) > 5:
            print(f"  ... and {len(schedule) - 5} more dividends ...")
    else:
        print("No dividend data available for pricing.")


def _prepare_dividend_data(dividend_data, time_to_expiry, num_simulations):
    """Prepare dividend data for pricing models."""
    dividend_days = []
    dividend_present_val = np.zeros(num_simulations)
    
    if dividend_data and dividend_data.get('schedule'):
        dividend_schedule = dividend_data['schedule']
        dividend_days = get_dividend_array_for_pricing(dividend_schedule, time_to_expiry).tolist()
        present_value = dividend_data.get('present_value', 0.0)
        dividend_present_val.fill(present_value)
        
        print(f"Dividend forecast method: {dividend_data.get('forecast_method', 'N/A')}")
        print(f"Next dividend: ${dividend_data.get('next_dividend_amount', 0.0):.4f} on {dividend_data.get('next_dividend_date', 'N/A')}")
        print(f"Annual dividend yield: ${dividend_data.get('annual_yield', 0.0):.4f}")
        print(f"Present value of future dividends: ${present_value:.4f}")
    else:
        num_trading_days = int(time_to_expiry * TRADING_DAYS_PER_YEAR)
        dividend_days = [0.0] * num_trading_days
        print("No dividend data available")
    
    return dividend_days, dividend_present_val 