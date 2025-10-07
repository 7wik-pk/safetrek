<template>
  <main class="page">
    <h1 class="title">Young Driver Education</h1>

    <!-- Card Grid -->
    <div class="grid">
      <div
        v-for="(card, i) in cards"
        :key="i"
        class="card"
        ref="cardRefs"
        @click="expandCard(i)"
      >
        <div class="card-image">
          <img :src="card.image" :alt="card.title" />
          <div class="card-overlay">
            <span class="tag">{{ card.tag }}</span>
          </div>
        </div>
        <div class="card-content">
          <h3>{{ card.title }}</h3>
        </div>
      </div>
    </div>

    <!-- Expanded Overlay -->
    <transition name="fade">
      <div v-if="expandedIndex !== null" class="overlay" @click="closeCard">
        <div class="expanded" ref="expandedCardRef">
          <img
            class="expanded-img"
            :src="cards[expandedIndex].image"
            :alt="cards[expandedIndex].title"
          />
          <div class="expanded-content" @click.stop>
            <span class="tag">{{ cards[expandedIndex].tag }}</span>
            <h2>{{ cards[expandedIndex].title }}</h2>
            <p>{{ cards[expandedIndex].desc }}</p>

            <!-- Mitigation Section -->
            <div v-if="cards[expandedIndex].mitigation" class="mitigation-box">
              <h3>Mitigation</h3>
              <p>{{ cards[expandedIndex].mitigation }}</p>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </main>
</template>

<script setup lang="ts">
import { ref, nextTick } from "vue"
import gsap from "gsap"

interface Card {
  title: string
  desc: string
  tag: string
  mitigation?: string
  image: string
}

const cards: Card[] = [
  {
    title: "Speed Awareness",
    desc: "Speed is a major contributing factor to crashes and road deaths. Young drivers often underestimate the dangers of speeding and overestimate their control. Some speed to impress peers.",
    tag: "Safety",
    mitigation:
      "At 60 km/h it takes about 45 m to stop — at 50 km/h it’s 35 m. That 10 m can mean avoiding or causing a crash.",
    image: new URL("@/assets/images/education/speed.jpg", import.meta.url).href,
  },
  {
    title: "Night Driving Risks",
    desc: "Nighttime and weekends pose higher crash risks, especially for new drivers. Reduced visibility and fatigue increase danger.",
    tag: "Awareness",
    mitigation:
      "Complete at least 120 hours of supervised driving. Avoid unnecessary night trips and plan safe transport.",
    image: new URL("@/assets/images/education/night.jpg", import.meta.url).href,
  },
  {
    title: "Driving Under the Influence",
    desc: "Some young drivers feel pressured to drive after drinking or drug use, impairing alertness and reaction time.",
    tag: "Responsibility",
    mitigation:
      "Victorian learner and probationary drivers must have zero BAC. Never drive under influence — plan alternatives.",
    image: new URL("@/assets/images/education/dui.jpeg", import.meta.url).href,
  },
  {
    title: "Driver Distraction",
    desc: "Young drivers are more prone to distraction due to inexperience. Phone use or multitasking multiplies crash risk.",
    tag: "Focus",
    mitigation:
      "Using any phone can increase crash risk 4×. Learners and P1 drivers can’t use phones — even hands-free.",
    image: new URL("@/assets/images/education/distraction.jpg", import.meta.url).href,
  },
  {
    title: "Fatigue and Long Drives",
    desc: "Young drivers often lead busy lives with little rest. Fatigue slows reactions and causes microsleeps.",
    tag: "Health",
    mitigation:
      "Get 6+ hours of sleep before long drives. Take breaks every 2 hours, and nap if drowsy — only sleep cures fatigue.",
    image: new URL("@/assets/images/education/fatigue.jpg", import.meta.url).href,
  },
  {
    title: "Seatbelt Saves Lives",
    desc: "Some young people neglect seatbelts on short trips. This drastically increases injury or ejection risk.",
    tag: "Protection",
    mitigation:
      "Seatbelts cut fatal injury risk by 45%. Unbelted passengers are 30× more likely to be ejected — always buckle up.",
    image: new URL("@/assets/images/education/seatbelt.jpg", import.meta.url).href,
  },
]

const expandedIndex = ref<number | null>(null)
const cardRefs = ref<HTMLElement[]>([])
const expandedCardRef = ref<HTMLElement | null>(null)

async function expandCard(i: number) {
  expandedIndex.value = i
  await nextTick()
  const expanded = expandedCardRef.value
  if (!expanded) return
  gsap.fromTo(
    expanded,
    { scale: 0.8, opacity: 0 },
    { scale: 1, opacity: 1, duration: 0.5, ease: "power3.out" }
  )
}

function closeCard() {
  const expanded = expandedCardRef.value
  if (!expanded) return
  gsap.to(expanded, {
    opacity: 0,
    scale: 0.9,
    duration: 0.4,
    ease: "power2.inOut",
    onComplete: () => (expandedIndex.value = null),
  })
}
</script>

<style scoped>
.page {
  padding: 40px;
  background: #fdfaf3;
  min-height: 100vh;
}

.title {
  font-size: 2.1rem;
  font-weight: 700;
  color: #222;
  margin-bottom: 30px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 24px;
}

/* ===== CARD ===== */
.card {
  border-radius: 18px;
  background: #fffdfa;
  overflow: hidden;
  cursor: pointer;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
  transition: all 0.3s ease;
}
.card:hover {
  transform: translateY(-6px) scale(1.02);
  box-shadow: 0 12px 26px rgba(255, 196, 0, 0.3);
}

.card-image {
  position: relative;
  overflow: hidden;
  height: 180px;
}
.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}
.card:hover img {
  transform: scale(1.08);
}

.card-overlay {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.55);
  padding: 4px 10px;
  border-radius: 6px;
}
.tag {
  font-size: 0.8rem;
  color: #fff6a0;
  text-transform: uppercase;
}

.card-content {
  padding: 12px 14px;
}
.card-content h3 {
  font-size: 1.05rem;
  color: #222;
  font-weight: 600;
}

/* ===== OVERLAY EXPANDED ===== */
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(6px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
}

.expanded {
  position: relative;
  width: 80vw;
  max-width: 900px;
  height: 70vh;
  background: #000;
  border-radius: 24px;
  overflow: hidden;
  color: #fff;
}
.expanded-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.8;
}
.expanded-content {
  position: absolute;
  bottom: 0;
  padding: 40px;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.85), transparent);
}
.expanded-content h2 {
  font-size: 1.8rem;
  margin: 8px 0;
  font-weight: 700;
}
.expanded-content p {
  color: #eee;
  line-height: 1.5;
}

/* ===== Mitigation Box ===== */
.mitigation-box {
  margin-top: 16px;
  padding: 14px 18px;
  background: rgba(46, 100, 200, 0.85);
  border-left: 4px solid #3b82f6;
  border-radius: 8px;
}
.mitigation-box h3 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #c7e0ff;
  margin-bottom: 6px;
}
.mitigation-box p {
  color: #e0f2fe;
  line-height: 1.5;
}

/* Fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
