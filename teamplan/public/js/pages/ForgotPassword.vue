<template>
  <div class="forgot-password-page">
    <div class="auth-container">
      <h1 class="auth-title">忘记密码</h1>  <!-- 原文: Forgot Password -->
      
      <div v-if="message" class="message" :class="{ error: isError }">
        {{ message }}
      </div>
      
      <form v-if="!resetLinkSent" @submit.prevent="sendResetLink">
        <div class="form-group">
          <label for="email">电子邮箱</label>  <!-- 原文: Email -->
          <input
            id="email"
            v-model="email"
            type="email"
            required
            placeholder="输入您的电子邮箱"  <!-- 原文: Enter your email -->
          />
        </div>
        
        <div class="form-actions">
          <Button
            type="submit"
            :loading="loading"
          >
            发送重置链接 
          </Button>
        </div>
      </form>
      
      <div v-else class="success-message">
        <p>重置密码链接已发送到您的电子邮箱。请检查您的收件箱。</p>  
        <Button @click="resetForm">
          返回  <!-- 原文: Back -->
        </Button>
      </div>
      
      <div class="auth-footer">
        <p>
          <router-link to="/login">返回登录</router-link>  <!-- 原文: Back to Login -->
        </p>
      </div>
    </div>
  </div>
</template>