<template>
  <div class="rx">
    <!-- Header -->
    <div class="rx-topbar">
      <div>
        <div class="eyebrow">Analytics</div>
        <h1 class="title">Regional Crash Heatmap</h1>
        <div class="sub">Pick a region, group results, and colour the map by the metric.</div>
      </div>
      <button class="tour-btn" @click="startTour">❓ Tour</button>
    </div>

    <!-- Filter bar -->
    <div class="filters" id="tour-filters">
      <label id="tour-level">
        <span>Region type</span>
        <select v-model="filterAreaLevel">
          <option value="sa4">Regional Zone (SA4)</option>
          <option value="sa3">Area (SA3)</option>
          <option value="sa2">Suburb (SA2)</option>
        </select>
      </label>

      <label id="tour-name">
        <span>Region name</span>
        <select v-model="filterAreaName" :disabled="loadingNames || !names.length">
          <option disabled value="">{{ loadingNames ? 'Loading…' : 'Select region' }}</option>
          <option v-for="n in names" :key="n" :value="n">{{ n }}</option>
        </select>
      </label>

      <label id="tour-group">
        <span>Group by</span>
        <select v-model="groupByAreaLevel">
          <option v-for="g in groupOptions" :key="g.value" :value="g.value">{{ g.label }}</option>
        </select>
      </label>

      <label id="tour-from">
        <span>From</span>
        <input type="date" v-model="dateFrom" />
      </label>

      <label id="tour-to">
        <span>To</span>
        <input type="date" v-model="dateTo" />
      </label>

      <label id="tour-metric">
        <span>Metric</span>
        <select v-model="colorMetric">
          <option value="num_accs">Accident Count</option>
          <option value="acc_per_sq_km">Accidents per km²</option>
        </select>
      </label>
    </div>

    <!-- Map -->
    <div id="map" class="map-container" />
  </div>
</template>

<script setup>
import { onMounted, ref, watch, computed } from 'vue'
import axios from 'axios'
import L from 'leaflet'

/* Guided tour (version-agnostic: works with driver.js v1 or v2) */
import * as DriverNS from 'driver.js'
import 'driver.js/dist/driver.css'

/* ----------- state ----------- */
const API = import.meta.env.VITE_API_BASE ?? '/api'

const colorMetric = ref('num_accs')
const map = ref(null)
const geoLayer = ref(null)
const regions = ref([])

/* ----------- filters ----------- */
const filterAreaLevel = ref('sa3')  // 'sa2' | 'sa3' | 'sa4'
const filterAreaName  = ref('')
const groupByAreaLevel = ref('sa2') // constrained by filterAreaLevel
const dateFrom        = ref('2020-01-01')
const dateTo          = ref('2024-12-31')

const names = ref([])
const loadingNames = ref(false)

/* group options depend on region level */
const groupOptions = computed(() => {
  if (filterAreaLevel.value === 'sa4') {
    return [
      { value: 'sa3', label: 'Area (SA3)' },
      { value: 'sa2', label: 'Suburb (SA2)' },
    ]
  }
  if (filterAreaLevel.value === 'sa3') {
    return [{ value: 'sa2', label: 'Suburb (SA2)' }]
  }
  return [{ value: 'sa2', label: 'Suburb (SA2)' }]
})

/* load distinct names for the chosen level */
async function loadNamesForLevel () {
  loadingNames.value = true
  try {
    const endpoint =
      filterAreaLevel.value === 'sa4' ? '/distinct_sa4' :
        filterAreaLevel.value === 'sa3' ? '/distinct_sa3' : '/distinct_sa2'
    const { data } = await axios.get(`${API}${endpoint}`)
    names.value = data
    if (!names.value.includes(filterAreaName.value)) {
      filterAreaName.value = names.value[0] || ''
    }
  } finally {
    loadingNames.value = false
  }
}

/* keep groupBy valid when level changes */
watch(filterAreaLevel, async () => {
  const valid = groupOptions.value.map(o => o.value)
  if (!valid.includes(groupByAreaLevel.value)) {
    groupByAreaLevel.value = valid[0]
  }
  await loadNamesForLevel()
  await fetchAccidentStats()
})

/* ----------- API + map rendering ----------- */
async function fetchAccidentStats() {
  try {
    const response = await axios.post(`${API}/accident_stats`, {
      filter_area_level:    filterAreaLevel.value,
      filter_area_name:     filterAreaName.value,
      group_by_area_level:  groupByAreaLevel.value,
      date_from:            dateFrom.value,
      date_to:              dateTo.value,
      order_by:             colorMetric.value === 'num_accs' ? 'count' : 'density',
      order_dir:            'desc',
      limit:                100,
    })
    regions.value = response.data
    renderPolygons()
    centerMapOnBounds()
  } catch (err) {
    console.error('Failed to fetch accident stats:', err)
  }
}

