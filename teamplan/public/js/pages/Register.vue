<template>
  <div class="register-page">
    <div class="auth-container">
      <div class="auth-logo">
        <img src="/assets/teamplan/images/logo.png" alt="teamplan" />
      </div>
      
      <h1 class="auth-title">注册</h1>  <!-- 原文: Register -->
      
      <div v-if="error" class="auth-error">
        {{ error }}
      </div>
      
      <form @submit.prevent="register">
        <div class="form-group">
          <label for="full-name">全名</label>  <!-- 原文: Full Name -->
          <input
            id="full-name"
            v-model="fullName"
            type="text"
            required
            placeholder="输入您的全名"  <!-- 原文: Enter your full name -->
          />
        </div>
        
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
            placeholder="创建密码"  <!-- 原文: Create a password -->
          />
          <p class="help-text">
            密码必须至少包含8个字符，包括一个数字和一个字母。 <!-- 原文: Password must be at least 8 characters long and include a number and a letter. -->
          </p>
        </div>
        
        <div class="form-group">
          <label for="confirm-password">确认密码</label>  <!-- 原文: Confirm Password -->
          <input
            id="confirm-password"
            v-model="confirmPassword"
            type="password"
            required
            placeholder="确认您的密码"  <!-- 原文: Confirm your password -->
          />
        </div>
        
        <div class="form-actions">
          <Button
            type="submit"
            :loading="loading"
          >
            注册  <!-- 原文: Register -->
          </Button>
        </div>
      </form>
      
      <div class="auth-footer">
        <p>
          已有账号?<router-link to="/login">登录</router-link>  <!-- 原文: Already have an account? Login -->
        </p>
      </div>
    </div>
  </div>
</template>
