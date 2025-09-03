<template>
  <!-- full-bleed hazard bar sitting on top of the footer -->
  <div class="footer-divider">
    <div class="footer-divider__inner"></div>
  </div>

  <footer class="footer">
    <div class="container footer__grid">
      <!-- Brand / short blurb -->
      <div class="footer__brand">
        <h3 class="footer__logo">SafeTrek</h3>
        <p class="footer__blurb">
          Helping every road user make informed decisions with planning, awareness,
          and real-time insights — for safer journeys.
        </p>

        <div class="footer__social">
          <a href="#" aria-label="Twitter" class="social">
            <svg viewBox="0 0 24 24" class="icon"><path fill="currentColor"
                                                        d="M22 5.8c-.7.3-1.4.5-2.1.6.8-.5 1.3-1.2 1.6-2.1-.7.5-1.6.8-2.5 1A3.7 3.7 0 0 0 12 7.8c0 .3 0 .6.1.9-3-.1-5.7-1.6-7.5-4-.3.5-.5 1.1-.5 1.8 0 1.2.6 2.3 1.6 3A3.7 3.7 0 0 1 3 9.1v.1c0 1.7 1.2 3.2 2.9 3.6-.3.1-.6.1-.9.1-.2 0-.4 0-.6-.1.4 1.4 1.8 2.5 3.4 2.6A7.4 7.4 0 0 1 2 17.6c-.3 0-.6 0-.9-.1A10.5 10.5 0 0 0 6.7 19C14.4 19 19 12.9 19 7.8v-.5c.7-.5 1.3-1.1 1.8-1.8z"/>
            </svg>
          </a>
          <a href="#" aria-label="LinkedIn" class="social">
            <svg viewBox="0 0 24 24" class="icon"><path fill="currentColor"
                                                        d="M6.9 21H3.5V9h3.4v12zM5.2 7.6c-1.1 0-2-.9-2-2s.9-2 2-2a2 2 0 110 4zM21 21h-3.4v-6.3c0-1.5-.5-2.6-1.8-2.6-1 0-1.6.7-1.9 1.3-.1.2-.1.5-.1.7V21h-3.4s.1-10.4 0-12.1H12v1.7c.4-.6 1.2-1.5 3-1.5 2.2 0 3.9 1.4 3.9 4.5V21z"/>
            </svg>
          </a>
          <a href="#" aria-label="GitHub" class="social">
            <svg viewBox="0 0 24 24" class="icon"><path fill="currentColor"
                                                        d="M12 2a10 10 0 00-3.2 19.5c.5.1.7-.2.7-.5v-1.9c-2.8.6-3.4-1.3-3.4-1.3-.5-1.1-1.2-1.4-1.2-1.4-1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 1.2 1 .1.8-.7 1.6-1 .7-.4 1.6-.4 2.4 0 .2-.7.6-1 .9-1.2-2.3-.3-4.6-1.2-4.6-5.1 0-1.1.4-2 1.1-2.8-.1-.3-.5-1.4.1-2.9 0 0 .9-.3 2.9 1.1.8-.2 1.7-.3 2.6-.3s1.8.1 2.6.3c2-1.4 2.9-1.1 2.9-1.1.6 1.5.3 2.6.1 2.9.7.8 1.1 1.7 1.1 2.8 0 3.9-2.3 4.8-4.6 5.1.6.5 1 .1 1 2v3c0 .3.2.6.7.5A10 10 0 0012 2z"/>
            </svg>
          </a>
        </div>
      </div>

      <!-- Quick links -->
      <nav class="footer__col">
        <h4>Explore</h4>
        <ul>
          <li><a href="#">Safe road insight</a></li>
          <li><a href="#">Crash Risk Explorer</a></li>
          <li><a href="#">Blackspot &amp; Corridor</a></li>
          <li><a href="#">Equity &amp; Vulnerability</a></li>
        </ul>
      </nav>

      <!-- Resources -->
      <nav class="footer__col">
        <h4>Resources</h4>
        <ul>
          <li><a href="#">Docs</a></li>
          <li><a href="#">Blog</a></li>
          <li><a href="#">Changelog</a></li>
          <li><a href="#">FAQ</a></li>
        </ul>
      </nav>

      <!-- Contact -->
      <div class="footer__col">
        <h4>Contact</h4>
        <ul class="footer__contact">
          <li><a href="mailto:hello@safetrek.dev">hello@safetrek.dev</a></li>
          <li><a href="tel:+0000000000">+00 0000 0000</a></li>
          <li>Melbourne, AU</li>
        </ul>
      </div>
    </div>

    <div class="footer__copy">
      <div class="container copy__inner">
        <span>© {{ new Date().getFullYear() }} SafeTrek. All rights reserved.</span>
        <div class="copy__links">
          <a href="#">Privacy</a>
          <a href="#">Terms</a>
          <a href="#">Cookies</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
