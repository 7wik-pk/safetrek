
import { createRouter, createWebHistory } from 'vue-router'


import SafeRoadInsightView from '../views/RoadInsightsView.vue'
import HomeView from "../views/HomeView.vue";



const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/safe-road-insight', name: 'safe-road-insight', component: SafeRoadInsightView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})


export default router
