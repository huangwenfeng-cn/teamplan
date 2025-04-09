<template>
  <div class="task-list-page">
    <PageHeader>
      <h1>任务</h1> <!-- 原文: Tasks -->
      <template #actions>
        <Button
          v-if="canCreateTask"
          icon="plus"
          @click="showNewTaskDialog = true"
        >
          创建任务 <!-- 原文: Create Task -->
        </Button>
      </template>
    </PageHeader>
    
    <!-- ... 现有代码 ... -->
    
    <div class="task-filters mb-4">
      <div class="filter-group">
        <span class="filter-label">状态：</span> <!-- 原文: Status: -->
        <Button
          v-for="status in statusOptions"
          :key="status.value"
          :class="{ active: filters.status === status.value }"
          small
          @click="setFilter('status', status.value)"
        >
          {{ status.label }}
        </Button>
      </div>
      <div class="filter-group">
        <span class="filter-label">分配给：</span> <!-- 原文: Assigned to: -->
        <Button
          v-for="option in assignedToOptions"
          :key="option.value"
          :class="{ active: filters.assigned_to === option.value }"
          small
          @click="setFilter('assigned_to', option.value)"
        >
          {{ option.label }}
        </Button>
      </div>
    </div>
    
    <!-- ... 现有代码 ... -->
  </div>
</template>

<script>
export default {
  // ... 现有代码 ...
  data() {
    return {
      // ... 现有代码 ...
      statusOptions: [
        { value: 'all', label: '全部' }, // 原文: All
        { value: 'open', label: '未完成' }, // 原文: Open
        { value: 'completed', label: '已完成' } // 原文: Completed
      ],
      assignedToOptions: [
        { value: 'all', label: '全部' }, // 原文: All
        { value: 'me', label: '我' }, // 原文: Me
        { value: 'unassigned', label: '未分配' } // 原文: Unassigned
      ],
      // ... 现有代码 ...
    }
  },
  // ... 现有代码 ...
}
</script>