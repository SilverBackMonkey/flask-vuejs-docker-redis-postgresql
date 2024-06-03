<template>
  <button
    class="checkbox"
    :class="{
      'checkbox-checked': innerValue,
      'checkbox__big': type === 'big',
    }"
    @click="innerValue = !innerValue"
  ></button>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';

export default defineComponent({
  name: 'CheckboxComponent',
  props: {
    type: {
      type: String,
      enum: ['default', 'big'],
      default: 'default',
    },
    value: {
      type: Boolean,
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

    return {
      innerValue,
    };
  },
});
</script>

<style scoped>
.checkbox {
  position: relative;
  width: 12px;
  height: 12px;
  border: 2px solid #9AA6FA;
  border-radius: 1px;
  cursor: pointer;
  outline: none;
  background: none;
}

.checkbox.checkbox__big {
  width: 16px;
  height: 16px;
  border-color: var(--theme-text-gray);
  border-radius: 2px;
}

.checkbox.checkbox-checked {
  border: 2px solid var(--theme-link-color);
}

.checkbox.checkbox__big.checkbox.checkbox-checked {
  border-color: var(--theme-text-gray);
}

.checkbox.checkbox-checked:not(.checkbox__big)::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 70%;
  height: 70%;
  transform: translate(-50%, -50%);
  background-color: var(--theme-link-color);
  mask-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 8 8'%3e%3cpath fill='%23fff' d='M6.564.75l-3.59 3.612-1.538-1.55L0 4.26 2.974 7.25 8 2.193z'/%3e%3c/svg%3e");
}

.checkbox.checkbox__big.checkbox.checkbox-checked::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 70%;
  height: 70%;
  transform: translate(-50%, -50%);
  background: url('@/assets/icons/arrow-smooth.svg');
  background-size: 100% 100%;
  background-repeat: no-repeat;
}
</style>
