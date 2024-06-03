<template>
  <Preloader />
  <div class="wrapper">
    <Header />
    <router-view />
    <Footer />
    <NewListModal />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import Preloader from './components/PreloaderComponent.vue';
import Header from './components/HeaderComponent.vue';
import Footer from './components/FooterComponent.vue';

import NewListModal from './components/modals/NewListModal.vue';

export default defineComponent({
  name: 'App',
  components: {
    Preloader,
    Header,
    Footer,
    NewListModal,
  },
  setup() {
    const wrapper: HTMLElement | null = document.querySelector('#app');

    if (!wrapper) {
      return;
    }

    const resize = () => {
      wrapper.style.transform = `scale(${window.innerWidth / 1512})`;
      document.body.style.height = `${wrapper.getBoundingClientRect().height}px`;
    };

    resize();

    window.addEventListener('resize', resize);
  },
});
</script>

<style>
:root {
  --theme-text-color: #1A1A1A;
  --theme-text-color-2: #131313;
  --theme-dark-color-1: #333333;
  --theme-light-color-1: #F6F6F6;
  --theme-link-color: #3348FB;
  --theme-table-color: #D6DBFD;
  --theme-disabled-color: #C2CAFC;
  --theme-text-color-contrast: #FFFFFF;
  --theme-text-gray: #999999;
  --theme-text-gray-2: #E6E6E6;
  --theme-text-gray-3: #808080;
  --theme-background-color: #EDEDED;
  --theme-horizontal-padding: 40px;
  --theme-vertical-padding: 20px;
}

* {
  box-sizing: border-box;
  padding: 0;
  margin: 0;
}

html, body {
  background: var(--theme-background-color);
  min-height: 100%;
  width: 100vw;
}

body {
  overflow-x: hidden;
}

html {
  height: fit-content;
}

#app, .wrapper {
  width: 1512px;
  transform-origin: 0 0;
  min-height: 100%;
}

.wrapper,
button, input, textarea {
  font-family: 'Gilroy', sans-serif;
}

h1, h2, h3, h4, h5, h6 {
  font-weight: 800;
  text-transform: uppercase;
}

h1 {
  font-size: 32px;
}

h2 {
  font-size: 24px;
}

h3 {
  font-size: 16px;
}

h4 {
  font-size: 14px;
}

h5 {
  font-size: 12px;
}

h6 {
  font-size: 10px;
}

a {
  color: var(--theme-link-color);
  text-decoration: underline;
  font-weight: 600;
  font-size: 16px;
}

@font-face {
  font-family: 'Gilroy';
  font-weight: 400;
  src: url('@/assets/fonts/gilroy/Gilroy-Regular.ttf') format('truetype');
}

@font-face {
  font-family: 'Gilroy';
  font-weight: 500;
  src: url('@/assets/fonts/gilroy/Gilroy-Medium.ttf') format('truetype');
}

@font-face {
  font-family: 'Gilroy';
  font-weight: 600;
  src: url('@/assets/fonts/gilroy/Gilroy-Semibold.ttf') format('truetype');
}

@font-face {
  font-family: 'Gilroy';
  font-weight: 800;
  src: url('@/assets/fonts/gilroy/Gilroy-Extrabold.ttf') format('truetype');
}
</style>
