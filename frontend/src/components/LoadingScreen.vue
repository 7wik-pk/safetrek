<template>
  <!-- Teleport to <body> so no parent can clip it -->
  <teleport to="body">
    <transition name="fade">
      <div v-if="show" class="loader-overlay" role="status" aria-live="polite">
        <div class="card">
          <div class="hazard" aria-hidden="true"></div>

          <div class="content">
            <!-- LEFT: the road work sign -->
            <div class="sign">
              <img v-if="signSrc" :src="signSrc" alt="Road Work sign" />
              <div v-else class="sign-fallback">ROAD<br />WORK</div>
            </div>

            <!-- RIGHT: title + progress -->
            <div class="right">
              <h2 class="title">{{ title }}</h2>
              <div class="bar" :aria-label="`Loading ${progress}%`">
                <div class="bar__fill" :style="{ width: progress + '%' }"></div>
                <div class="bar__shine"></div>
              </div>
              <p class="hint">{{ hint }}</p>
            </div>
          </div>

          <div class="hazard" aria-hidden="true"></div>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup>
const props = defineProps({
  show: { type: Boolean, default: false },
  progress: { type: Number, default: 30 },
  title: { type: String, default: 'Loading SafeTrek' },
  hint: { type: String, default: 'Please wait...' },
  signSrc: { type: String, default: '' },
})
</script>

<style scoped>
/* FULLSCREEN overlay */
.loader-overlay {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100svh;
  display: grid;
  place-items: center;
  background: #ffbb00;
  z-index: 999999;
}

/* Card */
.card {
  width: 80%;
  min-width: 400px;
  background: #2a2f39;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.45);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.hazard {
  height: clamp(22px, 5vw, 44px);
  background: repeating-linear-gradient(
    -45deg,
    #111 0 clamp(11px, 2.7vw, 24px),
    #f6b300 clamp(11px, 2.7vw, 24px) clamp(22px, 5.4vw, 48px)
  );
}

.content {
  display: grid;
  grid-template-columns: clamp(140px, 20vw, 220px) 1fr;
  gap: clamp(12px, 2.2vw, 24px);
  align-items: center;
  padding: clamp(16px, 2.6vw, 28px);
  background: linear-gradient(180deg, #2a2f39 0%, #1f232c 100%);
}

/* SIGN */
.sign {
  display: grid;
  place-items: center;
}
.sign img {
  width: clamp(110px, 18vw, 200px);
  height: auto;
  display: block;
  filter: drop-shadow(0 6px 16px rgba(0, 0, 0, 0.6));
}
.sign-fallback {
  width: clamp(110px, 18vw, 200px);
  height: clamp(110px, 18vw, 200px);
  background: #f6b300;
  color: #111;
  font-weight: 900;
  text-align: center;
  display: grid;
  place-items: center;
  border-radius: 12px;
  transform: rotate(45deg);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.5);
}
.sign-fallback > * {
  transform: rotate(-45deg);
}

/* TEXT + BAR */
.title {
  color: #ffd770;
  margin: 0 0 12px;
  font-weight: 800;
  font-size: clamp(18px, 2.5vw, 28px);
}
.hint {
  color: #cfd6e4;
  opacity: 0.72;
  margin-top: 8px;
  font-size: clamp(11px, 1.6vw, 13px);
}

.bar {
  position: relative;
  height: 18px;
  border-radius: 4px;
  background: #0f1116;
  border: 1px solid rgba(255, 255, 255, 0.12);
  overflow: hidden;
}
.bar__fill {
  height: 100%;
  background: #f6b300;
  transition: width 0.3s ease;
}
.bar__shine {
  position: absolute;
  inset: 0;
  background: linear-gradient(120deg, transparent, rgba(255, 255, 255, 0.25), transparent);
  animation: shine 1.3s linear infinite;
  mix-blend-mode: soft-light;
}
@keyframes shine {
  from {
    transform: translateX(-100%);
  }
  to {
    transform: translateX(100%);
  }
}

/* Fade in/out */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Small screens: stack */
@media (max-width: 560px) {
  .content {
    grid-template-columns: 1fr;
    text-align: center;
  }
}
</style>
