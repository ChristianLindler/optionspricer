import React, { useState } from "react"
import "bootstrap/dist/css/bootstrap.min.css"
import StockPriceChart from './Visualizations/StockPriceChart'
import OptionPriceDistribution from "./Visualizations/OptionPriceDistribution"

const OptionsPricer = () => {
    const [ticker, setTicker] = useState('GOOG')
    const [callOrPut, setCallOrPut] = useState('call')
    const [strikePrice, setStrikePrice] = useState(120)
    const [timeToExpiry, setTimeToExpiry] = useState(3)
    const [numSims, setNumSims] = useState(100)
    const [optionPrice, setOptionPrice] = useState(null)
    const [optionPriceStdev, setOptionPriceStdev] = useState(null)
    const [calculating, setCalculating] = useState(false)
    const [paths, setPaths] = useState([])

    const calculateOptionPrice = async () => {
      setCalculating(true)
      try {
        const response = await fetch('http://localhost:4000/price_option', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            // 'Access-Control-Allow-Origin': 'http:/localhost:5000/price_option',
            // 'Access-Control-Allow-Methods': 'DELETE, POST, GET, OPTIONS',
            // 'Access-Control-Allow-Headers':  'Content-Type, Authorization, X-Requested-With',
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
        setOptionPriceStdev(data.price_std)
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
          <div className="row mx-auto mb-4">
            <form className="col-md-2">
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
            <div className="col-md-2">
              <label>Ticker:</label>
              <input
                className="form-control"
                type="text"
                name="ticker"
                value={ticker}
                onChange={(event) => setTicker(event.target.value)}
              />
            </div>
            <div className="col-md-2">
              <label>Strike Price:</label>
              <input
                className="form-control"
                type="number"
                name="strikePrice"
                value={strikePrice}
                onChange={(event) => setStrikePrice(event.target.value)}
              />
            </div>
            <div className="col-md-2">
              <label>Years to Expiry:</label>
              <input
                className="form-control"
                type="number"
                name="timeToExpiration"
                value={timeToExpiry}
                onChange={(event) => setTimeToExpiry(event.target.value)}
              />
            </div>
            <div className="col-md-2">
              <label>Number of Simulations:</label>
              <input
                className="form-control"
                type="number"
                name="simulations"
                value={numSims}
                onChange={(event) => setNumSims(event.target.value)}
              />
            </div>
          </div>
          <button onClick={calculateOptionPrice} className="btn btn-primary">Calculate</button>
          <h2 className="mt-4">Option Price: {calculating ? 'loading' : optionPrice}</h2>
          <div className="row"></div>
          <div className="row">
            <div className="chart-container mx-auto mb-4 col-md-6" style={{ width: '100%', maxWidth: '500px', height: '500px' }}>
              <StockPriceChart paths={paths} strikePrice={strikePrice} />
            </div>
            <div className="chart-container mx-auto mb-4 col-md-6" style={{ width: '100%', maxWidth: '500px', height: '500px' }}>
              <OptionPriceDistribution mean={optionPrice} stdDev={optionPriceStdev} />
            </div>
          </div>
        </div>
      )
}

export default OptionsPricer


