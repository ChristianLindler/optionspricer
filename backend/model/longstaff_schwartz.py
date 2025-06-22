import numpy as np
import tqdm
import matplotlib.pyplot as plt

# https://www.youtube.com/watch?v=--Il6rgtVjM
# https://people.math.ethz.ch/~hjfurrer/teaching/LongstaffSchwartzAmericanOptionsLeastSquareMonteCarlo.pdf
def longstaff_schwartz(S, K, r, T, option_type='call', dividend_present_val=None):
    """
    Longstaff-Schwartz American option pricing method for call or put options.
    
    Args:
    S (np.ndarray): Price matrix, where each row represents a price path.
    K (float): Strike price of the option.
    r (float): Risk-free interest rate.
    T (float): Time to maturity.
    option_type (str): 'call' for call option or 'put' for put option.
    dividend_present_val (np.ndarray): Discounted payoff of future dividends per path.
    
    Returns:
    tuple: Option price and standard error.
    """

    num_sims, num_steps = S.shape
    dt = T / num_steps  # Time interval
    df = np.exp(-r * dt) # Discount factor per time interval

    if option_type == 'put':
        exercise_value = np.maximum(K - S, 0) # Intrinsic values for put option
    elif option_type == 'call':
        exercise_value = S - K # Intrinsic values for call option
        if dividend_present_val is not None and isinstance(dividend_present_val, np.ndarray):
            if dividend_present_val.ndim == 1:
                exercise_value = exercise_value + dividend_present_val[:, np.newaxis]
            else:
                exercise_value = exercise_value + dividend_present_val
        exercise_value = np.maximum(exercise_value, 0)
    else:
        raise ValueError("Invalid option_type. Use 'put' or 'call'.")

    cashflow = np.zeros_like(exercise_value)
    cashflow[:, -1] = exercise_value[:, -1] # No continuation value on final day, it equals exercise value

    for t in tqdm.trange(num_steps - 2, -1, -1):
        itm = exercise_value[:, t] > 0 # Matrix set to true where price is in the money
        
        if np.count_nonzero(itm) > 0:
            regression = np.polyfit(S[itm, t], cashflow[itm, t + 1] * df, 2) # Fit a polynomial to the prices vs their cashflows using least squares method
            continuation_value = np.polyval(regression, S[itm, t]) # Use polynomial to estimate the continuation value
        else:
            continuation_value = np.zeros(np.count_nonzero(itm))  # Fix: use correct shape for empty array
        
        # Exercise holds whether it is optimal exercise for each path on this timestep
        exercise = np.zeros(len(itm), dtype=bool) 
        exercise[itm] = exercise_value[itm, t] > continuation_value

        cashflow[exercise, t] = exercise_value[exercise, t]  # Cashflow is now the exercise value for paths where we exercised
        cashflow[exercise, t + 1 :] = 0  # Set future cash flows, for that path, equal to zero as we would have already exercised
        discount_path = cashflow[:, t] == 0  # Paths where we didn't exercise
        cashflow[discount_path, t] = cashflow[discount_path, t + 1] * df  # Discount cashflow for paths we didn't exercise

    # Expectation of the initial discounted cashflow
    option_price = np.mean(cashflow[:, 0])
    std_dev = np.std(cashflow[:, 0])
    se = std_dev / np.sqrt(len(cashflow[:, 0]))
    return option_price, se

