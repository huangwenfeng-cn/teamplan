<template>
  <div class="tasks-page">
    <PageHeader>
      <h1>任务</h1>  <!-- 原文: Tasks -->
      <template #actions>
        <Button
          icon="plus"
          @click="showNewTaskDialog = true"
        >
          新建任务  <!-- 原文: New Task -->
        </Button>
      </template>
    </PageHeader>
    
    <div class="tasks-filters">
      <div class="search-filter">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索任务..."  <!-- 原文: Search tasks... -->
        />
        <i class="icon icon-search"></i>
      </div>
      
      <div class="status-filter">
        <Button
          :class="{ active: statusFilter === 'all' }"
          @click="statusFilter = 'all'"
        >
          全部  <!-- 原文: All -->
        </Button>
        <Button
          :class="{ active: statusFilter === 'open' }"
          @click="statusFilter = 'open'"
        >
          未完成
        </Button>
        <Button
          :class="{ active: statusFilter === 'completed' }"
          @click="statusFilter = 'completed'"
        >
          已完成
        </Button>
      </div>
      
      <div class="project-filter">
        <select v-model="projectFilter">
          <option value="">所有项目</option> 
          <option
            v-for="project in projects"
            :key="project.name"
            :value="project.name"
          >
            {{ project.title }}
          </option>
        </select>
      </div>
      
      <div class="assigned-filter">
        <select v-model="assignedFilter">
          <option value="">所有分配</option> 
          <option value="me">分配给我</option> 
          <option value="unassigned">未分配</option> 
        </select>
      </div>
    </div>
    
    <div v-if="loading" class="loading-state">
      <p>加载中...</p> 
    </div>
    
    <div v-else-if="filteredTasks.length === 0" class="empty-state">
      <div v-if="hasFilters" class="no-results">
        <p>没有找到匹配的任务</p> 
        <Button @click="clearFilters">
          清除筛选条件
        </Button>
      </div>
      <div v-else class="no-tasks">
        <p>您还没有任何任务</p>  <!-- 原文: You don't have any tasks yet -->
        <Button
          icon="plus"
          @click="showNewTaskDialog = true"
        >
          创建第一个任务
        </Button>
      </div>
    </div>
    
    <div v-else class="tasks-list">
      <Task
        v-for="task in filteredTasks"
        :key="task.name"
        :task="task"
        @update="fetchTasks"
      />
    </div>
    
    <!-- 新建任务对话框 --> 
    <Dialog
      v-model="showNewTaskDialog"
      title="创建新任务" 
    >
      <div class="mb-4">
        <label for="task-title" class="block mb-1">任务标题</label>  <!-- 原文: Task Title -->
        <input
          id="task-title"
          v-model="newTask.title"
          class="w-full"
          placeholder="输入任务标题..."  <!-- 原文: Enter task title... -->
        />
      </div>
      <div class="mb-4">
        <label for="task-description" class="block mb-1">任务描述 (可选)</label>  
        <textarea
          id="task-description"
          v-model="newTask.description"
          class="w-full"
          placeholder="输入任务描述..."  <!-- 原文: Enter task description... -->
          rows="3"
        ></textarea>
      </div>
      <div class="mb-4">
        <label for="task-project" class="block mb-1">项目</label>  <!-- 原文: Project -->
        <select
          id="task-project"
          v-model="newTask.project"
          class="w-full"
        >
          <option value="">选择项目</option>  <!-- 原文: Select Project -->
          <option
            v-for="project in projects"
            :key="project.name"
            :value="project.name"
          >
            {{ project.title }}
          </option>
        </select>
      </div>
      <div class="mb-4">
        <label for="task-assigned-to" class="block mb-1">分配给</label> 
        <select
          id="task-assigned-to"
          v-model="newTask.assigned_to"
          class="w-full"
        >
          <option value="">未分配</option> 
          <option
            v-for="user in projectMembers"
            :key="user.name"
            :value="user.name"
          >
            {{ user.full_name || user.name }}
          </option>
        </select>
      </div>
      <div class="mb-4">
        <label for="task-due-date" class="block mb-1">截止日期 (可选)</label> 
        <input
          id="task-due-date"
          v-model="newTask.due_date"
          type="date"
          class="w-full"
        />
      </div>
      <template #actions>
        <Button secondary @click="showNewTaskDialog = false">
          取消  <!-- 原文: Cancel -->
        </Button>
        <Button
          :disabled="!newTask.title || !newTask.project"
          @click="createTask"
        >
          创建  <!-- 原文: Create -->
        </Button>
      </template>
    </Dialog>
  </div>
</template>