import React, { useState } from 'react'
import "bootstrap/dist/css/bootstrap.min.css"
import StockPriceChart from './Visualizations/StockPriceChart'
import OptionPriceDistribution from "./Visualizations/OptionPriceDistribution"
import OptionsPricerForm from './OptionsPricerForm'
import { Grid, Paper, makeStyles } from '@material-ui/core'
import OptionsPriceDisplay from './OptionsPriceDisplay'

const useStyles = makeStyles({
  container: {
    width: '95%',
    borderRadius: '10px',
    display: 'inline-flex',
    backgroundColor: '#1A2027',
    padding: '10px'
  },
  paper: {
    margin: '10px',
    borderRadius: '10px',
    backgroundColor: '#3A4047',
    elevation: 5,
    padding: '10px'
  }
})

const OptionsPricerDashboard = () => {
  const [optionData, setOptionData] = useState({})
  const { paths, optionPrice, optionPriceStdev, blackScholesPrice, strikePrice } = optionData

  const classes = useStyles()

  return (
    <div className={classes.body}>
      <Grid container justifyContent="center" className={classes.container}>
        <Grid item xs={8}>
          <Paper className={classes.paper} elevation={3}>
            <OptionsPricerForm setOptionData={setOptionData}/>
          </Paper>
        </Grid>
        <Grid item xs={4}>
          <Paper className={classes.paper} elevation={3}>
            <OptionPriceDistribution mean={optionPrice} stdDev={optionPriceStdev} />
          </Paper>
        </Grid>
        <Grid item xs={4}>
          <Paper className={classes.paper} elevation={3}>
            <OptionsPriceDisplay optionPrice={optionPrice} stdDev={optionPriceStdev} />
          </Paper>
        </Grid>
        <Grid item xs={8}>
          <Paper className={classes.paper} elevation={3}>
            <StockPriceChart paths={paths} strikePrice={strikePrice} />
          </Paper>
        </Grid>
      </Grid>
    </div>
  )
}

export default OptionsPricerDashboard