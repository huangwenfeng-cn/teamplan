<template>
  <div class="profile-page">
    <PageHeader>
      <h1>个人资料</h1>  <!-- 原文: Profile -->
    </PageHeader>
    
    <div class="profile-sections">
      <div class="profile-section">
        <h3>基本信息</h3>  <!-- 原文: Basic Information -->
        
        <div class="profile-avatar">
          <UserAvatar
            :user="user.name"
            :image-url="user.image"
            :size="80"
          />
          <div class="avatar-actions">
            <Button @click="showAvatarUploadDialog = true">
              更改头像  <!-- 原文: Change Avatar -->
            </Button>
          </div>
        </div>
        
        <div class="profile-form">
          <div class="form-group">
            <label for="full-name">全名</label>  <!-- 原文: Full Name -->
            <input
              id="full-name"
              v-model="profile.fullName"
              class="w-full"
            />
          </div>
          
          <div class="form-group">
            <label for="email">电子邮箱</label>  <!-- 原文: Email -->
            <input
              id="email"
              v-model="profile.email"
              class="w-full"
              disabled
            />
          </div>
          
          <div class="form-group">
            <label for="bio">个人简介</label>  <!-- 原文: Bio -->
            <textarea
              id="bio"
              v-model="profile.bio"
              class="w-full"
              rows="3"
              placeholder="介绍一下您自己..."  <!-- 原文: Tell us about yourself... -->
            ></textarea>
          </div>
          
          <Button @click="saveProfile">
            保存个人资料  <!-- 原文: Save Profile -->
          </Button>
        </div>
      </div>
      
      <div class="profile-section">
        <h3>更改密码</h3>  <!-- 原文: Change Password -->
        
        <div class="profile-form">
          <div class="form-group">
            <label for="current-password">当前密码</label>  <!-- 原文: Current Password -->
            <input
              id="current-password"
              v-model="password.current"
              type="password"
              class="w-full"
            />
          </div>
          
          <div class="form-group">
            <label for="new-password">新密码</label>  <!-- 原文: New Password -->
            <input
              id="new-password"
              v-model="password.new"
              type="password"
              class="w-full"
            />
          </div>
          
          <div class="form-group">
            <label for="confirm-password">确认新密码</label>  <!-- 原文: Confirm New Password -->
            <input
              id="confirm-password"
              v-model="password.confirm"
              type="password"
              class="w-full"
            />
          </div>
          
          <Button
            :disabled="!password.current || !password.new || !password.confirm"
            @click="changePassword"
          >
            更改密码  <!-- 原文: Change Password -->
          </Button>
        </div>
      </div>
    </div>
    
    <!-- 头像上传对话框 -->
    <Dialog
      v-model="showAvatarUploadDialog"
      title="上传头像"  <!-- 原文: Upload Avatar -->
    >
      <div class="avatar-upload">
        <div class="upload-preview">
          <img
            v-if="avatarPreview"
            :src="avatarPreview"
            alt="头像预览"  <!-- 原文: Avatar Preview -->
          />
          <div v-if="!avatarPreview" class="no-preview">
            <i class="icon icon-image"></i>
            <p>无预览</p>  <!-- 原文: No Preview -->
          </div>
        </div>
        
        <div class="upload-controls">
          <input
            type="file"
            accept="image/*"
            @change="onAvatarSelected"
          />
          <p class="upload-hint">
            支持 JPG, PNG 和 GIF 格式，最大 2MB。 <!-- 原文: Supports JPG, PNG or GIF, max 2MB. -->
          </p>
        </div>
      </div>
      
      <template #actions>
        <Button secondary @click="showAvatarUploadDialog = false">
          取消  <!-- 原文: Cancel -->
        </Button>
        <Button
          :disabled="!avatarFile"
          @click="uploadAvatar"
        >
          上传  <!-- 原文: Upload -->
        </Button>
      </template>
    </Dialog>
  </div>
</template>