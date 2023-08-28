import { createContext, useState, useMemo } from 'react'
import { createTheme } from '@material-ui/core'


export const tokens = {
    grey: {
        100: '#e0e0e0',
        200: '#c2c2c2',
        300: '#a3a3a3',
        400: '#858585',
        500: '#666666',
        600: '#525252',
        700: '#3d3d3d',
        800: '#292929',
        900: '#141414',
    },
    primary: {
        100: '#d0d1d5',
        200: '#a1a4ab',
        300: '#727681',
        400: '#434957',
        500: '#141b2d',
        600: '#101624',
        700: '#0c101b',
        800: '#080b12',
        900: '#040509',
    },
    violet: {
        100: '#f5ecff',
        200: '#ecd9ff',
        300: '#e2c5ff',
        400: '#d9b2ff',
        500: '#cf9fff',
        600: '#a67fcc',
        700: '#7c5f99',
        800: '#534066',
        900: '#292033',
    }
}
   
// mui theme
export const themeSettings = (mode) => {
    const colors = tokens
    const palette = {
        primary: {
          main: mode === 'dark' ? colors.primary[500] : colors.primary[900],
        },
        secondary: {
          main: mode === 'dark' ? colors.violet[700] : colors.violet[500],
        },
        neutral: {
          dark: colors.grey[700],
          main: colors.grey[500],
          light: colors.grey[100],
        },
        background: {
          default: mode === 'dark' ? colors.primary[500] : '#fcfcfc',
        },
      }
    const typography = {
        fontFamily: ['Source Sans Pro', 'sans-serif'].join(','),
        fontSize: 12,
        h1: {
            fontFamily: ['Source Sans Pro', 'sans-serif'].join(','),
            fontSize: 40,
        },
        h2: {
            fontFamily: ['Source Sans Pro', 'sans-serif'].join(','),
            fontSize: 32,
        },
        h3: {
            fontFamily: ['Source Sans Pro', 'sans-serif'].join(','),
            fontSize: 24,
        },
        h4: {
            fontFamily: ['Source Sans Pro', 'sans-serif'].join(','),
            fontSize: 20,
        },
        h5: {
            fontFamily: ['Source Sans Pro', 'sans-serif'].join(','),
            fontSize: 16,
        },
        h5: {
            fontFamily: ['Source Sans Pro', 'sans-serif'].join(','),
            fontSize: 14,
        },
    }
    return {
        palette: palette,
        typography: typography,
        mode: mode,
    }
}

export const ColorModeContext = createContext({
    toggleColorMode: () => {}
})

export const useMode = () => {
    const [mode, setMode] = useState('dark')

    const colorMode = useMemo(() => ({
        toggleColorMode: () => setMode((prev) => (prev === 'light') ? 'dark' : 'light')
    }), [])

    const theme = useMemo(() => createContext(themeSettings(mode)), [mode])
    return [theme, colorMode]
}