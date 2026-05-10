"""
Sovereign Core: The Reasoning Engine.
Includes Pattern Matching (Deterministic) and Vertex AI (LLM) reasoning paths.
"""

import logging
import json
from typing import List, Dict, Optional

logger = logging.getLogger("SovereignCore.Analyzer")

class SovereignAnalyzer:
    """
    Autonomous Analyzer.
    Uses a Pattern Registry for fast, deterministic analysis.
    """
    def __init__(self):
        self.registry = {
            "oomkill": self._detect_oomkill,
            "latency": self._detect_latency
        }

    def analyze(self, incident_type: str, logs: List[Dict]) -> Dict:
        """Core analysis loop."""
        handler = self.registry.get(incident_type)
        if not handler:
            return {"root_cause": "Unknown Incident Type", "confidence": 0.0}
        
        return handler(logs)

    def _detect_oomkill(self, logs: List[Dict]) -> Dict:
        for entry in logs:
            msg = entry.get("jsonPayload", {}).get("message", "").lower()
            if "oomkilling" in msg or "out of memory" in msg:
                return {
                    "root_cause": "Pod OOMKill",
                    "confidence": 0.95,
                    "remediation": "Increase resource.limits.memory in K8s manifest."
                }
        return {"root_cause": "Not Found", "confidence": 0.0}

    def _detect_latency(self, logs: List[Dict]) -> Dict:
        for entry in logs:
            msg = entry.get("jsonPayload", {}).get("message", "").lower()
            if "deadlineexceeded" in msg or "timeout" in msg:
                return {
                    "root_cause": "Service Timeout (60s)",
                    "confidence": 0.92,
                    "remediation": "Increase Cloud Run timeout or optimize downstream query latency."
                }
        return {"root_cause": "Not Found", "confidence": 0.0}

class VertexAIAnalyzer(SovereignAnalyzer):
    """
    Advanced Analyzer using Google Gemini via Vertex AI.
    Implements structured reasoning for complex incident analysis.
    """
    def __init__(self, model_name: str = "gemini-1.5-flash", project_id: str = "demo-project"):
        super().__init__()
        self.model_name = model_name
        self.project_id = project_id
        self._initialized = False

    def _initialize_sdk(self):
        """Initializes Vertex AI if credentials are present."""
        if self._initialized:
            return True
        try:
            import vertexai
            vertexai.init(project=self.project_id, location="us-central1")
            self._initialized = True
            return True
        except ImportError:
            logger.warning("vertexai SDK not installed. Run: pip install sovereign-core[gcp]")
            return False
        except Exception as e:
            logger.warning(f"Vertex AI initialization failed: {e}")
            return False

    def analyze_with_llm(self, incident_type: str, logs: List[Dict]) -> Dict:
        """
        Uses Gemini to analyze logs using structured reasoning.
        Falls back to deterministic analyzer if SDK is missing.
        """
        if not self._initialize_sdk():
            logger.info("Falling back to Deterministic Analysis (No Vertex AI detected).")
            return self.analyze(incident_type, logs)

        try:
            from vertexai.generative_models import GenerativeModel, Part
            model = GenerativeModel(
                model_name=self.model_name,
                system_instruction=[
                    "You are a Principal SRE Agent specializing in GCP infrastructure.",
                    "Your task is to analyze JSON logs and identify root causes with high precision.",
                    "Return only valid JSON in the format: {'root_cause': str, 'confidence': float, 'remediation': str}"
                ]
            )
            
            prompt = f"Analyze these {incident_type} logs and provide a root cause analysis:\n{json.dumps(logs, indent=2)}"
            response = model.generate_content(prompt)
            
            # Note: In production, we use response_schema for guaranteed JSON.
            # Here we provide a robust fallback for the PoC.
            return json.loads(response.text.strip("```json").strip("```"))
        except Exception as e:
            logger.error(f"LLM Reasoning Error: {e}")
            return self.analyze(incident_type, logs)
