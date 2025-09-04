<template>
  <section class="acc-wrap">
    <div class="card">
      <h2 class="title">Crash Statistics Explorer (By Region)</h2>

      <div class="layout">
        <!-- topbar across main column -->
        <div class="topbar">
          <label class="field">

            <span>Select region type</span>
            <select v-model="filterLevel">
              <option v-for="key in filterableLevels" :key="key" :value="key">
                {{ levelMeta[key].label }}
              </option>
            </select>

          </label>

          <label class="field">

            <span :title="levelMeta[filterLevel].tooltip">
              {{ levelMeta[filterLevel].label }} name
            </span>

            <select v-model="filterAreaName">
              <option disabled value="">
                -- select {{ filterLevel.toUpperCase() }} --
              </option>
              <option v-for="a in currentFilterOptions" :key="a" :value="a">
                {{ a }}
              </option>
            </select>
          </label>

          <label class="field">
            <span>Group results by</span>
            <select v-model="groupLevel">
              <option v-for="key in validGroupLevels" :key="key" :value="key">
                {{ levelMeta[key].label }}
              </option>
            </select>
          </label>
        </div>

        <!-- sidebar left -->
        <aside class="sidebar">

          <h3 class="sidebar-title">Filters</h3>

          <label class="field">
            <span>Date from</span>
            <div class="date-input">
              <Datepicker
                v-model="dateFrom"
                :minDate="minDate"
                :maxDate="dateTo"
                :format="'yyyy-MM-dd'"
              />
            </div>

          </label>

          <label class="field">
            <span>Date to</span>
            <div class="date-input">
              <Datepicker
                v-model="dateTo"
                :minDate="dateFrom"
                :maxDate="maxDate"
                :format="'yyyy-MM-dd'"
              />
            </div>

          </label>

          <p v-if="dateAdjusted" class="info-message">
            End date was adjusted to match the new start date.
          </p>

          <label class="field">
            <span>Order by</span>
            <select v-model="orderBy">
              <option value="count">Count</option>
              <option value="density">Density</option>
            </select>
          </label>

          <label class="field">
            <span>Sort by</span>
            <select v-model="orderDir">
              <option v-for="opt in sortOptions" :key="opt.value" :value="opt.value">
                {{ opt.label }}
              </option>
            </select>
          </label>

          <label class="field">
            <span>Limit Results</span>
            <input v-model.number="limit" type="number" min="1" max="100" />
          </label>

          <button class="btn" :disabled="!canQuery || loading" @click="fetchStats">
            {{ loading ? "Loading..." : "Show Results" }}
          </button>
        </aside>

        <!-- main results -->
        <main class="main">

          <!-- <div class="divider" /> -->

          <div v-if="loading" class="loading">
            <span class="spinner" /> Loading crash data...
          </div>

          <div v-else-if="results.length" class="results">

            <h3 v-if="lastUsedFilters.limit">
              Top {{ results.length }} by {{ lastUsedFilters.orderBy }}, Grouped by:
              <span :title="levelMeta[lastUsedFilters.groupLevel].tooltip">
                {{ levelMeta[lastUsedFilters.groupLevel].label }}
              </span>
            </h3>

            <table>
              <thead>
              <tr>
                <th>Area</th>
                <th class="num">Crashes</th>
                <th class="num">Area (km2)</th>
                <th class="num">Density (/km2)</th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="r in results" :key="r.sa_name">
                <td>{{ r.sa_name }}</td>
                <td class="num">{{ r.num_accs }}</td>
                <td class="num">{{ fmt(r.geom_area_sq_km) }}</td>
                <td class="num">{{ fmt(r.acc_per_sq_km) }}</td>
              </tr>
              </tbody>
            </table>
          </div>

          <div v-else-if="emptyMessage.length > 0" class="placeholder">
            <strong>{{ emptyMessage }}</strong>
          </div>

          <div v-else class="placeholder">
            Select filters on the left and click <strong>Show Results</strong>.
          </div>

          <p v-if="(lastUsedFilters.limit > results.length) && (results.length > 0)" class="placeholder">
            Only {{ results.length }} regions found within {{ filterAreaName }}.
          </p>

          <span v-if="error" class="error">{{ error }}</span>
        </main>
      </div>
    </div>
  </section>
  <div class="hazard hazard--bottom">
    <img src="../../assets/images/hazard-stripes.svg" alt="" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import Datepicker from 'vue3-datepicker';
import api from "@/lib/api";

const keyword = ref("");
const filterLevel = ref<"sa4" | "sa3">("sa4");
const groupLevel  = ref<"sa2" | "sa3">("sa2");
const filterAreaName = ref("");

const levelLabels = {
  sa2: 'Suburb (SA2)',
  sa3: 'District (SA3)',
  sa4: 'Regional Zone (SA4)'
}

