import logging
import sys
import os
from src.Safety_core.analyzer import VertexAIAnalyzer

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Safety-AI-Test")

def verify_gemini_integration():
    """
    Verifies that the Safety Analyzer can call Vertex AI.
    Requires: GOOGLE_APPLICATION_CREDENTIALS and a valid GCP Project.
    """
    project_id = os.getenv("GCP_PROJECT_ID", "your-project-id")
    
    logger.info(f"🚀 Initializing VertexAIAnalyzer for project: {project_id}")
    analyzer = VertexAIAnalyzer(project_id=project_id)

    # Simulated Byzantine Incident
    logs = [
        {"textPayload": "OOMKiller: pod 'api-gateway' terminated with exit code 137", "timestamp": 1715424000},
        {"textPayload": "CRITICAL: Memory pressure on node-x-4", "timestamp": 1715424001}
    ]
    
    logger.info("📡 Sending logs to Gemini 1.5 Pro...")
    result = analyzer.analyze(incident_type="oomkill", logs=logs)

    logger.info("--- AI REASONING RESULT ---")
    print(f"Root Cause: {result.get('root_cause')}")
    print(f"Remediation: {result.get('remediation')}")
    print(f"Engine: {result.get('engine')}")
    logger.info("---------------------------")

if __name__ == "__main__":
    verify_gemini_integration()
