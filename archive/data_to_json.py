import pandas as pd
import json

df = pd.read_csv("combined_tables.csv")

df[['Course', 'Number']] = df[['Course', 'Number']].ffill()

df['Number'] = df['Number'].astype(str).str.replace(',', '').astype(int)

courses_json = {}

for _, row in df.iterrows():
    course = row['Course']
    mark_type = row['Type of mark'] 
    
    if course not in courses_json:
        courses_json[course] = {
            "enrolment": row['Number'],
            "hsc": {},
            "sca": {}
        }
    
    # Fill mark data
    courses_json[course][mark_type] = {
        "Mean": row['Mean'],
        "SD": row['SD'],
        "Max Mark": row['Max.mark'],
        "P99": row['P99'],
        "P90": row['P90'],
        "P75": row['P75'],
        "P50": row['P50'],
        "P25": row['P25']
    }

json_output = json.dumps(courses_json, indent=4)
print(json_output)

with open("courses.json", "w") as f:
    f.write(json_output)
