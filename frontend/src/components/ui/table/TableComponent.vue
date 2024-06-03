<template>
  <div
    class="table"
  >
    <div class="table-modal" v-if="commentModal && isCommentModalShown"
      :style="{ top: modalPosition.Y + 'px', left: modalPosition.X + 'px' }">
      <Card>
        <div class="table-modal-header">
          <div class="table-modal-header-section">
            <img src="@/assets/icons/info.svg" alt="Info">
            <p>Comments are saved automatically</p>
          </div>
          <button @click="isCommentModalShown = false">
            <img src="@/assets/icons/cross.svg" alt="Cross">
          </button>
        </div>
        <div class="table-modal-comments">
          <div
            v-for="(comment, index) in data.comments"
            :key="index"
            class="table-modal-comment"
            :class="{
              'table-modal-comment__expand': activeComment === index,
            }"
          >
            <div class="table-modal-comment-visible">
              <span>
                {{ (getRowIndexByField(comment.field) + 1).toString().padStart(2, '0') }}
              </span>
              <p>{{ data.rows[getRowIndexByField(comment.field)]?.name.replace('ㅤ', '') }}</p>
              <p class="table-comment-spoiler" v-if="activeComment !== index">{{ comment.text }}</p>
              <button @click="activeComment = activeComment === index ? undefined : index">
                <img src="@/assets/icons/arrow-small.svg" alt="Arrow">
              </button>
            </div>
            <div class="table-modal-comment-hidden" v-if="activeComment === index">
              <div class="table-modal-comment-title">
                <input
                  type="text"
                  v-model="comment.title"
                  placeholder="Enter header text"
                  @change="saveComment(index)"
                  v-if="!comment.column"
                >
                <p v-else>{{ new Date(comment.createdAt).toLocaleDateString() }}</p>
                <div class="table-modal-comment-control">
                  <button @click="deleteComment(index)">
                    <img src="@/assets/icons/trash.svg" alt="Trash">
                  </button>
                </div>
              </div>
              <p>{{ new Date(comment.createdAt).toLocaleDateString() }}</p>

              <Textarea
                v-model:value="comment.text"
                placeholder="Enter comment text"
                @change="saveComment(index)"
              />
            </div>
          </div>
        </div>
      </Card>
    </div>
    <table>
      <thead>
        <tr v-if="!data.hideCategories">
          <th
            v-for="(category, index) in data.categories"
            :key="index"
            :colspan="
              category.values.length + (
                index === 0 || (
                  data.comments !== undefined && index === data.categories.length - 1
                ) ? 1 : 0
              )
            "
            class="table-category"
          >{{ category.name }}</th>
        </tr>
        <tr class="table-columns">
          <th>{{ data.columnName || '' }}</th>
          <th
            v-for="(column, index) in columns"
            :key="index"
          >{{ column }}</th>
          <th class="table-comment" v-if="data.comments !== undefined">
            <img src="@/assets/icons/comment.svg" alt="Comment">
          </th>
        </tr>
        <tr class="table-functions" v-if="hasFunctions">
          <template v-for="(category, index) in data.categories" :key="index">
            <th
              :colspan="
                category.values.length + (
                  index === 0 || (
                    data.comments !== undefined && index === data.categories.length - 1
                  ) ? 1 : 0
                )
              "
            >
              <template v-if="category.key === 'projected'">
                <slot name="functions" />
              </template>
            </th>
          </template>
        </tr>
      </thead>
      <tbody>
        <template v-for="(row, index) in data.rows" :key="index">
          <tr>
            <td class="table-row">
              <span v-if="row.showCounter">{{ (index + 1).toString().padStart(2, '0') }}</span>
              {{ row.name }}
              <Help align="bottom" v-if="row.help">{{ row.help }}</Help>
            </td>
            <template
              v-for="(category, index) in data.categories.filter((x) => !x.hidden)"
              :key="index"
            >
              <td
                v-for="(value, index) in category.values"
                :key="index"
                :style="{
                  'font-size': override(row, category).size || '',
                  'font-weight': override(row, category).weight || '',
                  'color': row.editable && category.editable
                    ? 'var(--theme-link-color)' : (category.color || ''),
                    'cursor': (row.editable && category.editable) ? 'pointer' : '',
                  }"
                class="table-value"
                @click="
                  (data.comments !== undefined && isCommentEnabled
                    && !(row.editable && category.editable)) ?
                  createComment($event, row.key, value[data.column]) : (
                    (row.editable && category.editable) ? (
                      data.editEvent ?
                      onFieldChange() :
                      editValue(
                        value,
                        row.key,
                        handleValue(row, value[row.key], value, category, false),
                      )
                    ) :
                    undefined
                  )
                "
              >
                {{
                  value[row.key] || value[row.key] === 0
                    ? handleValue(row, value[row.key], value, category)
                    : '-'
                }}
                <button
                  class="table-circle"
                  @click="showComment(getCommentIndex(row.key, value[data.column]))"
                  v-if="getCommentIndex(row.key, value[data.column]) !== -1"
                >•</button>
                <input
                  type="text"
                  v-model="value[row.key]"
                  class="table-editable"
                  @input="onEditEvent"
                  v-if="editableContext == value && editableKey == row.key"
                />
                <div class="table-new-comment"></div>
              </td>
            </template>
            <td
              class="table-comment"
              @click="(data.comments !== undefined && isCommentEnabled) &&
                createComment($event, row.key)"
              v-if="data.comments !== undefined"
            >
              <button
                @click="isCommentModalShown = true"
                v-if="(data.comments || []).filter((x) => x.field === row.key).length > 0"
              >
                <img src="@/assets/icons/comment.svg" alt="Comment">
              </button>
              <div class="table-new-comment"></div>
            </td>
          </tr>
          <tr class="table-spacer" v-if="row.separate"></tr>
        </template>
        <component
          v-for="(row, index) in rows"
          :key="index"
          :is="row"
          :index="data.rows.length + index"
          :comments="data.comments !== undefined"
        />
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import {
  defineComponent,
  PropType,
  nextTick,
  computed,
  ref,
  onUpdated,
  useSlots,
} from 'vue';
import { useStore } from 'vuex';

