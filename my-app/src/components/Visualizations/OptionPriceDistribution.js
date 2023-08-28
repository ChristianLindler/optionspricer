import React, { useEffect, useRef } from 'react'
import Chart from 'chart.js/auto'
import ChartAnnotationsPlugin from 'chartjs-plugin-annotation'
Chart.register(ChartAnnotationsPlugin)

const OptionPriceDistribution = ({ mean, stdDev }) => {
  const chartRef = useRef(null)
  const chartInstance = useRef(null)

  useEffect(() => {
    if (true) {
      const ctx = chartRef.current.getContext('2d')

      // Destroy the previous chart if it exists
      if (chartInstance.current) {
        chartInstance.current.destroy()
      }

      // Calculate PDF values based on mean and stdDev
      const xValues = []
      const pdfValues = []
      for (let x = mean - 3 * stdDev; x <= mean + 3 * stdDev; x += 0.1) {
        xValues.push(x.toFixed(2))
        pdfValues.push(
          calculateNormalDistributionPDF(x, mean, stdDev)
        );
      }

      chartInstance.current = new Chart(ctx, {
        type: 'line',
        data: {
          labels: xValues,
          datasets: [
            {
              data: pdfValues,
              borderWidth: 1,
              fill: false,
              borderColor: 'blue',
              label: 'PDF',
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
      });
    }
  }, [mean, stdDev])

  function calculateNormalDistributionPDF(x, mean, stdDev) {
    const a = 1 / (stdDev * Math.sqrt(2 * Math.PI))
    const b = Math.exp(-Math.pow(x - mean, 2) / (2 * Math.pow(stdDev, 2)))
    return a * b
  }

  return <canvas ref={chartRef} />
}

export default OptionPriceDistribution