<template>
  <div>
    <select v-model="colorMetric" class="metric-selector">
      <option value="num_accs">Accident Count</option>
      <option value="acc_per_sq_km">Accidents per km²</option>
    </select>
    <div id="map" class="map-container"></div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import axios from 'axios'
import L from 'leaflet'

const API = import.meta.env.VITE_API_BASE ?? '/api'

const colorMetric = ref('num_accs')
const map = ref(null)
const geoLayer = ref(null)
const regions = ref([])

// API call
async function fetchAccidentStats() {
  try {
    const response = await axios.post(`${API}/accident_stats`, {
      filter_area_level: 'sa3',
      filter_area_name: 'Melbourne city',
      group_by_area_level: 'sa2',
      date_from: '2020-01-01',
      date_to: '2025-01-01',
      order_by: 'count',
      order_dir: 'desc',
      limit: 100,
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
      <h4>${colorMetric.value === 'num_accs' ? 'Accident Count' : 'Accidents/km²'}</h4>
      ${labels.join('<br>')}
    `
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

    const polygon = isMultiPolygon(coords)
      ? L.polygon(coords) // MULTIPOLYGON
      : L.polygon([coords]) // POLYGON (wrapped for consistency)

    polygon.setStyle({
      color: '#333',
      weight: 1,
      fillColor: getColor(region[colorMetric.value], maxVal),
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

onMounted(() => {
  map.value = L.map('map').setView([-38.2, 144.2], 9)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
  }).addTo(map.value)

  fetchAccidentStats()
})

watch(colorMetric, () => {
  renderPolygons()
})
</script>

<style scoped>
/* Leaflet map styling */

.map-container {
  height: 600px;
  width: 100%;
}

.metric-selector {
  margin-bottom: 10px;
  padding: 6px;
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
