import React, { useState } from 'react'
import StockPriceChart from './Visualizations/StockPriceChart'
import OptionPriceDistribution from './Visualizations/OptionPriceDistribution'
import OptionsPricerForm from './OptionsPricerForm'
import { Grid, Paper, Typography, makeStyles, useTheme, useMediaQuery } from '@material-ui/core'
import OptionsPriceDisplay from './OptionsPriceDisplay'
import StockPriceDistribution from './Visualizations/StockReturnsHistogram'
import { theme as customTheme } from '../../theme'
import { Alert, CircularProgress } from '@mui/material'

const useStyles = makeStyles((theme) => ({
  container: {
    width: '95%',
    borderRadius: '10px',
    display: 'inline-flex',
    padding: '10px',
  },
  paper: {
    backgroundColor: customTheme.palette.primary,
    borderRadius: '10px',
    padding: '20px',
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
  },
  coloredPaper: {
    backgroundColor: customTheme.palette.secondary,
    borderRadius: '10px',
    padding: '20px',
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
  },
  flexContent: {
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
  },
  secondaryText: {
    color: customTheme.palette.secondary,
    fontFamily: customTheme.typography.fontFamily.secondary,
    fontSize: customTheme.typography.fontSize.xs,
    marginTop: '10px',
  },
  alertContainer: {
    position: 'fixed',
    bottom: '20px',
    left: '50%',
    transform: 'translateX(-50%)',
    width: '40%',
    zIndex: 9999,
    [theme.breakpoints.down('sm')]: {
      width: '90%',
      bottom: '10px',
    },
  },
  progressContainer: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100%',
  },
}))

const OptionsPricerDashboard = () => {
  const [optionData, setOptionData] = useState({paths: [0]})
  const { paths, usPrice, euPrice, usStdev, euStdev, strikePrice, vol, dividends } = optionData
  const [alertOpen, setAlertOpen] = useState(false)
  const [alertMessage, setAlertMessage] = useState('')
  const [calculating, setCalculating] = useState(false)
  const classes = useStyles()
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('md'))

  return (
    <Grid container justifyContent='center' className={classes.container} spacing={3}>
      {alertOpen && (
        <div className={classes.alertContainer}>
          <Alert severity='warning' onClose={() => setAlertOpen(false)}>
            {alertMessage}
          </Alert>
        </div>
      )}
      <Grid item xs={12} lg={8}>
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

      <Grid item xs={12} sm={6} lg={4}>
        <Paper className={classes.paper} elevation={10}>
          <StockPriceDistribution paths={paths} strikePrice={strikePrice} numBins={30}/>
        </Paper>
      </Grid>

      <Grid item xs={12} sm={6} lg={4}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Paper className={classes.coloredPaper} elevation={10}>
              <OptionsPriceDisplay usPrice={usPrice} euPrice={euPrice} dividends={dividends} />
            </Paper>
          </Grid>
          <Grid item xs={12}>
            <Paper className={classes.paper} elevation={10}>
              <OptionPriceDistribution mean={usPrice} stdDev={euStdev} />
            </Paper>
          </Grid>
        </Grid>
      </Grid>

      <Grid item xs={12} lg={8}>
        <Paper className={classes.paper} elevation={10}>
          {calculating ?
            <div className={classes.progressContainer}>
              <CircularProgress style={{color: customTheme.palette.secondary}} />
            </div>
          :
            <>
              <StockPriceChart paths={paths} strikePrice={strikePrice} />
            </>
          }
        </Paper>
      </Grid>
    </Grid>
  )
}

export default OptionsPricerDashboard