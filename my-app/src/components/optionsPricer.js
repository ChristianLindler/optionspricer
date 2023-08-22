import React, { Component, useState } from "react"
import "bootstrap/dist/css/bootstrap.min.css"

const OptionsPricer = () => {
    const [ticker, setTicker] = useState()
    const [strikePrice, setStrikePrice] = useState()
    const [timeToExpiry, setTimeToExpiry] = useState()
    const [numSims, setNumSims] = useState()
    const [optionPrice, setOptionPrice] = useState()

    const simulateOptionPrice = () => {
    // Monte Carlo option pricing will go here
    // Need to set option price, update state, and update chart data
    }

    return (
        <div>
          <h1>Monte Carlo Options Pricer</h1>
          <div>
            <label>Ticker:</label>
            <input
              type="text"
              name="ticker"
              value={ticker}
              onChange={(event) => setTicker(event.target.value)}
            />
          </div>
          <div>
            <label>Strike Price:</label>
            <input
              type="number"
              name="strikePrice"
              value={strikePrice}
              onChange={(event) => setStrikePrice(event.target.value)}
            />
          </div>
          <div>
            <label>Time to Expiration (days):</label>
            <input
              type="number"
              name="timeToExpiration"
              value={timeToExpiry}
              onChange={(event) => setTimeToExpiry(event.target.value)}
            />
          </div>
          <div>
            <label>Number of Simulations:</label>
            <input
              type="number"
              name="simulations"
              value={numSims}
              onChange={(event) => setNumSims(event.target.value)}
            />
          </div>
          <button onClick={simulateOptionPrice}>Calculate</button>
          {optionPrice !== null && (
            <div>
              <h2>Option Price: {optionPrice}</h2>
            </div>
          )}
        </div>
      )
}

export default OptionsPricer


