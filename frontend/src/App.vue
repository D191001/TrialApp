<template>
  <div id="app">
    <nav>
      <router-link to="/">Главная</router-link> |
      <router-link to="/login" v-if="!isAuthenticated">Войти</router-link>
      <span v-else>
        <span class="user-status">Вы авторизованы</span> |
        <a href="#" @click.prevent="logout">Выйти</a>
      </span>
    </nav>
    <router-view/>
    <div v-if="isAuthenticated" class="feedback-form">
      <h3>Обратная связь</h3>
      <textarea 
        v-model="feedbackText" 
        placeholder="Введите ваше сообщение"
        rows="4"
      ></textarea>
      <button @click="sendFeedback" :disabled="!feedbackText">Отправить</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isAuthenticated: false,
      feedbackText: ''
    }
  },
  created() {
    // Проверяем наличие токена при загрузке
    this.checkAuth()
  },
  methods: {
    checkAuth() {
      // Проверяем наличие токена в localStorage
      this.isAuthenticated = !!localStorage.getItem('token')
    },
    logout() {
      localStorage.removeItem('token')
      this.isAuthenticated = false
      this.$router.push('/login')
    },
    sendFeedback() {
      if (this.feedbackText) {
        // Здесь будет логика отправки на сервер
        console.log('Отправка обратной связи:', this.feedbackText)
        this.feedbackText = ''
        alert('Спасибо за обратную связь!')
      }
    }
  }
}
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  text-align: center;
  margin-top: 60px;
}

.user-status {
  color: green;
  font-weight: bold;
}

.feedback-form {
  max-width: 500px;
  margin: 20px auto;
  padding: 20px;
}

.feedback-form textarea {
  width: 100%;
  margin: 10px 0;
  padding: 8px;
}

.feedback-form button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.feedback-form button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>
