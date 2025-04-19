<template>
  <div class="callback">
    <h2>Выполняется вход...</h2>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Callback',
  async created() {
    const code = new URLSearchParams(window.location.search).get('code')
    if (code) {
      try {
        const response = await axios.get(`http://localhost:8000/auth/callback/yandex?code=${code}`)
        localStorage.setItem('token', response.data.access_token)
        this.$router.push('/')
      } catch (error) {
        console.error('Ошибка при получении токена:', error)
        this.$router.push('/login')
      }
    }
  }
}
</script>
