import React, { useState } from 'react'
import { Grid, Paper, makeStyles } from '@material-ui/core'
import { theme } from '../../theme'
import explanationText from './explanationText'
import DemoVis from './Visualizations/demoVis'

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
  primaryText: {
    color: 'white',
    fontFamily: theme.typography.fontFamily.primary,
    fontSize: theme.typography.fontSize.large,
  },
  secondaryText: {
    color: 'white',
    fontFamily: theme.typography.fontFamily.secondary,
    fontSize: theme.typography.fontSize.medium,
  }
})

const ModelExplanation = () => {
  const classes = useStyles()

  return (
    <Grid container justifyContent='center' className={classes.container} spacing={3}>
      <Grid item xs={8}>
        <Paper className={classes.paper} elevation={10}>
          <h1 className={classes.primaryText}>{explanationText.p1.title}</h1>
          <p className={classes.secondaryText}>{explanationText.p1.content}</p>
        </Paper>
      </Grid>

      <Grid item xs={4}>
        <Paper className={classes.paper} elevation={10}>
          <DemoVis paths={[[0, 4, 3, 5, 4, 6, 5, 7, 9, 5, 7], [0, 3, 5, 6, 5, 8, 6, 8, 9, 5, 6]]}/>
        </Paper>
      </Grid>

      <Grid item xs={4}>
        <Paper className={classes.paper} elevation={10}>
          <DemoVis paths={[[0, 4, 3, 5, 4, 6, 5, 7, 9, 5, 7], [0, 3, 5, 6, 5, 8, 6, 8, 9, 5, 6]]}/>
        </Paper>
      </Grid>

      <Grid item xs={8}>
        <Paper className={classes.paper} elevation={10}>
          <h1 className={classes.primaryText}>{explanationText.p2.title}</h1>
          <p className={classes.secondaryText}>{explanationText.p2.content}</p>
        </Paper>
      </Grid>

      <Grid item xs={8}>
        <Paper className={classes.paper} elevation={10}>
          <h1 className={classes.primaryText}>{explanationText.p3.title}</h1>
          <p className={classes.secondaryText}>{explanationText.p3.content}</p>
        </Paper>
      </Grid>

      <Grid item xs={4}>
        <Paper className={classes.paper} elevation={10}>
          <DemoVis paths={[[0, 4, 3, 5, 4, 6, 5, 7, 9, 5, 7], [0, 3, 5, 6, 5, 8, 6, 8, 9, 5, 6]]}/>
        </Paper>
      </Grid>
    </Grid>
  )
}

export default ModelExplanation