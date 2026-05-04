import vertexai
from vertexai.generative_models import GenerativeModel
import google.cloud.logging
import json

# Initialize
vertexai.init(project="YOUR_PROJECT_ID", location="asia-south1")
model = GenerativeModel("gemini-3.1-pro")

def analyze_logs(log_filter: str, limit: int = 30):
    """Analyze recent logs and return structured RCA"""
    client = google.cloud.logging.Client()
    entries = list(client.list_entries(filter_=log_filter, page_size=limit))
    
    log_text = "\n".join([str(entry.payload) for entry in entries])
    
    prompt = f"""You are an expert GCP QE Architect.
Analyze the following logs and provide **structured JSON output**:

{{
  "root_cause": "...",
  "confidence": 85,
  "impacted_services": ["GKE", "Cloud Run"],
  "recommended_quality_gate": "...",
  "suggested_fix": "...",
  "chaos_experiment_recommended": true/false
}}

Logs:
{log_text[:18000]}"""

    response = model.generate_content(prompt)
    print(response.text)
    return response.text

# Example usage
if __name__ == "__main__":
    analyze_logs('resource.type="k8s_container" severity>=ERROR')
