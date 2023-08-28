import './App.css';
import OptionsPricerDashboard from './components/OptionsPricerDashboard'
import { ColorModeContext, useMode } from './theme'
import { ThemeProvider, CssBaseline } from '@material-ui/core'

function App() {
  const [theme, colorMode] = useMode()
  return (
    //<ColorModeContext.Provider value={colorMode}>
      //<ThemeProvider theme={theme}>
        //<CssBaseline>
          <main className='content'>
            <div className="App">
              <h1 className="mt-5 mb-4">Monte Carlo Options Pricer</h1>
              <OptionsPricerDashboard />
            </div>
          </main>
        //</CssBaseline>
      //</ThemeProvider>
    //</ColorModeContext.Provider>
  );
}

export default App;
