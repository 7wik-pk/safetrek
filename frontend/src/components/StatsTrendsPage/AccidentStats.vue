<template>
  <section class="container my-4">
    <!-- Header -->
    <div class="d-flex align-items-center justify-content-between mb-3">
      <div>
        <div class="text-uppercase text-muted fw-semibold small">Analytics</div>
        <h1 class="h3 fw-bold m-0">Crash Statistics Explorer (By Region)</h1>
        <div class="text-muted">Pick a region, set filters, and view grouped results.</div>
      </div>
      <button class="btn btn-outline-secondary btn-sm" @click="startTour">❓ Tour</button>
    </div>

    <!-- Topbar across main column -->
    <div class="card mb-3" id="tour-topbar">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-12 col-lg-3" id="tour-level">
            <label class="form-label">Select region type</label>
            <select class="form-select" v-model="filterLevel">
              <option v-for="key in filterableLevels" :key="key" :value="key">
                {{ levelMeta[key].label }}
              </option>
            </select>
          </div>

          <div class="col-12 col-lg-6" id="tour-area">
            <label class="form-label" :title="levelMeta[filterLevel].tooltip">
              {{ levelMeta[filterLevel].label }} name
            </label>
            <select class="form-select" v-model="filterAreaName">
              <option disabled value="">-- select {{ filterLevel.toUpperCase() }} --</option>
              <option v-for="a in currentFilterOptions" :key="a" :value="a">{{ a }}</option>
            </select>
          </div>

          <div class="col-12 col-lg-3" id="tour-group">
            <label class="form-label">Group results by</label>
            <select class="form-select" v-model="groupLevel">
              <option v-for="key in validGroupLevels" :key="key" :value="key">
                {{ levelMeta[key].label }}
              </option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- Body: sidebar + main -->
    <div class="row g-3">
      <!-- Sidebar -->
      <aside class="col-12 col-lg-3">
        <div class="card" id="tour-filters">
          <div class="card-body">
            <h3 class="h6 fw-bold mb-3">Filters</h3>

            <!-- Date from -->
            <div class="mb-3" id="tour-datefrom">
              <label class="form-label">Date from</label>
              <div class="date-input">
                <Datepicker
                  v-model="dateFrom"
                  :minDate="minDate"
                  :maxDate="dateTo"
                  :format="'yyyy-MM-dd'"
                />
              </div>
            </div>

            <!-- Date to -->
            <div class="mb-3" id="tour-dateto">
              <label class="form-label">Date to</label>
              <div class="date-input">
                <Datepicker
                  v-model="dateTo"
                  :minDate="dateFrom"
                  :maxDate="maxDate"
                  :format="'yyyy-MM-dd'"
                />
              </div>
              <div v-if="dateAdjusted" class="form-text text-muted mt-1">
                End date was adjusted to match the new start date.
              </div>
            </div>


            <div class="mb-3" id="tour-orderby">
              <label class="form-label">Order by</label>
              <select class="form-select" v-model="orderBy">
                <option value="count">Count</option>
                <option value="density">Density</option>
              </select>
            </div>

            <div class="mb-3" id="tour-sort">
              <label class="form-label">Sort by</label>
              <select class="form-select" v-model="orderDir">
                <option v-for="opt in sortOptions" :key="opt.value" :value="opt.value">
                  {{ opt.label }}
                </option>
              </select>
            </div>

            <div class="mb-3" id="tour-limit">
              <label class="form-label">Limit Results</label>
              <input class="form-control" v-model.number="limit" type="number" min="1" max="100" />
            </div>

            <button
              id="tour-show"
              class="btn btn-dark w-100"
              :disabled="!canQuery || loading"
              @click="fetchStats"
            >
              {{ loading ? 'Loading…' : 'Show Results' }}
            </button>
          </div>
        </div>
      </aside>

      <!-- Main -->
      <main class="col-12 col-lg-9">
        <!-- Loading -->
        <div v-if="loading" class="card">
          <div class="card-body text-center py-5">
            <div class="spinner-border text-dark" role="status"></div>
            <div class="fw-semibold mt-2">Loading crash data…</div>
          </div>
        </div>

        <!-- Results -->
        <div v-else-if="results.length" class="card" id="tour-results">
          <div class="card-body">
            <h3 v-if="lastUsedFilters.limit" class="h5 fw-bold mb-3">
              Top {{ results.length }} by {{ lastUsedFilters.orderBy }},
              Grouped by:
              <span :title="levelMeta[lastUsedFilters.groupLevel].tooltip">
                {{ levelMeta[lastUsedFilters.groupLevel].label }}
              </span>
            </h3>

            <div class="table-responsive">
              <table class="table table-striped align-middle">
                <thead class="table-light">
                <tr>
                  <th>Area</th>
                  <th class="text-end">Crashes</th>
                  <th class="text-end">Area (km²)</th>
                  <th class="text-end">Density (/km²)</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="r in results" :key="r.sa_name">
                  <td>{{ r.sa_name }}</td>
                  <td class="text-end">{{ r.num_accs }}</td>
                  <td class="text-end">{{ fmt(r.geom_area_sq_km) }}</td>
                  <td class="text-end">{{ fmt(r.acc_per_sq_km) }}</td>
                </tr>
                </tbody>
              </table>
            </div>

            <div
              v-if="lastUsedFilters.limit > results.length && results.length > 0"
              class="alert alert-warning mt-3"
              role="alert"
            >
              Only {{ results.length }} regions found within {{ filterAreaName }}.
            </div>
          </div>
        </div>

        <!-- Empty states -->
        <div v-else-if="emptyMessage.length > 0" class="alert alert-info" role="alert">
          <strong>{{ emptyMessage }}</strong>
        </div>
        <div v-else class="card">
          <div class="card-body text-muted">
            Select filters and click <strong>Show Results</strong>.
          </div>
        </div>

        <!-- Error -->
        <div v-if="error" class="alert alert-danger mt-3" role="alert">{{ error }}</div>
      </main>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import Datepicker from 'vue3-datepicker'
