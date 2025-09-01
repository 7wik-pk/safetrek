<script setup>
import whySafetyImage from '@/assets/images/Homepage/why-safety.jpg'
import noteTape       from '@/assets/images/Homepage/note_tape.svg'
import hazardTop      from '@/assets/images/hazard-stripes.svg'
import hazardBottom   from '@/assets/images/hazard-stripes02.svg'
</script>

<template>
  <section class="why-safety">

    <div class="why-safety__content container">
      <!-- left sticky note style -->
      <div class="why-safety__note">
        <img :src="noteTape" alt="" class="note-tape" />
        <h2>Why Safety First?</h2>
        <p>
          Safety must be the starting point for all planning decisions.
          Reactive approaches to crashes often waste resources and fail to
          protect vulnerable communities. By embedding safety at the core of
          infrastructure, traffic management, and policy planning, we can
          shift from responding to accidents toward preventing them.
        </p>
        <button class="btn-primary">Learn more</button>
      </div>

      <!-- right image -->
      <div class="why-safety__image">
        <img :src="whySafetyImage" alt="Why Safety" />
      </div>
    </div>

    <div class="footer-divider">
      <div class="footer-divider__inner"></div>
    </div>
  </section>
</template>

<style scoped>
.why-safety {
  position: relative;
  background: linear-gradient(180deg, #e5a100 0%, #c98600 100%);
  padding: 60px 20px;
  overflow: hidden;
}

/* hazard stripes */
.hazard {
  display: block;
  width: 110%;
  height: 90px;
  object-fit: cover;
}
.hazard--top {
  margin-bottom: 30px;
}
.hazard--bottom {
  margin-top: 40px;
}

/* layout */
.why-safety__content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  align-items: center;
  max-width: 1100px;
  margin: 0 auto;
}

/* sticky note card */
.why-safety__note {
  position: relative;
  background: #f6b300;
  border-radius: 14px;
  padding: 30px;
  border: 3px solid #111;
  box-shadow: 6px 6px 0 rgba(0,0,0,.3);
}
.note-tape {
  position: absolute;
  top: -30px;
  left: -20px;
  width: 100px;
  transform: rotate(-6deg);
}
.why-safety__note h2 {
  font-size: 1.8rem;
  font-weight: 900;
  margin-bottom: 16px;
  color: #111;
}
.why-safety__note p {
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 20px;
  color: #222;
}

/* right image */
.why-safety__image img {
  width: 100%;
  display: block;
  border: 6px solid #111; /* stroke */
  border-radius: 6px;
  box-shadow: 0 12px 30px rgba(0,0,0,.35);
}

/* button */
.btn-primary {
  background: #111;
  color: #f6b300;
  padding: 10px 22px;
  border-radius: 24px;
  font-weight: 700;
  border: none;
  cursor: pointer;
}
.btn-primary:hover {
  background: #222;
}


/* ---------- Full-bleed hazard divider ---------- */
.footer-divider {
  position: relative;
  left: 50%;
  right: 50%;
  margin-top: 4vw;
  margin-left: -50vw;
  margin-right: -50vw;
  width: 100vw;
  background: linear-gradient(180deg, #d19600 0%, #c18500 100%);
}
.footer-divider__inner {
  /* visible height of the divider */
  height: 64px;
  margin-top: 20px;
  background-image: url('@/assets/images/hazard-stripes02.svg');
  background-repeat: repeat-x;
  background-size: auto 100%;
  background-position: center;
  filter: drop-shadow(0 6px 12px rgba(0,0,0,.35));
}
/* responsive */
@media (max-width: 860px) {
  .why-safety__content {
    grid-template-columns: 1fr;
    text-align: center;
  }
  .why-safety__note {
    margin-bottom: 30px;
  }
  .note-tape {
    left: 50%;
    transform: translateX(-50%) rotate(-6deg);
  }
}
</style>
