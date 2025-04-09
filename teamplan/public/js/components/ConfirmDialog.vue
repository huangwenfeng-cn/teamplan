<template>
  <Dialog
    v-model="isOpen"
    :title="title"
  >
    <div class="confirm-message">
      {{ message }}
    </div>
    <template #actions>
      <Button secondary @click="cancel">
        取消  <!-- 原文: Cancel -->
      </Button>
      <Button
        :class="{ 'is-danger': isDangerous }"
        @click="confirm"
      >
        确认  <!-- 原文: Confirm -->
      </Button>
    </template>
  </Dialog>
</template>

<script>
import Dialog from './Dialog.vue';
import Button from './Button.vue';

export default {
  components: {
    Dialog,
    Button
  },
  props: {
    modelValue: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: '确认'  // 原文: Confirm
    },
    message: {
      type: String,
      default: '您确定要执行此操作吗�?  // 原文: Are you sure you want to perform this action?
    },
    isDangerous: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    isOpen: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit('update:modelValue', value);
      }
    }
  },
  methods: {
    confirm() {
      this.$emit('confirm');
      this.isOpen = false;
    },
    cancel() {
      this.$emit('cancel');
      this.isOpen = false;
    }
  }
}
</script>
