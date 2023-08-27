import React, { useState } from "react"
import "bootstrap/dist/css/bootstrap.min.css"
import StockPriceChart from './StockPriceChart'

const OptionsPricer = () => {
    const [ticker, setTicker] = useState('GOOG')
    const [callOrPut, setCallOrPut] = useState('call')
    const [strikePrice, setStrikePrice] = useState(120)
    const [timeToExpiry, setTimeToExpiry] = useState(3)
    const [numSims, setNumSims] = useState(100)
    const [optionPrice, setOptionPrice] = useState(null)
    const [calculating, setCalculating] = useState(false)
    const [paths, setPaths] = useState([])

    const calculateOptionPrice = async () => {
      setCalculating(true)
      try {
        const response = await fetch('http://localhost:5000/price_option', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            callOrPut: callOrPut,
            ticker: ticker,
            K: strikePrice,
            T: timeToExpiry,
            numSims: numSims
          }),
        });
  
        if (!response.ok) {
          throw new Error('Network response was not ok')
        }
        const data = await response.json()
        setOptionPrice(data.option_price)
        setPaths(data.paths)
      } catch (error) {
        console.error('Error calculating option price:', error)
      }
      setCalculating(false)
    }
  

    const handleOptionChange = (event) => {
      setCallOrPut(event.target.value);
    };

    return (
        <div>
          <h1>Monte Carlo Options Pricer</h1>
          <form>
            <label>
              <input
                type="radio"
                value="call"
                checked={callOrPut === 'call'}
                onChange={handleOptionChange}
              />
              Call
            </label>
            <label>
              <input
                type="radio"
                value="put"
                checked={callOrPut === 'put'}
                onChange={handleOptionChange}
              />
              Put
            </label>
          </form>
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
            <label>Time to Expiration (years):</label>
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
          <button onClick={calculateOptionPrice}>Calculate</button>
          <h2>Option Price: {calculating ? 'loading' : optionPrice}</h2>
          {paths ? <StockPriceChart paths={paths} /> : <h1></h1>}
        </div>
      )
}

export default OptionsPricer


