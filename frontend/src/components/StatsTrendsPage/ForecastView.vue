<template>

  <section class="theme-wrap">
    <div class="theme-inner">
      <div class="header-row">
        <h2 class="title">Crash & Injury Forecast</h2>
        <div class="controls">

          <label class="field">
            <span>From year</span>
            <input type="number" v-model.number="yearFrom" min="2000" max="2100" />
          </label>

          <label class="field">
            <span>To year</span>
            <input type="number" v-model.number="yearTo" :min="yearFrom" max="2100" />
          </label>

          <label class="field">
            <span>Target year</span>
            <input type="number" v-model.number="targetYear" :min="yearTo" max="2100" />
          </label>

          <label class="field">
            <span>Method</span>
            <select v-model="method">
              <option value="ols">Trend (OLS)</option>
              <option value="mean">Average (Mean)</option>
            </select>
          </label>

          <button class="btn" :disabled="loading" @click="load">
            {{ loading ? "Loading…" : "Refresh" }}
          </button>
        </div>
      </div>

      <!-- Chart -->
      <div class="chart-box">
        <Line v-if="chartData" :data="chartData" :options="chartOptions" />
        <div v-else class="placeholder">Pick a range and press <b>Refresh</b>.</div>
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

const yearFrom   = ref<number>(2012);
const yearTo     = ref<number>(2024);
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
/* Theme tokens */
:root{
  --amber: #e14f00;
  --amber-soft: rgba(255, 0, 0, 0.15);
  --black: #111111;
  --muted: #5b6470;
  --white: #0048e8;
  --line: rgba(0,0,0,.12);
  --radius: 12px;
  --shadow: 0 8px 28px rgba(0,0,0,.12);
}

.theme-wrap{
  max-width: 1200px;
  margin: 22px auto 40px;
  padding: 0 16px;
}
.theme-inner{
  background: transparent;
}

.header-row{
  display:flex;
  align-items:flex-end;
  justify-content:space-between;
  gap: 16px;
  flex-wrap: wrap;
}
.title{
  margin: 0 0 8px;
  font-weight: 900;
  font-size: 32px;
  color: var(--black);
  letter-spacing: .3px;
}

.controls{
  display:grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 10px;
  align-items:end;
  min-width: 560px;
}
.field{ display:flex; flex-direction:column; gap:6px; }
.field > span{ font-size:.9rem; font-weight:800; color:var(--black); }
.field input, .field select{
  height: 44px;
  padding: 10px 12px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background:white;
  color: var(--black);
  box-shadow: 0 2px 8px rgba(0,0,0,.06);
}

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

.chart-box{
  height: 380px;
  margin-top: 12px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--amber-soft);
  box-shadow: var(--shadow);
  padding: 8px 10px;
}
.placeholder{ padding: 18px; color: var(--muted); }

.divider{
  height: 14px;
  margin: 14px 0 10px;
  border-radius: 8px;
  background:
    repeating-linear-gradient(
      -45deg,
      #111 0 18px,
      var(--amber) 18px 36px
    );
  opacity: .2;
}

/* Table */
.table-card{
  background: var(--white);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 10px 10px 4px;
}
.table-card h3{
  margin: 4px 6px 10px;
  font-weight: 900;
  color: var(--black);
}
table{ width:100%; border-collapse: collapse; }
thead th{
  background: #d89c00;
  text-align:left;
  padding: 12px 14px;
  border-bottom: 1px solid var(--line);
  font-weight: 900;
  color: #151922;
}
tbody td{
  padding: 12px 14px;
  border-bottom: 1px solid var(--line);
  color: #1b2330;
}
tbody tr:last-child td{ border-bottom: 0; }
.num{ text-align:right; }
.forecast-row td{ background: #ff0000; font-weight: 800; }
.error{ color:#c81e1e; font-weight:700; margin-top:10px; }

@media (max-width: 980px){
  .controls{
    grid-template-columns: 1fr 1fr;
  }
  .btn{ grid-column: 1 / -1; }
}
</style>
