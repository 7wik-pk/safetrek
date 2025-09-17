<template>
  <section class="theme-wrap">
    <div class="theme-inner">
      <div class="header-row">
        <h2 class="title">Crash & Injury Forecast</h2>

        <!-- Cards -->
        <div class="cards">
          <!-- Card 1: Time range -->
          <div class="card">
            <h3 class="card-title">Time range</h3>
            <div class="fields">
              <label class="field">
                <span>From year</span>
                <select v-model.number="yearFrom">
                  <option disabled value="">Select year</option>
                  <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
                </select>
              </label>

              <label class="field">
                <span>To year</span>
                <select v-model.number="yearTo">
                  <option disabled value="">Select year</option>
                  <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
                </select>
              </label>

              <label class="field">
                <span>Target year</span>
                <input type="number" v-model.number="targetYear" :min="yearTo" max="2100" />
              </label>
            </div>
          </div>

          <!-- Card 2: Options -->
          <div class="card">
            <h3 class="card-title">Forecast options</h3>
            <div class="fields">
              <label class="field">
                <span>Method</span>
                <select v-model="method">
                  <option value="ols">Trend (OLS)</option>
                  <option value="mean">Average (Mean)</option>
                </select>
              </label>

              <div class="field action-slot">
                <button class="btn" :disabled="loading" @click="load">
                  {{ loading ? "Loading…" : "Refresh" }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <p v-if="yearError" class="error">{{ yearError }}</p>
      </div>

      <!-- Chart -->
      <div class="chart-card">
        <div class="chart-box">
          <Line v-if="chartData" :data="chartData" :options="chartOptions" />
          <div v-else class="placeholder">Pick a range and press <b>Refresh</b>.</div>
        </div>
      </div>

      <div class="divider"></div>

      <!-- Table -->
      <div class="table-card" v-if="history.length">
        <h3>Yearly totals & forecast</h3>
        <table>
          <thead>
          <tr>
            <th>Year</th>
            <th class="num">Crashes</th>
            <th class="num">Total injuries</th>
            <th class="num">Serious injuries</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="row in history" :key="row.year">
            <td>{{ row.year }}</td>
            <td class="num">{{ fmt(row.crashes) }}</td>
            <td class="num">{{ fmt(row.total_injuries) }}</td>
            <td class="num">{{ fmt(row.serious_injuries) }}</td>
          </tr>
          <tr class="forecast-row" v-if="forecast">
            <td>{{ forecast.year }} (forecast)</td>
            <td class="num">{{ fmt(forecast.crashes) }}</td>
            <td class="num">{{ fmt(forecast.total_injuries) }}</td>
            <td class="num">{{ fmt(forecast.serious_injuries) }}</td>
          </tr>
          </tbody>
        </table>
      </div>

      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="yearError" class="error">{{ yearError }}</p>
    </div>
  </section>
</template>


<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import api from "@/lib/api";


import { Line } from "vue-chartjs";
import {
  Chart as ChartJS,
  LineElement, PointElement, LinearScale, CategoryScale,
  Title, Tooltip, Legend,
} from "chart.js";


ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Title, Tooltip, Legend);

type YearItem = {
  year: number;
  crashes: number;
  total_injuries: number;
  serious_injuries: number;
};
type ForecastPayload = {
  method: "ols" | "mean";
  history: YearItem[];
  forecast_year: number;
  forecast: YearItem;
  model_info?: any;
};
const minYear = 2012
const maxYear = 2024
const yearFrom   = ref(2019);
const yearTo     = ref(2024);

const years = computed(() => {
  const a = []
  for (let y = minYear; y <= maxYear; y++) a.push(y)
  return a})

// validation years
const yearError = computed(() => {
  if (yearFrom.value == null || yearTo.value == null) return ''

  if (yearFrom.value < minYear || yearFrom.value > maxYear) {
    return `“From year” must be between ${minYear} and ${maxYear}.`
  }
  if (yearTo.value < minYear || yearTo.value > maxYear) {
    return `“To year” must be between ${minYear} and ${maxYear}.`
  }
  if (yearFrom.value > yearTo.value) {
    return '“From year” cannot be after “To year”.'
  }
  return '' // valid
})

