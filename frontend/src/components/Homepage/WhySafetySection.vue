<script setup>
import { Swiper, SwiperSlide } from 'swiper/vue'
import 'swiper/css'
import 'swiper/css/navigation'

import { Navigation } from 'swiper/modules'

// images
import whySafetyImage from '/images/latest-projects/Building-Trades-373x373.jpg'
import service1 from '/images/bg2.jpg'
import service2 from '/images/bg3.jpg'
</script>

<template>
  <section class="why-safety">
    <h2 class="section-title">Our Mission</h2>

    <Swiper
      :modules="[Navigation]"
      navigation
      :loop="true"
      :space-between="30"
      class="services-swiper"
    >
      <!-- Slide 1 -->
      <SwiperSlide>
        <div class="slide-content">
          <img :src="whySafetyImage" alt="Why Safety First" class="slide-image" />
          <div class="slide-card">
            <h3>Why Safety First?</h3>
            <p>
              Safety is the foundation of thriving communities and sustainable cities. Every road
              crash not only impacts individuals and families but also places a burden on health
              systems and economies.
            </p>
          </div>
        </div>
      </SwiperSlide>

      <!-- Slide 2 -->
      <SwiperSlide>
        <div class="slide-content">
          <img :src="service1" alt="Service 1" class="slide-image" />
          <div class="slide-card">
            <h3>Promote equitable and safer communities</h3>
            <p>
              Ensure interventions protect the most vulnerable road users and support sustainable
              urban growth.
            </p>
          </div>
        </div>
      </SwiperSlide>

      <!-- Slide 3 -->
      <SwiperSlide>
        <div class="slide-content">
          <img :src="service2" alt="Service 2" class="slide-image" />
          <div class="slide-card">
            <h3>Empower evidence-based decisions</h3>
            <p>
              Equip planners and policymakers with tools to identify risks and design proactive
              safety measures.
            </p>
          </div>
        </div>
      </SwiperSlide>
    </Swiper>
  </section>
</template>

<style scoped>
/* make the section white */
.why-safety {
  background: #fff;
  padding: 56px 20px 80px;
  color: #111;
}

.section-title {
  text-align: center;
  font-size: clamp(26px, 4vw, 40px);
  font-weight: 900;
  margin-bottom: 28px;
}

/* ---- Swiper frame ---- */
.services-swiper {
  padding-inline: 70px; /* space for arrows */
  --slide-h: 520px;
}

/* allow bleed beyond container */
.services-swiper :deep(.swiper),
.services-swiper :deep(.swiper-wrapper),
.services-swiper :deep(.swiper-slide) {
  overflow: visible;
}

/* center slides */
.services-swiper .swiper-slide {
  display: flex;
  justify-content: center;
}

/* ---- Stage (image + overlay card) ---- */
.slide-content {
  position: relative;
  width: min(100%, 1140px);
  height: var(--slide-h);
  margin: 0 auto;
  overflow: visible; /* allow image/card overflow */
  box-shadow: 0 12px 38px rgba(0, 0, 0, 0.18);
}

/* Image fills stage and bleeds past edges */
.slide-image {
  position: absolute;
  inset: 0;
  width: 112%; /* wider than container */
  height: 100%;
  left: -6%; /* center the bleed */
  object-fit: cover;
  display: block;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.18);
}

/* Yellow overlay card */
.slide-card {
  position: absolute;
  top: 45%;
  left: 80%;
  right: clamp(40px, 6vw, 90px);
  transform: translateY(-50%);
  width: clamp(300px, 34%, 520px);
  background: #f6b300;
  border-radius: 6px;
  padding: 28px 32px;
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.25);
  z-index: 2;
}

.slide-card h3 {
  font-size: clamp(20px, 2.2vw, 28px);
  font-weight: 800;
  text-decoration: underline;
  text-underline-offset: 6px;
  margin: 0 0 12px;
  color: #111;
}

.slide-card p {
  font-size: 1rem;
  line-height: 1.6;
  margin: 0 0 16px;
  color: #1a1a1a;
}

.btn {
  position: relative;
  padding: 12px 20px;
  background: #111;
  color: #fff;
  font-weight: 800;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition:
    transform 0.15s ease,
    background 0.2s ease;
}
.btn:hover {
  background: #2c2c2c;
  transform: translateY(-1px);
}

/* small square accent like ref */
.btn::after {
  content: '';
  position: absolute;
  right: -14px;
  bottom: 8px;
  width: 10px;
  height: 10px;
  background: #111;
}

/* ---- Swiper arrows ---- */
.services-swiper :deep(.swiper-button-prev),
.services-swiper :deep(.swiper-button-next) {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #fff;
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.15);
}
.services-swiper :deep(.swiper-button-prev:after),
.services-swiper :deep(.swiper-button-next:after) {
  color: #111;
  font-size: 18px;
  font-weight: 900;
}

/* ---- Responsive ---- */
@media (max-width: 980px) {
  .services-swiper {
    padding-inline: 0;
  }
  .slide-content {
    height: 420px;
  }
  .slide-card {
    position: static;
    transform: none;
    width: auto;
    margin: 14px 16px 0;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.18);
  }
  .services-swiper :deep(.swiper-button-prev),
  .services-swiper :deep(.swiper-button-next) {
    display: none;
  }
}

@media (max-width: 600px) {
  .slide-content {
    height: 360px;
  }
}
</style>
