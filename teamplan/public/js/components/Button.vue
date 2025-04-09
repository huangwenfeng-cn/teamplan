<template>
  <button
    class="button"
    :class="{
      'is-primary': !secondary,
      'is-secondary': secondary,
      'is-small': size === 'small',
      'is-large': size === 'large',
      'is-full-width': fullWidth,
      'is-loading': loading
    }"
    :disabled="disabled || loading"
    @click="$emit('click', $event)"
  >
    <i v-if="icon && !loading" class="icon" :class="`icon-${icon}`"></i>
    <span v-if="loading" class="loading-spinner"></span>
    <span v-if="$slots.default" class="button-text">
      <slot></slot>
    </span>
  </button>
</template>

<script>
export default {
  props: {
    secondary: {
      type: Boolean,
      default: false
    },
    size: {
      type: String,
      default: 'medium',
      validator: value => ['small', 'medium', 'large'].includes(value)
    },
    fullWidth: {
      type: Boolean,
      default: false
    },
    icon: {
      type: String,
      default: ''
    },
    loading: {
      type: Boolean,
      default: false
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  emits: ['click']
}
</script>

<style scoped>
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s, border-color 0.2s, color 0.2s;
  border: 1px solid transparent;
}

.button:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.5);
}

.button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.is-primary {
  background-color: #4299e1;
  color: white;
}

.is-primary:hover:not(:disabled) {
  background-color: #3182ce;
}

.is-secondary {
  background-color: white;
  border-color: #e2e8f0;
  color: #4a5568;
}

.is-secondary:hover:not(:disabled) {
  background-color: #f7fafc;
}

.is-small {
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
}

.is-large {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
}

.is-full-width {
  width: 100%;
}

.icon {
  margin-right: 0.5rem;
}

.button-text:empty + .icon {
  margin-right: 0;
}

.loading-spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spin 0.75s linear infinite;
  margin-right: 0.5rem;
}

.button-text:empty + .loading-spinner {
  margin-right: 0;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
