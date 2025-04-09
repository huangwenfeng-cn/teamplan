<template>
  <div class="discussion-detail-page">
    <PageHeader>
      <div class="flex items-center">
        <Button
          icon="arrow-left"
          @click="goBack"
          class="mr-4"
        >
          返回  <!-- 原文: Back -->
        </Button>
        <h1>讨论详情</h1>  <!-- 原文: Discussion Detail -->
      </div>
      <template #actions>
        <Button
          v-if="canEdit"
          icon="edit"
          @click="showEditDiscussionDialog = true"
        >
          编辑  <!-- 原文: Edit -->
        </Button>
      </template>
    </PageHeader>
    
    <div v-if="loading" class="loading-state">
      <p>加载中...</p>  <!-- 原文: Load... -->
    </div>
    
    <div v-else-if="!discussion" class="error-state">
      <p>讨论未找到</p>  
      <Button @click="goToDiscussions">
        查看所有讨论 
      </Button>
    </div>
    
    <div v-else class="discussion-container">
      <div class="discussion-header">
        <h2 class="discussion-title">{{ discussion.title }}</h2>
        
        <div class="discussion-meta">
          <div class="meta-item">
            <span>创建者：</span>  <!-- 原文: Created by: -->
            <UserAvatar
              :user="discussion.owner"
              :image-url="discussion.owner_image"
              :size="20"
            />
            <span>{{ discussion.owner }}</span>
            <span>{{ formatDateTime(discussion.creation) }}</span>
          </div>
          
          <div v-if="discussion.project" class="meta-item">
            <span>项目：</span>  
            <router-link :to="{ name: 'Project', params: { id: discussion.project_name } }">
              {{ discussion.project }}
            </router-link>
          </div>
        </div>
      </div>
      
      <div class="discussion-content">
        <div class="content-body">
          {{ discussion.content }}
        </div>
      </div>
      
      <div class="discussion-comments">
        <h3>评论 ({{ comments.length }})</h3>  <!-- 原文: Comments -->
        
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
    
    <!-- 编辑讨论对话框 --> 
    <Dialog
      v-if="discussion"
      v-model="showEditDiscussionDialog"
      title="编辑讨论"  <!-- 原文: Edit Discussion -->
    >
      <div class="mb-4">
        <label for="edit-discussion-title" class="block mb-1">讨论标题</label>  <!-- 原文: Discussion Title -->
        <input
          id="edit-discussion-title"
          v-model="editDiscussion.title"
          class="w-full"
        />
      </div>
      <div class="mb-4">
        <label for="edit-discussion-content" class="block mb-1">讨论内容</label>  <!-- 原文: Discussion Content -->
        <textarea
          id="edit-discussion-content"
          v-model="editDiscussion.content"
          class="w-full"
          rows="5"
        ></textarea>
      </div>
      <template #actions>
        <Button secondary @click="showEditDiscussionDialog = false">
          取消  <!-- 原文: Cancel -->
        </Button>
        <Button
          :disabled="!editDiscussion.title || !editDiscussion.content"
          @click="updateDiscussion"
        >
          保存  <!-- 原文: Save -->
        </Button>
      </template>
    </Dialog>
  </div>
</template>