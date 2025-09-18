<script setup>
import { ref, computed, onMounted, watch } from 'vue'

const API = import.meta.env.VITE_API_BASE ?? '/api'

/* ---------- Allowed values ---------- */
const SEVERITIES = [
  'fatal accident',
  'non injury accident',
  'other injury accident',
  'serious injury accident',
]
const SPEED_ZONES = [
  '110 km/hr',
  '100 km/hr',
  '90 km/hr',
  '80 km/hr',
  '75 km/hr',
  '70 km/hr',
  '65 km/hr',
  '60 km/hr',
  '50 km/hr',
  '40 km/hr',
  '30km/hr',
  'camping grounds or off road',
]
const AGE_GROUPS = [
  '0-4',
  '5-12',
  '13-15',
  '16-17',
  '18-21',
  '22-25',
  '26-29',
  '30-39',
  '40-49',
  '50-59',
  '60-64',
  '65-69',
  '70+',
]
const SEXES = ['M', 'F', 'U']
const ROAD_USERS = [
  'bicyclists',
  'drivers',
  'e-scooter rider',
  'motorcyclists',
  'not known',
  'passengers',
  'pedestrians',
  'pillion passengers',
]
const HOSPITALISED = ['y', 'n']
const WEATHER = ['clear', 'dust', 'fog', 'not known', 'raining', 'smoke', 'snowing', 'strong winds']
const ROAD_TYPES = [
  'major',
  'suburban',
  'rural_and_low_traffic',
  'infrastructure',
  'commerical_and_civic',
  'pedestrian_and_recreational_paths',
]
const ORDER_BY_OPTS = {
  accident_count: 'Accident Count',
  accident_density_per_km: 'Accident Density (/km)',
}

const MIN_ACCIDENTS_OPTIONS = [0, 1, 2, 3, 5, 10]
const MIN_LENGTH_OPTIONS = [0.2, 0.5, 1, 2, 5]
const LIMIT_OPTIONS = [5, 10, 20, 50, 100]

/* ---------- Filters ---------- */
const sa_level = ref('sa3')
const sa_name = ref('')
const saNames = ref([])
const saLoading = ref(false)

const road_type = ref('major')

const date_from = ref('')
const date_to = ref('')
const time_from = ref('')
const time_to = ref('')

const severity = ref('')
const speed_zone = ref('')
const age_group = ref('')
const sex = ref('')
const road_user_type_desc = ref('')
const victims_hospitalised = ref('')
const atmosph_cond_desc = ref('')

const min_accidents_per_road = ref(0)
const min_road_length_km = ref(0.2)
const order_by = ref('accident_density_per_km')
const order_descending = ref(true)
const limit = ref(10)

/* ---------- UI ---------- */
const loading = ref(false)
const errorMsg = ref('')
const rows = ref([])

/* ---------- Helpers ---------- */
async function loadSANames() {
  saLoading.value = true
  errorMsg.value = ''
  try {
    const path = sa_level.value === 'sa3' ? '/distinct_sa3' : '/distinct_sa2'
    const res = await fetch(`${API}${path}`)
    const text = await res.text()
    if (!res.ok) throw new Error(`${res.status} ${res.statusText} — ${text}`)
    const data = JSON.parse(text)
    saNames.value = Array.isArray(data) ? data : []
    if (!saNames.value.includes(sa_name.value)) sa_name.value = saNames.value[0] || ''
  } catch (e) {
    console.error(e)
    errorMsg.value = e?.message || String(e)
    saNames.value = []
    sa_name.value = ''
  } finally {
    saLoading.value = false
  }
}

function buildBody() {
  const b = {
    sa_level: sa_level.value,
    sa_name: sa_name.value,
    road_type: road_type.value,
    order_by: order_by.value,
    order_desc: order_descending.value, // always descending
    limit: Number(limit.value),
  }
  const opt = {
    date_from,
    date_to,
    time_from,
    time_to,
    severity,
    speed_zone,
    age_group,
    sex,
    road_user_type_desc,
    victims_hospitalised,
    atmosph_cond_desc,
  }
  for (const [k, v] of Object.entries(opt)) if (v.value) b[k] = v.value
  b.min_accidents_per_road = Number(min_accidents_per_road.value)
  b.min_road_length_km = Number(min_road_length_km.value)
  return b
}

async function refresh() {
  loading.value = true
  errorMsg.value = ''
  try {
    if (!sa_name.value) throw new Error('Please select an SA name.')
    const res = await fetch(`${API}/road_accident_density`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(buildBody()),
    })
    const text = await res.text()
    if (!res.ok) throw new Error(`${res.status} ${res.statusText} — ${text}`)
    rows.value = JSON.parse(text) || []
  } catch (e) {
    console.error(e)
    errorMsg.value = e?.message || String(e)
    rows.value = []
  } finally {
    loading.value = false
  }
}

