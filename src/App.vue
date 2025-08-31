<script setup>
import { ref, onMounted } from 'vue'
import LoadingScreen from './components/LoadingScreen.vue'
import signUrl from './assets/roadwork.png'

const loading = ref(true)
const progress = ref(0)

onMounted(async () => {
  // simulate work
  for (let i = 0; i <= 100; i += 5) {
    await new Promise((r) => setTimeout(r, 160))
    progress.value = i
  }
  loading.value = false
})
</script>

<template>
  <LoadingScreen :show="loading" :progress="progress" :signSrc="signUrl" />
  <router-view />
</template>
