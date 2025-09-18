import { Buffer } from 'buffer'
window.Buffer = Buffer

import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import router from './router/index.js'
import './styles/design-system.css'

const appName = import.meta.env.VITE_APP_NAME;

createApp(App)
.use(router)
.provide('appName', appName)
.mount('#app')
