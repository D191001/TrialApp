<template>
  <div class="system-status">
    <div :class="['status-indicator', { 'is-healthy': isHealthy }]">
      Статус системы: {{ statusMessage }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const isHealthy = ref(false)
const statusMessage = ref('Проверка...')

const checkHealth = async () => {
  try {
    const response = await axios.get('/api/health-check')
    isHealthy.value = response.data.status === 'healthy'
    statusMessage.value = isHealthy.value ? 'Система работает' : 'Ошибка соединения'
  } catch (error) {
    isHealthy.value = false
    statusMessage.value = 'Ошибка соединения с сервером'
  }
}

onMounted(() => {
  checkHealth()
})
</script>
