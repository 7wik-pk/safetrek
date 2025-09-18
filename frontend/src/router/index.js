
import { createRouter, createWebHistory } from 'vue-router'


import StatsTrendsView from '../views/StatsTrendsView.vue'
import HomeView from "../views/HomeView.vue";
import RiskExplorer from "@/components/StatsTrendsPage/RiskExplorer.vue";



const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/stats-trends', name: 'stats-trends', component: StatsTrendsView },
  {path:'/risk-explorer',name:'risk-explorer',component:RiskExplorer},
]

const router = createRouter({
  history: createWebHistory(),
  routes
})


export default router
