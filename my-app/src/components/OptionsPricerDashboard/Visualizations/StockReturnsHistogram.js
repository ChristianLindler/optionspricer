import React from 'react'
import { useEffect, useRef } from 'react'
import { Chart } from 'chart.js/auto'
import { theme } from '../../../theme'

const StockReturnsHistogram = ({ paths, strikePrice, numBins }) => {
  const chartRef = useRef(null)
  const chartInstance = useRef(null)

  useEffect(() => {
    const ctx = chartRef.current.getContext('2d')
    // Destroy the previous chart if it exists
    if (chartInstance.current) {
      chartInstance.current.destroy()
    }
    const returnsData = paths.map(path => path[path.length - 1] - strikePrice)

    const [min, max] = [
      Math.min(...returnsData),
      Math.max(...returnsData),
    ]

    const binWidth = (max - min) / numBins
    const binRanges = Array.from({ length: numBins }, (_, i) => [
      min + i * binWidth,
      min + (i + 1) * binWidth,
    ])

    const binCounts = Array(numBins).fill(0)

    for (const ret of returnsData) {
      for (let i = 0; i < numBins; i++) {
        if (ret >= binRanges[i][0] && ret < binRanges[i][1]) {
          binCounts[i]++
          break
        }
      }
    }

    // Prepare chart data
    const chartData = {
      labels: binRanges.map(range => range[0].toFixed(2)),
      datasets: [
        {
          label: 'Frequency',
          data: binCounts,
          backgroundColor: theme.colors.secondary
        },
      ],
    }

    chartInstance.current = new Chart(ctx, {
      type: 'bar',
      data: chartData,
      options: {
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Frequency',
            },
          },
          x: {
            title: {
              display: true,
              text: 'Returns',
            },
          },
        },
      },
    })
  }, [paths, strikePrice, numBins])

  return (
    <div>
      <canvas ref={chartRef}></canvas>
    </div>
  )
}

export default StockReturnsHistogram