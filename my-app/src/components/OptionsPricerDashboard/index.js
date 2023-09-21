import React, { useState } from 'react'
import StockPriceChart from './Visualizations/StockPriceChart'
import OptionPriceDistribution from './Visualizations/OptionPriceDistribution'
import OptionsPricerForm from './OptionsPricerForm'
import { Grid, Paper, Typography, createTheme, makeStyles } from '@material-ui/core'
import OptionsPriceDisplay from './OptionsPriceDisplay'
import StockPriceDistribution from './Visualizations/StockReturnsHistogram'
import { theme } from '../../theme'
import { Alert, CircularProgress } from '@mui/material'

const useStyles = makeStyles({
  container: {
    width: '95%',
    borderRadius: '10px',
    display: 'inline-flex',
    padding: '10px',
  },
  paper: {
    borderRadius: '10px',
    backgroundColor: theme.palette.primary,
    padding: '20px',
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
  },
  coloredPaper: {
    borderRadius: '10px',
    backgroundColor: theme.palette.secondary,
    padding: '20px',
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
  },
  secondaryText: {
    color: theme.palette.secondary,
    fontFamily: theme.typography.fontFamily.secondary,
    fontSize: theme.typography.fontSize.xs,
    marginTop: '10px',
  },
  alertContainer: {
    position: 'fixed',
    bottom: '20px',
    left: '50%',
    transform: 'translateX(-50%)',
    width: '40%',
    zIndex: 9999,
  },
  progressContainer: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100%',
  },
})

const OptionsPricerDashboard = () => {
  const [optionData, setOptionData] = useState({paths: [0]})
  const { paths, usPrice, euPrice, usStdev, euStdev, strikePrice } = optionData
  const [alertOpen, setAlertOpen] = useState(false)
  const [alertMessage, setAlertMessage] = useState('')
  const [calculating, setCalculating] = useState(false)
  const classes = useStyles()

  return (
    <Grid container justifyContent='center' className={classes.container} spacing={3}>
      {alertOpen && (
        <div className={classes.alertContainer}>
          <Alert severity='warning' onClose={() => setAlertOpen(false)}>
            {alertMessage}
          </Alert>
        </div>
      )}
      <Grid item xs={12} md={8}>
        <Paper className={classes.paper} elevation={10}>
          <div className={classes.flexContent}>
            <OptionsPricerForm
              setOptionData={setOptionData}
              setAlertOpen={setAlertOpen}
              setAlertMessage={setAlertMessage}
              calculating={calculating}
              setCalculating={setCalculating}
            />
          </div>
        </Paper>
      </Grid>

      <Grid item xs={6} md={4}>
        <Paper className={classes.paper} elevation={10}>
          <StockPriceDistribution paths={paths} strikePrice={strikePrice} numBins={30}/>
        </Paper>
      </Grid>

      <Grid item xs={6} md={4}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Paper className={classes.coloredPaper} elevation={10}>
              <OptionsPriceDisplay name={'European Price'} price={euPrice} />
            </Paper>
          </Grid>

          <Grid item xs={12}>
            <Paper className={classes.paper} elevation={10}>
              <OptionPriceDistribution mean={usPrice} stdDev={euStdev} />
            </Paper>
          </Grid>
        </Grid>
      </Grid>

      <Grid item xs={12} md={8}>
        <Paper className={classes.paper} elevation={10}>
          {calculating ?
            <div className={classes.progressContainer}>
              <CircularProgress sx={{color:theme.palette.secondary}} />
            </div>
          :
            <div>
              <StockPriceChart paths={paths} strikePrice={strikePrice} />
              <Typography className={classes.secondaryText}>{
              '*While the model will simulate up to 100,000 paths, only up to 100 will be graphed'
              }</Typography>
            </div>
            }
        </Paper>
      </Grid>
    </Grid>
  )
}

export default OptionsPricerDashboard