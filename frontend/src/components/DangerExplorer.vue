<template>
  <section class="container my-4 bg-white p-3 p-sm-4 rounded-4 shadow-sm">
    <div class="d-flex align-items-center justify-content-between mb-3">
      <div>
        <div class="text-uppercase text-muted fw-semibold small">Analytics</div>
        <h1 class="h3 fw-bold m-0">Road Safety Hotspots Explorer</h1>
        <div class="text-muted">Switch between modules and follow the guided steps.</div>
      </div>
      <button class="btn btn-outline-secondary btn-sm" @click="startTour">❓ Tour</button>
    </div>

    <!-- Progress with labels -->
    <div class="mb-3">
      <div class="progress" style="height:14px;">
        <div
          class="progress-bar bg-dark"
          role="progressbar"
          :style="{ width: progressPct + '%' }"
          aria-valuemin="0"
          aria-valuemax="100"
          :aria-valuenow="progressPct"
        />
      </div>
      <div class="d-flex justify-content-between small mt-1">
        <div :class="['text-muted', { 'fw-semibold text-dark': step===1 }]">1. Suburb</div>
        <div :class="['text-muted', { 'fw-semibold text-dark': step===2 }]">2. Road & Filters</div>
        <div :class="['text-muted', { 'fw-semibold text-dark': step===3 }]">3. Results</div>
      </div>
    </div>

    <!-- PAGE 1: Suburb + Road Types -->
    <div v-if="step===1" class="card shadow-sm" id="tour-step1">
      <div class="card-body">
        <div class="d-flex align-items-baseline gap-2 mb-2">
          <h2 class="h5 m-0">Choose Suburb & road types</h2>
          <small class="text-muted">These choices fetch roads, then you set filters.</small>
        </div>

        <div class="mb-3" id="tour-sa2">
          <label class="form-label">Suburb (SA2)</label>
          <div class="d-flex gap-2 align-items-center">
            <select v-model="state.selectedSA2" class="form-select" @change="resetRoads">
              <option value="" disabled>Select a suburb…</option>
              <option v-for="name in sa2Options" :key="name" :value="name">{{ name }}</option>
            </select>
            <button
              class="btn btn-outline-secondary btn-sm"
              @click="loadSA2"
              :disabled="busy"
              title="Reload list"
              aria-label="Reload list"
            >↻</button>
          </div>
        </div>

        <div class="mb-3" id="tour-roadtypes">
          <label class="form-label">Road types</label>
          <div class="row g-2">
            <div v-for="opt in ROAD_TYPE_OPTIONS" :key="opt.value" class="col-12 col-sm-6 col-lg-4">
              <div class="border rounded-3 p-3 h-100">
                <div class="form-check">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    :id="'rt-'+opt.value"
                    v-model="state.roadTypeSelected[opt.value]"
                    :disabled="busy"
                  >
                  <label class="form-check-label" :for="'rt-'+opt.value">
                    <span class="fw-semibold">{{ opt.label }}</span>
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>

        <button id="tour-fetch" class="btn btn-dark w-100" @click="fetchRoadsAndNext" :disabled="!state.selectedSA2 || busy">
          {{ loading.roads ? 'Fetching…' : 'Fetch & Next →' }}
        </button>
      </div>
    </div>

    <!-- PAGE 2: Choose road & filters -->
    <div v-if="step===2" class="card shadow-sm" id="tour-step2">
      <div class="card-body">
        <div class="d-flex align-items-baseline gap-2 mb-2">
          <h2 class="h5 m-0">Choose road & filters</h2>
          <small class="text-muted">Roads were fetched using your selections on Page 1.</small>
        </div>

        <div class="mb-3" id="tour-road">
          <label class="form-label">Road</label>
          <div class="d-flex gap-2 align-items-center">
            <select v-model="state.selectedRoad" class="form-select" :disabled="!roads.length || busy">
              <option value="" disabled>Select a road…</option>
              <option v-for="r in roads" :key="r.road_name" :value="r.road_name">
                {{ r.road_name }} — {{ r.road_type }}<span v-if="r.road_length_km != null"> ({{ r.road_length_km.toFixed(2) }} km)</span>
              </option>
            </select>
            <button
              class="btn btn-outline-secondary btn-sm"
              @click="loadRoads"
              :disabled="busy || !state.selectedSA2"
              title="Refetch roads"
              aria-label="Refetch roads"
            >↻</button>
          </div>
        </div>

        <!-- Analysis buttons with distinct colors -->
        <div class="mb-3" id="tour-analysis">
          <label class="form-label d-block">Analysis</label>
          <div class="btn-group" role="tablist" aria-label="Analysis type">
            <button
              type="button"
              class="btn"
              :class="mode==='corridors' ? 'btn-primary' : 'btn-outline-primary'"
              role="tab"
              @click="!busy && setMode('corridors')"
              :disabled="busy"
            >Corridors</button>
            <button
              type="button"
              class="btn"
              :class="mode==='blackspots' ? 'btn-danger' : 'btn-outline-danger'"
              role="tab"
              @click="!busy && setMode('blackspots')"
              :disabled="busy"
            >Blackspots</button>
          </div>
        </div>

        <div class="row g-3" id="tour-dates">
          <div class="col-md-6">
            <label class="form-label">Date range</label>
            <div class="d-flex align-items-center gap-2">
              <input type="date" v-model="state.startDate" class="form-control" :disabled="busy" />
              <span class="text-muted">to</span>
              <input type="date" v-model="state.endDate" class="form-control" :disabled="busy" />
            </div>
            <div class="form-text">Defaults to last 3 years up to the latest date in DB.</div>
          </div>
          <div class="col-md-6">
            <label class="form-label">Optional time window</label>
            <div class="d-flex align-items-center gap-2">
              <input type="time" v-model="state.startTime" class="form-control" :disabled="busy" />
              <span class="text-muted">to</span>
              <input type="time" v-model="state.endTime" class="form-control" :disabled="busy" />
            </div>
            <div class="form-text">Leave blank to include all times.</div>
          </div>
        </div>

        <div class="row g-3 mt-1">
          <div class="col-md-4">
            <label class="form-label">Order by</label>
            <select v-model="state.orderBy" class="form-select" :disabled="busy">
              <option value="density">Density (acc/km)</option>
              <option value="count">Count</option>
            </select>
          </div>
          <div class="col-md-4">
            <label class="form-label">Direction</label>
            <select v-model.number="state.orderAsc" class="form-select" :disabled="busy">
              <option :value="0">Desc</option>
              <option :value="1">Asc</option>
            </select>
          </div>
          <div class="col-md-4">
            <label class="form-label">Limit</label>
            <input type="number" class="form-control" v-model.number="state.limit" min="1" max="100" :disabled="busy" />
          </div>
        </div>

        <div v-if="mode==='blackspots'" class="mt-3" id="tour-structures">
          <label class="form-label">Blackspot structure types</label>
          <div class="row g-2">
            <div v-for="opt in STRUCTURE_TYPE_OPTIONS" :key="opt.value" class="col-12 col-sm-6 col-lg-4">
              <div class="border rounded-3 p-3 h-100">
                <div class="form-check">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    :id="'st-'+opt.value"
                    v-model="state.structTypeSelected[opt.value]"
                    :disabled="busy"
                  >
                  <label class="form-check-label" :for="'st-'+opt.value">
                    <span class="fw-semibold">{{ opt.label }}</span>
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="d-flex gap-2 mt-4">
          <button class="btn btn-outline-secondary" @click="goTo(1)" :disabled="busy">← Back</button>
          <button class="btn" :class="mode==='corridors' ? 'btn-primary' : 'btn-danger'" @click="mode==='corridors' ? runCorridorsAndGo() : runBlackspotsAndGo()" :disabled="!canRun || busy">See Results →</button>
        </div>
      </div>
    </div>

    <!-- PAGE 3: Results as list -->
    <div v-if="step===3" class="card shadow-sm" id="tour-step3">
      <div class="card-body">
        <h2 class="h5 mb-3">Results</h2>

        <div v-if="mode==='corridors'">
          <div v-if="loading.results" class="text-center py-5">
            <div class="spinner-border text-dark" role="status"></div>
            <div class="fw-semibold mt-2">Loading…</div>
          </div>
          <template v-else>
            <ul v-if="corridors.length" class="list-group">
              <li v-for="(row,i) in corridors" :key="i" class="list-group-item">
                <div class="row g-2 align-items-center">
                  <div class="col-12 col-sm-2"><span class="text-muted small">#</span> {{ i+1 }}</div>
                  <div class="col-12 col-sm-4">
                    <span class="text-muted small">Segment type</span>
                    <div class="fw-semibold">{{ row.segment_type }}</div>
                  </div>
                  <div class="col-6 col-sm-3">
                    <span class="text-muted small">Accidents</span>
                    <div class="fw-semibold">{{ row.num_accidents }}</div>
                  </div>
                  <div class="col-6 col-sm-3">
                    <span class="text-muted small">Accidents / km</span>
                    <div class="fw-semibold">{{ row.accidents_per_km }}</div>
                  </div>
                </div>
              </li>
            </ul>
            <div v-else class="text-muted">No results. Try widening dates or removing time window.</div>
          </template>
        </div>

        <div v-if="mode==='blackspots'">
          <div v-if="loading.results" class="text-center py-5">
            <div class="spinner-border text-dark" role="status"></div>
            <div class="fw-semibold mt-2">Loading…</div>
          </div>
          <template v-else>
            <ul v-if="blackspots.length" class="list-group">
              <li v-for="(row,i) in blackspots" :key="i" class="list-group-item">
                <div class="row g-2 align-items-center">
                  <div class="col-12 col-sm-2"><span class="text-muted small">#</span> {{ i+1 }}</div>
                  <div class="col-12 col-sm-6">
                    <span class="text-muted small">Structure type</span>
                    <div class="fw-semibold">{{ row.structure_type }}</div>
                  </div>
                  <div class="col-12 col-sm-4">
                    <span class="text-muted small">Accidents</span>
                    <div class="fw-semibold">{{ row.num_accidents }}</div>
                  </div>
                </div>
              </li>
            </ul>
            <div v-else class="text-muted">No results. Try widening dates or removing filters.</div>
          </template>
        </div>

        <div class="d-flex gap-2 mt-4">
          <button class="btn btn-outline-secondary" @click="goTo(2)" :disabled="busy">← Filters</button>
          <button class="btn btn-outline-secondary" @click="goTo(1)" :disabled="busy">↺ Start</button>
        </div>
      </div>
    </div>

    <!-- Overlay during in-flight requests -->
    <div
      v-if="busy"
      class="position-fixed top-0 start-0 w-100 h-100 d-flex flex-column align-items-center justify-content-center bg-white bg-opacity-50"
      style="z-index:1050;"
    >
      <div class="spinner-border text-dark" role="status"></div>
      <div class="fw-semibold mt-2">Loading…</div>
    </div>
  </section>

  <FooterSection/>
