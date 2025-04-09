<template>
  <div v-if="task" class="task-page">
    <PageHeader>
      <div class="task-header">
        <div class="task-status">
          <span
            class="status-badge"
            :class="{ completed: task.status === 'Completed' }"
          >
            {{ task.status === 'Completed' ? '已完成' : '未完成' }}  
          </span>
        </div>
        <h1>{{ task.title }}</h1>
      </div>
      <template #actions>
        <Button
          v-if="task.status === 'Open'"
          @click="completeTask"
        >
          完成任务  <!-- 原文: Complete Task -->
        </Button>
        <Button
          v-else
          @click="reopenTask"
        >
          重新打开任务  <!-- 原文: Reopen Task -->
        </Button>
        <Button
          icon="edit"
          @click="showEditTaskDialog = true"
        >
          编辑任务  <!-- 原文: Edit Task -->
        </Button>
      </template>
    </PageHeader>
    
    <div class="task-details">
      <div class="task-meta">
        <div class="meta-item">
          <span class="meta-label">项目：</span> 
          <router-link
            :to="{ name: 'Project', params: { id: task.project_id } }"
          >
            {{ task.project }}
          </router-link>
        </div>
        
        <div class="meta-item">
          <span class="meta-label">创建者：</span>  <!-- 原文: Created by: -->
          <span>{{ task.owner }}</span>
          <span class="meta-date">{{ formatDateTime(task.creation) }}</span>
        </div>
        
        <div class="meta-item">
          <span class="meta-label">分配给：</span>  <!-- 原文: Assigned to: -->
          <span v-if="task.assigned_to">
            <UserAvatar
              :user="task.assigned_to"
              :image-url="task.assigned_to_image"
              :size="20"
            />
            {{ task.assigned_to }}
          </span>
          <span v-else class="text-muted">未分配</span> 
          <Button
            small
            @click="showAssignDialog = true"
          >
            更改  <!-- 原文: Change -->
          </Button>
        </div>
        
        <div class="meta-item">
          <span class="meta-label">截止日期：</span>  
          <span v-if="task.due_date">{{ formatDate(task.due_date) }}</span>
          <span v-else class="text-muted">无截止日期</span> 
          <Button
            small
            @click="showDueDateDialog = true"
          >
            更改  <!-- 原文: Change -->
          </Button>
        </div>
      </div>
      
      <div class="task-description">
        <h3>任务描述</h3>  <!-- 原文: Task Description -->
        <div v-if="task.description" class="description-content">
          {{ task.description }}
        </div>
        <div v-else class="text-muted">
          无描述 
        </div>
      </div>
      
      <div class="task-comments">
        <h3>评论</h3>  <!-- 原文: Comments -->
        <div v-if="comments.length === 0" class="empty-state">
          <p>暂无评论</p>  <!-- 原文: No comments yet -->
        </div>
        <div v-else class="comment-list">
          <Comment
            v-for="comment in comments"
            :key="comment.id"
            :comment="comment"
            @update="fetchComments"
            @delete="fetchComments"
          />
        </div>
        
        <div class="new-comment">
          <h4>添加评论</h4>  <!-- 原文: Add Comment -->
          <textarea
            v-model="newComment"
            class="w-full"
            placeholder="输入您的评论..."  <!-- 原文: Type your comment... -->
            rows="3"
          ></textarea>
          <Button
            :disabled="!newComment"
            @click="addComment"
          >
            提交评论  <!-- 原文: Submit Comment -->
          </Button>
        </div>
      </div>
    </div>
    
    <!-- 编辑任务对话框 --> 
    <Dialog
      v-model="showEditTaskDialog"
      title="编辑任务"  <!-- 原文: Edit Task -->
    >
      <div class="mb-4">
        <label for="edit-task-title" class="block mb-1">任务标题</label>  <!-- 原文: Task Title -->
        <input
          id="edit-task-title"
          v-model="editedTask.title"
          class="w-full"
        />
      </div>
      <div class="mb-4">
        <label for="edit-task-description" class="block mb-1">任务描述</label>  <!-- 原文: Task Description -->
        <textarea
          id="edit-task-description"
          v-model="editedTask.description"
          class="w-full"
          rows="3"
        ></textarea>
      </div>
      <div class="danger-zone">
        <h4>危险区域</h4>  <!-- 原文: Danger Zone -->
        <Button
          class="delete-button"
          @click="confirmDeleteTask"
        >
          删除任务  <!-- 原文: Delete Task -->
        </Button>
      </div>
      <template #actions>
        <Button secondary @click="showEditTaskDialog = false">
          取消  <!-- 原文: Cancel -->
        </Button>
        <Button @click="saveTaskEdits">
          保存  <!-- 原文: Save -->
        </Button>
      </template>
    </Dialog>
    
    <!-- 分配任务对话框 --> 
    <Dialog
      v-model="showAssignDialog"
      title="分配任务"  <!-- 原文: Assign Task -->
    >
      <div class="mb-4">
        <label for="assign-to" class="block mb-1">分配给</label> 
        <select
          id="assign-to"
          v-model="assignTo"
          class="w-full"
        >
          <option value="">未分配</option> 
          <option
            v-for="member in projectMembers"
            :key="member.user"
            :value="member.user"
          >
            {{ member.user }}
          </option>
        </select>
      </div>
      <template #actions>
        <Button secondary @click="showAssignDialog = false">
          取消  <!-- 原文: Cancel -->
        </Button>
        <Button @click="assignTask">
          分配  <!-- 原文: Assign -->
        </Button>
      </template>
    </Dialog>
    
    <!-- 设置截止日期对话框 --> 
    <Dialog
      v-model="showDueDateDialog"
      title="设置截止日期"  <!-- 原文: Set Due Date -->
    >
      <div class="mb-4">
        <label for="due-date" class="block mb-1">截止日期</label>  <!-- 原文: Due Date -->
        <input
          id="due-date"
          v-model="dueDate"
          type="date"
          class="w-full"
        />
      </div>
      <template #actions>
        <Button
          v-if="task.due_date"
          class="delete-button"
          @click="clearDueDate"
        >
          清除截止日期  <!-- 原文: Clear Due Date -->
        </Button>
        <Button secondary @click="showDueDateDialog = false">
          取消  <!-- 原文: Cancel -->
        </Button>
        <Button @click="setDueDate">
          保存  <!-- 原文: Save -->
        </Button>
      </template>
    </Dialog>
  </div>
  <div v-else class="loading-state">
    <p>加载中...</p>  
  </div>
</template>