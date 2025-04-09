<template>
  <div class="projects-page">
    <!-- ... 现有代码 ... -->
    
    <div class="status-filter">
      <Button
        :class="{ active: statusFilter === 'all' }"
        @click="statusFilter = 'all'"
      >
        全部  <!-- 原文: All -->
      </Button>
      <Button
        :class="{ active: statusFilter === 'active' }"
        @click="statusFilter = 'active'"
      >
        活跃  <!-- 原文: Active -->
      </Button>
      <Button
        :class="{ active: statusFilter === 'completed' }"
        @click="statusFilter = 'completed'"
      >
        已完成 
      </Button>
      <Button
        :class="{ active: statusFilter === 'archived' }"
        @click="statusFilter = 'archived'"
      >
        已归档 
      </Button>
    </div>
    
    <!-- ... 现有代码 ... -->
    
    <div v-if="loading" class="loading-state">
      <p>加载中...</p> 
    </div>
    
    <div v-else-if="filteredProjects.length === 0" class="empty-state">
      <div v-if="searchQuery" class="no-results">
        <p>没有找到匹配的项目</p> 
        <Button @click="clearSearch">
          清除搜索  <!-- 原文: Clear Search -->
        </Button>
      </div>
      <div v-else class="no-projects">
        <p>您还没有任何项目</p>  <!-- 原文: You don't have any projects yet -->
        <Button
          icon="plus"
          @click="showNewProjectDialog = true"
        >
          创建第一个项目
        </Button>
      </div>
    </div>
    
    <!-- ... 现有代码 ... -->
    
    <div class="project-description">
      <p v-if="project.description">{{ project.description }}</p>
      <p v-else class="text-muted">无描述</p>  
    </div>
    
    <!-- ... 现有代码 ... -->
    
    <!-- 新建项目对话框 --> 
    <Dialog
      v-model="showNewProjectDialog"
      title="创建新项目"  
    >
      <div class="mb-4">
        <label for="project-title" class="block mb-1">项目标题</label>  <!-- 原文: Project Title -->
        <input
          id="project-title"
          v-model="newProject.title"
          class="w-full"
          placeholder="输入项目标题..."  <!-- 原文: Enter project title... -->
        />
      </div>
      <div class="mb-4">
        <label for="project-description" class="block mb-1">项目描述 (可选)</label>  
        <textarea
          id="project-description"
          v-model="newProject.description"
          class="w-full"
          placeholder="输入项目描述..."  <!-- 原文: Enter project description... -->
          rows="3"
        ></textarea>
      </div>
      <!-- ... 现有代码 ... -->
    </Dialog>
  </div>
</template>

<script>
export default {
  // ... 现有代码 ...
  methods: {
    // ... 现有方法 ...
    translateStatus(status) {
      const statusMap = {
        'Active': '活跃',
        'Completed': '已完成', 
        'Archived': '已归档'  
      };
      return statusMap[status] || status;
    }
  }
}
</script>