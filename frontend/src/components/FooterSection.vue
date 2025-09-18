<template>
  <!-- Top strip -->
  <div class="footer-top">
    <div class="container footer-top__inner">
      <div class="footer-top__social">
        <a href="https://github.com/7wik-pk/safetrek" aria-label="GitHub" class="social">
          <svg viewBox="0 0 24 24" class="icon">
            <path
              fill="currentColor"
              d="M12 2a10 10 0 00-3.2 19.5c.5.1.7-.2.7-.5v-1.9c-2.8.6-3.4-1.3-3.4-1.3-.5-1.1-1.2-1.4-1.2-1.4-1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 1.2 1 .1.8-.7 1.6-1 .7-.4 1.6-.4 2.4 0 .2-.7.6-1 .9-1.2-2.3-.3-4.6-1.2-4.6-5.1 0-1.1.4-2 1.1-2.8-.1-.3-.5-1.4.1-2.9 0 0 .9-.3 2.9 1.1.8-.2 1.7-.3 2.6-.3s1.8.1 2.6.3c2-1.4 2.9-1.1 2.9-1.1.6 1.5.3 2.6.1 2.9.7.8 1.1 1.7 1.1 2.8 0 3.9-2.3 4.8-4.6 5.1.6.5 1 .1 1 2v3c0 .3.2.6.7.5A10 10 0 0012 2z"
            />
          </svg>
        </a>
      </div>

      <div class="brand-plate">
        <div class="brand-plate__logo">🛡️</div>
        <div class="brand-plate__text">
          <div class="brand-plate__name">SafeTrek</div>
          <div class="brand-plate__sub">Construction &amp; Industry</div>
        </div>
      </div>
    </div>
  </div>

  <!-- Main dotted footer -->
  <footer class="footer">
    <div class="container footer__grid">
      <!-- Column 2: Explore -->
      <nav class="footer__col">
        <h4 class="footer__title">Quick Links</h4>
        <ul>
          <li><router-link to="/" class="link">Home</router-link></li>
          <li>
            <router-link to="/stats-trends" class="link">Statistics &amp; Trends</router-link>
          </li>
          <li><a class="a-disabled">Crash Risk Explorer</a></li>
          <li><a class="a-disabled">Blackspot &amp; Corridor</a></li>
          <li><a class="a-disabled">Equity &amp; Vulnerability</a></li>
        </ul>
      </nav>
    </div>

    <div class="footer__copy">
      <div class="container copy__inner">
        <span>Copyright © 2025 SafeTrek. All rights reserved.</span>
        <div class="copy__links">
          <a href="#">Privacy</a>
          <a href="#">Terms</a>
          <a href="#">Cookies</a>
        </div>
      </div>
    </div>
  </footer>
</template>
<style scoped>
:root {
  --bg: #111; /* main dark background */
  --bg-dot: #0d0d0d; /* for dotted texture contrast */
  --dot: rgba(255, 255, 255, 0.04);
  --text: #e9e9e9;
  --muted: #a9a9a9;
  --gold: #f6b300;
  --tile: 22px; /* size for dotted pattern tile */
}

/* ------------ Top Bar ------------ */
.footer-top {
  background: #1a1a1a;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}
.footer-top__inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 12px 20px;
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 16px;
  align-items: center;
}
.footer-top__social {
  display: flex;
  gap: 10px;
}
.social {
  width: 36px;
  height: 36px;
  border-radius: 6px;
  background: #222;
  display: grid;
  place-items: center;
  transition:
    transform 0.2s ease,
    background 0.25s ease;
}
.social:hover {
  transform: translateY(-2px);
  background: var(--gold);
}
.icon {
  width: 18px;
  height: 18px;
  color: #fff;
}

.footer__top-links {
  display: flex;
  gap: 18px;
}
.footer__top-links .link {
  color: #cfcfcf;
  text-decoration: none;
  font-size: 14px;
}
.footer__top-links .link:hover {
  color: #fff;
}

.brand-plate {
  background: var(--gold);
  padding: 10px 16px;
  border-radius: 6px;
  display: flex;
  gap: 10px;
  align-items: center;
}
.brand-plate__logo {
  font-size: 18px;
}
.brand-plate__name {
  font-weight: 900;
}
.brand-plate__sub {
  font-size: 12px;
  opacity: 0.85;
}

/* ------------ Main Footer ------------ */
.footer {
  color: var(--text);
  background:
    radial-gradient(circle at 1px 1px, var(--dot) 1px, transparent 1px) /* dots */,
    var(--bg);
  background-size:
    var(--tile) var(--tile),
    auto;
}
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.footer__grid {
  display: grid;
  grid-template-columns: 1.2fr 1fr 1fr 1fr;
  gap: 40px;
  padding: 48px 0 32px;
}

/* Headings */
.footer__title {
  margin: 0 0 14px;
  font-size: 20px;
  font-weight: 800;
  letter-spacing: 0.2px;
}

/* Brand blurb & CTA */
.footer__blurb {
  color: var(--muted);
  line-height: 1.7;
  margin: 0 0 16px;
}
.footer__cta {
  display: inline-block;
  color: var(--gold);
  font-weight: 800;
  text-decoration: none;
  position: relative;
}
.footer__cta::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: -2px;
  height: 2px;
  background: var(--gold);
}

/* Column lists */
.footer__col ul {
  list-style: none;
  margin: 0;
  padding: 0;
}
.footer__col li + li {
  margin-top: 8px;
}
.footer__col a {
  color: var(--muted);
  text-decoration: none;
  transition: color 0.2s ease;
}
.footer__col a:hover {
  color: #fff;
  text-decoration: underline;
}

/* Disabled stub links */
.a-disabled {
  color: #666;
  pointer-events: none;
}

/* News list (simple, matches look) */
.news {
  display: grid;
  gap: 14px;
}
.news__item {
  display: grid;
  grid-template-columns: 64px 1fr;
  gap: 12px;
  align-items: center;
}
.news__media {
  width: 64px;
  height: 48px;
  border-radius: 4px;
  background: #2b2b2b;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.06);
}
.news__title {
  color: #ddd;
  text-decoration: none;
  font-weight: 600;
}
.news__title:hover {
  color: #fff;
  text-decoration: underline;
}
.news__meta {
  display: block;
  color: #8e8e8e;
  font-size: 12px;
  margin-top: 4px;
}

/* Contact */
.footer__contact li {
  color: var(--muted);
}

/* Bottom copy bar */
.footer__copy {
  background: #121212;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}
.copy__inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 14px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  color: #cfcfcf;
  font-size: 14px;
}
.copy__links {
  display: flex;
  gap: 16px;
}
.copy__links a {
  color: #cfcfcf;
  text-decoration: none;
}
.copy__links a:hover {
  color: #fff;
  text-decoration: underline;
}

/* ------------ Responsive ------------ */
@media (max-width: 1024px) {
  .footer__grid {
    grid-template-columns: 1fr 1fr;
    gap: 28px;
  }
}
@media (max-width: 640px) {
  .footer-top__inner {
    grid-template-columns: 1fr;
    justify-items: start;
  }
  .brand-plate {
    justify-self: start;
  }
  .footer__grid {
    grid-template-columns: 1fr;
  }
  .copy__inner {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
