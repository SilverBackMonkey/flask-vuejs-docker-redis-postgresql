<template>
  <td>
    <div class="table-row">
      <slot :instance="instance || {}" :index="index || 0" />
    </div>
  </td>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'RowComponent',
  props: {
    dataKey: {
      type: String,
      required: false,
      default: null,
    },
    instance: {
      type: Object,
      required: false,
    },
    index: {
      type: Number,
      required: false,
    },
  },
});
</script>

<style scoped>
td {
  height: 34px;
  padding: 0 4px;
}

.table-row {
  display: flex;
  align-items: center;
  font-size: 14px;
  font-weight: 500;
  line-height: 150%;
  letter-spacing: 0.28px;
}
</style>
