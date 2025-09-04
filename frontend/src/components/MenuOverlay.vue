<template>
  <teleport to="body">
    <transition name="fade">
      <div
        v-show="open"
        class="overlay"
        role="dialog"
        aria-modal="true"
        @click="emit('close')"
      >
        <div class="panel" @click.stop>
          <div class="panel__header">
            <span class="panel__title">Menu</span>
          </div>

          <nav class="links">
            <router-link to="/" class="link" @click="emit('close')">Home</router-link>
            <router-link to="/safe-road-insight" class="link" @click="emit('close')">
              Safer Road Insight
            </router-link>
            <!-- Add more links as needed in the future interation-->
          </nav>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup>
const props = defineProps({
  open: { type: Boolean, default: false }
})

const emit = defineEmits(['close'])
</script>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(0, 0, 0, 0.45);
  display: grid;
  place-items: start end;
  padding: 12px;
}

.panel {
  width: min(92vw, 360px);
  background: #111;
  color: #fff4c0;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0,0,0,.5);
  padding: 16px;
  border: 1px solid rgba(255,255,255,.08);
}

.panel__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.panel__title { font-weight: 800; letter-spacing: .02em; }

.close {
  appearance: none;
  background: transparent;
  border: none;
  color: #fff4c0;
  font-size: 20px;
  cursor: pointer;
}

.links { display: grid; gap: 10px; margin-top: 4px; }

.link {
  display: block;
  padding: 10px 12px;
  border-radius: 10px;
  text-decoration: none;
  color: #ffd05a;
  background: rgba(255,255,255,.03);
  border: 1px solid rgba(255,255,255,.05);
}
.link:hover { background: rgba(255,255,255,.08); }

.fade-enter-active, .fade-leave-active { transition: opacity .16s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