</template>

<script setup lang="ts">
import { reactive, ref, computed, onMounted } from 'vue'
import FooterSection from '@/components/FooterSection.vue'

// version-agnostic import for driver.js (works with v1.3.6 or v2)
import * as DriverNS from 'driver.js'
import 'driver.js/dist/driver.css'

/** CONFIG **/
const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000'
const REGION_LEVEL: 'sa2' | 'sa3' = 'sa2'

const ROAD_TYPE_OPTIONS = [
  { value: 'ambiguous', label: 'Ambiguous Classification' },
  { value: 'commerical_and_civic', label: 'Commercial & Civic Roads' }, // keep slug used by API
  { value: 'infrastructure', label: 'Infrastructure Roads' },
  { value: 'major', label: 'Major Roads' },
  { value: 'pedestrian_and_recreational_paths', label: 'Pedestrian & Recreational Paths' },
  { value: 'rural_and_low_traffic', label: 'Rural & Low-Traffic Roads' },
  { value: 'suburban', label: 'Suburban Roads' }
] as const

const STRUCTURE_TYPE_OPTIONS = [
  { value: 'barrier', label: 'Road Barrier' },
  { value: 'bridge', label: 'Bridge' },
  { value: 'ford', label: 'Low-Water Crossing (Ford)' },
  { value: 'gate', label: 'Road Gate' },
  { value: 'int_attribute', label: 'Intersection (Attribute Only)' },
  { value: 'int_coast', label: 'Coastal Intersection' },
  { value: 'int_locality', label: 'Locality Intersection' },
  { value: 'int_nosignal', label: 'Unsignalized Intersection' },
  { value: 'int_paper', label: 'Paper Road Intersection' },
  { value: 'int_signal', label: 'Signalized Intersection' },
  { value: 'level_crossing', label: 'Railway Level Crossing' },
  { value: 'road_end', label: 'Road End' },
  { value: 'roundabout', label: 'Roundabout' },
  { value: 'tunnel', label: 'Tunnel' }
] as const

