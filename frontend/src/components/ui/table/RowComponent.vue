<template>
  <tr class="table-spacer" v-if="separate"></tr>
  <tr>
    <td class="table-row">
      <span v-if="showCounter && index">{{ (index + 1).toString().padStart(2, '0') }}</span>
      {{ name }}
    </td>
    <slot />
    <td class="table-comment" v-if="comments"></td>
  </tr>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'RowComponent',
  props: {
    name: {
      type: String,
      required: true,
    },
    showCounter: {
      type: Boolean,
      default: true,
    },
    index: {
      type: Number,
      required: false,
    },
    comments: {
      type: Boolean,
      default: false,
    },
    separate: {
      type: Boolean,
      default: false,
    },
  },
});
</script>
