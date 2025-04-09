<template>
  <div class="discussions-page">
    <PageHeader>
      <h1>讨论</h1>  <!-- 原文: Discussions -->
      <template #actions>
        <Button
          icon="plus"
          @click="showNewDiscussionDialog = true"
        >
          新建讨论  <!-- 原文: New Discussion -->
        </Button>
      </template>
    </PageHeader>
    
    <div class="discussions-filters">
      <div class="search-filter">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索讨论..."  <!-- 原文: Search discussions... -->
        />
        <i class="icon icon-search"></i>
      </div>
      
      <div class="project-filter">
        <select v-model="projectFilter">
          <option value="">所有项目</option>  <!-- 原文: All Projects... -->
          <option
            v-for="project in projects"
            :key="project.name"
            :value="project.name"
          >
            {{ project.title }}
          </option>
        </select>
      </div>
      
      <div class="sort-filter">
        <select v-model="sortBy">
          <option value="recent">最近更新</option>  
          <option value="newest">最新创建</option>  
          <option value="oldest">最早创建</option>  
          <option value="most_comments">评论最多</option>  
        </select>
      </div>
    </div>
    
    <div v-if="loading" class="loading-state">
      <p>加载中...</p>  
    </div>
    
    <div v-else-if="filteredDiscussions.length === 0" class="empty-state">
      <div v-if="hasFilters" class="no-results">
        <p>没有找到匹配的讨论</p>  
        <Button @click="clearFilters">
          清除筛选条件
        </Button>
      </div>
      <div v-else class="no-discussions">
        <p>您还没有任何讨论</p>  <!-- 原文: You don't have any discussions yet -->
        <Button
          icon="plus"
          @click="showNewDiscussionDialog = true"
        >
          创建第一个讨论
        </Button>
      </div>
    </div>
    
    <div v-else class="discussions-list">
      <DiscussionCard
        v-for="discussion in filteredDiscussions"
        :key="discussion.name"
        :discussion="discussion"
      />
    </div>
    
    <!-- 新建讨论对话框 -->
    <Dialog
      v-model="showNewDiscussionDialog"
      title="创建新讨论" 
    >
      <div class="mb-4">
        <label for="discussion-title" class="block mb-1">讨论标题</label>  <!-- 原文: Discussion Title -->
        <input
          id="discussion-title"
          v-model="newDiscussion.title"
          class="w-full"
          placeholder="输入讨论标题..."  <!-- 原文: Enter discussion title... -->
        />
      </div>
      <div class="mb-4">
        <label for="discussion-content" class="block mb-1">讨论内容</label>  <!-- 原文: Discussion Content -->
        <textarea
          id="discussion-content"
          v-model="newDiscussion.content"
          class="w-full"
          placeholder="输入讨论内容..."  <!-- 原文: Enter discussion content... -->
          rows="5"
        ></textarea>
      </div>
      <div class="mb-4">
        <label for="discussion-project" class="block mb-1">项目 (可选)</label> 
        <select
          id="discussion-project"
          v-model="newDiscussion.project"
          class="w-full"
        >
          <option value="">无项目</option> 
          <option
            v-for="project in projects"
            :key="project.name"
            :value="project.name"
          >
            {{ project.title }}
          </option>
        </select>
      </div>
      <template #actions>
        <Button secondary @click="showNewDiscussionDialog = false">
          取消  <!-- 原文: Cancel -->
        </Button>
        <Button
          :disabled="!newDiscussion.title || !newDiscussion.content"
          @click="createDiscussion"
        >
          创建  <!-- 原文: Create -->
        </Button>
      </template>
    </Dialog>
  </div>
</template>