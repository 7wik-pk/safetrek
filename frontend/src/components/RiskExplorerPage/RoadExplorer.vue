<template>
  <div class="rx">

    <!-- Header -->
    <div class="rx-topbar">
      <div>
        <div class="eyebrow">Analytics</div>
        <h1 class="title">Road Corridor Risk (by Road Type)</h1>
        <div class="sub">Choose a region and filters, then draw risk-weighted road lines on the map.</div>
      </div>
      <button class="tour-btn" @click="startTour">❓ Tour</button>
    </div>

    <!-- Filters -->
    <div class="filters" id="tour-filters">
      <label id="tour-level">
        <span>Region type</span>
        <select v-model="saLevel" :disabled="loading">
          <option value="sa3">Area (SA3)</option>
          <option value="sa2">Suburb (SA2)</option>
        </select>
      </label>

      <label id="tour-name">
        <span>Region name</span>
        <select v-model="saName" :disabled="loading || loadingNames || !names.length">
          <option disabled value="">{{ loadingNames ? "Loading..." : "Select region" }}</option>
          <option v-for="n in names" :key="n" :value="n">{{ n }}</option>
        </select>
      </label>

      <label id="tour-roadtype">
        <span>Road type</span>
        <select v-model="roadType" :disabled="loading">
          <option value="major">Major</option>
          <option value="suburban">Suburban</option>
          <option value="rural_and_low_traffic">Rural & low traffic</option>
          <option value="infrastructure">Infrastructure</option>
          <option value="commerical_and_civic">Commercial & civic</option>
          <option value="pedestrian_and_recreational_paths">Pedestrian & rec. paths</option>
        </select>
      </label>

      <label id="tour-from">
        <span>From</span>
        <input type="date" v-model="dateFrom" :disabled="loading" @keyup.enter="onSearch" />
      </label>

      <label id="tour-to">
        <span>To</span>
        <input type="date" v-model="dateTo" :disabled="loading" @keyup.enter="onSearch" />
      </label>

      <label id="tour-metric">
        <span>Metric</span>
        <select v-model="metric" :disabled="loading">
          <option value="accident_count">Accident count</option>
          <option value="accident_density_per_km">Accidents / km</option>
        </select>
      </label>

      <label id="tour-limit">
        <span>Limit roads</span>
        <input type="number" v-model.number="limit" min="1" max="100" :disabled="loading" @keyup.enter="onSearch" />
      </label>

      <div class="actions" id="tour-actions">
        <button class="btn" :disabled="loading || !canSearch" @click="onSearch">
          {{ loading ? 'Searching...' : 'Search' }}
        </button>
        <small v-if="hasPending && !loading" class="dirty">Filters changed — press Search</small>
      </div>
    </div>

    <!-- Map + loading overlay -->
    <div class="map-wrap">
      <div id="roads-map" class="map-container" />
      <div v-if="loading" class="loading-overlay" aria-live="polite">
        <span class="spinner"></span>
        <div class="muted">
          Fetching roads...
          <br/>
          <small>[These queries can take up to 2 minutes depending on filters and volume of data]</small>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch, computed, nextTick } from "vue"
import axios from "axios"
import L from "leaflet"
import "leaflet/dist/leaflet.css"

/* Guided tour (version-agnostic: works with driver.js v1 or v2) */
import * as DriverNS from "driver.js"
import "driver.js/dist/driver.css"

const API = import.meta.env.VITE_API_BASE ?? "/api"

/* filters */
const saLevel  = ref("sa3")
const saName   = ref("")
const roadType = ref("major")
const dateFrom = ref("2023-01-01")
const dateTo   = ref("2024-12-31")
const metric   = ref("accident_density_per_km")
const limit    = ref(50)

const names = ref([])
const loadingNames = ref(false)

/* map */
const map = ref(null)
let resizeObserver = null
const roadsLayer = ref(null)

/* loading + request cancellation */
const loading = ref(false)
let abortCtrl = null
let reqToken = 0

/* "pending changes" + ready gate */
const hasPending = ref(false)
const ready = ref(false)
const canSearch = computed(() => !!saName.value)

/* --- name list --- */
async function loadNames() {
  loadingNames.value = true
  try {
    const ep = saLevel.value === "sa3" ? "/distinct_sa3" : "/distinct_sa2"
    const { data } = await axios.get(`${API}${ep}`)
    names.value = data
    if (!names.value.includes(saName.value)) saName.value = names.value[0] || ""
  } finally {
    loadingNames.value = false
  }
}

