import {
  ref,
  computed,
  reactive,
  watch,
  Ref,
} from 'vue';

import {
  ChartData as ChartJSData,
  ChartOptions,
  ChartDataset,
} from 'chart.js';

import { CompanyController } from '@/controllers/company/types';
import { Chart, ChartData } from '@/rest-api/companies/assets';

export const useChart = ( // eslint-disable-line
  type: Ref<string>,
  period: Ref<string>,
  initialOptions: ChartOptions,
  company: CompanyController,
) => {
  const loading = ref(true);
  const reactiveDataset: ChartDataset<'line'>[] = reactive([]);
  const data: ChartJSData<'line'> = {
    labels: [],
    datasets: [],
  };

  const options = computed(() => {
    const opt = { ...initialOptions };

    if (!opt.scales || !opt.scales['y-right'] || !opt.scales['y-right'].ticks) {
      console.log('not found');
      return opt;
    }

    if (!reactiveDataset.some((row) => row.yAxisID === 'y-right')) {
      opt.scales['y-right'].ticks.display = false;
    } else {
      opt.scales['y-right'].ticks.display = true;
    }

    return opt;
  });

  const createDataset = (label: string, values: ChartData[], color: string, axis: string) => {
    const dataset: number[] = [];

    for (let i = 0; i < values.length; i += 1) {
      if (!data.labels?.includes(values[i].label)) {
        data.labels?.push(values[i].label);
      }

      if (type.value === 'rebased') {
        if (i === 0) {
          dataset.push(0);
        } else {
          dataset.push(values[i].value / values[0].value - 1);
        }
      } else {
        dataset.push(values[i].value);
      }
    }

    const object = {
      label,
      data: dataset,
      yAxisID: axis,
      borderWidth: 3,
      pointRadius: 0,
      borderColor: color,
      fill: true,
      backgroundColor: 'transparent',
    };

    if (dataset.length > 0) {
      reactiveDataset.push(object);
      data.datasets?.push(object);
    }
  };

  const update = () => {
    loading.value = true;

    data.labels = [];
    data.datasets = [];
    reactiveDataset.splice(0);

    company.getChartData(period.value).then((payload) => {
      Object.keys(payload).forEach((key) => {
        const chartKey = key as keyof Chart;
        let label: string;
        let color: string;
        let axis = 'y-right';

        switch (chartKey) {
          case 'stockPrice':
            label = 'Stock price';
            color = '#9650FB';
            axis = 'y-left';
            break;
          case 'freeCashFlowPerShare':
            label = 'Free cash flow per share';
            color = '#3348FB';
            axis = type.value === 'rebased' ? 'y-left' : 'y-right';
            break;
          case 'earningsPerShare':
            label = 'Earnings per share';
            color = '#37D27F';
            axis = type.value === 'rebased' ? 'y-left' : 'y-right';
            break;
          default:
            return;
        }

        createDataset(label, payload[chartKey], color, axis);
      });
    }).finally(() => {
      loading.value = false;
    });
  };

  const computedData = computed(() => data);

  watch(() => [period.value, type.value], update);

  update();

  return {
    loading,
    options,
    data: computedData,
  };
};
