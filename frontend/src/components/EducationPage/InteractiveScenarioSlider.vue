<template>
  <section class="hazard-slider-section py-5">
    <div class="container">
      <h1 class="text-center mb-4 fw-bold text-primary">Interactive Driving Scenarios</h1>

      <!-- CAROUSEL -->
      <div id="hazardCarousel" class="carousel slide" data-bs-ride="carousel">
        <div class="carousel-inner">

          <!-- SCENARIO 1 -->
          <div class="carousel-item active">
            <InteractiveScenario
              :video-url="videos.rain"
              :hotspots="rainHotspots"
              title="Rainy-Day Hazard Perception"
              description="Learn how to handle slippery roads, reduced visibility, and hydroplaning during heavy rain."
              :info="[
    { icon: 'bi-cloud-rain', label: 'Weather', value: 'Heavy Rain' },
    { icon: 'bi-eye', label: 'Visibility', value: 'Low (200 m)' },
    { icon: 'bi-speedometer2', label: 'Risk Level', value: 'High' }
  ]"
              :tags="['Hydroplaning', 'Wet Roads', 'Brake Distance', 'Reduced Grip']"
            />

          </div>

          <!-- SCENARIO 2 -->
          <div class="carousel-item">
            <InteractiveScenario
              :video-url="videos.night"
              :hotspots="nightHotspots"
              title="Night Driving Awareness"
              description="Spot hidden dangers and manage glare at night."
              :info="[
                { icon: 'bi-moon-stars', label: 'Time', value: 'Night' },
                { icon: 'bi-lightning', label: 'Visibility', value: 'Medium' },
                { icon: 'bi-exclamation-triangle', label: 'Risk Level', value: 'Moderate' }
              ]"
              :tags="['Glare', 'Headlights', 'Overtaking', 'Pedestrians']"
            />
          </div>

          <!-- SCENARIO 3 -->
          <div class="carousel-item">
            <InteractiveScenario
              :video-url="videos.fog"
              :hotspots="fogHotspots"
              title="Foggy Conditions Challenge"
              description="Drive through dense fog while managing reduced visibility and unexpected turns."
              :info="[
                { icon: 'bi-cloud-fog', label: 'Weather', value: 'Thick Fog' },
                { icon: 'bi-eye-slash', label: 'Visibility', value: 'Very Low (100 m)' },
                { icon: 'bi-thermometer', label: 'Risk Level', value: 'High' }
              ]"
              :tags="['Fog Lights', 'Low Beam', 'Increased Gap']"
            />
          </div>
          <!-- SCENARIO 4 -->
          <div class="carousel-item">
            <InteractiveScenario
              :video-url="videos.speeding"
              :hotspots="speedingHotspots"
              title="Speeding Awareness"
              description="See how high speeds affect control, reaction times, and braking distance. Learn why every extra km/h matters."
              :info="[
      { icon: 'bi-speedometer2', label: 'Speed', value: 'High (100–120 km/h)' },
      { icon: 'bi-exclamation-triangle', label: 'Risk Level', value: 'Very High' },
      { icon: 'bi-stopwatch', label: 'Reaction Time', value: 'Reduced' }
    ]"
              :tags="['Braking Distance', 'Overtaking', 'Speed Limits', 'Reaction Time']"
            />
          </div>
        </div>

        <!-- CONTROLS -->
        <button class="carousel-control-prev" type="button" data-bs-target="#hazardCarousel" data-bs-slide="prev">
          <span class="carousel-control-prev-icon"></span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#hazardCarousel" data-bs-slide="next">
          <span class="carousel-control-next-icon"></span>
        </button>

      </div>
    </div>
  </section>
</template>

<script setup>
import InteractiveScenario from "@/components/EducationPage/InteractiveScenario.vue"

// 🎬 Video sources
const videos = {
  rain: new URL("@/assets/videos/hazard_video.mp4", import.meta.url).href,
  night: new URL("@/assets/videos/nightDriving.mp4", import.meta.url).href,
  fog: new URL("@/assets/videos/fog.mp4", import.meta.url).href,
  speeding: new URL("@/assets/videos/speeding.mp4", import.meta.url).href,
}

// 💧 RAINY DAY HOTSPOTS
const rainHotspots = [
  {
    top: "25%",
    left: "45%",
    type: "tip",
    popupTop: "20%",
    popupLeft: "60%",
    text: "☔ <b>Visibility Tip:</b> Turn on headlights and wipers early when it starts raining.",
    show: false,
  },
  {
    top: "70%",
    left: "50%",
    type: "tip",
    popupTop: "65%",
    popupLeft: "55%",
    text: "🚘 <b>Keep Distance:</b> Wet roads double braking distance.",
    show: false,
  },
  {
    top: "50%",
    left: "35%",
    type: "quiz",
    popupTop: "45%",
    popupLeft: "40%",
    question: "If your car hydroplanes, what should you do?",
    options: [
      "Brake hard and steer sharply",
      "Ease off accelerator and steer straight",
      "Accelerate to regain traction",
    ],
    answer: 1,
    selected: null,
    show: false,
  },
]

// 🌙 NIGHT DRIVING HOTSPOTS
const nightHotspots = [
  {
    top: "45%",
    left: "65%",
    type: "tip",
    popupTop: "40%",
    popupLeft: "70%",
    text: "💡 <b>Headlight Tip:</b> Use low beams around traffic to avoid glare.",
    show: false,
  },
  {
    top: "60%",
    left: "45%",
    type: "quiz",
    popupTop: "55%",
    popupLeft: "50%",
    question: "What should you do if you’re blinded by oncoming lights?",
    options: ["Close your eyes briefly", "Look to the left edge", "Turn on high beams"],
    answer: 1,
    selected: null,
    show: false,
  },
]

// 🌫️ FOG HOTSPOTS
const fogHotspots = [
  {
    top: "65%",
    left: "50%",
    type: "tip",
    popupTop: "60%",
    popupLeft: "55%",
    text: "🌫️ <b>Fog Safety:</b> Use fog lights, never high beams.",
    show: false,
  },
  {
    top: "40%",
    left: "75%",
    type: "quiz",
    popupTop: "35%",
    popupLeft: "80%",
    question: "If you can’t see 50m ahead, what should you do?",
    options: ["Maintain speed", "Pull over safely", "Turn on high beam"],
    answer: 1,
    selected: null,
    show: false,
  },
]
const speedingHotspots = [
  {
    top: "50%",
    left: "40%",
    type: "tip",
    popupTop: "45%",
    popupLeft: "45%",
    text: "🏎️ <b>Speed Tip:</b> Speeding reduces reaction time — every extra 10 km/h dramatically increases stopping distance.",
    show: false,
  },
  {
    top: "65%",
    left: "60%",
    type: "quiz",
    popupTop: "60%",
    popupLeft: "65%",
    question: "At 100 km/h, how long does it take to stop on a dry road?",
    options: ["40 m", "70 m", "100 m"],
    answer: 2,
    selected: null,
    show: false,
  },
  {
    top: "75%",
    left: "35%",
    type: "tip",
    popupTop: "70%",
    popupLeft: "40%",
    text: "🚨 <b>Awareness:</b> Speeding increases both crash severity and the chance of fatal injuries.",
    show: false,
  },
]

</script>


<style scoped>
.hazard-slider-section {
  background: linear-gradient(180deg, #f8fbfc 0%, #e9f7fa 100%);
}
.carousel-item {
  transition: transform 0.8s ease-in-out;
}
</style>
