import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import router from './router/index.js'

const appName = import.meta.env.VITE_APP_NAME;

createApp(App)
.use(router)
.provide('appName', appName)
.mount('#app')
