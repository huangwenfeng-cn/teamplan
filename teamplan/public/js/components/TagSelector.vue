<template>
  <div class="tag-selector">
    <div class="tags-container">
      <Tag
        v-for="(tag, index) in selectedTags"
        :key="index"
        :text="tag.text"
        :color="tag.color"
        removable
        @remove="removeTag(index)"
      />
      
      <div class="tag-input-container">
        <input
          ref="inputRef"
          type="text"
          class="tag-input"
          :placeholder="placeholder"
          v-model="inputValue"
          @focus="showSuggestions = true"
          @blur="hideSuggestionsDelayed"
          @keydown.enter.prevent="addTag"
          @keydown.delete="handleDelete"
        />
      </div>
    </div>
    
    <div
      v-if="showSuggestions && filteredSuggestions.length > 0"
      class="tag-suggestions"
    >
      <div
        v-for="(suggestion, index) in filteredSuggestions"
        :key="index"
        class="suggestion-item"
        :class="{ 'is-active': index === activeSuggestionIndex }"
        @mousedown="selectSuggestion(suggestion)"
        @mouseover="activeSuggestionIndex = index"
      >
        <div
          class="suggestion-color"
          :style="{ backgroundColor: suggestion.color }"
        ></div>
        <span class="suggestion-text">{{ suggestion.text }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch, nextTick } from 'vue';
import Tag from './Tag.vue';

export default {
  components: {
    Tag
  },
  props: {
    modelValue: {
      type: Array,
      default: () => []
    },
    suggestions: {
      type: Array,
      default: () => []
    },
    placeholder: {
      type: String,
      default: '添加标签...'  // 原文: Add tags...
    }
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const inputRef = ref(null);
    const inputValue = ref('');
    const showSuggestions = ref(false);
    const activeSuggestionIndex = ref(0);
    
    const selectedTags = computed(() => {
      return props.modelValue;
    });
    
    const filteredSuggestions = computed(() => {
      if (!inputValue.value) {
        return props.suggestions.filter(
          suggestion => !selectedTags.value.some(tag => tag.text === suggestion.text)
        );
      }
      
      const query = inputValue.value.toLowerCase();
      return props.suggestions.filter(
        suggestion => 
          suggestion.text.toLowerCase().includes(query) &&
          !selectedTags.value.some(tag => tag.text === suggestion.text)
      );
    });
    
    watch(inputValue, () => {
      activeSuggestionIndex.value = 0;
    });
    
    function addTag() {
      if (activeSuggestionIndex.value >= 0 && filteredSuggestions.value.length > 0) {
        selectSuggestion(filteredSuggestions.value[activeSuggestionIndex.value]);
        return;
      }
      
      if (!inputValue.value.trim()) return;
      
      // 检查是否已存在相同标签
      if (selectedTags.value.some(tag => tag.text.toLowerCase() === inputValue.value.toLowerCase())) {
        inputValue.value = '';
        return;
      }
      
      // 创建新标�?
      const newTag = {
        text: inputValue.value.trim(),
        color: getRandomColor()
      };
      
      const updatedTags = [...selectedTags.value, newTag];
      emit('update:modelValue', updatedTags);
      
      inputValue.value = '';
      
      // 保持焦点在输入框
      nextTick(() => {
        inputRef.value.focus();
      });
    }
    
    function removeTag(index) {
      const updatedTags = [...selectedTags.value];
      updatedTags.splice(index, 1);
      emit('update:modelValue', updatedTags);
    }
    
    function selectSuggestion(suggestion) {
      if (selectedTags.value.some(tag => tag.text === suggestion.text)) {
        return;
      }
      
      const updatedTags = [...selectedTags.value, suggestion];
      emit('update:modelValue', updatedTags);
      
      inputValue.value = '';
      
      // 保持焦点在输入框
      nextTick(() => {
        inputRef.value.focus();
      });
    }
    
    function handleDelete(event) {
      if (inputValue.value === '' && selectedTags.value.length > 0) {
        removeTag(selectedTags.value.length - 1);
      }
    }
    
    function hideSuggestionsDelayed() {
      setTimeout(() => {
        showSuggestions.value = false;
      }, 200);
    }
    
    function getRandomColor() {
      const colors = [
        '#4299e1', // 蓝色
        '#48bb78', // 绿色
        '#ed8936', // 橙色
        '#9f7aea', // 紫色
        '#f56565', // 红色
        '#38b2ac', // 青色
        '#ecc94b'  // 黄色
      ];
      
      return colors[Math.floor(Math.random() * colors.length)];
    }
    
    return {
      inputRef,
      inputValue,
      showSuggestions,
      activeSuggestionIndex,
      selectedTags,
      filteredSuggestions,
      addTag,
      removeTag,
      selectSuggestion,
      handleDelete,
      hideSuggestionsDelayed
    };
  }
}
</script>

<style scoped>
.tag-selector {
  position: relative;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.25rem;
  min-height: 42px;
}

.tag-input-container {
  flex: 1;
  min-width: 120px;
}

.tag-input {
  width: 100%;
  border: none;
  outline: none;
  padding: 0.25rem 0;
  font-size: 0.875rem;
}

.tag-suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.25rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  z-index: 10;
  max-height: 200px;
  overflow-y: auto;
}

.suggestion-item {
  display: flex;
  align-items: center;
  padding: 0.5rem 0.75rem;
  cursor: pointer;
}

.suggestion-item:hover,
.suggestion-item.is-active {
  background-color: #f7fafc;
}

.suggestion-color {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-right: 0.5rem;
}

.suggestion-text {
  font-size: 0.875rem;
}
</style>
