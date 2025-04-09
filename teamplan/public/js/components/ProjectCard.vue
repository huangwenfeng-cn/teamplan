<template>
  <div class="project-card">
    <router-link
      :to="{ name: 'Project', params: { id: project.name } }"
      class="project-link"
    >
      <div class="project-header">
        <h3 class="project-title">{{ project.title }}</h3>
        <div class="project-status" :class="statusClass">
          {{ statusText }}
        </div>
      </div>
      
      <div v-if="project.description" class="project-description">
        <p>{{ project.description }}</p>
      </div>
      
      <div class="project-meta">
        <div class="meta-item tasks">
          <i class="icon icon-check-square"></i>
          <span>{{ project.task_count || 0 }} 任务</span>  <!-- 原文: tasks -->
        </div>
        
        <div class="meta-item discussions">
          <i class="icon icon-message-square"></i>
          <span>{{ project.discussion_count || 0 }} 讨论</span>  <!-- 原文: discussions -->
        </div>
        
        <div class="meta-item members">
          <i class="icon icon-users"></i>
          <span>{{ project.member_count || 0 }} 成员</span>  <!-- 原文: members -->
        </div>
      </div>
      
      <div class="project-progress">
        <div class="progress-label">
          <span>进度</span>  <!-- 原文: Progress -->
          <span>{{ project.progress || 0 }}%</span>
        </div>
        <div class="progress-bar">
          <div
            class="progress-value"
            :style="{ width: `${project.progress || 0}%` }"
          ></div>
        </div>
      </div>
    </router-link>
  </div>
</template>

<script>
import { computed } from 'vue';

export default {
  props: {
    project: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const statusClass = computed(() => {
      const status = props.project.status || 'Open';
      return {
        'status-open': status === 'Open',
        'status-completed': status === 'Completed',
        'status-canceled': status === 'Canceled'
      };
    });
    
    const statusText = computed(() => {
      const statusMap = {
        'Open': '进行�?,  // 原文: In Progress
        'Completed': '已完�?,  // 原文: Completed
        'Canceled': '已取�?  // 原文: Canceled
      };
      
      return statusMap[props.project.status] || props.project.status;
    });
    
    return {
      statusClass,
      statusText
    };
  }
}
</script>

<style scoped>
.project-card {
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  overflow: hidden;
  transition: box-shadow 0.2s, transform 0.2s;
}

.project-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.project-link {
  display: block;
  padding: 1.25rem;
  color: inherit;
  text-decoration: none;
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.project-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #2d3748;
  margin: 0;
}

.project-status {
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
}

.status-open {
  background-color: #ebf8ff;
  color: #3182ce;
}

.status-completed {
  background-color: #f0fff4;
  color: #38a169;
}

.status-canceled {
  background-color: #fff5f5;
  color: #e53e3e;
}

.project-description {
  margin-bottom: 1rem;
  color: #4a5568;
  font-size: 0.875rem;
  line-height: 1.5;
}

.project-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.875rem;
  color: #718096;
}

.meta-item {
  display: flex;
  align-items: center;
}

.meta-item .icon {
  margin-right: 0.25rem;
}

.project-progress {
  margin-top: 0.5rem;
}

.progress-label {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: #718096;
  margin-bottom: 0.25rem;
}

.progress-bar {
  height: 0.5rem;
  background-color: #e2e8f0;
  border-radius: 0.25rem;
  overflow: hidden;
}

.progress-value {
  height: 100%;
  background-color: #4299e1;
  border-radius: 0.25rem;
}
</style>
