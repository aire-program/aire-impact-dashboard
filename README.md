# AIRE Impact Dashboard (Synthetic Data Mirror)
Applied AI Innovation & Research Enablement (AIRE) | College of Social Science | Michigan State University

## Purpose Within the AIRE Constellation
- Decision-support pillar alongside the AIRE Literacy Hub (responsible AI training) and the AIRE Researcher Sandbox (research experimentation).
- Leadership, program directors, and analysts need a clear view of institutional impact, departmental readiness, confidence growth, and adoption trends to steer responsible AI uptake.
- Integrates adoption, readiness, confidence, engagement, and qualitative signals so resources can be targeted to departments and audiences that need support.

## Institutional Positioning
- A professional program-evaluation instrument for monitoring reach, training effectiveness, adoption trajectories, and departmental needs.
- Supports evidence-based planning, accreditation, and continuous improvement across teaching, research, and administrative workflows.
- Provides transparent metrics for leadership to identify where responsible AI training is succeeding and where additional support structures are required.

## Rationale for an Institutional Analytics Layer
- A centralized view of uptake, competencies, and equity of access as AI adoption accelerates across the college.
- Ensures readiness, transparency, and stewardship; anchors reporting to Deans and program directors; supports governance and equitable access.
- Combines readiness, training coverage, participant adoption levels, and confidence growth to inform strategic investments and faculty development.

## Synthetic Data Notice
- This public GitHub version ships with realistic but entirely synthetic data.
- The internal dashboard uses secure institutional data; the public mirror exists for transparency, reproducibility, and collaborative review of the approach.
- Synthetic datasets populate every chart on first load, demonstrating the infrastructure without exposing institutional records.

## Dashboard Sections
- **Overview & Governance Signals:** Adoption index, coverage, completion, attendance footprint. Situational awareness for Deans/program directors; prioritize support for emerging demand or celebrate units exceeding targets.
- **AI Adoption & Departmental Readiness:** Composite adoption index plus readiness vs. coverage with targets. Spot prepared vs. at-risk departments; direct resources to units below coverage/readiness targets and replicate practices from high performers.
- **Learning Outcomes & Confidence:** Pre/post confidence and responsible AI understanding deltas. Validate training effectiveness; adjust modality and follow-on supports based on audience gains.
- **Participation & Engagement:** Attendance over time, format/audience breakdowns, completion. Optimize scheduling and staffing; align facilitators to peak months and effective formats.
- **Reflections & Sentiment:** Themed qualitative feedback with sentiment mix. Surface early signals on adoption, risks, and support needs; address recurring themes (ethical concerns, assessment) with targeted guidance.
- **Department Focus:** Targeted snapshot for a selected department. Brief chairs/associate deans with tailored insight; calibrate supports and track progress against readiness and coverage targets.

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
