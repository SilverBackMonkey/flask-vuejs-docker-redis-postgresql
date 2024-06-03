<template>
  <div class="company-chart">
    <div class="company-chart-header">
      <template v-if="type === 'rebased'">
        <p>%</p>
        <p>ㅤ</p>
      </template>
      <template v-else>
        <p>US$<br></p>
        <p v-if="data.datasets.some((row) => row.yAxisID === 'y-right')">US$ Per<br>Share</p>
      </template>
    </div>
    <div class="company-chart-wrapper">
      <div class="company-chart-wrapper-preloader" v-if="loading">
        <VueSpinner size="40" color="var(--theme-link-color)" />
      </div>
      <Line :data="data" :options="options" v-if="!loading" />
    </div>
    <ul class="company-chart-legend">
      <li
        v-for="(item, index) in data.datasets"
        :key="index"
      >
        <span :style="{background: item.borderColor as string}"></span>
        <p>{{ item.label }}</p>
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import {
  defineComponent,
  PropType,
  computed,
} from 'vue';

import { Line } from 'vue-chartjs';
import { VueSpinner } from 'vue3-spinners';

import { companyChartOptions } from '@/data/chart';

import { CompanyController } from '@/controllers/company/types';

import { useChart } from './controller';

export default defineComponent({
  name: 'CompanyChart',
  components: {
    Line,
    VueSpinner,
  },
  props: {
    type: {
      type: String,
      enum: ['rebased', 'absolut'],
      default: 'absolut',
    },
    period: {
      type: String,
      enum: ['10Y', '5Y', '1Y', '6M', '1M', '5D', '1D'],
      default: '10Y',
    },
    company: {
      type: Object as PropType<CompanyController>,
      required: true,
    },
  },
  setup(props) {
    const type = computed(() => props.type);
    const period = computed(() => props.period);

    const { loading, data, options } = useChart(type, period, companyChartOptions, props.company);

    return {
      data,
      loading,
      options,
    };
  },
});
</script>

<style>
.company-chart {
  max-width: 100%;
  width: 100%;
}

.company-chart > .company-chart-wrapper {
  position: relative;
  height: 420px;
}

.company-chart > .company-chart-wrapper > .company-chart-wrapper-preloader {
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 2;
  background: var(--theme-text-color-contrast);
}

.company-chart > .company-chart-wrapper > canvas {
  max-width: 100% !important;
  width: 100% !important;
}

.company-chart > .company-chart-legend {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  list-style-type: none;
  padding: 0 20px;
  height: 16px;
}

.company-chart > .company-chart-legend > li {
  display: flex;
  align-items: center;
  gap: 8px;
}

.company-chart > .company-chart-legend > li > span {
  display: block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.company-chart > .company-chart-legend > li > p {
  font-size: 12px;
  font-weight: 600;
  color: var(--theme-text-color-2);
}

.company-chart > .company-chart-header {
  padding: 0 0 0 15px;
  flex: 0 0 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.company-chart > .company-chart-header > p {
  font-size: 10px;
  font-weight: 400;
  color: var(--theme-text-color-2);
  text-transform: uppercase;
}
</style>
