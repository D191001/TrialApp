<template>
  <div class="login">
    <h1>Вход в систему</h1>
    <div v-if="error" class="error-message">{{ error }}</div>
    <button @click="loginWithYandex" class="yandex-button">
      Войти через Яндекс
    </button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Login',
  data() {
    return {
      error: null
    }
  },
  methods: {
    async loginWithYandex() {
      try {
        const response = await axios.get('/auth/login/yandex')
        if (response.data.auth_url) {
          window.location.href = response.data.auth_url
        }
      } catch (error) {
        this.error = 'Ошибка авторизации'
        console.error(error)
      }
    }
  }
}
</script>

<style scoped>
.login {
  padding: 20px;
}

.yandex-button {
  background-color: #fc0;
  color: #000;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  min-width: 200px;
}

.yandex-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.error-message {
  color: red;
  margin: 10px 0;
}
</style>
