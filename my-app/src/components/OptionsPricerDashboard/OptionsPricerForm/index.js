import React, { useState } from 'react'
import "bootstrap/dist/css/bootstrap.min.css"
import { Grid, FormControl, InputLabel, Input, Button, makeStyles, RadioGroup, Radio, FormControlLabel } from '@material-ui/core'

const useStyles = makeStyles({
  container: {
    width: '50%',
    margin: 'auto',
  }
})

const initialParameters = {
  callOrPut: 'call',
  ticker: 'GOOG',
  strikePrice: 120,
  timeToExpiry: 3,
  numSims: 200
}

const OptionsPricerForm = ({setOptionData}) => {
  const [optionParameters, setOptionParameters] = useState(initialParameters)
  const { callOrPut, ticker, strikePrice, timeToExpiry, numSims } = optionParameters
  const [calculating, setCalculating] = useState(false)

  const classes = useStyles()

  const formatFieldName = (fieldName) => {
    // regex to add spaces between words/capitalize
    return fieldName.replace(/([A-Z])/g, ' $1').trim().replace(/^\w/, (c) => c.toUpperCase())
  }

  const handleChange = (event) => {
    const { name, value } = event.target
    setOptionParameters((prevParameters) => ({...prevParameters, [name]: value}))
  }

  const handleRadioButtonPress = (option) => {
    setOptionParameters({...optionParameters, callOrPut: option})
  }

  const calculateOptionPrice = async () => {
    setCalculating(true)
    try {
      const response = await fetch('http://localhost:4000/price_option', {
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
        })
      })

      if (!response.ok) {
        throw new Error('Network response was not ok')
      }
      const data = await response.json()
      setOptionData({
        optionPrice: data.option_price,
        optionPriceStdev: data.price_std,
        paths: data.paths,
        blackScholesPrice: data.bs_price,
        strikePrice: strikePrice
      })
    } catch (error) {
      console.error('Error calculating option price:', error)
    }
    setCalculating(false)
  }

  return (
    <Grid container spacing={2} className={classes.container}>
        <Grid item xs={12} sm={6}>
        <RadioGroup name="callOrPut" onChange={handleRadioButtonPress}>
            <FormControlLabel
            value="call"
            control={<Radio />}
            label="Call"
            />
            <FormControlLabel
            value="put"
            control={<Radio />}
            label="Put"
            />
        </RadioGroup>
        <FormControl className={classes.input}>
            <InputLabel shrink={Boolean(ticker)}>
            {formatFieldName('ticker')}
            </InputLabel>
            <Input
            name="ticker"
            value={ticker}
            onChange={handleChange}
            type="text"
            />
        </FormControl>
        <FormControl className={classes.input}>
            <InputLabel shrink={Boolean(strikePrice)}>
            {formatFieldName('strikePrice')}
            </InputLabel>
            <Input
            name="strikePrice"
            value={strikePrice}
            onChange={handleChange}
            type="number"
            />
        </FormControl>
        </Grid>
        <Grid item xs={12} sm={6}>
        <FormControl className={classes.input}>
            <InputLabel shrink={Boolean(timeToExpiry)}>
            {formatFieldName('timeToExpiry')}
            </InputLabel>
            <Input
            name="timeToExpiry"
            value={timeToExpiry}
            onChange={handleChange}
            type="number"
            />
        </FormControl>
        <FormControl className={classes.input}>
            <InputLabel shrink={Boolean(numSims)}>
            {formatFieldName('numSims')}
            </InputLabel>
            <Input
            name="numSims"
            value={numSims}
            onChange={handleChange}
            type="number"
            />
        </FormControl>
        <Button className={classes.button} onClick={calculateOptionPrice} variant='contained' color='secondary' disabled={calculating}>Calculate</Button>
        </Grid>
    </Grid>
  )
}

export default OptionsPricerForm