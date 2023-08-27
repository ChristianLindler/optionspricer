import React, { useEffect, useRef } from 'react'
import Chart from 'chart.js/auto'

function StockPriceChart({ paths }) {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    // Destroy the previous chart when the component is unmounted
    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
    };
  }, []);

  useEffect(() => {
    if (chartRef.current && Array.isArray(paths) && paths.length > 0) {
      const ctx = chartRef.current.getContext('2d');

      // Destroy the previous chart if it exists
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }

      chartInstance.current = new Chart(ctx, {
        type: 'line',
        data: {
          labels: [...Array(paths[0].length).keys()], 
          datasets: paths.map((path, index) => ({
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
          }
        }
      });
    }
  }, [paths]);

  return <canvas ref={chartRef} />;
}

export default StockPriceChart;




