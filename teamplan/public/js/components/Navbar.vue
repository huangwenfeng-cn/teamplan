<template>
  <div class="navbar">
    <div class="navbar-left">
      <div class="search-container">
        <i class="icon icon-search"></i>
        <input
          type="text"
          class="search-input"
          placeholder="搜索..."  <!-- 原文: Search... -->
          v-model="searchQuery"
          @focus="showSearchResults = true"
          @blur="hideSearchResultsDelayed"
        />
      </div>
      
      <div
        v-if="showSearchResults && searchResults.length > 0"
        class="search-results"
      >
        <div
          v-for="(result, index) in searchResults"
          :key="index"
          class="search-result-item"
          @mousedown="navigateToResult(result)"
        >
          <i class="icon" :class="getResultIcon(result.type)"></i>
          <div class="result-content">
            <div class="result-title">{{ result.title }}</div>
            <div class="result-type">{{ getResultTypeName(result.type) }}</div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="navbar-right">
      <button
        class="navbar-button"
        @click="showNotifications = !showNotifications"
      >
        <i class="icon icon-bell"></i>
        <span v-if="unreadNotificationsCount > 0" class="notification-badge">
          {{ unreadNotificationsCount }}
        </span>
      </button>
      
      <div
        v-if="showNotifications"
        class="notifications-dropdown"
      >
        <div class="dropdown-header">
          <h3>通知</h3>  <!-- 原文: Notifications -->
          <button
            v-if="hasUnreadNotifications"
            class="mark-all-read"
            @click="markAllAsRead"
          >
            全部标为已读  <!-- 原文: Mark all as read -->
          </button>
        </div>
        
        <div v-if="loading" class="loading-state">
          <p>加载�?..</p>  <!-- 原文: Loading... -->
        </div>
        
        <div v-else-if="notifications.length === 0" class="empty-state">
          <p>暂无通知</p>  <!-- 原文: No notifications -->
        </div>
        
        <div v-else class="notifications-list">
          <Notification
            v-for="(notification, index) in notifications"
            :key="index"
            :notification="notification"
            @mark-as-read="markAsRead"
          />
        </div>
        
        <div class="dropdown-footer">
          <router-link to="/notifications" class="view-all">
            查看全部  <!-- 原文: View all -->
          </router-link>
        </div>
      </div>
      
      <div class="user-menu">
        <UserAvatar
          :user="currentUser.full_name || currentUser.name"
          :image-url="currentUser.image"
          :size="32"
          @click="showUserMenu = !showUserMenu"
        />
        
        <div
          v-if="showUserMenu"
          class="user-dropdown"
        >
          <div class="user-info">
            <div class="user-name">{{ currentUser.full_name || currentUser.name }}</div>
            <div class="user-email">{{ currentUser.email }}</div>
          </div>
          
          <div class="dropdown-divider"></div>
          
          <router-link to="/profile" class="dropdown-item">
            <i class="icon icon-user"></i>
            <span>个人资料</span>  <!-- 原文: Profile -->
          </router-link>
          
          <router-link to="/settings" class="dropdown-item">
            <i class="icon icon-settings"></i>
            <span>设置</span>  <!-- 原文: Settings -->
          </router-link>
          
          <div class="dropdown-divider"></div>
          
          <button @click="logout" class="dropdown-item">
            <i class="icon icon-log-out"></i>
            <span>退出登�?/span>  <!-- 原文: Logout -->
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import UserAvatar from './UserAvatar.vue';
import Notification from './Notification.vue';

