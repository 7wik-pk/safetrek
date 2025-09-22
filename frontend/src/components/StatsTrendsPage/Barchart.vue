<template>
  <section class="factor-card">
    <header class="head">
      <h2 class="title">Factor Insights</h2>

      <div class="controls">
        <select v-model="selectedFactor" class="select">
          <option v-for="f in factors" :key="f.value" :value="f.value">{{ f.label }}</option>
        </select>

        <button class="btn" @click="load" :disabled="loading">
          {{ loading ? 'Loading...' : 'Refresh' }}
        </button>
      </div>
    </header>

    <div class="chart-wrap">
      <Bar v-if="chartData" :data="chartData" :options="chartOptions" />
      <p v-else class="placeholder">Pick a factor, then click Refresh.</p>
    </div>

    <footer v-if="error" class="error">{{ error }}</footer>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import api from '@/lib/api'

// Chart.js
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, CategoryScale, LinearScale, BarElement)

type FactorItem = {
  category: string
  severity: string
  count: number
}

const factors = [
  { label: 'Time of Day', value: 'time_bucket' },
  { label: 'Light Condition', value: 'light_condition' },
  { label: 'Road Geometry', value: 'road_geometry' },
  { label: 'Speed Zone', value: 'speed_zone' },
  { label: 'Atmospheric Condition', value: 'atmospheric_condition' },
  { label: 'Sex', value: 'sex' },
  { label: 'Age Group', value: 'age_group' },
  { label: 'Helmet/Belt Worn', value: 'helmet_belt_worn' }
]

const selectedFactor = ref('time_bucket')
const loading = ref(false)
const error = ref('')
const chartData = ref<any | null>(null)

async function load() {
  error.value = ''
  loading.value = true
  try {
    const { data } = await api.get<FactorItem[]>('/factor_counts', {
      params: { factor: selectedFactor.value }
    })

    const categories = [...new Set(data.map((d) => d.category))]
    const injuryCounts = categories.map(
      (cat) => data.find((d) => d.category === cat && d.severity === 'Injury')?.count || 0
    )
    const seriousCounts = categories.map(
      (cat) => data.find((d) => d.category === cat && d.severity === 'SeriousInjury')?.count || 0
    )

    chartData.value = {
      labels: categories,
      datasets: [
        {
          label: 'Injury',
          data: injuryCounts,
          backgroundColor: '#4caf50'
        },
        {
          label: 'Serious Injury',
          data: seriousCounts,
          backgroundColor: '#f44336'
        }
      ]
    }
  } catch (e: any) {
    error.value = e?.response?.data?.detail || e.message || 'Request failed'
    chartData.value = null
  } finally {
    loading.value = false
  }
}

load()

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top' as const,
      labels: { color: '#111111', usePointStyle: true }
    },
    title: {
      display: false
    }
  },
  scales: {
    x: {
      ticks: { color: '#111111', maxRotation: 45, minRotation: 0 },
      grid: { color: 'rgba(17,17,17,0.10)' }
    },
    y: {
      beginAtZero: true,
      ticks: { color: '#111111' },
      grid: { color: 'rgba(17,17,17,0.10)' }
    }
  }
}
</script>

<style scoped>
.factor-card {
  margin: 22px auto 40px;
  max-width: 1200px;
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
.title {
  font-size: 1.4rem;
  font-weight: 800;
  margin: 0;
}
.controls {
  display: flex;
  gap: 8px;
  align-items: center;
}
.select {
  padding: 8px 10px;
  border: 1px solid rgba(17, 17, 17, 0.25);
  border-radius: 10px;
  background: #fff7d6;
  color: #111111;
}
.btn {
  padding: 10px 16px;
  border: none;
  border-radius: 10px;
  background-color: #111111;
  color: #f6b300;
  font-weight: 700;
  letter-spacing: 0.2px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn:hover {
  background-color: #1a1a1a;
}
.btn:active {
  transform: scale(0.98);
}
.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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
  background: rgba(246, 179, 0, 0.1);
  border-radius: 10px;
}
.error {
  color: #b91c1c;
  margin-top: 10px;
  font-weight: 600;
}
</style>
