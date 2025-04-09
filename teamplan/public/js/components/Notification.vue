<template>
  <div
    class="notification-item"
    :class="{ 'is-unread': !notification.read }"
    @click="viewNotification"
  >
    <div class="notification-icon">
      <i class="icon" :class="getNotificationIcon(notification.type)"></i>
    </div>
    
    <div class="notification-content">
      <div class="notification-message">
        {{ getNotificationMessage(notification) }}
      </div>
      
      <div class="notification-meta">
        <span class="notification-time">
          {{ formatDateTime(notification.creation) }}
        </span>
      </div>
    </div>
    
    <div class="notification-actions">
      <button
        v-if="!notification.read"
        class="mark-read-button"
        @click.stop="markAsRead(notification)"
      >
        <i class="icon icon-check"></i>
        <span>标为已读</span>  <!-- 原文: Mark as read -->
      </button>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';
import { formatDateTime } from '../utils/date';

export default {
  props: {
    notification: {
      type: Object,
      required: true
    }
  },
  emits: ['mark-as-read'],
  setup(props, { emit }) {
    const router = useRouter();
    
    function getNotificationIcon(type) {
      const icons = {
        'task': 'icon-check-square',
        'discussion': 'icon-message-square',
        'project': 'icon-folder',
        'comment': 'icon-message-circle',
        'event': 'icon-calendar',
        'mention': 'icon-at-sign'
      };
      
      return icons[type] || 'icon-bell';
    }
    
    function getNotificationMessage(notification) {
      // 这里可以根据通知类型和内容生成适当的消�?
      // 例如�?{user} �?{project} 中提到了�?
      return notification.message || '您有一条新通知';  // 原文: You have a new notification
    }
    
    function viewNotification() {
      // 如果未读，标记为已读
      if (!props.notification.read) {
        markAsRead(props.notification);
      }
      
      // 导航到相关页�?
      if (props.notification.link) {
        router.push(props.notification.link);
      }
    }
    
    function markAsRead(notification) {
      emit('mark-as-read', notification);
    }
    
    return {
      getNotificationIcon,
      getNotificationMessage,
      viewNotification,
      markAsRead,
      formatDateTime
    };
  }
}
</script>

<style scoped>
.notification-item {
  display: flex;
  align-items: flex-start;
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
  cursor: pointer;
  transition: background-color 0.2s;
}

.notification-item:hover {
  background-color: #f7fafc;
}

.notification-item.is-unread {
  background-color: #ebf8ff;
}

.notification-icon {
  margin-right: 1rem;
  color: #4299e1;
  font-size: 1.25rem;
}

.notification-content {
  flex: 1;
}

.notification-message {
  margin-bottom: 0.5rem;
  color: #2d3748;
}

.notification-item.is-unread .notification-message {
  font-weight: 500;
}

.notification-meta {
  font-size: 0.75rem;
  color: #a0aec0;
}

.notification-actions {
  margin-left: 1rem;
}

.mark-read-button {
  display: flex;
  align-items: center;
  background: none;
  border: none;
  color: #4299e1;
  font-size: 0.875rem;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
}

.mark-read-button:hover {
  background-color: #e6f7ff;
}

.mark-read-button .icon {
  margin-right: 0.25rem;
}
</style>
