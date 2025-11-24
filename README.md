Applied AI Literacy – Program Impact Dashboard  
AIRE Program – Applied AI Innovation & Research Enablement, College of Social Science, Michigan State University  

The Applied AI Literacy – Program Impact Dashboard is part of the Applied AI Innovation & Research Enablement (AIRE) Program, an institutional initiative in the College of Social Science at Michigan State University. The program was created to support responsible, evidence-based AI adoption across teaching, learning, and research.

This dashboard was originally developed and deployed on internal MSU systems as the analytics and reporting layer for the Applied AI Literacy initiative. It provided college leadership with a data-driven understanding of how AI literacy efforts were progressing across departments, roles, and time.

This GitHub repository is a public, synthetic-data mirror of that dashboard, released to support transparency, reproducibility, and cross-institutional collaboration around AI literacy evaluation and governance. All data in this repository is synthetic and generated programmatically.

Executive Summary  
The Applied AI Literacy – Program Impact Dashboard gives leadership a consolidated view of:

- participation and engagement  
- confidence and readiness shifts  
- adoption behaviors after training  
- departmental readiness and resource needs  
- reflections and qualitative themes  
- forecasting of future training demand  

Institutional Rationale  
1. Evidence-based program evaluation  
2. Support for policy, governance, and strategic planning  
3. Transparent, reproducible methodology  
4. Cross-unit collaboration  

Dashboard Capabilities  
1. AI Adoption and Readiness Analytics  
2. Learning Impact and Confidence Deltas  
3. Engagement and Pathway Tracking  
4. Reflections and Voice-of-Community Analysis  
5. Forecasting and Predictive Indicators  

Relationship to the AIRE Program and AI Literacy Hub  
The Program Impact Dashboard complements the Applied AI Literacy Hub (hosted under the applied-ai-literacy GitHub organization), which provides microcourses and teaching resources for AI literacy, and the AI Researcher Developer Sandbox, which offers a technical environment for research workflows. Together, these projects form a cohesive portfolio that spans pedagogy, research enablement, and institutional analytics.

Synthetic Data  
All data is fully synthetic and produced via scripts/generate_dummy_data.py. The schema and patterns are modeled on realistic institutional scenarios but contain no real records.

Repository Overview  
app/ — Streamlit multipage dashboard  
data/ — Synthetic CSVs and schemas  
notebooks/ — KPI exploration and forecasting examples  
scripts/ — Data generation and report builders  
tests/ — Data, loader, and KPI tests  
docs/ — KPI definitions and methodology  
.github/workflows — CI and smoke tests  

Running the Dashboard  
Clone the repository, create a virtual environment, install requirements, generate dummy data, and run:

- python scripts/generate_dummy_data.py  
- streamlit run app/main.py  

CI & Testing  
The pytest suite validates dataset integrity, data loader behavior, KPI logic, and forecasting functions. GitHub Actions performs CI and smoke tests to ensure that the dashboard remains reproducible and deployable.

Documentation  
Documentation is located in docs/, including an overview, KPI definitions, data model, and deployment notes.

License & Openness  
This project is released under the MIT License to support transparency, evidence-based AI literacy evaluation, and inter-institutional adaptation. See LICENSE for details.