import api from '@/lib/api'

/** Guided tour (version-agnostic: driver.js v1 or v2) */
import * as DriverNS from 'driver.js'
import 'driver.js/dist/driver.css'

const filterLevel = ref<'sa4' | 'sa3'>('sa4')
const groupLevel = ref<'sa2' | 'sa3'>('sa2')
const filterAreaName = ref('')

const levelMeta = {
  sa2: { label: 'Suburb (SA2)', tooltip: 'Typically aligns with suburbs or small communities' },
  sa3: { label: 'District (SA3)', tooltip: 'Groups multiple suburbs; may align with council or service regions' },
  sa4: { label: 'Regional Zone (SA4)', tooltip: 'Large zones used for labor market and regional planning' },
} as const

const dateFrom = ref<Date | null>(new Date('2020-01-01'))
const dateTo = ref<Date | null>(new Date('2024-12-31'))
const maxDate = new Date('2024-12-31')
const minDate = new Date('2020-01-01')
const orderBy = ref<'count' | 'density'>('density')
const orderDir = ref<'asc' | 'desc'>('desc')
const limit = ref<number>(5)

function formatDate(d: Date | null, human_readable: boolean = false): string | undefined {
  if (!d) return undefined
  return human_readable
    ? d.toLocaleDateString('en-AU', { day: 'numeric', month: 'short', year: 'numeric' })
    : d.toISOString().split('T')[0]
}

const lastUsedFilters = ref({ limit: 0 as any, orderBy: '', groupLevel: '' })

const loading = ref(false)
const error = ref('')
const results = ref<any[]>([])

const sa4Options = ref<string[]>([])
const sa3Options = ref<string[]>([])
const emptyMessage = ref('')

const sortOptions = computed(() =>
  orderBy.value === 'count'
    ? [
      { value: 'desc', label: 'Most accidents first' },
      { value: 'asc', label: 'Fewest accidents first' },
    ]
    : orderBy.value === 'density'
      ? [
        { value: 'desc', label: 'Highest density (risky) first' },
        { value: 'asc', label: 'Lowest density (safe) first' },
      ]
      : [
        { value: 'desc', label: 'Descending' },
        { value: 'asc', label: 'Ascending' },
      ],
)

const currentFilterOptions = computed(() =>
  filterLevel.value === 'sa4' ? sa4Options.value : sa3Options.value,
)

const canQuery = computed(() => !!filterAreaName.value && !!filterLevel.value && !!groupLevel.value)
const filterableLevels = computed<('sa3' | 'sa4')[]>(() => ['sa4', 'sa3'])
const validGroupLevels = computed<('sa2' | 'sa3')[]>(() =>
  filterLevel.value === 'sa4' ? ['sa3', 'sa2'] : filterLevel.value === 'sa3' ? ['sa2'] : [],
)

