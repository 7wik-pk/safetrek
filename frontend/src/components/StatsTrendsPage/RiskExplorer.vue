<script setup>
import {ref, onMounted, watch, computed, nextTick} from 'vue'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl-css'

// ---------- API & Mapbox ----------
const API = import.meta.env.VITE_API_BASE ?? '/api'
mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN || 'pk.eyJ1IjoiY2hhcmxpZWVlMTkiLCJhIjoiY205ZHZjc2ttMTg0NzJscTE0MzRyYXlpYSJ9.-EKrTcL6Q_Wk1KvmrS_25g'

// ---------- WKT → GeoJSON ----------
function wktToGeoJSON(wkt) {
  const toCoords = (str) =>
    str.trim().split(',').map(pair => {
      const [x, y] = pair.trim().split(/\s+/).map(Number)
      return [x, y]
    })

  if (wkt.startsWith('POLYGON')) {
    const rings = wkt
      .slice(wkt.indexOf('((') + 2, wkt.lastIndexOf('))'))
      .split('),(')
      .map(r => toCoords(r))
    return { type: 'Polygon', coordinates: rings }
  }

  if (wkt.startsWith('MULTIPOLYGON')) {
    const polys = wkt
      .slice(wkt.indexOf('(((') + 3, wkt.lastIndexOf(')))'))
      .split(')), ((')
      .map(poly => {
        const rings = poly.split('), (').map(r => toCoords(r))
        return rings
      })
    return { type: 'MultiPolygon', coordinates: polys }
  }

  console.warn('Unsupported WKT:', wkt)
  return null
}

// ---------- State ----------
const mapEl = ref(null)
const map = ref(null)
const isReady = ref(false)
let ro = null

const filterAreaLevel = ref('sa4') // 'sa2' | 'sa3' | 'sa4'
const filterAreaName  = ref('')
const groupBy         = ref('sa2') // <= filter
const dateFrom        = ref('2020-01-01')
const dateTo          = ref('2024-12-31')
const metric          = ref('density') // 'density' | 'count'
const sortDir         = ref('desc')
const limit           = ref(1000)

const names = ref([])
const loadingNames = ref(false)
const err = ref('')

// ---------- Group-by options ----------
const groupOptions = computed(() => {
  if (filterAreaLevel.value === 'sa4') return [
    { value: 'sa3', label: 'Area (SA3)' },
    { value: 'sa2', label: 'Suburb (SA2)' },
  ]
  if (filterAreaLevel.value === 'sa3') return [
    { value: 'sa2', label: 'Suburb (SA2)' },
  ]
  return [{ value: 'sa2', label: 'Suburb (SA2)' }]
})

watch(filterAreaLevel, () => {
  const valid = groupOptions.value.map(o => o.value)
  if (!valid.includes(groupBy.value)) groupBy.value = valid[0]
})