function centerMapOnBounds() {
  if (!regions.value.length || !map.value) return
  const polygons = regions.value.map((region) => L.polygon(parseGeometry(region.geom)))
  const group = L.featureGroup(polygons)
  const bounds = group.getBounds()
  map.value.flyToBounds(bounds, { padding: [40, 40], duration: 1.2 })
}

function getColor(value, max) {
  const ratio = max ? (value / max) : 0
  const r = Math.floor(255 * ratio)
  const g = Math.floor(255 * (1 - ratio))
  return `rgb(${r},${g},0)`
}

function parseGeometry(geomStr) {
  if (!geomStr || typeof geomStr !== 'string') return []
  const isMulti = geomStr.startsWith('MULTIPOLYGON')
  const cleaned = geomStr.replace(/(MULTIPOLYGON|POLYGON)\s*/i, '').replace(/^\(+|\)+$/g, '').trim()
  const ringGroups = isMulti ? cleaned.split(')),((') : [cleaned.replace(/^\(+|\)+$/g, '')]
  const parsed = ringGroups.map((ring) =>
    ring.split(',').map((pair) => {
      const [lonStr, latStr] = pair.trim().split(/\s+/)
      const lon = parseFloat(lonStr); const lat = parseFloat(latStr)
      if (isNaN(lat) || isNaN(lon)) return null
      return [lat, lon]
    }).filter(Boolean)
  )
  return isMulti ? [parsed] : parsed
}

function isMultiPolygon(coords) { return Array.isArray(coords[0][0]) }

let legendControl = null
function addLegend(maxValue) {
  if (legendControl) legendControl.remove()
  legendControl = L.control({ position: 'bottomright' })
  legendControl.onAdd = () => {
    const div = L.DomUtil.create('div', 'info legend')
    const grades = [0, 0.2, 0.4, 0.6, 0.8, 1]
    const labels = grades.map((g) => {
      const value = Math.round(g * maxValue)
      return `<i style="background:${getColor(value, maxValue)}"></i> ${value}`
    })
    div.innerHTML = `<h4>${colorMetric.value === 'num_accs' ? 'Accident Count' : 'Accidents/km²'}</h4>${labels.join('<br>')}`
    return div
  }
  legendControl.addTo(map.value)
}

function renderPolygons() {
  if (!map.value || regions.value.length === 0) return
  if (geoLayer.value) geoLayer.value.remove()

  const maxVal = Math.max(...regions.value.map((r) => r[colorMetric.value]))
  geoLayer.value = L.layerGroup()

  regions.value.forEach((region) => {
    const coords = parseGeometry(region.geom)
    const polygon = isMultiPolygon(coords) ? L.polygon(coords) : L.polygon([coords])
    polygon.setStyle({ color: '#333', weight: 1, fillColor: getColor(region[colorMetric.value], maxVal), fillOpacity: 0.6 })
    polygon.bindPopup(`
      <strong>${region.sa_name}</strong><br>
      Accidents: ${region.num_accs}<br>
      Acc/km²: ${Number(region.acc_per_sq_km).toFixed(2)}<br>
    `)
    geoLayer.value.addLayer(polygon)
  })

  geoLayer.value.addTo(map.value)
  addLegend(maxVal)
}

/* ----------- lifecycle / watchers ----------- */
onMounted(async () => {
  map.value = L.map('map', { zoomControl: true }).setView([-38.2, 144.2], 9)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
  }).addTo(map.value)

  await loadNamesForLevel()
  if (filterAreaName.value) await fetchAccidentStats()

  // Optional: auto-show tour first visit
  if (!localStorage.getItem('heatmapTourSeen')) {
    setTimeout(startTour, 400)
  }
})

watch(colorMetric, renderPolygons)
watch([filterAreaName, groupByAreaLevel, dateFrom, dateTo], fetchAccidentStats)

