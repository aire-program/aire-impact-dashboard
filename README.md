# AIRE Impact Dashboard  
### *Public Synthetic-Data Mirror of the Internal Institutional Analytics System*  
### Applied AI Innovation & Research Enablement (AIRE) Program  
College of Social Science, Michigan State University

---

## Overview

The **AIRE Impact Dashboard** is the institutional analytics environment used within the College of Social Science at Michigan State University to understand how responsible AI literacy is developing across departments, roles, and instructional pathways.

Developed as part of the **Applied AI Innovation & Research Enablement (AIRE) Program**, the dashboard brings together participation records, pre–post confidence measures, workshop attributes, departmental readiness indicators, and qualitative reflections to create a coherent view of how AI literacy is adopted, strengthened, and sustained across the college.

The internal version of the dashboard ran on secure MSU systems and served as a regular point of reference for college leadership, department chairs, faculty development teams, assessment specialists, and governance committees. It supported day-to-day program monitoring as well as longer-term planning for resource allocation, professional development, and responsible AI implementation.

This public GitHub repository is a **synthetic-data mirror** of that internal system. It reproduces the structure, workflow, and analytical logic of the institutional dashboard while using fully fabricated data so that external users can explore, run, modify, and understand the framework without exposing confidential institutional information. Every chart and metric loads immediately with meaningful synthetic values, making the environment suitable for demonstration, collaboration, and further development.

---

## Position in the AIRE Program

The dashboard is one of three components that make up the AIRE Program’s coordinated approach to responsible AI enablement:

- **AIRE Literacy Hub** — a curricular and training environment that supports faculty, staff, students, and researchers in developing responsible AI practices through workshops, modules, and learning pathways.

- **AIRE Researcher Sandbox** — a research-facing toolkit providing notebooks, pipelines, and safe experimentation environments for scholars who want to integrate AI into their research methods and data workflows.

- **AIRE Impact Dashboard** — the decision-intelligence layer that analyzes how training is being used, how confidence and competency are shifting, where departments are ready to advance, and where additional support will be needed in the coming terms.

Together, these three elements form a continuous cycle: learning → experimentation → insight.  
The dashboard closes the loop by translating activity and feedback into actionable intelligence for leadership.

---

## Purpose and Use in Institutional Decision-Making

AI literacy work affects faculty, staff, students, and research units differently. Some departments rapidly embrace new technologies; others proceed more cautiously or require additional support. To manage this diversity across a large and interdisciplinary college, leadership needs a stable view of:

- patterns of participation across roles and units  
- whether training is improving confidence and competency  
- which departments are developing readiness for deeper integration  
- areas where additional mentoring, workshops, or consultations are needed  
- how teams are responding to responsible AI guidance  
- emerging questions, concerns, risks, and opportunities reported by participants  

The dashboard consolidates these signals into a single environment that leadership can consult throughout the year. It helps program designers refine workshop sequences, supports accreditation- or reporting-related needs, guides decision-making around professional development, and provides a clearer sense of where the college stands in relation to its goals for responsible and ethical AI adoption.

---

## How the Dashboard Is Structured

The dashboard organizes the AIRE Program’s data into several interconnected views, each highlighting a different dimension of institutional progress.

### Overall Program Picture

A high-level summary distilling participation levels, shifts in confidence, adoption indicators, and readiness patterns. This view anchors the rest of the dashboard and helps leadership quickly understand college-wide trends.

### Departmental Adoption and Readiness

Charts that show how units compare in terms of readiness, training coverage, and adoption behaviors. These insights help identify departments that are well-positioned for future AI initiatives and those that may require tailored support.

### Learning Outcomes and Confidence Growth

Pre- and post-training confidence measures that show how well participants feel they understand responsible AI practice, how comfortable they are with tools, and how those self-assessments change after engagement with the AIRE curriculum.

### Participation and Engagement Trends

A time-based view of workshops, microcourses, and training sessions, segmented by role and format. These patterns are useful for planning workshop schedules, anticipating demand, and coordinating faculty development resources.

### Reflections and Emerging Themes

Qualitative feedback from participants, categorized by sentiment and thematic focus. These insights help identify early concerns, areas where more guidance is needed, and opportunities for program improvement.

### Department Readiness Matrix

A combined view of readiness and training coverage that highlights which departments may be ready to begin more advanced or specialized responsible AI initiatives.

These sections interact through filters that allow leadership to examine the data for all departments, specific subsets, or single units, and to isolate the behaviors of different groups such as faculty, staff, and graduate students.

---

## Synthetic Data and Public Transparency

To make this dashboard publicly accessible without exposing institutional information, the GitHub version uses **entirely synthetic data**. The datasets have been carefully constructed to resemble real institutional patterns—varied participation, uneven adoption levels, real-world shifts in confidence, meaningful reflection themes—without duplicating or revealing any data used internally.

This approach allows researchers, developers, and collaborators to:

- run the dashboard immediately  
- explore the analytic model  
- understand how data flows into KPIs  
- upload their own datasets  
- integrate or extend the dashboard in their own environments  

The synthetic dataset also supports teaching, demonstration, and onboarding without requiring access to restricted institutional systems.

---

## Data Upload and Local Exploration

The dashboard includes a dedicated **Data Management** interface. This interface allows users to upload their own CSV files (following documented column formats) and explore how the dashboard behaves with alternative datasets.

Uploaded data is:

- validated against established schemas  
- held in the local session only  
- used to recompute all metrics and visualizations  

The synthetic dataset remains available as the default for immediate use.

---

## Filtering and Comparative Analysis

Filters support a wide range of institutional questions. Users can:

- select all departments to see college-wide patterns  
- choose a single department to examine its trajectory in detail  
- compare several departments for deeper analysis  
- view trends for specific roles (faculty, staff, graduate students)  
- adjust date ranges to focus on recent semesters or annual cycles  

Every visualization adapts to the selected filters, making the dashboard useful for strategic planning meetings and data-driven conversations.

---

## Running the Dashboard Locally

Install dependencies:

    pip install -r requirements.txt

Run the dashboard:

    streamlit run app.py

The environment will load using the synthetic dataset so that all views are populated immediately.

---

## Testing and Continuous Integration

This repository includes:

- schema validation  
- data integrity tests  
- KPI validation tests  
- import and environment checks  
- a GitHub Actions-based CI workflow  

All tests may be run via:

    pytest

---

## License

Distributed as an open resource in support of transparent, responsible AI literacy development and collaborative institutional analytics.