/** STATE **/
const sa2Options = ref<string[]>([])
const state = reactive({
  selectedSA2: '',
  roadTypeSelected: Object.fromEntries(ROAD_TYPE_OPTIONS.map(o => [o.value, true])) as Record<string, boolean>,
  selectedRoad: '',
  startDate: '',
  endDate: '',
  startTime: '',
  endTime: '',
  orderBy: 'density' as 'density' | 'count',
  orderAsc: 0 as 0 | 1,
  limit: 10,
  structTypeSelected: Object.fromEntries(STRUCTURE_TYPE_OPTIONS.map(o => [o.value, false])) as Record<string, boolean>
})

const loading = reactive({ sa2: false, roads: false, results: false })
const mode = ref<'corridors' | 'blackspots'>('corridors')
const step = ref(1)

// Data results
const roads = ref<{ road_name: string; road_type: string; road_length_km: number | null }[]>([])
const corridors = ref<any[]>([])
const blackspots = ref<any[]>([])

/** COMPUTEDS **/
const selectedRoadTypes = computed(() =>
  Object.entries(state.roadTypeSelected).filter(([, v]) => v).map(([k]) => k)
)
const selectedStructTypes = computed(() =>
  Object.entries(state.structTypeSelected).filter(([, v]) => v).map(([k]) => k)
)
const canRun = computed(() => !!state.selectedSA2 && !!state.selectedRoad)
const busy = computed(() => loading.sa2 || loading.roads || loading.results)
const progressPct = computed(() => (step.value === 1 ? 33 : step.value === 2 ? 66 : 100))

