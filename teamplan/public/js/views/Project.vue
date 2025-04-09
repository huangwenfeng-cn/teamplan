<template>
  <div class="project-view">
    <div class="project-header">
      <div class="project-color" :style="{ backgroundColor: project.color || '#4299e1' }"></div>
      <h1 class="project-title">{{ project.title }}</h1>
      
      <div class="project-actions">
        <Button
          icon="edit"
          secondary
          @click="showEditDialog = true"
        >
          编辑项目  <!-- 原文: Edit Project -->
        </Button>
      </div>
    </div>
    
    <div class="project-tabs">
      <router-link
        :to="{ name: 'ProjectOverview', params: { id: projectId } }"
        class="tab"
      >
        概览  <!-- 原文: Overview -->
      </router-link>
      
      <router-link
        :to="{ name: 'ProjectTasks', params: { id: projectId } }"
        class="tab"
      >
        任务  <!-- 原文: Tasks -->
      </router-link>
      
      <router-link
        :to="{ name: 'ProjectDiscussions', params: { id: projectId } }"
        class="tab"
      >
        讨论  <!-- 原文: Discussions -->
      </router-link>
      
      <router-link
        :to="{ name: 'ProjectFiles', params: { id: projectId } }"
        class="tab"
      >
        文件  <!-- 原文: Files -->
      </router-link>
      
      <router-link
        :to="{ name: 'ProjectMembers', params: { id: projectId } }"
        class="tab"
      >
        成员  <!-- 原文: Members -->
      </router-link>
    </div>
    
    <router-view></router-view>
    
    <Dialog
      v-model="showEditDialog"
      title="编辑项目"  <!-- 原文: Edit Project -->
    >
      <form @submit.prevent="updateProject">
        <div class="form-group">
          <label for="project-title">项目名称</label>  <!-- 原文: Project Title -->
          <input
            id="project-title"
            v-model="editForm.title"
            type="text"
            required
          />
        </div>
        
        <div class="form-group">
          <label for="project-description">项目描述</label>  <!-- 原文: Project Description -->
          <textarea
            id="project-description"
            v-model="editForm.description"
            rows="4"
          ></textarea>
        </div>
        
        <div class="form-group">
          <label>项目颜色</label>  <!-- 原文: Project Color -->
          <div class="color-picker">
            <div
              v-for="color in availableColors"
              :key="color"
              class="color-option"
              :class="{ 'is-selected': editForm.color === color }"
              :style="{ backgroundColor: color }"
              @click="editForm.color = color"
            ></div>
          </div>
        </div>
        
        <div class="dialog-actions">
          <Button
            secondary
            @click="showEditDialog = false"
          >
            取消  <!-- 原文: Cancel -->
          </Button>
          
          <Button
            type="submit"
          >
            保存  <!-- 原文: Save -->
          </Button>
        </div>
      </form>
    </Dialog>
  </div>
</template>
