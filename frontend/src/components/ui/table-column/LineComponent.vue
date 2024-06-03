<template>
  <tr>
    <slot />
  </tr>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'LineComponent',
});
</script>
