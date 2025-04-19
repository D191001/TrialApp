<template>
  <div class="feedback-form">
    <h2>Оставьте свой отзыв</h2>
    <input type="email" v-model="email" placeholder="Ваш email">
    <textarea v-model="comment" placeholder="Ваш комментарий"></textarea>
    <button @click="submitFeedback">Отправить</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      email: '',
      comment: ''
    };
  },
  methods: {
    async submitFeedback() {
      try {
        const response = await axios.post('/feedback', { // Замените на URL вашего API
          email: this.email,
          comment: this.comment
        });
        console.log('Отзыв отправлен', response.data);
        alert('Спасибо за ваш отзыв!');
        this.email = '';
        this.comment = '';
      } catch (error) {
        console.error('Ошибка отправки отзыва', error);
        alert('Ошибка отправки отзыва.');
      }
    }
  }
};
</script>

<style scoped>
.feedback-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-top: 20px;
}

.feedback-form h2 {
  margin-bottom: 15px;
}

.feedback-form input,
.feedback-form textarea {
  width: 300px;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.feedback-form textarea {
  height: 100px;
}

.feedback-form button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.feedback-form button:hover {
  background-color: #0056b3;
}
</style>
