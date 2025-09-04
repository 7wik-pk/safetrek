import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import router from './router/index.js'

const appName = import.meta.env.VITE_APP_NAME;

// sessionStorage.setItem('access_granted', 'false')
const accessGranted = sessionStorage.getItem('access_granted') === 'true'

// const accessGranted = localStorage.getItem('access_granted') === 'true'

if (accessGranted) {
  createApp(App)
  .use(router)
  .provide('appName', appName)
  .mount('#app')
} else {
  import('./components/PasswordGate.vue').then(({ default: Gate }) => {
    createApp(Gate).mount('#app')
  })
}
