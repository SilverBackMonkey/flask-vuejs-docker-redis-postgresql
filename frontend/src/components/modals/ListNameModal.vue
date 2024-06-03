<template>
  <Modal class="modal__list" name="rename-list">
    <h3>Rename list</h3>
    <Input placeholder="Enter a name for the new list" v-model:value="listName" />
    <Button
      :loading="loading"
      :disabled="!listName"
      @click="onClickSave"
    >Save</Button>
  </Modal>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

import Modal from '@/components/ModalComponent.vue';

import Input from '@/components/ui/InputComponent.vue';
import Button from '@/components/ui/ButtonComponent.vue';

import * as api from '@/rest-api/lists';

export default defineComponent({
  name: 'ListNameModal',
  components: {
    Modal,
    Input,
    Button,
  },
  props: {
    listId: {
      type: Number,
      required: true,
    },
  },
  setup(props) {
    const listName = ref('');
    const loading = ref(false);

    const onClickSave = () => {
      loading.value = true;

      api.edit(props.listId, listName.value).then((payload) => {
        window.location.reload();
      });
    };

    return {
      loading,
      listName,
      onClickSave,
    };
  },
});
</script>

<style>
.modal.modal__list .modal-inner {
  max-width: 484px;
  width: 100%;
  align-items: center;
}

.modal.modal__list input {
  width: 100%;
}
</style>
