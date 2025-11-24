# AIRE Impact Dashboard (Synthetic Data)

Applied AI Innovation & Research Enablement (AIRE) | College of Social Science, Michigan State University

## Institutional Context
This dashboard mirrors an internally deployed AIRE Impact Dashboard originally hosted on MSU systems to help leadership, program managers, and analysts understand the impact of an AI literacy initiative. The GitHub version ships **only synthetic dummy data** that mimics realistic patterns; no institutional data is present. The synthetic data ensures the dashboard is fully populated on first run for transparency, learning, and collaboration.

## What You Can Explore
- Aggregate analytics across all departments.
- Any combination of departments through the department multiselect.
- Single-department deep dives.
- Filters by user group (faculty, staff, graduate students, and mixed audiences) that update every chart.
- Date-range filtering across workshops and reflections.

## Key KPIs and Sections
- **Overview:** Adoption index, coverage, completion, and total attendances for the selected filters.
- **AI Adoption & Readiness:** Composite adoption index (readiness, coverage, participant adoption levels).
- **Learning Outcomes & Confidence:** Pre/post confidence and responsible AI understanding with effect deltas.
- **Participation & Engagement:** Attendance over time plus breakdown by format and audience.
- **Reflections & Sentiment:** Qualitative themes and sentiment distribution from participant reflections.
- **Department Readiness Matrix:** Readiness vs. coverage with participant volume context.

## Synthetic Data
Located in `data/synthetic/`. Files include workshops, participants, confidence surveys (pre/post), reflections, and departments. Data spans over a year, covers 12 departments, multiple user groups, and is structured so charts are populated by default while remaining realistic.

## Filters and How They Work
- **Date range:** Limits workshops, surveys, and reflections to the selected window.
- **Departments:** Select one, multiple, or all departments; KPIs and charts respect the selection.
- **User groups:** Filter by faculty, staff, graduate students, or mixed audiences; affects participant-driven metrics and workshop audience views.

## Run Locally
```
pip install -r requirements.txt
streamlit run app.py
```
Streamlit opens at the provided local URL with all charts populated from the synthetic dataset.

## Testing and CI
- Run tests locally with `pytest`.
- GitHub Actions (`.github/workflows/ci.yml`) installs dependencies and runs the test suite on push/pull_request to `main`.

## Interpretation Guide
- **Overview cards:** Rapid sense of reach and completion; adoption index is scaled 0–100.
- **Adoption radar:** Compare readiness and adoption momentum across selected departments.
- **Confidence change:** Bars show pre vs. post averages; positive deltas indicate learning gains.
- **Engagement:** Time series highlights demand cycles; format/audience bars show where participation concentrates.
- **Reflections:** Sentiment mix plus top themes surface qualitative signals and risks.
- **Readiness matrix:** Bubbles show how coverage correlates with readiness; use filters to isolate divisions.

## License
MIT License. See `LICENSE` for details.