// ---------- Load distinct names ----------
async function loadNamesForLevel() {
  loadingNames.value = true
  try {
    const endpoint =
      filterAreaLevel.value === 'sa4' ? '/distinct_sa4' :
        filterAreaLevel.value === 'sa3' ? '/distinct_sa3' :
          '/distinct_sa2'
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

// ---------- Color stops (single source of truth) ----------
const DENSITY_STOPS = [
  { t: 0,  color: '#f1eef6' },
  { t: 2,  color: '#d0d1e6' },
  { t: 5,  color: '#a6bddb' },
  { t: 10, color: '#74a9cf' },
  { t: 15, color: '#3690c0' },
  { t: 20, color: '#0570b0' },
  { t: 30, color: '#034e7b' },
]
const COUNT_STOPS = [
  { t: 0,   color: '#f1eef6' },
  { t: 10,  color: '#d0d1e6' },
  { t: 25,  color: '#aa4a56' },
  { t: 50,  color: '#7d0088' },
  { t: 75,  color: '#7a003d' },
  { t: 100, color: '#510030' },
  { t: 150, color: '#290000' },
]
const stopsForMetric = (m) => (m === 'density' ? DENSITY_STOPS : COUNT_STOPS)

// Use the stops for the layer paint
function colorPaint(metricKey) {
  const prop = metricKey === 'density' ? ['get', 'acc_per_sq_km'] : ['get', 'num_accs']
  const stops = stopsForMetric(metricKey)
  const expr = ['interpolate', ['linear'], prop]
  stops.forEach(s => expr.push(s.t, s.color))
  return { 'fill-color': expr, 'fill-opacity': 0.7 }
}

// ---------- Legend (reactive; rendered by Vue) ----------
const legendItems = computed(() => {
  const stops = stopsForMetric(metric.value)
  return stops.map((s, i) => {
    const next = stops[i + 1]
    return {
      color: s.color,
      label: next ? `${s.t}–${next.t}` : `${s.t}+`
    }
  })
})

// ---------- API ----------
async function fetchStats() {
  const body = {
    filter_area_level:   filterAreaLevel.value,
    filter_area_name:    filterAreaName.value,
    group_by_area_level: groupBy.value,
    date_from:           dateFrom.value || null,
    date_to:             dateTo.value   || null,
    order_by:            metric.value === 'density' ? 'density' : 'count',
    order_dir:           sortDir.value,
    limit:               100
  }

  const res = await fetch(`${API}/accident_stats`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  })
  if (!res.ok) {
    const txt = await res.text().catch(()=>'')
    throw new Error(`accident_stats ${res.status} ${txt}`)
  }
  const rows = await res.json()

  const features = rows.map(r => {
    const geom = wktToGeoJSON(r.geom)
    return {
      type: 'Feature',
      geometry: geom,
      properties: {
        sa_name: r.sa_name,
        num_accs: r.num_accs,
        geom_area_sq_km: r.geom_area_sq_km,
        acc_per_sq_km: r.acc_per_sq_km
      }
    }
  }).filter(f => f.geometry)

  return { type: 'FeatureCollection', features }
}

// ---------- Map wiring ----------
function ensureLayers(geojson) {
  const srcId = 'acc-polys'
  const fillId = 'acc-polys-fill'
  const lineId = 'acc-polys-outline'

  if (map.value.getSource(srcId)) {
    map.value.getSource(srcId).setData(geojson)
  } else {
    map.value.addSource(srcId, { type: 'geojson', data: geojson })
    map.value.addLayer({
      id: fillId,
      type: 'fill',
      source: srcId,
      paint: colorPaint(metric.value)
    })
    map.value.addLayer({
      id: lineId,
      type: 'line',
      source: srcId,
      paint: { 'line-color': '#333', 'line-width': 0.6 }
    })
  }

  const bbox = turfBbox(geojson)
  map.value.fitBounds(bbox, { padding: 24, duration: 600 })
}

function turfBbox(fc) {
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity
  const scan = (coords) => {
    if (typeof coords[0] === 'number') {
      const [x, y] = coords
      minX = Math.min(minX, x); minY = Math.min(minY, y)
      maxX = Math.max(maxX, x); maxY = Math.max(maxY, y)
    } else {
      coords.forEach(scan)
    }
  }
  fc.features.forEach(f => scan(f.geometry.coordinates))
  return [[minX, minY], [maxX, maxY]]
}

function updatePaint() {
  const fillId = 'acc-polys-fill'
  if (map.value?.getLayer?.(fillId)) {
    const paint = colorPaint(metric.value)
    Object.entries(paint).forEach(([k, v]) => map.value.setPaintProperty(fillId, k, v))
  }
}

async function refresh() {
  err.value = ''
  if (!filterAreaName.value) return
  const geojson = await fetchStats()
  ensureLayers(geojson)
}

// ---------- Lifecycle ----------
onMounted(async () => {
  await nextTick();
  map.value = new mapboxgl.Map({
    container: mapEl.value,
    style: 'mapbox://styles/mapbox/light-v11',
    center: [144.96, -37.81],
    zoom: 7
  })

  map.value.addControl(new mapboxgl.NavigationControl(), 'top-right')

  map.value.on('load', async () => {
    isReady.value = true
    await loadNamesForLevel()
    await refresh()

    requestAnimationFrame(() => map.value && map.value.resize())

    if (window.ResizeObserver && mapEl.value) {
           ro = new ResizeObserver(() => map.value && map.value.resize())
             ro.observe(mapEl.value)
    }

    map.value.on('mousemove', 'acc-polys-fill', (e) => {
      map.value.getCanvas().style.cursor = 'pointer'
      const f = e.features?.[0]
      if (!f) return
      const p = f.properties
      const html = `
        <div style="font-weight:600">${p.sa_name}</div>
        <div>Crashes: ${p.num_accs}</div>
        <div>Density (/km²): ${Number(p.acc_per_sq_km).toFixed(2)}</div>
        <div>Area (km²): ${Number(p.geom_area_sq_km).toFixed(2)}</div>
      `
      const popup = new mapboxgl.Popup({ closeButton: false })
        .setLngLat(e.lngLat)
        .setHTML(html)
        .addTo(map.value)
      map.value.once('mousemove', () => popup.remove())
    })
  })
})

watch(metric, () => isReady.value && updatePaint())
watch([filterAreaLevel], async () => { if (isReady.value) { await loadNamesForLevel(); await refresh(); }})
watch([filterAreaName, groupBy, dateFrom, dateTo, sortDir], () => isReady.value && refresh())
</script>

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
      <div ref="mapEl" class="map"></div>

      <!-- Legend rendered by Vue (so scoped CSS applies) -->
      <div id="legend" class="legend">
        <div class="legend-title">
          {{ metric === 'density' ? 'Density (/km²)' : 'Crashes' }}
        </div>
        <div class="legend-row" v-for="li in legendItems" :key="li.label">
          <span class="swatch" :style="{ background: li.color }"></span>
          <span>{{ li.label }}</span>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.page { display: grid; gap: 12px; padding: 12px; }
.panel { background: #fff3cd; border: 1px solid #f7e39c; border-radius: 10px; padding: 10px; }
.row { display: grid; grid-template-columns: repeat(auto-fit,minmax(180px,1fr)); gap: 10px; }
label { display: grid; gap: 6px; font-size: 14px; }
input, select { padding: 8px 10px; border: 1px solid #ccc; border-radius: 8px; }

.error { margin-top: 8px; color: #7f1d1d; background: #fee2e2; border: 1px solid #fecaca; padding: 8px 10px; border-radius: 8px; }

.map-wrap { position: relative; height: calc(100vh - 200px); border-radius: 12px; overflow: hidden; }
.map { position: absolute; inset: 0; }

.legend {
  position: absolute; bottom: 12px; left: 12px;
  background: rgba(255,255,255,.95);
  padding: 10px; border-radius: 10px; font-size: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,.15);
}
.legend-title { font-weight: 700; margin-bottom: 6px; }
.legend-row { display: flex; align-items: center; gap: 6px; margin: 2px 0; }
.swatch { width: 16px; height: 10px; border-radius: 2px; display: inline-block; }

.row label {
  justify-self: start;        /* keep to the content width */
  width: max-content;         /* compact cell */
}


label select,
label input[type="date"],
label input[type="text"] {
  width: 200px;               /* tweak to taste (e.g. 220–280px) */
  max-width: 100%;            /* allow shrinking on small screens */
}


@media (max-width: 640px) {
  label select,
  label input[type="date"],
  label input[type="text"] {
    width: 100%;
  }
}

</style>
