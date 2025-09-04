<script setup>
import missionImage from '@/assets/images/Homepage/our-mission01.jpg'
import missionFrame from '@/assets/images/Homepage/our-mission02.svg'
import noteTape     from '@/assets/images/Homepage/note_tape.svg'

import { ref } from 'vue'

const showNotice = ref(false)

function showComingSoon() {
  showNotice.value = true
}

</script>

<template>
  <section class="mission">
    <div class="mission__content container">
      <!-- left: taped image -->
      <div class="mission__image">
        <!-- frame -->
        <img :src="missionFrame" alt="" class="mission-frame" />

        <!-- tape -->
        <img :src="noteTape" alt="Note tape" class="note-tape" />

        <!-- photo -->
        <img :src="missionImage" alt="Our Mission" class="photo" />
      </div>

      <!-- right: text -->
      <div class="mission__text">
        <h2>Our Mission</h2>
        <p>
          Our mission is to equip city planners and
          policymakers with the tools needed to make data-driven proactive road safety decisions By transforming fragmented crash demographic and socio-economic data into clear location-specific insights we enable smarter planning and more equitable interventions
        </p>
        <button class="btn-primary coming-soon" @click="showComingSoon">Learn more</button>

        <div v-if="showNotice" class="coming-soon-box">
          This section is coming soon. Stay tuned!
        </div>
      </div>
    </div>
  </section>

  <div class="footer-divider">
    <div class="footer-divider__inner"></div>
  </div>
</template>

<style scoped>
.mission {
  position: relative;
  background: linear-gradient(180deg, #f6b300 0%, #e5a100 100%);
  padding: 70px 20px;
}

/* layout */
.mission__content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  align-items: center;
  max-width: 1100px;
  margin: 0 auto;
}

/* image group */
.mission__image {
  position: relative;
  display: inline-block;
}
.mission-frame {
  position: absolute;
  top: -30px;
  left: -30px;
  width: 100%;
  height: auto;
  z-index: 0;
}
.note-tape {
  position: absolute;
  top: -60px;
  left: -30px;
  width: 150px;
  transform: rotate(5deg);
  z-index: 2;
}
.photo {
  position: relative;
  display: block;
  width: 100%;
  border-radius: 8px;
  border: 10px solid #111;
  box-shadow: 0 12px 30px rgba(0,0,0,.35);
  z-index: 1;
}

/* text */
.mission__text h2 {
  font-size: 2rem;
  font-weight: 900;
  margin-bottom: 16px;
  color: #111;
}
.mission__text p {
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 20px;
  color: #222;
}

/* coming soon button */
.btn-primary.coming-soon {
  background: #333;
  color: #aaa300;
  padding: 10px 24px;
  border: none;
  border-radius: 20px;
  font-weight: 700;
  cursor: pointer;
  opacity: 0.6;
  pointer-events: auto; /* still clickable */
  transition: background 0.3s ease;
}

/* coming soon message */
.coming-soon-box {
  margin-top: 16px;
  padding: 12px 20px;
  background: #fff8e1;
  border-left: 4px solid #f6b300;
  color: #222;
  font-weight: 600;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ---------- Full-bleed hazard divider ---------- */
.footer-divider {
  position: relative;
  left: 0;
  right: 0;
  margin-left: 0;
  margin-right: 0;
  width: 100%;
  background: linear-gradient(180deg, #d19600 0%, #c18500 100%);
}
.footer-divider__inner {
  /* visible height of the divider */
  height: 64px;
  background-image: url('@/assets/images/hazard-stripes.svg');
  background-repeat: repeat-x;
  background-size: auto 100%;
  background-position: center;
  filter: drop-shadow(0 6px 12px rgba(0,0,0,.35));
}

/* responsive */
@media (max-width: 860px) {
  .mission__content {
    grid-template-columns: 1fr;
    text-align: center;
  }
  .note-tape {
    left: 50%;
    transform: translateX(-50%) rotate(-10deg);
  }
}
</style>
