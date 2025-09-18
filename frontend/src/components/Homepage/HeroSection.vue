<template>
  <section class="hero">
    <Swiper
      :modules="[Autoplay, Pagination, Navigation, EffectFade]"
      :loop="true"
      :autoplay="{ delay: 4000, disableOnInteraction: false }"
      :speed="1000"
      :effect="'fade'"
      :pagination="{ clickable: true }"
      :navigation="true"
      class="hero-swiper"
    >
      <!-- Slide 1 -->
      <SwiperSlide>
        <div class="slide">
          <img class="bg" src="/images/slider/01.jpg" alt="Slide 1" />
          <div class="overlay"></div>
          <div class="caption">
            <h2 class="title animate-fade-in-up">Identify Risky Areas</h2>
            <p class="subtitle animate-fade-in-up delay-1">Find out more</p>
            <router-link to="stats-trends" class="btn animate-fade-in-up delay-2">Explore Statistics & Insights</router-link>
          </div>
        </div>
      </SwiperSlide>

      <!-- Slide 2 -->
      <SwiperSlide>
        <div class="slide">
          <img class="bg" src="/images/slider/02.jpg" alt="Slide 2" />
          <div class="overlay"></div>
          <div class="caption">
            <h2 class="title animate-fade-in-up">Roads with SafeTrek</h2>
            <p class="subtitle animate-fade-in-up delay-1">
              Helping planners make informed decisions with statistics, visuals and insights
            </p>
            <router-link to="stats-trends" class="btn animate-fade-in-up delay-2">Explore Statistics & Insights</router-link>
          </div>
        </div>
      </SwiperSlide>

      <!-- Slide 3 -->
      <SwiperSlide>
        <div class="slide">
          <img class="bg" src="/images/slider/03.jpg" alt="Slide 3" />
          <div class="overlay"></div>
          <div class="caption">
            <h2 class="title animate-fade-in-up">Crash data</h2>
            <p class="subtitle animate-fade-in-up delay-1">
               With Demographics, vehicle type, weather, and road conditions
            </p>
            <router-link to="stats-trends" class="btn animate-fade-in-up delay-2">Explore Statistics & Insights</router-link>
          </div>
        </div>
      </SwiperSlide>
    </Swiper>
  </section>
</template>

<script setup lang="ts">
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Autoplay, Pagination, Navigation, EffectFade } from 'swiper/modules'

// Swiper CSS
import 'swiper/css'
import 'swiper/css/navigation'
import 'swiper/css/pagination'
import 'swiper/css/effect-fade'
</script>

<style scoped>
.hero-swiper {
  width: 100%;
  height: 90vh;
  min-height: 600px;
}

.slide {
  position: relative;
  width: 100%;
  height: 100%;
}

.bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.55); /* dark overlay */
  z-index: 1;
}

.caption {
  position: relative;
  z-index: 2;
  top: 40%;
  left: 10%;
  color: #fff;
  max-width: 600px;
}

.title {
  font-size: clamp(32px, 5vw, 64px);
  font-weight: 800;
  margin-bottom: 0.5rem;
  color: #fff;
}

.subtitle {
  font-size: clamp(16px, 2vw, 24px);
  margin-bottom: 1.5rem;
  color: #f1f1f1;
}

.btn {
  display: inline-block;
  padding: 12px 28px;
  border: 2px solid #fff;
  color: #fff;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s;
}
.btn:hover {
  background: #f15a24;
  border-color: #f15a24;
}

/* Animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  opacity: 0;
  animation: fadeInUp 1s ease forwards;
}
.delay-1 {
  animation-delay: 0.4s;
}
.delay-2 {
  animation-delay: 0.8s;
}
</style>
