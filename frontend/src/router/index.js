import { createRouter, createWebHistory } from 'vue-router'

import StatsTrendsView from '../views/StatsTrendsView.vue'
import HomeView from '../views/HomeView.vue'
import RiskExplorer from '@/components/StatsTrendsPage/RiskExplorer.vue'
import BlogPage from '@/components/BlogPage.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/stats-trends', name: 'stats-trends', component: StatsTrendsView },
  { path: '/risk-explorer', name: 'risk-explorer', component: RiskExplorer },
  { path: '/blog', name: 'blog', component: BlogPage },
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
