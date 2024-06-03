<template>
  <th :colspan="colspan">
    <div class="table-category">
      <slot />
    </div>
  </th>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'CategoryComponent',
  props: {
    colspan: {
      type: Number,
      default: 1,
    },
  },
});
</script>

<style scoped>
th {
  background: var(--theme-link-color);
  border-left: 1px solid var(--theme-text-color-contrast);
  height: 44px;
}

.table-category {
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--theme-text-color-contrast);
  font-size: 10px;
  font-weight: 800;
  line-height: 110%;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}
</style>
