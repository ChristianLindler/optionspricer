import React, { useEffect, useRef, useState } from 'react'
import Chart from 'chart.js/auto'
import ChartAnnotationsPlugin from 'chartjs-plugin-annotation'
import { theme } from '../../../theme'
Chart.register(ChartAnnotationsPlugin)

const OptionPriceDistribution = ({ mean, stdDev }) => {
  const chartRef = useRef(null)
  const chartInstance = useRef(null)

  useEffect(() => {
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
            borderWidth: 1,
            backgroundColor: theme.colors.lighterSecondary,
            fill: true,
            borderColor: theme.colors.secondary,
            borderWidth: 3,
            label: 'Probability Density',
            pointStyle: 'none',
            pointRadius: 0
          },
        ],
      },
      options: {
        plugins: {
          legend: {
            display: false,
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

  return <canvas ref={chartRef} />
}

export default OptionPriceDistribution