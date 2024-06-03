import { ChartOptions } from 'chart.js';

const chartOptions: ChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false,
    },
    tooltip: {
      displayColors: false,
      backgroundColor: 'rgba(0, 0, 0, 0.65)',
      titleFont: {
        size: 12,
        family: 'Gilroy',
      },
      bodyFont: {
        size: 12,
        family: 'Gilroy',
        style: 'normal',
      },
    },
  },
  interaction: {
    intersect: false,
    mode: 'index',
  },
  scales: {
    'y-right': {
      type: 'linear',
      position: 'right',
      grid: {
        display: false,
      },
      border: {
        display: false,
      },
      ticks: {
        display: true,
        padding: 10,
        color: '#808080',
        font: {
          size: 10,
          family: 'Gilroy',
          style: 'normal',
          lineHeight: 2,
        },
        callback: (tickValue, index, ticks) => (typeof tickValue === 'number' && tickValue < 0 ? `(${Math.abs(tickValue)})` : tickValue),
      },
    },
    'y-left': {
      type: 'linear',
      position: 'left',
      grid: {
        display: true,
        drawOnChartArea: true,
        drawTicks: false,
      },
      border: {
        display: false,
      },
      ticks: {
        display: true,
        padding: 10,
        color: '#808080',
        font: {
          size: 10,
          family: 'Gilroy',
          style: 'normal',
          lineHeight: 2,
        },
        callback: (tickValue, index, ticks) => {
          if (typeof tickValue === 'number') {
            const value = tickValue / 10e5;

            if (value < 0) {
              return `(${Math.abs(value).toLocaleString()})`;
            }

            return value.toLocaleString();
          }

          return tickValue;
        },
      },
    },
    x: {
      offset: true,
      grid: {
        display: false,
      },
      border: {
        display: false,
      },
      ticks: {
        display: true,
        color: '#808080',
        padding: 20,
        font: {
          size: 10,
          family: 'Gilroy',
          style: 'normal',
          lineHeight: 2,
        },
      },
    },
  },
};

export default chartOptions;
