<template>
  <div class="search-component">
    <div class="search-input-container">
      <i class="icon icon-search search-icon"></i>
      <input
        type="text"
        class="search-input"
        :placeholder="placeholder"
        v-model="searchQuery"
        @focus="showResults = true"
        @blur="hideResultsDelayed"
        @keydown.esc="clearSearch"
        @keydown.enter="search"
        @keydown.down="navigateResults(1)"
        @keydown.up="navigateResults(-1)"
      />
      <button
        v-if="searchQuery"
        class="clear-button"
        @click.stop="clearSearch"
      >
        <i class="icon icon-x"></i>
      </button>
    </div>
    
    <div
      v-if="showResults && (isLoading || results.length > 0 || recentSearches.length > 0)"
      class="search-results"
    >
      <div v-if="isLoading" class="search-loading">
        <p>搜索�?..</p>  <!-- 原文: Searching... -->
      </div>
      
      <div v-else-if="results.length > 0" class="results-list">
        <div class="results-section">
          <div class="section-title">搜索结果</div>  <!-- 原文: Search Results -->
          
          <div
            v-for="(result, index) in results"
            :key="result.id"
            class="result-item"
            :class="{ 'is-active': activeResultIndex === index }"
            @mousedown="selectResult(result)"
            @mouseover="activeResultIndex = index"
          >
            <div class="result-icon">
              <i :class="getResultIcon(result.type)"></i>
            </div>
            
            <div class="result-content">
              <div class="result-title">{{ result.title }}</div>
              <div class="result-subtitle">{{ getResultSubtitle(result) }}</div>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else-if="searchQuery && results.length === 0" class="no-results">
        <p>未找到结�?/p>  <!-- 原文: No results found -->
      </div>
      
      <div v-else-if="recentSearches.length > 0" class="recent-searches">
        <div class="section-title">最近搜�?/div>  <!-- 原文: Recent Searches -->
        
        <div
          v-for="(search, index) in recentSearches"
          :key="index"
          class="recent-item"
          @mousedown="applyRecentSearch(search)"
        >
          <div class="recent-icon">
            <i class="icon icon-clock"></i>
          </div>
          
          <div class="recent-query">{{ search }}</div>
          
          <button
            class="remove-button"
            @mousedown.stop="removeRecentSearch(index)"
          >
            <i class="icon icon-x"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';

