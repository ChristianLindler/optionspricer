import React from 'react'
import {
  Grid,
  TextField,
  Container,
  Button,
  makeStyles,
  RadioGroup,
  Radio,
  FormControlLabel,
  Typography,
} from '@material-ui/core'
import { theme as customTheme } from '../../../theme'
import { uniqueSupportedTickers } from '../../../data/supportedTickers'

const useStyles = makeStyles({
  button: {
    color: 'white',
    fontFamily: customTheme.typography.fontFamily.primary,
    backgroundColor: customTheme.palette.secondary
  },
  radioButton: {
    color: 'white',
    '&.Mui-checked': {
      color: customTheme.palette.secondary
    },
  },
  secondaryText: {
    color: 'white',
    fontFamily: customTheme.typography.fontFamily.primary,
  }
})

const OptionsPricerForm = ({ setOptionData, setAlertOpen, setAlertMessage, calculating, setCalculating }) => {
  const classes = useStyles()

  const calculateOptionPrice = async (event) => {
    event.preventDefault()
    const formData = new FormData(event.currentTarget)

    const callOrPut = formData.get('callOrPut')
    const ticker = formData.get('ticker')
    const K = parseFloat(formData.get('strikePrice'))
    const daysToExpiry = parseInt(formData.get('timeToExpiry'))
    const numSims = parseInt(formData.get('numSims'))
    
    // Convert days to years for backend
    const T = daysToExpiry / 365.0
    
    // Validation with new limits
    if (K <= 0 || daysToExpiry <= 0 || daysToExpiry > 365 || numSims < 100 || numSims > 10000) {
      setAlertOpen(true)
      setAlertMessage('Check the values: Strike > 0, Days: 1-365, Simulations: 100-10,000')
      return
    }
    
    // Validate ticker is supported
    if (!uniqueSupportedTickers.includes(ticker.toUpperCase())) {
      setAlertOpen(true)
      setAlertMessage(`Ticker ${ticker} is not supported. Please use a Fortune 500 company ticker symbol.`)
      return
    }

    setCalculating(true)
    try {
      // Use localhost for local development, fallback to production URL
      const apiURL = process.env.NODE_ENV === 'development' 
        ? 'http://localhost:5000/price_option'
        : 'https://optionspricerapp-edb45e3d36e0.herokuapp.com/price_option'
      
      const response = await fetch(apiURL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          callOrPut: callOrPut,
          ticker: ticker.toUpperCase(),
          K: K,
          T: T,  // Converted to years
          numSims: numSims,
        }),
      })

      if (!response.ok) {
        throw new Error('Network response was not ok')
      }
      const data = await response.json()
      
      // Validate the response data structure
      if (!data || typeof data !== 'object') {
        throw new Error('Invalid response format from server')
      }
      
      // Validate paths data - ensure it's a 2D array with valid dimensions
      if (!data.paths || !Array.isArray(data.paths) || data.paths.length === 0) {
        throw new Error('Invalid paths data received from server')
      }
      
      // Check if paths is a proper 2D array
      if (!Array.isArray(data.paths[0]) || data.paths[0].length === 0) {
        throw new Error('Paths data is not in expected 2D array format')
      }
      
      // Validate other required fields
      if (typeof data.us_option_price !== 'number' || typeof data.eu_option_price !== 'number') {
        throw new Error('Invalid option prices received from server')
      }
      
      setOptionData({
        usPrice: data.us_option_price,
        euPrice: data.eu_option_price,
        usStdev: data.us_price_std,
        euStdev: data.eu_price_std,
        paths: data.paths,
        vol: data.vol,
        dividends: data.dividends,
        strikePrice: K,
      })
    } catch (error) {
      setAlertOpen(true)
      setAlertMessage(`Error Calculating Options Price: ${error.message}. Please ensure you entered a valid Fortune 500 company ticker symbol.`)
      setOptionData({paths: [[0]]}) // Set a safe default
      console.error('Error calculating option price:', error)
    }
    setCalculating(false)
  }

  return (
    <Container component='form' onSubmit={calculateOptionPrice}>
      <Grid container>
        <Grid item xs={6}>
          <Grid container direction='column'>
            <RadioGroup name='callOrPut' defaultValue='call'>
              <Grid container>
                <Grid item xs={6}>
                  <FormControlLabel
                    value='call'
                    control={<Radio className={classes.radioButton}/>}
                    label={<Typography className={classes.secondaryText}>Call</Typography>}
                  />
                </Grid>
                <Grid item xs={6}>
                  <FormControlLabel
                    value='put'
                    control={<Radio className={classes.radioButton}/>}
                    label={<Typography className={classes.secondaryText}>Put</Typography>}
                  />
                </Grid>
              </Grid>
            </RadioGroup>
            <TextField
              margin='normal'
              required
              fullWidth
              id='ticker'
              label='Company'
              name='ticker'
              type='text'
              autoFocus
              defaultValue="VZ"
              InputLabelProps={{style: {fontFamily: customTheme.typography.fontFamily.primary, color: 'white'}}}
              InputProps={{style: {fontFamily: customTheme.typography.fontFamily.primary, color: 'white'}}}
            />
            <TextField
              margin='normal'
              required
              fullWidth
              id='strikePrice'
              label='Strike Price'
              name='strikePrice'
              type='number'
              defaultValue={40}
              InputLabelProps={{style: {fontFamily: customTheme.typography.fontFamily.primary, color: 'white'}}}
              InputProps={{style: {fontFamily: customTheme.typography.fontFamily.primary, color: 'white'}}}
            />
          </Grid>
        </Grid>
        <Grid item xs={6}>
          <Grid container direction='column'>
            <TextField
              margin='normal'
              required
              fullWidth
              id='timeToExpiry'
              label='Time to Expiry (days)'
              name='timeToExpiry'
              type='number'
              defaultValue={60}
              inputProps={{
                min: 1,
                max: 365,
                step: '1',
              }}
              InputLabelProps={{style: {fontFamily: customTheme.typography.fontFamily.primary, color: 'white'}}}
              InputProps={{
                style: {fontFamily: customTheme.typography.fontFamily.primary, color: 'white'}
              }}
            />
            <TextField
              margin='normal'
              required
              fullWidth
              id='numSims'
              label='Number of Simulations (max 10,000)'
              name='numSims'
              type='number'
              defaultValue={1000}
              inputProps={{
                min: 100,
                max: 10000,
                step: '100',
              }}
              InputLabelProps={{style: {fontFamily: customTheme.typography.fontFamily.primary, color: 'white'}}}
              InputProps={{style: {fontFamily: customTheme.typography.fontFamily.primary, color: 'white'}}}
            />
            <Button
              type='submit'
              fullWidth
              variant='contained'
              style={{ marginTop: '24px', marginBottom: '16px' }}
              className={classes.button}
              disabled={calculating}
            >
              Calculate
            </Button>
          </Grid>
        </Grid>
      </Grid>
    </Container>
  )
}

export default OptionsPricerForm