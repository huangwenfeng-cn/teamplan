<template>
  <div class="login-page">
    <div class="auth-container">
      <div class="auth-logo">
        <img src="/assets/teamplan/images/logo.png" alt="teamplan" />
      </div>
      
      <h1 class="auth-title">登录</h1>
      
      <div v-if="error" class="auth-error">
        {{ error }}
      </div>
      
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="email">电子邮箱</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            placeholder="输入您的电子邮箱"
          />
        </div>
        
        <div class="form-group">
          <label for="password">密码</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            placeholder="输入您的密码"
          />
        </div>
        
        <div class="form-actions">
          <Button
            type="submit"
            :loading="loading"
          >
            登录
          </Button>
        </div>
      </form>
      
      <div class="auth-footer">
        <p>
          <router-link to="/forgot-password">忘记密码?</router-link>
        </p>
        <p>
          还没有账号？ <router-link to="/register">注册</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      loading: false,
      error: null
    }
  },
  methods: {
    async login() {
      this.loading = true
      this.error = null
      
      try {
        await this.$auth.login(this.email, this.password)
        this.$router.push('/')
      } catch (err) {
        this.error = err.message || '登录失败，请检查您的凭据'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f7f9fc;
}

.auth-container {
  width: 100%;
  max-width: 400px;
  padding: 2rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.auth-logo {
  text-align: center;
  margin-bottom: 1.5rem;
}

.auth-logo img {
  height: 48px;
}

.auth-title {
  font-size: 1.5rem;
  font-weight: 600;
  text-align: center;
  margin-bottom: 1.5rem;
}

.auth-error {
  background-color: #fee2e2;
  color: #b91c1c;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 1rem;
}

.form-actions {
  margin-top: 1.5rem;
}

.form-actions button {
  width: 100%;
}

.auth-footer {
  margin-top: 1.5rem;
  text-align: center;
}

.auth-footer p {
  margin: 0.5rem 0;
}

a {
  color: #4f46e5;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
