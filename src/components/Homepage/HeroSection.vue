<template>
  <section class="hero">
    <!-- hazard stripes -->
    <div class="hazard hazard--top">
      <img src="../../assets/images/hazard-stripes.svg" alt="" />
    </div>

    <!-- background + overlay -->
    <div class="hero__bg">
      <img src="@/assets/images/Homepage/top-image.jpg" alt="Background" />
      <div class="overlay"></div>
    </div>

    <!-- content -->
    <div class="hero__content">
      <img class="sign" src="@/assets/images/roadwork.png" alt="Road Work Sign" />
      <div class="text">
        <h1>Identify for safer road</h1>
        <p>
          Stay prepared, stay safe. Our goal is to help every road user make
          informed decisions by combining planning, awareness, and real-time
          insights. Together, we can reduce risks and create safer journeys for everyone.
        </p>
        <button class="btn-primary">Learn more</button>
      </div>
    </div>

    <div class="hazard hazard--bottom">
      <img src="../../assets/images/hazard-stripes.svg" alt="" />
    </div>
  </section>

</template>

<style scoped>
.hero {
  position: relative;
  overflow: hidden;
  text-align: left;
}

/* background */
.hero__bg {
  position: absolute;
  inset: 0;
}
.hero__bg img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.hero__bg .overlay {
  position: absolute;
  inset: 0;
  background: rgba(246, 179, 0, 0.65); /* softer yellow */
}

/* hazard stripes */
.hazard {
  position: relative;
  width: 100%;
  z-index: 2;
}
.hazard img {
  width: 100%;
  height: 30px;
  object-fit: cover;
}
.hazard--top {
  margin-bottom: 120px; /* tuck neatly */
}
.hazard--bottom {
  margin-top: -10px;
  transform: rotate(180deg);
}

/* content */
.hero__content {
  position: relative;
  z-index: 3;
  display: flex;
  align-items: center;
  gap: 2rem;
  max-width: 1100px;
  margin: 0 auto;
  padding: 60px 20px;
  color: #111;
}
.sign {
  width: 160px;
  flex-shrink: 0;
}
.text h1 {
  font-size: 2.2rem;
  font-weight: 900;
  margin-bottom: 12px;
}
.text p {
  font-size: 1rem;
  line-height: 1.5;
  margin-bottom: 20px;
  font-weight: 600;
}

/* button */
.btn-primary {
  background: #111;
  color: #f6b300;
  padding: 10px 24px;
  border: none;
  border-radius: 20px;
  font-weight: 700;
  cursor: pointer;
}
.btn-primary:hover {
  background: #222;
}

/* responsive */
@media (max-width: 768px) {
  .hero__content {
    flex-direction: column;
    text-align: center;
  }
  .sign {
    width: 120px;
  }
}
</style>
