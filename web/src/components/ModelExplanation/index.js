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
  primaryText: {
    color: 'white',
    fontFamily: theme.typography.fontFamily.primary,
    fontSize: theme.typography.fontSize.large,
  },
  secondaryText: {
    color: 'white',
    fontFamily: theme.typography.fontFamily.secondary,
    fontSize: theme.typography.fontSize.medium,
  },
  button: {
    color: 'white',
    fontFamily: theme.typography.fontFamily.primary,
    backgroundColor: theme.palette.secondary
  },
})

const ModelExplanation = () => {
  const classes = useStyles()

  return (
    <Grid container justifyContent='center' className={classes.container} spacing={3}>
      <Grid item xs={8}>
        <Paper className={classes.paper} elevation={10}>
          <h1 className={classes.primaryText}>{explanationText.p1.title}</h1>
          <p className={classes.secondaryText}>{explanationText.p1.line1}</p>
          <p className={classes.secondaryText}>{explanationText.p1.line2}</p>
          <p className={classes.secondaryText}>{explanationText.p1.line3}</p>
        </Paper>
      </Grid>

      <Grid item xs={4}>
        <Paper className={classes.paper} elevation={10}>
          <p className={classes.primaryText}>Example Random Asset Path</p>
          <DemoVis paths={[[100, 99, 99, 98, 102, 104, 103, 101, 104, 106, 101, 102, 103, 102, 101, 107, 111, 110, 116, 116, 113, 112, 114, 117, 119, 119, 116, 117, 119, 119, 118, 120]]}/>
        </Paper>
      </Grid>

      <Grid item xs={4}>
        <Paper className={classes.paper} elevation={10}>
          <p className={classes.primaryText}>Correlated Brownian Motions</p>
          <DemoVis paths={[[-.0727, .01391, -0.0099, 0.0511, -0.01836, 0.0086, 0.1047, 0.0239, 0.0399, 0.0217, -0.0534, 0.0533, -0.0158, -0.063, 0.0267, 0.0102, 0.0402, 0.0929, -0.0453, -0.0287],
                           [ 0.089, .03884,  0.1002, 0.0059,  0.00067, -.0245, -.1166, -.0668, -0.061, -.0882,  0.0473, -.0197, 0.00986, -0.029, -.0022, -.0073, -.0671, -.0573, 0.03599, -0.0362]]}/>
        </Paper>
      </Grid>

      <Grid item xs={8}>
        <Paper className={classes.paper} elevation={10}>
          <h1 className={classes.primaryText}>{explanationText.p2.title}</h1>
          <p className={classes.secondaryText}>{explanationText.p2.line1}</p>
          <p className={classes.secondaryText}>{explanationText.p2.line2}</p>
          <p className={classes.secondaryText}>{explanationText.p2.line3}</p>
        </Paper>
      </Grid>

      <Grid item xs={8}>
        <Paper className={classes.paper} elevation={10}>
          <h1 className={classes.primaryText}>{explanationText.p3.title}</h1>
          <p className={classes.secondaryText}>{explanationText.p3.line1}</p>
          <p className={classes.secondaryText}>{explanationText.p3.line2}</p>
          <p className={classes.secondaryText}>{explanationText.p3.line3}</p>
          <p className={classes.secondaryText}>{explanationText.p3.line4}</p>
          <p className={classes.secondaryText}>{explanationText.p3.line5}</p>
          <p className={classes.secondaryText}>{explanationText.p3.line6}</p>
          <p className={classes.secondaryText}>{explanationText.p3.line7}</p>
        </Paper>
      </Grid>

      <Grid item xs={4}>
        <Paper className={classes.paper} elevation={10}>
          <p className={classes.primaryText}>Example Exercise</p>
          <DemoVis
            paths={[[100, 98, 96, 98, 100, 98, 97, 94, 94, 96, 93, 95, 93, 90, 92, 92, 91, 96, 93, 90, 86, 86, 88, 87],
                    [100, 99, 99, 98, 102, 104, 103, 101, 104, 106, 101, 102, 103, 102, 101, 107, 111, 110, 116]]}
            annotationX={18}
            annotationY={116}
          />
          <p className={classes.secondaryText}>In this example, we exercise the call option for the in-the-money path when its exercise value exceeds its continuation value. The out of the money path, on the other hand, is never excercised.</p>
        </Paper>
      </Grid>
    </Grid>
  )
}

export default ModelExplanation