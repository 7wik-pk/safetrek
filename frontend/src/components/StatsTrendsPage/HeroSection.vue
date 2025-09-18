<script setup lang="ts">
import { ref, onMounted, nextTick, onBeforeUnmount } from 'vue'

// Keep these three modules in the tabs
import AccidentStats from './AccidentStats.vue'
import TrendCharts   from './TrendCharts.vue'
import ForecastView  from './ForecastView.vue'

// New: the road list module
import CrashRoadList from '@/components/StatsTrendsPage/CrashRoadList.vue'

// Tabs shown on THIS page (RiskExplorer removed)
const tabs = [
  { label: 'Accident Stats',      comp: AccidentStats },
  { label: 'Statistics & Trends', comp: TrendCharts },
  { label: 'Forecast View',       comp: ForecastView },
  { label: 'Accident Roads',      comp: CrashRoadList },
]

const active = ref(0)

// sliding ink refs
const inkEl   = ref<HTMLElement | null>(null)
const chipEls = ref<HTMLElement[]>([])

function setChipEl(el: HTMLElement | null, i: number) {
  if (el) chipEls.value[i] = el
}

function moveInkOnly(i: number) {
  nextTick(() => {
    const el = chipEls.value[i]
    if (el && inkEl.value) {
      inkEl.value.style.left  = `${el.offsetLeft}px`
      inkEl.value.style.width = `${el.offsetWidth}px`
    }
  })
}

function moveInk(i: number) {
  active.value = i
  moveInkOnly(i)
}

function onResize() {
  moveInkOnly(active.value)
}

onMounted(() => {
  moveInkOnly(active.value)
  window.addEventListener('resize', onResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', onResize)
})
</script>

<template>
  <section class="analytics-hero">
    <div class="overlay" />
    <div class="container">
      <div class="hero-inner">
        <button class="back" @click="$router.back()">‹ Back</button>
        <p class="eyebrow">ANALYTICS</p>
        <h1 class="title">Explore insights across four lenses.</h1>
        <p class="sub">Switch between modules using the chips below.</p>
      </div>
    </div>
  </section>

  <!-- Metric selector -->
  <div class="container">
    <div class="metrics">
      <span ref="inkEl" class="ink"></span>
      <button
        v-for="(t, i) in tabs"
        :key="t.label"
        :ref="el => setChipEl(el as HTMLElement, i)"
        class="chip"
        :aria-selected="i === active"
        @click="moveInk(i)"
      >
        {{ t.label }}
      </button>
    </div>
  </div>

  <!-- Panels: keep all mounted, switch with v-show -->
  <div class="content">
    <div class="container panels">
      <div class="panel" v-show="active === 0">
        <AccidentStats />
      </div>
      <div class="panel" v-show="active === 1">
        <TrendCharts />
      </div>
      <div class="panel" v-show="active === 2">
        <ForecastView />
      </div>
      <div class="panel" v-show="active === 3">
        <CrashRoadList />
      </div>
    </div>
  </div>
</template>

<style scoped>
:root { --gold:#f6b300; --gold-2:#c98600; --ink:#0b0b0b; }
.analytics-hero{position:relative;min-height:36vh;display:grid;align-items:end;background:#fff;color:#111;border-bottom:1px solid #ececec;}
.analytics-hero .overlay{position:absolute;inset:0;background:transparent;}
.container{max-width:1180px;margin:0 auto;padding:0 22px;}
.hero-inner{position:relative;z-index:1;padding:28px 0 20px;}
.back{appearance:none;border:0;background:#f4f4f4;color:#333;font-weight:700;padding:9px 14px;border-radius:999px;margin-bottom:10px;cursor:pointer;transition:background .2s ease,transform .1s ease;}
.back:hover{background:#eaeaea;} .back:active{transform:translateY(1px);}
.eyebrow{margin:0 0 4px;letter-spacing:.08em;font-weight:800;color:#777;}
.title{margin:0 0 6px;font-size:clamp(22px,3.4vw,34px);line-height:1.15;font-weight:900;}
.sub{margin:0;color:#666;font-size:clamp(13px,1.8vw,16px);}

.metrics{
  position:relative;display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:14px auto 8px;
  background:#fff;border:1px solid #ece7d5;border-radius:12px;padding:8px;overflow:hidden;box-shadow:0 6px 24px rgba(0,0,0,.06);
}
.chip{position:relative;z-index:1;appearance:none;border:0;height:42px;border-radius:10px;font-weight:800;font-size:clamp(13px,1.6vw,15px);letter-spacing:.02em;color:#333;background:transparent;cursor:pointer;transition:color .2s ease, transform .1s ease;}
.chip[aria-selected="true"]{color:#111;} .chip:active{transform:translateY(1px);}

.ink{position:absolute;top:8px;left:0;height:calc(100% - 16px);border-radius:10px;background:linear-gradient(180deg,var(--gold),var(--gold-2));transition:left .25s ease,width .25s ease;z-index:0;box-shadow:0 8px 18px rgba(0,0,0,.18);}

.content{background:#fff;padding:14px 0 40px;}
.panels{position:relative;}
.panel{}

@media (max-width:820px){ .metrics{grid-template-columns:1fr 1fr;} }
@media (max-width:480px){ .metrics{grid-template-columns:1fr;} }
</style>
