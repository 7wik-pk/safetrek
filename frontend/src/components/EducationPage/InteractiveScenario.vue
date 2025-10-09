<template>
  <div class="card border-0 shadow-sm overflow-hidden" style="border-radius: 14px;">
    <!-- VIDEO -->
    <div class="position-relative bg-dark">
      <video
        :key="videoUrl"
        ref="videoRef"
        autoplay
        muted
        playsinline
        loop
        preload="auto"
        class="w-100 hero-video"
      >
        <source :src="videoUrl" type="video/mp4" />
      </video>


      <!--  this hotspot loop -->
      <div
        v-for="(spot, i) in hotspots"
        :key="'spot-' + i"
        class="hotspot"
        :class="spot.type === 'tip' ? 'hotspot-tip' : 'hotspot-quiz'"
        :style="{ top: spot.top, left: spot.left }"
        @click="togglePopup(i)"
      ></div>

      <!--  Add popups too -->
      <transition-group name="fade" tag="div">
        <div
          v-for="(spot, i) in hotspots"
          :key="'popup-' + i"
          v-show="spot.show"
          ref="popupRefs"
          class="popup"
          :class="spot.type === 'tip' ? 'popup-tip' : 'popup-quiz'"
          :style="{ top: spot.popupTop, left: spot.popupLeft }"
        >
          <button class="close-btn" @click.stop="spot.show = false">×</button>

          <div v-if="spot.type === 'tip'">
            <p v-html="spot.text"></p>
          </div>

          <div v-else>
            <p><b>{{ spot.question }}</b></p>
            <div
              v-for="(opt, j) in spot.options"
              :key="'opt-' + j"
              class="quiz-option"
            >
              <button
                :class="{
              correct: spot.selected === j && j === spot.answer,
              wrong: spot.selected === j && j !== spot.answer
            }"
                @click.stop="selectAnswer(i, j)"
              >
                {{ opt }}
              </button>
            </div>
            <p v-if="spot.selected !== null">
              <b>{{ spot.selected === spot.answer ? '✅ Correct!' : '❌ Try again!' }}</b>
            </p>
          </div>
        </div>
      </transition-group>
    </div>

    <!-- DESCRIPTION -->
    <div class="card-body text-center bg-light">
      <h2 class="fw-bold text-primary mb-3">{{ title }}</h2>
      <p class="text-muted fs-5 mb-4">{{ description }}</p>

      <hr class="my-4" />

      <!-- INFO -->
      <div class="row text-center gy-3">
        <div class="col-md-4" v-for="(item, i) in info" :key="i">
          <i :class="['fs-2 text-info', item.icon]"></i>
          <h6 class="fw-semibold mt-2 text-dark">{{ item.label }}</h6>
          <p class="text-muted mb-0">{{ item.value }}</p>
        </div>
      </div>

      <hr class="my-4" />

      <!-- TAGS -->
      <div class="d-flex flex-wrap justify-content-center gap-2 mb-4">
        <span v-for="(t, i) in tags" :key="i" class="badge rounded-pill bg-info-subtle text-info px-3 py-2">
          {{ t }}
        </span>
      </div>
    </div>
  </div>

</template>

<script setup>
import { ref, nextTick, watch } from "vue"

const props = defineProps({
  videoUrl: String,
  hotspots: Array,
  title: String,
  description: String,
  info: Array,
  tags: Array
})

const videoRef = ref(null)
const popupRefs = ref([])

// Always use the hotspots from props directly
const hotspots = ref([])

watch(
  () => props.hotspots,
  (newVal) => {
    hotspots.value = newVal ? JSON.parse(JSON.stringify(newVal)) : []
  },
  { immediate: true, deep: true }
)

// --- interactions ---
async function togglePopup(i) {
  const spot = hotspots.value[i]
  if (!spot) return
  spot.show = !spot.show
  await nextTick()

  const popupEl = popupRefs.value[i]
  const videoBox = videoRef.value?.getBoundingClientRect()
  if (!popupEl || !videoBox) return

  const popupRect = popupEl.getBoundingClientRect()
  let adjustY = 0,
    adjustX = 0
  if (popupRect.top < videoBox.top) adjustY = 20
  if (popupRect.bottom > videoBox.bottom) adjustY = -20
  if (popupRect.right > videoBox.right) adjustX = -20
  if (popupRect.left < videoBox.left) adjustX = 20
  popupEl.style.transform = `translate(calc(-50% + ${adjustX}px), calc(-50% + ${adjustY}px))`

  if (spot.type === "tip" && spot.show) {
    setTimeout(() => (spot.show = false), 5000)
  }
}

