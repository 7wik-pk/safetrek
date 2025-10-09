<template>
  <!-- FULL-WIDTH: Interactive Video -->
  <section class="section-full section-blue">
    <div class="inner">
      <!-- Breadcrumb -->
      <nav aria-label="breadcrumb" class="mb-3">
        <ol class="breadcrumb small mb-0">
          <li class="breadcrumb-item">
            <a href="/" class="text-decoration-none text-warning fw-semibold">Home</a>
          </li>
          <li class="breadcrumb-item active text-secondary" aria-current="page">
            Young Driver Education
          </li>
        </ol>
      </nav>
      <h2 class="section-title">Interactive Hazard Training</h2>
      <p class="section-desc">
        Watch the scenario and click hotspots to learn safe responses in real time.
      </p>
      <InteractiveScenarioSlider />
    </div>
  </section>

  <!-- FULL-WIDTH: Young Driver Cards -->
  <section class="section-full section-yellow">
    <div class="inner">
      <h2 class="section-title">Young Driver Education</h2>
      <p class="section-desc">
        Explore common risks faced by young drivers and how to prevent them.
      </p>
      <YoungDriverEducation />
    </div>
  </section>

  <FooterSection />
</template>

<script setup lang="ts">
import { ref } from "vue"
import YoungDriverEducation from "@/components/EducationPage/YoungDriverEducation.vue"
import InteractiveScenarioSlider from '@/components/EducationPage/InteractiveScenarioSlider.vue'
import FooterSection from '@/components/FooterSection.vue'
import LearningRoadmap from '@/components/EducationPage/LearningRoadmap.vue'

const selectedTopic = ref(null)
function filterCards(topic: string) {
  selectedTopic.value = topic
}
</script>

<style scoped>
/* ===== PAGE WRAPPER ===== */
.page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 60px 24px 20px;
  background: linear-gradient(to bottom, #fffdf7, #f9f7f2);
  color: #222;
  text-align: center;
}

header {
  border-bottom: 6px solid #f4b400 !important;
}

.tracking-wide {
  letter-spacing: 1.5px;
}

.btn-outline-warning {
  border-color: #f4b400 !important;
  color: #444 !important;
  background-color: #fff8dc !important;
}
.btn-outline-warning:hover {
  background-color: #f4b400 !important;
  color: #111 !important;
}


/* ===== SECTIONS ===== */
/* ----- Full-width sections ----- */
.section-full {
  width: 100%;
  padding: 80px 0;
  margin: 0;
}
.section-full .inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

/* Background themes */
.section-blue {
  background: linear-gradient(180deg, #eaf3ff 0%, #ffffff 100%);
}
.section-yellow {
  background: linear-gradient(180deg, #fff9e6 0%, #fffdf7 100%);
}
.section {
  margin-bottom: 100px;
  background: #fffefa;
  padding: 40px 36px;
  border-radius: 18px;
  box-shadow: 0 6px 30px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.section:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 36px rgba(255, 193, 7, 0.15);
}

/* Section headings */
.section-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #111;
  margin-bottom: 10px;
  position: relative;
  text-align: left;
}
.section-title::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -6px;
  width: 60px;
  height: 3px;
  background: #f4b400;
  border-radius: 2px;
}
.section-desc {
  color: #666;
  font-size: 1rem;
  margin-bottom: 32px;
  text-align: left;
}

/* ===== DIFFERENT SECTION THEMES ===== */
.education-section {
  border-left: 6px solid #fbbc05;
}
.video-section {
  background: linear-gradient(to right, #eef7ff, #ffffff);
  border-left: 6px solid #4285f4;
}


/* Responsive */
@media (max-width: 768px) {
  .page {
    padding: 40px 16px 0;
  }
  .section-full {
    padding: 60px 0;
  }
  .section-title {
    font-size: 1.5rem;
  }
}
</style>
