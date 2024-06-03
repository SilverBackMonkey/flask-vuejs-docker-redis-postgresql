<template>
  <Table
    :data="computedTableData"
    :compiler="compile"
    :updating="updating"
    class="list-table"
  >
    <Category :colspan="1" class="company-name">
      <Button type="transparent">Base</Button>
      <Button type="transparent" :visually-disabled="true">Lens</Button>
      <Button type="transparent" :visually-disabled="true">Holdings</Button>
    </Category>
    <Category :colspan="4">
      Valuation
    </Category>
    <Category :colspan="3" class="list-buttons">
      Historical Performance:
      <Button
        type="transparent"
        @click="innerPeriod = '10Y'"
        :visually-disabled="innerPeriod !== '10Y'"
      >10Y</Button>
      <Button
        type="transparent"
        @click="innerPeriod = '5Y'"
        :visually-disabled="innerPeriod !== '5Y'"
      >5Y</Button>
      <Button
        type="transparent"
        @click="innerPeriod = '1Y'"
        :visually-disabled="innerPeriod !== '1Y'"
      >1Y</Button>
    </Category>
    <Category :colspan="3" class="list-buttons list-buttons__gap">
      Forecast:
      <Button type="transparent">Averages</Button>
      <Button type="transparent" :visually-disabled="true">Analysts</Button>
      <Button type="transparent" :visually-disabled="true">Custom</Button>
    </Category>
    <Category :colspan="3">
      Fundamentals
    </Category>
    <Category :colspan="1">
      Comments
    </Category>

    <Column class="sort-column" data-key="name">
      Sort by:
      <Button type="transparent" class="sort-button" @click="sortMenu = !sortMenu">
        {{ sort.title }}
        <img
          src="@/assets/icons/arrow-down.svg"
          alt="Arrow"
          :class="{
            'reversed-arrow': sortMenu
          }"
        >
        <div class="sort-menu" v-if="sortMenu">
          <button
            v-for="(item, index) in sortItems"
            :key="index"
            class="sort-button"
            :class="{'sort-button__active': sort.key === item.key}"
            @click="sort = item"
          >{{ item.title }}</button>
        </div>
      </Button>
    </Column>

    <Row
      class="list-name"
      data-key="name"
      v-slot="{ instance, index }"
    >
      <div class="list-counter">
        {{ (index + 1).toString().padStart(2, '0') }}
      </div>
      <p>
        {{ instance.company.name }}
      </p>
      <div class="list-symbol">
        {{ instance.company.symbol }}
      </div>
    </Row>

    <Row
      class="list-price"
      data-key="company.stockPrice"
      v-slot="{ instance }"
    >
      <p>
        {{ instance.company.stockPrice }}
        <span
          class="list-price__green"
          v-if="instance.company.stockPriceChange >= 0"
        >(+{{ Math.round(instance.company.stockPriceChange * 100) / 100 }})</span>
        <span class="list-price__red" v-else>
          ({{ Math.round(instance.company.stockPriceChange * 100) / 100 }})
        </span>
      </p>
    </Row>

    <Row
      data-key="change"
      v-slot="{ instance }"
    >
      <div class="list-change">
        <div class="list-change-circle" :style="{
          left: `${priceChange(instance.company)}%`
        }" />
      </div>
    </Row>

    <Row
      data-key="totalReturn"
    >-</Row>

    <Row
      data-key="priceChange"
    >-</Row>

    <Row
      data-key="leverage"
    >-</Row>

    <Row
      data-key="comment"
    ></Row>

    <Line class="list-total">
      <Row>
        Total
      </Row>

      <Row>
        -
      </Row>

      <Row>
        <div class="list-change">
          <div class="list-change-circle" :style="{
            left: `${averageChange}%`
          }" />
        </div>
      </Row>

      <Row
        v-for="(column, index) in allowedColumns"
        :key="index"
      >
        {{ column.handler ? column.handler(average(column)) : average(column) }}
      </Row>
    </Line>
  </Table>