function selectAnswer(i, j) {
  const spot = hotspots.value[i]
  if (spot && spot.type === "quiz") spot.selected = j
}

// --- play video on prop change ---
watch(
  () => props.videoUrl,
  async () => {
    if (videoRef.value) {
      videoRef.value.load()
      await nextTick()
      try {
        await videoRef.value.play()
      } catch {}
    }
  },
  { immediate: true }
)
console.log("🔥 Received hotspots:", props.hotspots)
</script>

<style scoped>
.hero-video {
  height: 60vh;
  object-fit: cover;
  border-bottom: 4px solid #00b4d8;
}
.btn-gradient {
  background: linear-gradient(90deg, #00b4d8, #0096c7);
  border: none;
  color: #fff;
  border-radius: 12px;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 4px 12px rgba(0, 180, 216, 0.3);
}
.btn-gradient:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 180, 216, 0.4);
}
.position-relative.bg-dark {
  position: relative;
  overflow: hidden;
}

/* 🔹 Force video behind */
.hero-video {
  position: relative;
  z-index: 1;
  pointer-events: none; /* prevent blocking hotspot clicks */
}

/* 🔹 Hotspots above */
.hotspot {
  position: absolute;
  z-index: 5;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  transform: translate(-50%, -50%);
  transition: transform 0.2s;
  animation: pulse 1.5s infinite;
}

/* Add bright debug color temporarily */
.hotspot-tip {
  background: rgba(255, 0, 0, 0.85);
  box-shadow: 0 0 12px rgba(255, 0, 0, 0.6);
}
.hotspot-quiz {
  background: rgba(0, 200, 0, 0.85);
  box-shadow: 0 0 12px rgba(0, 255, 0, 0.6);
}

/* 🔹 Popups even higher */
.popup {
  position: absolute;
  z-index: 10;
}
.video-overlay-debug {
  position: absolute;
  inset: 0;
  border: 4px dashed yellow;
  z-index: 20;
  pointer-events: none;
}
/* high-contrast popup styles */
.popup-tip {
  background: linear-gradient(180deg, #ff4d4d, #b30000);
  border: 2px solid #ff9999;
  color: #fff;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.25);
}

.popup-quiz {
  background: linear-gradient(180deg, #00994d, #007a3d);
  border: 2px solid #33ff99;
  color: #fff;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.25);
}

/* Optional: make text easier to read */
.popup p {
  font-size: 15px;
  line-height: 1.6;
  color: #fff;
}
.quiz-option {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 8px;
}

/* Default button */
.quiz-option button {
  background: #f4f7fa;
  color: #222;
  border: 2px solid #d0e3eb;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 0.95rem;
  text-align: left;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s ease;
}

/* Hover effect */
.quiz-option button:hover {
  background: #e3f5ff;
  border-color: #00b4d8;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 180, 216, 0.2);
}

/* Selected states */
.correct {
  background-color: #e7fbe8 !important;
  border-color: #28a745 !important;
  color: #155724 !important;
  box-shadow: 0 0 10px rgba(40, 167, 69, 0.4);
  font-weight: 600;
}

.wrong {
  background-color: #fde8e8 !important;
  border-color: #dc3545 !important;
  color: #721c24 !important;
  box-shadow: 0 0 10px rgba(220, 53, 69, 0.4);
  font-weight: 600;
}

/* Result feedback text */
.popup p b {
  display: inline-block;
  margin-top: 6px;
  font-weight: 600;
  color: #222;
}

.popup {
  animation: fadeIn 0.3s ease forwards;
  border-radius: 10px;
  padding: 16px 20px;
  backdrop-filter: blur(2px);
}
@keyframes fadeIn {
  from { opacity: 0; transform: translate(-50%, -60%); }
  to { opacity: 1; transform: translate(-50%, -50%); }
}


</style>