export default {
  components: {
    UserAvatar,
    Notification
  },
  setup() {
    const router = useRouter();
    const searchQuery = ref('');
    const showSearchResults = ref(false);
    const searchResults = ref([]);
    const showNotifications = ref(false);
    const showUserMenu = ref(false);
    const notifications = ref([]);
    const loading = ref(false);
    const currentUser = ref({
      name: '',
      full_name: '',
      email: '',
      image: ''
    });
    
    const unreadNotificationsCount = computed(() => {
      return notifications.value.filter(n => !n.read).length;
    });
    
    const hasUnreadNotifications = computed(() => {
      return unreadNotificationsCount.value > 0;
    });
    
    function getResultIcon(type) {
      const icons = {
        'task': 'icon-check-square',
        'discussion': 'icon-message-square',
        'project': 'icon-folder',
        'event': 'icon-calendar'
      };
      
      return icons[type] || 'icon-file';
    }
    
    function getResultTypeName(type) {
      const types = {
        'task': '任务',  // 原文: Task
        'discussion': '讨论',  // 原文: Discussion
        'project': '项目',  // 原文: Project
        'event': '事件'  // 原文: Event
      };
      
      return types[type] || type;
    }
    
    function navigateToResult(result) {
      const routes = {
        'task': { name: 'TaskDetail', params: { id: result.id } },
        'discussion': { name: 'DiscussionDetail', params: { id: result.id } },
        'project': { name: 'Project', params: { id: result.id } },
        'event': { name: 'Calendar' }
      };
      
      if (routes[result.type]) {
        router.push(routes[result.type]);
      }
      
      showSearchResults.value = false;
      searchQuery.value = '';
    }
    
    function hideSearchResultsDelayed() {
      setTimeout(() => {
        showSearchResults.value = false;
      }, 200);
    }
    
    function markAsRead(notification) {
      // 这里应该调用API标记通知为已�?
      console.log('标记通知为已�?', notification);
      
      // 更新本地状�?
      const index = notifications.value.findIndex(n => n.id === notification.id);
      if (index !== -1) {
        notifications.value[index].read = true;
      }
    }
    
    function markAllAsRead() {
      // 这里应该调用API标记所有通知为已�?
      console.log('标记所有通知为已�?);
      
      // 更新本地状�?
      notifications.value.forEach(notification => {
        notification.read = true;
      });
    }
    
    function logout() {
      // 这里应该调用API登出
      console.log('登出');
      
      // 重定向到登录页面
      router.push('/login');
    }
    
    function handleClickOutside(event) {
      if (showNotifications.value && !event.target.closest('.navbar-button') && !event.target.closest('.notifications-dropdown')) {
        showNotifications.value = false;
      }
      
      if (showUserMenu.value && !event.target.closest('.user-menu')) {
        showUserMenu.value = false;
      }
    }
    
    async function fetchNotifications() {
      loading.value = true;
      try {
        // 这里应该调用API获取通知
        // 示例数据
        notifications.value = [
          {
            id: 1,
            type: 'task',
            message: '张三分配给你一个新任务',
            read: false,
            creation: '2023-05-15T10:30:00',
            link: { name: 'TaskDetail', params: { id: 'task1' } }
          },
          {
            id: 2,
            type: 'discussion',
            message: '李四在讨论中提到了你',
            read: true,
            creation: '2023-05-14T15:45:00',
            link: { name: 'DiscussionDetail', params: { id: 'discussion1' } }
          }
        ];
      } catch (error) {
        console.error('获取通知失败:', error);
      } finally {
        loading.value = false;
      }
    }
    
    async function fetchCurrentUser() {
      try {
        // 这里应该调用API获取当前用户
        // 示例数据
        currentUser.value = {
          name: 'admin',
          full_name: '管理�?,
          email: 'admin@example.com',
          image: ''
        };
      } catch (error) {
        console.error('获取当前用户失败:', error);
      }
    }
    
    async function searchItems() {
      if (!searchQuery.value.trim()) {
        searchResults.value = [];
        return;
      }
      
      try {
        // 这里应该调用API搜索
        // 示例数据
        searchResults.value = [
          {
            id: 'task1',
            title: '完成项目文档',
            type: 'task'
          },
          {
            id: 'discussion1',
            title: '关于新功能的讨论',
            type: 'discussion'
          },
          {
            id: 'project1',
            title: '项目A',
            type: 'project'
          }
        ];
      } catch (error) {
        console.error('搜索失败:', error);
      }
    }
    
    // 监听搜索查询变化
    watch(searchQuery, () => {
      searchItems();
    });
    
    onMounted(() => {
      // 添加点击外部关闭下拉菜单的事件监�?
      document.addEventListener('click', handleClickOutside);
      
      // 获取数据
      fetchNotifications();
      fetchCurrentUser();
    });
    
    onBeforeUnmount(() => {
      // 移除事件监听
      document.removeEventListener('click', handleClickOutside);
    });
    
    return {
      searchQuery,
      showSearchResults,
      searchResults,
      showNotifications,
      showUserMenu,
      notifications,
      loading,
      currentUser,
      unreadNotificationsCount,
      hasUnreadNotifications,
      getResultIcon,
      getResultTypeName,
      navigateToResult,
      hideSearchResultsDelayed,
      markAsRead,
      markAllAsRead,
      logout
    };
  }
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 64px;
  padding: 0 1.5rem;
  background-color: white;
  border-bottom: 1px solid #e2e8f0;
}

.navbar-left {
  position: relative;
}

.search-container {
  display: flex;
  align-items: center;
  background-color: #f7fafc;
  border-radius: 0.25rem;
  padding: 0.5rem 0.75rem;
}

.search-input {
  border: none;
  background: none;
  outline: none;
  margin-left: 0.5rem;
  width: 200px;
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  width: 300px;
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.25rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  z-index: 10;
  max-height: 400px;
  overflow-y: auto;
}

.search-result-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.search-result-item:hover {
  background-color: #f7fafc;
}

.search-result-item .icon {
  margin-right: 0.75rem;
  color: #4299e1;
}

.result-content {
  flex: 1;
}

.result-title {
  font-weight: 500;
  color: #2d3748;
}

.result-type {
  font-size: 0.75rem;
  color: #718096;
}

.navbar-right {
  display: flex;
  align-items: center;
}

.navbar-button {
  position: relative;
  background: none;
  border: none;
  color: #4a5568;
  font-size: 1.25rem;
  padding: 0.5rem;
  margin-right: 1rem;
  cursor: pointer;
}

.notification-badge {
  position: absolute;
  top: 0;
  right: 0;
  background-color: #e53e3e;
  color: white;
  font-size: 0.75rem;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notifications-dropdown {
  position: absolute;
  top: 64px;
  right: 1.5rem;
  width: 350px;
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.25rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.dropdown-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.dropdown-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

.mark-all-read {
  background: none;
  border: none;
  color: #4299e1;
  font-size: 0.875rem;
  cursor: pointer;
}

.loading-state,
.empty-state {
  padding: 2rem 0;
  text-align: center;
  color: #a0aec0;
}

.notifications-list {
  max-height: 400px;
  overflow-y: auto;
}

.dropdown-footer {
  padding: 0.75rem;
  text-align: center;
  border-top: 1px solid #e2e8f0;
}

.view-all {
  color: #4299e1;
  text-decoration: none;
  font-size: 0.875rem;
}

.user-menu {
  position: relative;
}

.user-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  width: 200px;
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.25rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.user-info {
  padding: 1rem;
}

.user-name {
  font-weight: 500;
  color: #2d3748;
}

.user-email {
  font-size: 0.75rem;
  color: #718096;
}

.dropdown-divider {
  height: 1px;
  background-color: #e2e8f0;
  margin: 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  color: #4a5568;
  text-decoration: none;
  transition: background-color 0.2s;
}

.dropdown-item:hover {
  background-color: #f7fafc;
}

.dropdown-item .icon {
  margin-right: 0.75rem;
}
</style>
