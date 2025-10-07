<template>
  <main class="page">
    <!-- PAGE TITLE -->
    <header class="page-header">
      <h1 class="main-title">Education</h1>
      <p class="subtitle">
        Learn key safe-driving principles through interactive lessons and scenarios.
      </p>
    </header>

    <!-- SECTION: Flashcards -->
    <section class="section education-section">
      <h2 class="section-title">Young Driver Education</h2>
      <p class="section-desc">
        Explore common risks faced by young drivers and how to prevent them.
      </p>
      <YoungDriverEducation />
    </section>

    <!-- SECTION: Interactive Video -->
    <section class="section video-section">
      <h2 class="section-title">Interactive Hazard Training</h2>
      <p class="section-desc">
        Watch the scenario and click hotspots to learn safe responses in real time.
      </p>
      <InteractiveVideo />
    </section>
  </main>
</template>

<script setup lang="ts">
import YoungDriverEducation from "@/components/EducationPage/YoungDriverEducation.vue"
import InteractiveVideo from "@/components/EducationPage/InteractiveVideo.vue"
</script>

<style scoped>
/* ===== PAGE WRAPPER ===== */
.page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 40px 24px 80px;
  background: linear-gradient(to bottom, #fffdf7, #f9f7f2);
  font-family: "Inter", sans-serif;
  color: #222;
}

/* ===== PAGE HEADER ===== */
.page-header {
  text-align: center;
  margin-bottom: 60px;
}
.main-title {
  font-size: 2.8rem;
  font-weight: 800;
  color: #f4b400; /* warm yellow accent */
  margin-bottom: 12px;
}
.subtitle {
  font-size: 1.1rem;
  color: #555;
  max-width: 700px;
  margin: 0 auto;
  line-height: 1.6;
}

/* ===== SECTIONS ===== */
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

/* ===== SECTION TITLES ===== */
.section-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #111;
  margin-bottom: 10px;
  position: relative;
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
  margin-bottom: 24px;
}

/* ===== DIFFERENT SECTION THEMES ===== */
.education-section {
  border-left: 6px solid #fbbc05;
}
.video-section {
  background: linear-gradient(to right, #eef7ff, #ffffff);
  border-left: 6px solid #4285f4;
}

/* ===== RESPONSIVE ===== */
@media (max-width: 768px) {
  .page {
    padding: 20px 16px 60px;
  }
  .main-title {
    font-size: 2.2rem;
  }
  .section {
    padding: 24px;
  }
}
</style>