import { useCompiler } from '@/controllers/compiler';

import { COMMENT_CURSOR } from '@/store/actions/application';

import Card from '../CardComponent.vue';
import Textarea from '../TextareaComponent.vue';
import Help from '../HelpComponent.vue';

import {
  TableCategory,
  TableData,
  TableOverride,
  TableRow,
} from './types';

export default defineComponent({
  name: 'TableComponent',
  components: {
    Card,
    Textarea,
    Help,
  },
  props: {
    data: {
      type: Object as PropType<TableData>,
      required: true,
    },
    commentModal: {
      type: Boolean,
      required: false,
      default: true,
    },
  },
  emits: ['edit', 'newComment', 'editComment', 'deleteComment'],
  setup(props, { emit }) {
    const store = useStore();

    const slots = useSlots();
    const defaultSlot = slots.default && slots.default();
    const rows = defaultSlot?.filter((item) => (item.type as any).name === 'RowComponent') || [];
    const hasFunctions = !!slots.functions;

    const editableContext = ref<any>();
    const editableKey = ref<string>();

    const isCommentModalShown = ref(false);
    const modalPosition = ref<any>({ X: Number, Y: Number });
    const activeComment = ref<number | undefined>(undefined);

    const computedData = computed(() => props.data);
    const { compile, clearCache } = useCompiler(computedData);

    const isCommentEnabled = computed(() => store.state.application.commentCursor);
    const columns = computed(() => {
      const data: string[] = [];
      props.data.categories.forEach((category) => {
        if (!category.hidden) {
          category.values.forEach((value) => {
            data.push(value[props.data.column]);
          });
        }
      });

      return data;
    });

    const override = (row: TableRow, category: TableCategory): TableRow | TableOverride => {
      if (row.override && row.override[category.name]) {
        return row.override[category.name];
      }
      return row;
    };

    const handleValue = (
      row: TableRow,
      value: number | string,
      context: any,
      category: TableCategory,
      render = true,
    ) => {
      let expression: string | number | undefined = Number(value);

      if (Number.isNaN(expression)) {
        expression = value.toString();
      }

      expression = compile(expression, context);

      if (typeof expression === 'string') {
        return expression;
      }

      const overrided = override(row, category);
      if (row.key === 'enterpriseValue') {
        console.log(' ******************************** here is enterprise value ******************************** ');
        console.log(value);
        console.log(' ******************************** here is context ********************************');
        console.log(context);
        console.log(' ******************************** here is category ********************************');
        console.log(category);
        console.log(' ******************************** here is render ********************************');
        console.log(render);
        console.log(' ******************************** here is expression ********************************');
        console.log(expression);
        console.log(' ******************************** here is overrided ********************************');
        console.log(overrided);
        if (overrided.handler && render) {
          console.log(overrided.handler(expression));
        }
      }
      return overrided.handler && render ? overrided.handler(expression) : expression;
    };

    const onFieldChange = (column?: string, field?: string, value?: number) => {
      emit('edit', column, field, value);
    };

    const editValue = (context: any, key: string, value: any) => {
      context[key] = value; // eslint-disable-line
      editableContext.value = context;
      editableKey.value = key;

      nextTick(() => {
        const editable = document.querySelector('.table-editable');

        if (editable === undefined) {
          return;
        }

        const onClickOutside = (event: Event | KeyboardEvent) => {
          if (event.type !== 'keydown' || (event as KeyboardEvent).code !== 'Enter') {
            const target = event.target as HTMLElement;

            if (target.classList.contains('table-editable') || target.classList.contains('table-value')) {
              return;
            }
          }

          if (editableContext.value && editableKey.value) {
            const numeric = Number(editableContext.value[editableKey.value as string]);
            if (!Number.isNaN(numeric)) {
              onFieldChange(
                editableContext.value[props.data.column],
                editableKey.value,
                numeric,
              );
            }
          }

          editableContext.value = undefined;
          editableKey.value = undefined;

          window.removeEventListener('mousedown', onClickOutside);
          window.removeEventListener('keydown', onClickOutside);
        };

        window.addEventListener('mousedown', onClickOutside);
        window.addEventListener('keydown', onClickOutside);
      });
    };

    const onEditEvent = (event: Event) => {
      const target = event.target as HTMLInputElement;
      target.value = target.value.replace(',', '.');
    };

    const showComment = (index: number) => {
      activeComment.value = index;
      isCommentModalShown.value = true;
      // store.commit(COMMENT_CURSOR, false);
    };

    const closeComment = () => {
      isCommentModalShown.value = false;
      // store.commit(COMMENT_CURSOR, true);
    };

    const createComment = (event: MouseEvent, field: string, column?: string) => {
      // Get mouse coordinates relative to the document
      const mouseX = event.pageX - (event.pageX - 300) * (1 / 2);
      const mouseY = event.pageY - window.innerHeight * (1 / 2)
        - (event.pageY - window.scrollY - window.innerHeight / 2) / 5 + 50;
      const modalWidth = 850; // Adjust as needed
      const documentWidth = document.documentElement.clientWidth;
      const documentHeight = document.documentElement.clientHeight;
      const modalX = Math.min(mouseX, documentWidth - modalWidth);
      modalPosition.value = { X: modalX, Y: mouseY };
      emit('newComment', {
        column,
        field,
        title: '',
        text: '',
        createdAt: (new Date()).toISOString(),
      });

      if ((props.data.comments?.length || 0) > 0) {
        showComment(0);
      }
    };

    const getCommentIndex = (field: string, column: string) => (
      props.data.comments || []
    ).findIndex((x) => x.field === field && x.column == column);  // eslint-disable-line

    const saveComment = (index: number) => {
      emit('editComment', index);
    };

    const deleteComment = (index: number) => {
      emit('deleteComment', index);
    };

    const getRowIndexByField = (field: string) => props.data.rows.findIndex((x) => x.key === field);

    onUpdated(() => clearCache());

    return {
      rows,
      columns,
      hasFunctions,
      handleValue,
      editValue,
      onFieldChange,
      onEditEvent,
      editableContext,
      editableKey,
      activeComment,
      isCommentModalShown,
      isCommentEnabled,
      modalPosition,
      createComment,
      getCommentIndex,
      showComment,
      closeComment,
      saveComment,
      deleteComment,
      getRowIndexByField,
      override,
    };
  },
});
</script>

