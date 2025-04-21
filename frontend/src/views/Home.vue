<template>
  <div class="home">
    <h1>{{ isAuthenticated ? 'Добро пожаловать!' : 'Пожалуйста, войдите в систему' }}</h1>
    <div v-if="isAuthenticated">
      <feedback-form />
    </div>
    <div v-else>
      <router-link to="/login" class="login-link">Войти</router-link>
    </div>
  </div>
</template>

<script>
import FeedbackForm from '@/components/FeedbackForm.vue'

export default {
  name: 'Home',
  components: {
    FeedbackForm
  },
  data() {
    return {
      isAuthenticated: false
    }
  },
  created() {
    this.checkAuth()
  },
  methods: {
    checkAuth() {
      this.isAuthenticated = !!localStorage.getItem('token')
    }
  }
}
</script>

<style scoped>
.login-link {
  display: inline-block;
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #fc0;
  color: #000;
  text-decoration: none;
  border-radius: 4px;
}
</style>
