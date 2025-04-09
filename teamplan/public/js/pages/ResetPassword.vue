<template>
  <div class="reset-password-page">
    <div class="auth-container">
      <h1 class="auth-title">重置密码</h1>  <!-- 原文: Reset Password -->
      
      <div v-if="message" class="message" :class="{ error: isError }">
        {{ message }}
      </div>
      
      <form v-if="!passwordReset" @submit.prevent="resetPassword">
        <div class="form-group">
          <label for="new-password">新密码</label>  <!-- 原文: New Password -->
          <input
            id="new-password"
            v-model="newPassword"
            type="password"
            required
            placeholder="输入新密码"  
          />
        </div>
        
        <div class="form-group">
          <label for="confirm-password">确认密码</label>  <!-- 原文: Confirm Password -->
          <input
            id="confirm-password"
            v-model="confirmPassword"
            type="password"
            required
            placeholder="确认新密码" 
          />
        </div>
        
        <div class="form-actions">
          <Button
            type="submit"
            :loading="loading"
          >
            重置密码  <!-- 原文: Reset Password -->
          </Button>
        </div>
      </form>
      
      <div v-else class="success-message">
        <p>您的密码已成功重置。</p> 
        <Button @click="goToLogin">
          前往登录  <!-- 原文: Go to Login -->
        </Button>
      </div>
    </div>
  </div>
</template>