onMounted(async () => {
  try {
    const [sa4, sa3] = await Promise.all([
      api.get<string[]>('/distinct_sa4'),
      api.get<string[]>('/distinct_sa3'),
    ])
    sa4Options.value = sa4.data
    sa3Options.value = sa3.data

    if (filterLevel.value === 'sa4' && sa4.data.length) {
      filterAreaName.value = sa4.data[0]
      await fetchStats()
    } else if (filterLevel.value === 'sa3' && sa3.data.length) {
      filterAreaName.value = sa3.data[0]
    }
  } catch (e: any) {
    error.value = e?.response?.data?.detail || e.message || 'Failed to load area lists'
  }
})

watch(filterLevel, (lvl) => {
  filterAreaName.value = ''
  const valid = validGroupLevels.value
  if (valid.length) groupLevel.value = valid[0]

  if (lvl === 'sa3') {
    groupLevel.value = 'sa2'
    if (sa3Options.value.length) filterAreaName.value = sa3Options.value[0]
  } else {
    if (sa4Options.value.length) filterAreaName.value = sa4Options.value[0]
  }
})

const dateAdjusted = ref(false)
watch(dateFrom, (newFrom) => {
  if (newFrom && dateTo.value && newFrom > dateTo.value) {
    dateTo.value = newFrom
    dateAdjusted.value = true
  } else {
    dateAdjusted.value = false
  }
})

function fmt(n: number) {
  return Number(n).toLocaleString(undefined, { maximumFractionDigits: 2 })
}

async function fetchStats() {
  error.value = ''
  results.value = []
  emptyMessage.value = ''
  loading.value = true

  try {
    const payload: any = {
      filter_area_level: filterLevel.value,
      filter_area_name: filterAreaName.value,
      group_by_area_level: groupLevel.value,
      order_by: orderBy.value,
      order_dir: orderDir.value,
      limit: limit.value,
    }
    if (dateFrom.value) payload.date_from = formatDate(dateFrom.value)
    if (dateTo.value) payload.date_to = formatDate(dateTo.value)

    if (new Date(dateFrom.value as any) > new Date(dateTo.value as any)) {
      error.value = 'Start date cannot be after end date.'
      loading.value = false
      return
    }

    const { data } = await api.post('/accident_stats', payload)
    results.value = data

    if (!data.length) {
      results.value = []
      const name = filterAreaName.value
      emptyMessage.value =
        `No crash data was found for "${name}" between ${formatDate(dateFrom.value, true)} and ${formatDate(dateTo.value, true)}.\n` +
        `Our system only stores data from ${formatDate(minDate, true)} to ${formatDate(maxDate, true)}.`
    } else {
      emptyMessage.value = ''
      lastUsedFilters.value = {
        limit: limit.value as any,
        orderBy: orderBy.value,
        groupLevel: groupLevel.value,
      }
    }
  } catch (e: any) {
    error.value = e?.response?.data?.detail || e.message || 'Request failed'
  } finally {
    loading.value = false
  }
}

/** Guided tour */
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

    const steps: any[] = []
    if (document.querySelector('#tour-topbar')) {
      steps.push(
        { element: '#tour-topbar', popover: { title: 'Top controls', description: 'Choose the region type, pick a specific area, and set how to group the results.' } },
        { element: '#tour-level', popover: { title: 'Region type', description: 'Regional Zone (SA4) or District (SA3).' } },
        { element: '#tour-area', popover: { title: 'Area name', description: 'Select the exact region to analyze.' } },
        { element: '#tour-group', popover: { title: 'Group by', description: 'Aggregate results by SA3 or SA2 depending on your region type.' } },
      )
    }
    if (document.querySelector('#tour-filters')) {
      steps.push(
        { element: '#tour-filters', popover: { title: 'Filters', description: 'Use dates and sorting to refine the analysis.' } },
        { element: '#tour-datefrom', popover: { title: 'Date from', description: 'Pick the start date.' } },
        { element: '#tour-dateto', popover: { title: 'Date to', description: 'Pick the end date.' } },
        { element: '#tour-orderby', popover: { title: 'Order by', description: 'Order by crash count or density.' } },
        { element: '#tour-sort', popover: { title: 'Sort direction', description: 'Highest/lowest or most/fewest first.' } },
        { element: '#tour-limit', popover: { title: 'Limit', description: 'How many rows to return.' } },
        { element: '#tour-show', popover: { title: 'Run query', description: 'Click to fetch results.' } },
      )
    }
    if (document.querySelector('#tour-results')) {
      steps.push(
        { element: '#tour-results', popover: { title: 'Results', description: 'Table shows grouped crash metrics. Use the sidebar to adjust filters and rerun.' } },
      )
    }
    if (!steps.length) {
      alert('Open the page and then click Tour again.')
      return
    }

    // v2 API
    if (typeof (DriverNS as any).driver === 'function') {
      const d = (DriverNS as any).driver(options)
      if (typeof d.setSteps === 'function') d.setSteps(steps)
      else if (typeof d.defineSteps === 'function') d.defineSteps(steps)
      else (d as any).steps = steps
      if (typeof d.drive === 'function') d.drive()
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
  } catch (e) {
    console.warn('driver.js failed to start', e)
    alert('To launch the guided tour, please install driver.js:\n\n  npm i driver.js')
  }
}
</script>

