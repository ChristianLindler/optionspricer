import React from 'react'
import { AppBar, Toolbar, Typography, Button, makeStyles } from '@material-ui/core'
import { theme } from '../../theme'

const useStyles = makeStyles(() => ({
  header: {
    backgroundColor: theme.palette.primary,
  },
  title: {
    color: theme.palette.secondary,
    fontFamily: theme.typography.fontFamily.primary,
    fontSize: theme.typography.fontSize.large,
    flexGrow: 1,
  },
  button: {
    fontFamily: theme.typography.fontFamily.primary,
    color: 'white'
  }
}))

const Header = ({ activePage, setActivePage }) => {
  const classes = useStyles()

  const handlePageChange = (page) => {
    setActivePage(page)
  }

  return (
    <AppBar position='static' className={classes.header}>
      <Toolbar>
        <Typography className={classes.title}>
          Options Pricing with the Heston Model
        </Typography>
        <Button
          className={classes.button}
          style={{
            color:
              activePage === 'dashboard'
                ? theme.palette.secondary
                : theme.palette.text,
          }}
          onClick={() => handlePageChange('dashboard')}
          
        >
          Options Pricer
        </Button>
        <Button
          className={classes.button}
          style={{
            color:
              activePage === 'behindTheModel'
                ? theme.palette.secondary
                : theme.palette.text,
          }}
          onClick={() => handlePageChange('behindTheModel')}
        >
          Behind the Model
        </Button>
        <Button
          className={classes.button}
          style={{
            color: theme.palette.text,
          }}
          onClick={() => window.location.href='https://github.com/ChristianLindler/optionspricer'}
        >
          GitHub
        </Button>
      </Toolbar>
    </AppBar>
  )
}

export default Header