const isYearValid = computed(() => yearError.value === '')
const targetYear = ref<number>(2028);
const method     = ref<"ols" | "mean">("ols");

const loading = ref(false);
const error   = ref("");
const history = ref<YearItem[]>([]);
const forecast = ref<YearItem | null>(null);

async function load() {
  error.value = "";
  loading.value = true;
  try {
    const { data } = await api.get<ForecastPayload>("/forecast/yearly", {
      params: {
        year_from: yearFrom.value,
        year_to: yearTo.value,
        target_year: targetYear.value,
        method: method.value,
      },
    });
    history.value = data.history;
    forecast.value = data.forecast;
  } catch (e: any) {
    error.value = e?.response?.data?.detail || e.message || "Request failed";
  } finally {
    loading.value = false;
  }
}
onMounted(load);

/* ---------- Chart ---------- */
const labels = computed(() => {
  const base = history.value.map(h => String(h.year));
  if (forecast.value) base.push(String(forecast.value.year));
  return base;
});

// SafeTrek palette
const C_BLACK = "#111111";
const C_AMBER = "#E1A600";
const C_AMBER_SOFT = "rgba(225,166,0,.18)";
const C_RED = "#D9480F";

function mkSeries(values: number[], label: string, color: string) {
  return {
    label,
    data: values,
    borderColor: color,
    backgroundColor: color,
    tension: 0.25,
    borderWidth: 2,
    pointRadius: 3,
    pointHoverRadius: 5,
    fill: false,
  };
}

const chartData = computed(() => {
  if (!history.value.length) return null;

  const y = history.value.map(h => h.year);
  const crashes = history.value.map(h => h.crashes);
  const total   = history.value.map(h => h.total_injuries);
  const serious = history.value.map(h => h.serious_injuries);

  const datasets: any[] = [
    mkSeries(crashes, "Crashes", C_BLACK),
    mkSeries(total, "Total injuries", "#1E3A8A"),   // deep blue for contrast
    mkSeries(serious, "Serious injuries", C_RED),
  ];

  if (forecast.value) {
    const pad = new Array(y.length).fill(null);
    datasets.push(
      { label: "Crashes (forecast)", data: [...pad, forecast.value.crashes], showLine: false, pointRadius: 6, pointStyle: "triangle", backgroundColor: C_BLACK, borderColor: C_BLACK },
      { label: "Total injuries (forecast)", data: [...pad, forecast.value.total_injuries], showLine: false, pointRadius: 6, pointStyle: "rectRot", backgroundColor: C_AMBER, borderColor: C_AMBER },
      { label: "Serious injuries (forecast)", data: [...pad, forecast.value.serious_injuries], showLine: false, pointRadius: 6, pointStyle: "star", backgroundColor: C_RED, borderColor: C_RED },
    );
  }

  return { labels: labels.value, datasets };
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: "top" as const,
      labels: { color: C_BLACK, boxWidth: 18, usePointStyle: false },
    },
    title: { display: false },
    tooltip: { mode: "index" as const, intersect: false, backgroundColor: "#111", titleColor: "#FFD54A", bodyColor: "#fff" },
  },
  interaction: { mode: "index" as const, intersect: false },
  layout: { padding: { left: 6, right: 6, top: 4, bottom: 6 } },
  scales: {
    x: {
      ticks: { color: C_BLACK },
      grid: { color: "rgba(17,17,17,.10)" }, // subtle dark grid
    },
    y: {
      beginAtZero: true,
      ticks: { color: C_BLACK },
      grid: { color: "rgba(17,17,17,.10)" },
    },
  },
  backgroundColor: "transparent",
} as const;

/* ---------- utils ---------- */
function fmt(n: number) {
  return Number(n).toLocaleString();
}
</script>

