<template>
  <nav class="nav">
    <!-- Brand -->
    <div class="nav__brand">
      <router-link to="/" class="link">
        <img
          src="@/assets/images/safetrek_logo.svg"
          alt="SafeTrek Logo"
          class="logo"
        />
        <span class="brand-name">SafeTrek</span>
      </router-link>
    </div>

    <!-- Desktop menu -->
    <ul class="nav__links">
      <li><router-link to="/" class="link" active-class="active">Home</router-link></li>
      <li><router-link to="/stats-trends" class="link" active-class="active">Statistics & Trends</router-link></li>
      <li><router-link to="" class="link" >Blackspot & Corridor</router-link></li>
      <li><router-link to="" class="link" >Equity & Vulnerability</router-link></li>
    </ul>

    <!-- Mobile toggle -->
    <button class="nav__toggle" type="button" @click="toggleMenu">
      MENU
    </button>

    <!-- Overlay menu for mobile -->
    <MenuOverlay :open="isMenuOpen" @close="closeMenu" />
  </nav>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import MenuOverlay from './MenuOverlay.vue'

const isMenuOpen = ref(false)
const route = useRoute()

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const closeMenu = () => {
  isMenuOpen.value = false
}

watch(
  () => route.fullPath,
  () => {
    isMenuOpen.value = false
  }
)
</script>

<style scoped>
.nav {
  height: 90px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(0, 0, 0, 0.7); /* semi-transparent over hero */
  position: fixed;
  width: 100%;
  top: 0;
  z-index: 50;
  backdrop-filter: blur(6px);
}

/* Brand */
.nav__brand {
  display: flex;
  align-items: center;
  gap: 10px;
}
.nav__brand img.logo {
  height: 60px;
  width: auto;
  object-fit: contain;
}
.brand-name {
  font-size: 1.4rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: 0.5px;
}

/* Links */
.nav__links {
  display: flex;
  gap: 24px;
  list-style: none;
}
.link {
  color: #fff;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}
.link:hover,
.link.active {
  color: #f15a24; /* orange accent */
}

/* Mobile toggle */
.nav__toggle {
  display: none; /* hidden on desktop */
  appearance: none;
  border: 0;
  border-radius: 999px;
  padding: 12px 24px;
  background: #0a0a0a;
  color: #ffc21a;
  cursor: pointer;
  font-weight: 700;
  letter-spacing: 0.02em;
}

/* Responsive */
@media (max-width: 900px) {
  .nav__links {
    display: none;
  }
  .nav__toggle {
    display: block;
  }
}
</style>