</template>

<script lang="ts">
import {
  defineComponent,
  ref,
  computed,
  PropType,
  onUpdated,
} from 'vue';

import {
  TableComponent as Table,
  CategoryComponent as Category,
  ColumnComponent as Column,
  RowComponent as Row,
  LineComponent as Line,
} from '@/components/ui/table-column';

import Button from '@/components/ui/ButtonComponent.vue';

import { TableData } from '@/components/ui/table/types';

import { tableData } from '@/data/list';

import { List } from '@/rest-api/lists/assets';
import { Company } from '@/rest-api/companies/assets';

import { useCompiler } from '@/controllers/compiler';

import * as render from '@/services/renderers';
import { nestedKey } from '@/services/nested-key';

export default defineComponent({
  name: 'TableView',
  components: {
    Table,
    Category,
    Column,
    Button,
    Row,
    Line,
  },
  props: {
    list: {
      type: Object as PropType<List>,
      required: false,
    },
    period: {
      type: String,
      required: true,
    },
    updating: {
      type: Boolean,
      required: true,
    },
  },
  emits: ['update:period'],
  setup(props, { emit }) {
    const sortMenu = ref(false);
    const sortItems = [
      {
        key: 'marketCap',
        title: 'Market Cap',
      },
      {
        key: 'name',
        title: 'A-Z',
      },
    ];
    const sort = ref(sortItems[0]);

    const computedTableData = computed(() => {
      if (!props.list) {
        return {};
      }

      const newData = { ...tableData };
      newData.data = props.list.companies;

      if (sort.value.key === 'marketCap') {
        newData.data.sort(
          (a, b) => (b.valuationAndEarnings.marketCap - a.valuationAndEarnings.marketCap),
        );
      } else if (sort.value.key === 'name') {
        newData.data.sort((a, b) => {
          if (a.company.name < b.company.name) {
            return -1;
          }

          return 1;
        });
      }

      return newData;
    });

    const compilerData = computed(() => {
      const data: TableData = {
        categories: [
          {
            name: 'Actual',
            key: 'actual',
            values: props.list ? props.list.companies : [],
          },
        ],
        rows: (computedTableData.value as any).rows || [],
        column: 'name',
        columnName: 'Fiscal',
      };

      return data;
    });

    const { compile, clearCache } = useCompiler(compilerData, true);

    const priceChange = (instance: Company): number => {
      const range = (instance.week52High - instance.week52Low);
      const offset = (instance.stockPrice - instance.week52Low);

      const result = (offset / range) * 100;

      if (result > 100) {
        return 100;
      }

      if (result < 0) {
        return 0;
      }

      return result;
    };

    const averageChange = computed(() => {
      if (!props.list || props.list.companies.length === 0) {
        return 0;
      }

      const lowPrice = props.list.companies.reduce(
        (previous, next) => (previous.company.week52Low < next.company.week52Low ? previous : next),
      ).company.week52Low;

      const maxPrice = props.list.companies.reduce(
        (previous, next) => (previous.company.week52Low > next.company.week52Low ? previous : next),
      ).company.week52High;

      const totalPrice = props.list.companies.reduce(
        (partialSum, instance) => (partialSum + instance.company.stockPrice), // eslint-disable-line
        0,
      );

      const averagePrice = totalPrice / props.list.companies.length;

      const range = (maxPrice - lowPrice);
      const offset = (averagePrice - lowPrice);

      const result = (offset / range) * 100;

      if (result > 100) {
        return 100;
      }

      if (result < 0) {
        return 0;
      }

      return result;
    });

    const average = (column: any): number | undefined => {
      const values = props.list?.companies.map((item) => nestedKey(column.key, item)) || [];

      if (values.length === 0 || (typeof values[0] === 'object' && Object.keys(values[0]).length === 0)) {
        return undefined;
      }

      const sum = values.reduce(
        (partialSum, value, index) => partialSum + compile(value, props.list?.companies[index]),  // eslint-disable-line
        0,
      );

      return sum / values.length;
    };

    const allowedColumns = computed(() => {
      if (Object.keys(computedTableData.value).length === 0) {
        return [];
      }

      const columns = (computedTableData.value as any).columns.filter(
        (column: any) => (['name', 'company.stockPrice', 'change'].indexOf(column.key) === -1),
      );

      return columns;
    });

    const innerPeriod = computed({
      get() {
        return props.period;
      },
      set(newValue) {
        emit('update:period', newValue);
      },
    });

    onUpdated(() => {
      clearCache();
    });

    return {
      computedTableData,
      sortMenu,
      sort,
      sortItems,
      render,
      innerPeriod,
      allowedColumns,
      priceChange,
      averageChange,
      compile,
      average,
    };
  },
});
</script>

