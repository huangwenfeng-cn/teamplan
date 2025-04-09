<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-header">
        <img
          src="/assets/teamplan/images/logo.png"
          alt="teamplan"
          class="logo"
        />
        <h1>创建账号</h1>  <!-- 原文: Create an Account -->
      </div>
      
      <form @submit.prevent="register" class="register-form">
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <div class="form-group">
          <label for="full-name">全名</label>  <!-- 原文: Full Name -->
          <input
            id="full-name"
            v-model="fullName"
            type="text"
            required
          />
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
            autocomplete="new-password"
          />
        </div>
        
        <div class="form-group">
          <label for="confirm-password">确认密码</label>  <!-- 原文: Confirm Password -->
          <input
            id="confirm-password"
            v-model="confirmPassword"
            type="password"
            required
            autocomplete="new-password"
          />
        </div>
        
        <Button
          type="submit"
          :loading="loading"
          full-width
        >
          注册  <!-- 原文: Register -->
        </Button>
      </form>
      
      <div class="register-footer">
        <p>
          已有账号�?
          <router-link to="/login">登录</router-link>  <!-- 原文: Already have an account? Login -->
        </p>
      </div>
    </div>
  </div>
</template>
