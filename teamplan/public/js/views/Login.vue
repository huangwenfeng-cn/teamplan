<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-header">
        <img
          src="/assets/teamplan/images/logo.png"
          alt="teamplan"
          class="logo"
        />
        <h1>欢迎回来</h1>  <!-- 原文: Welcome Back -->
      </div>
      
      <form @submit.prevent="login" class="login-form">
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <div class="form-group">
          <label for="email">邮箱</label>  <!-- 原文: Email -->
          <input
            id="email"
            v-model="email"
            type="email"
            required
            autocomplete="email"
          />
        </div>
        
        <div class="form-group">
          <label for="password">密码</label>  <!-- 原文: Password -->
          <input
            id="password"
            v-model="password"
            type="password"
            required
            autocomplete="current-password"
          />
        </div>
        
        <div class="form-options">
          <label class="remember-me">
            <input type="checkbox" v-model="rememberMe" />
            <span>记住�?/span>  <!-- 原文: Remember me -->
          </label>
          
          <router-link to="/forgot-password" class="forgot-password">
            忘记密码�? <!-- 原文: Forgot password? -->
          </router-link>
        </div>
        
        <Button
          type="submit"
          :loading="loading"
          full-width
        >
          登录  <!-- 原文: Login -->
        </Button>
      </form>
      
      <div class="login-footer">
        <p>
          还没有账号？
          <router-link to="/register">注册</router-link>  <!-- 原文: Don't have an account? Register -->
        </p>
      </div>
    </div>
  </div>
</template>
