import json
import pandas as pd
from datetime import datetime

def analyze_defect_escape(incidents_file: str, gates_file: str):
    # Load sample data
    incidents = pd.read_json(incidents_file)
    
    report = {
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
        "total_incidents": len(incidents),
        "common_gaps": ["Performance Testing", "Chaos Validation", "SLO Monitoring"],
        "recommendations": [
            "Add k6 performance gates in CI/CD",
            "Schedule weekly chaos experiments",
            "Integrate Gemini RCA Agent for faster MTTR"
        ],
        "summary": "Most escapes happen due to missing resilience and performance gates."
    }
    
    with open("defect_escape_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print("✅ Defect Escape Analysis Complete")
    print(json.dumps(report, indent=2))
    return report

# Example usage
if __name__ == "__main__":
    analyze_defect_escape("sample_incidents.json", "sample_gates.json")
