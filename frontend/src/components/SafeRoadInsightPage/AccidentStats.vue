<template>
  <section class="acc-wrap">
    <div class="card">
      <h2 class="title">Crash Statistics Explorer</h2>

      <div class="layout">
        <!-- topbar across main column -->
        <div class="topbar">
          <label class="field">
            <span>Filter by area level</span>
            <select v-model="filterLevel">
              <option value="sa4">Region (SA4)</option>
              <option value="sa3">Sub-region / District (SA3)</option>
            </select>
          </label>

          <label class="field">
            <span>Area name</span>
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
            <span>Group by</span>
            <select v-model="groupLevel">
              <option value="sa2">Local Area / Suburb (SA2)</option>
              <option v-if="filterLevel === 'sa4'" value="sa3">Sub-region / District (SA3)</option>
            </select>
          </label>
        </div>

        <!-- sidebar left -->
        <aside class="sidebar">
          <label class="field">
            <span>Date from</span>
            <input v-model="dateFrom" type="date" />
          </label>

          <label class="field">
            <span>Date to</span>
            <input v-model="dateTo" type="date" />
          </label>

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
            <span>Top Number</span>
            <input v-model.number="limit" type="number" min="1" max="100" />
          </label>

          <button class="btn" :disabled="!canQuery || loading" @click="fetchStats">
            {{ loading ? "Loading…" : "Show Results" }}
          </button>
        </aside>

        <!-- main results -->
        <main class="main">

          <div class="divider" />

          <div v-if="results.length" class="results">
            <h3>Top {{ limit }} ({{ orderBy }}) grouped by {{ groupLevel.toUpperCase() }}</h3>
            <table>
              <thead>
              <tr>
                <th>Area</th>
                <th class="num">Accidents</th>
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

          <div v-else class="placeholder">
            Select filters on the left and click <strong>Show Results</strong>.
          </div>

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
import api from "@/lib/api";

const keyword = ref("");
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

const sa4Options = ref<string[]>([]);
const sa3Options = ref<string[]>([]);

const currentFilterOptions = computed(() =>
  filterLevel.value === "sa4" ? sa4Options.value : sa3Options.value
);

const canQuery = computed(
  () => !!filterAreaName.value && !!filterLevel.value && !!groupLevel.value
);

onMounted(async () => {
  try {
    const [sa4, sa3] = await Promise.all([
      api.get<string[]>("/distinct_sa4"),
      api.get<string[]>("/distinct_sa3"),
    ]);
    sa4Options.value = sa4.data;
    sa3Options.value = sa3.data;
  } catch (e: any) {
    error.value = e?.response?.data?.detail || e.message || "Failed to load area lists";
  }
});

watch(filterLevel, (lvl) => {
  filterAreaName.value = "";
  if (lvl === "sa3") groupLevel.value = "sa2";
});

function fmt(n: number) {
  return Number(n).toLocaleString(undefined, { maximumFractionDigits: 2 });
}

async function fetchStats() {
  error.value = "";
  results.value = [];
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
</script>

<style scoped>
/* ====== Theme tokens (SafeTrek) ====== */
:root{
  --amber: #e1a600;         /* matches your hero tint */
  --amber-2: #000000;       /* lighter accent */
  --charcoal: #0f1419;      /* near-black text */
  --muted: #5b6470;         /* secondary text */
  --panel: #ffffff;         /* cards */
  --line: #e7eaee;          /* borders */
  --line-2:#cbd5e1;
  --radius-lg: 14px;
  --radius: 10px;
  --shadow: 0 12px 28px rgba(0,0,0,.12);
  --shadow-soft: 0 2px 10px rgba(0,0,0,.06);
}

/* overall wrapper centers the white card */
.acc-wrap{
  max-width: 1200px;
  margin: 26px auto 40px;
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
.layout{
  display:grid;
  grid-template-columns: 260px 1fr;
  grid-template-rows: auto 1fr;
  gap: 22px 24px;
}

/* top filters across main column */
.topbar{
  grid-column: 2 / 3;
  display:grid;
  grid-template-columns: repeat(3,1fr);
  gap: 14px;
}

/* left sidebar with stacked controls */
.sidebar{
  grid-column: 1 / 2;
  grid-row: 1 / 3;
  display:flex;
  flex-direction:column;
  gap:14px;
}

/* main area */
.main{
  grid-column: 2 / 3;
  display:flex;
  flex-direction:column;
  gap:14px;
}

/* inputs */
.field{ display:flex; flex-direction:column; gap:6px; }
.field > span{
  font-size:.9rem; font-weight:800; color:var(--charcoal);
  letter-spacing:.1px;
}
.field select, .field input{
  padding: 12px 14px;
  border: 1px solid var(--line-2);
  border-radius: 12px;
  background: #fff;
  color: var(--charcoal);
  box-shadow: var(--shadow-soft);
  transition: border-color .15s ease, box-shadow .15s ease;
}
.field select:focus, .field input:focus{
  outline:none;
  border-color:#aab7c7;
  box-shadow: 0 0 0 3px rgba(241,193,66,.3);
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
  opacity: .15;              /* subtle — not shouting */
}

/* primary action button (black/amber) */
.btn{
  height: 46px;
  border: 0;
  border-radius: 12px;
  background: #dfa500;
  color: var(--amber-2);
  font-weight: 900;
  letter-spacing:.2px;
  cursor: pointer;
  box-shadow: var(--shadow-soft);
  transition: transform .05s ease, filter .18s ease, opacity .15s ease;
}
.btn:hover{ filter: brightness(1.55); }
.btn:active{ transform: translateY(1px); }
.btn:disabled{ opacity:.85; cursor:not-allowed; }

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
  margin-bottom: 120px; /* tuck neatly */
}
.hazard--bottom {
  margin-top: -10px;
  transform: rotate(180deg);
}
</style>
