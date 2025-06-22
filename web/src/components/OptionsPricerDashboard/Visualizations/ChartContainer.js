import React from 'react'
import { makeStyles } from '@material-ui/core'
import { theme as customTheme } from '../../../theme'

const useStyles = makeStyles({
  container: {
    position: 'relative',
    width: '100%',
    height: '360px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  shortContainer: {
    position: 'relative',
    width: '100%',
    height: '200px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  noDataContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100%',
    color: customTheme.charts.colors.textSecondary,
    fontFamily: customTheme.charts.fontFamily,
    fontSize: customTheme.charts.fontSize.medium,
    textAlign: 'center',
    padding: '20px',
  },
  noDataIcon: {
    fontSize: '48px',
    marginBottom: '12px',
    opacity: 0.5,
  },
  noDataText: {
    margin: '0',
    fontWeight: 400,
  },
  canvas: {
    width: '100% !important',
    height: '100% !important',
  },
})

const ChartContainer = ({ children, hasData, title, subtitle, short = false }) => {
  const classes = useStyles()

  if (!hasData) {
    return (
      <div className={short ? classes.shortContainer : classes.container}>
        <div className={classes.noDataContainer}>
          <h4 className={classes.noDataText}>{title || 'No Data Available'}</h4>
          {subtitle && <p className={classes.noDataText}>{subtitle}</p>}
        </div>
      </div>
    )
  }

  return (
    <div className={short ? classes.shortContainer : classes.container}>
      {children}
    </div>
  )
}

export default ChartContainer 