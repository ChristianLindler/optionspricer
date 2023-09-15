from datetime import datetime
from options import get_implied_vol, price_european_option, longstaff_schwartz, get_tickers
from monte_carlo import generate_paths
from black_scholes import black_scholes
from scipy.optimize import minimize, basinhopping
import yfinance as yf

NUM_STEPS = 100

def expiration_to_T(expiration_date_str):
    expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d').date()
    current_date = datetime.now().date()
    delta = expiration_date - current_date
    return {"expiry_date": expiration_date_str, "T": delta.days / 365.25}  # Convert days to years, considering leap years.

def price_option(call_or_put, ticker, K, T, n, params):
    '''
    call_or_put: whether option is call or put (string)
    ticker: Stock ticker
    K: Strike Price
    T: Time to expiry
    n: num simulations
    Returns: price of option
    params: [volatility, vol_of_vol, theta, rho, r, kappa]
    '''
    stock_data = yf.Ticker(ticker)
    initial_price = stock_data.history(period='1d')['Close'].iloc[0]
    volatility, vol_of_vol, theta, rho, r, kappa = params
    # TEMP VALUES
    # volatility = get_implied_vol(ticker)
    # theta = volatility ** 2 # long term mean of variance
    # vol_of_vol = 0.3
    # rho = -0.7 # brownian motion correlations
    # r = 0.041 # risk free interest rate
    # kappa = 5 # variance reversion rate
    dt = T/NUM_STEPS

    # Drift set to risk free interest rate (risk neutral pricing)
    time_points, heston_paths = generate_paths(n, initial_price, r, volatility, NUM_STEPS, T, kappa, vol_of_vol, theta, rho)
    eu_heston_price, heston_price_std, heston_payoff_std = price_european_option(call_or_put, heston_paths, K, r, T)
    bs_price = black_scholes(call_or_put, initial_price, K, T, volatility, r)
    us_heston_price = longstaff_schwartz(heston_paths, K, r, T, call_or_put)
    #heston_price = gpt_longstaff_schwartz(heston_paths, call_or_put, K, r, T)
    return us_heston_price, eu_heston_price, heston_paths.tolist(), heston_price_std, heston_payoff_std, bs_price

def get_market_price(ticker, strike, expiry_date, call_or_put='call'):
    option_data = yf.Ticker(ticker).option_chain(expiry_date)
    #option_data = yf.Ticker(ticker).option_chain('2023-09-15')
    # Filter call options by strike
    if call_or_put == 'call':
        options_list = option_data.calls
    elif call_or_put == 'put':
        options_list = option_data.puts
    option_at_strike = options_list[options_list['strike'] == strike]
    if not option_at_strike.empty:
        return option_at_strike['lastPrice'].iloc[0]
    return None

def objective_function(params, tickers, T_values, num_sims=1000):
    """
    params [volatility, vol_of_vol, theta, rho, r, kappa]
    tickers  [tickers]
    """
    total_error = 0
    volatility, vol_of_vol, theta, rho, r, kappa = params
    for ticker in tickers:
        strike = yf.Ticker(ticker).history(period='1d')['Close'].iloc[0]
        for t_value in T_values:
            time_to_expiry = t_value['T']
            expiry_date = t_value['expiry_date']
            for option_type in ['call', 'put']:
                model_price, _, _, _, _, _ = price_option(option_type, ticker, strike, time_to_expiry, num_sims, params)
                market_price = get_market_price(ticker, strike, expiry_date, option_type)
                if market_price is not None:
                    total_error += (model_price - market_price) ** 2
    return total_error

initial_guess = [get_implied_vol('GOOG'), 0.3, get_implied_vol('GOOG') ** 2, -0.7, 0.041, 5] # [volatility, vol_of_vol, theta, rho, r, kappa]
#tickers = get_tickers()
tickers = ['GOOG']
ticker_obj = yf.Ticker('GOOG')  # Replace with ticker you're interested in.
expirations = ticker_obj.options
selected_expirations = expirations[:2]  # Replace with expiration dates you're interested in.
T_values = [expiration_to_T(exp_date) for exp_date in selected_expirations]

bounds = [       # I completely made these up
    (0.01, 3),   # volatility range
    (0.01, 3),   # vol_of_vol range
    (0, 9),      # theta (assuming a 0 to 1 range; adjust if needed)
    (-1, 1),     # rho range
    (0, 0.1),    # r range
    (0, 10)      # kappa range
]

minimizer_kwargs = {
    "method": "L-BFGS-B", 
    "bounds": bounds, 
    "args": (tickers, T_values)
}

result = basinhopping(objective_function, initial_guess, minimizer_kwargs=minimizer_kwargs, niter=100, stepsize=0.5)
#result = minimize(objective_function, initial_guess, args=(tickers, T_values), bounds=bounds, method='L-BFGS-B')

optimal_params = result.x
minimum_value = result.fun
print("Minimum error: ", minimum_value)
print("[volatility, vol_of_vol, theta, rho, r, kappa]")
print(optimal_params)
print("original volatility: ")
print(get_implied_vol('GOOG'))
print("original theta: ")
print(get_implied_vol('GOOG') ** 2)