/* --- geometry + render helpers --- */
function parseLineWKT(wkt) {
  if (!wkt || typeof wkt !== "string") return null
  const isMulti = /^MULTILINESTRING/i.test(wkt)
  const clean = wkt.replace(/^(MULTI)?LINESTRING\s*/i, "").replace(/^\(+|\)+$/g, "").trim()
  const toLine = (s) => s.split(",").map((pair) => {
    const [lon, lat] = pair.trim().split(/\s+/).map(Number)
    return [lat, lon]
  }).filter(Boolean)
  if (isMulti) return clean.split(/\)\s*,\s*\(/).map(toLine)
  return toLine(clean)
}

function getColor(value, max) {
  const ratio = max > 0 ? value / max : 0
  const r = Math.floor(255 * ratio)
  const g = Math.floor(255 * (1 - ratio))
  return `rgb(${r},${g},0)`
}

let legendControl = null
function setLegend(maxVal) {
  if (legendControl) legendControl.remove()
  legendControl = L.control({ position: "bottomright" })
  legendControl.onAdd = () => {
    const div = L.DomUtil.create("div", "info legend")
    const title = metric.value === "accident_count" ? "Accident count" : "Accidents / km"
    const grades = [0, 0.2, 0.4, 0.6, 0.8, 1]
      .map((g) => Math.round(g * maxVal))
      .filter((v, i, arr) => i === 0 || v !== arr[i - 1])
    div.innerHTML = `<h4>${title}</h4>` + grades.map((v) => {
      const c = getColor(v, maxVal)
      return `<i style="background:${c}"></i> ${v}`
    }).join("<br>")
    return div
  }
  legendControl.addTo(map.value)
}

function renderRoads(rows) {
  if (!map.value) return
  if (roadsLayer.value) roadsLayer.value.remove()
  roadsLayer.value = L.layerGroup()

  const key = metric.value
  const maxVal = rows.length ? Math.max(...rows.map((r) => Number(r[key] || 0))) : 0

  const polys = []
  rows.forEach((r) => {
    const line = parseLineWKT(r.road_geom)
    if (!line) return

    const color = getColor(Number(r[key] || 0), maxVal)
    const weight = 3 + Math.min(7, (Number(r[key] || 0) / (maxVal || 1)) * 7)

    const add = (coords) => {
      const pl = L.polyline(coords, { color, weight, opacity: 0.9 })
      pl.bindPopup(`
        <strong>${r.road_name || "Unnamed road"}</strong><br/>
        Crashes: ${Number(r.accident_count || 0)}<br/>
        Length: ${Number(r.road_length_km || 0).toFixed(2)} km<br/>
        Density: ${Number(r.accident_density_per_km || 0).toFixed(2)} /km
      `)
      roadsLayer.value.addLayer(pl)
      polys.push(pl)
    }

    Array.isArray(line[0]) && Array.isArray(line[0][0]) ? line.forEach(add) : add(line)
  })

  roadsLayer.value.addTo(map.value)
  setLegend(maxVal)

  if (polys.length) {
    const group = L.featureGroup(polys)
    map.value.fitBounds(group.getBounds(), { padding: [40, 40], duration: 1.0 })
  }
}

/* --- fetch --- */
async function fetchRoads() {
  if (!saName.value) return
  if (abortCtrl) abortCtrl.abort()
  abortCtrl = new AbortController()
  const token = ++reqToken

  loading.value = true
  try {
    const payload = {
      sa_level: saLevel.value,
      sa_name: saName.value,
      road_type: roadType.value,
      date_from: dateFrom.value,
      date_to: dateTo.value,
      min_road_length_km: 0.2,
      order_by: metric.value,
      order_desc: true,
      limit: Math.min(100, Math.max(1, Number(limit.value) || 1)),
    }

    const { data } = await axios.post(`${API}/road_accident_density`, payload, {
      signal: abortCtrl.signal,
      timeout: 120000,
    })

    if (token !== reqToken) return
    renderRoads(data)
    centerMapOnRoads()
  } catch (e) {
    if (axios.isCancel?.(e) || e?.name === "CanceledError") return
    console.error(e)
  } finally {
    if (token === reqToken) loading.value = false
  }
}

