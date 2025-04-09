<template>
  <div
    class="user-avatar"
    :style="{
      width: `${size}px`,
      height: `${size}px`,
      fontSize: `${size / 2}px`
    }"
  >
    <img
      v-if="imageUrl"
      :src="imageUrl"
      :alt="user"
      class="avatar-image"
    />
    <div v-else class="avatar-initials">
      {{ initials }}
    </div>
  </div>
</template>

<script>
import { computed } from 'vue';

export default {
  props: {
    user: {
      type: String,
      required: true
    },
    imageUrl: {
      type: String,
      default: ''
    },
    size: {
      type: Number,
      default: 40
    }
  },
  setup(props) {
    const initials = computed(() => {
      if (!props.user) return '';
      
      const parts = props.user.split(/\s+/);
      if (parts.length === 1) {
        return props.user.charAt(0).toUpperCase();
      }
      
      return (parts[0].charAt(0) + parts[parts.length - 1].charAt(0)).toUpperCase();
    });
    
    return {
      initials
    };
  }
}
</script>

<style scoped>
.user-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  overflow: hidden;
  background-color: #4299e1;
  color: white;
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-initials {
  font-weight: 600;
}
</style>
