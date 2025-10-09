<template>
  <div class="overlay-container">
    <div
      v-for="(spot, i) in data"
      :key="i"
      class="hotspot"
      :class="spot.type"
      :style="{ top: spot.top, left: spot.left }"
      @click="toggle(i)"
    ></div>

    <transition name="fade">
      <div v-if="activeSpot !== null" class="popup" :class="data[activeSpot].type">
        <button class="close-btn" @click="activeSpot = null">×</button>

        <!-- Tip -->
        <div v-if="data[activeSpot].type === 'tip'">
          <p v-html="data[activeSpot].text"></p>
        </div>

        <!-- Quiz -->
        <div v-else>
          <p><b>{{ data[activeSpot].question }}</b></p>
          <div
            v-for="(opt, j) in data[activeSpot].options"
            :key="j"
            class="quiz-option"
          >
            <button
              @click.stop="selectAnswer(j)"
              :class="{
                correct: selected === j && j === data[activeSpot].answer,
                wrong: selected === j && j !== data[activeSpot].answer,
              }"
            >
              {{ opt }}
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from "vue"
const props = defineProps({ data: Array })
const activeSpot = ref(null)
const selected = ref(null)

function toggle(i) {
  activeSpot.value = activeSpot.value === i ? null : i
  selected.value = null
}
function selectAnswer(i) {
  selected.value = i
}
</script>

<style scoped>
.overlay-container {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 2;
}
.hotspot {
  position: absolute;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  cursor: pointer;
  pointer-events: all;
  animation: pulse 1.5s infinite;
}
.hotspot.tip {
  background: rgba(255, 0, 0, 0.8);
}
.hotspot.quiz {
  background: rgba(0, 255, 0, 0.8);
}
.popup {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0, 0, 0, 0.75);
  color: white;
  padding: 14px;
  border-radius: 10px;
  max-width: 280px;
  z-index: 5;
  pointer-events: all;
}
.quiz-option button {
  width: 100%;
  background: #333;
  color: #fff;
  border: none;
  margin: 5px 0;
  padding: 6px;
  border-radius: 6px;
}
.correct {
  background: #2ecc71 !important;
}
.wrong {
  background: #e74c3c !important;
}
.close-btn {
  position: absolute;
  top: 4px;
  right: 8px;
  background: none;
  color: white;
  border: none;
  cursor: pointer;
}
@keyframes pulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); }
  50% { transform: translate(-50%, -50%) scale(1.15); }
}
.fade-enter-active,
.fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from,
.fade-leave-to { opacity: 0; }
</style>
