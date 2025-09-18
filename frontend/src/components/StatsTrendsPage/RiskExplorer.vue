<template>
  <section class="page">
    <header class="panel">
      <div class="row">
        <label>
          Region type
          <select v-model="filterAreaLevel">
            <option value="sa4">Regional Zone (SA4)</option>
            <option value="sa3">Area (SA3)</option>
            <option value="sa2">Suburb (SA2)</option>
          </select>
        </label>

        <label>
          Region name
          <select v-model="filterAreaName" :disabled="loadingNames || !names.length">
            <option disabled value="">{{ loadingNames ? 'Loading…' : 'Select a region' }}</option>
            <option v-for="n in names" :key="n" :value="n">{{ n }}</option>
          </select>
        </label>

        <label>
          Group by
          <select v-model="groupBy">
            <option v-for="g in groupOptions" :key="g.value" :value="g.value">{{ g.label }}</option>
          </select>
        </label>

        <label>
          From
          <input type="date" v-model="dateFrom" />
        </label>
        <label>
          To
          <input type="date" v-model="dateTo" />
        </label>

        <label>
          Metric
          <select v-model="metric">
            <option value="density">Density (/km²)</option>
            <option value="count">Crashes (count)</option>
          </select>
        </label>
      </div>
      <div v-if="err" class="error">{{ err }}</div>
    </header>

    <div class="map-wrap">
      <div ref="mapEl" class="map-container"></div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, watch, computed, nextTick } from 'vue'
// import mapboxgl from 'mapbox-gl'
// import 'mapbox-gl-css'

import axios from 'axios'
import L from 'leaflet'

// ---------- API & Mapbox ----------
const API = import.meta.env.VITE_API_BASE ?? '/api'
// mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN || 'pk.eyJ1IjoiY2hhcmxpZWVlMTkiLCJhIjoiY205ZHZjc2ttMTg0NzJscTE0MzRyYXlpYSJ9.-EKrTcL6Q_Wk1KvmrS_25g'

// Leaflet functions

function centerMapOnBounds() {
  if (!regions.value.length || !map.value) return

  const polygons = regions.value.map((region) => {
    const coords = parseGeometry(region.geom)
    return L.polygon(coords)
  })

  const group = L.featureGroup(polygons)
  const bounds = group.getBounds()

  map.value.flyToBounds(bounds, {
    padding: [40, 40], // optional: adds margin around edges
    duration: 1.5, // smooth transition
  })
}

// Color scale
function getColor(value, max) {
  const ratio = value / max
  const r = Math.floor(255 * ratio)
  const g = Math.floor(255 * (1 - ratio))
  return `rgb(${r},${g},0)`
}

// Parse MULTIPOLYGON string
function parseGeometry(geomStr) {
  if (!geomStr || typeof geomStr !== 'string') return []

  const isMulti = geomStr.startsWith('MULTIPOLYGON')
  const cleaned = geomStr
    .replace(/(MULTIPOLYGON|POLYGON)\s*/i, '')
    .replace(/^\(+|\)+$/g, '')
    .trim()

  const ringGroups = isMulti ? cleaned.split(')),((') : [cleaned.replace(/^\(+|\)+$/g, '')]

  const parsed = ringGroups.map((ring) => {
    return ring
      .split(',')
      .map((pair) => {
        const [lonStr, latStr] = pair.trim().split(/\s+/)
        const lon = parseFloat(lonStr)
        const lat = parseFloat(latStr)
        if (isNaN(lat) || isNaN(lon)) return null
        return [lat, lon]
      })
      .filter((coord) => coord !== null)
  })

  return isMulti ? [parsed] : parsed
}

function isMultiPolygon(coords) {
  return Array.isArray(coords[0][0])
}

let legendControl = null

// Dynamic map legend
function addLegend(maxValue) {
  if (legendControl) {
    legendControl.remove()
  }

  legendControl = L.control({ position: 'bottomright' })

  legendControl.onAdd = function () {
    const div = L.DomUtil.create('div', 'info legend')
    const grades = [0, 0.2, 0.4, 0.6, 0.8, 1] // normalized scale

    const labels = grades.map((g) => {
      const value = Math.round(g * maxValue)
      const color = getColor(value, maxValue)
      return `<i style="background:${color}"></i> ${value}`
    })

    div.innerHTML = `
      <h5>Reference Legend<br>[${metricField.value === 'num_accs' ? 'Accident Count' : 'Accidents/km²]'}</h5>
      ${labels.join('<br>')}
    `
    return div
  }

  legendControl.addTo(map.value)
}

function renderPolygons() {
  if (!map.value || regions.value.length === 0) return
  if (geoLayer.value) geoLayer.value.remove()

  const maxVal = Math.max(...regions.value.map((r) => r[metricField.value]))
  geoLayer.value = L.layerGroup()

  regions.value.forEach((region) => {
    const coords = parseGeometry(region.geom)

    const polygon = isMultiPolygon(coords)
      ? L.polygon(coords) // MULTIPOLYGON
      : L.polygon([coords]) // POLYGON (wrapped for consistency)

    polygon.setStyle({
      color: '#333',
      weight: 1,
      fillColor: getColor(region[metricField.value], maxVal),
      fillOpacity: 0.6,
    })

    polygon.bindPopup(`
      <strong>${region.sa_name}</strong><br>
      Accidents: ${region.num_accs}<br>
      Acc/km²: ${region.acc_per_sq_km.toFixed(2)}<br>
      <a href="/region-roads/${encodeURIComponent(region.sa_name)}" class="popup-btn">
        View risky roads within this region
      </a>
    `)

    geoLayer.value.addLayer(polygon)
  })

  geoLayer.value.addTo(map.value)
  addLegend(maxVal)
}