<style scoped>
/* Page shell */
.theme-wrap {
  background: #fff;
}
.theme-inner {
  max-width: 1180px;
  margin: 0 auto;
  padding: 18px 22px 28px;
}

/* Header */
.header-row {
  display: grid;
  gap: 12px;
}
.title {
  margin: 0;
  font-size: clamp(22px, 3.2vw, 28px);
  font-weight: 900;
  color: #111;
}

/* Card layout for control blocks */
.cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}
@media (max-width: 860px){
  .cards { grid-template-columns: 1fr; }
}

/* Card */
.card {
  background: #fff;
  border: 1px solid #ece7d5;
  border-radius: 12px;
  box-shadow: 0 8px 22px rgba(0,0,0,.06);
  padding: 14px 14px 12px;
}
.card-title {
  margin: 0 0 8px;
  font-size: 16px;
  font-weight: 800;
  letter-spacing: .02em;
  color: #111;
}

/* Fields grid inside a card */
.fields {
  display: grid;
  grid-template-columns: repeat(3, minmax(160px, 1fr));
  gap: 10px;
}
@media (max-width: 960px){
  .fields { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 600px){
  .fields { grid-template-columns: 1fr; }
}

.field {
  display: grid;
  gap: 6px;
}
.field > span {
  font-size: 12px;
  font-weight: 700;
  color: #555;
  letter-spacing: .02em;
}
select, input[type="number"] {
  padding: 10px 12px;
  border: 1px solid #d9d5c6;
  border-radius: 10px;
  background: #f6fbf7;                  /* soft light fill */
  color: #222;
  font-size: 14px;
  line-height: 1;
}
select:focus, input[type="number"]:focus {
  outline: none;
  border-color: #f0c24b;                /* brand gold-ish */
  box-shadow: 0 0 0 3px rgba(246,179,0,.18);
}

/* Put the button at the bottom-right of the card */
.action-slot {
  display: grid;
  align-content: end;
  justify-content: end;
}

/* Primary action */
.btn {
  appearance: none;
  border: 0;
  border-radius: 999px;
  padding: 10px 18px;
  font-weight: 800;
  letter-spacing: .02em;
  background: linear-gradient(180deg, #f6b300, #c98600);
  color: #111;
  cursor: pointer;
  box-shadow: 0 10px 20px rgba(0,0,0,.12);
  transition: transform .12s ease, filter .2s ease;
}
.btn:hover { filter: brightness(1.03); transform: translateY(-1px); }
.btn:disabled { opacity: .6; cursor: not-allowed; transform: none; }

/* Chart card for consistent look */
.chart-card {
  background: #fff;
  border: 1px solid #ece7d5;
  border-radius: 12px;
  box-shadow: 0 8px 22px rgba(0,0,0,.06);
  padding: 14px;
  margin-top: 6px;
}
.chart-box { min-height: 320px; }
.placeholder { color: #666; padding: 30px 6px; }

/* Divider */
.divider {
  height: 1px;
  background: #efefef;
  margin: 14px 0;
}

/* Table card */
.table-card {
  background: #fff;
  border: 1px solid #ece7d5;
  border-radius: 12px;
  box-shadow: 0 8px 22px rgba(0,0,0,.06);
  padding: 14px;
}
.table-card h3 {
  margin: 0 0 10px;
  font-size: 16px;
  font-weight: 800;
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}
thead th {
  text-align: left;
  color: #555;
  font-weight: 700;
  border-bottom: 1px solid #eee7d7;
  padding: 8px 6px;
}
tbody td {
  padding: 8px 6px;
  border-bottom: 1px solid #f3f0e6;
}
tbody tr:last-child td { border-bottom: 0; }
.num { text-align: right; }
.forecast-row td { font-weight: 700; background: #fffdf3; }

/* Error */
.error {
  color: #7f1d1d;
  background: #fee2e2;
  border: 1px solid #fecaca;
  padding: 8px 10px;
  border-radius: 8px;
  margin-top: 8px;
}
</style>

