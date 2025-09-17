<template>
  <section class="trend-card">
    <header class="head">
      <h2 class="title">Crash & Injury Trends</h2>

      <div class="controls">
        <select v-model="mode" class="select">
          <option value="monthly">Monthly (by year)</option>
          <option value="yearly">Yearly (range)</option>
        </select>

        <!-- year pickers (locked 2020-2024) -->
        <template v-if="mode === 'monthly'">
          <select v-model.number="year" class="select">
            <option v-for="y in YEARS" :key="y" :value="y">{{ y }}</option>
          </select>
        </template>
        <template v-else>
          <select v-model.number="yearFrom" class="select">
            <option v-for="y in YEARS" :key="'from-'+y" :value="y">{{ y }}</option>
          </select>
          <span class="arrow">→</span>
          <select v-model.number="yearTo" class="select">
            <option v-for="y in YEARS" :key="'to-'+y" :value="y">{{ y }}</option>
          </select>
        </template>

        <button class="btn" @click="load" :disabled="loading">
          {{ loading ? "Loading..." : "Refresh" }}
        </button>
      </div>
    </header>

    <div class="chart-wrap">
      <Line v-if="chartData" :data="chartData" :options="chartOptions" />
      <p v-else class="placeholder">Pick a year or range, then click Refresh.</p>
    </div>

    <footer v-if="error" class="error">{{ error }}</footer>
  </section>
</template>

<script setup lang="ts">
import {ref, computed, onMounted, watchEffect} from "vue";
import api from "@/lib/api";

// Chart.js
import { Line } from "vue-chartjs";
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Title,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";

ChartJS.register(
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Title,
  Tooltip,
  Legend,
  Filler
);

// chart-area background plugin
const chartAreaBg = {
  id: "chartAreaBg",
  beforeDraw(chart: any, _args: any, opts: any) {
    const { ctx, chartArea } = chart;
    if (!chartArea) return;
    const { left, top, width, height } = chartArea;
    ctx.save();
    ctx.fillStyle = opts?.color || "rgba(246,179,0,0.12)";
    ctx.fillRect(left, top, width, height);
    ctx.restore();
  },
};
ChartJS.register(chartAreaBg as any);


type MonthlyItem = {
  period: string; // 'YYYY-MM'
  crashes: number;
  total_injuries: number;
  serious_injuries: number;
};
type MonthlyResp = {
  year: number;
  data: MonthlyItem[];
};
type YearlyItem = {
  year: number;
  crashes: number;
  total_injuries: number;
  serious_injuries: number;
};

// ----- Theme colors -----
const THEME = {
  text: "#111111",
  grid: "rgba(17,17,17,0.10)",
  // series
  crashes: "#111827",
  injuries: "#0004ff",
  serious: "#b91c1c",
  crashesFill: "rgba(17,24,39,0.08)",
  injuriesFill: "rgb(0,4,253)",
  seriousFill: "rgba(185,28,28,0.12)",
};

// ----- Year limits -----
const YEARS = [2020, 2021, 2022, 2023, 2024];
const mode = ref<"monthly" | "yearly">("yearly");
const year = ref<number>(2022);
const yearFrom = ref<number>(2018 in YEARS ? 2018 : 2020); // guard
const yearTo = ref<number>(2022);

// enforce 2020–2024 always
const clampYear = (y: number) => Math.min(2024, Math.max(2020, y));
watchEffect(() => {
  if (mode.value === "monthly") {
    year.value = clampYear(year.value);
  } else {
    yearFrom.value = clampYear(yearFrom.value);
    yearTo.value = clampYear(yearTo.value);
  }
});

// State
const loading = ref(false);
const error = ref("");
const monthly = ref<MonthlyItem[] | null>(null);
const yearly = ref<YearlyItem[] | null>(null);

