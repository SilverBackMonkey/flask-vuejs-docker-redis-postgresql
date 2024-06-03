<template>
  <Card class="list-header" v-if="list">
    <div class="list-header-side">
      <Dropdown
        class="list-title"
        :values="listsDropdownValues"
        v-model:value="listsDropdownValue"
      >
        <h2>{{ list.name }}</h2>
        <img
          :class="{
            'reversed-arrow': false,
          }"
          src="@/assets/icons/arrow-down-smooth.svg"
          alt="Arrow"
        >
      </Dropdown>
      <Dropdown
        class="list-header-button"
        :values="settingsDropdown"
        v-model:value="settingsDropdownValue"
      >
        <img src="@/assets/icons/edit.svg" alt="Edit">
      </Dropdown>
      <Dropdown
        class="list-header-button"
      >
        <img src="@/assets/icons/plus.svg" alt="Plus">

        <template #content>
          <div class="list-company-search">
            <Input type="string" placeholder="Search" v-model:value="companySearch" />
          </div>
          <div class="list-company-values">
            <div
              v-for="(company, index) in filteredCompanies"
              :key="index"
              class="list-company-value"
            >
              <Checkbox
                v-model:value="company.isSubscribed"
                v-on:update:value="toggleSubscrption(company)"
              />
              {{ company.name }}
            </div>
          </div>
        </template>
      </Dropdown>
      <button class="list-header-button">
        <img src="@/assets/icons/alert.svg" alt="Alert">
      </button>
      <button class="list-header-button">
        <img src="@/assets/icons/share.svg" alt="Share">
      </button>
    </div>
    <div class="list-header-side">
      <div class="list-filter">
        <span>View:</span>
        <Button type="transparent">Extended</Button>
        <Button type="transparent" :visually-disabled="true">Condensed</Button>
      </div>
      <div class="list-filter">
        <span class="list-checkbox">Show highlights</span> <Checkbox :value="true" />
      </div>
    </div>
    <div class="list-header-side">
      <div class="list-search">
        <Input type="string" placeholder="Search" />
      </div>
      <img src="@/assets/icons/settings.svg" alt="Settings">
    </div>
  </Card>
  <ListNameModal
    :list-id="list?.id || 0"
  />
</template>

<script lang="ts">
import {
  defineComponent,
  PropType,
  ref,
  reactive,
  watch,
  computed,
  onMounted,
} from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

import Levenshtein from 'levenshtein';

import Card from '@/components/ui/CardComponent.vue';
import Button from '@/components/ui/ButtonComponent.vue';
import Checkbox from '@/components/ui/CheckboxComponent.vue';
import Input from '@/components/ui/InputComponent.vue';
import { DropdownComponent as Dropdown, DropdownValue } from '@/components/ui/dropdown';

import ListNameModal from '@/components/modals/ListNameModal.vue';

import * as api from '@/rest-api/lists';
import { List } from '@/rest-api/lists/assets';

import * as companyApi from '@/rest-api/companies';

import { SHOW_MODAL } from '@/store/actions/application';

import CompanyListSimple from './types';
import { settingsDropdown } from './dropdown';

