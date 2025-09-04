<template>
  <div class="homepage">
    <HeroSection />
    <accident-stats/>
    <TrendCharts/>
    <ForecastView/>
    <FooterSection/>
  </div>
</template>

<script setup>
import HeroSection from '@/components/StatsTrendsPage/HeroSection.vue'
import AccidentStats from "@/components/StatsTrendsPage/AccidentStats.vue";
import TrendCharts from "@/components/StatsTrendsPage/TrendCharts.vue";
import FooterSection from "@/components/FooterSection.vue";
import ForecastView from "@/components/StatsTrendsPage/ForecastView.vue";

</script>

<style scoped>

</style>
