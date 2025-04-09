<template>
  <div class="notifications-page">
    <PageHeader>
      <h1>通知</h1>  <!-- 原文: Notifications -->
      <template #actions>
        <Button
          v-if="unreadNotificationsCount > 0"
          @click="markAllAsRead"
        >
          全部标为已读  <!-- 原文: Mark All as Read -->
        </Button>
      </template>
    </PageHeader>
    
    <div class="notifications-filters">
      <div class="filter-buttons">
        <Button
          :class="{ active: filter === 'all' }"
          @click="filter = 'all'"
        >
          全部  <!-- 原文: All -->
        </Button>
        <Button
          :class="{ active: filter === 'unread' }"
          @click="filter = 'unread'"
        >
          未读  <!-- 原文: Unread -->
        </Button>
      </div>
    </div>
    
    <div v-if="loading" class="loading-state">
      <p>加载中?..</p>  <!-- 原文: Loading... -->
    </div>
    
    <div v-else-if="filteredNotifications.length === 0" class="empty-state">
      <p>没有通知</p>  <!-- 原文: No notifications -->
    </div>
    
    <div v-else class="notifications-list">
      <Notification
        v-for="notification in filteredNotifications"
        :key="notification.name"
        :notification="notification"
        @mark-as-read="markAsRead"
      />
    </div>
  </div>
</template>
