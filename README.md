## Options Pricing Overview

https://www.optionspricerapp.com/

### `options.py`

#### 1. **European Options Pricing:**
   - The `price_european_option` function calculates the price of European call or put options using the final prices of simulated asset paths. It computes the discounted payoff of the option, considering the strike price, risk-free interest rate, and time until expiry.
   - The function supports pricing for both call and put options, providing the mean payoff, mean payoff sample standard deviation, and payoff sample standard deviation.

#### 2. **American Options Pricing - Longstaff Schwartz Method:**
   - The `longstaff_schwartz` function implements the Longstaff-Schwartz method for pricing American options. It supports both call and put options.
   - The function iteratively computes the option price, considering whether it's optimal to exercise the option at each time step. It uses polynomial regression to estimate the continuation value at each step, deciding whether to exercise based on a comparison between the exercise and continuation values.

### `options_pricer.py`

- The `price_option` function in `options_pricer.py` is a comprehensive function for pricing options. It retrieves the initial stock price and implied volatility, then uses these values, along with user-specified parameters, to generate asset paths using the Heston model.
- The function then prices European and American options using the `price_european_option` and `longstaff_schwartz` functions from `options.py`. It returns the prices of both types of options along with their standard deviations and the generated asset paths.

#### Parameters:
- `call_or_put`: Specifies whether the option is a call or put.
- `ticker`: The stock ticker.
- `K`: The strike price.
- `T`: Time to expiry.
- `n`: Number of simulations.

### Supporting Modules:
- The repository also contains supporting modules like `black_scholes.py` for Black-Scholes pricing, `monte_carlo.py` for generating asset paths using the Heston model, and `brownian_motion.py` for generating correlated Brownian motions, which are integral to the options pricing process.

For a deeper understanding, users are encouraged to review the code and comments within each function in the respective files.
