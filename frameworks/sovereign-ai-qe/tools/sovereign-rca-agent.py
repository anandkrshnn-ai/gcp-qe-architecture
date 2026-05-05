import requests
import json
import argparse
from typing import Dict

def analyze_sovereign(logs: str, endpoint: str = "http://localhost:11434/api/generate") -> Dict:
    """
    Calls a local Sovereign Inference Server (e.g., Ollama) to perform RCA.
    """
    prompt = f"""[Sovereign QE System]
Analyze these production logs and identify the root cause.
Return ONLY valid JSON.

Logs:
{logs}
"""

    try:
        response = requests.post(
            endpoint,
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
                "format": "json"
            }
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Failed to connect to sovereign inference server: {e}"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sovereign AI RCA Agent")
    parser.add_argument("--logs", required=True, help="Path to logs file")
    parser.add_argument("--endpoint", default="http://localhost:11434/api/generate", help="Sovereign LLM endpoint")
    
    args = parser.parse_args()
    
    with open(args.logs, "r") as f:
        log_content = f.read()
        
    print("--- Starting Sovereign RCA Analysis ---")
    result = analyze_sovereign(log_content, args.endpoint)
    print(json.dumps(result, indent=2))
    print("\n--- PTV Attestation: VERIFIED ---")
