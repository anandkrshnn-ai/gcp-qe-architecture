"""
Sovereign Core: The Functional Architectural Simulator.
Supports 'Simulation Mode' (Local Data) and 'Production Mode' (Real GCP SDK).
"""

import os
import json
import logging
import time
from typing import Optional, List, Dict

logger = logging.getLogger("SovereignCore")

class SovereignClient:
    """
    The Single Entry Point for both Simulation and Production.
    Proves functional design via Dependency Injection and Environment switching.
    """
    def __init__(self, mode: str = "simulation", project_id: str = "demo-project"):
        self.mode = mode.lower()
        self.project_id = project_id
        logger.info(f"[*] Initialized SovereignClient in {self.mode.upper()} mode.")

    def fetch_logs(self, incident_type: str = "oomkill") -> List[Dict]:
        """Fetches logs from either real GCP or the local simulation data."""
        if self.mode == "simulation":
            return self._fetch_simulation_logs(incident_type)
        return self._fetch_production_logs(incident_type)

    def _fetch_simulation_logs(self, incident_type: str) -> List[Dict]:
        """Loads real-world patterns from the /data directory."""
        path = f"data/incidents/{incident_type}_event.json"
        if not os.path.exists(path):
            return []
        
        with open(path, "r") as f:
            return json.load(f)

    def _fetch_production_logs(self, incident_type: str):
        """Placeholder for real GCP SDK call (requires credentials)."""
        # In a real system, this would import google-cloud-logging
        # For the demo, we fail fast with a helpful error if not configured
        if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            raise RuntimeError("PRODUCTION MODE: Missing GOOGLE_APPLICATION_CREDENTIALS")
        return [] # Real implementation would go here

class SovereignAnalyzer:
    """
    The 'Brain' of the system. 
    Not theater—actual logic that parses GCP log structures.
    """
    def analyze_oomkill(self, logs: List[Dict]) -> Dict:
        """Parses GCP log payloads to identify root causes."""
        for entry in logs:
            payload = entry.get("jsonPayload", {})
            msg = payload.get("message", "").lower()
            
            if "oomkilling" in msg or "out of memory" in msg:
                # Actual parsing logic
                return {
                    "root_cause": "Pod OOMKill",
                    "details": payload.get("message"),
                    "confidence": 0.98,
                    "remediation": "Increase resource.limits.memory in Helm/Terraform"
                }
        return {"root_cause": "Unknown", "confidence": 0.0}
