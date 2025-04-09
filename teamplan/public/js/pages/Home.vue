<template>
  <div class="home-page">
    <PageHeader>
      <h1>仪表盘</h1>  <!-- 修复: 仪表盘?/h1> -->
    </PageHeader>
    
    <div class="dashboard-sections">
      <div class="dashboard-section">
        <h3>我的任务</h3>  <!-- 原文: My Tasks -->
        
        <div v-if="loading.tasks" class="loading-state">
          <p>加载中...</p> 
        </div>
        
        <div v-else-if="myTasks.length === 0" class="empty-state">
          <p>您没有待处理的任务</p> 
          <Button
            icon="plus"
            @click="goToNewTask"
          >
            创建任务  <!-- 原文: Create Task -->
          </Button>
        </div>
        
        <div v-else class="tasks-list">
          <Task
            v-for="task in myTasks"
            :key="task.name"
            :task="task"
            @update="fetchTasks"
          />
        </div>
        
        <div class="section-footer">
          <router-link to="/tasks">
            查看所有任务 
          </router-link>
        </div>
      </div>
      
      <div class="dashboard-section">
        <h3>最近的讨论</h3>  <!-- 原文: Recent Discussions -->
        
        <div v-if="loading.discussions" class="loading-state">
          <p>加载中...</p> 
        </div>
        
        <div v-else-if="recentDiscussions.length === 0" class="empty-state">
          <p>没有最近的讨论</p>  <!-- 原文: No recent discussions -->
          <Button
            icon="plus"
            @click="goToNewDiscussion"
          >
            创建讨论  <!-- 原文: Create Discussion -->
          </Button>
        </div>
        
        <div v-else class="discussions-list">
          <DiscussionCard
            v-for="discussion in recentDiscussions"
            :key="discussion.name"
            :discussion="discussion"
          />
        </div>
        
        <div class="section-footer">
          <router-link to="/discussions">
            查看所有讨论 
          </router-link>
        </div>
      </div>
      
      <div class="dashboard-section">
        <h3>活动提要</h3>  <!-- 原文: Activity Feed -->
        
        <div v-if="loading.activities" class="loading-state">
          <p>加载中...</p> 
        </div>
        
        <div v-else>
          <ActivityFeed :activities="recentActivities" />
        </div>
      </div>
      
      <div class="dashboard-section">
        <h3>即将到来的事件</h3> 
        
        <div v-if="loading.events" class="loading-state">
          <p>加载中...</p> 
        </div>
        
        <div v-else-if="upcomingEvents.length === 0" class="empty-state">
          <p>没有即将到来的事件</p> 
          <Button
            icon="plus"
            @click="goToCalendar"
          >
            创建事件  <!-- 原文: Create Event -->
          </Button>
        </div>
        
        <div v-else class="events-list">
          <EventCard
            v-for="event in upcomingEvents"
            :key="event.name"
            :event="event"
          />
        </div>
        
        <div class="section-footer">
          <router-link to="/calendar">
            查看日历  <!-- 原文: View Calendar -->
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>