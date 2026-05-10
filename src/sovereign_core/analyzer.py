"""
Sovereign Core: The Reasoning Engine.
Includes Pattern Matching (Deterministic) and Vertex AI (LLM) reasoning paths.
"""

import logging
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
    [FUTURE] Advanced Analyzer using Google Gemini via Vertex AI.
    Inherits from the base analyzer to provide 'LLM-enhanced' reasoning.
    """
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        super().__init__()
        self.model_name = model_name

    def analyze_with_llm(self, incident_type: str, logs: List[Dict]) -> Dict:
        """
        Uses Gemini to analyze logs when pattern matching is insufficient.
        """
        # Placeholder for real Vertex AI integration
        logger.info(f"Reasoning with {self.model_name}...")
        
        # In production, this would call vertexai.generative_models.GenerativeModel
        # For the PoC, we fall back to the deterministic analyzer
        return self.analyze(incident_type, logs)
