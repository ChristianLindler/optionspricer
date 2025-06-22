import React, { useEffect, useRef } from 'react'
import Chart from 'chart.js/auto'
import ChartAnnotationsPlugin from 'chartjs-plugin-annotation'
import { theme as customTheme } from '../../../theme'
import ChartContainer from './ChartContainer'

Chart.register(ChartAnnotationsPlugin)

const numSamplePaths = 100

const StockPriceChart = ({ paths, strikePrice }) => {
  const chartRef = useRef(null)
  const chartInstance = useRef(null)

  useEffect(() => {
    // Destroy the previous chart when the component is unmounted
    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy()
      }
    }
  }, [])

  useEffect(() => {
    // Validate and sanitize paths data
    if (!paths || !Array.isArray(paths) || paths.length === 0) {
      return
    }
    
    // Ensure paths is a 2D array with valid data
    const validPaths = paths.filter(path => 
      Array.isArray(path) && path.length > 0 && 
      path.every(price => typeof price === 'number' && !isNaN(price))
    )
    
    if (validPaths.length === 0) {
      return
    }
    
    const chartPaths = validPaths.length > numSamplePaths ? validPaths.slice(0, numSamplePaths) : validPaths

    // Check if canvas element exists
    if (!chartRef.current) {
      return
    }

    if (chartRef.current && chartPaths) {
      const ctx = chartRef.current.getContext('2d')

      // Destroy the previous chart if it exists
      if (chartInstance.current) {
        chartInstance.current.destroy()
      }

      chartInstance.current = new Chart(ctx, {
        type: 'line',
        data: {
          labels: [...Array(chartPaths[0].length).keys()], 
          datasets: chartPaths.map((path, index) => ({
            data: path,
            borderWidth: 1,
            borderColor: `hsl(${(index * 137.5) % 360}, 70%, 60%)`,
            backgroundColor: `hsla(${(index * 137.5) % 360}, 70%, 60%, 0.1)`,
            fill: false,
            label: '',
            pointStyle: 'none',
            radius: 0,
            tension: 0.1,
          })),
        },
        options: {
          ...customTheme.charts.commonOptions,
          plugins: {
            ...customTheme.charts.commonOptions.plugins,
            annotation: {
              annotations: [
                {
                  type: 'line',
                  mode: 'horizontal',
                  scaleID: 'y',
                  value: strikePrice,
                  borderColor: 'red',
                  borderWidth: 2,
                  borderDash: [5, 5],
                  label: {
                    enabled: true,
                    content: 'Strike Price',
                    color: customTheme.charts.colors.text,
                    font: {
                      size: 12,
                      family: customTheme.charts.fontFamily,
                      weight: '500',
                    },
                    position: 'end',
                    backgroundColor: 'rgba(0,0,0,0.7)',
                    padding: 6,
                    borderRadius: 4,
                  },
                },
              ],
            }
          },
          elements: {
            point: {
              radius: 0,
            },
          },
        }
      })
    }
  }, [paths, strikePrice])

  // Check if we have valid data
  const hasValidData = paths && Array.isArray(paths) && paths.length > 0 && 
    paths.some(path => Array.isArray(path) && path.length > 0 && 
      path.every(price => typeof price === 'number' && !isNaN(price)))

  return (
    <ChartContainer 
      hasData={hasValidData}
      title="Stock Price Paths"
      subtitle="Run a calculation to see simulated price paths (up to 100 paths shown)"
    >
      <canvas ref={chartRef} />
    </ChartContainer>
  )
}

export default StockPriceChart




