<template>
  <Container class="lists-container">
    <Header :list="list" v-on:update="update" />
    <Table :list="list" :updating="updating" v-model:period="period" />
  </Container>
</template>

<script lang="ts">
import {
  defineComponent,
  onMounted,
  ref,
  watch,
} from 'vue';
import { useStore } from 'vuex';
import { useRoute } from 'vue-router';

import * as api from '@/rest-api/lists';
import { List } from '@/rest-api/lists/assets';

import { LOADING } from '@/store/actions/application';

import Container from '@/components/ContainerComponent.vue';

import Header from './HeaderView.vue';
import Table from './TableView.vue';

export default defineComponent({
  name: 'ListView',
  components: {
    Container,
    Header,
    Table,
  },
  setup() {
    const store = useStore();
    const route = useRoute();

    const updating = ref(false);
    const period = ref('10Y');
    const list = ref<List>();

    store.commit(LOADING, true);

    const update = () => {
      updating.value = true;

      api.get(Number(route.params.id), period.value).then((payload) => {
        const receivedList = payload;

        receivedList.companies.forEach((company) => {
          const instance = company as any;

          if (period.value === '10Y') {
            instance.freeCashFlowGrowth = company.valuationAndEarnings.freeCashFlowPerShare10y;
            instance.earningsPerShareGrowth = company.valuationAndEarnings.earningsPerShare10y;
          } else if (period.value === '5Y') {
            instance.freeCashFlowGrowth = company.valuationAndEarnings.freeCashFlowPerShare5y;
            instance.earningsPerShareGrowth = company.valuationAndEarnings.earningsPerShare5y;
          } else {
            instance.freeCashFlowGrowth = company.valuationAndEarnings.freeCashFlowPerShareLtm;
            instance.earningsPerShareGrowth = company.valuationAndEarnings.earningsPerShareLtm;
          }

          instance.roa = '=financials.0.netIncome<this>/financials.0.totalAssets<this>*100';
          instance.roe = '=financials.0.netIncome<this>/financials.0.shareholdersEquity<this>*100';
        });

        list.value = receivedList;

        store.commit(LOADING, false);
        updating.value = false;
      });
    };

    watch(period, () => {
      update();
    });

    onMounted(() => {
      update();
    });

    return {
      list,
      period,
      updating,
      update,
    };
  },
});
</script>
