<template>
  <button
    class="dropdown-button"
    @click.self="toggleMenu"
  >
    <div class="dropdown-value">
      <slot>
        <p>{{ model.title }}</p>
      </slot>
    </div>
    <div class="dropdown-menu" v-if="dropdownMenu">
      <slot name="content">
        <button
          v-for="(item, index) in values"
          :key="index"
          class="dropdown-menu-button"
          :class="{'dropdown-menu-button__active': model.key === item.key}"
          @click="selectValue(item)"
        >{{ item.title }}</button>
      </slot>
    </div>
  </button>
</template>

<script lang="ts">
import {
  defineComponent,
  PropType,
  computed,
  ref,
} from 'vue';

import Value from './types';

export default defineComponent({
  name: 'DropdownComponent',
  props: {
    value: {
      type: Object as PropType<Value>,
      required: false,
      default: undefined,
    },
    values: {
      type: Array as PropType<Value[]>,
      required: false,
      default: undefined,
    },
  },
  emits: ['update:value'],
  setup(props, { emit }) {
    const dropdownMenu = ref(false);

    const model = computed({
      get() {
        return props.value;
      },
      set(value) {
        emit('update:value', value);
      },
    });

    const toggleMenu = () => {
      dropdownMenu.value = !dropdownMenu.value;
    };

    const selectValue = (item: Value) => {
      model.value = item;
      dropdownMenu.value = false;
    };

    return {
      dropdownMenu,
      model,
      toggleMenu,
      selectValue,
    };
  },
});
</script>

<style scoped>
.dropdown-button {
  position: relative;
  background: transparent;
  border: none;
  outline: none;
}

.dropdown-value,
.dropdown-value * {
  pointer-events: none;
}

.dropdown-menu {
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

.dropdown-menu > .dropdown-menu-button {
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

.dropdown-menu > .dropdown-menu-button__active {
  background: #F4F6FF;
}
</style>
