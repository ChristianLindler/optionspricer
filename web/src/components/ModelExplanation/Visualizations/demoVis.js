import React, { useEffect, useRef } from 'react'
import Chart from 'chart.js/auto'
import ChartAnnotationsPlugin from 'chartjs-plugin-annotation'
Chart.register(ChartAnnotationsPlugin)

const numSamplePaths = 100

const DemoVis = ({ paths, annotationX, annotationY }) => {
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
          datasets: chartPaths.map((path) => ({
            data: path,
            borderWidth: 1,
            fill: false,
            label: '',
            pointStyle: 'none',
            radius: 0,
          })),
        },
        options: {
          plugins: {
            legend: {
              display: false,
            },
            annotation: {
              annotations: [],
            },
          },
        },
      })

      // Add annotation if annotationX and annotationY are provided
      if (annotationX !== undefined && annotationY !== undefined) {
        const annotation = {
          type: 'point',
          xScaleID: 'x',
          yScaleID: 'y',
          xValue: annotationX,
          yValue: annotationY,
          borderColor: 'red',
          borderWidth: 2,
          radius: 5,
        }

        chartInstance.current.options.plugins.annotation.annotations.push(annotation)
        chartInstance.current.update()
      }
    }
  }, [paths, annotationX, annotationY])

  // Validate and sanitize paths data for early return
  if (!paths || !Array.isArray(paths) || paths.length === 0) {
    return <div>No valid price paths available</div>
  }
  
  // Ensure paths is a 2D array with valid data
  const validPaths = paths.filter(path => 
    Array.isArray(path) && path.length > 0 && 
    path.every(price => typeof price === 'number' && !isNaN(price))
  )
  
  if (validPaths.length === 0) {
    return <div>No valid price paths available</div>
  }

  return <canvas ref={chartRef} width={'100%'} />
}

export default DemoVis