export default defineComponent({
  name: 'HeaderView',
  components: {
    Card,
    Button,
    Checkbox,
    Input,
    Dropdown,
    ListNameModal,
  },
  props: {
    list: {
      type: Object as PropType<List>,
      required: false,
    },
  },
  emits: ['update'],
  setup(props, { emit }) {
    const store = useStore();
    const router = useRouter();

    const companies: CompanyListSimple[] = reactive([]);
    const companySearch = ref('');

    const settingsDropdownValue = ref<DropdownValue>({
      key: '',
      title: '',
    });

    const listsDropdown: DropdownValue[] = reactive([]);
    const listsDropdownValue = ref<DropdownValue>({
      key: '',
      title: '',
    });

    const listsDropdownValues = computed(() => [
      ...listsDropdown,
      {
        key: 'create',
        title: 'Create new list',
      },
    ]);

    watch(listsDropdownValue, async (value) => {
      if (!props.list) {
        return;
      }

      const storedKey = value.key;

      if (Number(storedKey) === props.list.id) {
        return;
      }

      listsDropdownValue.value = {
        key: props.list.id.toString(),
        title: props.list.name,
      };

      if (storedKey === 'create') {
        store.commit(SHOW_MODAL, 'new-list');
        return;
      }

      await router.push({ name: 'list', params: { id: storedKey } });
      window.location.reload();
    });

    watch(settingsDropdownValue, (value) => {
      if (value.key === '') {
        return;
      }

      const storedKey = value.key;
      settingsDropdownValue.value = {
        key: '',
        title: '',
      };

      if (!props.list) {
        return;
      }

      if (storedKey === 'rename') {
        store.commit(SHOW_MODAL, 'rename-list');
      } else if (storedKey === 'delete') {
        const reply = confirm('Are you sure you want to delete this list?');  // eslint-disable-line

        if (!reply) {
          return;
        }

        api.removeList(props.list.id).then(() => {
          window.location.replace('/');
        });
      }
    });

    const updateCompanies = () => {
      if (!props.list) {
        return;
      }

      companyApi.list().then((payload) => {
        companies.splice(0);

        payload.forEach((item) => {
          const isSubscribed = !!(props.list as List).companies.find(
            (company) => (company.company.symbol === item.symbol),
          );

          const company: CompanyListSimple = {
            ...item,
            isSubscribed,
          };

          companies.push(company);
        });
      });
    };

    const toggleSubscrption = (company: CompanyListSimple) => {
      if (!props.list) {
        return;
      }

      const method = company.isSubscribed ? api.add : api.remove;

      method(props.list.id, company.symbol).finally(() => {
        emit('update');
      });
    };

    const filteredCompanies = computed(() => {
      if (!companySearch.value) {
        return companies;
      }

      const searchString = companySearch.value.toLocaleLowerCase();

      const toReturn = companies.filter((item) => {
        const name = item.name.toLowerCase();
        const symbol = item.symbol.toLowerCase();

        if (name.startsWith(searchString)) {
          return true;
        }

        if (symbol.startsWith(searchString)) {
          return true;
        }

        const nameAlgorithm = new Levenshtein(companySearch.value, item.name);

        if (nameAlgorithm.distance <= 5) {
          return true;
        }

        const symbolAlgorithm = new Levenshtein(companySearch.value, item.symbol);

        if (symbolAlgorithm.distance <= 2) {
          return true;
        }

        return false;
      });

      return toReturn;
    });

    watch(() => props.list, () => {
      if (props.list !== undefined) {
        listsDropdownValue.value = {
          key: props.list.id.toString(),
          title: props.list.name,
        };
      }

      updateCompanies();
    });

    onMounted(() => {
      api.lists().then((payload) => {
        listsDropdown.splice(0);
        payload.forEach((item) => {
          listsDropdown.push({
            key: item.id.toString(),
            title: item.name,
          });
        });
      });

      updateCompanies();
    });

    return {
      companies,
      companySearch,
      filteredCompanies,
      settingsDropdown,
      settingsDropdownValue,
      listsDropdownValues,
      listsDropdownValue,
      toggleSubscrption,
    };
  },
});
</script>

<style scoped>
.list-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  padding-top: 8px;
  padding-bottom: 8px;
}

.list-header-side {
  display: flex;
  align-items: center;
  gap: 20px;
}

.list-header-button {
  background: transparent;
  border: none;
  outline: none;
  cursor: pointer;
}

.list-title {
  cursor: pointer;
}

.list-title h2 {
  font-size: 16px;
  font-weight: 800;
  line-height: 110%;
  letter-spacing: 0.32px;
  text-transform: uppercase;
}

.list-filter {
  display: flex;
  align-items: center;
  gap: 8px;
}

.list-filter > span {
  color: var(--theme-text-color-2);
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.list-filter > button {
  font-size: 12px;
  font-weight: 600;
}

.list-checkbox {
  color: var(--theme-link-color);
}

.list-search {
  position: relative;
}

.list-search > input {
  padding: 8.5px 24px 8.5px 48px;
  border-radius: 100px;
  width: auto;
  font-size: 14px;
  font-weight: 600;
  line-height: 110%;
  letter-spacing: 0.28px;
  text-transform: uppercase;
  color: var(--theme-link-color);
  width: 127px;
}

.list-search > input::placeholder {
  color: var(--theme-link-color);
}

.list-search::before {
  content: '';
  position: absolute;
  width: 16px;
  height: 16px;
  background: no-repeat url('@/assets/icons/search.svg');
  background-size: 100% 100%;
  left: 24px;
  top: 50%;
  transform: translateY(-50%);
}

.list-company-search {
  position: relative;
  margin-bottom: 16px;
}

.list-company-search::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 8px;
  width: 16px;
  height: 16px;
  background: no-repeat url('@/assets/icons/search.svg');
  background-size: 100% 100%;
  transform: translateY(-50%);
  cursor: default;
}

.list-company-search > input {
  width: 100%;
  color: var(--theme-link-color);
  padding: 8px 8px 8px 33px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.list-company-search > input::placeholder {
  color: #7283FA;
}

.list-company-values {
  max-height: 329px;
  overflow-y: scroll;
}

.list-company-values::-webkit-scrollbar,
.list-company-values::-webkit-scrollbar-thumb {
  width: 4px;
  border-radius: 16px;
}

.list-company-values::-webkit-scrollbar-button {
  display: none;
}

.list-company-values::-webkit-scrollbar {
  background: rgba(0, 0, 0, .1);
}

.list-company-values::-webkit-scrollbar-thumb {
  background: var(--theme-link-color);
}

.list-company-value {
  display: flex;
  align-items: center;
  text-align: left;
  padding: 7px 0;
  font-size: 12px;
  font-weight: 600;
  gap: 8px;
}

.list-company-value > .checkbox {
  border-radius: 2px;
  border: 1px solid rgba(0, 0, 0, .4);
  width: 18px;
  height: 18px;
}
</style>

<style>
.list-title > .dropdown-value {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}
</style>
