<template>
  <div v-if="modelValue" class="dialog-overlay" @click="closeOnOverlayClick && close()">
    <div class="dialog" @click.stop>
      <div class="dialog-header">
        <h2 class="dialog-title">{{ title }}</h2>
        <button class="close-button" @click="close">
          <i class="icon icon-x"></i>
        </button>
      </div>
      
      <div class="dialog-body">
        <slot></slot>
      </div>
      
      <div v-if="$slots.actions" class="dialog-footer">
        <slot name="actions"></slot>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted, onBeforeUnmount } from 'vue';

export default {
  props: {
    modelValue: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: ''
    },
    closeOnOverlayClick: {
      type: Boolean,
      default: true
    }
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    function close() {
      emit('update:modelValue', false);
    }
    
    function handleEscape(event) {
      if (event.key === 'Escape' && props.modelValue) {
        close();
      }
    }
    
    onMounted(() => {
      document.addEventListener('keydown', handleEscape);
    });
    
    onBeforeUnmount(() => {
      document.removeEventListener('keydown', handleEscape);
    });
    
    return {
      close
    };
  }
}
</script>

<style scoped>
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
}

.dialog {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.dialog-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.dialog-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #2d3748;
}

.close-button {
  background: none;
  border: none;
  color: #a0aec0;
  cursor: pointer;
  font-size: 1.25rem;
}

.dialog-body {
  padding: 1rem;
  overflow-y: auto;
  flex: 1;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid #e2e8f0;
}
</style>
