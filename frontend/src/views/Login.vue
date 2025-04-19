<template>
  <div class="login">
    <h1>Вход в систему</h1>
    <div v-if="error" class="error-message">{{ error }}</div>
    <button 
      @click="loginWithYandex" 
      class="yandex-button"
      :disabled="isLoading"
    >
      <span v-if="isLoading">Загрузка...</span>
      <span v-else>Войти через Яндекс</span>
    </button>
  </div>
</template>

<script>
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

export default {
  name: 'Login',
  data() {
    return {
      isLoading: false,
      error: null
    }
  },
  methods: {
    async loginWithYandex() {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await api.get('/auth/login/yandex')
        console.log('Ответ сервера:', response)
        
        if (response.data && response.data.auth_url) {
          window.location.href = response.data.auth_url
        } else {
          this.error = 'Некорректный ответ от сервера'
        }
      } catch (error) {
        console.error('Полная информация об ошибке:', error)
        
        if (error.code === 'ECONNABORTED') {
          this.error = 'Превышено время ожидания ответа от сервера'
        } else if (error.code === 'ERR_NETWORK') {
          this.error = 'Сервер недоступен. Убедитесь, что бэкенд запущен на порту 8000'
        } else {
          this.error = `Ошибка: ${error.message}`
        }
      } finally {
        this.isLoading = false
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