<style scoped>
/* Minimal extras to tighten spacing with Bootstrap */
.card > .card-body :is(label.form-label) { font-weight: 600; }
.table thead th { font-weight: 700; }
/* --- Branded date input wrapper --- */
.date-input {
  position: relative;
  height: 44px;
  display: flex;
  align-items: center;
  border: 1px solid #e2e8f0;      /* matches your inputs */
  border-radius: 12px;
  background: #f9fafb;
  padding: 0;                      /* inner input controls the padding */
  transition:
    border-color .15s ease,
    box-shadow .15s ease,
    background-color .15s ease;
}

/* focus ring in your yellow/black theme */
.date-input:focus-within {
  border-color: #f6b300;
  box-shadow: 0 0 0 .2rem rgba(246, 179, 0, .25);
  background: #fff;
}

/* make the inner input look like a normal field */
.date-input :deep(.v3dp__input),
.date-input :deep(input) {
  width: 100%;
  height: 100%;
  border: 0 !important;
  outline: none !important;
  background: transparent;
  padding: 0 42px 0 14px;  /* space for calendar icon on the right */
  font-size: 0.95rem;
  font-weight: 600;
  color: #0f1419;
  box-shadow: none !important;
}

/* wrapper elements some builds add */
.date-input :deep(.v3dp__input_wrap),
.date-input :deep(.v3dp__datepicker) {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
}

/* hide any default icons from the lib if present */
.date-input :deep(.v3dp__clear-button),
.date-input :deep(.v3dp__calendar-button),
.date-input :deep(.dp__icon) {
  display: none !important;
}

/* calendar icon (right side) */
.date-input::after {
  content: '';
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  opacity: .6;
  pointer-events: none;
  background-repeat: no-repeat;
  background-size: 18px 18px;
  /* simple calendar glyph in charcoal */
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%230f1419' viewBox='0 0 24 24'%3E%3Cpath d='M7 2a1 1 0 0 1 1 1v1h8V3a1 1 0 1 1 2 0v1h1a2 2 0 0 1 2 2v13a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h1V3a1 1 0 0 1 1-1Zm12 8H5v9a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-9ZM19 6H5v2h14V6Z'/%3E%3C/svg%3E");
}

/* --- Popup / calendar panel (keep it within theme & above cards) --- */
:deep(.v3dp__calendar),
:deep(.dp__menu) {
  border: 1px solid #e2e8f0 !important;
  border-radius: 12px !important;
  background: #fff !important;
  box-shadow: 0 8px 28px rgba(0,0,0,.12) !important;
  z-index: 2000 !important;  /* keep above cards */
  overflow: hidden;
}

/* Month header / weekday row */
:deep(.v3dp__heading),
:deep(.dp__calendar_header) {
  background: linear-gradient(#fffdfa, #fff7e1);
  border-bottom: 1px solid #e2e8f0;
  font-weight: 800;
  color: #151922;
}

/* day cells */
:deep(.v3dp__day),
:deep(.dp__cell_inner) {
  border-radius: 10px !important;
}

/* hover */
:deep(.v3dp__day:hover),
:deep(.dp__cell_inner:hover) {
  background: #eef3ff !important;
}

/* selected day / range edges if enabled */
:deep(.v3dp__day--selected),
:deep(.dp__active_date),
:deep(.dp__range_start),
:deep(.dp__range_end) {
  background: #f6b300 !important;
  color: #000 !important;
}

/* disabled dates */
:deep(.v3dp__day--disabled),
:deep(.dp__cell_disabled) {
  color: #9aa4af !important;
  opacity: .6 !important;
}

/* make sure popovers aren’t clipped by cards */
.card,
.card-body { overflow: visible; }

</style>