<style>
.table {
  --font-size-8: 8px;
  --font-size-10: 10px;
  --font-size-12: 12px;
  --font-size-14: 14px;
  position: relative;
  display: flex;
  border-top-left-radius: 16px;
  border-top-right-radius: 16px;
  font-size: var(--font-size-12);
  font-weight: 500;
  text-align: left;
  height: 100%;
}

.table.table__comment {
  cursor: url('@/assets/icons/cursor.svg'), auto;
}

.table > .table-modal {
  position: fixed;
  /* position: fixed;
  top: 50%;
  left: 50%; */
  transform: translate(0%, 0%);
  z-index: 10;
  min-width: 428px;
}

.table > .table-modal .table-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 16px;
}

.table > .table-modal .table-modal-header > .table-modal-header-section {
  display: flex;
  align-items: center;
  gap: 8px;
}

.table > .table-modal .table-modal-header > .table-modal-header-section > p {
  font-size: var(--font-size-14);
  font-weight: 600;
}

.table > .table-modal .table-modal-comment {
  border-top: 1px solid var(--theme-text-gray-2);
  padding: 9px 0;
}

.table > .table-modal .table-modal-comment .table-modal-comment-visible {
  position: relative;
  display: flex;
  gap: 8px;
  align-items: center;
}

.table > .table-modal .table-modal-comment .table-modal-comment-visible > span {
  font-size: var(--font-size-10);
  color: var(--theme-text-gray);
}

