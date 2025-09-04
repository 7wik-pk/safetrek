
import { createRouter, createWebHistory } from 'vue-router'


import StatsTrendsView from '../views/StatsTrendsView.vue'
import HomeView from "../views/HomeView.vue";



const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/stats-trends', name: 'stats-trends', component: StatsTrendsView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})


export default router
