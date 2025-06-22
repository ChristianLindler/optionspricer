import React from 'react'
import { useEffect, useRef } from 'react'
import { Chart } from 'chart.js/auto'
import { theme as customTheme } from '../../../theme'
import ChartContainer from './ChartContainer'

const StockReturnsHistogram = ({ paths, strikePrice, numBins }) => {
  const chartRef = useRef(null)
  const chartInstance = useRef(null)

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

    // Check if canvas element exists
    if (!chartRef.current) {
      return
    }

    const ctx = chartRef.current.getContext('2d')
    // Destroy the previous chart if it exists
    if (chartInstance.current) {
      chartInstance.current.destroy()
    }
    
    const returnsData = validPaths.map(path => path[path.length - 1] - strikePrice)

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
      labels: binRanges.map(range => range[0].toFixed(1)),
      datasets: [
        {
          label: 'Frequency',
          data: binCounts,
          backgroundColor: customTheme.charts.colors.primary,
          borderColor: customTheme.charts.colors.primary,
          borderWidth: 1,
          borderRadius: 2,
          borderSkipped: false,
        },
      ],
    }

    chartInstance.current = new Chart(ctx, {
      type: 'bar',
      data: chartData,
      options: {
        ...customTheme.charts.commonOptions,
        scales: {
          ...customTheme.charts.commonOptions.scales,
          y: {
            ...customTheme.charts.commonOptions.scales.y,
            beginAtZero: true,
            title: {
              display: true,
              text: 'Frequency',
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
              text: 'Returns on Final Day',
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
      },
    })
  }, [paths, strikePrice, numBins])

  // Check if we have valid data
  const hasValidData = paths && Array.isArray(paths) && paths.length > 0 && 
    paths.some(path => Array.isArray(path) && path.length > 0 && 
      path.every(price => typeof price === 'number' && !isNaN(price)))

  return (
    <ChartContainer 
      hasData={hasValidData}
      title="Returns Distribution"
      subtitle="Run a calculation to see the distribution of returns"
      short={true}
    >
      <canvas ref={chartRef} />
    </ChartContainer>
  )
}

export default StockReturnsHistogram