<template>
  <div class="video-card" @click="toggleExpand">
    <!-- Default thumbnail view -->
    <div v-if="!expanded" class="thumbnail">
      <img :src="thumbnail" alt="Video Thumbnail" class="thumb-img" />
      <div class="tag">{{ tag }}</div>
      <h3>{{ title }}</h3>
    </div>

    <!-- Expanded cinematic view -->
    <transition name="expand">
      <div v-if="expanded" class="expanded">
        <div class="video-wrapper">
          <video
            ref="videoRef"
            :src="videoSrc"
            autoplay
            muted
            playsinline
            loop
            class="video-player"
          ></video>
        </div>

        <!-- Description panel -->
        <div class="description">
          <h2>{{ title }}</h2>
          <p>{{ description }}</p>
        </div>

        <!-- Close button -->
        <button class="close-btn" @click.stop="toggleExpand(false)">×</button>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue"

const props = defineProps<{
  title: string
  tag: string
  thumbnail: string
  videoSrc: string
  description: string
}>()

const expanded = ref(false)
const videoRef = ref<HTMLVideoElement | null>(null)

function toggleExpand(force?: boolean) {
  expanded.value = force ?? !expanded.value
}

watch(expanded, (isOpen) => {
  if (isOpen) videoRef.value?.play()
  else videoRef.value?.pause()
})
</script>

<style scoped>
/* --- Default Thumbnail Card --- */
.video-card {
  position: relative;
  border-radius: 14px;
  overflow: hidden;
  cursor: pointer;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease;
  background: #fffdf8;
}
.video-card:hover {
  transform: translateY(-5px);
}

.thumbnail {
  position: relative;
}
.thumb-img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 14px;
}
.tag {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: rgba(255, 204, 0, 0.9);
  color: #111;
  font-weight: 700;
  font-size: 0.75rem;
  padding: 4px 8px;
  border-radius: 6px;
  letter-spacing: 0.05em;
}
.thumbnail h3 {
  padding: 10px;
  background: #fff;
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

/* --- Expanded Cinematic View --- */
.expanded {
  position: fixed;
  inset: 0;
  z-index: 100;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  backdrop-filter: blur(8px);
  overflow-y: auto;
  padding: 60px 0;
}

.video-wrapper {
  width: 80%;
  max-width: 900px;
  aspect-ratio: 16/9;
  background: black;
  border-radius: 12px 12px 0 0;
  overflow: hidden;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
}

.video-player {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* --- White Description Panel --- */
.description {
  background: white;
  color: #111;
  width: 80%;
  max-width: 900px;
  padding: 28px;
  border-radius: 0 0 12px 12px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  margin-top: -5px;
}
.description h2 {
  font-size: 1.6rem;
  margin-bottom: 10px;
  font-weight: 700;
}
.description p {
  font-size: 1rem;
  line-height: 1.6;
  color: #333;
}

/* --- Close Button --- */
.close-btn {
  position: fixed;
  top: 30px;
  right: 40px;
  background: rgba(255, 255, 255, 0.3);
  border: none;
  color: white;
  font-size: 2rem;
  line-height: 1;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  cursor: pointer;
  transition: background 0.3s;
}
.close-btn:hover {
  background: rgba(255, 255, 255, 0.5);
}

/* --- Smooth Animation --- */
.expand-enter-active,
.expand-leave-active {
  transition: all 0.4s ease;
}
.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>
