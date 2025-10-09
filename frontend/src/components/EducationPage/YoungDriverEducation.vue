<template>
  <main class="page">
    <h1 class="title">Young Driver Education Infographic</h1>

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
              <ul>
                <li v-for="(line, i) in formatMitigation(cards[expandedIndex].mitigation)" :key="i">
                  {{ line }}
                </li>
              </ul>
            </div>

          </div>
        </div>
      </div>
    </transition>
    <!-- Sources Section -->
    <section class="sources mt-5">
      <h2>Sources</h2>
      <ul>
        <li>
          <a
            href="https://teendriversource.research.chop.edu/teen-crash-risks-prevention/rules-of-the-road/seat-belt-use-facts-and-stats"
            target="_blank"
            rel="noopener"
          >
            Teen Driver Source – Seat Belt Use Facts and Stats
          </a>
        </li>
        <li>
          <a
            href="https://www.tac.vic.gov.au/road-safety/road-users/p-plate-drivers/risks-for-young-drivers"
            target="_blank"
            rel="noopener"
          >
            Risks for Young Drivers – TAC (Transport Accident Commission), 2025
          </a>
        </li>
        <li>
          <a
            href="https://www.vicroads.vic.gov.au/"
            target="_blank"
            rel="noopener"
          >
            VicRoads – Guide for Young Driver Safety Programs
          </a>
        </li>
      </ul>
    </section>

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
function formatMitigation(text: string): string[] {
  return text
    .split(/\r?\n+/) // split by new lines
    .map(line => line.trim())
    .filter(line => line.length > 0) // remove empty lines
}

