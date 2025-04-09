<template>
  <div class="comment" :id="`comment-${comment.name}`">
    <div class="comment-avatar">
      <UserAvatar
        :user="comment.owner"
        :image-url="comment.owner_image"
        :size="40"
      />
    </div>
    
    <div class="comment-content">
      <div class="comment-header">
        <div class="comment-author">{{ comment.owner }}</div>
        <div class="comment-time">{{ formatDateTime(comment.creation) }}</div>
      </div>
      
      <div class="comment-body" v-html="comment.content"></div>
      
      <div class="comment-actions">
        <button
          v-if="canReply"
          class="action-button"
          @click="$emit('reply', comment)"
        >
          <i class="icon icon-corner-up-left"></i>
          <span>回复</span>  <!-- 原文: Reply -->
        </button>
        
        <button
          v-if="canEdit"
          class="action-button"
          @click="startEditing"
        >
          <i class="icon icon-edit"></i>
          <span>编辑</span>  <!-- 原文: Edit -->
        </button>
        
        <button
          v-if="canDelete"
          class="action-button text-red-500"
          @click="confirmDelete"
        >
          <i class="icon icon-trash"></i>
          <span>删除</span>  <!-- 原文: Delete -->
        </button>
      </div>
      
      <div v-if="isEditing" class="comment-edit-form">
        <textarea
          v-model="editContent"
          class="edit-textarea"
          rows="4"
        ></textarea>
        
        <div class="edit-actions">
          <button
            class="cancel-button"
            @click="cancelEditing"
          >
            取消  <!-- 原文: Cancel -->
          </button>
          
          <button
            class="save-button"
            @click="saveEdit"
          >
            保存  <!-- 原文: Save -->
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { formatDateTime } from '../utils/date';
import UserAvatar from './UserAvatar.vue';

export default {
  components: {
    UserAvatar
  },
  props: {
    comment: {
      type: Object,
      required: true
    },
    currentUser: {
      type: String,
      default: ''
    }
  },
  emits: ['update', 'delete', 'reply'],
  setup(props, { emit }) {
    const isEditing = ref(false);
    const editContent = ref('');
    
    const canEdit = computed(() => {
      return props.currentUser === props.comment.owner;
    });
    
    const canDelete = computed(() => {
      return props.currentUser === props.comment.owner;
    });
    
    const canReply = computed(() => {
      return true; // 所有用户都可以回复
    });
    
    function startEditing() {
      editContent.value = props.comment.content;
      isEditing.value = true;
    }
    
    function cancelEditing() {
      isEditing.value = false;
      editContent.value = '';
    }
    
    async function saveEdit() {
      if (!editContent.value.trim()) {
        return;
      }
      
      try {
        // 这里应该调用API更新评论
        console.log('更新评论:', props.comment.name, editContent.value);
        
        // 通知父组件更�?
        emit('update', {
          name: props.comment.name,
          content: editContent.value
        });
        
        isEditing.value = false;
      } catch (error) {
        console.error('更新评论失败:', error);
      }
    }
    
    function confirmDelete() {
      if (confirm('您确定要删除此评论吗�?)) {
        // 这里应该调用API删除评论
        console.log('删除评论:', props.comment.name);
        
        // 通知父组件删�?
        emit('delete', props.comment.name);
      }
    }
    
    return {
      isEditing,
      editContent,
      canEdit,
      canDelete,
      canReply,
      startEditing,
      cancelEditing,
      saveEdit,
      confirmDelete,
      formatDateTime
    };
  }
}
</script>

<style scoped>
.comment {
  display: flex;
  margin-bottom: 1.5rem;
}

.comment-avatar {
  margin-right: 1rem;
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}

.comment-author {
  font-weight: 500;
  color: #2d3748;
  margin-right: 0.5rem;
}

.comment-time {
  font-size: 0.75rem;
  color: #a0aec0;
}

.comment-body {
  margin-bottom: 0.75rem;
  line-height: 1.5;
}

.comment-actions {
  display: flex;
  gap: 1rem;
}

.action-button {
  display: flex;
  align-items: center;
  background: none;
  border: none;
  color: #718096;
  font-size: 0.875rem;
  cursor: pointer;
  padding: 0;
}

.action-button:hover {
  color: #4299e1;
}

.action-button .icon {
  margin-right: 0.25rem;
}

.text-red-500:hover {
  color: #e53e3e;
}

.comment-edit-form {
  margin-top: 1rem;
}

.edit-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.25rem;
  resize: vertical;
  margin-bottom: 0.75rem;
}

.edit-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

.cancel-button,
.save-button {
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
  cursor: pointer;
}

.cancel-button {
  background-color: #e2e8f0;
  color: #4a5568;
  border: none;
}

.save-button {
  background-color: #4299e1;
  color: white;
  border: none;
}
</style>
