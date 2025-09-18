<script setup>
import blog1 from '@/assets/images/Homepage/blog1.jpg'
import blog2 from '@/assets/images/Homepage/blog2.jpg'
import blog3 from '@/assets/images/Homepage/blog3.jpg'
</script>

<template>
  <section class="blog">
    <div class="container blog__header">
      <h2>News Articles & Journals</h2>
    </div>

    <div class="container blog__grid">
      <!-- Article 1 -->
      <article class="card">
        <div class="card__media">
          <img :src="blog1" alt="Transport accidents" />
        </div>
        <div class="card__body">
          <h3 class="card__title">Australian Institute of Health and Welfare</h3>
          <a
            class="card__link"
            href="https://www.aihw.gov.au/reports/injury/transport-accidents"
            target="_blank"
          >
            Read More →
          </a>
          <div class="card__meta">
            <span>12 Feb 2025</span>
          </div>
        </div>
      </article>

      <!-- Article 2 -->
      <article class="card">
        <div class="card__media">
          <img :src="blog2" alt="Human cost, machine insight" />
        </div>
        <div class="card__body">
          <h3 class="card__title">
            A journal paper published by Dr Ali Soltani from Flinders University
          </h3>
          <a
            class="card__link"
            href="https://www.sciencedirect.com/science/article/pii/S2213624X2500077X?via%3Dihub"
            target="_blank"
          >
            Read More →
          </a>
          <div class="card__meta">
            <span>10 Feb 2025</span>
          </div>
        </div>
      </article>

      <!-- Article 3 -->
      <article class="card">
        <div class="card__media">
          <img :src="blog3" alt="How work planners can improve road safety awareness" />
        </div>
        <div class="card__body">
          <h3 class="card__title">The Guardian's recent article on rising road accidents</h3>
          <a
            class="card__link"
            href="https://www.theguardian.com/australia-news/2025/jan/27/australia-road-toll-2024-1300-deaths-highest-in-more-than-a-decade"
            target="_blank"
          >
            Read More →
          </a>
          <div class="card__meta">
            <span>27 Jan 2025</span>
          </div>
        </div>
      </article>
    </div>
  </section>
</template>

<style scoped>
.blog {
  background: #fff;
  padding: 80px 20px;
  color: #111;
}

/* header */
.blog__header {
  display: flex;
  justify-content: center;
  margin-bottom: 40px;
}
.blog__header h2 {
  font-weight: 800;
  font-size: clamp(26px, 3vw, 40px);
  margin: 0;
}

/* grid */
.blog__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

/* card */
.card {
  background: #fff;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 6px 22px rgba(0, 0, 0, 0.1);
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
  display: flex;
  flex-direction: column;
}
.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 14px 32px rgba(0, 0, 0, 0.15);
}

.card__media {
  width: 100%;
  height: 220px;
  overflow: hidden;
}
.card__media img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card__body {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.card__title {
  font-size: 1.05rem;
  font-weight: 700;
  color: #222;
  line-height: 1.4;
  margin: 0;
}

.card__link {
  font-size: 0.95rem;
  font-weight: 600;
  color: #f15a24;
  text-decoration: none;
}
.card__link:hover {
  text-decoration: underline;
}

.card__meta {
  font-size: 0.85rem;
  color: #666;
  margin-top: auto;
}

/* responsive */
@media (max-width: 1024px) {
  .blog__grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 640px) {
  .blog__grid {
    grid-template-columns: 1fr;
  }
}
</style>
