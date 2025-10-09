<template>
  <section class="interactive-video-section py-5">
    <div class="container">
      <!-- WRAPPER CARD -->
      <div class="card border-0 shadow-sm overflow-hidden" style="border-radius: 14px;">
        <!-- HERO VIDEO -->
        <div class="position-relative bg-dark">
          <video
            ref="videoRef"
            autoplay
            muted
            playsinline
            loop
            preload="auto"
            class="w-100 hero-video"
          >
            <source :src="videoUrl" type="video/mp4" />
            Your browser does not support the video tag.
          </video>

          <!-- HOTSPOTS -->
          <div
            v-for="(spot, i) in hotspots"
            :key="'spot-' + i"
            class="hotspot"
            :class="spot.type === 'tip' ? 'hotspot-tip' : 'hotspot-quiz'"
            :style="{ top: spot.top, left: spot.left }"
            @click="togglePopup(i)"
          ></div>

          <!-- POPUPS -->
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

              <!-- Tip -->
              <div v-if="spot.type === 'tip'">
                <p v-html="spot.text"></p>
              </div>

              <!-- Quiz -->
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

        <!-- DESCRIPTION BELOW -->
        <div class="card-body text-center bg-light">
          <h2 class="fw-bold text-primary mb-3">Rainy-Day Hazard Perception</h2>
          <p class="text-muted fs-5 mb-4">
            When rain hits the road, every second counts. This scenario tests how quickly
            you can identify hazards — from slippery turns to hidden puddles.
            Learn, react, and master wet-weather driving like a pro 🌧️.
          </p>

          <hr class="my-4" />

          <!-- INFO ROW -->
          <div class="row text-center gy-3">
            <div class="col-md-4">
              <i class="bi bi-cloud-rain fs-2 text-info"></i>
              <h6 class="fw-semibold mt-2 text-dark">Weather</h6>
              <p class="text-muted mb-0">Heavy Rain</p>
            </div>
            <div class="col-md-4">
              <i class="bi bi-eye fs-2 text-info"></i>
              <h6 class="fw-semibold mt-2 text-dark">Visibility</h6>
              <p class="text-muted mb-0">Low (200 m)</p>
            </div>
            <div class="col-md-4">
              <i class="bi bi-speedometer2 fs-2 text-info"></i>
              <h6 class="fw-semibold mt-2 text-dark">Risk Level</h6>
              <p class="text-muted mb-0">High</p>
            </div>
          </div>

          <hr class="my-4" />

          <!-- TAGS -->
          <div class="d-flex flex-wrap justify-content-center gap-2 mb-4">
            <span class="badge rounded-pill bg-info-subtle text-info px-3 py-2">Hydroplaning</span>
            <span class="badge rounded-pill bg-info-subtle text-info px-3 py-2">Wet Roads</span>
            <span class="badge rounded-pill bg-info-subtle text-info px-3 py-2">Brake Distance</span>
            <span class="badge rounded-pill bg-info-subtle text-info px-3 py-2">Reduced Grip</span>
          </div>
        </div>

      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, nextTick } from "vue"
import videoUrl from "@/assets/videos/hazard_video.mp4"

const videoRef = ref(null)
const popupRefs = ref([])

const hotspots = ref([
  { top: "25%", left: "55%", type: "tip", popupTop: "20%", popupLeft: "60%", text: "☔ <b>Visibility Tip:</b> Always turn on headlights and wipers during rain to stay visible.", show: false },
  { top: "70%", left: "50%", type: "tip", popupTop: "65%", popupLeft: "55%", text: "🚘 <b>Keep Distance:</b> Rain makes roads slippery. Leave at least a 4-second gap.", show: false },
  { top: "50%", left: "35%", type: "quiz", popupTop: "45%", popupLeft: "40%", question: "If your car starts to hydroplane, what should you do?", options: ["Brake hard and steer sharply", "Ease off the accelerator and steer straight", "Accelerate quickly to regain traction"], answer: 1, selected: null, show: false },
  { top: "80%", left: "65%", type: "tip", popupTop: "75%", popupLeft: "70%", text: "🌊 <b>Flooded Roads:</b> Avoid driving through standing water. Even 15 cm can stall your car.", show: false },
  { top: "40%", left: "75%", type: "quiz", popupTop: "35%", popupLeft: "80%", question: "When visibility becomes very poor, what’s the safest action?", options: ["Turn on hazard lights and keep driving slowly", "Pull over safely and wait for conditions to improve", "Speed up to get out faster"], answer: 1, selected: null, show: false },
])

async function togglePopup(i) {
  const spot = hotspots.value[i]
  if (!spot) return
  spot.show = !spot.show
  await nextTick()
  const popupEl = popupRefs.value[i]
  const videoBox = videoRef.value?.getBoundingClientRect()
  if (!popupEl || !videoBox) return
  const popupRect = popupEl.getBoundingClientRect()
  let adjustY = 0, adjustX = 0
  if (popupRect.top < videoBox.top) adjustY = 20
  if (popupRect.bottom > videoBox.bottom) adjustY = -20
  if (popupRect.right > videoBox.right) adjustX = -20
  if (popupRect.left < videoBox.left) adjustX = 20
  popupEl.style.transform = `translate(calc(-50% + ${adjustX}px), calc(-50% + ${adjustY}px))`
  if (spot.type === "tip" && spot.show) setTimeout(() => (spot.show = false), 5000)
}

function selectAnswer(i, j) {
  const spot = hotspots.value[i]
  if (spot && spot.type === "quiz") spot.selected = j
}
</script>

<style scoped>
.hero-video {
  height: 60vh;
  object-fit: cover;
}

/* Hotspots */
.hotspot {
  position: absolute;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  transform: translate(-50%, -50%);
  transition: transform 0.2s;
  z-index: 5;
  animation: pulse 1.5s infinite;
}
.hotspot:hover { transform: translate(-50%, -50%) scale(1.15); }
.hotspot-tip  { background: rgba(255, 0, 0, 0.85); box-shadow: 0 0 12px rgba(255, 0, 0, 0.6); }
.hotspot-quiz { background: rgba(0, 200, 0, 0.85); box-shadow: 0 0 12px rgba(0, 255, 0, 0.6); }

/* Popups */
.popup {
  position: absolute;
  transform: translate(-50%, -50%);
  color: #fff;
  padding: 12px 16px;
  border-radius: 10px;
  font-size: 14px;
  max-width: 260px;
  line-height: 1.5;
  z-index: 10;
  opacity: 0;
  animation: fadeIn 0.3s ease forwards;
}
.popup-tip  { background: rgba(255, 0, 0, 0.85); border: 2px solid #ff5050; }
.popup-quiz { background: rgba(0, 150, 0, 0.85); border: 2px solid #00ff66; }

/* Quiz Buttons */
.quiz-option button {
  display: block;
  width: 100%;
  margin: 4px 0;
  padding: 6px;
  border: none;
  border-radius: 6px;
  background: #333;
  color: #fff;
  cursor: pointer;
  transition: background 0.3s;
}
.quiz-option button:hover { background: #555; }
.correct { background-color: #2ecc71 !important; }
.wrong   { background-color: #e74c3c !important; }

.btn-gradient {
  background: linear-gradient(90deg, #a9d800, #c78800);
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

/* Animations */
@keyframes fadeIn { from { opacity: 0; transform: translate(-50%, -60%); } to { opacity: 1; transform: translate(-50%, -50%); } }
@keyframes pulse  { 0%,100% { transform: translate(-50%, -50%) scale(1); } 50% { transform: translate(-50%, -50%) scale(1.15); } }
</style>
