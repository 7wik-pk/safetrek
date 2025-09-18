<template>
  <section class="mission">
    <div class="mission__container">
      <!-- Top row -->
      <div class="mission__intro">
        <div class="intro-left">
          <h4>WHO WE ARE</h4>
          <h2>SafeTrek<br />Road data provider</h2>
        </div>
        <div class="intro-right">
          <h3>Identify Risky Areas & Roads with SafeTrek</h3>
          <p>
            Road crashes cause 40,000+ serious injuries in Australia every year. The challenge isn’t lack of data – it’s that valuable crash information is fragmented, hard to access, and rarely presented in a way that helps policymakers act. SafeTrek is an interactive web platform that transforms raw crash records into actionable insights.
            By combining crash data with demographics, vehicle type, weather, and road conditions.
          </p>
        </div>
      </div>

      <!-- Bottom row (cards) -->
      <div class="mission__services">
        <div class="service-card">
          <img src="/img/features/g4.jpg" alt="Electrical Engineering" />
          <div class="card-content">
            <h4>Traffic Safety</h4>
            <router-link
              :to="{ path: '/blog', hash: '#traffic-safety' }"
              class="learn-more"
            >
              LEARN MORE →
            </router-link>
          </div>
        </div>

        <div class="service-card">
          <img src="/img/features/02.jpg" alt="Construction Service" />
          <div class="card-content">
            <h4>Fleet Safety</h4>
            <router-link :to="{ path: '/blog', hash: '#fleet-safety' }" class="learn-more">
              LEARN MORE →
            </router-link>
          </div>
        </div>

        <div class="service-card">
          <img src="/img/features/b1.jpg" alt="Chemical Services" />
          <div class="card-content">
            <h4>Risk</h4>
            <router-link :to="{ path: '/blog', hash: '#risk-pro' }" class="learn-more">
              LEARN MORE →
            </router-link>
          </div>
        </div>

        <div class="service-card">
          <img src="/img/features/p4.jpg" alt="Chemical Services" />
          <div class="card-content">
            <h4>Insurance</h4>
            <router-link :to="{ path: '/blog', hash: '#senior-analyst' }" class="learn-more">
              LEARN MORE →
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
// No JS needed — static section
</script>

<style scoped>
.mission {
  background: #fff;
  padding: 80px 20px;
  color: #111;
}

.mission__container {
  max-width: 1200px;
  margin: 0 auto;
}

/* ---------- Top row ---------- */
.mission__intro {
  display: flex;
  gap: 40px;
  margin-bottom: 60px;
  align-items: stretch;
}

.intro-left {
  flex: 1;
  background: #ffc21a;
  padding: 40px;
  color: #000;
  border-radius: 8px;
}

.intro-left h4 {
  font-size: clamp(0.85rem, 0.8rem + 0.2vw, 0.95rem);
  font-weight: 600;
  margin-bottom: 10px;
}

.intro-left h2 {
  font-size: clamp(1.4rem, 1.1rem + 1.2vw, 1.9rem);
  font-weight: 700;
  line-height: 1.3;
}

.intro-right {
  flex: 2;
}

.intro-right h3 {
  font-size: clamp(1.1rem, 1rem + 0.6vw, 1.4rem);
  margin-bottom: 12px;
}

.intro-right p {
  color: #555;
  line-height: 1.7;
  margin-bottom: 16px;
}

.learn-more {
  color: #000;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.2s;
}
.learn-more:hover {
  color: #f15a24;
}

/* ---------- Bottom row (cards) ---------- */
.mission__services {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 24px;
}

.service-card {
  position: relative;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background: #fff;
}

.service-card img {
  width: 100%;
  height: 250px;
  object-fit: cover;
  aspect-ratio: 16 / 9;
}

.card-content {
  position: absolute;
  bottom: 16px;
  left: 16px;
  right: 16px;
  background: #fff;
  padding: 16px;
  border-radius: 6px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

/* Hover only on devices that support hover */
@media (hover: hover) and (pointer: fine) {
  .service-card:hover .card-content {
    transform: translateY(-10px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
  }
}

/* ---------- Tablet (≤ 1024px) ---------- */
@media (max-width: 1024px) {
  .mission {
    padding: 64px 20px;
  }

  .mission__intro {
    gap: 28px;
    margin-bottom: 44px;
  }

  .mission__services {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 20px;
  }

  .service-card img {
    height: 220px;
  }
}

/* ---------- Phablet / large mobile (≤ 768px) ---------- */
@media (max-width: 768px) {
  .mission {
    padding: 56px 16px;
  }

  .mission__intro {
    flex-direction: column;
  }

  .intro-left {
    padding: 28px;
  }

  .mission__services {
    grid-template-columns: 1fr;
    gap: 18px;
  }

  .service-card img {
    height: 210px;
  }
}

/* ---------- Small mobile (≤ 480px) ---------- */
@media (max-width: 480px) {
  .mission {
    padding: 44px 14px;
  }

  .intro-left {
    padding: 22px;
  }

  .card-content {
    bottom: 12px;
    left: 12px;
    right: 12px;
    padding: 12px;
  }

  .service-card img {
    height: 190px;
  }
}

/* Reduce motion friendly */
@media (prefers-reduced-motion: reduce) {
  .card-content {
    transition: none;
  }
}
</style>