.table > .table-modal > .card {
  padding-bottom: 0;
}

.table > .table-modal .table-modal-comment .table-modal-comment-visible > p {
  font-size: var(--font-size-12);
  font-weight: 500;
  color: var(--theme-text-color-2);
}

.table > .table-modal .table-modal-comment .table-modal-comment-visible > .table-comment-spoiler {
  color: #B3B3B3;
  font-size: 12px;
  white-space: nowrap;
  text-overflow: ellipsis;
  max-width: 165px;
  overflow: hidden;
}

.table > .table-modal .table-modal-comment .table-modal-comment-visible > button {
  position: absolute;
  top: 50%;
  right: 0;
  top: 50%;
  transform: translateY(-50%) rotateX(180deg);
}

.table > .table-modal .table-modal-comment.table-modal-comment__expand
.table-modal-comment-visible > button {
  transform: translateY(-50%);
}

.table > .table-modal .table-modal-comment .table-modal-comment-hidden {
  background: #F4F6FF;
  padding: 16px;
  border-radius: 16px;
  margin-top: 9px;
}

.table > .table-modal .table-modal-comment .table-modal-comment-hidden input,
.table > .table-modal .table-modal-comment .table-modal-comment-hidden textarea {
  background: none;
  outline: none;
  border: none;
  color: var(--theme-text-color-2);
}

.table > .table-modal .table-modal-comment .table-modal-comment-hidden input::placeholder,
.table > .table-modal .table-modal-comment .table-modal-comment-hidden textarea::placeholder {
  color: var(--theme-text-color-2);
}

.table > .table-modal .table-modal-comment .table-modal-comment-hidden textarea {
  display: block;
  height: auto;
  width: 100%;
  resize: none;
}

.table > .table-modal .table-modal-comment .table-modal-comment-hidden
.table-modal-comment-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 7px;
}

.table > .table-modal .table-modal-comment .table-modal-comment-hidden
.table-modal-comment-title > input {
  text-transform: uppercase;
  font-size: var(--font-size-14);
  font-weight: 800;
}

.table > .table-modal .table-modal-comment .table-modal-comment-hidden > p {
  font-size: var(--font-size-12);
  font-weight: 600;
  color: #B3B3B3;
  margin-bottom: 16px;
}

.table > .table-modal button {
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  outline: none;
  background: none;
  cursor: pointer;
}

.table table {
  border: none;
  border-collapse: collapse;
  width: 100%;
}

.table table > thead {
  /* position: sticky; */
  top: 0;
  z-index: 3;
}

.table table > thead > tr:first-child > th:first-child {
  border-top-left-radius: 16px;
}

.table table > thead > tr:first-child > th:last-child {
  border-top-right-radius: 16px;
}