/* ----------- Guided tour ----------- */
function startTour() {
  try {
    const options = {
      showProgress: true,
      animate: true,
      opacity: 0.4,
      nextBtnText: 'Next',
      prevBtnText: 'Back',
      doneBtnText: 'Done',
      stagePadding: 6,
      allowClose: true,
    }

    // Build steps only for elements that exist to avoid “top-left” popovers
    const maybe = (selector, popover) =>
      document.querySelector(selector) ? { element: selector, popover } : null

    const steps = [
      maybe('#tour-filters', { title: 'Filters', description: 'Pick your region, grouping level, dates and metric.' }),
      maybe('#tour-level',   { title: 'Region type', description: 'Choose SA4(Regional Zone), SA3(Area) or SA2(Suburb) scope for the filter.' }),
      maybe('#tour-name',    { title: 'Region name', description: 'Select the specific region to analyse.' }),
      maybe('#tour-group',   { title: 'Group by', description: 'Aggregate results to SA3(Area) or SA2(Suburb) polygons.' }),
      maybe('#tour-from',    { title: 'Start date', description: 'Limit the period by start date.' }),
      maybe('#tour-to',      { title: 'End date', description: 'Limit the period by end date.' }),
      maybe('#tour-metric',  { title: 'Metric', description: 'Colour polygons by crash count or density.' }),
      maybe('#map',          { title: 'Map', description: 'Hover for values, click polygons for details.' }),
    ].filter(Boolean)

    if (!steps.length) { alert('Open the page and then click Tour again.'); return }

    // v2 API
    if (typeof (DriverNS).driver === 'function') {
      const d = (DriverNS).driver(options)
      if (typeof d.setSteps === 'function') d.setSteps(steps)
      else if (typeof d.defineSteps === 'function') d.defineSteps(steps)
      else d.steps = steps
      if (typeof d.drive === 'function') d.drive()
      localStorage.setItem('heatmapTourSeen', '1')
      return
    }

    // v1 API
    const DriverCtor = (DriverNS).default || (DriverNS)
    const d = new DriverCtor(options)
    if (typeof d.defineSteps === 'function') d.defineSteps(steps)
    else if (typeof d.setSteps === 'function') d.setSteps(steps)
    else d.steps = steps
    if (typeof d.start === 'function') d.start()
    else if (typeof d.drive === 'function') d.drive()
    localStorage.setItem('heatmapTourSeen', '1')
  } catch (e) {
    console.warn('driver.js failed to start', e)
    alert('To launch the guided tour, please install driver.js:\n\n  npm i driver.js')
  }
}
</script>

<style scoped>
.rx { display: grid; gap: 12px; }

/* Header */
.rx-topbar{
  display:flex; align-items:center; justify-content:space-between;
  gap:12px; padding:6px 2px;
}
.eyebrow{ text-transform:uppercase; letter-spacing:.08em; font-size:12px; color:#6b7280; font-weight:700; }
.title{ margin:2px 0 0; font-size:22px; font-weight:900; color:#0f1419; }
.sub{ color:#6b7280; }

/* Tour button styled to theme */
.tour-btn{
  padding:8px 12px; border-radius:10px; border:1px solid #e5e7eb;
  background:#fff; color:#111; font-weight:700; cursor:pointer;
}
.tour-btn:hover{ background:#fff7cc; border-color:#f6b300; }

/* Filter bar styling to match theme */
.filters{
  background:#fffdf2;             /* softer than pure yellow */
  border:2px solid #f7e39c;
  border-radius:12px;
  padding:10px;
  display:grid;
  gap:12px;
  grid-template-columns: repeat(6, minmax(180px, 1fr));
  overflow: visible;               /* ensure tour popovers aren’t clipped */
}
label{ display:grid; gap:6px; font-size:14px; }
label > span{ color:#374151; font-weight:800; font-size:12px; }

select, input[type="date"]{
  padding:10px 12px;
  border:1px solid #cbd5e1;
  border-radius:10px;
  background:#fff;
  font-weight:600;
}
select:focus, input[type="date"]:focus{
  outline:none; border-color:#f6b300; box-shadow:0 0 0 .2rem rgba(246,179,0,.25);
  background:#fff;
}

/* Map */
.map-container {
  height: 600px;
  width: 100%;
  border-radius:12px;
  overflow:hidden;
  background:#fff;
  box-shadow:0 2px 10px rgba(0,0,0,.06);
  border:1px solid #ececec;
  position: relative;
  z-index: 0;
}

/* Legend + popup */
:global(.info.legend) {
  background: white;
  padding: 10px;
  font-size: 14px;
  line-height: 1.4;
  border-radius: 8px;
  box-shadow: 0 0 12px rgba(0,0,0,0.18);
  border: 1px solid #e5e7eb;
}
:global(.info.legend h4) { margin: 0 0 6px; font-weight: 900; font-size:13px; color:#0f1419; }
:global(.info.legend i)  { width: 26px; height: 18px; display: inline-block; margin-right: 8px; background: #ccc; vertical-align: middle; }

/* Responsive */
@media (max-width: 1200px) {
  .filters { grid-template-columns: repeat(3, minmax(180px, 1fr)); }
}
@media (max-width: 720px) {
  .filters { grid-template-columns: 1fr; }
}
</style>
