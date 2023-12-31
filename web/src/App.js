import { useState } from 'react'
import './App.css'
import Header from './components/Header'
import OptionsPricerDashboard from './components/OptionsPricerDashboard'
import { theme } from './theme'
import { makeStyles } from '@material-ui/core'
import ModelExplanation from './components/ModelExplanation'
import Footer from './components/Footer'

const useStyles = makeStyles({
  app: {
    backgroundColor: theme.palette.background,
    minHeight: '100vh', // Make sure the content covers at least one screen height
    display: 'flex',
    flexDirection: 'column',
  },
  content: {
    flex: 1, // Allow content to grow and take remaining space
    marginTop: 10,
    alignItems: 'center',
    display: 'flex',
    flexDirection: 'column',
  },
})

function App() {
  const classes = useStyles()
  const [activePage, setActivePage] = useState('dashboard')

  return (
    <div className={classes.app}>
      <Header activePage={activePage} setActivePage={setActivePage} />
      <div className={classes.content}>
        {activePage === 'dashboard' ? 
          <OptionsPricerDashboard className={classes.dashboard} />
        :
          <ModelExplanation />
        }
      </div>
      <Footer />
    </div>
  )
}

export default App