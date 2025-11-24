import pandas as pd
import os
import sys

# Add parent dir to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.data_loader import load_all_data
from app.kpi_calculations import calculate_participation_metrics, calculate_confidence_deltas

def main():
    print("Building Example Reports...")
    
    try:
        data = load_all_data()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please run scripts/generate_dummy_data.py first.")
        return

    # Report 1: Executive Summary
    print("\n--- Executive Summary ---")
    participation = calculate_participation_metrics(data["workshops"])
    print(f"Total Workshops: {participation['total_workshops']}")
    print(f"Total Registrations: {participation['total_registrations']}")
    print(f"Attendance Rate: {participation['avg_attendance_rate']:.1f}%")
    
    deltas = calculate_confidence_deltas(data["assessments_pre"], data["assessments_post"])
    print(f"Overall Readiness Improvement: +{deltas['overall_readiness_delta']:.2f}")

    # Report 2: Departmental Breakdown
    print("\n--- Top 5 Departments by Engagement ---")
    dept_engagement = data["assessments_post"]["department_id"].value_counts().head(5)
    print(dept_engagement)

    print("\nReport generation complete.")

if __name__ == "__main__":
    main()
