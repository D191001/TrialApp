import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'

axios.defaults.baseURL = 'http://localhost:8000'; // Замените на URL вашего API

const app = createApp(App)
app.config.globalProperties.$axios = axios
app.use(router)
app.mount('#app')
