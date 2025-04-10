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
        <p>æç´¢ä¸?..</p>  <!-- åæ: Searching... -->
      </div>
      
      <div v-else-if="results.length > 0" class="results-list">
        <div class="results-section">
          <div class="section-title">æç´¢ç»æ</div>  <!-- åæ: Search Results -->
          
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
        <p>æªæ¾å°ç»æ?/p>  <!-- åæ: No results found -->
      </div>
      
      <div v-else-if="recentSearches.length > 0" class="recent-searches">
        <div class="section-title">æè¿æç´?/div>  <!-- åæ: Recent Searches -->
        
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
      default: 'æç´¢...'  // åæ: Search...
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
    
    // çå¬æç´¢æ¥è¯¢åå
    watch(searchQuery, (newQuery) => {
      activeResultIndex.value = -1;
      
      if (!newQuery) {
        results.value = [];
        isLoading.value = false;
        return;
      }
      
      // é²æå¤ç
      clearTimeout(searchTimeout);
      isLoading.value = true;
      
      searchTimeout = setTimeout(() => {
        performSearch(newQuery);
      }, props.debounce);
    });
    
    // æ§è¡æç´¢
    async function performSearch(query) {
      try {
        // è¿éåºè¯¥è°ç¨APIæ§è¡æç´¢
        // ç¤ºä¾æ°æ®
        results.value = [
          {
            id: 1,
            type: 'task',
            title: 'å®ç°æç´¢åè½',  // åæ: Implement search functionality
            project: 'ç½ç«éæ',  // åæ: Website Redesign
            url: '/tasks/1'
          },
          {
            id: 2,
            type: 'project',
            title: 'ç½ç«éæ',  // åæ: Website Redesign
            description: 'å¬å¸ç½ç«çéæ°è®¾è®¡åå¼å?,  // åæ: Redesign and development of company website
            url: '/projects/1'
          },
          {
            id: 3,
            type: 'discussion',
            title: 'å³äºæ°åè½çè®¨è®º',  // åæ: Discussion about new features
            project: 'äº§åå¼å?,  // åæ: Product Development
            url: '/discussions/1'
          }
        ];
      } catch (error) {
        console.error('æç´¢å¤±è´¥:', error);
        results.value = [];
      } finally {
        isLoading.value = false;
      }
    }
    
    // æ¸é¤æç´¢
    function clearSearch() {
      searchQuery.value = '';
      results.value = [];
      showResults.value = false;
    }
    
    // æ§è¡æç´¢
    function search() {
      if (!searchQuery.value) return;
      
      // æ·»å å°æè¿æç´?
      addToRecentSearches(searchQuery.value);
      
      // è¿éå¯ä»¥å®ç°å¯¼èªå°æç´¢ç»æé¡µé?
      router.push({
        name: 'SearchResults',
        query: { q: searchQuery.value }
      });
      
      showResults.value = false;
    }
    
    // éæ©ç»æ
    function selectResult(result) {
      // æ·»å å°æè¿æç´?
      addToRecentSearches(searchQuery.value);
      
      // å¯¼èªå°ç»æURL
      if (result.url) {
        router.push(result.url);
      }
      
      showResults.value = false;
    }
    
    // å¯¼èªç»æ
    function navigateResults(direction) {
      if (results.value.length === 0) return;
      
      if (direction > 0) {
        // åä¸å¯¼èª
        activeResultIndex.value = (activeResultIndex.value + 1) % results.value.length;
      } else {
        // åä¸å¯¼èª
        activeResultIndex.value = activeResultIndex.value <= 0 ? results.value.length - 1 : activeResultIndex.value - 1;
      }
    }
    
    // å»¶è¿éèç»æ
    function hideResultsDelayed() {
      setTimeout(() => {
        showResults.value = false;
      }, 200);
    }
    
    // è·åç»æå¾æ 
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
    
    // è·åç»æå¯æ é¢?
    function getResultSubtitle(result) {
      if (result.type === 'task' || result.type === 'discussion') {
        return `å?${result.project} ä¸­`;  // åæ: In ${result.project}
      } else if (result.type === 'project') {
        return result.description || 'é¡¹ç®';  // åæ: Project
      } else if (result.type === 'file') {
        return `å?${result.project} ä¸­çæä»¶`;  // åæ: File in ${result.project}
      } else if (result.type === 'user') {
        return result.email || 'ç¨æ·';  // åæ: User
      }
      
      return '';
    }
    
    // æ·»å å°æè¿æç´?
    function addToRecentSearches(query) {
      if (!query) return;
      
      // ç§»é¤å·²å­å¨çç¸åæ¥è¯¢
      const index = recentSearches.value.indexOf(query);
      if (index !== -1) {
        recentSearches.value.splice(index, 1);
      }
      
      // æ·»å å°æåé¢
      recentSearches.value.unshift(query);
      
      // éå¶æè¿æç´¢æ°é?
      if (recentSearches.value.length > 5) {
        recentSearches.value = recentSearches.value.slice(0, 5);
      }
      
      // ä¿å­å°æ¬å°å­å?
      localStorage.setItem('recentSearches', JSON.stringify(recentSearches.value));
    }
    
    // åºç¨æè¿æç´?
    function applyRecentSearch(query) {
      searchQuery.value = query;
      search();
    }
    
    // ç§»é¤æè¿æç´?
    function removeRecentSearch(index) {
      recentSearches.value.splice(index, 1);
      localStorage.setItem('recentSearches', JSON.stringify(recentSearches.value));
    }
    
    // åå§åæ¶ä»æ¬å°å­å¨å è½½æè¿æç´?
    onMounted(() => {
      try {
        const savedSearches = localStorage.getItem('recentSearches');
        if (savedSearches) {
          recentSearches.value = JSON.parse(savedSearches);
        }
      } catch (error) {
        console.error('å è½½æè¿æç´¢å¤±è´?', error);
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