// ---------- State ----------
const mapEl = ref(null)
const map = ref(null)
const isReady = ref(false)
let ro = null
const geoLayer = ref(null)
const regions = ref([])

const filterAreaLevel = ref('sa3') // 'sa2' | 'sa3' | 'sa4'
const filterAreaName = ref('')
const groupBy = ref('sa2') // <= filter
const dateFrom = ref('2020-01-01')
const dateTo = ref('2024-12-31')
const metric = ref('density') // 'density' | 'count'
const sortDir = ref('desc')
const limit = ref(100)

const names = ref([])
const loadingNames = ref(false)
const err = ref('')

const metricField = computed(() => {
  return metric.value === 'count' ? 'num_accs' : 'acc_per_sq_km'
})

// ---------- Group-by options ----------
const groupOptions = computed(() => {
  if (filterAreaLevel.value === 'sa4')
    return [
      { value: 'sa3', label: 'Area (SA3)' },
      { value: 'sa2', label: 'Suburb (SA2)' },
    ]
  if (filterAreaLevel.value === 'sa3') return [{ value: 'sa2', label: 'Suburb (SA2)' }]
  return [{ value: 'sa2', label: 'Suburb (SA2)' }]
})

watch(filterAreaLevel, () => {
  const valid = groupOptions.value.map((o) => o.value)
  if (!valid.includes(groupBy.value)) groupBy.value = valid[0]
})

// ---------- Load distinct names ----------
async function loadNamesForLevel() {
  loadingNames.value = true
  try {
    const endpoint =
      filterAreaLevel.value === 'sa4'
        ? '/distinct_sa4'
        : filterAreaLevel.value === 'sa3'
          ? '/distinct_sa3'
          : '/distinct_sa2'
    const r = await fetch(`${API}${endpoint}`)
    if (!r.ok) throw new Error(`${endpoint} ${r.status}`)
    names.value = await r.json()
    if (!names.value.includes(filterAreaName.value)) {
      filterAreaName.value = names.value[0] || ''
    }
  } catch (e) {
    err.value = e instanceof Error ? e.message : String(e)
  } finally {
    loadingNames.value = false
  }
}

// ---------- API ----------

async function fetchAccidentStats() {
  try {
    const response = await axios.post(`${API}/accident_stats`, {
      filter_area_level: filterAreaLevel.value,
      filter_area_name: filterAreaName.value,
      group_by_area_level: groupBy.value,
      date_from: dateFrom.value || null,
      date_to: dateTo.value || null,
      order_by: metric.value === 'density' ? 'density' : 'count',
      order_dir: sortDir.value,
      limit: 100,
    })
    regions.value = response.data
    renderPolygons()
    centerMapOnBounds()
  } catch (err) {
    console.error('Failed to fetch accident stats:', err)
  }
}

// ---------- Lifecycle ----------
onMounted(async () => {
  loadNamesForLevel()
  await nextTick()
  map.value = L.map(mapEl.value).setView([-38.2, 144.2], 9)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
  }).addTo(map.value)

  isReady.value = true
  fetchAccidentStats()
})

watch(metric, () => isReady.value && fetchAccidentStats())
watch([filterAreaLevel], async () => {
  if (isReady.value) {
    await loadNamesForLevel()
    await fetchAccidentStats()
  }
})
watch(
  [filterAreaName, groupBy, dateFrom, dateTo, sortDir],
  () => isReady.value && fetchAccidentStats(),
)
</script>

<style scoped>
.page {
  display: grid;
  gap: 12px;
  padding: 4rem;
}
.panel {
  background: #fff3cd;
  border: 1px solid #f7e39c;
  border-radius: 10px;
  padding: 10px;
}
.row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 10px;
}
label {
  display: grid;
  gap: 6px;
  font-size: 14px;
}
input,
select {
  padding: 8px 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.error {
  margin-top: 8px;
  color: #7f1d1d;
  background: #fee2e2;
  border: 1px solid #fecaca;
  padding: 8px 10px;
  border-radius: 8px;
}

.map-wrap {
  position: relative;
  height: calc(100vh - 200px);
  border-radius: 12px;
  overflow: hidden;
}
.map {
  position: absolute;
  inset: 0;
}

.map-container {
  height: 600px;
  width: 100%;
}

.row label {
  justify-self: start; /* keep to the content width */
  width: max-content; /* compact cell */
}

label select,
label input[type='date'],
label input[type='text'] {
  width: 200px; /* tweak to taste (e.g. 220–280px) */
  max-width: 100%; /* allow shrinking on small screens */
}

@media (max-width: 640px) {
  label select,
  label input[type='date'],
  label input[type='text'] {
    width: 100%;
  }
}
</style>

<style>
.info.legend {
  background: white;
  padding: 10px;
  font-size: 14px;
  line-height: 1.4;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.info.legend h4 {
  margin: 0 0 6px;
  font-weight: bold;
}

.info.legend i {
  width: 18px;
  height: 18px;
  display: inline-block;
  margin-right: 8px;
  background: #ccc; /* fallback */
  vertical-align: middle;
}

.popup-btn {
  display: inline-block;
  margin-top: 8px;
  padding: 6px 12px;
  background: #f15a24;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: 600;
  transition: background 0.2s;
}

.popup-btn:hover {
  background: #d94e1f;
}
</style>
