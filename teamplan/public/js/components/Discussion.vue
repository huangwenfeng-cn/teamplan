<template>
  <div class="discussion">
    <div class="discussion-header">
      <div class="discussion-info">
        <h2 class="discussion-title">{{ discussion.title }}</h2>
        <div class="discussion-meta">
          <div class="author">
            <UserAvatar
              :user="discussion.author"
              :image-url="discussion.author_image"
              :size="24"
            />
            <span>{{ discussion.author }}</span>
          </div>
          <div class="date">
            {{ formatDate(discussion.created_at) }}
          </div>
        </div>
      </div>
      
      <div class="discussion-actions">
        <Button
          v-if="canEdit"
          icon="edit"
          secondary
          @click="showEditDialog = true"
        >
          编辑  <!-- 原文: Edit -->
        </Button>
      </div>
    </div>
    
    <div class="discussion-content" v-html="discussion.content"></div>
    
    <div class="discussion-tags" v-if="discussion.tags && discussion.tags.length > 0">
      <Tag
        v-for="tag in discussion.tags"
        :key="tag.text"
        :text="tag.text"
        :color="tag.color"
      />
    </div>
    
    <div class="discussion-comments">
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
    
    <Dialog
      v-model="showEditDialog"
      title="编辑讨论"  <!-- 原文: Edit Discussion -->
    >
      <form @submit.prevent="updateDiscussion">
        <div class="form-group">
          <label for="discussion-title">标题</label>  <!-- 原文: Title -->
          <input
            id="discussion-title"
            v-model="editForm.title"
            type="text"
            required
          />
        </div>
        
        <div class="form-group">
          <label for="discussion-content">内容</label>  <!-- 原文: Content -->
          <textarea
            id="discussion-content"
            v-model="editForm.content"
            rows="10"
            required
          ></textarea>
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
