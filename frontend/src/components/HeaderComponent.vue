<template>
  <header>
    <div class="header-logotype">
      <img src="@/assets/logo.svg" alt="TopFunds">
    </div>
    <nav>
      <router-link to="/">Section 1</router-link> |
      <router-link to="/">Section 2</router-link> |
      <router-link to="/">Section 3</router-link> |
      <router-link to="/">Section 4</router-link>
    </nav>
    <div class="header-toggle">
      <Toggle :values="toggleValues" v-model:value="toggleValue" />
    </div>
  </header>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

import Toggle from './ui/ToggleComponent.vue';

export default defineComponent({
  name: 'HeaderComponent',
  components: {
    Toggle,
  },
  setup() {
    const toggleValues = ref(['Light', 'Pro']);
    const toggleValue = ref(toggleValues.value[0]);

    return {
      toggleValues,
      toggleValue,
    };
  },
});
</script>

<style>
header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--theme-text-color);
  padding: var(--theme-vertical-padding) var(--theme-horizontal-padding);
}

header > nav {
  display: flex;
  gap: 30px;
}

header > nav,
header > nav > a {
  color: var(--theme-text-color-contrast) !important;
  font-size: 14px;
}

header > .header-logotype > img {
  height: 16px;
  width: auto;
}

header > .header-logotype,
header > .header-toggle {
  flex: .2;
}

header > .header-toggle {
  display: flex;
  justify-content: flex-end;
}
</style>
