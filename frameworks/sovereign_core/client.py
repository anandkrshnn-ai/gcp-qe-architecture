"""
Sovereign Core: The Generalizable Architectural Simulator (PoC).
Features a Pattern Registry for multi-incident analysis.
"""

import os
import json
import logging
from typing import List, Dict, Optional

logger = logging.getLogger("SovereignCore")

class SovereignClient:
    def __init__(self, mode: str = "simulation", project_id: str = "demo-project"):
        self.mode = mode.lower()
        self.project_id = project_id

    def fetch_logs(self, incident_type: str) -> List[Dict]:
        if self.mode == "simulation":
            return self._fetch_simulation_logs(incident_type)
        return self._fetch_production_logs(incident_type)

    def _fetch_simulation_logs(self, incident_type: str) -> List[Dict]:
        path = f"data/incidents/{incident_type}_event.json"
        if not os.path.exists(path):
            return []
        with open(path, "r") as f:
            return json.load(f)

    def _fetch_production_logs(self, incident_type: str) -> List[Dict]:
        """REAL SDK Implementation (Requires Credentials)."""
        try:
            from google.cloud import logging_v2
            client = logging_v2.Client(project=self.project_id)
            # Map incident types to real GCP filters
            filters = {
                "oomkill": 'resource.type="gke_container" AND jsonPayload.reason="OOMKilling"',
                "latency": 'resource.type="cloud_run_revision" AND severity="ERROR" AND jsonPayload.message:"DeadlineExceeded"'
            }
            entries = client.list_entries(filter_=filters.get(incident_type, ""))
            return [entry.to_dict() for entry in entries]
        except ImportError:
            raise RuntimeError("Missing 'google-cloud-logging' dependency.")
        except Exception as e:
            raise RuntimeError(f"GCP SDK Error: {e}")

class SovereignAnalyzer:
    """Generalizable Analyzer using a Pattern Registry."""
    def __init__(self):
        self.registry = {
            "oomkill": self._detect_oomkill,
            "latency": self._detect_latency
        }

    def analyze(self, incident_type: str, logs: List[Dict]) -> Dict:
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