export default {
  props: {
    placeholder: {
      type: String,
      default: '搜索...'  // 原文: Search...
    },
    debounce: {
      type: Number,
      default: 300
    }
  },
  setup(props) {
    const router = useRouter();
    
    const searchQuery = ref('');
    const results = ref([]);
    const isLoading = ref(false);
    const showResults = ref(false);
    const activeResultIndex = ref(-1);
    const recentSearches = ref([]);
    
    let searchTimeout = null;
    
    // 监听搜索查询变化
    watch(searchQuery, (newQuery) => {
      activeResultIndex.value = -1;
      
      if (!newQuery) {
        results.value = [];
        isLoading.value = false;
        return;
      }
      
      // 防抖处理
      clearTimeout(searchTimeout);
      isLoading.value = true;
      
      searchTimeout = setTimeout(() => {
        performSearch(newQuery);
      }, props.debounce);
    });
    
    // 执行搜索
    async function performSearch(query) {
      try {
        // 这里应该调用API执行搜索
        // 示例数据
        results.value = [
          {
            id: 1,
            type: 'task',
            title: '实现搜索功能',  // 原文: Implement search functionality
            project: '网站重构',  // 原文: Website Redesign
            url: '/tasks/1'
          },
          {
            id: 2,
            type: 'project',
            title: '网站重构',  // 原文: Website Redesign
            description: '公司网站的重新设计和开�?,  // 原文: Redesign and development of company website
            url: '/projects/1'
          },
          {
            id: 3,
            type: 'discussion',
            title: '关于新功能的讨论',  // 原文: Discussion about new features
            project: '产品开�?,  // 原文: Product Development
            url: '/discussions/1'
          }
        ];
      } catch (error) {
        console.error('搜索失败:', error);
        results.value = [];
      } finally {
        isLoading.value = false;
      }
    }
    
    // 清除搜索
    function clearSearch() {
      searchQuery.value = '';
      results.value = [];
      showResults.value = false;
    }
    
    // 执行搜索
    function search() {
      if (!searchQuery.value) return;
      
      // 添加到最近搜�?
      addToRecentSearches(searchQuery.value);
      
      // 这里可以实现导航到搜索结果页�?
      router.push({
        name: 'SearchResults',
        query: { q: searchQuery.value }
      });
      
      showResults.value = false;
    }
    
    // 选择结果
    function selectResult(result) {
      // 添加到最近搜�?
      addToRecentSearches(searchQuery.value);
      
      // 导航到结果URL
      if (result.url) {
        router.push(result.url);
      }
      
      showResults.value = false;
    }
    
    // 导航结果
    function navigateResults(direction) {
      if (results.value.length === 0) return;
      
      if (direction > 0) {
        // 向下导航
        activeResultIndex.value = (activeResultIndex.value + 1) % results.value.length;
      } else {
        // 向上导航
        activeResultIndex.value = activeResultIndex.value <= 0 ? results.value.length - 1 : activeResultIndex.value - 1;
      }
    }
    
    // 延迟隐藏结果
    function hideResultsDelayed() {
      setTimeout(() => {
        showResults.value = false;
      }, 200);
    }
    
    // 获取结果图标
    function getResultIcon(type) {
      const icons = {
        task: 'icon icon-check-square',
        project: 'icon icon-folder',
        discussion: 'icon icon-message-circle',
        file: 'icon icon-file',
        user: 'icon icon-user'
      };
      
      return icons[type] || 'icon icon-search';
    }
    
    // 获取结果副标�?
    function getResultSubtitle(result) {
      if (result.type === 'task' || result.type === 'discussion') {
        return `�?${result.project} 中`;  // 原文: In ${result.project}
      } else if (result.type === 'project') {
        return result.description || '项目';  // 原文: Project
      } else if (result.type === 'file') {
        return `�?${result.project} 中的文件`;  // 原文: File in ${result.project}
      } else if (result.type === 'user') {
        return result.email || '用户';  // 原文: User
      }
      
      return '';
    }
    
    // 添加到最近搜�?
    function addToRecentSearches(query) {
      if (!query) return;
      
      // 移除已存在的相同查询
      const index = recentSearches.value.indexOf(query);
      if (index !== -1) {
        recentSearches.value.splice(index, 1);
      }
      
      // 添加到最前面
      recentSearches.value.unshift(query);
      
      // 限制最近搜索数�?
      if (recentSearches.value.length > 5) {
        recentSearches.value = recentSearches.value.slice(0, 5);
      }
      
      // 保存到本地存�?
      localStorage.setItem('recentSearches', JSON.stringify(recentSearches.value));
    }
    
    // 应用最近搜�?
    function applyRecentSearch(query) {
      searchQuery.value = query;
      search();
    }
    
    // 移除最近搜�?
    function removeRecentSearch(index) {
      recentSearches.value.splice(index, 1);
      localStorage.setItem('recentSearches', JSON.stringify(recentSearches.value));
    }
    
    // 初始化时从本地存储加载最近搜�?
    onMounted(() => {
      try {
        const savedSearches = localStorage.getItem('recentSearches');
        if (savedSearches) {
          recentSearches.value = JSON.parse(savedSearches);
        }
      } catch (error) {
        console.error('加载最近搜索失�?', error);
      }
    });
    
    return {
      searchQuery,
      results,
      isLoading,
      showResults,
      activeResultIndex,
      recentSearches,
      clearSearch,
      search,
      selectResult,
      navigateResults,
      hideResultsDelayed,
      getResultIcon,
      getResultSubtitle,
      applyRecentSearch,
      removeRecentSearch
    };
  }
}
</script>

<style scoped>
.search-component {
  position: relative;
  width: 100%;
}

.search-input-container {
  display: flex;
  align-items: center;
  border: 1px solid #e2e8f0;
  border-radius: 0.25rem;
  padding: 0.5rem;
  background-color: white;
}

.search-icon {
  color: #a0aec0;
  margin-right: 0.5rem;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 0.875rem;
}

.clear-button {
  background: none;
  border: none;
  color: #a0aec0;
  cursor: pointer;
  padding: 0.25rem;
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.25rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-top: 0.25rem;
  z-index: 10;
  max-height: 400px;
  overflow-y: auto;
}

.search-loading,
.no-results {
  padding: 1rem;
  text-align: center;
  color: #a0aec0;
}

.section-title {
  padding: 0.5rem 1rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: #718096;
  background-color: #f7fafc;
  border-bottom: 1px solid #e2e8f0;
}

.result-item,
.recent-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.result-item:hover,
.recent-item:hover,
.result-item.is-active {
  background-color: #f7fafc;
}

.result-icon,
.recent-icon {
  margin-right: 0.75rem;
  color: #4a5568;
}

.result-content {
  flex: 1;
}

.result-title {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.result-subtitle {
  font-size: 0.75rem;
  color: #718096;
}

.recent-query {
  flex: 1;
}

.remove-button {
  background: none;
  border: none;
  color: #a0aec0;
  cursor: pointer;
  padding: 0.25rem;
  visibility: hidden;
}

.recent-item:hover .remove-button {
  visibility: visible;
}
</style>
