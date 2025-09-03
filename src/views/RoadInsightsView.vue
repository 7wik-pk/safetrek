<template>
  <div class="homepage">
    <HeroSection />
    <accident-stats/>
    <TrendCharts/>
    <FooterSection/>
  </div>
</template>

<script setup>
import HeroSection from '@/components/SafeRoadInsightPage/HeroSection.vue'
import AccidentStats from "@/components/SafeRoadInsightPage/AccidentStats.vue";
import TrendCharts from "@/components/SafeRoadInsightPage/TrendCharts.vue";
import FooterSection from "@/components/FooterSection.vue";

</script>

<style scoped>

</style>
