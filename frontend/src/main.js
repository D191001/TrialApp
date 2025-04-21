import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'

axios.defaults.baseURL = process.env.NODE_ENV === 'production'
    ? '/api'
    : 'http://localhost:8000';
axios.defaults.withCredentials = true;

const app = createApp(App)
app.config.globalProperties.$axios = axios
app.use(router)
app.mount('#app')