.table table > thead,
.table table > tbody {
  width: 100%;
  border: none;
  border-collapse: collapse;
}

.table tr {
  height: 32px;
}

.table th, .table td {
  height: 100%;
  min-width: 61px;
  width: 61px;
  padding: 0 3px;
}

.table .table-category {
  background: var(--theme-link-color);
  font-weight: 800;
  font-size: var(--font-size-10);
  color: var(--theme-text-color-contrast);
  text-transform: uppercase;
  text-align: center;
  border-right: 1px solid var(--theme-background-color);
}

.table .table-columns {
  background: var(--theme-table-color);
}

.table tbody > tr > th {
  position: relative;
  z-index: 0;
}

.table tbody > tr > .table-row > .helper {
  display: inline-block;
  margin-left: 4px;
  margin-bottom: -2px;
}

.table .table-columns > th,
.table tbody > tr > .table-row:first-child {
  font-weight: 600;
}

.table .table-columns > th:first-child {
  padding-left: 45px;
  min-width: calc(170px + 45px);
  box-sizing: border-box;
}

.table .table-functions {
  background: #F4F6FF;
}

.table .table-functions th > * {
  margin-right: 36px;
  font-weight: 500;
  font-size: var(--font-size-10) !important;
}

.table .table-functions th > *:last-child {
  margin-right: 0;
}

.table tbody > tr > .table-row:first-child {
  padding-left: 24px;
  min-width: calc(154px + 24px);
  box-sizing: border-box;
}

.table tbody > tr > .table-row > span {
  font-size: var(--font-size-10);
  font-weight: 400;
  color: var(--theme-text-gray-3);
  padding-right: 8px;
}

.table tbody > tr > td {
  --padding-right: 7px;
  border-top: 1px solid var(--theme-background-color);
  background: var(--theme-text-color-contrast);
  padding-right: var(--padding-right);
}

.table tbody > tr > td:last-child {
  padding-right: 0;
}

.table .table-spacer {
  height: 16px;
}

.table .table-value {
  position: relative;
}

.table .table-comment {
  position: relative;
  width: 36px;
  min-width: 36px;
  padding-right: 24px;
  box-sizing: border-box;
}

.table .table-comment > button {
  background: none;
  outline: none;
  border: none;
  cursor: pointer;
}

.table .table-editable {
  position: absolute;
  top: 20%;
  left: 50%;
  max-width: 100%;
  width: 100%;
  height: 120%;
  transform: translate(-50%, -20%);
  border: none;
  outline: none;
  border-radius: 8px;
  box-shadow: 0px 4px 24px 0px rgba(51, 72, 251, 0.3), 0px 4px 16px 0px rgba(0, 0, 0, 0.05);
  text-align: center;
  z-index: 1;
  padding: 0 8px;
  color: var(--theme-link-color);
  font-weight: 500;
  font-size: var(--font-size-12);
}

.table tbody > tr > td > .table-circle {
  color: var(--theme-link-color);
  font-size: 12px;
  font-weight: 500;
  border: none;
  outline: none;
  background: none;
  cursor: pointer;
}

.table tbody > tr > td > .table-new-comment {
  position: absolute;
  top: 50%;
  right: calc(var(--padding-right) + 10px);
  transform: translateY(-50%);
  width: 14px;
  height: 14px;
  background: url('@/assets/icons/add-comment.svg');
  background-size: 100% 100%;
  background-repeat: no-repeat;
  display: none;
}

.table.table__comment tbody > tr > td:hover > .table-new-comment {
  display: block;
}

/* @media screen and (max-width: 1512px) {
  .table {
    --font-size-12: 11px;
    --font-size-14: 13px;
  }

  .table th, .table td {
    min-width: 40px;
    width: 40px;
    padding: 0 2px;
  }

  .table tbody > tr > td {
    --padding-right: 3px;
  }
}

@media screen and (max-width: 1410px) {
  .table {
    --font-size-8: 7px;
    --font-size-10: 9px;
  }
}

@media screen and (max-width: 1300px) {
  .table {
    --font-size-8: 6px;
    --font-size-10: 8px;
    --font-size-12: 10px;
    --font-size-14: 12px;
  }

  .table .table-functions th > * {
    margin-right: 24px;
  }
} */
</style>
