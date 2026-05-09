import json
import os
from tools import fetch_logs, inspect_environment, check_resource_usage, query_k8s_events, TOOL_DEFINITIONS
from mock_data import SCENARIOS

class SovereignSREAgent:
    """
    Autonomous Diagnostic Agent following NemoClaw principles.
    Uses Gemini (Vertex AI) to reason about production failures.
    """

    def __init__(self, mode="mock"):
        self.mode = mode
        self.system_prompt = """
        You are 'The Sovereign SRE', a high-privilege, low-trust autonomous agent.
        Your goal is to perform Root Cause Analysis (RCA) on production incidents.
        
        Rules:
        1. Use available tools to gather evidence.
        2. Never guess; cite specific evidence from logs or metrics.
        3. Provide the RCA in structured JSON format.
        """

    def run_rca(self, scenario_id="oom_kill"):
        scenario = SCENARIOS.get(scenario_id)
        print(f"[*] Starting RCA for: {scenario['alert']}")
        
        if self.mode == "mock":
            return self._run_mock_reasoning(scenario)
        else:
            # Placeholder for real Vertex AI loop
            print("[!] Real Vertex AI mode requires GOOGLE_APPLICATION_CREDENTIALS.")
            return None

    def _run_mock_reasoning(self, scenario):
        """Simulates the Gemini reasoning loop."""
        print("\n[THOUGHT] I see an SLO alert for transaction-engine. I need to check the K8s events first.")
        events = query_k8s_events("production")
        print(f"[ACTION] query_k8s_events(namespace='production') -> {len(events)} events found.")
        
        print("\n[THOUGHT] The events show an OOMKilling. I need to check the resource usage and logs for the pod.")
        usage = check_resource_usage("transaction-engine-v1-8f92")
        print(f"[ACTION] check_resource_usage('transaction-engine-v1-8f92') -> Memory: {usage['memory_usage']} / {usage['limit']}")
        
        logs = scenario["logs"]
        print(f"[ACTION] fetch_logs('transaction-engine-v1-8f92') -> Found OOMError in logs.")
        
        print("\n[THOUGHT] Final Analysis: The service is hitting its 2GB memory limit during batch processing.")
        
        rca_report = {
            "root_cause": "Java Heap Space exhaustion during high-volume batch processing.",
            "confidence": 95,
            "evidence": [
                "K8s Event: OOMKilling detected.",
                "Logs: ERROR java.lang.OutOfMemoryError: Java heap space",
                f"Metrics: Memory usage at {usage['memory_usage']} of {usage['limit']} limit."
            ],
            "recommended_action": "Increase memory limit to 4GB or optimize batch_size logic in transaction-engine.",
            "attestation": "Analyzed within NemoClaw Sandbox (GCP us-central1)"
        }
        
        print("\n[SUCCESS] RCA COMPLETE")
        print(json.dumps(rca_report, indent=2))
        return rca_report

if __name__ == "__main__":
    agent = SovereignSREAgent(mode="mock")
    agent.run_rca()
