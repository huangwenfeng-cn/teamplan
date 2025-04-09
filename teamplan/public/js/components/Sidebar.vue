<template>
  <div class="sidebar" :class="{ 'is-collapsed': isCollapsed }">
    <div class="sidebar-header">
      <router-link to="/" class="logo-link">
        <img
          src="/assets/teamplan/images/logo.png"
          alt="teamplan"
          class="logo"
        />
      </router-link>
      <button class="collapse-button" @click="toggleCollapse">
        <i class="icon" :class="isCollapsed ? 'icon-chevron-right' : 'icon-chevron-left'"></i>
      </button>
    </div>
    
    <div class="sidebar-content">
      <nav class="sidebar-nav">
        <router-link
          to="/"
          class="nav-item"
          exact
        >
          <i class="icon icon-home"></i>
          <span class="nav-text">首页</span>  <!-- 原文: Home -->
        </router-link>
        
        <router-link
          to="/projects"
          class="nav-item"
        >
          <i class="icon icon-folder"></i>
          <span class="nav-text">项目</span>  <!-- 原文: Projects -->
        </router-link>
        
        <router-link
          to="/tasks"
          class="nav-item"
        >
          <i class="icon icon-check-square"></i>
          <span class="nav-text">任务</span>  <!-- 原文: Tasks -->
        </router-link>
        
        <router-link
          to="/discussions"
          class="nav-item"
        >
          <i class="icon icon-message-square"></i>
          <span class="nav-text">讨论</span>  <!-- 原文: Discussions -->
        </router-link>
        
        <router-link
          to="/calendar"
          class="nav-item"
        >
          <i class="icon icon-calendar"></i>
          <span class="nav-text">日历</span>  <!-- 原文: Calendar -->
        </router-link>
      </nav>
      
      <div class="sidebar-projects">
        <div class="projects-header">
          <h3>我的项目</h3>  <!-- 原文: My Projects -->
          <router-link
            to="/projects/new"
            class="new-project-button"
            v-if="!isCollapsed"
          >
            <i class="icon icon-plus"></i>
          </router-link>
        </div>
        
        <div v-if="loading" class="loading-state">
          <p>加载�?..</p>  <!-- 原文: Loading... -->
        </div>
        
        <div v-else-if="projects.length === 0" class="empty-state">
          <p>暂无项目</p>  <!-- 原文: No projects -->
        </div>
        
        <div v-else class="projects-list">
          <router-link
            v-for="project in projects"
            :key="project.name"
            :to="{ name: 'Project', params: { id: project.name } }"
            class="project-item"
            :title="project.title"
          >
            <div class="project-color" :style="{ backgroundColor: project.color || '#4299e1' }"></div>
            <span class="project-title">{{ project.title }}</span>
          </router-link>
        </div>
      </div>
    </div>
    
    <div class="sidebar-footer">
      <div class="user-menu" @click="showUserMenu = !showUserMenu">
        <UserAvatar
          :user="currentUser.full_name || currentUser.name"
          :image-url="currentUser.image"
          :size="32"
        />
        <div v-if="!isCollapsed" class="user-info">
          <div class="user-name">{{ currentUser.full_name || currentUser.name }}</div>
          <div class="user-email">{{ currentUser.email }}</div>
        </div>
        <i v-if="!isCollapsed" class="icon icon-chevron-down"></i>
      </div>
      
      <div v-if="showUserMenu" class="user-dropdown">
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
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import UserAvatar from './UserAvatar.vue';

