import React, { useEffect, useState } from 'react'
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
    align: 'left',
    justifyContent: 'center',
    textAlign: 'left',
  }
})

const OptionsPriceDisplay = ({ usPrice, euPrice, dividends }) => {
  const classes = useStyles()
  const [priceStrings, setPriceStrings] = useState([])

  useEffect(() => {
    let numDividends = 0;
    let dividendPayment = 0;
    if (dividends !== undefined) {
      for (let i = 0; i < dividends.length; i++) {
        if (dividends[i] !== 0) {
          numDividends++
          dividendPayment = parseFloat(dividends[i]).toFixed(2)
        }
      }
    }

    const euPriceStr = isNaN(euPrice) ? '' : '$' + Number(euPrice).toFixed(2)
    let usPriceStr = isNaN(usPrice) ? '' : '$' + Number(usPrice).toFixed(2)
    let dividendStr = `Assuming no dividend payments before expiry`
    if (numDividends === 0) {
      usPriceStr = euPriceStr
    } else if (usPriceStr !== '') {
      dividendStr = `Assuming ${numDividends} dividend payments of $${dividendPayment} before expiry`
    }
    setPriceStrings([usPriceStr, euPriceStr, dividendStr])


  }, [usPrice, euPrice, dividends])

  return (
    <div className='option-box'>
      <Grid container>
        <Grid item xs={12} className={classes.gridItem}>
          <h4 className={classes.secondaryText}>{'US Price:  ' + priceStrings[0]}</h4>
        </Grid>
        <Grid item xs={12} className={classes.gridItem}>
          <h4 className={classes.secondaryText}>{'EU Price:  ' + priceStrings[1]}</h4>
        </Grid>
        <Grid item xs={12} className={classes.gridItem}>
          <p className={classes.secondaryText}>{priceStrings[2]}</p>
        </Grid>
      </Grid>
    </div>
  )
}

export default OptionsPriceDisplay