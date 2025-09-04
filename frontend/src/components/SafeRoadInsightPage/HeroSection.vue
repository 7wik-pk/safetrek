<template>
  <section class="hero">
    <!-- hazard stripes -->
    <div class="hazard hazard--top">
      <img src="../../assets/images/hazard-stripes.svg" alt="" />
    </div>

    <!-- background + overlay -->
    <div class="hero__bg">
      <img src="@/assets/images/SafeRoadInsightPage/hero-image.jpg" alt="Background" />
      <div class="overlay"></div>
    </div>

    <!-- content -->
    <div class="hero__content">
        <SplitText
          text="Safer roads start with insights"
          class-name="forecast-title"
          :delay="100"
          :duration="0.6"
          ease="power3.out"
          split-type="chars"
          :from="{ opacity: 0, y: 40 }"
          :to="{ opacity: 1, y: 0 }"
          :threshold="0.1"
          root-margin="-100px"
          text-align="center"
          @animation-complete="handleAnimationComplete"
        />
    </div>

    <div class="hazard hazard--bottom">
      <img src="../../assets/images/hazard-stripes.svg" alt="" />
    </div>
  </section>

</template>

<style scoped>
.hero {
  position: relative;
  overflow: hidden;
  text-align: center;
}

/* background */
.hero__bg {
  position: absolute;
  inset: 0;
}
.hero__bg img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.hero__bg .overlay {
  position: absolute;
  inset: 0;
  background: rgba(246, 179, 0, 0.65); /* softer yellow */
}

/* hazard stripes */
.hazard {
  position: relative;
  width: 100%;
  z-index: 2;
}
.hazard img {
  width: 100%;
  height: 30px;
  object-fit: cover;
}
.hazard--top {
  margin-bottom: 120px; /* tuck neatly */
}
.hazard--bottom {
  margin-top: -10px;
  transform: rotate(180deg);
}

/* content */
.hero__content {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 2rem;
  justify-content: center;
  flex-direction: column;
  max-width: 1100px;
  margin: 0 auto;
  padding: 60px 20px;
  color: #111;
}

.text h1 {
  font-size: 2.2rem;
  font-weight: 900;
  margin-bottom: 50px;
  text-align: center;
}
.text p {
  font-size: 1rem;
  line-height: 1.5;
  margin-bottom: 20px;
  font-weight: 600;
}

/* button */
.btn-primary {
  background: #111;
  color: #f6b300;
  padding: 10px 24px;
  border: none;
  border-radius: 20px;
  font-weight: 700;
  cursor: pointer;
}
.btn-primary:hover {
  background: #222;
}

/* responsive */
@media (max-width: 768px) {
  .hero__content {
    flex-direction: column;
    text-align: center;
  }
  .sign {
    width: 120px;
  }
}
.forecast-title {
  font-size: 4rem;
  font-weight: 700;
  color: #000;
  letter-spacing: 2px;
  padding-bottom: 50px;
}

</style>
<script setup lang="ts">
import SplitText from "@/assets/VueAnimation/SplitText .vue";

const handleAnimationComplete = () => {
  console.log('All letters have animated!');
};
</script>
