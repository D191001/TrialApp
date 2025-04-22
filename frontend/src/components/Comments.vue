<template>
  <div class="comments-section">
    <div v-if="isLoggedIn">
      <form @submit.prevent="submitComment">
        <textarea v-model="newComment" required></textarea>
        <button type="submit">Отправить комментарий</button>
      </form>
    </div>
    <div class="comments-list">
      <div v-for="comment in comments" :key="comment.id" class="comment">
        <p>{{ comment.text }}</p>
        <small>{{ comment.author_email }} - {{ formatDate(comment.created_at) }}</small>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const comments = ref([])
const newComment = ref('')
const isLoggedIn = ref(false)

const loadComments = async () => {
  const response = await axios.get('/api/feedback/comments')
  comments.value = response.data
}

const submitComment = async () => {
  try {
    await axios.post('/api/feedback/comments', {
      text: newComment.value
    })
    newComment.value = ''
    await loadComments()
  } catch (error) {
    console.error('Ошибка при отправке комментария:', error)
  }
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleString()
}

onMounted(async () => {
  try {
    await axios.get('/api/auth/me')
    isLoggedIn.value = true
  } catch {
    isLoggedIn.value = false
  }
  loadComments()
})
</script>
