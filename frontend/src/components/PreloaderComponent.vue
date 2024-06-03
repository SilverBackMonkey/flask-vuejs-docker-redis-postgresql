<template>
  <div class="preloader" v-if="isPreloaderShown">
    <VueSpinner size="60" color="var(--theme-link-color)" />
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';
import { useStore } from 'vuex';

import { VueSpinner } from 'vue3-spinners';

export default defineComponent({
  name: 'PreloaderComponent',
  components: {
    VueSpinner,
  },
  setup() {
    const store = useStore();

    const isPreloaderShown = computed(() => store.getters.isPreloaderShown);

    return {
      isPreloaderShown,
    };
  },
});
</script>

<style scoped>
.preloader {
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: var(--theme-background-color);
  z-index: 1000;
}
</style>
