<template>
  <Modal class="modal__list" name="new-list" v-on:shown="reset">
    <h3>New List</h3>
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
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

import Modal from '@/components/ModalComponent.vue';

import Input from '@/components/ui/InputComponent.vue';
import Button from '@/components/ui/ButtonComponent.vue';

import * as api from '@/rest-api/lists';

import { HIDE_MODAL } from '@/store/actions/application';

export default defineComponent({
  name: 'ForecastModal',
  components: {
    Modal,
    Input,
    Button,
  },
  setup() {
    const store = useStore();
    const router = useRouter();

    const listName = ref('');
    const loading = ref(false);

    const onClickSave = () => {
      loading.value = true;

      api.create(listName.value).then(async (payload) => {
        loading.value = false;
        store.commit(HIDE_MODAL);

        await router.push({ name: 'list', params: { id: payload.id } });

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
