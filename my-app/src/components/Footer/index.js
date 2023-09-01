import React from 'react'
import { AppBar, Toolbar, Typography, makeStyles } from '@material-ui/core'
import { theme } from '../../theme'

const useStyles = makeStyles(() => ({
  footer: {
    backgroundColor: theme.colors.primary,
    marginTop: 10,
    display: 'flex', // Add flex display
    justifyContent: 'space-between', // Align items horizontally
    alignItems: 'flex-start', // Align items vertically
    padding: '10px', // Add padding for better spacing
  },
  primaryText: {
    color: theme.colors.secondary,
    fontFamily: theme.typography.fontFamily.primary,
    fontSize: theme.typography.fontSize.small,
  },
  secondaryText: {
    color: theme.colors.text,
    fontFamily: theme.typography.fontFamily.secondary,
    fontSize: theme.typography.fontSize.xs,
    marginTop: '10px',
  },
  diagonalSplit: {
    flex: '1', // Take up half of the available space
    background: `linear-gradient(to bottom right, ${theme.colors.primary} 50%, transparent 50%)`, // Diagonal split
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
      <div className={classes.diagonalSplit} />
    </AppBar>
  )
}

export default Footer