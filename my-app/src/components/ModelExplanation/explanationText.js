const explanationText = {
    p1: {
        title: 'Geometric Brownian Motion',
        line1: `The basic Monte Carlo method for estimating option prices involves simulating multiple stochastic paths for a stock using Geometric Brownian Motion (GBM). GBM is described by the following formula:`,
        line2: `Change in Price = Drift * CurrentPrice * dt + AssetVolatility * BrownianMotionIncrement * CurrentPrice`,
        line3: `The Brownian motion increment is a random variable that follows a normal distribution centered around zero with a variance of dt. It's essential to note that this randomness is scaled by the current stock price and volatility. This term reflects the instantaneous volatility of the asset at that time step and determines how much the stock price will fluctuate during the infinitesimal time interval dt.
        While GBM can generate realistic stock price paths, it has several limitations and ultimately converges to the Black-Scholes Model, which is a less computationally intensive method. This basic model makes multiple assumptions, including constant volatility, a normal distribution of returns, and the absence of jumps.`
      },
      p2: {
        title: 'The Heston Model',
        line1: `The Heston Model addresses these limitations. It introduces stochastic volatility as a key feature. While the original GBM equation can still be used for asset prices, an additional equation for asset volatility must be considered:`,
        line2: `Change in Volatility = MeanReversionRate * (MeanOfVariance - AssetVariance) * dt + VolatilityOfAssetVolatility * AssetVolatility * BrownianMotionIncrement`  ,
        line3: `Note the new variables introduced in this equation. In the first term, volatility experiences a mean-reverting jump, scaled by the MeanReversionRate. The second term mirrors the second term of our equation for the change in price.
        To fully capture the relationship between asset price and volatility, we must introduce one more variable: the correlation (rho) between the two Brownian motions. This correlation accounts for the negative relationship between asset prices and volatility. For example, as asset prices fall, market participants may react by buying at the lower price or selling out of fear, leading to increased volatility. By correlating the two Brownian motions with rho, we capture this relationship, resulting in a model that aligns with real-world tendencies.`
      },
      p3: {
        title: 'The Longstaff-Schwartz Process',
        line1: `When estimating the price of a European option based on the provided asset paths, the procedure is relatively straightforward: you average the discounted payoffs at the end of these paths. However, the valuation of American options is a more intricate process due to their ability to be exercised at any time. The process involves the following steps:`,
        line2: `1. Begin by creating an exercise value matrix for the American option (max(K - S, 0) for puts, max(S-K, 0) for calls)`,
        line3: `2. To construct a cash flow matrix, work backward in time. At each time step, use least squares to fit a polynomial to the spot prices and their corresponding cash flows. This resulting function calculates the continuation value based on the current asset price.`,
        line4: `3. Compare the exercise value to the continuation value. If the exercise value is greater than the continuation value, it is reasonable to assume that the option would be exercised. Consequently, the future cash flow for that path is set to zero.`,
        line5: `4. In cases where the exercise value is less than the continuation value, discount the cash flow at time t+1 using the risk free interest rate to obtain the cash flow at time t.`,
        line6: `5. After constructing this cash flow matrix, average the initial cash flows across all paths to approximate the value of the American option.`,
        line7: `By following these steps, the Longstaff-Schwartz process provides a comprehensive method for estimating the value of American options, accounting for the flexibility of early exercise.`
      },
}

export default explanationText