const cards: Card[] = [
  {
    title: "Speeding Awareness",
    desc: "Speed is a major contributing factor to crashes and road deaths. Young drivers underestimate the dangers of speed and overestimate their ability to control a vehicle safely. Some also speed to impress peers.",
    tag: "Speeding",
    mitigation: `The faster you drive the higher the chances that you’ll be seriously injured if you crash. You don’t have to be speeding to die — if you crash at 70km/h it’s likely that your injuries will be fatal. Even just 30km/h is enough to kill a pedestrian.
As a young driver it’s important to pay attention to not only the posted speed limit but the recommended speed. When you are driving too fast you will have less time to notice and avoid hazards.
Many newer cars have features that allow you to set your maximum speed. The car will then sound a warning if you go over your set speed. This is a useful feature for ensuring that you’re keeping below the signed speed limit.`,
    image: new URL("@/assets/images/education/speed.jpg", import.meta.url).href,
  },
  {
    title: "Night Driving Risks",
    desc: "Night time and weekend driving are high crash risk times for all drivers, but pose a particularly high risk for inexperienced drivers. This may be because they are carrying passengers of similar age, who may distract the inexperienced driver. Some drive while affected by alcohol or other drugs.",
    tag: "Night Driving",
    mitigation: `Avoid driving at night in the first few months of having your Ps.
If it’s possible, ask your supervising driver or a fully licensed driver to accompany you when driving at night.
Don’t drive when you’d usually be sleeping — fatigue will increase the risk of crashing.
If you need to drive at night, try to stick to short trips and avoid long road trips at this time.`,
    image: new URL("@/assets/images/education/night.jpg", import.meta.url).href,
  },
  {
    title: "Driving Under the Influence",
    desc: "Some young people use alcohol and other drugs as a part of their lifestyle and social behaviour. They can also be pressured by peers to drive when impaired by alcohol and other drugs.",
    tag: "DUI",
    mitigation: `Under Victoria’s Graduated Licensing System, all learner and probationary drivers must have a zero blood alcohol concentration (BAC).
Alcohol slows your reaction times and can affect your decision making ability, which increases your chances of making a mistake when driving.
To reduce the risks, you are required to have a 0.00 Blood Alcohol Concentration at all times when driving.
If you’re drinking, leave the car and organise a designated driver, arrange to have someone pick you up, or use public transport and rideshare options.
If you get caught drink driving you will lose your licence, need to complete a behaviour change program and, after you get it back, you’ll have to get an alcohol interlock fitted in your car.`,
    image: new URL("@/assets/images/education/dui.jpeg", import.meta.url).href,
  },
  {
    title: "Driver Distraction",
    desc: "Research has shown that young drivers are at increased risk of a crash due to distraction, because of their inexperience in dealing with the demands of driving. Texting is very dangerous and illegal, as is speaking on a hand-held phone while driving. Under Victoria’s Graduated Licensing System, a learner or P1 driver is not permitted to use a mobile phone of any kind — this includes hand-held, hands-free, or sending text messages.",
    tag: "Distraction",
    mitigation: `Just a couple of seconds is all it takes for a crash to happen. In fact, at 50km/h, even a 2 second glance at your phone means you’ll travel up to 28 metres blind.
As a P Plate driver you’re not allowed to use your phone for anything when you’re driving. So it’s best to put it on silent, turn it off, or put it on “Do Not Disturb While Driving.”
If you find you’re still tempted, then put your phone somewhere out of reach so you can’t get to it.`,
    image: new URL("@/assets/images/education/distraction.jpg", import.meta.url).href,
  },
  {
    title: "Fatigue and Long Drives",
    desc: "Tiredness is especially relevant for young drivers due to their lifestyle, which may include socialising late at night, and working and/or studying for long hours. Young people lead busy lifestyles that can lead to not having enough sleep or having to drive at times when they would normally be asleep, which can lead to crashes where fatigue is either the cause or a contributing factor.",
    tag: "Fatigue",
    mitigation: `Plan your route in advance so that you’re not relying on your phone to find your way, or get a passenger to be your navigator. Planning your route will help you become familiar with where you’re going and work out where to take breaks along the way.
Long drives can be draining, and if you’ve had a late night you might find that you’re feeling tired. It’s important to break up long drives and stop every two hours, or swap with another driver.
Avoid driving at times when you would usually be sleeping. If you’ve got a drive that’s more than a few hours long, then it’s worth thinking about doing the drive over a couple of days.
If you’re tired, then pull over and take a power nap. It will mean you’ll take a little longer to get where you’re going, but it’s better than never arriving at all.`,
    image: new URL("@/assets/images/education/fatigue.jpg", import.meta.url).href,
  },
  {
    title: "Seatbelts Save Lives",
    desc: "Seat belts save lives and prevent injuries. However, young people’s perceptions about risk and risk-taking can lead to a tendency not to wear seatbelts. This may be due to a low perception of risk, the ‘short trip’ syndrome, driving in familiar territory, not developing a routine, or simply forgetting due to distractions. Failing to wear seatbelts is also often related to other risks, such as carrying more passengers than seatbelts or poor vehicle condition.",
    tag: "Seatbelt",
    mitigation: `When used properly, seat belts reduce the risk of fatal injury to front seat passengers by 45% and the risk of moderate to critical injury by 50%.
People not wearing a seat belt are 30 times more likely to be ejected from a vehicle during a crash.`,
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
    { scale: 0.85, opacity: 0 },
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
  display: flex;
  flex-direction: column;
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
  margin-bottom: 30px; /* reduce from large default spacing */
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
.mitigation-box[data-tag="Speeding"] {
  background: rgba(255, 61, 61, 0.9);
  border-left: 4px solid #ff3b3b;
}
.mitigation-box[data-tag="Night Driving"] {
  background: rgba(40, 75, 160, 0.9);
  border-left: 4px solid #4169e1;
}
.mitigation-box[data-tag="DUI"] {
  background: rgba(155, 0, 130, 0.9);
  border-left: 4px solid #ff5ff6;
}
.mitigation-box[data-tag="Distraction"] {
  background: rgba(240, 160, 0, 0.9);
  border-left: 4px solid #ffb300;
}
.mitigation-box[data-tag="Fatigue"] {
  background: rgba(0, 123, 255, 0.9);
  border-left: 4px solid #00bfff;
}
.mitigation-box[data-tag="Seatbelt"] {
  background: rgba(0, 160, 80, 0.9);
  border-left: 4px solid #00cc66;
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
.sources {
  margin-top: 20px;
  padding-top: 12px;
  border-top: 1px solid #ddd;
  font-size: 0.95rem;
}

.sources h2 {
  font-size: 1.2rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 10px;
}

.sources ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sources li {
  margin-bottom: 6px;
}

.sources a {
  color: #0077b6;
  font-weight: 500;
  text-decoration: none;
  transition: color 0.2s ease;
}

.sources a:hover {
  color: #0096c7;
  text-decoration: underline;
}


</style>
