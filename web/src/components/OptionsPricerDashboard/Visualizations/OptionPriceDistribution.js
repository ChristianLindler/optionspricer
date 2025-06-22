import React, { useEffect, useRef } from 'react'
import Chart from 'chart.js/auto'
import ChartAnnotationsPlugin from 'chartjs-plugin-annotation'
import { theme as customTheme } from '../../../theme'
import ChartContainer from './ChartContainer'

Chart.register(ChartAnnotationsPlugin)

const OptionPriceDistribution = ({ mean, stdDev }) => {
  const chartRef = useRef(null)
  const chartInstance = useRef(null)

  useEffect(() => {
    // Check if canvas element exists
    if (!chartRef.current) {
      return
    }

    const ctx = chartRef.current.getContext('2d')

    // Destroy the previous chart if it exists
    if (chartInstance.current) {
      chartInstance.current.destroy()
    }

    // Calculate PDF values based on mean and stdDev
    const xValues = []
    const pdfValues = []
    for (let x = mean - 3 * stdDev; x <= mean + 3 * stdDev; x += stdDev/20) {
      xValues.push(x.toFixed(2))
      pdfValues.push(
        calculateNormalDistributionPDF(x, mean, stdDev)
      )
    }

    chartInstance.current = new Chart(ctx, {
      type: 'line',
      data: {
        labels: xValues,
        datasets: [
          {
            data: pdfValues,
            backgroundColor: customTheme.charts.colors.secondary,
            fill: true,
            borderColor: customTheme.charts.colors.primary,
            borderWidth: 2,
            label: 'Probability Density',
            pointStyle: 'none',
            pointRadius: 0,
            tension: 0.4,
          },
        ],
      },
      options: {
        ...customTheme.charts.commonOptions,
        scales: {
          ...customTheme.charts.commonOptions.scales,
          y: {
            ...customTheme.charts.commonOptions.scales.y,
            beginAtZero: true,
            title: {
              display: true,
              text: 'Probability Density',
              color: customTheme.charts.colors.text,
              font: {
                size: 13,
                family: customTheme.charts.fontFamily,
                weight: '500',
              },
            },
          },
          x: {
            ...customTheme.charts.commonOptions.scales.x,
            title: {
              display: true,
              text: 'Option Price',
              color: customTheme.charts.colors.text,
              font: {
                size: 13,
                family: customTheme.charts.fontFamily,
                weight: '500',
              },
            },
          },
        },
        plugins: {
          ...customTheme.charts.commonOptions.plugins,
        },
        elements: {
          point: {
            radius: 0,
          },
        },
      },
    })
  }, [mean, stdDev])

  function calculateNormalDistributionPDF(x, mean, stdDev) {
    const a = 1 / (stdDev * Math.sqrt(2 * Math.PI))
    const b = Math.exp(-Math.pow(x - mean, 2) / (2 * Math.pow(stdDev, 2)))
    return a * b
  }

  // Check if we have valid data
  const hasValidData = typeof mean === 'number' && typeof stdDev === 'number' && 
    !isNaN(mean) && !isNaN(stdDev) && stdDev > 0

  return (
    <ChartContainer 
      hasData={hasValidData}
      title="Option Price Distribution"
      subtitle="Run a calculation to see the probability distribution"
      short={true}
    >
      <canvas ref={chartRef} />
    </ChartContainer>
  )
}

export default OptionPriceDistribution