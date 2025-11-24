import os

files_main = ['app/main.py']
files_pages = [
    'app/pages/01_Overview.py',
    'app/pages/02_Adoption_and_Readiness.py',
    'app/pages/03_Learning_Impact.py',
    'app/pages/04_Engagement_and_Pathways.py',
    'app/pages/05_Reflections_and_VoC.py',
    'app/pages/06_Forecasts_and_Reports.py'
]

snippet_main = """import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

"""

snippet_pages = """import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

"""

def prepend_to_file(filepath, snippet):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath} (not found)")
        return

    with open(filepath, 'r') as f:
        content = f.read()
    
    # Avoid double patching
    if "sys.path.append" in content:
        print(f"Skipping {filepath} (already patched)")
        return

    with open(filepath, 'w') as f:
        f.write(snippet + content)
    print(f"Patched {filepath}")

for f in files_main:
    prepend_to_file(f, snippet_main)

for f in files_pages:
    prepend_to_file(f, snippet_pages)
