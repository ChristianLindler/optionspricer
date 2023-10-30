import React, { useState } from 'react'
import 'bootstrap/dist/css/bootstrap.min.css'
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
import { theme } from '../../../theme'

const useStyles = makeStyles({
  button: {
    color: 'white',
    fontFamily: theme.typography.fontFamily.primary,
    backgroundColor: theme.palette.secondary
  },
  radioButton: {
    color: 'white',
    '&.Mui-checked': {
      color: theme.palette.secondary
    },
  },
  secondaryText: {
    color: 'white',
    fontFamily: theme.typography.fontFamily.primary,
  }
})

const OptionsPricerForm = ({ setOptionData, setAlertOpen, setAlertMessage, calculating, setCalculating }) => {
  const classes = useStyles()

  const calculateOptionPrice = async (event) => {
    event.preventDefault()
    const formData = new FormData(event.currentTarget)

    const callOrPut = formData.get('callOrPut')
    const ticker = formData.get('ticker')
    const K = formData.get('strikePrice')
    const T = formData.get('timeToExpiry')
    const numSims = formData.get('numSims')
    
    if (K < 0 || T < 0 || numSims < 2 || numSims > 100000) {
      setAlertOpen(true)
      setAlertMessage('Check the values entered in the form')
      return
    }

    setCalculating(true)
    try {
      
      const herokuURL = 'https://optionspricer-369a3f4b4a0f.herokuapp.com/price_option'
      const response = await fetch('http://localhost:5000/price_option'
      , {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          callOrPut: callOrPut,
          ticker: ticker,
          K: K,
          T: T,
          numSims: numSims,
        }),
      })

      if (!response.ok) {
        throw new Error('Network response was not ok')
      }
      const data = await response.json()
      setOptionData({
        usPrice: data.us_option_price,
        euPrice: data.eu_option_price,
        usStdev: data.us_price_std,
        euStdev: data.eu_price_std,
        paths: data.paths,
        vol: data.vol,
        dividends: data.dividends,
        strikePrice: formData.get('strikePrice'),
      })
    } catch (error) {
      console.error('Error calculating option price:', error)
    }
    setCalculating(false)
  }

  return (
    <Container component='form' onSubmit={calculateOptionPrice}>
      <Grid container width={'100%'}>
        <Grid item xs={6}>
          <Grid container direction='column'>
            <RadioGroup name='callOrPut' defaultValue='call' fullwidth>
              <Grid container>
                <Grid item xs={6}>
                  <FormControlLabel
                    value='call'
                    control={<Radio className={classes.radioButton}/>}
                    label={<Typography className={classes.secondaryText}>Call</Typography>}
                    fullWidth
                  />
                </Grid>
                <Grid item xs={6}>
                  <FormControlLabel
                    value='put'
                    control={<Radio className={classes.radioButton}/>}
                    label={<Typography className={classes.secondaryText}>Put</Typography>}
                    fullWidth
                  />
                </Grid>
              </Grid>
            </RadioGroup>
            <TextField
              className={classes.textField}
              margin='normal'
              required
              width={'100%'}
              id='ticker'
              label='Ticker'
              name='ticker'
              autoFocus
              defaultValue={'MSFT'}
              InputLabelProps={{style: {fontFamily: theme.typography.fontFamily.primary, color: 'white'}}}
              InputProps={{style: {fontFamily: theme.typography.fontFamily.primary, color: 'white'}}}
            />
            <TextField
              className={classes.secondaryFontText}
              margin='normal'
              required
              fullWidth
              id='strikePrice'
              label='Strike Price'
              name='strikePrice'
              type='number'
              autoFocus
              defaultValue={300}
              InputLabelProps={{style: {fontFamily: theme.typography.fontFamily.primary, color: 'white'}}}
              InputProps={{style: {fontFamily: theme.typography.fontFamily.primary, color: 'white'}}}
            />
          </Grid>
        </Grid>
        <Grid item xs={6}>
          <Grid container direction='column'>
            <TextField
              className={classes.secondaryFontText}
              margin='normal'
              required
              fullWidth
              id='timeToExpiry'
              label='Time to Expiry (years)'
              name='timeToExpiry'
              type='number'
              autoFocus
              defaultValue={1}
              InputLabelProps={{style: {fontFamily: theme.typography.fontFamily.primary, color: 'white'}}}
              InputProps={{
                style: {fontFamily: theme.typography.fontFamily.primary, color: 'white'}
              }}
              inputProps={{
                step: '0.01',
              }}
            />
            <TextField
              className={classes.secondaryFontText}
              margin='normal'
              required
              fullWidth
              id='numSims'
              label='Number of Simulations (max 100,000)'
              name='numSims'
              type='number'
              autoFocus
              defaultValue={5000}
              InputLabelProps={{style: {fontFamily: theme.typography.fontFamily.primary, color: 'white'}}}
              InputProps={{style: {fontFamily: theme.typography.fontFamily.primary, color: 'white'}}}
            />
            <Button
              type='submit'
              fullWidth
              variant='contained'
              sx={{ mt: 3, mb: 2 }}
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