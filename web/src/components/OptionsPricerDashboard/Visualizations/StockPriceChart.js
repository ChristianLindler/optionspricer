import React, { useEffect, useRef } from 'react'
import Chart from 'chart.js/auto'
import ChartAnnotationsPlugin from 'chartjs-plugin-annotation'
Chart.register(ChartAnnotationsPlugin)

const numSamplePaths = 100

const StockPriceChart = ({ paths, strikePrice }) => {
  paths = paths.length > numSamplePaths ? paths.slice(0, numSamplePaths) : paths
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
    if (chartRef.current && paths) {
      const ctx = chartRef.current.getContext('2d')

      // Destroy the previous chart if it exists
      if (chartInstance.current) {
        chartInstance.current.destroy()
      }

      chartInstance.current = new Chart(ctx, {
        type: 'line',
        data: {
          labels: [...Array(paths[0].length).keys()], 
          datasets: paths.map((path) => ({
            data: path,
            borderWidth: 1,
            fill: false,
            label: '',
            pointStyle: 'none',
            radius: 0
          })),
        },
        options: {
          plugins: {
            legend: {
              display: false,
            },
            annotation: {
              annotations: [
                {
                  type: 'line',
                  mode: 'horizontal',
                  scaleID: 'y',
                  value: strikePrice,
                  borderColor: 'red',
                  borderWidth: 1,
                  label: {
                    enabled: true,
                    content: 'Strike Price',
                  },
                },
              ],
            }
          }
        }
      })
    }
  }, [paths, strikePrice])

  return <canvas ref={chartRef} width={'100%'}/>
}


export default StockPriceChart




