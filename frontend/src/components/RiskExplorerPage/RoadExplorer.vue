<template>
  <div class="rx">
    <!-- Filters -->
    <div class="filters">
      <label>
        <span>Region type</span>
        <select v-model="saLevel" :disabled="loading">
          <option value="sa3">Area (SA3)</option>
          <option value="sa2">Suburb (SA2)</option>
        </select>
      </label>

      <label>
        <span>Region name</span>
        <select v-model="saName" :disabled="loading || loadingNames || !names.length">
          <option disabled value="">{{ loadingNames ? "Loading…" : "Select region" }}</option>
          <option v-for="n in names" :key="n" :value="n">{{ n }}</option>
        </select>
      </label>

      <label>
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

      <label>
        <span>From</span>
        <input type="date" v-model="dateFrom" :disabled="loading" @keyup.enter="onSearch" />
      </label>

      <label>
        <span>To</span>
        <input type="date" v-model="dateTo" :disabled="loading" @keyup.enter="onSearch" />
      </label>

      <label>
        <span>Metric</span>
        <select v-model="metric" :disabled="loading">
          <option value="accident_count">Accident count</option>
          <option value="accident_density_per_km">Accidents / km</option>
        </select>
      </label>

      <label>
        <span>Limit roads</span>
        <input type="number" v-model.number="limit" min="1" max="100" :disabled="loading" @keyup.enter="onSearch" />
      </label>

      <div class="actions">
        <button class="btn" :disabled="loading || !canSearch" @click="onSearch">
          {{ loading ? 'Searching…' : 'Search' }}
        </button>
        <small v-if="hasPending && !loading" class="dirty">Filters changed — press Search</small>
      </div>
    </div>

    <!-- Map + loading overlay -->
    <div class="map-wrap">
      <div id="roads-map" class="map-container"></div>

      <div v-if="loading" class="loading-overlay" aria-live="polite">
        <span class="spinner"></span>
        <div>Fetching roads…</div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from "vue"
import axios from "axios"
import L from "leaflet"

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
const roadsLayer = ref(null)

/* loading + request cancellation */
const loading = ref(false)
let abortCtrl = null
let reqToken = 0

/* “pending changes” + ready gate */
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

/* --- your helpers for rendering --- */
function parseLineWKT(wkt) {
  if (!wkt || typeof wkt !== "string") return null
  const isMulti = /^MULTILINESTRING/i.test(wkt)
  const clean = wkt.replace(/^(MULTI)?LINESTRING\s*/i, "").replace(/^\(+|\)+$/g, "").trim()
  const toLine = (s) => s.split(",").map((pair) => {
    const [lon, lat] = pair.trim().split(/\s+/).map(Number)
    return [lat, lon]
  })
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

/* --- your fetch --- */
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
      timeout: 30000,
    })

    if (token !== reqToken) return
    renderRoads(data)
  } catch (e) {
    if (axios.isCancel?.(e) || e?.name === "CanceledError") return
    console.error(e)
  } finally {
    if (token === reqToken) loading.value = false
  }
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

  await loadNames()
  if (saName.value) await fetchRoads()
  ready.value = true
})

/* don’t auto-fetch; just mark “pending” when filters change */
watch(saLevel, async () => {
  await loadNames()
  if (ready.value) hasPending.value = true
})
watch([saName, roadType, dateFrom, dateTo, metric, limit], () => {
  if (ready.value) hasPending.value = true
})
</script>

<style scoped>/* ===== Filter panel (yellow box) ===== */
:root{
  --panel-bg:   #fff3cd;  /* pale yellow */
  --panel-bdr:  #f7e39c;  /* soft gold border */
}

.rx { display: grid; gap: 10px; }


/* =============== Filter panel (yellow card) =============== */
.filters{
  /* card look */
  background:#fff3cd;                 /* pale yellow */
  border:1px solid #f7e39c;           /* soft gold edge */
  border-radius:12px;
  padding:12px 14px;
  box-shadow:0 1px 0 rgba(0,0,0,.03) inset;

  /* layout */
  display:grid;
  grid-template-columns: repeat(6, minmax(180px, 1fr));
  column-gap:16px;
  row-gap:12px;
  align-items:end;
}

/* label + control blocks */
.filters > label{
  display:grid;
  gap:6px;
  min-width:0;                        /* prevent overlap when tight */
}
.filters > label > span{
  color:#555;
  font-weight:700;
  font-size:12px;
}

/* inputs */
.filters select,
.filters input[type="date"],
.filters input[type="text"],
.filters input[type="number"]{
  width:100%;
  box-sizing:border-box;
  padding:10px 12px;
  border:1px solid #cbd5e1;
  border-radius:8px;
  background:#fff;
}

/* action area (e.g., Search button) */
.filters .actions{
  display:flex;
  align-items:end;
  gap:10px;
}

.filters .btn:disabled{ opacity:.6; cursor:not-allowed; }
/* action area (e.g., Search button) */
.actions{
  display: flex;
  align-items: center;
  gap: 10px;
  align-self: end;
}

/* primary button */
.btn{
  padding: 10px 16px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  background: #111;
  color: #f6b300;
  font-weight: 800;
}
.btn:disabled{ opacity: .6; cursor: not-allowed; }
.dirty{ color:#7a5a00; font-weight:700; }

/* ===== Map & loading (unchanged) ===== */
.map-wrap{ position: relative; }
.map-container{
  height: 600px; width: 100%;
  border-radius: 12px; overflow: hidden; background: #fff;
  box-shadow: 0 2px 10px rgba(0,0,0,.06);
  border: 1px solid #ececec;
}

/* loading overlay */
.loading-overlay{
  position: absolute; inset: 0;
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

/* legend (global) */
:global(.info.legend){
  background:#fff; padding:10px; font-size:14px; line-height:1.4;
  border-radius:6px; box-shadow:0 0 10px rgba(0,0,0,.2);
}
:global(.info.legend h4){ margin:0 0 6px; font-weight:700; }
:global(.info.legend i){ width:24px; height:14px; display:inline-block; margin-right:8px; }

/* ===== Responsive tweaks ===== */
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
