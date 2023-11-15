import React, { useEffect, useRef } from 'react'
import Chart from 'chart.js/auto'
import ChartAnnotationsPlugin from 'chartjs-plugin-annotation'
Chart.register(ChartAnnotationsPlugin)

const numSamplePaths = 100

const DemoVis = ({ paths, annotationX, annotationY }) => {
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

  return <canvas ref={chartRef} width={'100%'} />
}

export default DemoVis