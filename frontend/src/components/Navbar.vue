<template>
  <nav class="nav">
    <div class="nav__brand">
      <router-link to="/" class="link" ><img src="@/assets/images/safetrek_logo.svg" alt="SafeTrek Logo" class="logo" /></router-link>
    </div>


    <button class="nav__toggle" type="button" @click="toggleMenu">
      MENU
    </button>

    <!-- Overlay menu -->
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
}
.nav__brand {
  padding-top: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.nav__toggle {
  appearance: none;
  border: 0;
  border-radius: 999px;
  padding: 16px 32px;
  background: #0a0a0a;
  color: #ffc21a;
  cursor: pointer;
  font-weight: 700;
  letter-spacing: .02em;
}

.nav__brand img.logo {
  height: 85px;
  width: auto;
  display: block;
  object-fit: contain;
}


</style>
