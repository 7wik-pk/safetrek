<script setup>
import ctaBg from "/img/bg/choose-02.jpg"
</script>

<template>
  <section
    class="cta-section"
    :style="{ backgroundImage: `url(${ctaBg})` }"
  >
    <div class="cta-overlay"></div>
    <div class="cta-container">
      <div class="cta-text">
        <span class="cta-subtitle">TURN DATA INTO ACTION</span>
        <h2>Quality & Integrity Across Disciplines
        </h2>
        <p>
          Discover how SafeTrek's comprehensive data platform serves diverse professional needs.
        </p>
      </div>
      <div class="cta-action">
        <router-link class="cta-btn" to="/stats-trends">Find out more</router-link>
      </div>
    </div>
  </section>
</template>

<style scoped>
.cta-section {
  position: relative;
  background-size: cover;
  background-position: center;
  padding: 80px 20px;
  color: #fff;
  margin: 60px 0;
  border-radius: 6px;
  overflow: hidden;
}

.cta-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.65);
  z-index: 1;
}

.cta-container {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  gap: 40px;
}

.cta-text {
  max-width: 700px;
}
.cta-subtitle {
  font-size: 0.9rem;
  letter-spacing: 1px;
  color: #f6b300;
  display: block;
  margin-bottom: 12px;
  font-weight: 600;
}
.cta-text h2 {
  font-size: clamp(26px, 4vw, 42px);
  font-weight: 800;
  margin-bottom: 16px;
}
.cta-text p {
  font-size: 1rem;
  line-height: 1.6;
  max-width: 620px;
}.cta-btn {
   position: relative;
   padding: 14px 32px;
   background: #f6b300;     /* base yellow */
   color: #111;
   border: none;
   border-radius: 4px;
   font-weight: 800;
   font-size: 1rem;
   cursor: pointer;
   overflow: hidden;        /* keep fill inside button */
   isolation: isolate;      /* new stacking context */
   transition: color .35s ease, transform .2s ease;
   will-change: transform;
 }

/* small white dot (starts bottom-right, but centered for expansion) */
.cta-btn::after {
  content: "";
  position: absolute;
  left: 50%;
  top: 50%;
  width: 15px;
  height: 10px;
  background: #fff;
  border-radius: 50%;
  z-index: -1;
  transform: translate(-50%, -50%) scale(0.05); /* tiny dot in center */
  transform-origin: center;
  transition: transform .45s cubic-bezier(.22, .61, .36, 1);
  will-change: transform;
}

/* hover/focus expands the white circle to cover button */
.cta-btn:hover,
.cta-btn:focus-visible {
  color: #111;  /* still dark text */
  transform: translateY(-2px);
}

.cta-btn:hover::after,
.cta-btn:focus-visible::after {
  transform: translate(-50%, -50%) scale(15); /* expands evenly */
}

.cta-btn:active {
  transform: translateY(0);
}

/* Responsive */
@media (max-width: 860px) {
  .cta-container {
    flex-direction: column;
    text-align: center;
  }
  .cta-action {
    margin-top: 20px;
  }
}
@media (prefers-reduced-motion: reduce) {
  .cta-btn,
  .cta-btn::after {
    transition: none;
  }
}
</style>