function centerMapOnRoads() {
  if (!map.value || !roadsLayer.value) return
  const polylines = []
  roadsLayer.value.eachLayer((layer) => {
    if (layer instanceof L.Polyline) polylines.push(layer)
  })
  if (!polylines.length) return
  const group = L.featureGroup(polylines)
  const bounds = group.getBounds()
  map.value.flyToBounds(bounds, { padding: [40, 40], duration: 1.2 })
}

/* Button handler */
function onSearch() {
  hasPending.value = false
  fetchRoads()
}

/* lifecycle */
onMounted(async () => {
  map.value = L.map("roads-map").setView([-37.81, 144.96], 9)
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors",
  }).addTo(map.value)

  resizeObserver = new ResizeObserver(() => map.value?.invalidateSize())
  nextTick(() => {
    const container = map.value?.getContainer?.()
    if (container) {
      resizeObserver.observe(container)
      map.value.invalidateSize()
      centerMapOnRoads()
    }
  })

  await loadNames()
  if (saName.value) await fetchRoads()
  ready.value = true
})

onBeforeUnmount(() => {
  try { resizeObserver?.disconnect() } catch {}
})

/* mark "pending" when filters change */
watch(saLevel, async () => {
  await loadNames()
  if (ready.value) {
    hasPending.value = true
    saName.value = names.value[0]
    roadType.value = saLevel.value === 'sa2' ? 'suburban' : 'major'
  }
})
watch([saName, roadType, dateFrom, dateTo, metric, limit], () => {
  if (ready.value) hasPending.value = true
})

/* -------- Guided tour (robust targets + recenter) -------- */
function startTour() {
  try {
    const options: any = {
      showProgress: true,
      animate: true,
      opacity: 0.4,
      stagePadding: 6,
      allowClose: true,
      nextBtnText: 'Next',
      prevBtnText: 'Back',
      doneBtnText: 'Done',
    };

    // helper: return a step only if the element exists & is visible
    const step = (selector: string, title: string, description: string) => {
      const el = document.querySelector(selector) as HTMLElement | null;
      if (!el) return null;

      const recenter = () => {
        // make sure it’s in view (works for window-scrolling pages)
        try { el.scrollIntoView({ block: 'center', inline: 'center', behavior: 'instant' as any }); } catch {}
      };

      return {
        element: el,                                  // pass the node, not the selector
        popover: { title, description, side: 'bottom', align: 'start' }, // v2 props
        // v2 callback name:
        onHighlightStarted: recenter,
        // v1 callback name (kept too for compatibility):
        onHighlighted: recenter,
      };
    };

    const steps = [
      step('#tour-filters',   'Filters',        'Choose region, road type, dates, and metric.'),
      step('#tour-level select',    'Region type',   'Pick Area (SA3) or Suburb (SA2).'),
      step('#tour-name select',     'Region name',   'Select the specific region to analyse.'),
      step('#tour-roadtype select', 'Road type',     'Limit results to a road category.'),
      step('#tour-from input[type="date"]', 'Start date', 'Set the beginning of the time window.'),
      step('#tour-to input[type="date"]',   'End date',   'Set the end of the time window.'),
      step('#tour-metric select',   'Metric',        'Colour/weight lines by crashes or crashes per km.'),
      step('#tour-limit input',     'Limit roads',   'Cap how many roads to draw on the map.'),
      step('#tour-actions .btn',    'Run search',    'Click Search to fetch and render the roads.'),
      step('#roads-map',            'Map',           'Hover for values; click lines for details.'),
    ].filter(Boolean);

    if (!steps.length) {
      alert('Open the page and then click Tour again.');
      return;
    }

    // v2 API
    if (typeof (DriverNS as any).driver === 'function') {
      const d = (DriverNS as any).driver(options);
      if (typeof (d as any).setSteps === 'function') (d as any).setSteps(steps);
    else if (typeof (d as any).defineSteps === 'function') (d as any).defineSteps(steps);
    else (d as any).steps = steps;
      if (typeof (d as any).drive === 'function') (d as any).drive();
      return;
    }

    // v1 API
    const DriverCtor: any = (DriverNS as any).default || (DriverNS as any);
    const d = new DriverCtor(options);
    if (typeof d.defineSteps === 'function') d.defineSteps(steps);
    else if (typeof d.setSteps === 'function') d.setSteps(steps);
    else (d as any).steps = steps;
    if (typeof d.start === 'function') d.start();
    else if (typeof (d as any).drive === 'function') (d as any).drive();
  } catch (e) {
    console.warn('driver.js failed to start', e);
    alert('To launch the guided tour, please install driver.js:\n\n  npm i driver.js');
  }
}