const levelMeta = {
  sa2: {
    label: 'Suburb (SA2)',
    tooltip: 'Typically aligns with suburbs or small communities'
  },
  sa3: {
    label: 'District (SA3)',
    tooltip: 'Groups multiple suburbs; may align with council or service regions'
  },
  sa4: {
    label: 'Regional Zone (SA4)',
    tooltip: 'Large zones used for labor market and regional planning'
  }
}

const dateFrom = ref<Date | null>(new Date("2020-01-01"));
const dateTo   = ref<Date | null>(new Date("2024-12-31"));
const maxDate  = new Date("2024-12-31");
const minDate  = new Date("2020-01-01");
const orderBy  = ref<"count" | "density">("density");
const orderDir = ref<"asc" | "desc">("desc");
const limit    = ref<number>(5);

function formatDate(d: Date | null, human_readable: boolean = false): string | undefined {
  if (!d) return undefined;

  return human_readable
    ? d.toLocaleDateString("en-AU", { day: "numeric", month: "short", year: "numeric" })
    : d.toISOString().split("T")[0];
}

const lastUsedFilters = ref({
  limit: null,
  orderBy: '',
  groupLevel: '',
});

const loading = ref(false);
const error = ref("");
const results = ref<any[]>([]);

const sa4Options = ref<string[]>([]);
const sa3Options = ref<string[]>([]);

const emptyMessage = ref("");

const sortOptions = computed(() => {
  if (orderBy.value === 'count') {
    return [
      { value: 'desc', label: 'Most accidents first' },
      { value: 'asc', label: 'Fewest accidents first' },
    ];
  } else if (orderBy.value === 'density') {
    return [
      { value: 'desc', label: 'Highest density (risky) first' },
      { value: 'asc', label: 'Lowest density (safe) first' },
    ];
  } else {
    return [
      { value: 'desc', label: 'Descending' },
      { value: 'asc', label: 'Ascending' },
    ];
  }
});

const currentFilterOptions = computed(() =>
  filterLevel.value === "sa4" ? sa4Options.value : sa3Options.value
);

const canQuery = computed(
  () => !!filterAreaName.value && !!filterLevel.value && !!groupLevel.value
);

const filterableLevels = computed<("sa3" | "sa4")[]>(() => ['sa4', 'sa3'])

const validGroupLevels = computed<("sa2" | "sa3")[]>(() => {
  return filterLevel.value === 'sa4'
    ? ['sa3', 'sa2']
    : filterLevel.value === 'sa3'
    ? ['sa2']
    : []
})

onMounted(async () => {
  try {
    const [sa4, sa3] = await Promise.all([
      api.get<string[]>("/distinct_sa4"),
      api.get<string[]>("/distinct_sa3"),
    ]);
    sa4Options.value = sa4.data;
    sa3Options.value = sa3.data;

    // Set default area name based on initial filterLevel
    if (filterLevel.value === "sa4" && sa4.data.length) {
      filterAreaName.value = sa4.data[0];
      await fetchStats();
    } else if (filterLevel.value === "sa3" && sa3.data.length) {
      filterAreaName.value = sa3.data[0];
    }

  } catch (e: any) {
    error.value = e?.response?.data?.detail || e.message || "Failed to load area lists";
  }
});

watch(filterLevel, (lvl) => {
  filterAreaName.value = "";

  // Reset groupLevel to first valid option
  const valid = validGroupLevels.value
  if (valid.length) {
    groupLevel.value = valid[0]
  }

  if (lvl === "sa3") {
    groupLevel.value = "sa2";
    if (sa3Options.value.length) {
      filterAreaName.value = sa3Options.value[0];
    }
  } else {
    if (sa4Options.value.length) {
      filterAreaName.value = sa4Options.value[0];
    }
  }
});

const dateAdjusted = ref(false);

watch(dateFrom, (newFrom) => {
  if (newFrom && dateTo.value && newFrom > dateTo.value) {
    dateTo.value = newFrom;
    dateAdjusted.value = true;
  } else {
    dateAdjusted.value = false;
  }
});

function fmt(n: number) {
  return Number(n).toLocaleString(undefined, { maximumFractionDigits: 2 });
}

