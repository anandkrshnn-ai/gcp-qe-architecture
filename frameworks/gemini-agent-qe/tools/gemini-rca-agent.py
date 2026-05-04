import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig, Tool
import google.cloud.logging
import json
from typing import Dict

vertexai.init(project="YOUR_PROJECT_ID", location="asia-south1")

model = GenerativeModel(
    "gemini-3.1-pro",
    generation_config=GenerationConfig(
        temperature=0.1,
        max_output_tokens=2048,
        response_mime_type="application/json"
    )
)

def analyze_incident(log_filter: str, limit: int = 50) -> Dict:
    client = google.cloud.logging.Client()
    entries = list(client.list_entries(filter_=log_filter, page_size=limit))
    
    log_context = "\n".join([str(entry.payload) for entry in entries[-40:]])
    
    prompt = f"""You are an expert GCP Quality Engineering Architect.
Analyze the logs and return **only** valid JSON:

{{
  "root_cause": "concise description",
  "confidence": 85,
  "impacted_services": ["GKE", "Cloud Run"],
  "severity": "High/Medium/Low",
  "recommended_gates": ["k6 Performance", "Chaos Testing"],
  "suggested_fix": "specific actionable command/config",
  "chaos_suggestion": "pod-kill | network-latency | none",
  "reasoning": "brief explanation"
}}

Logs:
{log_context}"""

    response = model.generate_content(prompt)
    result = json.loads(response.text)
    return result

if __name__ == "__main__":
    # Example usage (uncomment and replace with real project ID to test)
    # result = analyze_incident("resource.type=\"cloud_run_revision\" severity>=ERROR")
    # print(json.dumps(result, indent=2))
    pass
