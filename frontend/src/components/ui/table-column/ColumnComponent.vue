<template>
  <th>
    <div class="table-column">
      <slot />
    </div>
  </th>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'ColumnComponent',
  props: {
    dataKey: {
      type: String,
      required: false,
      default: null,
    },
  },
});
</script>

<style scoped>
th {
  min-width: 76px;
  height: 44px;
  padding: 0 4px;
}

.table-column {
  color: var(--theme-dark-color-1);
  font-size: 12px;
  font-weight: 600;
}
</style>
