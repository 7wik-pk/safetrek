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
              <option value="" disabled>Select a road...</option>
              <option v-for="r in roads" :key="r.road_name" :value="r.road_name">
                {{ r.road_name }} - {{ r.road_type }}<span v-if="r.road_length_km != null"> ({{ r.road_length_km.toFixed(2) }} km)</span>
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

    <!-- PAGE 3: Results as map -->
    <div v-if="step===3" class="card shadow-sm" id="tour-step3">
      <div class="card-body">
        <h2 class="h5 mb-3">Most dangerous {{ mode }} on {{ state.selectedRoad }}, {{ state.selectedSA2 }}</h2>

        <div class="map-wrap">
          <div id="results-map" class="map-container" />
          <!-- Overlay message when no results -->
          <div
            v-if="!loading.results && step === 3 && ((mode==='corridors' && !corridors.length) || (mode==='blackspots' && !blackspots.length))"
            class="no-results-overlay"
          >
            <div class="no-results-message">
              <div class="fw-semibold mb-1">No results found. Try selecting bigger (or more prominent) roads, adjusting filters,
                {{ mode==='corridors'
                  ? 'or widening the date range.'
                  : 'or adjusting structure types.' }}
              </div>
            </div>
          </div>

          <div v-if="loading.results" class="loading-overlay" aria-live="polite">
            <span class="spinner-border text-dark" role="status"></span>
            <div class="fw-semibold mt-2">Loading map...</div>
          </div>
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
      <div class="fw-semibold mt-2">
        Loading, please wait...
        <div v-if="mode==='blackspots'" class="text-muted small">Blackspots can take up to 2 minutes to query, please be patient.</div>
      </div>
    </div>
  </section>

  <FooterSection/>
</template>

<script setup lang="ts">
import { reactive, ref, computed, onMounted, watch, nextTick } from 'vue'
import FooterSection from '@/components/FooterSection.vue'

import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// version-agnostic import for driver.js (works with v1.3.6 or v2)
import * as DriverNS from 'driver.js'
import 'driver.js/dist/driver.css'

/** CONFIG **/
const API_BASE = import.meta.env.VITE_API_BASE ?? '/api'
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

const map = ref<L.Map | null>(null)
const resultsLayer = ref<L.LayerGroup | null>(null)

function parseLineWKT(wkt: string): [number, number][][] {
  if (!wkt || typeof wkt !== "string") return []

  const isMulti = wkt.startsWith("MULTILINESTRING")
  const clean = wkt.replace(/^(MULTI)?LINESTRING\s*/i, "").replace(/^\(+|\)+$/g, "").trim()

  const parseCoords = (s: string): [number, number][] =>
    s.split(",").map(pair => {
      const [lon, lat] = pair.trim().split(/\s+/).map(Number)
      return [lat, lon]
    })

  if (isMulti) {
    return clean.split(/\)\s*,\s*\(/).map(parseCoords)
  } else {
    return [parseCoords(clean)]
  }
}

let legendControl: L.Control | null = null

function setLegend(title: string, maxVal: number) {
  if (legendControl) legendControl.remove()

  legendControl = L.control({ position: "bottomright" })
  legendControl.onAdd = () => {
    const div = L.DomUtil.create("div", "info legend")
    const grades = [0, 0.2, 0.4, 0.6, 0.8, 1]
      .map(g => Math.round(g * maxVal))
      .filter((v, i, arr) => i === 0 || v !== arr[i - 1])

    div.innerHTML = `<h4>${title}</h4>` + grades.map(v => {
      const c = getColor(v, maxVal)
      return `<i style="background:${c}"></i> ${v}`
    }).join("<br>")
    return div
  }

  legendControl.addTo(map.value!)
}

function renderCorridorResults(rows: any[]) {
  if (!map.value) return
  if (resultsLayer.value) resultsLayer.value.remove()
  resultsLayer.value = L.layerGroup()

  const maxDensity = Math.max(...rows.map(r => r.accidents_per_km || 0))

  const polylines: L.Polyline[] = []

  rows.forEach(row => {
    const segments = parseLineWKT(row.segment_geom_wkt)
    if (!segments.length) return

    const color = getColor(row.accidents_per_km, maxDensity)
    const weight = 3 + Math.min(7, (row.accidents_per_km / (maxDensity || 1)) * 7)

    segments.forEach(coords => {
      const polyline = L.polyline(coords, {
        color,
        weight,
        opacity: 0.9
      }).bindPopup(`
        <strong>${row.road_name}</strong><br/>
        Segment type: ${row.segment_type}<br/>
        Accidents: ${row.num_accidents}<br/>
        Density: ${row.accidents_per_km} / km
      `)

      polyline.addTo(resultsLayer.value!)
      polylines.push(polyline)
    })

  })

  resultsLayer.value.addTo(map.value)
  setLegend("Accidents / km", maxDensity)

  if (polylines.length) {
    const group = L.featureGroup(polylines)
    map.value.fitBounds(group.getBounds(), { padding: [40, 40] })
  }
}