/** GUARD to prevent late responses navigating UI **/
let inflightToken: symbol | null = null
const newToken = () => Symbol('inflight')
const cancelInflight = () => { inflightToken = newToken() }

/** HELPERS **/
async function fetchJSON<T>(url: string) {
  const r = await fetch(url)
  if (!r.ok) throw new Error(`${r.status} ${r.statusText}`)
  return (await r.json()) as T
}
function toIsoDate(d: Date) { return d.toISOString().slice(0, 10) }
function resetRoads() { roads.value = []; state.selectedRoad = '' }

/** Load Suburbs + default dates */
async function loadSA2() {
  if (busy.value) return
  loading.sa2 = true
  const token = newToken(); inflightToken = token
  try {
    sa2Options.value = await fetchJSON<string[]>(`${API_BASE}/distinct_sa2`)
  } finally {
    if (inflightToken === token) loading.sa2 = false
  }
}

async function loadDefaultDates() {
  try {
    const maxDate = await fetchJSON<string | null>(`${API_BASE}/max_accident_date`)
    const end = maxDate ? new Date(maxDate) : new Date()
    const start = new Date(end); start.setFullYear(end.getFullYear() - 3)
    state.startDate = toIsoDate(start); state.endDate = toIsoDate(end)
  } catch {
    const end = new Date(); const start = new Date(); start.setFullYear(end.getFullYear() - 3)
    state.startDate = toIsoDate(start); state.endDate = toIsoDate(end)
  }
}