<style scoped>
.company-name {
  width: 228px;
}

.company-name .button {
  color: var(--theme-text-color-contrast) !important;
  border: 1px solid var(--theme-text-color-contrast);
  padding: 4px 12px;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
}

.company-name .button.button__disabled {
  border: none;
  padding: 4px 13px;
}

.sort-button {
  position: relative;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  font-size: 12px;
  font-weight: 600;
  text-transform: none;
  gap: 4.3px;
}

.sort-button > img {
  margin-top: 1px;
}

.sort-menu {
  position: absolute;
  top: calc(100% + 15px);
  left: 50%;
  transform: translateX(-20%);
  width: 286px;
  background: var(--theme-text-color-contrast);
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0px 8px 18px 0px rgba(0, 0, 0, 0.06);
  z-index: 2;
}

.sort-menu > .sort-button {
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
  text-align: left;
  justify-content: flex-start;
}

.sort-menu > .sort-button__active {
  background: #F4F6FF;
}

.list-buttons .button {
  font-size: 10px;
  font-weight: 800;
  line-height: 110%;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  color: var(--theme-text-color-contrast);
}

.list-buttons .button.button__disabled {
  color: #AEB7FB;
}

.list-counter {
  font-size: 10px;
  font-weight: 400;
  line-height: 110%;
  letter-spacing: 0.2px;
  color: var(--theme-text-gray-3);
}

.list-symbol {
  background: var(--theme-text-gray-2);
  padding: 2px 4px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: 500;
  line-height: 110%;
  letter-spacing: 0.2px;
  text-transform: uppercase;
  color: var(--theme-text-gray-3);
}

.list-price {
  font-size: 14px;
  font-weight: 500;
  line-height: 150%;
  letter-spacing: 0.28px;
}

.list-price .list-price__green {
  color: #21B232;
}

.list-price .list-price__red {
  color: #FC382C;
}

.list-change {
  position: relative;
  height: 2px;
  width: 40px;
  background: var(--theme-text-gray-2);
}

.list-change-circle {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: var(--theme-text-gray-3);
}

.list-total {
  background: #F4F6FF;
  font-weight: 600;
}
</style>

<style>
.list-table tr > th:first-child,
.list-table tr > td:first-child {
  padding-left: 24px;
}

.company-name > .table-category {
  justify-content: flex-start;
}

.sort-column > .table-column {
  display: flex;
  align-items: center;
  gap: 2px;
}

.list-buttons > .table-category {
  gap: 8px;
}

.list-buttons.list-buttons__gap > .table-category {
  gap: 10px;
}

.list-name > .table-row {
  display: flex;
  align-items: center;
  gap: 4px;
}

.list-name > .table-row > p {
  font-size: 14px;
  font-weight: 600;
  line-height: 150%;
  letter-spacing: 0.28px;
  color: var(--theme-text-color-2);
  white-space: nowrap;
}

.list-total .table-row {
  font-weight: 600;
}
</style>
