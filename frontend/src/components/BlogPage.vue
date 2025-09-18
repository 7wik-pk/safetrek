<script setup>
// centralize route targets here so you can change them once
const LINKS = {
  riskExplorer: '/risk-explorer',
  correlations: '/stats-trends', // main Statistics & Trends/correlation dashboard
  highRisk: '/stats-trends', // accident roads/high-risk roads analysis
  forecast: { name: 'StatisticsTrends', query: { tab: 'forecast' } }, // example named route+tab
}
</script>

<template>
  <div class="bg-white">
    <div class="container py-4">
      <!-- breadcrumb -->
      <nav aria-label="breadcrumb" class="mb-3">
        <ol class="breadcrumb small">
          <li class="breadcrumb-item"><a href="/">Home</a></li>
          <li class="breadcrumb-item active" aria-current="page">Disclaimer & Guidance</li>
        </ol>
      </nav>

      <div class="row g-4">
        <!-- sidebar -->
        <aside class="col-lg-3">
          <div class="card shadow-sm sticky-top toc" style="top: 90px">
            <div class="card-body">
              <h6 class="text-uppercase text-muted fw-bold mb-2">On this page</h6>
              <nav class="nav flex-column small">
                <a class="nav-link px-0 py-1" href="#disclaimer">Disclaimer</a>
                <a class="nav-link px-0 py-1" href="#traffic-safety">Traffic Safety</a>
                <a class="nav-link px-0 py-1" href="#fleet-safety">Fleet Safety</a>
                <a class="nav-link px-0 py-1" href="#risk-pro">Risk Professionals</a>
                <a class="nav-link px-0 py-1" href="#senior-analyst"
                  >Senior Risk Assessment Analyst</a
                >
                <a class="nav-link px-0 py-1" href="#police-analyst"
                  >Traffic Safety Data Analyst (Vic Police)</a
                >
              </nav>
            </div>
          </div>
        </aside>

        <!-- main -->
        <main class="col-lg-9">
          <!-- title -->
          <header class="mb-3">
            <h1 class="display-6 fw-bold mb-0">What is SafeTrek?</h1>
            <p class="text-muted mb-0">
              Guidance on making evidence-based decisions with our maps and dashboards.
            </p>
          </header>

          <!-- disclaimer -->
          <section id="disclaimer" class="mb-4">
            <div class="alert bg-yellow-50 border-0 shadow-sm py-3 px-4">
              <div class="d-flex align-items-start">
                <span class="accent-dot me-2 mt-1"></span>
                <div>
                  <h2 class="h4 fw-bold mb-1">Disclaimer</h2>
                  <p class="mb-0">
                    <strong>SafeTrek does not aim to make decisions for you.</strong>
                    The visualisations from SafeTrek are simply a means to inform your decisions
                    further.
                  </p>
                </div>
              </div>
            </div>
          </section>

          <!-- TRAFFIC SAFETY -->
          <section id="traffic-safety" class="mb-5">
            <h2 class="section-title">Traffic Safety</h2>

            <h3 class="sub-title">Risk Explorer Map — Suggestions</h3>
            <ul class="sg-list mb-3">
              <li>
                Use the layer toggle to compare <strong>before/after</strong> crash patterns when
                assessing development impact on road safety.
              </li>
              <li>
                Export high-resolution maps with clear legends and data sources for documentation.
              </li>
              <li>
                Apply council/suburb boundary overlays to compare safety performance across
                jurisdictions.
              </li>
              <li>
                Filter by time periods to show baseline versus post-development crash patterns.
              </li>
            </ul>
            <router-link :to="LINKS.riskExplorer" class="btn btn-warning fw-bold mb-3"
              >🚦 Go to Risk Explorer</router-link
            >

            <h3 class="sub-title">Multi-factor Correlation Dashboard — Suggestions</h3>
            <ul class="sg-list mb-3">
              <li>
                Focus on statistically significant correlations (<code>p &lt; 0.05</code>) when
                presenting findings to government and industry partners.
              </li>
              <li>
                Document your methodology and data limitations when interpreting correlation
                patterns.
              </li>
              <li>Save commonly used filter combinations as templates for similar case types.</li>
            </ul>

            <h3 class="sub-title">High-risk Roads Analysis — Suggestions</h3>
            <ul class="sg-list mb-2">
              <li>
                Compare proposed development locations against existing high-risk road networks.
              </li>
              <li>
                Use exposure-adjusted metrics to prioritise intervention recommendations by
                cost-effectiveness.
              </li>
              <li>
                Document data collection dates and methodology for expert-witness requirements.
              </li>
            </ul>
            <router-link :to="LINKS.correlations" class="btn btn-warning fw-bold mb-3"
              >📊 Go to Statistics &amp; Trends</router-link
            >
          </section>

          <!-- FLEET SAFETY -->
          <section id="fleet-safety" class="mb-5">
            <h2 class="section-title">Fleet Safety</h2>

            <h3 class="sub-title">Risk Explorer Map — Suggestions</h3>
            <ul class="sg-list mb-3">
              <li>
                Identify alternative routes that avoid high-risk areas during peak danger times.
              </li>
              <li>
                Use demographic overlays to identify age/experience-specific risk areas for targeted
                training programs.
              </li>
              <li>
                Compare crash patterns across seasons to adjust delivery schedules and driver
                briefings.
              </li>
              <li>
                Export regional risk summaries to support premium-reduction discussions with
                insurers.
              </li>
            </ul>
            <router-link :to="LINKS.riskExplorer" class="btn btn-warning fw-bold mb-3"
              >🚦 Go to Risk Explorer</router-link
            >

            <h3 class="sub-title">Multi-factor Correlation Dashboard — Suggestions</h3>
            <ul class="sg-list mb-3">
              <li>
                Use time-of-day correlations to set speed limits or driving restrictions for
                high-risk periods.
              </li>
              <li>
                Analyse crash patterns by vehicle type to inform future fleet purchasing decisions.
              </li>
              <li>
                Identify weather conditions that significantly increase risk for your vehicle types.
              </li>
              <li>
                Correlate crash factors with driver demographics to improve hiring and training
                criteria.
              </li>
            </ul>

            <h3 class="sub-title">High-risk Roads Analysis — Suggestions</h3>
            <ul class="sg-list mb-2">
              <li>Flag high-risk roads in your fleet management system for driver warnings.</li>
              <li>Avoid high-risk roads during their peak danger times when possible.</li>
              <li>
                Create location-specific safety briefings for regularly used high-risk corridors.
              </li>
              <li>Track improvement in accident rates after implementing route modifications.</li>
            </ul>
            <router-link :to="LINKS.correlations" class="btn btn-warning fw-bold mb-3"
              >📊 Go to Statistics &amp; Trends</router-link
            >
          </section>

          <!-- RISK PROFESSIONALS -->
          <section id="risk-pro" class="mb-5">
            <h2 class="section-title">Risk Professionals</h2>

            <h3 class="sub-title">Risk Explorer Map — Suggestions</h3>
            <ul class="sg-list mb-3">
              <li>
                <strong>Route optimisation:</strong> identify alternative routes that avoid
                high-risk areas during peak danger times.
              </li>
              <li>
                <strong>Driver training:</strong> use demographic overlays to identify
                age/experience-specific risk areas.
              </li>
              <li>
                <strong>Seasonal planning:</strong> compare crash patterns across seasons to adjust
                schedules and briefings.
              </li>
              <li>
                <strong>Insurance negotiations:</strong> export regional risk summaries to support
                premium reductions.
              </li>
            </ul>
            <router-link :to="LINKS.riskExplorer" class="btn btn-warning fw-bold mb-3"
              >🚦 Go to Risk Explorer</router-link
            >

            <h3 class="sub-title">Multi-factor Correlation Dashboard — Suggestions</h3>
            <ul class="sg-list mb-3">
              <li>
                <strong>Fleet policies:</strong> use time-of-day correlations to set speed limits or
                driving restrictions.
              </li>
              <li>
                <strong>Vehicle selection:</strong> analyse crash patterns by vehicle type to guide
                purchases.
              </li>
              <li>
                <strong>Weather protocols:</strong> identify conditions that significantly increase
                risk.
              </li>
              <li>
                <strong>Driver performance:</strong> correlate crash factors with demographics to
                refine hiring and training.
              </li>
            </ul>

            <h3 class="sub-title">High-risk Roads Analysis — Suggestions</h3>
            <ul class="sg-list mb-2">
              <li><strong>Route planning:</strong> flag high-risk roads for driver warnings.</li>
              <li>
                <strong>Delivery scheduling:</strong> avoid high-risk roads during peak danger
                times.
              </li>
              <li><strong>Driver briefings:</strong> create corridor-specific safety briefings.</li>
              <li>
                <strong>Performance metrics:</strong> track improvement after route modifications.
              </li>
            </ul>
            <router-link :to="LINKS.correlations" class="btn btn-warning fw-bold mb-3"
              >📊 Go to Statistics &amp; Trends</router-link
            >
          </section>

          <!-- SENIOR RISK ASSESSMENT ANALYST -->
          <section id="senior-analyst" class="mb-5">
            <h2 class="section-title">Senior Risk Assessment Analyst</h2>

            <h3 class="sub-title">Risk Explorer Map — Suggestions</h3>
            <ul class="sg-list mb-3">
              <li>
                <strong>Premium pricing:</strong> use SA2/SA3 risk ratings to adjust base premiums
                by region.
              </li>
              <li>
                <strong>Market analysis:</strong> compare risk levels across regions to identify
                underserved high-risk markets.
              </li>
              <li>
                <strong>Portfolio management:</strong> monitor regional risk changes to adjust
                renewal pricing.
              </li>
              <li>
                <strong>Competitive intelligence:</strong> find low-risk areas to offer more
                competitive rates.
              </li>
            </ul>
            <router-link :to="LINKS.riskExplorer" class="btn btn-warning fw-bold mb-3"
              >🚦 Go to Risk Explorer</router-link
            >

            <h3 class="sub-title">Multi-factor Correlation Dashboard — Suggestions</h3>
            <ul class="sg-list mb-3">
              <li>
                <strong>Underwriting rules:</strong> use strong correlations to define automated
                criteria and red flags.
              </li>
              <li>
                <strong>Risk models:</strong> export correlation matrices to feed actuarial models.
              </li>
              <li>
                <strong>Claims prediction:</strong> identify factor combinations predicting higher
                claim frequency/severity.
              </li>
              <li>
                <strong>Product development:</strong> design products for specific risk profiles.
              </li>
            </ul>

            <h3 class="sub-title">High-risk Roads Analysis — Suggestions</h3>
            <ul class="sg-list mb-2">
              <li>
                <strong>Route restrictions:</strong> implement premium adjustments/coverage limits
                for fleets using high-risk corridors.
              </li>
              <li>
                <strong>Client advisory:</strong> provide high-risk road lists for route planning
                and risk management.
              </li>
              <li>
                <strong>Claims investigation:</strong> use road risk rankings to inform claim
                assessment and fraud detection.
              </li>
              <li>
                <strong>Risk communication:</strong> share insights with clients to help reduce
                exposure and claims.
              </li>
            </ul>
            <router-link :to="LINKS.correlations" class="btn btn-warning fw-bold mb-3"
              >📊 Go to Statistics &amp; Trends</router-link
            >
          </section>

          <!-- TRAFFIC SAFETY DATA ANALYST (POLICE) -->
          <section id="police-analyst" class="mb-5">
            <h2 class="section-title">Traffic Safety Data Analyst (Victoria Police)</h2>

            <h3 class="sub-title">Risk Explorer Map — Suggestions</h3>
            <ul class="sg-list mb-3">
              <li>
                <strong>Patrol deployment:</strong> schedule units to high-risk areas during peak
                crash times for maximum prevention impact.
              </li>
              <li>
                <strong>Resource allocation:</strong> use risk density to justify additional
                resources for high-crash districts.
              </li>
              <li>
                <strong>Community engagement:</strong> share anonymised risk maps with councils to
                support safety initiatives.
              </li>
              <li>
                <strong>Operation planning:</strong> coordinate speed cameras and enforcement with
                temporal crash patterns.
              </li>
            </ul>
            <router-link :to="LINKS.riskExplorer" class="btn btn-warning fw-bold mb-3"
              >🚦 Go to Risk Explorer</router-link
            >

            <h3 class="sub-title">Multi-factor Correlation Dashboard — Suggestions</h3>
            <ul class="sg-list mb-3">
              <li>
                <strong>Enforcement strategy:</strong> target the strongest risk-factor combinations
                (e.g., young drivers at night).
              </li>
              <li>
                <strong>Prevention programs:</strong> design community education based on
                demographic correlations.
              </li>
              <li>
                <strong>Tactical response:</strong> adjust patrol strategies using weather–crash and
                seasonal patterns.
              </li>
              <li>
                <strong>Performance measurement:</strong> track effectiveness by monitoring changes
                in targeted factors.
              </li>
            </ul>

            <h3 class="sub-title">High-risk Roads Analysis — Suggestions</h3>
            <ul class="sg-list mb-2">
              <li>
                <strong>Speed camera placement:</strong> position cameras on high-risk roads with
                appropriate history to support legal requirements.
              </li>
              <li>
                <strong>Patrol routes:</strong> design routes that cover multiple high-risk segments
                efficiently.
              </li>
              <li>
                <strong>Traffic management:</strong> coordinate with engineers to implement
                improvements at highest-risk locations.
              </li>
              <li>
                <strong>Public communication:</strong> use evidence-based risk data to explain
                enforcement to media and community.
              </li>
              <li class="fst-italic">
                <strong>Speed Camera Placement:</strong> focus on segments with high density,
                recurring night-time crashes, and over-speed factors.
              </li>
            </ul>
            <router-link :to="LINKS.correlations" class="btn btn-warning fw-bold mb-3"
              >📊 Go to Statistics &amp; Trends</router-link
            >
          </section>
        </main>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* keep headings visible beneath fixed navbar and for anchor jumps */
.bg-white {
  padding-top: 80px;
}
section {
  scroll-margin-top: 80px;
}

/* smooth anchor scroll */
html :global(html) {
  scroll-behavior: smooth;
}

/* yellow theme accents */
.bg-yellow-50 {
  background: #fff8db;
}
.section-title {
  font-size: 1.6rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
  position: relative;
  padding-bottom: 0.35rem;
}
.section-title::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: 0;
  width: 72px;
  height: 4px;
  background: #f6b300;
  border-radius: 2px;
}
.sub-title {
  font-weight: 700;
  color: #374151;
  margin: 1rem 0 0.35rem;
}
.sg-list {
  padding-left: 1.25rem;
  margin: 0;
}
.sg-list li {
  margin-bottom: 0.4rem;
}
.sg-list li::marker {
  color: #f6b300;
}

.accent-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #f6b300;
  display: inline-block;
}

/* sidebar */
.toc .nav-link {
  color: #6b7280;
}
.toc .nav-link:hover {
  color: #111;
}
.card {
  border-radius: 0.75rem;
}
.list-group-item {
  border: 0;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
}

/* buttons – theme gold */
.btn-warning {
  background-color: #f6b300;
  border: none;
}
.btn-warning:hover {
  background-color: #c98600;
}
</style>
