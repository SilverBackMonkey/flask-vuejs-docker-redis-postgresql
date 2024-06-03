<template>
  <div class="login">
    <Card class="login-inner">
      <h2 style="text-align: center;">Sign up with email</h2>
      <Input placeholder="E-mail" v-model:value="email" />
      <Input placeholder="Password" type="password" v-model:value="password" />
      <Input placeholder="Repeat password" type="password" v-model:value="passwordRepeat" />
      <p>Do you already have an account? <a href="/login">Sign in</a></p>
      <Button
        :loading="loading"
        :disabled="!email && !password"
        @click="register"
      >Sign up</Button>
    </Card>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

import Card from '@/components/ui/CardComponent.vue';
import Input from '@/components/ui/InputComponent.vue';
import Button from '@/components/ui/ButtonComponent.vue';

import { LOADING } from '@/store/actions/application';
import { SIGNUP_REQUEST } from '@/store/actions/user';

export default defineComponent({
  name: 'RegisterView',
  components: {
    Card,
    Input,
    Button,
  },
  setup() {
    const store = useStore();
    const router = useRouter();

    const email = ref('');
    const password = ref('');
    const passwordRepeat = ref('');

    const loading = ref(false);

    onMounted(() => {
      store.commit(LOADING, false);
    });

    const register = () => {
      if (password.value !== passwordRepeat.value) {
        alert('The specified passwords do not match');
        return;
      }

      loading.value = true;

      const context = {
        email: email.value,
        password: password.value,
      };

      store.dispatch(SIGNUP_REQUEST, context).then(() => {
        router.push({ name: 'login' });
      }).finally(() => {
        loading.value = false;
      });
    };

    return {
      email,
      password,
      passwordRepeat,
      loading,
      register,
    };
  },
});
</script>

<style scoped>
.login {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login > .login-inner {
  display: flex;
  flex-direction: column;
  gap: 20px;
  min-width: 320px;
}

.login > .login-inner > * {
  width: 100%;
}
</style>
