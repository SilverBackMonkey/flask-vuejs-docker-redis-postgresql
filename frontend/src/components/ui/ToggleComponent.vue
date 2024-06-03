<template>
  <div class="toggle">
    <template
      v-for="(currentValue, index) in values"
      :key="index"
    >
      <p
        :class="{
          enabled: currentValue === innerValue,
        }"
      >{{ currentValue }}</p>
      <span v-if="Number(index) < values.length - 1">|</span>
    </template>
    <button
      class="toggle-button"
      :class="{
        'toggle-button__enabled': innerValue === values[1],
      }"
      @click="toggleValue"
    >
      <div class="toggle-circle"></div>
    </button>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';

export default defineComponent({
  name: 'ToggleComponent',
  props: {
    values: {
      type: Object,
      required: true,
    },
    value: {
      type: String,
      required: true,
    },
  },
  emits: ['update:value'],
  setup(props, { emit }) {
    const innerValue = computed({
      get() {
        return props.value;
      },
      set(newValue) {
        emit('update:value', newValue);
      },
    });

    const toggleValue = () => {
      innerValue.value = innerValue.value === props.values[0] ? props.values[1] : props.values[0];
    };

    return {
      innerValue,
      toggleValue,
    };
  },
});
</script>

<style>
.toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--theme-text-color-contrast);
}

.toggle > p:not(.enabled) {
  color: var(--theme-text-gray-3);
}

.toggle > .toggle-button {
  position: relative;
  width: 40px;
  height: 24px;
  padding: 2px;
  background: var(--theme-text-gray-3);
  outline: none;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: .15s ease;
}

.toggle > .toggle-button.toggle-button__enabled {
  background: #21B232;
}

.toggle > .toggle-button > .toggle-circle {
  position: absolute;
  top: 2px;
  left: 2px;
  height: 20px;
  width: 20px;
  background: #FFFFFF;
  border-radius: 50%;
  transition: .15s ease;
}

.toggle > .toggle-button.toggle-button__enabled > .toggle-circle {
  left: calc(100% - 22px);
}
</style>
