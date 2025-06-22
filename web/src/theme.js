export const theme = {
    palette: {
        primary: '#222A3F',
        //secondary: '#7BCDB6',
        secondary: '#B179fE',
        lighterSecondary: 'rgba(180, 125, 260, 0.2)',
        background: '#151A2D',
        darkText: 'black',
        lightText: 'white',
        error: '#f44336',
        warning: '#ff9800',
        success: '#4caf50',
        info: '#2196f3',
    },
    typography: {
        fontFamily: {
            primary: 'Poppins, sans-serif',
            secondary: 'Open Sans, sans-serif',
        },
        fontSize: {
            xs: '12px',
            small: '14px',
            medium: '16px',
            large: '24px',
            xl: '32px',
        },
        fontWeight: {
            light: 300,
            regular: 400,
            medium: 500,
            bold: 700,
        },
    },
    spacing: {
        xs: '4px',
        small: '8px',
        medium: '16px',
        large: '24px',
        xl: '32px',
        xxl: '48px',
    },
    breakpoints: {
        mobile: '600px',
        tablet: '960px',
        desktop: '1280px',
    },
    shadows: {
        small: '0 2px 4px rgba(0,0,0,0.1)',
        medium: '0 4px 8px rgba(0,0,0,0.15)',
        large: '0 8px 16px rgba(0,0,0,0.2)',
    },
    borderRadius: {
        small: '4px',
        medium: '8px',
        large: '12px',
        xl: '16px',
    },
    components: {
        paper: {
            backgroundColor: '#222A3F',
            borderRadius: '12px',
            padding: '20px',
            boxShadow: '0 4px 8px rgba(0,0,0,0.15)',
        },
        coloredPaper: {
            backgroundColor: '#B179fE',
            borderRadius: '12px',
            padding: '20px',
            boxShadow: '0 4px 8px rgba(0,0,0,0.15)',
        },
        button: {
            backgroundColor: '#B179fE',
            color: 'white',
            borderRadius: '8px',
            padding: '12px 24px',
            border: 'none',
            cursor: 'pointer',
            transition: 'all 0.2s ease',
            '&:hover': {
                backgroundColor: '#9B6FE8',
                transform: 'translateY(-1px)',
            },
        },
        textField: {
            backgroundColor: 'rgba(255,255,255,0.05)',
            borderRadius: '8px',
            border: '1px solid rgba(255,255,255,0.1)',
            color: 'white',
            '&:focus': {
                borderColor: '#B179fE',
                boxShadow: '0 0 0 2px rgba(177, 121, 254, 0.2)',
            },
        },
    },
    charts: {
        fontFamily: 'Poppins, sans-serif',
        fontSize: {
            small: '11px',
            medium: '13px',
            large: '15px',
        },
        colors: {
            primary: '#B179fE',
            secondary: 'rgba(177, 121, 254, 0.3)',
            grid: 'rgba(255, 255, 255, 0.08)',
            text: 'rgba(255, 255, 255, 0.8)',
            textSecondary: 'rgba(255, 255, 255, 0.6)',
        },
        commonOptions: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false,
                },
            },
            scales: {
                x: {
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.8)',
                        font: {
                            family: 'Poppins, sans-serif',
                            size: 11,
                        },
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.08)',
                        drawBorder: false,
                    },
                    border: {
                        color: 'rgba(255, 255, 255, 0.1)',
                    },
                },
                y: {
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.8)',
                        font: {
                            family: 'Poppins, sans-serif',
                            size: 11,
                        },
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.08)',
                        drawBorder: false,
                    },
                    border: {
                        color: 'rgba(255, 255, 255, 0.1)',
                    },
                },
            },
        },
    },
}