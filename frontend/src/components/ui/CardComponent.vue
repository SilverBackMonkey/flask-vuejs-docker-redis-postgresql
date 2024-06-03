<template>
  <div class="card">
    <div class="card-loading" v-if="loading">
      <VueSpinner color="var(--theme-link-color)" size="30" />
    </div>
    <slot />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import { VueSpinner } from 'vue3-spinners';

export default defineComponent({
  name: 'CardComponent',
  components: {
    VueSpinner,
  },
  props: {
    loading: {
      type: Boolean,
      default: false,
    },
  },
});
</script>

<style>
.card {
  position: relative;
  background: var(--theme-text-color-contrast);
  box-shadow: 0px 8px 18px 0px rgba(0, 0, 0, .06);
  padding: 16px 24px;
  border-radius: 16px;
}

.card > .card-loading {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  top: 5px;
  left: 5px;
  width: calc(100% - 10px);
  height: calc(100% - 10px);
  background: var(--theme-text-color-contrast);
  z-index: 2;
}
</style>
