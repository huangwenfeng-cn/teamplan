<template>
  <div v-if="project" class="project-page">
    <PageHeader>
      <h1>{{ project.title }}</h1>
      <template #actions>
        <Button
          icon="settings"
          @click="showProjectSettings = true"
        >
          项目设置  <!-- 原文: Project Settings -->
        </Button>
      </template>
    </PageHeader>
    
    <div class="project-tabs">
      <Button
        :class="{ active: activeTab === 'overview' }"
        @click="activeTab = 'overview'"
      >
        概览  <!-- 原文: Overview -->
      </Button>
      <Button
        :class="{ active: activeTab === 'tasks' }"
        @click="activeTab = 'tasks'"
      >
        任务  <!-- 原文: Tasks -->
      </Button>
      <Button
        :class="{ active: activeTab === 'discussions' }"
        @click="activeTab = 'discussions'"
      >
        讨论  <!-- 原文: Discussions -->
      </Button>
      <Button
        :class="{ active: activeTab === 'members' }"
        @click="activeTab = 'members'"
      >
        成员  <!-- 原文: Members -->
      </Button>
    </div>
    
    <div class="project-content">
      <div v-if="activeTab === 'overview'" class="project-overview">
        <div class="project-description">
          <h3>项目描述</h3>  <!-- 原文: Project Description -->
          <p v-if="project.description">{{ project.description }}</p>
          <p v-else class="text-muted">无描述</p>  
        </div>
        
        <div class="project-stats">
          <div class="stat-card">
            <h4>任务</h4>  <!-- 原文: Tasks -->
            <div class="stat-value">{{ taskStats.total }}</div>
            <div class="stat-details">
              <div>已完成: {{ taskStats.completed }}</div>  
              <div>未完成: {{ taskStats.open }}</div>  
            </div>
          </div>
          
          <div class="stat-card">
            <h4>讨论</h4>  <!-- 原文: Discussions -->
            <div class="stat-value">{{ discussionCount }}</div>
          </div>
          
          <div class="stat-card">
            <h4>成员</h4>  <!-- 原文: Members -->
            <div class="stat-value">{{ memberCount }}</div>
          </div>
        </div>
        
        <div class="recent-activity">
          <h3>最近活动</h3> 
          <ActivityFeed :activities="recentActivities" />
        </div>
      </div>
      
      <div v-if="activeTab === 'tasks'" class="project-tasks">
        <div class="section-header">
          <h3>项目任务</h3>  <!-- 原文: Project Tasks -->
          <Button
            icon="plus"
            @click="showNewTaskDialog = true"
          >
            添加任务  <!-- 原文: Add Task -->
          </Button>
        </div>
        
        <div class="task-filters">
          <Button
            :class="{ active: taskFilter === 'all' }"
            @click="taskFilter = 'all'"
          >
            全部  <!-- 原文: All -->
          </Button>
          <Button
            :class="{ active: taskFilter === 'open' }"
            @click="taskFilter = 'open'"
          >
            未完成 
          </Button>
          <Button
            :class="{ active: taskFilter === 'completed' }"
            @click="taskFilter = 'completed'"
          >
            已完成 
          </Button>
        </div>
        
        <div v-if="filteredTasks.length === 0" class="empty-state">
          <p>没有任务</p>  <!-- 原文: No tasks -->
        </div>
        
        <div v-else class="task-list">
          <Task
            v-for="task in filteredTasks"
            :key="task.id"
            :task="task"
            @update="fetchTasks"
          />
        </div>
      </div>
      
      <div v-if="activeTab === 'discussions'" class="project-discussions">
        <div class="section-header">
          <h3>项目讨论</h3>  <!-- 原文: Project Discussions -->
          <Button
            icon="plus"
            @click="showNewDiscussionDialog = true"
          >
            添加讨论  <!-- 原文: Add Discussion -->
          </Button>
        </div>
        
        <div v-if="discussions.length === 0" class="empty-state">
          <p>没有讨论</p>  <!-- 原文: No discussions -->
        </div>
        
        <div v-else class="discussion-list">
          <DiscussionCard
            v-for="discussion in discussions"
            :key="discussion.id"
            :discussion="discussion"
          />
        </div>
      </div>
      
      <div v-if="activeTab === 'members'" class="project-members">
        <div class="section-header">
          <h3>项目成员</h3>  <!-- 原文: Project Members -->
          <Button
            icon="plus"
            @click="showAddMemberDialog = true"
          >
            添加成员  <!-- 原文: Add Member -->
          </Button>
        </div>
        
        <div v-if="members.length === 0" class="empty-state">
          <p>没有成员</p>  <!-- 原文: No members -->
        </div>
        
        <div v-else class="member-list">
          <div
            v-for="member in members"
            :key="member.user"
            class="member-item"
          >
            <UserAvatar
              :user="member.user"
              :image-url="member.user_image"
              :size="32"
            />
            <div class="member-info">
              <div class="member-name">{{ member.user }}</div>
              <div class="member-role">{{ member.role }}</div>
            </div>
            <div class="member-actions">
              <Button
                v-if="canManageMembers && member.user !== currentUser"
                small
                icon="trash"
                @click="removeMember(member)"
              >
                移除  <!-- 原文: Remove -->
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 项目设置对话框 -->
    <Dialog
      v-model="showProjectSettings"
      title="项目设置"  <!-- 原文: Project Settings -->
    >
      <div class="mb-4">
        <label for="project-title" class="block mb-1">项目标题</label>  <!-- 原文: Project Title -->
        <input
          id="project-title"
          v-model="editedProject.title"
          class="w-full"
        />
      </div>
      <div class="mb-4">
        <label for="project-description" class="block mb-1">项目描述</label>  <!-- 原文: Project Description -->
        <textarea
          id="project-description"
          v-model="editedProject.description"
          class="w-full"
          rows="3"
        ></textarea>
      </div>
      <div class="danger-zone">
        <h4>危险区域</h4>  <!-- 原文: Danger Zone -->
        <Button
          class="delete-button"
          @click="confirmDeleteProject"
        >
          删除项目  <!-- 原文: Delete Project -->
        </Button>
      </div>
      <template #actions>
        <Button secondary @click="showProjectSettings = false">
          取消  <!-- 原文: Cancel -->
        </Button>
        <Button @click="saveProjectSettings">
          保存  <!-- 原文: Save -->
        </Button>
      </template>
    </Dialog>
    
    <!-- 新任务对话框 -->
    <Dialog
      v-model="showNewTaskDialog"
      title="创建新任务"  
    >
      <div class="mb-4">
        <label for="task-title" class="block mb-1">任务标题</label>  <!-- 原文: Task Title -->
        <input
          id="task-title"
          v-model="newTask.title"
          class="w-full"
          placeholder="输入任务标题..."  <!-- 原文: Enter task title... -->
        />
      </div>
      <div class="mb-4">
        <label for="task-description" class="block mb-1">任务描述 (可选)</label>  
        <textarea
          id="task-description"
          v-model="newTask.description"
          class="w-full"
          placeholder="输入任务描述..."  <!-- 原文: Enter task description... -->
          rows="3"
        ></textarea>
      </div>
      <div class="mb-4">
        <label for="task-assigned-to" class="block mb-1">分配给</label> 
        <select
          id="task-assigned-to"
          v-model="newTask.assigned_to"
          class="w-full"
        >
          <option value="">未分配</option> 
          <option
            v-for="member in members"
            :key="member.user"
            :value="member.user"
          >
            {{ member.user }}
          </option>
        </select>
      </div>
      <div class="mb-4">
        <label for="task-due-date" class="block mb-1">截止日期 (可选)</label> 
        <input
          id="task-due-date"
          v-model="newTask.due_date"
          type="date"
          class="w-full"
        />
      </div>
      <template #actions>
        <Button secondary @click="showNewTaskDialog = false">
          取消  <!-- 原文: Cancel -->
        </Button>
        <Button
          :disabled="!newTask.title"
          @click="createTask"
        >
          创建  <!-- 原文: Create -->
        </Button>
      </template>
    </Dialog>
    
    <!-- 新讨论对话框 -->
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
      <div>
        <label for="discussion-content" class="block mb-1">讨论内容</label>  <!-- 原文: Discussion Content -->
        <textarea
          id="discussion-content"
          v-model="newDiscussion.content"
          class="w-full"
          placeholder="输入讨论内容..."  <!-- 原文: Enter discussion content... -->
          rows="5"
        ></textarea>
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
    
    <!-- 添加成员对话框 -->
    <Dialog
      v-model="showAddMemberDialog"
      title="添加项目成员"  <!-- 原文: Add Project Member -->
    >
      <div class="mb-4">
        <label for="member-user" class="block mb-1">用户</label>  <!-- 原文: User -->
        <select
          id="member-user"
          v-model="newMember.user"
          class="w-full"
        >
          <option value="">选择用户</option>  <!-- 原文: Select User -->
          <option
            v-for="user in availableUsers"
            :key="user.name"
            :value="user.name"
          >
            {{ user.full_name }} ({{ user.name }})
          </option>
        </select>
      </div>
      <div class="mb-4">
        <label for="member-role" class="block mb-1">角色</label>  <!-- 原文: Role -->
        <select
          id="member-role"
          v-model="newMember.role"
          class="w-full"
        >
          <option value="Member">成员</option>  <!-- 原文: Member -->
          <option value="Admin">管理员</option>  
        </select>
      </div>
      <template #actions>
        <Button secondary @click="showAddMemberDialog = false">
          取消  <!-- 原文: Cancel -->
        </Button>
        <Button
          :disabled="!newMember.user || !newMember.role"
          @click="addMember"
        >
          添加  <!-- 原文: Add -->
        </Button>
      </template>
    </Dialog>
  </div>
  <div v-else class="loading-state">
    <p>加载中...</p>  
  </div>
</template>