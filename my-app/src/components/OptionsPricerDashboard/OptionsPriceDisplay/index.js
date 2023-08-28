import React from 'react'
import { makeStyles } from '@material-ui/core';

const useStyles = makeStyles({
    container: {
      width: '100%',
      height: '100%',
      borderRadius: '10px',
      display: 'inline-flex',
      backgroundColor: '#1A2027',
      padding: '10px'
    }
  })

const OptionsPriceDisplay = ({ optionPrice, stdDev }) => {
  return (
    <div className="option-box">
      <div className="option-price">
        <p>Option Price</p>
        <h2>${optionPrice}</h2>
      </div>
      <div className="confidence-interval">
        <p>68% Confidence Interval</p>
        <p>${(optionPrice - stdDev)} - ${(optionPrice + stdDev)}</p>
      </div>
    </div>
  );
};

export default OptionsPriceDisplay;