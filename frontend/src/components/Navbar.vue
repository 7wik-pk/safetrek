<template>
  <nav class="nav">
    <div class="nav__brand">SafeTrek</div>

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

// Auto-close any time the route changes
watch(
  () => route.fullPath,
  () => {
    isMenuOpen.value = false
  }
)
</script>

<style scoped>
.nav {
  position: relative;
  z-index: 10000;              /* Make sure button sits above hero, etc. */
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: transparent;     /* Your style */
}

.nav__brand {
  font-weight: 700;
}

.nav__toggle {
  appearance: none;
  border: 0;
  border-radius: 999px;
  padding: 8px 16px;
  background: #0a0a0a;
  color: #ffc21a;
  cursor: pointer;
  font-weight: 700;
  letter-spacing: .02em;
}
</style>
