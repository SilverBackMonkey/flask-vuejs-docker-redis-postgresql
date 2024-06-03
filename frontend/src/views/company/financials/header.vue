<template>
  <div class="financials-header">
    <div class="financials-title">
      <h1>Financials</h1>
      <p>all figures in US$ Millions except per share data</p>
    </div>
    <div class="financials-control financials-control__type">
      <Button
        v-for="(type, index) in typeControl"
        :key="index"
        :type="selectedType === type ? 'secondary' : 'transparent'"
        size="small"
        @click="changeType(type)"
      >{{ type }}</Button>
    </div>
    <div class="financials-control">
      <p>Periods:</p>
      <div class="financials-control-values">
        <Button
          v-for="(period, index) in periodControl"
          :key="index"
          :disabled="selectedPeriod !== period"
          type="transparent"
          size="small"
        >{{ period }}</Button>
      </div>
    </div>
    <div class="financials-control">
      <p>View:</p>
      <div class="financials-control-values">
        <Button
          v-for="(view, index) in viewControl"
          :key="index"
          :disabled="selectedView !== view"
          type="transparent"
          size="small"
        >{{ view }}</Button>
      </div>
    </div>
    <div class="financials-control">
      <p>Forecast:</p>
      <div class="financials-control-values">
        <Button
          v-for="(forecast, index) in forecastControl"
          :key="index"
          :visually-disabled="selectedForecast !== forecast"
          type="transparent"
          size="small"
          @click="company.setForecast(
            forecast === forecastControl.CUSTOM ? company.forecasts[0] : undefined
          )"
        >{{ forecast }}</Button>
      </div>
    </div>
    <div class="financials-control">
      <p>ㅤ</p>
      <div class="financials-control-values">
        Show forecast vs demo <Checkbox v-model:value="isCompare" />
      </div>
    </div>
    <Button
      style="cursor: pointer !important;"
      :visually-disabled="isCommentEnabled"
      @click="toggleComment"
    >Add comment</Button>
  </div>
</template>

<script lang="ts">
import {
  defineComponent,
  ref,
  computed,
  PropType,
} from 'vue';
import { useStore } from 'vuex';

import Button from '@/components/ui/ButtonComponent.vue';
import Checkbox from '@/components/ui/CheckboxComponent.vue';

import { CompanyController } from '@/controllers/company/types';

import { COMMENT_CURSOR } from '@/store/actions/application';

import * as controls from './data/controls';

export default defineComponent({
  name: 'FinancialsHeader',
  components: {
    Button,
    Checkbox,
  },
  props: {
    company: {
      type: Object as PropType<CompanyController>,
      required: true,
    },
  },
  setup(props) {
    const store = useStore();

    const isCompare = ref(false);
    const selectedType = ref(localStorage.getItem('financials-type') || controls.typeControl.TABLE);
    const selectedPeriod = ref(localStorage.getItem('financials-period') || controls.periodControl.ANNUAL);
    const selectedView = ref(localStorage.getItem('financials-view') || controls.viewControl.EXTENDED);

    const selectedForecast = computed(() => {
      if (props.company.forecast.value !== undefined) {
        return 'custom';
      }
      return 'averages';
    });

    const changeType = (newType: controls.typeControl) => {
      localStorage.setItem('financials-type', newType);
      selectedType.value = newType;
    };

    const changePeriod = (newPeriod: controls.typeControl) => {
      localStorage.setItem('financials-period', newPeriod);
      selectedPeriod.value = newPeriod;
    };

    const changeView = (newView: controls.typeControl) => {
      localStorage.setItem('financials-view', newView);
      selectedView.value = newView;
    };

    const isCommentEnabled = computed(() => store.state.application.commentCursor);

    const toggleComment = () => {
      store.commit(COMMENT_CURSOR, !store.state.application.commentCursor);
    };

    return {
      isCompare,
      selectedType,
      selectedPeriod,
      selectedView,
      selectedForecast,
      ...controls,
      changeType,
      changePeriod,
      changeView,
      isCommentEnabled,
      toggleComment,
    };
  },
});
</script>

<style scoped>
.financials-header {
  display: flex;
  flex-wrap: wrap;
  column-gap: 24px;
  grid-gap: 10px;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  margin-bottom: 20px;
}

.financials-header > .financials-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.financials-header > .financials-title > p {
  font-size: 12px;
  color: var(--theme-text-color-2);
  max-width: 134px;
  line-height: 14px;
}

.financials-header > .financials-control.financials-control__type {
  display: flex;
  align-items: center;
}

.financials-header > .financials-control.financials-control__type > button {
  padding: 5px 16px !important;
}

.financials-header > .financials-control > p {
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 2px;
  text-transform: uppercase;
}

.financials-header > .financials-control > .financials-control-values {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 600;
  color: var(--theme-link-color);
  text-transform: uppercase;
}

.financials-header > .financials-control > .financials-control-values > * {
  cursor: pointer;
}

@media screen and (max-width: 1352px) {
  .financials-header,
  .financials-header p,
  .financials-header button,
  .financials-header > .financials-control > .financials-control-values {
    font-size: 10px !important;
  }
}

@media screen and (max-width: 1220px) {
  .financials-header > button {
    padding: 9px 18px !important;
  }

  .financials-header > .financials-control.financials-control__type > button {
    padding: 4px 14px !important;
  }
}
</style>