/** Fetch roads (Step 2 refetch button) */
async function loadRoads() {
  if (!state.selectedSA2 || busy.value) return
  loading.roads = true; roads.value = []
  const token = newToken(); inflightToken = token
  try {
    const params = new URLSearchParams({ sa2_name: state.selectedSA2 })
    selectedRoadTypes.value.forEach(rt => params.append('road_types', rt))
    const data = await fetchJSON<typeof roads.value>(`${API_BASE}/roads_by_region?${params.toString()}`)
    if (inflightToken !== token) return
    roads.value = data
    if (!state.selectedRoad && data.length) state.selectedRoad = data[0].road_name
  } finally {
    if (inflightToken === token) loading.roads = false
  }
}

/** Step 1: fetch + next in one click */
const fetchRoadsAndNext = async () => {
  if (!state.selectedSA2 || busy.value) return
  cancelInflight()
  loading.roads = true; roads.value = []
  const token = newToken(); inflightToken = token
  try {
    const params = new URLSearchParams({ sa2_name: state.selectedSA2 })
    selectedRoadTypes.value.forEach(rt => params.append('road_types', rt))
    const data = await fetchJSON<typeof roads.value>(`${API_BASE}/roads_by_region?${params.toString()}`)
    if (inflightToken !== token) return
    roads.value = data
    if (!state.selectedRoad && data.length) state.selectedRoad = data[0].road_name
    step.value = 2
  } finally {
    if (inflightToken === token) loading.roads = false
  }
}

/** Runs */
async function runCorridors() {
  const params = new URLSearchParams({
    region_level: REGION_LEVEL,
    region_name: state.selectedSA2,
    road_name: state.selectedRoad,
    start_date: state.startDate,
    end_date: state.endDate,
    order_by: state.orderBy,
    order_dir_asc: String(Boolean(state.orderAsc)),
    limit: String(state.limit)
  })
  if (state.startTime && state.endTime) {
    params.set('start_time', state.startTime + ':00')
    params.set('end_time', state.endTime + ':00')
  }
  const url = `${API_BASE}/corridor_crash_density?${params.toString()}`
  return await fetchJSON<any[]>(url)
}

async function runBlackspots() {
  const params = new URLSearchParams({
    region_level: REGION_LEVEL,
    region_name: state.selectedSA2,
    road_name: state.selectedRoad,
    start_date: state.startDate,
    end_date: state.endDate,
    order_dir_asc: String(Boolean(state.orderAsc)),
    limit: String(state.limit)
  })
  if (state.startTime && state.endTime) {
    params.set('start_time', state.startTime + ':00')
    params.set('end_time', state.endTime + ':00')
  }
  selectedStructTypes.value.forEach(st => params.append('structure_types', st))
  const url = `${API_BASE}/blackspot_crash_density?${params.toString()}`
  return await fetchJSON<any[]>(url)
}

// Navigation + in-flight guarded run actions
const goTo = (n: number) => { cancelInflight(); step.value = n }
const setMode = (m: 'corridors' | 'blackspots') => { if (!busy.value) mode.value = m }

