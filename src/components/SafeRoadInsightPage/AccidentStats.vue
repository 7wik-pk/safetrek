<template>
  <section class="acc-wrap">
    <h2 class="title">Crash Statistics Explorer</h2>

    <!-- Row 1: free text (you can wire this to your own backend later) -->
    <div class="row">
      <label class="field">
        <span>Keyword (optional)</span>
        <input v-model="keyword" type="text" placeholder="Type anything…" />
      </label>
    </div>

    <!-- Row 2: Filter level & area -->
    <div class="row two">
      <label class="field">
        <span>Filter by area level</span>
        <select v-model="filterLevel">
          <option value="sa4">SA4</option>
          <option value="sa3">SA3</option>
        </select>
      </label>

      <label class="field">
        <span>Area name</span>
        <select v-model="filterAreaName">
          <option disabled value="">-- select {{ filterLevel.toUpperCase() }} --</option>
          <option v-for="a in currentFilterOptions" :key="a" :value="a">{{ a }}</option>
        </select>
      </label>
    </div>

    <!-- Row 3: Group-by level -->
    <div class="row two">
      <label class="field">
        <span>Group by</span>
        <select v-model="groupLevel">
          <!-- SA2 always allowed -->
          <option value="sa2">SA2</option>
          <!-- SA3 allowed only when filter is SA4 (backend rule: group lower than filter) -->
          <option v-if="filterLevel === 'sa4'" value="sa3">SA3</option>
        </select>
      </label>

      <!-- If grouping by SA2, you can optionally let users pre-narrow to a specific SA2 later -->
      <div class="field info">
        Group level must be <em>lower</em> than filter level (backend rule).
      </div>
    </div>

    <!-- Row 4: Dates -->
    <div class="row two">
      <label class="field">
        <span>Date from</span>
        <input v-model="dateFrom" type="date" />
      </label>
      <label class="field">
        <span>Date to</span>
        <input v-model="dateTo" type="date" />
      </label>
    </div>

    <!-- Row 5: Ordering + Limit -->
    <div class="row three">
      <label class="field">
        <span>Order by</span>
        <select v-model="orderBy">
          <option value="count">Count</option>
          <option value="density">Density</option>
        </select>
      </label>

      <label class="field">
        <span>Direction</span>
        <select v-model="orderDir">
          <option value="desc">Desc</option>
          <option value="asc">Asc</option>
        </select>
      </label>

      <label class="field">
        <span>Top N</span>
        <input v-model.number="limit" type="number" min="1" max="100" />
      </label>
    </div>

    <div class="actions">
      <button class="btn" :disabled="!canQuery" @click="fetchStats">Show Results</button>
      <span v-if="loading" class="loading">Loading…</span>
      <span v-if="error" class="error">{{ error }}</span>
    </div>

    <!-- Results -->
    <div v-if="results.length" class="results">
      <h3>Top {{ limit }} ({{ orderBy }}) grouped by {{ groupLevel.toUpperCase() }}</h3>
      <table>
        <thead>
        <tr>
          <th>Area</th>
          <th class="num">Accidents</th>
          <th class="num">Area (km²)</th>
          <th class="num">Density (/km²)</th>
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
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import api from "@/lib/api";

// --- UI state
const keyword = ref(""); // optional; not sent to backend (reserved for your future filter)
const filterLevel = ref<"sa4" | "sa3">("sa4");
const groupLevel  = ref<"sa2" | "sa3">("sa2");
const filterAreaName = ref("");

const dateFrom = ref<string>("2020-01-01");
const dateTo   = ref<string>("2024-12-31");
const orderBy  = ref<"count" | "density">("density");
const orderDir = ref<"asc" | "desc">("desc");
const limit    = ref<number>(5);

const loading = ref(false);
const error = ref("");
const results = ref<any[]>([]);

// --- Dropdown data
const sa4Options = ref<string[]>([]);
const sa3Options = ref<string[]>([]);
const sa2Options = ref<string[]>([]); // loaded if you ever need SA2 list directly

// Which list feeds the "Area name" select
const currentFilterOptions = computed(() =>
  filterLevel.value === "sa4" ? sa4Options.value : sa3Options.value
);

// Enable/disable button
const canQuery = computed(() => !!filterAreaName.value && !!filterLevel.value && !!groupLevel.value);

// Fetch distinct lists on mount
onMounted(async () => {
  await Promise.all([loadSA4(), loadSA3()]);
});

// When filter level changes, clear the chosen name and adjust allowed group level
watch(filterLevel, (lvl) => {
  filterAreaName.value = "";
  // If user filters by SA3, group must be SA2
  if (lvl === "sa3" && groupLevel.value !== "sa2") {
    groupLevel.value = "sa2";
  }
});

// --- API calls (distinct lists)
async function loadSA4() {
  const { data } = await api.get<string[]>("/distinct_sa4");
  sa4Options.value = data;
}
async function loadSA3() {
  const { data } = await api.get<string[]>("/distinct_sa3");
  sa3Options.value = data;
}
// If you want an SA2 dropdown later:
async function loadSA2() {
  const { data } = await api.get<string[]>("/distinct_sa2");
  sa2Options.value = data;
}

// --- Query stats
async function fetchStats() {
  error.value = "";
  results.value = [];
  loading.value = true;

  try {
    const payload: any = {
      filter_area_level: filterLevel.value,
      filter_area_name: filterAreaName.value,
      group_by_area_level: groupLevel.value,   // must be lower than filter level (backend rule)
      order_by: orderBy.value,                 // "count" or "density"
      order_dir: orderDir.value,               // "asc" or "desc"
      limit: limit.value,
    };

    if (dateFrom.value) payload.date_from = dateFrom.value;
    if (dateTo.value)   payload.date_to   = dateTo.value;

    const { data } = await api.post("/accident_stats", payload);
    results.value = data;
  } catch (e: any) {
    error.value = e?.response?.data?.detail || e.message || "Request failed";
  } finally {
    loading.value = false;
  }
}

// formatting helper
function fmt(n: number) {
  return Number(n).toLocaleString(undefined, { maximumFractionDigits: 2 });
}
</script>

<style scoped>
.acc-wrap {
  max-width: 980px;
  margin: 24px auto 64px auto;
  padding: 0 16px;
  color: #0f172a;
}

.title {
  font-size: 1.6rem;
  font-weight: 800;
  margin: 0 0 1rem;
}

.row {
  display: grid;
  gap: 16px;
  margin-bottom: 16px;
}
.row.two   { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.row.three { grid-template-columns: repeat(3, minmax(0, 1fr)); }

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.field > span {
  font-size: .9rem;
  font-weight: 600;
}
.field input, .field select {
  padding: 10px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  background: #fff;
}

.info {
  align-self: end;
  color: #475569;
  font-size: .9rem;
}

.actions {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 12px 0 20px;
}
.btn {
  padding: 10px 16px;
  border-radius: 8px;
  border: 0;
  background: #111827;
  color: #fbbf24;
  font-weight: 700;
  cursor: pointer;
}
.btn:disabled {
  opacity: .5; cursor: not-allowed;
}
.loading { color: #2563eb; }
.error   { color: #dc2626; }

.results h3 {
  margin: 24px 0 8px;
  font-size: 1.1rem;
  font-weight: 800;
}
table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
}
th, td { padding: 10px 12px; border-bottom: 1px solid #eef2f7; }
th { background: #f8fafc; text-align: left; }
.num { text-align: right; }
@media (max-width: 780px) {
  .row.two   { grid-template-columns: 1fr; }
  .row.three { grid-template-columns: 1fr; }
}
</style>
