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
  },
  gridItem: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center', // Center horizontally
    justifyContent: 'center', // Center vertically
    textAlign: 'center',
  }
})

const OptionsPriceDisplay = ({ name, price }) => {
  const classes = useStyles()
  return (
    <div className='option-box'>
      <Grid container>
        <Grid item xs={6} className={classes.gridItem}>
          <h4 className={classes.secondaryText}>{name + ':'}</h4>
        </Grid>
        <Grid item xs={6} className={classes.gridItem}>
          <h2 className={classes.primaryText}>{isNaN(price) ? '' : '$' + Number(price).toFixed(2)}</h2>
        </Grid>
      </Grid>
    </div>
  )
}

export default OptionsPriceDisplay