const runCorridorsAndGo = async () => {
  if (!canRun.value || busy.value) return
  cancelInflight(); loading.results = true
  const token = newToken(); inflightToken = token
  try {
    const res = await runCorridors()
    if (inflightToken !== token) return
    corridors.value = res; blackspots.value = []; step.value = 3
  } finally {
    if (inflightToken === token) loading.results = false
  }
}

const runBlackspotsAndGo = async () => {
  if (!canRun.value || busy.value) return
  cancelInflight(); loading.results = true
  const token = newToken(); inflightToken = token
  try {
    const res = await runBlackspots()
    if (inflightToken !== token) return
    blackspots.value = res; corridors.value = []; step.value = 3
  } finally {
    if (inflightToken === token) loading.results = false
  }
}

/** Guided tour — works with driver.js v1 or v2 */
function startTour() {
  try {
    const options: any = {
      showProgress: true,
      animate: true,
      opacity: 0.4,
      nextBtnText: 'Next',
      prevBtnText: 'Back',
      doneBtnText: 'Done',
    }

    // Only include steps for DOM nodes that exist at this moment
    const steps: any[] = []
    if (document.querySelector('#tour-step1')) {
      steps.push(
        { element: '#tour-step1', popover: { title: 'Step 1: Suburb', description: 'Pick the suburb and road types to include.' } },
        { element: '#tour-sa2', popover: { title: 'Suburb (SA2)', description: 'Choose the suburb to analyze.' } },
        { element: '#tour-roadtypes', popover: { title: 'Road types', description: 'Uncheck the types you don’t want.' } },
        { element: '#tour-fetch', popover: { title: 'Fetch roads', description: 'Fetch all roads and continue to filters.' } },
      )
    }
    if (document.querySelector('#tour-step2')) {
      steps.push(
        { element: '#tour-step2', popover: { title: 'Step 2: Filters', description: 'Choose the road and set filters for analysis.' } },
        { element: '#tour-analysis', popover: { title: 'Analysis type', description: 'Corridors vs Blackspots.' } },
        { element: '#tour-dates', popover: { title: 'Date & time', description: 'Pick the analysis window.' } },
        { element: '#tour-structures', popover: { title: 'Blackspot structures', description: 'Optional filters for blackspots.' } },
      )
    }
    if (document.querySelector('#tour-step3')) {
      steps.push(
        { element: '#tour-step3', popover: { title: 'Step 3: Results', description: 'View hotspots and adjust filters if needed.' } },
      )
    }

    if (!steps.length) {
      alert('Open a page section first (e.g., Step 1 or Step 2), then click Tour.')
      return
    }

    // v2 API
    if (typeof (DriverNS as any).driver === 'function') {
      const d = (DriverNS as any).driver(options)
      if (typeof d.setSteps === 'function') d.setSteps(steps)
      else if (typeof d.defineSteps === 'function') d.defineSteps(steps)
      else (d as any).steps = steps
      if (typeof d.drive === 'function') d.drive()
      localStorage.setItem('dangerExplorerTourSeen', '1')
      return
    }

    // v1 API
    const DriverCtor: any = (DriverNS as any).default || (DriverNS as any)
    const d = new DriverCtor(options)
    if (typeof d.defineSteps === 'function') d.defineSteps(steps)
    else if (typeof d.setSteps === 'function') d.setSteps(steps)
    else (d as any).steps = steps
    if (typeof d.start === 'function') d.start()
    else if (typeof d.drive === 'function') d.drive()
    localStorage.setItem('dangerExplorerTourSeen', '1')
  } catch (e) {
    console.warn('driver.js failed to start', e)
    alert('To launch the guided tour, please install driver.js:\n\n  npm i driver.js')
  }
}

onMounted(async () => {
  await Promise.all([loadSA2(), loadDefaultDates()])
  // keep manual start via ❓ button to avoid blocking users
})
</script>

<style scoped>
/* Bootstrap handles styling; wrapper ensures white background */
</style>
