<template>
  <div class="settings-page">
    <PageHeader>
      <h1>设置</h1>  <!-- 原文: Settings -->
    </PageHeader>
    
    <div class="settings-sections">
      <div class="settings-section">
        <h3>个人资料</h3>  <!-- 原文: Profile -->
        <div class="setting-item">
          <label for="full-name">全名</label>  <!-- 原文: Full Name -->
          <input
            id="full-name"
            v-model="profile.fullName"
            class="w-full"
          />
        </div>
        <div class="setting-item">
          <label for="email">电子邮箱</label>  <!-- 原文: Email -->
          <input
            id="email"
            v-model="profile.email"
            class="w-full"
            disabled
          />
        </div>
        <Button @click="saveProfile">
          保存个人资料  <!-- 原文: Save Profile -->
        </Button>
      </div>
      
      <div class="settings-section">
        <h3>通知设置</h3>  <!-- 原文: Notification Settings -->
        
        <div class="settings-form">
          <div class="form-group">
            <label class="checkbox-label">
              <input
                v-model="settings.emailNotifications"
                type="checkbox"
              />
              接收电子邮件通知  <!-- 原文: Receive Email Notifications -->
            </label>
            <p class="help-text">
              当有重要更新时通过电子邮件通知。 <!-- 原文: Get notified via email when there are important updates -->
            </p>
          </div>
          
          <div class="form-group">
            <label class="checkbox-label">
              <input
                v-model="settings.taskAssignments"
                type="checkbox"
              />
              任务分配通知  <!-- 原文: Task Assignment Notifications -->
            </label>
            <p class="help-text">
              当任务分配给您时收到通知  <!-- 原文: Get notified when tasks are assigned to you -->
            </p>
          </div>
          
          <div class="form-group">
            <label class="checkbox-label">
              <input
                v-model="settings.commentMentions"
                type="checkbox"
              />
              评论提及通知  <!-- 原文: Comment Mention Notifications -->
            </label>
            <p class="help-text">
              当有人在评论中提及您时收到通知  <!-- 原文: Get notified when someone mentions you in a comment -->
            </p>
          </div>
          
          <div class="form-group">
            <label class="checkbox-label">
              <input
                v-model="settings.projectUpdates"
                type="checkbox"
              />
              项目更新通知  <!-- 原文: Project Update Notifications -->
            </label>
            <p class="help-text">
              当您参与的项目有更新时收到通知  <!-- 原文: Get notified about updates to projects you're involved in -->
            </p>
          </div>
        </div>
      </div>
      
      <div class="settings-section">
        <h3>界面设置</h3>  <!-- 原文: Interface Settings -->
        
        <div class="settings-form">
          <div class="form-group">
            <label for="language">语言</label>  <!-- 原文: Language -->
            <select
              id="language"
              v-model="settings.language"
              class="w-full"
            >
              <option value="zh-CN">中文 (简介?</option>
              <option value="en-US">English (US)</option>
              <option value="es-ES">Español</option>
              <option value="fr-FR">Français</option>
              <option value="de-DE">Deutsch</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="theme">主题</label>  <!-- 原文: Theme -->
            <select
              id="theme"
              v-model="settings.theme"
              class="w-full"
            >
              <option value="light">浅色</option>  <!-- 原文: Light -->
              <option value="dark">深色</option>  <!-- 原文: Dark -->
              <option value="system">跟随系统</option>  <!-- 原文: System -->
            </select>
          </div>
          
          <div class="form-group">
            <label for="date-format">日期格式</label>  <!-- 原文: Date Format -->
            <select
              id="date-format"
              v-model="settings.dateFormat"
              class="w-full"
            >
              <option value="yyyy-MM-dd">YYYY-MM-DD</option>
              <option value="dd/MM/yyyy">DD/MM/YYYY</option>
              <option value="MM/dd/yyyy">MM/DD/YYYY</option>
            </select>
          </div>
        </div>
      </div>
      
      <div class="settings-section">
        <h3>隐私设置</h3>  <!-- 原文: Privacy Settings -->
        
        <div class="settings-form">
          <div class="form-group">
            <label class="checkbox-label">
              <input
                v-model="settings.showOnlineStatus"
                type="checkbox"
              />
              显示在线状态? <!-- 原文: Show Online Status -->
            </label>
            <p class="help-text">
              允许其他用户查看您的在线状态? <!-- 原文: Allow other users to see when you're online -->
            </p>
          </div>
          
          <div class="form-group">
            <label class="checkbox-label">
              <input
                v-model="settings.shareActivityData"
                type="checkbox"
              />
              分享活动数据  <!-- 原文: Share Activity Data -->
            </label>
            <p class="help-text">
              允许系统收集您的活动数据以改进用户体验? <!-- 原文: Allow the system to collect your activity data to improve user experience -->
            </p>
          </div>
        </div>
      </div>
    </div>
    
    <div class="settings-actions">
      <Button @click="saveSettings">
        保存设置  <!-- 原文: Save Settings -->
      </Button>
      <Button secondary @click="resetSettings">
        重置为默认? <!-- 原文: Reset to Default -->
      </Button>
    </div>
  </div>
</template>
