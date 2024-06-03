<template>
  <div class="helper" :class="{'helper__bottom': align === 'bottom'}">
    <img src="@/assets/icons/help.svg" alt="Help">
    <div class="helper-hover">
      <slot />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'HelpComponent',
  props: {
    align: {
      type: String,
      enum: ['top', 'bottom'],
      default: 'top',
    },
  },
});
</script>

<style>
.helper {
  position: relative;
  width: 12px;
  height: 12px;
  cursor: pointer;
  z-index: 2;
}

.helper > img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.helper > .helper-hover {
  display: none;
  position: absolute;
  background: #D6DBFD;
  font-size: 12px;
  line-height: 14px;
  font-weight: 600;
  color: var(--theme-link-color);
  text-align: center;
  padding: 12px 16px;
  left: 50%;
  top: -10px;
  transform: translate(-50%, -100%);
}

.helper.helper__bottom > .helper-hover {
  top: auto;
  bottom: 0;
  transform: translate(-50%, calc(100% + 10px));
}

.helper:hover > .helper-hover {
  display: block;
  width: 217px;
  border-radius: 10px;
  text-transform: none;
}

.helper:hover > .helper-hover::after {
  content: '';
  position: absolute;
  left: 50%;
  bottom: -19px;
  transform: translateX(-50%);
  border: 10px solid transparent;
  border-top: 10px solid #D6DBFD;
}

.helper.helper__bottom > .helper-hover::after {
  bottom: auto;
  top: -19px;
  transform: translateX(-50%) rotateX(180deg);
}
</style>
