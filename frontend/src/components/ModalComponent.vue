<template>
  <div class="modal" ref="modal" v-if="openedModal === name">
    <div class="modal-inner">
      <button class="modal-exit" @click="hideModal">
        <img src="@/assets/icons/cross.svg" alt="Cross">
      </button>
      <slot />
    </div>
  </div>
</template>

<script lang="ts">
import {
  defineComponent,
  computed,
  watch,
  ref,
  nextTick,
} from 'vue';
import { useStore } from 'vuex';

import { HIDE_MODAL } from '@/store/actions/application';

export default defineComponent({
  name: 'ModalComponent',
  props: {
    name: {
      name: String,
      required: true,
    },
  },
  emits: ['shown'],
  setup(props, { emit }) {
    const store = useStore();

    const modal = ref();
    const openedModal = computed(() => store.state.application.modal);

    const updatePosition = () => {
      if (!modal.value) {
        return;
      }

      const scale = Math.abs(window.innerWidth / 1512);

      modal.value.style.height = `${window.innerHeight / scale}px`;
      modal.value.style.top = '0px';

      nextTick(() => {
        modal.value.style.top = `${window.scrollY / scale}px`;
      });
    };

    watch(openedModal, () => {
      if (openedModal.value === props.name) {
        emit('shown');

        window.addEventListener('scroll', updatePosition);

        nextTick(() => {
          updatePosition();
        });
      }
    });

    const hideModal = () => {
      window.removeEventListener('scroll', updatePosition);
      store.commit(HIDE_MODAL);
    };

    return {
      modal,
      openedModal,
      hideModal,
    };
  },
});
</script>

<style>
.modal {
  position: absolute;
  left: 0;
  width: 100%;
  background: rgba(0, 0, 0, .7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal > .modal-inner {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: var(--theme-text-color-contrast);
  padding: 44px 40px 40px 40px;
  border-radius: 16px;
  text-align: center;
}

.modal > .modal-inner > .modal-exit {
  position: absolute;
  width: 14px;
  height: 14px;
  right: 22px;
  top: 22px;
  cursor: pointer;
  border: none;
  outline: none;
  background: none;
}

.modal > .modal-inner > .modal-exit > img {
  width: 100%;
  height: 100%;
}
</style>
