<template>
  <textarea
    v-model="innerValue"
    ref="textarea"
    @input="calculateHeight"
    :style="{
      height: textareaHeight,
    }"
  />
</template>

<script lang="ts">
import {
  defineComponent,
  nextTick,
  computed,
  ref,
  onMounted,
} from 'vue';

export default defineComponent({
  name: 'TextareaComponent',
  props: {
    value: {
      type: String,
      required: true,
    },
  },
  emits: ['update:value'],
  setup(props, { emit }) {
    const textarea = ref();
    const textareaHeight = ref('auto');

    const calculateHeight = () => {
      textareaHeight.value = 'auto';

      nextTick(() => {
        if (textarea.value !== undefined) {
          textareaHeight.value = `${textarea.value.scrollHeight}px`;
        }
      });
    };

    const innerValue = computed({
      get() {
        return props.value;
      },
      set(newValue) {
        emit('update:value', newValue);
      },
    });

    onMounted(() => {
      calculateHeight();
    });

    return {
      textarea,
      textareaHeight,
      calculateHeight,
      innerValue,
    };
  },
});
</script>
