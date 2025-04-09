<template>
  <div class="discussion-card">
    <router-link
      :to="{ name: 'DiscussionDetail', params: { id: discussion.name } }"
      class="discussion-link"
    >
      <div class="discussion-header">
        <h3 class="discussion-title">{{ discussion.title }}</h3>
      </div>
      
      <div class="discussion-preview">
        <p>{{ discussionPreview }}</p>
      </div>
      
      <div class="discussion-meta">
        <div class="meta-item author">
          <UserAvatar
            :user="discussion.owner"
            :image-url="discussion.owner_image"
            :size="20"
          />
          <span>{{ discussion.owner }}</span>
        </div>
        
        <div class="meta-item date">
          <i class="icon icon-clock"></i>
          <span>{{ formatDate(discussion.creation) }}</span>
        </div>
        
        <div v-if="discussion.project" class="meta-item project">
          <i class="icon icon-folder"></i>
          <span>{{ discussion.project }}</span>
        </div>
        
        <div class="meta-item comments">
          <i class="icon icon-message-circle"></i>
          <span>{{ discussion.comment_count || 0 }} 评论</span>  <!-- 原文: comments -->
        </div>
      </div>
    </router-link>
  </div>
</template>

<script>
import { computed } from 'vue';
import { formatDate } from '../utils/date';
import UserAvatar from './UserAvatar.vue';

export default {
  components: {
    UserAvatar
  },
  props: {
    discussion: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const discussionPreview = computed(() => {
      if (!props.discussion.content) return '';
      
      // 截取内容的前100个字符作为预�?
      const preview = props.discussion.content.substring(0, 100);
      return preview.length < props.discussion.content.length
        ? `${preview}...`
        : preview;
    });
    
    return {
      discussionPreview,
      formatDate
    };
  }
}
</script>

<style scoped>
.discussion-card {
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  overflow: hidden;
  transition: box-shadow 0.2s, transform 0.2s;
}

.discussion-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.discussion-link {
  display: block;
  padding: 1.25rem;
  color: inherit;
  text-decoration: none;
}

.discussion-header {
  margin-bottom: 0.75rem;
}

.discussion-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #2d3748;
  margin: 0;
}

.discussion-preview {
  margin-bottom: 1rem;
  color: #4a5568;
  font-size: 0.875rem;
  line-height: 1.5;
}

.discussion-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  font-size: 0.75rem;
  color: #718096;
}

.meta-item {
  display: flex;
  align-items: center;
}

.meta-item .icon {
  margin-right: 0.25rem;
}

.meta-item.author {
  display: flex;
  align-items: center;
}

.meta-item.author span {
  margin-left: 0.25rem;
}
</style>
