<template>
  <div class="task-list">
    <div class="list-header">
      <h3 class="list-title">{{ title }}</h3>
      <div class="list-actions">
        <Button
          v-if="canAddTask"
          icon="plus"
          size="small"
          @click="showAddTaskForm = true"
        >
          添加任务  <!-- 原文: Add Task -->
        </Button>
      </div>
    </div>
    
    <div v-if="loading" class="loading-state">
      <p>加载�?..</p>  <!-- 原文: Loading... -->
    </div>
    
    <div v-else-if="tasks.length === 0" class="empty-state">
      <p>暂无任务</p>  <!-- 原文: No tasks -->
    </div>
    
    <div v-else class="tasks">
      <div
        v-for="task in tasks"
        :key="task.name"
        class="task-item"
        :class="{ 'is-completed': task.status === 'Completed' }"
      >
        <div class="task-checkbox">
          <input
            type="checkbox"
            :checked="task.status === 'Completed'"
            @change="toggleTaskStatus(task)"
          />
        </div>
        
        <div class="task-content">
          <router-link
            :to="{ name: 'TaskDetail', params: { id: task.name } }"
            class="task-title"
          >
            {{ task.subject }}
          </router-link>
          
          <div v-if="task.description" class="task-description">
            {{ task.description }}
          </div>
          
          <div class="task-meta">
            <div v-if="task.due_date" class="task-due-date">
              <i class="icon icon-calendar"></i>
              <span>{{ formatDate(task.due_date) }}</span>
            </div>
            
            <div v-if="task.assigned_to" class="task-assignee">
              <i class="icon icon-user"></i>
              <span>{{ task.assigned_to }}</span>
            </div>
            
            <div v-if="task.project" class="task-project">
              <i class="icon icon-folder"></i>
              <span>{{ task.project }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="showAddTaskForm" class="add-task-form">
      <input
        v-model="newTask.subject"
        class="task-input"
        placeholder="任务标题..."  <!-- 原文: Task title... -->
        @keydown.enter="addTask"
      />
      
      <div class="form-actions">
        <Button
          secondary
          @click="showAddTaskForm = false"
        >
          取消  <!-- 原文: Cancel -->
        </Button>
        
        <Button
          :disabled="!newTask.subject"
          @click="addTask"
        >
          添加  <!-- 原文: Add -->
        </Button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { formatDate } from '../utils/date';
import Button from './Button.vue';

export default {
  components: {
    Button
  },
  props: {
    title: {
      type: String,
      default: '任务'  // 原文: Tasks
    },
    tasks: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    },
    projectId: {
      type: String,
      default: ''
    }
  },
  emits: ['add-task', 'update-task'],
  setup(props, { emit }) {
    const showAddTaskForm = ref(false);
    const newTask = ref({
      subject: '',
      project: props.projectId
    });
    
    const canAddTask = ref(true); // 这里可以根据实际需求实现权限检�?
    
    function toggleTaskStatus(task) {
      const updatedTask = { ...task };
      updatedTask.status = task.status === 'Completed' ? 'Open' : 'Completed';
      
      emit('update-task', updatedTask);
    }
    
    function addTask() {
      if (!newTask.value.subject.trim()) {
        return;
      }
      
      emit('add-task', { ...newTask.value });
      
      // 重置表单
      newTask.value = {
        subject: '',
        project: props.projectId
      };
      
      showAddTaskForm.value = false;
    }
    
    return {
      showAddTaskForm,
      newTask,
      canAddTask,
      toggleTaskStatus,
      addTask,
      formatDate
    };
  }
}
</script>

<style scoped>
.task-list {
  margin-bottom: 2rem;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.list-title {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
}

.loading-state,
.empty-state {
  padding: 2rem 0;
  text-align: center;
  color: #a0aec0;
}

.tasks {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.task-item {
  display: flex;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.25rem;
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
  display: flex;
  align-items: flex-start;
  padding-top: 0.25rem;
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

.task-description {
  font-size: 0.875rem;
  color: #718096;
  margin-bottom: 0.5rem;
}

.task-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  font-size: 0.75rem;
  color: #718096;
}

.task-due-date,
.task-assignee,
.task-project {
  display: flex;
  align-items: center;
}

.task-meta .icon {
  margin-right: 0.25rem;
}

.add-task-form {
  margin-top: 1rem;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.25rem;
}

.task-input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.25rem;
  margin-bottom: 0.75rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}
</style>
