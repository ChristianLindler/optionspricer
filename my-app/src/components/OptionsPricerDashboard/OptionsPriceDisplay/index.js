import React from 'react'
import { Grid, makeStyles } from '@material-ui/core'
import { theme } from '../../../theme'

const useStyles = makeStyles({
  container: {
    width: '100%',
    height: '100%',
    borderRadius: '10px',
    display: 'inline-flex',
    padding: '10px'
  },
  primaryText: {
    color: 'white',
    fontFamily: theme.typography.fontFamily.primary,
  },
  secondaryText: {
    color: 'white',
    fontFamily: theme.typography.fontFamily.primary,
  }
})

const OptionsPriceDisplay = ({ usPrice, euPrice, usStdev }) => {
  const classes = useStyles()
  return (
    <div className='option-box'>
      <Grid container>
        <Grid item xs={6}>
          <p className={classes.secondaryText}>American Option Price:</p>
          <h2 className={classes.primaryText}>${Number(usPrice).toFixed(2)}</h2>
        </Grid>
        <Grid item xs={6}>
          <p className={classes.secondaryText}>European Option Price:</p>
          <h2 className={classes.primaryText}>${Number(euPrice).toFixed(2)}</h2>
        </Grid>
      </Grid>
      <div className={classes.secondaryText}>
        <p>US 68% Confidence Interval:</p>
        <p>${Number(usPrice - usStdev).toFixed(2)} - ${Number(usPrice + usStdev).toFixed(2)}</p>
      </div>
    </div>
  )
}

export default OptionsPriceDisplay