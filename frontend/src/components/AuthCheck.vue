<template>
  <div class="auth-status">
    <div v-if="isLoggedIn">
      <p>Пользователь: {{ userEmail }}</p>
      <button @click="logout">Выйти</button>
    </div>
    <div v-else>
      <button @click="loginWithYandex">Войти через Яндекс</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const isLoggedIn = ref(false)
const userEmail = ref('')

const checkAuth = async () => {
  try {
    const response = await axios.get('/api/auth/me')
    isLoggedIn.value = true
    userEmail.value = response.data.email
  } catch {
    isLoggedIn.value = false
  }
}

const loginWithYandex = () => {
  window.location.href = '/api/auth/login/yandex'
}

const logout = async () => {
  await axios.post('/api/auth/logout')
  isLoggedIn.value = false
}

onMounted(() => {
  checkAuth()
})
</script>
