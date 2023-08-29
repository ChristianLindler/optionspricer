import React, { useState } from 'react'
import StockPriceChart from './Visualizations/StockPriceChart'
import OptionPriceDistribution from './Visualizations/OptionPriceDistribution'
import OptionsPricerForm from './OptionsPricerForm'
import { Grid, Paper, Typography, makeStyles } from '@material-ui/core'
import OptionsPriceDisplay from './OptionsPriceDisplay'
import StockPriceDistribution from './Visualizations/StockReturnsHistogram'
import { theme } from '../../theme'

const useStyles = makeStyles({
  container: {
    width: '95%',
    borderRadius: '10px',
    display: 'inline-flex',
    padding: '10px',
  },
  paper: {
    borderRadius: '10px',
    backgroundColor: theme.colors.primary,
    padding: '20px',
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
  },
  coloredPaper: {
    borderRadius: '10px',
    backgroundColor: theme.colors.secondary,
    padding: '20px',
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
  },
  secondaryText: {
    color: theme.colors.secondary,
    fontFamily: theme.typography.fontFamily.secondary,
    fontSize: theme.typography.fontSize.xs,
    marginTop: '10px',
  },
})

const OptionsPricerDashboard = () => {
  const [optionData, setOptionData] = useState({paths: [0]})
  const { paths, optionPrice, optionPriceStdev, blackScholesPrice, strikePrice } = optionData

  const classes = useStyles()

  return (
    <Grid container justifyContent='center' className={classes.container} spacing={3}>
      <Grid item xs={8}>
        <Paper className={classes.paper} elevation={10}>
          <div className={classes.flexContent}>
            <OptionsPricerForm setOptionData={setOptionData}/>
          </div>
          
        </Paper>
      </Grid>

      <Grid item xs={4}>
        <Paper className={classes.paper} elevation={10}>
          <StockPriceDistribution paths={paths} strikePrice={strikePrice} numBins={20}/>
        </Paper>
      </Grid>

      <Grid item xs={4}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Paper className={classes.coloredPaper} elevation={10}>
              <OptionsPriceDisplay optionPrice={optionPrice} stdDev={optionPriceStdev} />
            </Paper>
          </Grid>

          <Grid item xs={12}>
            <Paper className={classes.paper} elevation={10}>
              <OptionPriceDistribution mean={optionPrice} stdDev={optionPriceStdev} />
            </Paper>
          </Grid>
        </Grid>
      </Grid>

      <Grid item xs={8}>
        <Paper className={classes.paper} elevation={10}>
          <StockPriceChart paths={paths} strikePrice={strikePrice} />
          <Typography className={classes.secondaryText}>{
            '*While the model will simulate up to 10,000 paths, only up to 100 will be graphed'
          }</Typography>
          
        </Paper>
      </Grid>
    </Grid>
  )
}

export default OptionsPricerDashboard