<template>
  <div id="app">
    <SystemHealth />
    <AuthCheck />
    <Comments />
  </div>
</template>

<script setup lang="ts">
import SystemHealth from './components/SystemHealth.vue'
import AuthCheck from './components/AuthCheck.vue'
import Comments from './components/Comments.vue'
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
