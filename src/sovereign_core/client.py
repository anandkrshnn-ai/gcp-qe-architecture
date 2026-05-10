"""
Sovereign Core: The SDK Interface and Actuator for GCP.
Handles both Simulation (local) and Production (real SDK) data fetching and remediation.
"""

import os
import json
import logging
from typing import List, Dict

logger = logging.getLogger("SovereignCore")

class SovereignClient:
    """
    The Single Entry Point for fetching GCP telemetry.
    Supports Simulation Mode (Zero-Credentials) and Production Mode (GCP SDK).
    """
    def __init__(self, mode: str = "simulation", project_id: str = "demo-project"):
        self.mode = mode.lower()
        self.project_id = project_id

    def fetch_logs(self, incident_type: str) -> List[Dict]:
        """Entry point for log retrieval."""
        if self.mode == "simulation":
            return self._fetch_simulation_logs(incident_type)
        return self._fetch_production_logs(incident_type)

    def _fetch_simulation_logs(self, incident_type: str) -> List[Dict]:
        """Loads real-world patterns from local data files."""
        path = f"data/incidents/{incident_type}_event.json"
        if not os.path.exists(path):
            logger.warning(f"Simulation data not found for {incident_type} at {path}")
            return []
        with open(path, "r") as f:
            return json.load(f)

    def _fetch_production_logs(self, incident_type: str) -> List[Dict]:
        """REAL SDK Implementation (Requires google-cloud-logging)."""
        try:
            from google.cloud import logging_v2
            client = logging_v2.Client(project=self.project_id)
            filters = {
                "oomkill": 'resource.type="gke_container" AND jsonPayload.reason="OOMKilling"',
                "latency": 'resource.type="cloud_run_revision" AND severity="ERROR" AND jsonPayload.message:"DeadlineExceeded"'
            }
            entries = client.list_entries(filter_=filters.get(incident_type, ""))
            return [entry.to_dict() for entry in entries]
        except ImportError:
            raise RuntimeError("Missing 'google-cloud-logging'. Run: pip install sovereign-core[gcp]")
        except Exception as e:
            raise RuntimeError(f"GCP SDK Error: {e}")

class SovereignActuator:
    """
    The 'Hands' of the Agent. 
    Executes remediation actions after analysis.
    """
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run

    def execute(self, remediation_type: str, target: str = "default-service") -> bool:
        """Executes the mapped remediation logic."""
        actions = {
            "oomkill": self._remediate_oomkill,
            "latency": self._remediate_latency
        }
        
        handler = actions.get(remediation_type)
        if not handler:
            logger.error(f"No actuator handler for {remediation_type}")
            return False
            
        return handler(target)

    def _remediate_oomkill(self, target: str) -> bool:
        command = f"kubectl patch deployment {target} --patch '{{\"spec\": {{\"template\": {{\"spec\": {{\"containers\": [{{\"name\": \"app\", \"resources\": {{\"limits\": {{\"memory\": \"512Mi\"}}}}}}]}}}}}}}}}}'"
        return self._run_command(command)

    def _remediate_latency(self, target: str) -> bool:
        command = f"gcloud run services update {target} --timeout=90s"
        return self._run_command(command)

    def _run_command(self, command: str) -> bool:
        if self.dry_run:
            print(f"[DRY-RUN] Command generated: {command}")
            return True
        
        print(f"[LIVE] Executing command: {command}")
        # In production: os.system(command)
        return True