// Load from API
async function load() {
  error.value = "";
  loading.value = true;
  try {
    if (mode.value === "monthly") {
      const { data } = await api.get<MonthlyResp>("/trends/monthly", {
        params: { year: year.value },
      });
      monthly.value = data.data;
      yearly.value = null;
    } else {
      const { data } = await api.get<YearlyItem[]>("/trends/yearly", {
        params: { year_from: yearFrom.value, year_to: yearTo.value },
      });
      yearly.value = data;
      monthly.value = null;
    }
  } catch (e: any) {
    error.value =
      e?.response?.data?.detail || e?.response?.data || e.message || "Request failed";
    monthly.value = null;
    yearly.value = null;
  } finally {
    loading.value = false;
  }
}

onMounted(load);

//  Chart data
function mkSeries(
  label: string,
  data: number[],
  stroke: string,
  fill: string
) {
  return {
    label,
    data,
    borderColor: stroke,
    backgroundColor: fill,
    tension: 0.3,
    pointRadius: 3,
    pointHoverRadius: 5,
    borderWidth: 2,
    fill: false,
  };
}

const chartData = computed(() => {
  if (monthly.value) {
    const labels = monthly.value.map((d) => d.period);
    return {
      labels,
      datasets: [
        mkSeries("Crashes", monthly.value.map((d) => d.crashes), THEME.crashes, THEME.crashesFill),
        mkSeries("Total injuries", monthly.value.map((d) => d.total_injuries), THEME.injuries, THEME.injuriesFill),
        mkSeries("Serious injuries", monthly.value.map((d) => d.serious_injuries), THEME.serious, THEME.seriousFill),
      ],
    };
  }
  if (yearly.value) {
    const labels = yearly.value.map((d) => String(d.year));
    return {
      labels,
      datasets: [
        mkSeries("Crashes", yearly.value.map((d) => d.crashes), THEME.crashes, THEME.crashesFill),
        mkSeries("Total injuries", yearly.value.map((d) => d.total_injuries), THEME.injuries, THEME.injuriesFill),
        mkSeries("Serious injuries", yearly.value.map((d) => d.serious_injuries), THEME.serious, THEME.seriousFill),
      ],
    };
  }
  return null;
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: "top" as const,
      labels: { color: THEME.text, usePointStyle: true, pointStyle: "line" as const },
    },
    title: { display: false },
    tooltip: { mode: "index" as const, intersect: false },
    // our custom background
    chartAreaBg: { color: "rgba(246,179,0,0.10)" },
  },
  interaction: { mode: "index" as const, intersect: false },
  scales: {
    x: {
      ticks: { color: THEME.text, maxRotation: 0, autoSkip: true },
      grid: { color: THEME.grid },
    },
    y: {
      beginAtZero: true,
      ticks: { color: THEME.text },
      grid: { color: THEME.grid },
    },
  },
};
</script>

<style scoped>
.trend-card {
  margin: 22px auto 40px;
  max-width: 1400px;
  padding: 16px 16px;
  background: transparent;
  border: 1px solid rgba(17, 17, 17, 0.1);
  border-radius: 12px;
}
.head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}
h3 {
  margin: 0;
  font-size: 28px;
  color: #111111;
}
.controls {
  display: flex;
  gap: 8px;
  align-items: center;
}
.select {
  padding: 8px 10px;
  border: 1px solid rgba(17,17,17,0.25);
  border-radius: 10px;
  background: #fff7d6;
  color: #111111;
}
.arrow {
  color: #111111;
  opacity: 0.9;
  padding: 0 4px;
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

.chart-wrap {
  height: 380px;
  margin-top: 10px;
  border-radius: 10px;
  overflow: hidden;
}
.placeholder {
  color: #333;
  text-align: center;
  padding: 24px;
  background: rgba(246,179,0,0.10);
  border-radius: 10px;
}
.error {
  color: #b91c1c;
  margin-top: 10px;
  font-weight: 600;
}

.title {
  font-size: 1.6rem;
  font-weight: 800;
  margin: 0 0 1rem;
}
/* hazard stripes */
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
