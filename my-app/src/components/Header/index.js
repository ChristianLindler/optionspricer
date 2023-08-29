import React from 'react'
import { AppBar, Toolbar, Typography, Button, makeStyles } from '@material-ui/core'
import { theme } from '../../theme'

const useStyles = makeStyles(() => ({
  header: {
    backgroundColor: theme.colors.primary,
  },
  title: {
    color: theme.colors.secondary,
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
          European Options Pricing with the Heston Model
        </Typography>
        <Button
          className={classes.button}
          style={{
            color:
              activePage === 'dashboard'
                ? theme.colors.secondary
                : theme.colors.text,
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
                ? theme.colors.secondary
                : theme.colors.text,
          }}
          onClick={() => handlePageChange('behindTheModel')}
        >
          Behind the Model
        </Button>
      </Toolbar>
    </AppBar>
  )
}

export default Header