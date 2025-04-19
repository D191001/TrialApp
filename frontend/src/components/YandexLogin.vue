<template>
  <div class="login">
    <button @click="loginWithYandex" class="yandex-btn">
      Войти через Яндекс
    </button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'YandexLogin',
  methods: {
    async loginWithYandex() {
      try {
        const response = await axios.get('http://localhost:8000/auth/login/yandex');
        window.location.href = response.data.auth_url;
      } catch (error) {
        console.error('Ошибка авторизации:', error);
      }
    }
  }
}
</script>

<style scoped>
.yandex-btn {
  background: #fc0;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>
