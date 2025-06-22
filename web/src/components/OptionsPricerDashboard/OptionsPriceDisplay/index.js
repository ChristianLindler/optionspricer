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
  priceLabel: {
    color: 'white',
    fontFamily: theme.typography.fontFamily.primary,
    fontSize: '20px',
    fontWeight: 600,
    margin: '8px 0',
    lineHeight: 1.2,
  },
  priceValue: {
    color: 'white',
    fontFamily: theme.typography.fontFamily.primary,
    fontSize: '24px',
    fontWeight: 700,
    marginLeft: '8px',
  },
  dividendText: {
    color: 'white',
    fontFamily: theme.typography.fontFamily.primary,
    fontSize: '14px',
    marginTop: '12px',
    opacity: 0.9,
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
    const euPriceStr = isNaN(euPrice) ? '' : '$' + Number(euPrice).toFixed(2)
    let usPriceStr = isNaN(usPrice) ? '' : '$' + Number(usPrice).toFixed(2)
    let dividendStr = `No dividend payments expected during option period`
    
    // Handle new dividend structure with option period info
    if (dividends && dividends.option_period_info) {
      const optionInfo = dividends.option_period_info
      const actualDividends = optionInfo.dividends_in_period
      const forecastDividends = optionInfo.forecast_dividends
      
      // Use actual dividends if available, otherwise use forecasted ones
      const dividendsToShow = actualDividends.length > 0 ? actualDividends : forecastDividends
      
      if (dividendsToShow && dividendsToShow.length > 0) {
        // Calculate total dividend amount
        const totalAmount = dividendsToShow.reduce((sum, [_, amount]) => sum + amount, 0)
        dividendStr = `${dividendsToShow.length} dividend(s) during option period (total: $${totalAmount.toFixed(2)})`
      }
    } else if (dividends && dividends.schedule && dividends.schedule.length > 0) {
      // Fallback to old format
      const schedule = dividends.schedule
      const numDividends = schedule.length
      const avgDividend = (schedule.reduce((sum, [_, amount]) => sum + amount, 0) / numDividends).toFixed(2)
      
      dividendStr = `Using ${numDividends} recent dividend payments (avg: $${avgDividend})`
      
      // If American option price is different from European, it means dividends are being considered
      if (usPrice !== euPrice && !isNaN(usPrice) && !isNaN(euPrice)) {
        dividendStr += ` - Dividends factored into pricing`
      }
    } else if (dividends && Array.isArray(dividends)) {
      // Handle old array format for backward compatibility
      let numDividends = 0;
      let dividendPayment = 0;
      for (let i = 0; i < dividends.length; i++) {
        if (dividends[i] !== 0) {
          numDividends++
          dividendPayment = parseFloat(dividends[i]).toFixed(2)
        }
      }
      
      if (numDividends > 0) {
        dividendStr = `Assuming ${numDividends} dividend payments of $${dividendPayment} before expiry`
      }
    }
    
    setPriceStrings([usPriceStr, euPriceStr, dividendStr])
  }, [usPrice, euPrice, dividends])

  return (
    <div className='option-box'>
      <Grid container>
        <Grid item xs={12} className={classes.gridItem}>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <span className={classes.priceLabel}>US Price:</span>
            <span className={classes.priceValue}>{priceStrings[0]}</span>
          </div>
        </Grid>
        <Grid item xs={12} className={classes.gridItem}>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <span className={classes.priceLabel}>EU Price:</span>
            <span className={classes.priceValue}>{priceStrings[1]}</span>
          </div>
        </Grid>
        <Grid item xs={12} className={classes.gridItem}>
          <p className={classes.dividendText}>{priceStrings[2]}</p>
        </Grid>
      </Grid>
    </div>
  )
}

export default OptionsPriceDisplay