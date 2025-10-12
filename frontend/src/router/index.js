import { createRouter, createWebHistory } from 'vue-router'

import StatsTrendsView from '../views/StatsTrendsView.vue'
import HomeView from '../views/HomeView.vue'
import BlogPage from '@/components/AboutPage.vue'
import RiskView from "@/components/RiskExplorerPage/RiskView.vue";
import EducationView from '@/views/EducationView.vue'
import DangerExplorer from '@/components/DangerExplorer.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/stats-trends', name: 'stats-trends', component: StatsTrendsView },
  { path: '/risk-explorer', name: 'risk-explorer', component: RiskView },
  { path: '/about', name: 'about', component: BlogPage },
  { path: '/education', name: 'education', component: EducationView },
  { path: '/risk-finder', name: 'risk-finder', component: DangerExplorer },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
        top: 80,
      }
    }
    return { top: 0 }
  },
})

export default router