export default {
  components: {
    UserAvatar
  },
  setup() {
    const router = useRouter();
    const isCollapsed = ref(false);
    const showUserMenu = ref(false);
    const projects = ref([]);
    const loading = ref(true);
    const currentUser = ref({
      name: '',
      full_name: '',
      email: '',
      image: ''
    });
    
    function toggleCollapse() {
      isCollapsed.value = !isCollapsed.value;
      localStorage.setItem('sidebar_collapsed', isCollapsed.value);
    }
    
    function logout() {
      // 这里应该调用API登出
      console.log('登出');
      
      // 重定向到登录页面
      router.push('/login');
    }
    
    function handleClickOutside(event) {
      if (showUserMenu.value && !event.target.closest('.user-menu') && !event.target.closest('.user-dropdown')) {
        showUserMenu.value = false;
      }
    }
    
    async function fetchProjects() {
      loading.value = true;
      try {
        // 这里应该调用API获取项目
        // 示例数据
        projects.value = [
          {
            name: 'project1',
            title: '项目A',
            color: '#4299e1'
          },
          {
            name: 'project2',
            title: '项目B',
            color: '#48bb78'
          }
        ];
      } catch (error) {
        console.error('获取项目失败:', error);
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
    
    onMounted(() => {
      // 从本地存储中恢复侧边栏状�?
      const savedState = localStorage.getItem('sidebar_collapsed');
      if (savedState !== null) {
        isCollapsed.value = savedState === 'true';
      }
      
      // 添加点击外部关闭用户菜单的事件监�?
      document.addEventListener('click', handleClickOutside);
      
      // 获取数据
      fetchProjects();
      fetchCurrentUser();
    });
    
    onBeforeUnmount(() => {
      // 移除事件监听
      document.removeEventListener('click', handleClickOutside);
    });
    
    return {
      isCollapsed,
      showUserMenu,
      projects,
      loading,
      currentUser,
      toggleCollapse,
      logout
    };
  }
}
</script>

<style scoped>
.sidebar {
  display: flex;
  flex-direction: column;
  width: 240px;
  height: 100vh;
  background-color: #f8fafc;
  border-right: 1px solid #e2e8f0;
  transition: width 0.3s;
}

.sidebar.is-collapsed {
  width: 64px;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.logo-link {
  display: flex;
  align-items: center;
}

.logo {
  height: 32px;
}

.collapse-button {
  background: none;
  border: none;
  color: #a0aec0;
  cursor: pointer;
  padding: 0.25rem;
}

.sidebar-content {
  flex: 1;
  overflow-y: auto;
  padding: 1rem 0;
}

.sidebar-nav {
  margin-bottom: 1.5rem;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  color: #4a5568;
  text-decoration: none;
  transition: background-color 0.2s;
}

.nav-item:hover {
  background-color: #edf2f7;
}

.nav-item.router-link-active {
  background-color: #ebf8ff;
  color: #3182ce;
}

.nav-item .icon {
  margin-right: 0.75rem;
  font-size: 1.25rem;
}

.sidebar.is-collapsed .nav-text {
  display: none;
}

.sidebar-projects {
  padding: 0 1rem;
}

.projects-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.projects-header h3 {
  margin: 0;
  font-size: 0.875rem;
  font-weight: 600;
  color: #718096;
  text-transform: uppercase;
}

.new-project-button {
  color: #a0aec0;
  text-decoration: none;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 1rem 0;
  color: #a0aec0;
  font-size: 0.875rem;
}

.projects-list {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.project-item {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  border-radius: 0.25rem;
  color: #4a5568;
  text-decoration: none;
  transition: background-color 0.2s;
}

.project-item:hover {
  background-color: #edf2f7;
}

.project-item.router-link-active {
  background-color: #ebf8ff;
  color: #3182ce;
}

.project-color {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 0.5rem;
}

.sidebar.is-collapsed .project-title {
  display: none;
}

.sidebar-footer {
  position: relative;
  padding: 1rem;
  border-top: 1px solid #e2e8f0;
}

.user-menu {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.user-info {
  margin-left: 0.75rem;
  flex: 1;
}

.user-name {
  font-weight: 500;
  color: #2d3748;
}

.user-email {
  font-size: 0.75rem;
  color: #718096;
}

.user-dropdown {
  position: absolute;
  bottom: 100%;
  left: 0;
  right: 0;
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.25rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  z-index: 10;
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

.dropdown-divider {
  height: 1px;
  background-color: #e2e8f0;
  margin: 0.5rem 0;
}
</style>
