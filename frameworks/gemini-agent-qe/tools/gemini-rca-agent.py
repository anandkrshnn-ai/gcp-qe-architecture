import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
import google.cloud.logging
import json
import argparse
import sys
from typing import Dict

def load_mock_logs(file_path: str) -> str:
    with open(file_path, "r") as f:
        logs = json.load(f)
    return "\n".join([str(log.get("textPayload") or log.get("jsonPayload") or log.get("protoPayload")) for log in logs])

def analyze_incident(log_filter: str, project_id: str = None, mock_file: str = None) -> Dict:
    # 1. Gather Context
    if mock_file:
        print(f"--- Running in MOCK mode using {mock_file} ---")
        log_context = load_mock_logs(mock_file)
    else:
        if not project_id or project_id == "YOUR_PROJECT_ID":
            print("Error: project_id required for live mode.")
            sys.exit(1)
        
        vertexai.init(project=project_id, location="asia-south1")
        client = google.cloud.logging.Client(project=project_id)
        entries = list(client.list_entries(filter_=log_filter, page_size=40))
        log_context = "\n".join([str(entry.payload) for entry in entries])

    # 2. Configure Model
    # Note: In mock mode, we simulate the logic to ensure the downstream pipeline works.
    if mock_file:
        return {
            "root_cause": "GKE Pod OOMKill detected in mock logs",
            "confidence": 95,
            "impacted_services": ["GKE", "Mock-Service"],
            "severity": "High",
            "recommended_gates": ["k6 Performance", "Chaos Mesh Pod-Kill"],
            "suggested_fix": "Add resources.limits.memory to the deployment manifest",
            "chaos_suggestion": "pod-kill",
            "reasoning": f"Simulated analysis based on {len(log_context.splitlines())} log lines."
        }

    model = GenerativeModel(
        "gemini-1.5-pro",
        generation_config=GenerationConfig(
            temperature=0.1,
            max_output_tokens=2048,
            response_mime_type="application/json"
        )
    )

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
    return json.loads(response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gemini RCA Agent")
    parser.add_argument("--project", help="GCP Project ID", default="YOUR_PROJECT_ID")
    parser.add_argument("--filter", help="Cloud Logging filter", default="resource.type=\"k8s_container\" severity>=ERROR")
    parser.add_argument("--mock", help="Path to mock logs JSON file")
    
    args = parser.parse_args()
    
    try:
        result = analyze_incident(args.filter, args.project, args.mock)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
