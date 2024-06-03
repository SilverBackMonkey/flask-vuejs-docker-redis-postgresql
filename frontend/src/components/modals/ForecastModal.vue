<template>
  <Modal class="modal__forecast" name="forecast" v-on:shown="reset">
    <h3>Forecast editing</h3>
    <p>
      Your forecast has been successfully edited.
      Give it a name to save it in your forecast list.
    </p>
    <Input placeholder="Enter the forecast name..." v-model:value="forecastName" />
    <Button
      :loading="loading"
      :disabled="!forecastName"
      @click="onClickSave"
    >Save</Button>
  </Modal>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

import Modal from '@/components/ModalComponent.vue';

import Input from '@/components/ui/InputComponent.vue';
import Button from '@/components/ui/ButtonComponent.vue';

export default defineComponent({
  name: 'ForecastModal',
  components: {
    Modal,
    Input,
    Button,
  },
  emits: ['save'],
  setup(_, { emit }) {
    const forecastName = ref('');
    const loading = ref(false);

    const onClickSave = () => {
      loading.value = true;
      emit('save', forecastName.value);
    };

    const reset = () => {
      forecastName.value = '';
      loading.value = false;
    };

    return {
      loading,
      forecastName,
      onClickSave,
      reset,
    };
  },
});
</script>

<style>
.modal.modal__forecast .modal-inner {
  max-width: 464px;
  align-items: center;
}

.modal.modal__forecast input {
  width: 100%;
}

.modal.modal__forecast p {
  font-size: 16px;
}
</style>