function renderBlackspotResults(rows: any[]) {
  if (!map.value) return
  if (resultsLayer.value) resultsLayer.value.remove()
  resultsLayer.value = L.layerGroup()

  const maxAccidents = Math.max(...rows.map(r => r.num_accidents || 0))

  const points: L.CircleMarker[] = []

  rows.forEach(row => {
    const match = row.structure_geom_wkt.match(/^POINT\(([^ ]+) ([^ ]+)\)$/)
    if (!match) return
    const [lon, lat] = [parseFloat(match[1]), parseFloat(match[2])]

    const radius = 6 + Math.min(10, (row.num_accidents / (maxAccidents || 1)) * 10)
    const color = getColor(row.num_accidents, maxAccidents)

    const marker = L.circleMarker([lat, lon], {
      radius,
      color,
      fillColor: color,
      fillOpacity: 0.8,
      weight: 1
    }).bindPopup(`
      <strong>${row.road_name}</strong><br/>
      Structure type: ${row.structure_type}<br/>
      Accidents: ${row.num_accidents}
    `)

    marker.addTo(resultsLayer.value!)
    points.push(marker)
  })

  resultsLayer.value.addTo(map.value)
  setLegend("Accident count", maxAccidents)

  if (points.length) {
    const group = L.featureGroup(points)
    map.value.fitBounds(group.getBounds(), { padding: [40, 40] })
  }
}

function getColor(value: number, max: number): string {
  const ratio = max > 0 ? value / max : 0
  const r = Math.floor(255 * ratio)
  const g = Math.floor(255 * (1 - ratio))
  return `rgb(${r},${g},0)`
}

watch(step, async (newStep) => {
  if (newStep === 3 && !map.value) {
    await nextTick()
    const container = document.getElementById("results-map")
    if (!container) {
      console.warn("Map container not found")
      return
    }

    map.value = L.map(container).setView([-37.81, 144.96], 12)
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap contributors"
    }).addTo(map.value)

    if (mode.value === 'corridors') renderCorridorResults(corridors.value)
    else renderBlackspotResults(blackspots.value)
  }
})

watch(step, (newStep) => {
  if (newStep !== 3 && map.value) {
    map.value.remove()
    map.value = null
    resultsLayer.value = null
    if (legendControl) {
      legendControl.remove()
      legendControl = null
    }
  }
})

/** GUARD to prevent late responses navigating UI **/
let inflightToken: symbol | null = null
const newToken = () => Symbol('inflight')
const cancelInflight = () => { inflightToken = newToken() }

/** HELPERS **/
import axios from 'axios'

async function fetchJSON<T>(
  url: string,
  options?: {
    method?: 'GET' | 'POST'
    payload?: any
    timeoutMs?: number
  }
): Promise<T> {
  const method = options?.method ?? 'GET'
  const timeout = options?.timeoutMs ?? 180000 // default 3mins
  const payload = options?.payload ?? {}

  try {
    if (method === 'POST') {
      const response = await axios.post<T>(url, payload, { timeout })
      return response.data
    } else {
      const response = await axios.get<T>(url, { timeout })
      return response.data
    }
  } catch (err: any) {
    if (axios.isAxiosError(err) && err.code === 'ECONNABORTED') {
      throw new Error('Request timed out')
    }
    throw err
  }
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
  return await fetchJSON<any[]>(url, {method: 'POST', timeoutMs: 180000}) // allow 3 min timeout
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
  return await fetchJSON<any[]>(url, {method: 'POST', timeoutMs: 180000}) // allow 3 min timeout
}

// Navigation + in-flight guarded run actions
const goTo = (n: number) => { cancelInflight(); step.value = n }
const setMode = (m: 'corridors' | 'blackspots') => {
  if (busy.value) return
  mode.value = m

  if (m === 'blackspots') {
    // Check all structure types
    const defaults = [ 'int_signal', 'level_crossing', 'int_nosignal', 'road_end', 'roundabout']
    Object.keys(state.structTypeSelected).forEach(key => {
      state.structTypeSelected[key] = defaults.includes(key)
    })
  }
}

const runCorridorsAndGo = async () => {
  if (!canRun.value || busy.value) return
  cancelInflight(); loading.results = true
  const token = newToken(); inflightToken = token
  try {
    const res = await runCorridors()
    if (inflightToken !== token) return
    corridors.value = res;
    renderCorridorResults(res);
    blackspots.value = []; step.value = 3
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
    blackspots.value = res
    renderBlackspotResults(res)
    corridors.value = []
    step.value = 3
  } catch (err) {
    console.error("Blackspot query failed:", err)
    alert("Blackspot query failed due to a timeout/internal server error. Please try again or adjust filters.")
  } finally {
    if (inflightToken === token) loading.results = false
  }
}

/** Guided tour - works with driver.js v1 or v2 */
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

.map-wrap {
  position: relative;
  margin-top: 1rem;
}
.map-container {
  height: 60vh;
  width: 100%;
  border-radius: 12px;
  overflow: hidden;
  background: #fff;
  border: 1px solid #ececec;
}
.loading-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(255,255,255,0.75);
  font-weight: 600;
  z-index: 10;
}

.info.legend {
  background: #fff;
  padding: 10px;
  font-size: 14px;
  line-height: 1.4;
  border-radius: 8px;
  box-shadow: 0 0 12px rgba(0,0,0,.18);
  border: 1px solid #e5e7eb;
}
.info.legend h4 {
  margin: 0 0 6px;
  font-weight: 900;
  font-size: 13px;
  color: #0f1419;
}
.info.legend i {
  width: 24px;
  height: 14px;
  display: inline-block;
  margin-right: 8px;
}

.no-results-overlay {
  position: absolute;
  inset: 0;
  background: rgba(255,255,255,0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
  pointer-events: none;
}

.no-results-message {
  text-align: center;
  background: #fff;
  padding: 16px 24px;
  border-radius: 12px;
  box-shadow: 0 0 12px rgba(0,0,0,0.1);
  max-width: 300px;
}

</style>