// purely presentational; no script needed
</script>

<style scoped>
:root {
  --gold-1: #e0a70a;
  --gold-2: #c48800;
  --dark: #141414;
  --dark-2: #1b1c20;
  --text: #f8f6ee;
  --muted: #cfc8b0;
}

/* ---------- Full-bleed hazard divider ---------- */
.footer-divider {
  position: relative;
  left: 50%;
  right: 50%;
  margin-left: -50vw;
  margin-right: -50vw;
  width: 100vw;
  background: linear-gradient(180deg, #d19600 0%, #c18500 100%);
}
.footer-divider__inner {
  /* visible height of the divider */
  height: 64px;
  background-image: url('@/assets/images/hazard-stripes02.svg');
  background-repeat: repeat-x;
  background-size: auto 100%;
  background-position: center;
  filter: drop-shadow(0 6px 12px rgba(0,0,0,.35));
}

/* ---------- Footer ---------- */
.footer {
  background: linear-gradient(180deg, #c18500 0%, #b27700 100%);
  color: var(--text);
  padding-top: 32px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

/* main grid */
.footer__grid {
  display: grid;
  grid-template-columns: 1.2fr repeat(3, 1fr);
  gap: 32px 40px;
  padding: 32px 0 20px;
}

/* brand / socials */
.footer__logo {
  font-size: 28px;
  font-weight: 800;
  margin: 0 0 6px;
}
.footer__blurb {
  color: var(--muted);
  margin: 0 0 16px;
  line-height: 1.5;
}
.footer__social {
  display: flex;
  gap: 12px;
}
.social {
  width: 36px;
  height: 36px;
  border-radius: 999px;
  background: #0f0f0f;
  display: grid;
  place-items: center;
  transition: transform .15s ease, background .2s ease;
}
.social:hover { transform: translateY(-2px); background: #000; }
.icon { width: 18px; height: 18px; color: #ffd770; }

/* columns */
.footer__col h4 {
  font-size: 16px;
  margin: 0 0 12px;
  letter-spacing: .3px;
}
.footer__col ul { list-style: none; margin: 0; padding: 0; }
.footer__col li + li { margin-top: 8px; }
.footer__col a {
  color: var(--text);
  text-decoration: none;
  opacity: .9;
}
.footer__col a:hover { opacity: 1; text-decoration: underline; }
.footer__contact li { color: var(--text); opacity: .9; }

/* bottom copy bar */
.footer__copy {
  margin-top: 18px;
  border-top: 1px solid rgba(0,0,0,.25);
  background: rgba(0,0,0,.1);
}
.copy__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 0;
  font-size: 14px;
}
.copy__links {
  display: flex;
  gap: 16px;
}
.copy__links a {
  color: var(--text);
  opacity: .85;
  text-decoration: none;
}
.copy__links a:hover { opacity: 1; text-decoration: underline; }

/* ---------- Responsive ---------- */
@media (max-width: 960px) {
  .footer__grid { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 640px) {
  .footer__grid { grid-template-columns: 1fr; }
  .copy__inner { flex-direction: column; align-items: flex-start; }
}
</style>
