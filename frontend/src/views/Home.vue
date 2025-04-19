<template>
  <div class="home">
    <h1>Добро пожаловать</h1>
    <div v-if="isAuthenticated">
      <p>Вы вошли в систему</p>
      <FeedbackForm />
    </div>
    <div v-else>
      <p>Пожалуйста, войдите через Яндекс</p>
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
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem('token')
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
