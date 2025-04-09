<template>
  <div class="login-page">
    <div class="auth-container">
      <div class="auth-logo">
        <img src="/assets/teamplan/images/logo.png" alt="teamplan" />
      </div>
      
      <h1 class="auth-title">登录</h1>  <!-- 原文: Login -->
      
      <div v-if="error" class="auth-error">
        {{ error }}
      </div>
      
      <form @submit.prevent="login">
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
        
        <div class="form-group">
          <label for="password">密码</label>  <!-- 原文: Password -->
          <input
            id="password"
            v-model="password"
            type="password"
            required
            placeholder="输入您的密码"  <!-- 原文: Enter your password -->
          />
        </div>
        
        <div class="form-actions">
          <Button
            type="submit"
            :loading="loading"
          >
            登录  <!-- 原文: Login -->
          </Button>
        </div>
      </form>
      
      <div class="auth-footer">
        <p>
          <router-link to="/forgot-password">忘记密码?</router-link>  <!-- 原文: Forgot Password? -->
        </p>
        <p>
          还没有账号？ <router-link to="/register">注册</router-link>  <!-- 原文: Don't have an account? Register -->
        </p>
      </div>
    </div>
  </div>
</template>
