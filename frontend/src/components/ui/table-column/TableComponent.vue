<template>
  <div class="table-vertical">
    <div class="table-updating" v-if="updating">
      <VueSpinner size="30" color="var(--theme-link-color)" />
    </div>
    <table>
      <thead>
        <tr class="table-categories">
          <component
            v-for="(category, index) in categories"
            :key="index"
            :is="category"
          />
        </tr>
        <tr class="table-columns">
          <template
            v-for="(column, index) in data.columns"
            :key="index"
          >
            <component
              :is="columnOverride(column.key?.toString() || '')"
              v-if="column.key && columnOverride(column.key)"
            />
            <ColumnComponent
              v-else
            >
              {{ column.name }}
            </ColumnComponent>
          </template>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(row, index) in data.data"
          :key="index"
        >
          <template
            v-for="(column, idx) in data.columns"
            :key="idx"
          >
            <component
              :is="rowOverride(column.key?.toString() || '')"
              :index="index"
              :instance="row"
              v-if="column.key && rowOverride(column.key)"
            />
            <RowComponent v-else>
              {{ handleValue(column, row) }}
            </RowComponent>
          </template>
        </tr>

        <component
          v-for="(line, index) in lines"
          :key="index"
          :is="line"
        />
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import {
  defineComponent,
  useSlots,
  PropType,
  Component,
} from 'vue';

import { VueSpinner } from 'vue3-spinners';

import { nestedKey } from '@/services/nested-key';

import { TableData } from './types';

import ColumnComponent from './ColumnComponent.vue';
import RowComponent from './RowComponent.vue';
import { TableColumn } from './types/column';

export default defineComponent({
  name: 'TableComponent',
  components: {
    VueSpinner,
    ColumnComponent,
    RowComponent,
  },
  props: {
    data: {
      type: Object as PropType<TableData>,
      required: true,
    },
    compiler: {
      type: Function,
      required: true,
    },
    updating: {
      type: Boolean,
      required: true,
    },
  },
  setup(props) {
    const slots = useSlots();

    const defaultSlot = slots.default && slots.default();
    const categories = defaultSlot?.filter((item) => (item.type as any).name === 'CategoryComponent') || [];
    const columns = defaultSlot?.filter((item) => (item.type as any).name === 'ColumnComponent') || [];
    const rows = defaultSlot?.filter((item) => (item.type as any).name === 'RowComponent') || [];
    const lines = defaultSlot?.filter((item) => (item.type as any).name === 'LineComponent') || [];

    const columnOverride = (key: string): Component | undefined => columns.find((x) => x.props && x.props['data-key'] === key);
    const rowOverride = (key: string): Component | undefined => rows.find((x) => x.props && x.props['data-key'] === key);

    const handleValue = (column: TableColumn, row: object): any => {
      const value = nestedKey(column.key, row);
      const compiled = props.compiler(value, row);

      return column.handler ? column.handler(compiled) : compiled;
    };

    return {
      categories,
      columns,
      lines,
      columnOverride,
      rowOverride,
      handleValue,
    };
  },
});
</script>

<style scoped>
.table-vertical {
  position: relative;
  display: flex;
  border-top-left-radius: 16px;
  border-top-right-radius: 16px;
  font-size: var(--font-size-12);
  font-weight: 500;
  text-align: left;
  height: 100%;
  width: 100%;
  border-radius: 16px;
  overflow: hidden;
}

.table-vertical table {
  border: none;
  border-collapse: collapse;
  width: 100%;
}

.table-vertical table > tbody > tr:nth-child(2n - 1) {
  background: var(--theme-light-color-1);
}

.table-vertical table > tbody > tr:nth-child(2n) {
  background: var(--theme-text-color-contrast);
}

.table-columns {
  background: #D6DBFD;
}

.table-updating {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  top: 88px;
  left: 0;
  height: calc(100% - 88px);
  width: 100%;
  background: rgba(255, 255, 255, .75);
  z-index: 2;
}
</style>

<style>
.table-vertical table thead > tr > th:first-child {
  border: none;
}
</style>
