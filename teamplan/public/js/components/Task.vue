<template>
  <div class="task-item" :class="{ 'is-completed': task.status === 'Completed' }">
    <div class="task-checkbox">
      <button
        class="checkbox-button"
        @click="toggleTaskStatus"
      >
        <i class="icon" :class="task.status === 'Completed' ? 'icon-check-circle' : 'icon-circle'"></i>
      </button>
    </div>
    
    <div class="task-content">
      <router-link
        :to="{ name: 'TaskDetail', params: { id: task.name } }"
        class="task-title"
      >
        {{ task.title }}
      </router-link>
      
      <div class="task-meta">
        <div v-if="task.project" class="meta-item project">
          <router-link :to="{ name: 'Project', params: { id: task.project_name } }">
            {{ task.project }}
          </router-link>
        </div>
        
        <div v-if="task.due_date" class="meta-item due-date" :class="{ 'is-overdue': isOverdue }">
          <i class="icon icon-calendar"></i>
          <span>{{ formatDate(task.due_date) }}</span>
          <span v-if="isOverdue" class="overdue-label">已逾期</span>  <!-- 原文: Overdue -->
        </div>
      </div>
    </div>
    
    <div class="task-actions">
      <div v-if="task.assigned_to" class="assigned-to">
        <UserAvatar
          :user="task.assigned_to"
          :image-url="task.assigned_to_image"
          :size="24"
        />
      </div>
      
      <button
        v-if="canEdit"
        class="action-button"
        @click="showEditMenu = !showEditMenu"
      >
        <i class="icon icon-more-vertical"></i>
      </button>
      
      <div v-if="showEditMenu" class="edit-menu">
        <button @click="editTask">
          <i class="icon icon-edit"></i> 编辑  <!-- 原文: Edit -->
        </button>
        <button @click="deleteTask" class="text-red-500">
          <i class="icon icon-trash"></i> 删除  <!-- 原文: Delete -->
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { formatDate } from '../utils/date';
import UserAvatar from './UserAvatar.vue';

export default {
  components: {
    UserAvatar
  },
  props: {
    task: {
      type: Object,
      required: true
    }
  },
  emits: ['update'],
  setup(props, { emit }) {
    const router = useRouter();
    const showEditMenu = ref(false);
    
    const isOverdue = computed(() => {
      if (!props.task.due_date) return false;
      
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      
      const dueDate = new Date(props.task.due_date);
      dueDate.setHours(0, 0, 0, 0);
      
      return dueDate < today && props.task.status !== 'Completed';
    });
    
    const canEdit = computed(() => {
      // 这里可以根据实际需求实现权限检�?
      return true;
    });
    
    function toggleTaskStatus() {
      const newStatus = props.task.status === 'Completed' ? 'Open' : 'Completed';
      
      // 这里应该调用API更新任务状�?
      console.log(`将任�?${props.task.name} 的状态更新为 ${newStatus}`);
      
      // 通知父组件更�?
      emit('update');
    }
    
    function editTask() {
      showEditMenu.value = false;
      router.push({ name: 'TaskDetail', params: { id: props.task.name } });
    }
    
    function deleteTask() {
      if (confirm('您确定要删除此任务吗�?)) {
        // 这里应该调用API删除任务
        console.log(`删除任务 ${props.task.name}`);
        
        // 通知父组件更�?
        emit('update');
      }
      
      showEditMenu.value = false;
    }
    
    return {
      showEditMenu,
      isOverdue,
      canEdit,
      toggleTaskStatus,
      editTask,
      deleteTask,
      formatDate
    };
  }
}
</script>

<style scoped>
.task-item {
  display: flex;
  align-items: flex-start;
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
  transition: background-color 0.2s;
}

.task-item:hover {
  background-color: #f7fafc;
}

.task-item.is-completed .task-title {
  text-decoration: line-through;
  color: #a0aec0;
}

.task-checkbox {
  margin-right: 0.75rem;
  padding-top: 0.125rem;
}

.checkbox-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  color: #a0aec0;
  font-size: 1.25rem;
}

.task-item.is-completed .checkbox-button {
  color: #48bb78;
}

.task-content {
  flex: 1;
}

.task-title {
  display: block;
  font-weight: 500;
  color: #2d3748;
  text-decoration: none;
  margin-bottom: 0.25rem;
}

.task-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  font-size: 0.875rem;
  color: #718096;
}

.meta-item {
  display: flex;
  align-items: center;
}

.meta-item.project a {
  color: #4299e1;
  text-decoration: none;
}

.meta-item.due-date.is-overdue {
  color: #e53e3e;
}

.meta-item .icon {
  margin-right: 0.25rem;
}

.overdue-label {
  margin-left: 0.25rem;
  font-size: 0.75rem;
  background-color: #e53e3e;
  color: white;
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
}

.task-actions {
  display: flex;
  align-items: center;
  position: relative;
}

.assigned-to {
  margin-right: 0.5rem;
}

.action-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  color: #a0aec0;
}

.edit-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.25rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  z-index: 10;
  min-width: 120px;
}

.edit-menu button {
  display: flex;
  align-items: center;
  width: 100%;
  text-align: left;
  padding: 0.5rem;
  background: none;
  border: none;
  cursor: pointer;
}

.edit-menu button:hover {
  background-color: #f7fafc;
}

.edit-menu button .icon {
  margin-right: 0.5rem;
}
</style>
