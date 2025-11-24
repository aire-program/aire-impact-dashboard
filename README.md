# AIRE Impact Dashboard (Synthetic Data Mirror)
Applied AI Innovation & Research Enablement (AIRE) | College of Social Science | Michigan State University

## Purpose Within the AIRE Constellation
- **WHAT:** Decision-support pillar alongside the AIRE Literacy Hub (responsible AI training) and the AIRE Researcher Sandbox (research experimentation).
- **WHY:** Leadership, program directors, and analysts need a clear view of institutional impact, departmental readiness, confidence growth, and adoption trends to steer responsible AI uptake.
- **HOW:** Integrates adoption, readiness, confidence, engagement, and qualitative signals so resources can be targeted to departments and audiences that need support.

## Institutional Positioning
- **WHAT:** A professional program-evaluation instrument for monitoring reach, training effectiveness, adoption trajectories, and departmental needs.
- **WHY:** Supports evidence-based planning, accreditation, and continuous improvement across teaching, research, and administrative workflows.
- **HOW:** Provides transparent metrics for leadership to identify where responsible AI training is succeeding and where additional support structures are required.

## Rationale for an Institutional Analytics Layer
- **WHAT:** A centralized view of uptake, competencies, and equity of access as AI adoption accelerates across the college.
- **WHY:** Ensures readiness, transparency, and stewardship; anchors reporting to Deans and program directors; supports governance and equitable access.
- **HOW:** Combines readiness, training coverage, participant adoption levels, and confidence growth to inform strategic investments and faculty development.

## Synthetic Data Notice
- **WHAT:** This public GitHub version ships with realistic but entirely synthetic data.
- **WHY:** The internal dashboard uses secure institutional data; the public mirror exists for transparency, reproducibility, and collaborative review of the approach.
- **HOW:** Synthetic datasets populate every chart on first load, demonstrating the infrastructure without exposing institutional records.

## Dashboard Sections (WHAT / WHY / HOW)
- **Overview & Governance Signals:** WHAT: adoption index, coverage, completion, attendance footprint. WHY: situational awareness for Deans/program directors. HOW: prioritize support for emerging demand or celebrate units exceeding targets.
- **AI Adoption & Departmental Readiness:** WHAT: composite adoption index plus readiness vs. coverage with targets. WHY: spot prepared vs. at-risk departments. HOW: direct resources to units below coverage/readiness targets; replicate practices from high performers.
- **Learning Outcomes & Confidence:** WHAT: pre/post confidence and responsible AI understanding deltas. WHY: validate training effectiveness. HOW: adjust modality and follow-on supports based on audience gains.
- **Participation & Engagement:** WHAT: attendance over time, format/audience breakdowns, completion. WHY: optimize scheduling and staffing. HOW: align facilitators to peak months and effective formats.
- **Reflections & Sentiment:** WHAT: themed qualitative feedback with sentiment mix. WHY: surface early signals on adoption, risks, and support needs. HOW: address recurring themes (ethical concerns, assessment) with targeted guidance.
- **Department Focus:** WHAT: targeted snapshot for a selected department. WHY: brief chairs/associate deans with tailored insight. HOW: calibrate supports and track progress against readiness and coverage targets.

## Filters and How They Work
- **Date range:** Limits workshops, surveys, and reflections to the selected window.
- **Departments:** Select one, multiple, or all departments; KPIs and charts respect the selection.
- **User groups:** Filter by faculty, staff, graduate students, or mixed audiences; affects participant-driven metrics and workshop audience views.

## Run Locally
```
pip install -r requirements.txt
streamlit run app.py
```
All charts are populated from synthetic data on first load.

## Testing and CI
- Run tests locally with `pytest`.
- GitHub Actions (`.github/workflows/ci.yml`) installs dependencies and runs the test suite on push/pull_request to `main`.

## License
MIT License. See `LICENSE` for details.
