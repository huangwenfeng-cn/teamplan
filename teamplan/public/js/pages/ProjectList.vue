<template>
  <div class="project-list-page">
    <PageHeader>
      <h1>项目</h1>  <!-- 原文: Projects -->
      <template #actions>
        <Button
          v-if="canCreateProject"
          icon="plus"
          @click="showNewProjectDialog = true"
        >
          创建项目  <!-- 原文: Create Project -->
        </Button>
      </template>
    </PageHeader>
    
    <Dialog
      v-model="showNewProjectDialog"
      title="创建新项目"  <!-- 原文: Create New Project -->
    >
      <div class="mb-4">
        <label for="project-title" class="block mb-1">项目标题</label> <!-- 原文: Project Title -->
        <input
          id="project-title"
          v-model="newProjectTitle"
          class="w-full"
          placeholder="输入项目标题..." <!-- 原文: Enter project title... -->
          @keydown.enter="createProject"
        />
      </div>
      <div>
        <label for="project-description" class="block mb-1">项目描述 (可选)</label> <!-- 原文: Project Description (optional) -->
        <textarea
          id="project-description"
          v-model="newProjectDescription"
          class="w-full"
          placeholder="输入项目描述..." <!-- 原文: Enter project description... -->
          rows="3"
        ></textarea>
      </div>
      <template #actions>
        <Button secondary @click="showNewProjectDialog = false">
          取消  <!-- 原文: Cancel -->
        </Button>
        <Button
          :loading="creatingProject"
          :disabled="!newProjectTitle"
          @click="createProject"
        >
          创建  <!-- 原文: Create -->
        </Button>
      </template>
    </Dialog>
  </div>
</template>