/* Clear all filters to defaults */
async function clearForm() {
  sa_level.value = 'sa3'
  await loadSANames() // will set first SA name
  road_type.value = 'major'
  date_from.value = ''
  date_to.value = ''
  time_from.value = ''
  time_to.value = ''
  severity.value = ''
  speed_zone.value = ''
  age_group.value = ''
  sex.value = ''
  road_user_type_desc.value = ''
  victims_hospitalised.value = ''
  atmosph_cond_desc.value = ''
  min_accidents_per_road.value = 0
  min_road_length_km.value = 0.2
  order_by.value = 'accident_density_per_km'
  order_descending.value = true
  limit.value = 10
  rows.value = []
  errorMsg.value = ''
}

/* ---------- Table helpers ---------- */
const totalCount = computed(() => rows.value.reduce((s, r) => s + Number(r.accident_count || 0), 0))
const avgDensity = computed(() =>
  rows.value.length
    ? rows.value.reduce((s, r) => s + Number(r.accident_density_per_km || 0), 0) / rows.value.length
    : 0,
)

/* ---------- Init ---------- */
onMounted(async () => {
  await loadSANames()
  if (sa_name.value) refresh()
})
watch(sa_level, loadSANames)
</script>

<template>
  <div class="wrap">
    <div class="panel">
      <h2 class="title">Road accident density</h2>

      <div class="grid">
        <label>SA level</label>
        <select v-model="sa_level">
          <option value="sa3">District (SA3)</option>
          <option value="sa2">Suburb (SA2)</option>
        </select>

        <label>SA name</label>
        <select v-model="sa_name" :disabled="saLoading || !saNames.length">
          <option v-for="n in saNames" :key="n" :value="n">{{ n }}</option>
        </select>

        <label>Road type</label>
        <select v-model="road_type">
          <option v-for="t in ROAD_TYPES" :key="t" :value="t">{{ t }}</option>
        </select>

        <label>Sort by</label>
        <select v-model="order_by">
          <option v-for="(label, o) in ORDER_BY_OPTS" :key="o" :value="o">{{ label }}</option>
        </select>

        <label>Sort direction</label>
        <select v-model="order_descending">
          <option :value="false">Safest First (Ascending)</option>
          <option :value="true">Riskiest First (Descending)</option>
        </select>

        <label>Limit</label>
        <select v-model="limit">
          <option v-for="n in LIMIT_OPTIONS" :key="n" :value="n">{{ n }}</option>
        </select>
      </div>

      <details>
        <summary>Filters</summary>
        <div class="grid">
          <label>From</label><input type="date" v-model="date_from" /> <label>To</label
          ><input type="date" v-model="date_to" /> <label>Time from</label
          ><input type="time" step="1" v-model="time_from" /> <label>Time to</label
          ><input type="time" step="1" v-model="time_to" />

          <label>Severity</label>
          <select v-model="severity">
            <option value="">Any</option>
            <option v-for="s in SEVERITIES" :key="s" :value="s">{{ s }}</option>
          </select>

          <label>Speed zone</label>
          <select v-model="speed_zone">
            <option value="">Any</option>
            <option v-for="s in SPEED_ZONES" :key="s" :value="s">{{ s }}</option>
          </select>

          <label>Age group</label>
          <select v-model="age_group">
            <option value="">Any</option>
            <option v-for="a in AGE_GROUPS" :key="a" :value="a">{{ a }}</option>
          </select>

          <label>Sex</label>
          <select v-model="sex">
            <option value="">Any</option>
            <option v-for="s in SEXES" :key="s" :value="s">{{ s }}</option>
          </select>

          <label>Road user</label>
          <select v-model="road_user_type_desc">
            <option value="">Any</option>
            <option v-for="u in ROAD_USERS" :key="u" :value="u">{{ u }}</option>
          </select>

          <label>Hospitalised</label>
          <select v-model="victims_hospitalised">
            <option value="">Any</option>
            <option v-for="h in HOSPITALISED" :key="h" :value="h">{{ h }}</option>
          </select>

          <label>Weather</label>
          <select v-model="atmosph_cond_desc">
            <option value="">Any</option>
            <option v-for="w in WEATHER" :key="w" :value="w">{{ w }}</option>
          </select>

          <label>
            Min acc/road
            <span
              class="hint"
              title="Ignore roads with fewer than this many crashes in the selected period."
              >ⓘ</span
            >
          </label>
          <select v-model="min_accidents_per_road">
            <option v-for="n in MIN_ACCIDENTS_OPTIONS" :key="n" :value="n">{{ n }}</option>
          </select>

          <label>
            Min len (km)
            <span
              class="hint"
              title="Ignore very short road segments. Length is measured along the road centreline."
              >ⓘ</span
            >
          </label>
          <select v-model="min_road_length_km">
            <option v-for="n in MIN_LENGTH_OPTIONS" :key="n" :value="n">{{ n }}</option>
          </select>
        </div>
      </details>

      <div class="actions">
        <button @click="refresh" :disabled="loading || !sa_name">Run query</button>
        <button @click="clearForm" class="secondary">Clear filters</button>
        <button @click="downloadCSV" :disabled="!rows.length">Export CSV</button>
      </div>

      <p v-if="errorMsg" class="err">{{ errorMsg }}</p>

      <!-- <div v-if="loading" class="loading-block">
        <div class="spinner"></div>
        <p class="muted">
          Fetching road-wise accident data...<br/>[these queries can take upto 2 minutes depending on
          filters and volume of data, please wait]
        </p>
      </div> -->

      <div v-if="rows.length" class="stats">
        <span
          ><strong>{{ rows.length }}</strong> roads</span
        >
        <span
          ><strong>{{ totalCount.toLocaleString() }}</strong> accidents</span
        >
        <span
          >avg density <strong>{{ avgDensity.toFixed(2) }}</strong> /km</span
        >
      </div>

      <p v-else-if="!loading && !errorMsg" class="muted">No results. Try adjusting filters.</p>

      <!-- <div class="table-wrap" v-if="rows.length">
        <table>
          <thead>
            <tr>
              <th style="width: 44%">Road</th>
              <th class="num">Crashes</th>
              <th class="num">Length (km)</th>
              <th class="num">Density (/km)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(r, i) in rows" :key="i">
              <td>{{ r.road_name || 'Unnamed road' }}</td>
              <td class="num">{{ Number(r.accident_count ?? 0) }}</td>
              <td class="num">{{ Number(r.road_length_km ?? 0).toFixed(2) }}</td>
              <td class="num">{{ Number(r.accident_density_per_km ?? 0).toFixed(2) }}</td>
            </tr>
          </tbody>
        </table>
      </div> -->

      <div class="table-container">
        <div class="table-wrap" v-if="rows.length">
          <table>
            <thead>
              <tr>
                <th style="width: 44%">Road</th>
                <th class="num">Crashes</th>
                <th class="num">Length (km)</th>
                <th class="num">Density (/km)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(r, i) in rows" :key="i">
                <td>{{ r.road_name || 'Unnamed road' }}</td>
                <td class="num">{{ Number(r.accident_count ?? 0) }}</td>
                <td class="num">{{ Number(r.road_length_km ?? 0).toFixed(2) }}</td>
                <td class="num">{{ Number(r.accident_density_per_km ?? 0).toFixed(2) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Overlay shown only when loading -->
        <div v-if="loading" class="overlay">
          <div class="spinner"></div>
          <p class="muted">
            Fetching road-wise accident data...<br />
            <small
              >[These queries can take up to 2 minutes depending on filters and volume of
              data]</small
            >
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.wrap {
  display: flex;
  justify-content: center;
  padding: 16px;
}
.panel {
  width: min(1100px, 100%);
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 8px 26px rgba(0, 0, 0, 0.06);
}
.title {
  margin: 0 0 10px;
  font-size: 20px;
}
.grid {
  display: grid;
  grid-template-columns: 140px 1fr;
  gap: 8px;
  margin-bottom: 8px;
}
.grid input,
.grid select {
  padding: 6px 8px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
}
.hint {
  margin-left: 6px;
  font-size: 12px;
  color: #6b7280;
  cursor: help;
}
.actions {
  display: flex;
  gap: 8px;
  margin: 10px 0;
}
.actions button {
  padding: 8px 10px;
  border: 0;
  border-radius: 10px;
  background: #111827;
  color: #fff;
  cursor: pointer;
}
.actions .secondary {
  background: #6b7280;
}
.actions button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.err {
  color: #b91c1c;
  margin: 8px 0;
}
.stats {
  display: flex;
  gap: 16px;
  margin: 8px 0 12px;
  color: #374151;
}
.table-wrap {
  overflow: auto;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  opacity: 1;
  transition: opacity 0.3s ease;
}

.table-container {
  position: relative;
}

.table-container.loading .table-wrap {
  opacity: 0.4; /* dim the table when loading */
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}
thead th {
  text-align: left;
  background: #f8fafc;
  border-bottom: 1px solid #e5e7eb;
  padding: 10px;
}
tbody td {
  padding: 10px;
  border-bottom: 1px solid #f1f5f9;
}
.num {
  text-align: right;
}
.muted {
  color: #6b7280;
  margin-top: 6px;
}
details {
  margin: 8px 0;
  padding: 6px 8px;
  background: #f8fafc;
  border-radius: 8px;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(2px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 10;
  text-align: center;
  padding: 1em;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 4px solid #ccc;
  border-top-color: #333;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 1em;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
