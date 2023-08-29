import { useState } from 'react'
import './App.css'
import Header from './components/Header'
import OptionsPricerDashboard from './components/OptionsPricerDashboard'
import { theme } from './theme'
import { makeStyles } from '@material-ui/core'

const useStyles = makeStyles({
  app: {
    backgroundColor: theme.colors.background,
  },
  content: {
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
    <main className='content'>
      <div className={classes.app}>
        <Header activePage={activePage} setActivePage={setActivePage} />
        <div className={classes.content}>
          {activePage === 'dashboard' ? 
            <OptionsPricerDashboard className={classes.dashboard}/>
          :
            <h1/>
          }
        </div>
      </div>
    </main>
  )
}

export default App
