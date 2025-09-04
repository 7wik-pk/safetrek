<script setup>
import blog1 from '@/assets/images/Homepage/blog1.jpg'
import blog2 from '@/assets/images/Homepage/blog2.jpg'
import blog3 from '@/assets/images/Homepage/blog3.jpg'
import hazardBottom from "@/assets/images/hazard-stripes02.svg";
</script>

<template>
  <section class="blog">
    <div class="container blog__header">
      <h2>News Articles & Journals</h2>
      <!-- <RouterLink to="/articles" class="btn-outline">ALL Articles</RouterLink> -->
    </div>

    <div class="container blog__grid">
      <article class="card">
        <div class="card__media" >
          <img :src="blog1" alt="Transport accidents" />
        </div>
        <!-- <h3 class="card__kicker">Articles</h3> -->
        <a class="card__title" href="https://www.aihw.gov.au/reports/injury/transport-accidents">Australian Institute of Health and Welfare</a>
      </article>

      <article class="card">
        <div class="card__media">
          <img :src="blog2" alt="Human cost, machine insight" />
        </div>
        <!-- <h3 class="card__kicker">Articles</h3> -->
        <a class="card__title" href="https://www.sciencedirect.com/science/article/pii/S2213624X2500077X?via%3Dihub">
          A journal paper published by Dr Ali Soltani from Flinders University
        </a>
      </article>

      <article class="card">
        <div class="card__media">
          <img :src="blog3" alt="How work planners can improve road safety awareness" />
        </div>
        <!-- <h3 class="card__kicker">Articles</h3> -->
        <a class="card__title" href="https://www.theguardian.com/australia-news/2025/jan/27/australia-road-toll-2024-1300-deaths-highest-in-more-than-a-decade">
          The Guardian's recent article on rising road accidents
        </a>
      </article>
    </div>

  </section>
</template>

<style scoped>
/* section wrapper */
.blog {
  background: linear-gradient(180deg, #f6b300 0%, #c98600 100%);
  padding: 56px 20px 64px;
  color: #111;

}

/* header */
.blog__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 28px;
}
.blog__header h2 {
  font-weight: 900;
  font-size: clamp(22px, 3vw, 34px);
  margin: 0;
}
.btn-outline {
  appearance: none;
  background: #dfac29;
  color: #111;
  border: 2px solid #111;
  border-radius: 999px;
  padding: 8px 18px;
  font-weight: 800;
  cursor: pointer;
  text-decoration: none;
  box-shadow: 0 4px 10px rgba(0,0,0,.15);
}
.btn-outline:hover { background: #ff7a17; }

/* grid */
.blog__grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 34px;
  align-items: start;
}

/* cards */
.card {
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: #df9d00;
}

/* uniform media sizing */
.card__media {
  aspect-ratio: 16 / 9;
  width: 100%;
  border: 4px solid #111;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 8px 22px rgba(0,0,0,.25);
  background: #000;
}
.card__media img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* text */
.card__kicker {
  font-size: 18px;
  font-weight: 900;
  margin-left: 10px;
  margin-top: 10px;
}
.card__title {
  margin-top: 2%;
  margin-bottom: 2%;
  margin-left: 10px;
  font-size: 15px;
  line-height: 1.4;
  color: #111;

  min-height: 3.2em;
}


.stopline-bleed {
  position: relative;
  left: 50%;
  right: 50%;
  margin-left: -50vw;
  margin-right: -50vw;
  width: 100vw;           /* span the viewport */
}

/* Tape track (height = visual thickness) */
.stopline-wrap {
  margin-top:20px;

  position: relative;
  height: 90px;
  overflow: hidden;
}


/* responsive */
@media (max-width: 1200px) {
  .blog__grid { grid-template-columns: repeat(2, minmax(0,1fr)); }
}
@media (max-width: 640px) {
  .blog__grid { grid-template-columns: 1fr; }
  .blog__header { flex-direction: column; align-items: flex-start; }
}
</style>
