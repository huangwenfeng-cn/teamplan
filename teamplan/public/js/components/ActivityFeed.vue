<template>
  <div class="activity-feed">
    <div v-if="activities.length === 0" class="empty-state">
      <p>暂无活动</p>  <!-- 原文: No activities -->
    </div>
    
    <div v-else class="activity-list">
      <div
        v-for="(activity, index) in activities"
        :key="index"
        class="activity-item"
      >
        <div class="activity-icon">
          <i class="icon" :class="getActivityIcon(activity.activity_type)"></i>
        </div>
        
        <div class="activity-content">
          <div class="activity-header">
            <UserAvatar
              :user="activity.user"
              :image-url="activity.user_image"
              :size="24"
            />
            <span class="activity-user">{{ activity.user }}</span>
            <span class="activity-action">{{ getActivityText(activity) }}</span>
          </div>
          
          <div class="activity-details">
            <router-link
              v-if="activity.reference_doctype && activity.reference_name"
              :to="getActivityLink(activity)"
              class="activity-link"
            >
              {{ activity.reference_title || activity.reference_name }}
            </router-link>
            <span v-else>{{ activity.content }}</span>
          </div>
          
          <div class="activity-time">
            {{ formatDateTime(activity.creation) }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { formatDateTime } from '../utils/date';
import UserAvatar from './UserAvatar.vue';

export default {
  components: {
    UserAvatar
  },
  props: {
    activities: {
      type: Array,
      default: () => []
    }
  },
  setup() {
    function getActivityIcon(type) {
      const icons = {
        'Task': 'icon-check-square',
        'Discussion': 'icon-message-square',
        'Project': 'icon-folder',
        'Comment': 'icon-message-circle',
        'Event': 'icon-calendar',
        'User': 'icon-user'
      };
      
      return icons[type] || 'icon-activity';
    }
    
    function getActivityText(activity) {
      const actions = {
        'create': '创建�?,  // 原文: created
        'update': '更新�?,  // 原文: updated
        'delete': '删除�?,  // 原文: deleted
        'complete': '完成�?,  // 原文: completed
        'comment': '评论�?,  // 原文: commented on
        'assign': '分配�?,  // 原文: assigned
        'join': '加入�?  // 原文: joined
      };
      
      const types = {
        'Task': '任务',  // 原文: task
        'Discussion': '讨论',  // 原文: discussion
        'Project': '项目',  // 原文: project
        'Comment': '评论',  // 原文: comment
        'Event': '事件',  // 原文: event
        'User': '用户'  // 原文: user
      };
      
      const action = actions[activity.action] || activity.action;
      const type = types[activity.reference_doctype] || activity.reference_doctype;
      
      return `${action} ${type}`;
    }
    
    function getActivityLink(activity) {
      const routes = {
        'Task': { name: 'TaskDetail', params: { id: activity.reference_name } },
        'Discussion': { name: 'DiscussionDetail', params: { id: activity.reference_name } },
        'Project': { name: 'Project', params: { id: activity.reference_name } },
        'Event': { name: 'Calendar' }
      };
      
      return routes[activity.reference_doctype] || { name: 'Home' };
    }
    
    return {
      getActivityIcon,
      getActivityText,
      getActivityLink,
      formatDateTime
    };
  }
}
</script>

<style scoped>
.activity-feed {
  padding: 1rem 0;
}

.empty-state {
  text-align: center;
  padding: 2rem 0;
  color: #a0aec0;
}

.activity-list {
  display: flex;
  flex-direction: column;
}

.activity-item {
  display: flex;
  padding: 1rem 0;
  border-bottom: 1px solid #e2e8f0;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  margin-right: 1rem;
  color: #4299e1;
  font-size: 1.25rem;
}

.activity-content {
  flex: 1;
}

.activity-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}

.activity-user {
  font-weight: 500;
  margin: 0 0.5rem;
}

.activity-action {
  color: #718096;
}

.activity-details {
  margin-bottom: 0.5rem;
}

.activity-link {
  color: #4299e1;
  text-decoration: none;
}

.activity-link:hover {
  text-decoration: underline;
}

.activity-time {
  font-size: 0.75rem;
  color: #a0aec0;
}
</style>
