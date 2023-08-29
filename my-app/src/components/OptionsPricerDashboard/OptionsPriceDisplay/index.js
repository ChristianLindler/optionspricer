import React from 'react'
import { makeStyles } from '@material-ui/core'
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

const OptionsPriceDisplay = ({ optionPrice, stdDev }) => {
  const classes = useStyles()
  return (
    <div className="option-box">
      <div className="option-price">
        
        <p className={classes.secondaryText}>Option Price:</p>
        <h2 className={classes.primaryText}>${Number(optionPrice).toFixed(2)}</h2>
      </div>
      <div className={classes.secondaryText}>
        <p>68% Confidence Interval:</p>
        <p>${(optionPrice - stdDev).toFixed(2)} - ${(optionPrice + stdDev).toFixed(2)}</p>
      </div>
    </div>
  )
}

export default OptionsPriceDisplay