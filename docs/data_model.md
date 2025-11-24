# Data Model

The dashboard relies on a relational schema of CSV files.

## Entities

### Departments (`departments.csv`)
- Static list of academic and administrative units.
- Includes baseline readiness metadata.

### Workshops (`workshops.csv`)
- Training events with metadata (modality, track, level).
- Aggregated registration/attendance counts.

### Assessments (`assessments_pre.csv`, `assessments_post.csv`)
- Linked to `person_id` and `workshop_id`.
- Captures Likert-scale (1-5) responses on confidence and readiness.

### Adoption Events (`adoption_events.csv`)
- Longitudinal tracking of tool usage.
- Linked to `person_id`.

### Reflections (`reflections.csv`)
- Qualitative feedback and sentiment.
- Thematic tags.
