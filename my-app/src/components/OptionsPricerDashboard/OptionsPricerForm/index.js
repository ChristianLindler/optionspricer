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
    backgroundColor: theme.colors.secondary
  },
  radioButton: {
    color: 'white',
    '&.Mui-checked': {
      color: theme.colors.secondary
    },
  },
  secondaryText: {
    color: 'white',
    fontFamily: theme.typography.fontFamily.primary,
  }
})

const OptionsPricerForm = ({ setOptionData }) => {
  const [calculating, setCalculating] = useState(false)

  const classes = useStyles()

  const calculateOptionPrice = async (event) => {
    event.preventDefault()
    const formData = new FormData(event.currentTarget)
    setCalculating(true)
    try {
      const response = await fetch('http://localhost:4000/price_option', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          callOrPut: formData.get('callOrPut'),
          ticker: formData.get('ticker'),
          K: formData.get('strikePrice'),
          T: formData.get('timeToExpiry'),
          numSims: formData.get('numSims'),
        }),
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
              defaultValue={'GOOG'}
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
              defaultValue={130}
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
              InputProps={{style: {fontFamily: theme.typography.fontFamily.primary, color: 'white'}}}
            />
            <TextField
              className={classes.secondaryFontText}
              margin='normal'
              required
              fullWidth
              id='numSims'
              label='Number of Simulations'
              name='numSims'
              type='number'
              autoFocus
              defaultValue={100}
              InputLabelProps={{style: {fontFamily: theme.typography.fontFamily.primary, color: 'white'}}}
              InputProps={{style: {fontFamily: theme.typography.fontFamily.primary, color: 'white'}}}
            />
            <Button
              type='submit'
              fullWidth
              variant='contained'
              sx={{ mt: 3, mb: 2 }}
              className={classes.button}
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