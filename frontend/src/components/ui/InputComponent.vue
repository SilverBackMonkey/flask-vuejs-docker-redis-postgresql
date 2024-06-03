<template>
  <input type="text" v-model="innerValue" />
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';

export default defineComponent({
  name: 'InputComponent',
  props: {
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

    return {
      innerValue,
    };
  },
});
</script>

<style scoped>
input {
  background: #F4F6FF;
  padding: 16px;
  border-radius: 8px;
  border: none;
  outline: none;
  font-size: 16px;
  font-weight: 400;
  color: #7283FA;
}
</style>
