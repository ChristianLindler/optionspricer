import React from 'react'
import { AppBar, makeStyles } from '@material-ui/core'
import { theme } from '../../theme'

const useStyles = makeStyles(() => ({
  footer: {
    backgroundColor: theme.palette.primary,
    marginTop: 10,
    display: 'flex', // Add flex display
    justifyContent: 'space-between', // Align items horizontally
    alignItems: 'flex-start', // Align items vertically
    padding: '10px', // Add padding for better spacing
  },
  primaryText: {
    color: theme.palette.secondary,
    fontFamily: theme.typography.fontFamily.primary,
    fontSize: theme.typography.fontSize.small,
  },
  secondaryText: {
    color: theme.palette.text,
    fontFamily: theme.typography.fontFamily.secondary,
    fontSize: theme.typography.fontSize.xs,
    marginTop: '10px',
  },
}))

const Footer = () => {
  const classes = useStyles()

  return (
    <AppBar position='static' className={classes.footer}>
      <div className={classes.primaryText}>
        <a
          href='https://github.com/ChristianLindler/optionspricer'
          target='_blank'
          rel='noopener noreferrer'
          style={{ textDecoration: 'none', color: 'inherit' }}
        >
          GitHub
        </a>
      </div>
    </AppBar>
  )
}

export default Footer