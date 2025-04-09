<template>
  <div class="task-detail-page">
    <PageHeader>
      <div class="flex items-center">
        <Button
          icon="arrow-left"
          @click="goBack"
          class="mr-4"
        >
          返回  <!-- 原文: Back -->
        </Button>
        <h1>任务详情</h1>  <!-- 原文: Task Detail -->
      </div>
      <template #actions>
        <Button
          v-if="canEdit"
          icon="edit"
          @click="showEditTaskDialog = true"
        >
          编辑  <!-- 原文: Edit -->
        </Button>
      </template>
    </PageHeader>
    
    <div v-if="loading" class="loading-state">
      <p>加载中...</p>  
    </div>
    
    <div v-else-if="!task" class="error-state">
      <p>任务未找到</p>  
      <Button @click="goToTasks">
        查看所有任务 
      </Button>
    </div>
    
    <div v-else class="task-container">
      <div class="task-header">
        <div class="task-status">
          <Button
            :class="{ 'is-completed': task.status === 'Completed' }"
            @click="toggleTaskStatus"
          >
            <i class="icon" :class="task.status === 'Completed' ? 'icon-check-circle' : 'icon-circle'"></i>
            <span>{{ task.status === 'Completed' ? '已完成' : '未完成' }}</span> 
          </Button>
        </div>
        
        <h2 class="task-title">{{ task.title }}</h2>
        
        <div class="task-meta">
          <div v-if="task.project" class="meta-item">
            <span>项目：</span> 
            <router-link :to="{ name: 'Project', params: { id: task.project_name } }">
              {{ task.project }}
            </router-link>
          </div>
          
          <div class="meta-item">
            <span>创建者：</span>  <!-- 原文: Created by: -->
            <span>{{ task.owner }}</span>
            <span>{{ formatDateTime(task.creation) }}</span>
          </div>
          
          <div class="meta-item">
            <span>分配给：</span>  <!-- 原文: Assigned to: -->
            <span v-if="task.assigned_to">
              <UserAvatar
                :user="task.assigned_to"
                :image-url="task.assigned_to_image"
                :size="20"
              />
              <span>{{ task.assigned_to }}</span>
            </span>
            <span v-else>未分配</span> 
          </div>
          
          <div v-if="task.due_date" class="meta-item">
            <span>截止日期：</span>  
            <span :class="{ 'is-overdue': isOverdue }">
              {{ formatDate(task.due_date) }}
              <span v-if="isOverdue" class="overdue-label">已逾期</span>  <!-- 原文: Overdue -->
            </span>
          </div>
        </div>
      </div>
      
      <div class="task-content">
        <div class="task-description">
          <h3>描述</h3>  <!-- 原文: Description -->
          <div v-if="task.description" class="description-content">
            {{ task.description }}
          </div>
          <div v-else class="empty-description">
            <p>无描述</p>  
          </div>
        </div>
        
        <div class="task-comments">
          <h3>评论</h3>  <!-- 原文: Comments -->
          
          <div class="comment-form">
            <textarea
              v-model="newComment"
              placeholder="添加评论..."  <!-- 原文: Add a comment... -->
              rows="3"
            ></textarea>
            <Button
              :disabled="!newComment.trim()"
              @click="addComment"
            >
              发表评论  <!-- 原文: Post Comment -->
            </Button>
          </div>
          
          <div v-if="comments.length === 0" class="empty-comments">
            <p>暂无评论</p>  <!-- 原文: No comments yet -->
          </div>
          
          <div v-else class="comments-list">
            <div
              v-for="comment in comments"
              :key="comment.name"
              class="comment"
            >
              <div class="comment-header">
                <div class="comment-author">
                  <UserAvatar
                    :user="comment.owner"
                    :image-url="comment.owner_image"
                    :size="24"
                  />
                  <span>{{ comment.owner }}</span>
                </div>
                <div class="comment-time">
                  {{ formatDateTime(comment.creation) }}
                </div>
              </div>
              <div class="comment-content">
                {{ comment.content }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 编辑任务对话框 --> 
    <Dialog
      v-if="task"
      v-model="showEditTaskDialog"
      title="编辑任务"  <!-- 原文: Edit Task -->
    >
      <div class="mb-4">
        <label for="edit-task-title" class="block mb-1">任务标题</label>  <!-- 原文: Task Title -->
        <input
          id="edit-task-title"
          v-model="editTask.title"
          class="w-full"
        />
      </div>
      <div class="mb-4">
        <label for="edit-task-description" class="block mb-1">任务描述</label>  <!-- 原文: Task Description -->
        <textarea
          id="edit-task-description"
          v-model="editTask.description"
          class="w-full"
          rows="3"
        ></textarea>
      </div>
      <div class="mb-4">
        <label for="edit-task-assigned-to" class="block mb-1">分配给</label> 
        <select
          id="edit-task-assigned-to"
          v-model="editTask.assigned_to"
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
        <label for="edit-task-due-date" class="block mb-1">截止日期</label>  <!-- 原文: Due Date -->
        <input
          id="edit-task-due-date"
          v-model="editTask.due_date"
          type="date"
          class="w-full"
        />
      </div>
      <template #actions>
        <Button secondary @click="showEditTaskDialog = false">
          取消  <!-- 原文: Cancel -->
        </Button>
        <Button
          :disabled="!editTask.title"
          @click="updateTask"
        >
          保存  <!-- 原文: Save -->
        </Button>
      </template>
    </Dialog>
  </div>
</template>