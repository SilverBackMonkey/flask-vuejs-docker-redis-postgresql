<template>
  <Table
    class="financials-table"
    :data="tableData"
    v-on:edit="onEditEvent"
    v-on:new-comment="createComment"
    v-on:edit-comment="saveComment"
    v-on:delete-comment="deleteComment"
  >
    <template #functions>
      <Button
        type="transparent"
        size="small"
        style="position: relative;"
        @click="forecastMenu = !forecastMenu"
      >
        {{
          company.forecast.value ?
          `${company.forecast.value.name} - ${
            new Date(company.forecast.value.updatedAt).toLocaleDateString()
          }`
          : 'Forecast name'
        }}
        <img
          src="@/assets/icons/arrow-down.svg"
          alt="Arrow"
          :class="{
            'reversed-arrow': forecastMenu
          }"
        >
        <div class="forecast-menu" v-if="forecastMenu">
          <button
            v-for="(forecast, index) in company.forecasts"
            :key="index"
            class="forecast-button"
            :class="{
              'forecast-button__active': forecast.id == company.forecast.value?.id
            }"
            @click="company.setForecast(forecast)"
          >{{ forecast.name }} - {{ new Date(forecast.updatedAt).toLocaleDateString() }}</button>
        </div>
      </Button>
      <Button type="transparent" size="small">Save</Button>
      <Button
        type="transparent"
        size="small"
        @click="exportExcel(company, tableData)"
      >Export</Button>
      <Button type="transparent" size="small">Embed</Button>
    </template>
    <Row name="CEO" :separate="true">
      <td
        v-for="(ceo, index) in ceoData"
        :key="index"
        :colspan="ceo.endYear && ceo.startYear ? ceo.endYear - ceo.startYear : 1"
        class="ceo-row"
        :class="{
          'ceo-row__last': index === ceoData.length - 1,
        }"
      >
        <div class="ceo-row-inner">
          <div class="ceo-backdrop"></div>
          <div class="ceo-photo"></div>
          <div class="ceo-name">
            {{ ceo.fullName }}
          </div>
        </div>
      </td>
      <td
        class="ceo-filler"
        :colspan="tableData.categories[tableData.categories.length - 1].values.length"
      >
        <div class="ceo-backdrop"></div>
      </td>
    </Row>
  </Table>
</template>

<script lang="ts">
import {
  defineComponent,
  PropType,
  computed,
  ref,
} from 'vue';
import { useStore } from 'vuex';

import { CompanyController } from '@/controllers/company/types';

import Button from '@/components/ui/ButtonComponent.vue';

import {
  TableComponent as Table,
  RowComponent as Row,
} from '@/components/ui/table';
import { TableData } from '@/components/ui/table/types';

import { SHOW_MODAL } from '@/store/actions/application';

import { exportExcel } from '@/services/excel';

import { Comment } from '@/rest-api/comments/assets';

import { tableRows } from './data/rows';
import { forecastControl } from './data/controls';

export default defineComponent({
  name: 'FinancialsTable',
  components: {
    Table,
    Row,
    Button,
  },
  props: {
    company: {
      type: Object as PropType<CompanyController>,
      required: true,
    },
    forecast: {
      type: String as PropType<forecastControl>,
      required: true,
    },
  },
  setup(props) {
    const store = useStore();

    const forecastMenu = ref(false);

    const ceoData = computed(() => props.company.ceo.map((ceo, index) => {
      if (!ceo.startYear) {
        return ceo;
      }
      const years = props.company.financials.actual.map((item) => Number(item.year));
      const startedFrom = Math.max(Math.min(...years), ceo.startYear);
      const relative = (index !== props.company.ceo.length - 1 ? 1 : 3);

      return {
        fullName: ceo.fullName,
        startYear: startedFrom,
        endYear: (ceo.endYear || Math.max(...years)) + relative,
      };
    }));

    const tableData = computed(() => {
      const {
        actual,
        average,
        estimated,
        projected,
      } = props.company.financials;

      const data: TableData = {
        categories: [
          {
            name: 'Actual',
            key: 'actual',
            values: actual,
          },
          {
            name: '10 year gagr',
            tableName: '10y GAGR',
            key: 'average',
            values: average,
            color: 'var(--theme-text-gray-3)',
          },
          {
            name: 'Estimated',
            key: 'estimated',
            values: estimated,
            editable: true,
          },
          {
            name: 'Projected',
            key: 'projected',
            values: projected,
            editable: true,
          },
        ],
        rows: tableRows,
        column: 'year',
        columnName: 'Fiscal',
        comments: props.company.comments,
        editEvent: props.company.forecast.value === undefined,
      };

      return data;
    });

    const onEditEvent = (column?: string, field?: string, value?: number) => {
      if (props.forecast !== forecastControl.CUSTOM) {
        store.commit(SHOW_MODAL, 'forecast');
      } else if (column && field && value !== undefined) {
        props.company.saveForecast(column, field, value);
      }
    };

    const createComment = (comment: Comment) => {
      props.company.addComment(comment);
    };

    const saveComment = (index: number) => {
      props.company.saveComment(index);
    };

    const deleteComment = (index: number) => {
      props.company.deleteComment(index);
    };

    // const toggleComment = () => {
    //   store.commit(COMMENT_CURSOR, !store.state.application.commentCursor);
    // };

    return {
      forecastMenu,
      ceoData,
      tableData,
      onEditEvent,
      exportExcel,
      createComment,
      saveComment,
      deleteComment,
    };
  },
});
</script>

<style scoped>
.financials-table .ceo-row {
  position: relative;
  z-index: 2;
}

.financials-table .ceo-row > .ceo-row-inner {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  width: 100%;
  font-weight: 500;
}

.financials-table .ceo-row > .ceo-row-inner > .ceo-backdrop {
  position: absolute;
  background: #AEB7FB;
  top: 50%;
  transform: translateY(-50%);
  width: calc(100% + 12px);
  height: 18px;
  z-index: 0;
}

.financials-table .ceo-row > .ceo-row-inner > .ceo-name {
  position: relative;
  z-index: 2;
}

.financials-table .ceo-row.ceo-row__last > .ceo-row-inner > .ceo-backdrop {
  background: #D6DBFD;
}

.financials-table .ceo-row > .ceo-row-inner > .ceo-photo {
  position: absolute;
  left: 0;
  transform: translateX(-50%);
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #B3B3B3;
  z-index: 1;
}

.financials-table .ceo-filler {
  position: relative;
  z-index: 1;
}

.financials-table .ceo-filler > .ceo-backdrop {
  position: absolute;
  background: #EDEDED;
  left: -12px;
  top: 50%;
  transform: translateY(-50%);
  width: calc(100% + 12px);
  height: 18px;
  z-index: 0;
  border-top-right-radius: 100px;
  border-bottom-right-radius: 100px;
}

.financials-table .forecast-menu {
  position: absolute;
  top: calc(100% + 15px);
  left: 50%;
  transform: translateX(-50%);
  width: 286px;
  background: var(--theme-text-color-contrast);
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0px 8px 18px 0px rgba(0, 0, 0, 0.06);
  z-index: 2;
}

.financials-table .forecast-menu > .forecast-button {
  width: 100%;
  outline: none;
  border: none;
  border-radius: 4px;
  padding: 8px;
  font-size: 12px;
  font-weight: 500;
  background: none;
  text-align: left;
  cursor: pointer;
}

.financials-table .forecast-menu > .forecast-button__active {
  background: #F4F6FF;
}

.financials-table .reversed-arrow {
  transform: rotateX(180deg);
}
</style>
