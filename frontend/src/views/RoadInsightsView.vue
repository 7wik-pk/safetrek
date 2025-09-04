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
import HeroSection from '@/components/SafeRoadInsightPage/HeroSection.vue'
import AccidentStats from "@/components/SafeRoadInsightPage/AccidentStats.vue";
import TrendCharts from "@/components/SafeRoadInsightPage/TrendCharts.vue";
import FooterSection from "@/components/FooterSection.vue";
import ForecastView from "@/components/SafeRoadInsightPage/ForecastView.vue";

</script>

<style scoped>

</style>
