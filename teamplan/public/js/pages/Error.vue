<template>
  <div class="error-page">
    <div class="error-container">
      <h1 class="error-code">{{ errorCode }}</h1>
      <h2 class="error-title">{{ errorTitle }}</h2>
      <p class="error-message">{{ errorMessage }}</p>
      <Button @click="goHome">
        返回首页  <!-- 原文: Go Home -->
      </Button>
    </div>
  </div>
</template>

<script>
export default {
  // ... 现有代码 ...
  computed: {
    errorTitle() {
      switch (this.errorCode) {
        case 404:
          return '页面未找到';  
        case 403:
          return '禁止访问';  // 原文: Forbidden
        case 500:
          return '服务器错误'; 
        default:
          return '发生错误';  // 原文: Error Occurred
      }
    },
    errorMessage() {
      switch (this.errorCode) {
        case 404:
          return '您请求的页面不存在。'; 
        case 403:
          return '您没有权限访问此页面。';  
        case 500:
          return '服务器处理您的请求时出错。'; 
        default:
          return '处理您的请求时发生未知错误。';  
      }
    }
  },
  methods: {
    goHome() {
      this.$router.push({ name: 'Home' });
    }
  }
}
</script>