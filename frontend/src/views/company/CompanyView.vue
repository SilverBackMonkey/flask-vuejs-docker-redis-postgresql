<template>
  <Container>
    <Header :company="company" />
    <div class="company-summary">
      <div class="company-summary-left">
        <FinancialPerformance :company="company" />
        <Notes />
      </div>
      <div class="company-summary-right">
        <Calculator :company="company" />
        <Valuation :company="company" />
      </div>
    </div>
    <Summary :company="company" />
    <Financials id="financials" :company="company" />
    <ValueEstimate :company="company" />
    <Reports :company="company" />
  </Container>
  <ForecastModal v-on:save="createForecast" />
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRoute } from 'vue-router';

import { useCompany } from '@/controllers/company';

import { LOADING, HIDE_MODAL } from '@/store/actions/application';

import Container from '@/components/ContainerComponent.vue';

import ForecastModal from '@/components/modals/ForecastModal.vue';

import Header from './CompanyHeader.vue';
import FinancialPerformance from './CompanyFinancialPerformance.vue';
import Calculator from './CompanyCalculator.vue';
import Valuation from './CompanyValuation.vue';
import Summary from './CompanySummary.vue';
import Financials from './financials';
import Notes from './CompanyNotes.vue';
import ValueEstimate from './value-estimate';
import Reports from './CompanyReports.vue';

export default defineComponent({
  name: 'CompanyView',
  components: {
    Container,
    ForecastModal,
    Header,
    FinancialPerformance,
    Calculator,
    Valuation,
    Summary,
    Financials,
    Notes,
    ValueEstimate,
    Reports,
  },
  setup() {
    const store = useStore();
    const route = useRoute();
    const symbol = route.params.symbol as string;
    const company = useCompany(symbol);

    store.commit(LOADING, true);

    const createForecast = (name: string) => {
      company.createForecast(name).then(() => {
        store.commit(HIDE_MODAL);
      });
    };

    onMounted(() => {
      company.update().finally(() => {
        store.commit(LOADING, false);
      });
    });

    return {
      company,
      createForecast,
    };
  },
});
</script>

<style>
.company-summary {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.company-summary > .company-summary-left {
  flex: 1;
}

.company-summary > .company-summary-right {
  flex: 0 0 467px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
</style>
