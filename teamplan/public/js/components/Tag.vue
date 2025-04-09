<template>
  <div
    class="tag"
    :style="{ backgroundColor: bgColor, color: textColor }"
  >
    <span class="tag-text">{{ text }}</span>
    <button
      v-if="removable"
      class="remove-button"
      @click.stop="$emit('remove')"
    >
      <i class="icon icon-x"></i>
    </button>
  </div>
</template>

<script>
import { computed } from 'vue';

export default {
  props: {
    text: {
      type: String,
      required: true
    },
    color: {
      type: String,
      default: '#4299e1'
    },
    removable: {
      type: Boolean,
      default: false
    }
  },
  emits: ['remove'],
  setup(props) {
    // 根据背景色自动计算文本颜�?
    const textColor = computed(() => {
      // 简单的亮度计算
      const hex = props.color.replace('#', '');
      const r = parseInt(hex.substr(0, 2), 16);
      const g = parseInt(hex.substr(2, 2), 16);
      const b = parseInt(hex.substr(4, 2), 16);
      
      // 亮度公式
      const brightness = (r * 299 + g * 587 + b * 114) / 1000;
      
      // 亮度大于 128 使用深色文本，否则使用浅色文�?
      return brightness > 128 ? '#2d3748' : '#ffffff';
    });
    
    // 计算背景色（稍微淡化�?
    const bgColor = computed(() => {
      // 如果颜色是十六进制格�?
      if (props.color.startsWith('#')) {
        return props.color + '33'; // 添加 20% 透明�?
      }
      return props.color;
    });
    
    return {
      textColor,
      bgColor
    };
  }
}
</script>

<style scoped>
.tag {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.tag-text {
  margin-right: 0.25rem;
}

.remove-button {
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  opacity: 0.7;
}

.remove-button:hover {
  opacity: 1;
}
</style>
