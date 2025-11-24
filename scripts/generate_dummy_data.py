import pandas as pd
import numpy as np
import uuid
import random
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

DATA_DIR = "data/dummy"
os.makedirs(DATA_DIR, exist_ok=True)

def generate_departments(n=10):
    divisions = ["Social Science", "Humanities", "Natural Science", "Engineering"]
    sizes = ["small", "medium", "large"]
    
    depts = []
    for i in range(n):
        dept_id = f"DEPT_{i+1:03d}"
        depts.append({
            "department_id": dept_id,
            "department_name": f"Department of {random.choice(['Sociology', 'Psychology', 'Economics', 'History', 'Political Science', 'Anthropology', 'Geography', 'Criminal Justice', 'Social Work', 'Human Development'])} {i+1}",
            "division": random.choice(divisions),
            "size_band": random.choice(sizes),
            "baseline_ai_readiness": round(random.uniform(0.1, 0.8), 2)
        })
    return pd.DataFrame(depts)

def generate_workshops(departments, n=20):
    tracks = ["fundamentals", "advanced", "ethics", "assessment", "special_topic"]
    levels = ["intro", "intermediate", "advanced"]
    modalities = ["online", "in_person", "hybrid"]
    
    workshops = []
    start_date = datetime(2023, 1, 1)
    
    for i in range(n):
        ws_id = f"WS_{i+1:03d}"
        date = start_date + timedelta(days=random.randint(0, 365))
        capacity = random.choice([20, 30, 50, 100])
        registrations = random.randint(int(capacity * 0.5), capacity)
        attended = random.randint(int(registrations * 0.7), registrations)
        
        workshops.append({
            "workshop_id": ws_id,
            "title": f"AI Workshop {i+1}: {random.choice(['Basics', 'Ethics', 'Prompt Engineering', 'Data Analysis', 'Future Trends'])}",
            "date": date.strftime("%Y-%m-%d"),
            "modality": random.choice(modalities),
            "track": random.choice(tracks),
            "level": random.choice(levels),
            "host_department_id": random.choice(departments["department_id"].tolist()),
            "capacity": capacity,
            "registrations": registrations,
            "attended": attended
        })
    return pd.DataFrame(workshops)

def generate_assessments(workshops, departments, n_participants=200):
    roles = ["faculty", "staff", "grad_student"]
    
    pre_assessments = []
    post_assessments = []
    
    # Generate a pool of people
    people = [f"P_{i+1:04d}" for i in range(n_participants)]
    
    for _, ws in workshops.iterrows():
        # Simulate attendees for this workshop
        attendees = random.sample(people, k=min(ws["attended"], len(people)))
        
        for person_id in attendees:
            dept_id = random.choice(departments["department_id"].tolist())
            role = random.choice(roles)
            
            # Pre-assessment (lower scores)
            pre_conf_tools = random.randint(1, 4)
            pre_conf_ped = random.randint(1, 4)
            pre_conf_risk = random.randint(1, 4)
            pre_readiness = random.randint(1, 4)
            
            pre_assessments.append({
                "assessment_id": str(uuid.uuid4()),
                "person_id": person_id,
                "workshop_id": ws["workshop_id"],
                "timestamp": (datetime.strptime(ws["date"], "%Y-%m-%d") - timedelta(days=random.randint(1, 5))).isoformat(),
                "role": role,
                "department_id": dept_id,
                "confidence_ai_tools": pre_conf_tools,
                "confidence_pedagogical_use": pre_conf_ped,
                "confidence_risk_mitigation": pre_conf_risk,
                "overall_readiness": pre_readiness
            })
            
            # Post-assessment (higher scores on average)
            post_assessments.append({
                "assessment_id": str(uuid.uuid4()),
                "person_id": person_id,
                "workshop_id": ws["workshop_id"],
                "timestamp": (datetime.strptime(ws["date"], "%Y-%m-%d") + timedelta(days=random.randint(0, 2))).isoformat(),
                "role": role,
                "department_id": dept_id,
                "confidence_ai_tools": min(5, pre_conf_tools + random.randint(0, 2)),
                "confidence_pedagogical_use": min(5, pre_conf_ped + random.randint(0, 2)),
                "confidence_risk_mitigation": min(5, pre_conf_risk + random.randint(0, 2)),
                "overall_readiness": min(5, pre_readiness + random.randint(0, 2))
            })
            
    return pd.DataFrame(pre_assessments), pd.DataFrame(post_assessments)

def generate_adoption_events(assessments_post, n=300):
    tool_categories = ["llm_assistant", "automated_feedback", "grading_helper", "data_analysis", "content_generation"]
    contexts = ["course_design", "assessment", "research", "administration"]
    
    events = []
    unique_people = assessments_post[["person_id", "department_id"]].drop_duplicates()
    
    for _ in range(n):
        person = unique_people.sample(1).iloc[0]
        
        events.append({
            "event_id": str(uuid.uuid4()),
            "person_id": person["person_id"],
            "department_id": person["department_id"],
            "date": (datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),
            "tool_category": random.choice(tool_categories),
            "context": random.choice(contexts),
            "intensity": random.randint(1, 10),
            "risk_flag": random.random() < 0.05 # 5% risk flag
        })
    return pd.DataFrame(events)

def generate_reflections(assessments_post, n=150):
    sentiments = ["positive", "mixed", "negative"]
    themes = ["confidence", "time", "policy", "support", "tools"]
    
    reflections = []
    unique_people = assessments_post[["person_id", "department_id", "role"]].drop_duplicates()
    
    for _ in range(n):
        person = unique_people.sample(1).iloc[0]
        
        reflections.append({
            "reflection_id": str(uuid.uuid4()),
            "person_id": person["person_id"],
            "workshop_id": None, # Optional
            "timestamp": (datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365))).isoformat(),
            "department_id": person["department_id"],
            "role": person["role"],
            "reflection_text": "This is a synthetic reflection text about AI adoption.",
            "sentiment": random.choices(sentiments, weights=[0.6, 0.3, 0.1])[0],
            "theme": random.choice(themes)
        })
    return pd.DataFrame(reflections)

def main():
    print("Generating synthetic data...")
    
    df_depts = generate_departments()
    df_workshops = generate_workshops(df_depts)
    df_pre, df_post = generate_assessments(df_workshops, df_depts)
    df_events = generate_adoption_events(df_post)
    df_reflections = generate_reflections(df_post)
    
    # Save to CSV
    df_depts.to_csv(f"{DATA_DIR}/departments.csv", index=False)
    df_workshops.to_csv(f"{DATA_DIR}/workshops.csv", index=False)
    df_pre.to_csv(f"{DATA_DIR}/assessments_pre.csv", index=False)
    df_post.to_csv(f"{DATA_DIR}/assessments_post.csv", index=False)
    df_events.to_csv(f"{DATA_DIR}/adoption_events.csv", index=False)
    df_reflections.to_csv(f"{DATA_DIR}/reflections.csv", index=False)
    
    print("Data generation complete.")
    print(f"Departments: {len(df_depts)}")
    print(f"Workshops: {len(df_workshops)}")
    print(f"Assessments Pre: {len(df_pre)}")
    print(f"Assessments Post: {len(df_post)}")
    print(f"Adoption Events: {len(df_events)}")
    print(f"Reflections: {len(df_reflections)}")

if __name__ == "__main__":
    main()
