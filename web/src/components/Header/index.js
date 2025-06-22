import React from 'react'
import { AppBar, Toolbar, Typography, Button, makeStyles, useMediaQuery, useTheme } from '@material-ui/core'
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
  },
  mobileToolbar: {
    flexDirection: 'column',
    alignItems: 'flex-start',
    padding: '8px 16px',
  },
  mobileButtons: {
    display: 'flex',
    flexDirection: 'column',
    width: '100%',
    marginTop: '8px',
  },
  mobileButton: {
    justifyContent: 'flex-start',
    padding: '4px 0',
    minHeight: '32px',
  }
}))

const Header = ({ activePage, setActivePage }) => {
  const classes = useStyles()
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'))

  const handlePageChange = (page) => {
    setActivePage(page)
  }

  return (
    <AppBar position='static' className={classes.header}>
      <Toolbar className={isMobile ? classes.mobileToolbar : ''}>
        <Typography className={classes.title}>
          Options Pricing with the Heston Model
        </Typography>
        {isMobile ? (
          <div className={classes.mobileButtons}>
            <Button
              className={`${classes.button} ${classes.mobileButton}`}
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
              className={`${classes.button} ${classes.mobileButton}`}
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
              className={`${classes.button} ${classes.mobileButton}`}
              style={{
                color: theme.palette.text,
              }}
              onClick={() => window.location.href='https://github.com/ChristianLindler/optionspricer'}
            >
              GitHub
            </Button>
          </div>
        ) : (
          <>
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
          </>
        )}
      </Toolbar>
    </AppBar>
  )
}

export default Header