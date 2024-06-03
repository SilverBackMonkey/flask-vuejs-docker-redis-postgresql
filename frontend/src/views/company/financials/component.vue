<template>
  <div class="financials">
    <Header :company="company" ref="controls" />
    <Table
      ref="table"
      :company="company"
      :forecast="controls ? controls.selectedForecast : forecastControl.AVERAGES"
      :class="{
        'financials-disabled': !controls || controls.selectedType !== typeControl.TABLE
      }"
    />
    <Chart
      :company="company"
      :data="table && table.tableData"
      :class="{
        'financials-disabled': !controls || controls.selectedType !== typeControl.CHART
      }"
    />
  </div>
</template>

<script lang="ts">
import {
  defineComponent,
  PropType,
  ref,
} from 'vue';

import { CompanyController } from '@/controllers/company/types';

import Header from './header.vue';
import Table from './table.vue';
import Chart from './chart.vue';

import { typeControl, forecastControl } from './data/controls';

export default defineComponent({
  name: 'CompanyFinancials',
  components: {
    Header,
    Table,
    Chart,
  },
  props: {
    company: {
      type: Object as PropType<CompanyController>,
      required: true,
    },
  },
  setup() {
    const controls = ref();
    const table = ref();

    return {
      controls,
      table,
      forecastControl,
      typeControl,
    };
  },
});
</script>

<style>
.financials {
  margin-bottom: 32px;
}

.financials .financials-disabled {
  display: none;
}
</style>