</script>

<style scoped>
/* ===== Header ===== */
.rx { display: grid; gap: 12px; }

.rx-topbar{
  display:flex; align-items:center; justify-content:space-between;
  gap:12px; padding:6px 2px;
}
.eyebrow{ text-transform:uppercase; letter-spacing:.08em; font-size:12px; color:#6b7280; font-weight:700; }
.title{ margin:2px 0 0; font-size:22px; font-weight:900; color:#0f1419; }
.sub{ color:#6b7280; }
.tour-btn{
  padding:8px 12px; border-radius:10px; border:1px solid #e5e7eb;
  background:#fff; color:#111; font-weight:800; cursor:pointer;
}
.tour-btn:hover{ background:#fff7cc; border-color:#f6b300; }

/* ===== Filter panel (yellow card) ===== */
.filters{
  background:#fff3cd;                 /* pale yellow */
  border:1px solid #f7e39c;           /* soft gold edge */
  border-radius:12px;
  padding:12px 14px;
  box-shadow:0 1px 0 rgba(0,0,0,.03) inset;

  display:grid;
  grid-template-columns: repeat(6, minmax(180px, 1fr));
  column-gap:16px; row-gap:12px;
  align-items:end;

  overflow: visible; /* let tour popovers show fully */
}
.filters > label{ display:grid; gap:6px; min-width:0; }
.filters > label > span{ color:#555; font-weight:800; font-size:12px; }
.filters select,
.filters input[type="date"],
.filters input[type="number"]{
  width:100%; box-sizing:border-box; padding:10px 12px;
  border:1px solid #cbd5e1; border-radius:8px; background:#fff; font-weight:600;
}
.filters select:focus,
.filters input[type="date"]:focus,
.filters input[type="number"]:focus{
  outline:none; border-color:#f6b300; box-shadow:0 0 0 .2rem rgba(246,179,0,.25);
  background:#fff;
}

.actions{ display:flex; align-items:center; gap:10px; align-self:end; }
.btn{
  padding:10px 16px; border:none; border-radius:10px; cursor:pointer;
  background:#111; color:#f6b300; font-weight:800;
}
.btn:disabled{ opacity:.6; cursor:not-allowed; }
.dirty{ color:#7a5a00; font-weight:700; }

/* ===== Map & loading ===== */
.map-wrap{ position: relative; }
.map-container{
  height: 60vh; width: 100%;
  border-radius: 12px; overflow: hidden; background: #fff;
  box-shadow: 0 2px 10px rgba(0,0,0,.06);
  border: 1px solid #ececec;
  position: relative;
  z-index: 0; /* let Driver.js overlay sit above */
}
.loading-overlay{
  position: absolute; inset: 0;
  text-align: center;
  z-index: 10;
  display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px;
  background: rgba(255,255,255,.75); backdrop-filter: blur(1px);
  font-weight: 700; color: #111;
}
.spinner{
  width: 52px; height: 52px; border-radius: 50%;
  border: 6px solid rgba(246,179,0,.25);
  border-top-color: #005ef6; animation: spin 1s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.filters { overflow: visible; }
.map-container { position: relative; z-index: 0; }

/* v2 + v1 popovers above everything */
:deep(.driver-popover),
:deep(.driver-popover-item) { z-index: 2147483647 !important; }

/* Legend */
:global(.info.legend){
  background:#fff; padding:10px; font-size:14px; line-height:1.4;
  border-radius:8px; box-shadow:0 0 12px rgba(0,0,0,.18); border:1px solid #e5e7eb;
}
:global(.info.legend h4){ margin:0 0 6px; font-weight:900; font-size:13px; color:#0f1419; }
:global(.info.legend i){ width:24px; height:14px; display:inline-block; margin-right:8px; }

/* ===== Responsive ===== */
@media (max-width: 1100px){
  .filters{ grid-template-columns: repeat(3, minmax(200px, 1fr)); }
}
@media (max-width: 640px){
  .filters{ grid-template-columns: repeat(2, minmax(160px, 1fr)); }
}
@media (max-width: 420px){
  .filters{ grid-template-columns: 1fr; }
}
</style>