async function fetchStats() {
  error.value = "";
  results.value = [];
  emptyMessage.value = "";
  loading.value = true;

  try {
    const payload: any = {
      filter_area_level: filterLevel.value,
      filter_area_name: filterAreaName.value,
      group_by_area_level: groupLevel.value,
      order_by: orderBy.value,
      order_dir: orderDir.value,
      limit: limit.value,
    };

    if (dateFrom.value) payload.date_from = formatDate(dateFrom.value);
    if (dateTo.value)   payload.date_to   = formatDate(dateTo.value);

    if (new Date(dateFrom.value) > new Date(dateTo.value)) {
      error.value = "Start date cannot be after end date.";
      loading.value = false;
      return;
    }

    const { data } = await api.post("/accident_stats", payload);
    results.value = data;

    if (!data.length) {

      results.value = [];
      const level = filterLevel.value.toUpperCase();
      const name = filterAreaName.value;

      emptyMessage.value = `No crash data was found for "${name}" between ${formatDate(dateFrom.value, true)} and ${formatDate(dateTo.value, true)}.\nOur system only stores data from ${formatDate(minDate, true)} to ${formatDate(maxDate, true)}.`;

    } else {
      results.value = data;
      emptyMessage.value = '';
      lastUsedFilters.value = {
        limit: limit.value,
        orderBy: orderBy.value,
        groupLevel: groupLevel.value,
      };
    }

  } catch (e: any) {
    error.value = e?.response?.data?.detail || e.message || "Request failed";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
:root{
  --amber: #0047e1;         /* matches hero tint */
  --amber-2: #000000;       /* lighter accent */
  --charcoal: #0f1419;      /* near-black text */
  --muted: #5b6470;         /* secondary text */
  --panel: #ffffff;         /* cards */
  --line: #ef0000;          /* borders */
  --line-2:#cbd5e1;
  --radius-lg: 14px;
  --radius: 10px;
  --shadow: 0 12px 28px rgba(0,0,0,.12);
  --shadow-soft: 0 2px 10px rgba(0,0,0,.06);
}

/* overall wrapper centers the white card */
.acc-wrap{
  max-width: 1200px;
  margin: 22px auto 40px;
  padding: 0 16px;
}

/* white panel with soft shadow + rounded */
.card{
  background: var(--panel);
  border: 1px solid rgba(15,20,25,.06);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
  padding: 22px 24px 26px;
}

.date-input {
  border: none;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  outline: none !important;
  box-shadow: none !important;
  border-color: none !important;
  padding: 14px 16px;
  border: 1px solid var(--line-2);
  border-radius: 12px;
  background-color: #f9fafb;
  color: var(--charcoal);
  font-size: 0.95rem;
  font-weight: 600;
  /* box-shadow: var(--shadow-soft); */
  transition: border-color 0.2s ease, box-shadow 0.2s ease, background-color 0.2s ease;
  appearance: none;
}

.v3dp__datepicker:focus {
  outline: none;
  /* border-color: var(--amber); */
  box-shadow: none;
  background-color: #ffffff;
}

.v3dp__datepicker:hover {
  background-color: #ffffff;
  border-color: #aab7c7;
}

.v3dp__datepicker:disabled {
  background-color: #f0f0f0;
  color: #999;
  cursor: not-allowed;
}

/* title: bold + subtle amber underline */
.title{
  margin: 0 0 16px;
  font-size: 28px;
  font-weight: 900;
  color: var(--charcoal);
  position: relative;
}
.title::after{
  content:"";
  position:absolute;
  left:0; bottom:-8px;
  width:88px; height:4px;
  background: linear-gradient(90deg, var(--amber), transparent);
  border-radius: 2px;
}

/* grid layout (sidebar + main) */
.layout {
  display: grid;
  grid-template-columns: 260px 1fr; /* sidebar left, main right */
  grid-template-rows: auto 1fr;
  gap: 22px 24px;
}

/* top filters across main column */
.topbar {
  grid-column: 2 / 3;
  grid-row: 1 / 2;
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  gap: 14px;
}

.sidebar-title {
  font-size: 1rem;
  font-weight: 800;
  color: var(--charcoal);
  margin-bottom: 6px;
  padding-bottom: 4px;
  border-bottom: 1px solid var(--line-2);
}

/* left sidebar with stacked controls */
.sidebar {
  grid-column: 1 / 2;
  grid-row: 2 / 3;
  display: flex;
  flex-direction: column;
  gap: 14px;
  font-size: 0.85rem;
  margin-top: 6px;
}

.sidebar .field > span {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--muted);
}

.sidebar .field select,
.sidebar .field input {
  padding: 10px 12px;
  font-size: 0.85rem;
  border-radius: 10px;
}

/* main area */
.main {
  grid-column: 2 / 3;
  grid-row: 2 / 3;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

/* inputs */
.field{ display:flex; flex-direction:column; gap:6px; }
.field > span{
  font-size:.9rem; font-weight:800; color:var(--charcoal);
  letter-spacing:.1px;
}

.field select,
.field input {
  padding: 14px 16px;
  border: 1px solid var(--line-2);
  border-radius: 12px;
  background-color: #f9fafb;
  color: var(--charcoal);
  font-size: 0.95rem;
  font-weight: 600;
  box-shadow: var(--shadow-soft);
  transition: border-color 0.2s ease, box-shadow 0.2s ease, background-color 0.2s ease;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 20 20' fill='%230f1419' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill-rule='evenodd' d='M5.23 7.21a.75.75 0 011.06.02L10 11.584l3.71-4.354a.75.75 0 111.14.976l-4.25 5a.75.75 0 01-1.14 0l-4.25-5a.75.75 0 01.02-1.06z' clip-rule='evenodd'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 16px 16px;
}

.field select:focus,
.field input:focus {
  outline: none;
  border-color: var(--amber);
  box-shadow: 0 0 0 3px rgba(0, 71, 225, 0.2);
  background-color: #ffffff;
}

.field select:hover,
.field input:hover {
  background-color: #ffffff;
  border-color: #aab7c7;
}

.field select:disabled,
.field input:disabled {
  background-color: #f0f0f0;
  color: #999;
  cursor: not-allowed;
}

.field > span {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--muted);
  margin-bottom: 2px;
}

/* keyword field */
.keyword input{
  width:100%;
  padding:12px 14px;
  border:1px solid var(--line-2);
  border-radius: 12px;
  box-shadow: var(--shadow-soft);
}

/* hazard-style divider between filters and table */
.divider{
  height: 10px;
  width: 100%;
  border-radius: 6px;
  background:
    repeating-linear-gradient(
      -45deg,
      #111 0 16px,
      var(--amber) 16px 32px
    );
  opacity: .15;
}

/* primary action button (black/amber) */
.btn {
  padding: 10px 16px;
  border: none;
  border-radius: 10px;
  background-color: #111111; /* solid black */
  color: #f6b300;            /* gold text */
  font-weight: 700;
  letter-spacing: 0.2px;
  cursor: pointer;
  box-shadow: var(--shadow-soft, 0 2px 6px rgba(0,0,0,0.2));
  transition: background-color 0.2s ease, transform 0.05s ease, filter 0.18s ease, opacity 0.15s ease;
}

.btn:hover {
  background-color: #1a1a1a; /* slightly lighter black for hover */
  filter: brightness(1.2);   /* subtle glow */
}

.btn:active {
  transform: scale(0.98);
  background-color: #1a1a1a; /* maintain hover color on click */
  color: #f6b300;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background-color: #111111; /* prevent transparency */
  color: #999999;            /* muted text for disabled state */
}

/* results */
.results h3{
  margin: 6px 6px 10px;
  font-size: 28px;
  font-weight: 900;
  color: var(--charcoal);
}

/* table */
table{
  width:100%;
  border-collapse:collapse;
  background:#fff;
  border:1px solid var(--line);
  border-radius: 12px;
  overflow:hidden;
  box-shadow: var(--shadow-soft);
}
thead th{
  background: linear-gradient(#fffdfa, #fff7e1);
  color:#151922;
  text-align:left;
  padding:14px 16px;
  border-bottom:1px solid var(--line);
  font-weight:900;
}
tbody td{
  padding:14px 16px;
  border-bottom:1px solid var(--line);
  color:#1b2330;
}
tbody tr:nth-child(odd) td{
  background:#fafbff;
}
tbody tr:last-child td{
  border-bottom:0;
}
.num{ text-align:right; }

/* empty state + errors */
.placeholder{
  padding: 22px;
  color: var(--muted);
  border:1px dashed var(--line-2);
  border-radius: 12px;
  background:#fffef7;
}

.placeholder:hover {
  cursor: pointer;
  transition: box-shadow 0.2s ease;
  box-shadow: 0 0 0 2px var(--line-2);
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 20px;
  min-height: 200px;
  font-size: 1.25rem; /* larger text */
  font-weight: 600;
  color: #090909;     /* gold text */
  letter-spacing: 0.4px;
  text-align: center;
}

.spinner {
  width: 52px;
  height: 52px;
  margin-bottom: 20px;
  border: 6px solid rgba(246, 179, 0, 0.2); /* gold tint */
  border-top-color: #005ef6;               /* solid gold */
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error{ color:#c81e1e; font-weight:700; }

/* responsive */
@media (max-width: 980px){
  .layout{
    grid-template-columns: 1fr;
    grid-template-rows: auto auto auto;
  }
  .topbar{
    grid-column: 1 / 2;
    grid-template-columns: 1fr;
  }
  .sidebar{
    grid-column: 1 / 2; grid-row: auto;
    flex-direction: row; flex-wrap: wrap;
  }
  .sidebar .field{ min-width: 200px; flex: 1 1 220px; }
  .btn{ width: 200px; }
}
.hazard {
  position: relative;
  width: 100%;
  z-index: 2;
}
.hazard img {
  width: 100%;
  height: 30px;
  object-fit: cover;
}
.hazard--top {
  margin-bottom: 120px;
}
.hazard--bottom {
  margin-top: -10px;
  transform: rotate(180deg);
}
</style>
