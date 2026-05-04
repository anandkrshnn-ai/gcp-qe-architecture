import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
import google.cloud.logging
import json

vertexai.init(project="YOUR_PROJECT_ID", location="asia-south1")

model = GenerativeModel(
    "gemini-3.1-pro",
    generation_config=GenerationConfig(
        temperature=0.1,        # Low temperature for consistent analysis
        max_output_tokens=2048,
        response_mime_type="application/json"   # Force JSON output
    )
)

def analyze_incident(log_filter: str, limit: int = 40):
    client = google.cloud.logging.Client()
    entries = list(client.list_entries(filter_=log_filter, page_size=limit))
    
    log_context = "\n".join([str(entry.payload) for entry in entries[-30:]])
    
    prompt = f"""You are a senior GCP Quality Engineering Architect with 10+ years experience.

Analyze the logs below and return **only valid JSON** with this exact structure:

{{
  "root_cause": "short description",
  "confidence_percent": 85,
  "impacted_services": ["GKE", "Cloud Run"],
  "severity": "High/Medium/Low",
  "recommended_quality_gates": ["Performance Testing", "Chaos Testing"],
  "suggested_fix": "specific command or config change",
  "chaos_experiment_suggestion": "pod-kill | network-latency | none",
  "reasoning_summary": "2-3 sentence explanation"
}}

Logs:
{log_context}"""

    response = model.generate_content(prompt)
    print(response.text)
    return response.text
