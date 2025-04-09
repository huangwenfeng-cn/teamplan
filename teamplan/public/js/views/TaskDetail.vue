<template>
  <div class="task-detail">
    <div v-if="loading" class="loading-state">
      <p>加载�?..</p>  <!-- 原文: Loading... -->
    </div>
    
    <div v-else-if="!task" class="error-state">
      <p>任务未找�?/p>  <!-- 原文: Task not found -->
    </div>
    
    <div v-else class="task-content">
      <div class="task-header">
        <div class="task-status">
          <input
            type="checkbox"
            :checked="task.status === 'Completed'"
            @change="toggleTaskStatus"
          />
          <span class="status-text">{{ task.status === 'Completed' ? '已完�? : '进行�? }}</span>  <!-- 原文: Completed / In Progress -->
        </div>
        
        <div class="task-actions">
          <Button
            icon="edit"
            secondary
            @click="showEditDialog = true"
          >
            编辑  <!-- 原文: Edit -->
          </Button>
          
          <Button
            icon="trash"
            secondary
            @click="confirmDelete"
          >
            删除  <!-- 原文: Delete -->
          </Button>
        </div>
      </div>
      
      <h1 class="task-title">{{ task.subject }}</h1>
      
      <div class="task-meta">
        <div class="meta-item">
          <div class="meta-label">项目</div>  <!-- 原文: Project -->
          <div class="meta-value">
            <router-link
              v-if="task.project"
              :to="{ name: 'Project', params: { id: task.project_name } }"
            >
              {{ task.project }}
            </router-link>
            <span v-else>�?/span>  <!-- 原文: None -->
          </div>
        </div>
        
        <div class="meta-item">
          <div class="meta-label">指派�?/div>  <!-- 原文: Assigned To -->
          <div class="meta-value">
            <div v-if="task.assigned_to" class="user-info">
              <UserAvatar
                :user="task.assigned_to"
                :image-url="task.assigned_to_image"
                :size="24"
              />
              <span>{{ task.assigned_to }}</span>
            </div>
            <span v-else>未指�?/span>  <!-- 原文: Unassigned -->
          </div>
        </div>
        
        <div class="meta-item">
          <div class="meta-label">截止日期</div>  <!-- 原文: Due Date -->
          <div class="meta-value">
            <span v-if="task.due_date">{{ formatDate(task.due_date) }}</span>
            <span v-else>无截止日�?/span>  <!-- 原文: No due date -->
          </div>
        </div>
        
        <div class="meta-item">
          <div class="meta-label">标签</div>  <!-- 原文: Tags -->
          <div class="meta-value">
            <div v-if="task.tags && task.tags.length > 0" class="tags-list">
              <Tag
                v-for="tag in task.tags"
                :key="tag.text"
                :text="tag.text"
                :color="tag.color"
              />
            </div>
            <span v-else>无标�?/span>  <!-- 原文: No tags -->
          </div>
        </div>
      </div>
      
      <div v-if="task.description" class="task-description">
        <h3>描述</h3>  <!-- 原文: Description -->
        <div v-html="task.description"></div>
      </div>
      
      <div class="task-comments">
        <h3>评论 ({{ comments.length }})</h3>  <!-- 原文: Comments -->
        
        <div class="comment-form">
          <UserAvatar
            :user="currentUser.full_name || currentUser.name"
            :image-url="currentUser.image"
            :size="40"
          />
          <div class="comment-input-container">
            <textarea
              v-model="newComment"
              class="comment-input"
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
        </div>
        
        <div v-if="comments.length === 0" class="no-comments">
          <p>暂无评论</p>  <!-- 原文: No comments yet -->
        </div>
        
        <div v-else class="comments-list">
          <Comment
            v-for="comment in comments"
            :key="comment.name"
            :comment="comment"
            :current-user="currentUser.name"
            @update="updateComment"
            @delete="deleteComment"
            @reply="replyToComment"
          />
        </div>
      </div>
    </div>
    
    <Dialog
      v-model="showEditDialog"
      title="编辑任务"  <!-- 原文: Edit Task -->
    >
      <form @submit.prevent="updateTask">
        <div class="form-group">
          <label for="task-subject">标题</label>  <!-- 原文: Subject -->
          <input
            id="task-subject"
            v-model="editForm.subject"
            type="text"
            required
          />
        </div>
        
        <div class="form-group">
          <label for="task-description">描述</label>  <!-- 原文: Description -->
          <textarea
            id="task-description"
            v-model="editForm.description"
            rows="4"
          ></textarea>
        </div>
        
        <div class="form-group">
          <label for="task-status">状�?/label>  <!-- 原文: Status -->
          <select id="task-status" v-model="editForm.status">
            <option value="Open">进行�?/option>  <!-- 原文: Open -->
            <option value="Completed">已完�?/option>  <!-- 原文: Completed -->
          </select>
        </div>
        
        <div class="form-group">
          <label for="task-assigned-to">指派�?/label>  <!-- 原文: Assigned To -->
          <select id="task-assigned-to" v-model="editForm.assigned_to">
            <option value="">未指�?/option>  <!-- 原文: Unassigned -->
            <option
              v-for="member in projectMembers"
              :key="member.name"
              :value="member.name"
            >
              {{ member.full_name || member.name }}
            </option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="task-due-date">截止日期</label>  <!-- 原文: Due Date -->
          <DatePicker
            id="task-due-date"
            v-model="editForm.due_date"
            clearable
          />
        </div>
        
        <div class="form-group">
          <label>标签</label>  <!-- 原文: Tags -->
          <TagSelector
            v-model="editForm.tags"
            :suggestions="tagSuggestions"
          />
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
