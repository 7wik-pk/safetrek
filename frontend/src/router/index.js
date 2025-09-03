// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// Pages
import SafeRoadInsightView from '../views/RoadInsightsView.vue'
import HomeView from "../views/HomeView.vue";

// If you really want a /menu route as a page, import it
// import MenuOverlay from '@/components/MenuOverlay.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/safe-road-insight', name: 'safe-road-insight', component: SafeRoadInsightView }
  // If /menu is only an overlay (not a page), remove this route.
  // If you want it as a page, uncomment the import above and add:
  // { path: '/menu', name: 'menu', component: MenuOverlay },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})


export default router
