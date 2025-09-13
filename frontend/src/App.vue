<script setup>
import {ref, onMounted, watch} from 'vue'
import LoadingScreen from './components/LoadingScreen.vue'
import signUrl from './assets/images/roadwork.png'
import Navbar from './components/Navbar.vue'
import MenuOverlay from './components/MenuOverlay.vue'
import HomeView from "@/views/HomeView.vue";
import 'mapbox-gl/dist/mapbox-gl.css'

const loading = ref(true)
const progress = ref(0)
const menuOpen = ref(false)


onMounted(async () => {
  // simulate work
  for (let i = 0; i <= 100; i += 5) {
    await new Promise((r) => setTimeout(r, 60))
    progress.value = i
  }
  loading.value = false
  document.title = import.meta.env.VITE_APP_NAME || 'SafeTrek'
})
</script>

<template>
  <main class="main">
  <LoadingScreen :show="loading" :progress="progress" :signSrc="signUrl" />
  <Navbar :open="menuOpen" @toggle="menuOpen = !menuOpen" />
  <MenuOverlay :open="menuOpen" @close="menuOpen = false" />
  <router-view></router-view>
  </main>
</template>
<style scoped>
.main{
  background: #f0ae00;
}
</style>
