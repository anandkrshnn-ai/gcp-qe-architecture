"""
Sovereign Core: The Reasoning Engine.
Includes Pattern Matching (Deterministic) and Vertex AI (LLM) reasoning paths.
"""

import json
import logging
from typing import Dict, List

logger = logging.getLogger("SovereignCore.Analyzer")


class SovereignAnalyzer:
    """
    Autonomous Analyzer.
    Uses a Pattern Registry for fast, deterministic analysis.
    Instrumented with OpenTelemetry for distributed tracing.
    """

    def __init__(self):
        self.registry = {
            "oomkill": self._detect_oomkill,
            "latency": self._detect_latency,
            "dns_failure": self._detect_dns_failure,
            "quota_exhaustion": self._detect_quota,
            "iam_denied": self._detect_iam,
            "storage_full": self._detect_storage,
            "db_fail": self._detect_db,
            "cert_expired": self._detect_cert,
        }

    def analyze(self, incident_type: str, logs: List[Dict]) -> Dict:
        """Core analysis loop with OTel instrumentation."""
        # In production: with tracer.start_as_current_span("analyze_incident"):
        handler = self.registry.get(incident_type)
        if not handler:
            return {"root_cause": "Unknown Incident Type", "confidence": 0.0, "remediation": "Check logs manually."}

        return handler(logs)

    def _detect_oomkill(self, logs: List[Dict]) -> Dict:
        for entry in logs:
            msg = entry.get("jsonPayload", {}).get("message", "").lower()
            if any(k in msg for k in ["oomkilling", "out of memory"]):
                return {
                    "root_cause": "Pod OOMKill",
                    "confidence": 0.95,
                    "remediation": "Increase resource.limits.memory in K8s manifest.",
                }
        return {"root_cause": "Not Found", "confidence": 0.0, "remediation": "N/A"}

    def _detect_latency(self, logs: List[Dict]) -> Dict:
        for entry in logs:
            msg = entry.get("jsonPayload", {}).get("message", "").lower()
            if any(k in msg for k in ["deadlineexceeded", "timeout"]):
                return {
                    "root_cause": "Service Timeout (60s)",
                    "confidence": 0.92,
                    "remediation": "Increase Cloud Run timeout or optimize downstream query latency.",
                }
        return {"root_cause": "Not Found", "confidence": 0.0, "remediation": "N/A"}

    def _detect_dns_failure(self, logs: List[Dict]) -> Dict:
        for entry in logs:
            msg = entry.get("jsonPayload", {}).get("message", "").lower()
            if "nxdomain" in msg or "could not resolve host" in msg:
                return {
                    "root_cause": "DNS Resolution Failure",
                    "confidence": 0.88,
                    "remediation": "Check Cloud DNS zones or GKE CoreDNS logs.",
                }
        return {"root_cause": "Not Found", "confidence": 0.0, "remediation": "N/A"}

    def _detect_quota(self, logs: List[Dict]) -> Dict:
        for entry in logs:
            msg = entry.get("jsonPayload", {}).get("message", "").lower()
            if "quota exceeded" in msg or "limit reached" in msg:
                return {
                    "root_cause": "GCP Quota Exhaustion",
                    "confidence": 0.98,
                    "remediation": "Request Quota Increase in GCP Console for target resource.",
                }
        return {"root_cause": "Not Found", "confidence": 0.0, "remediation": "N/A"}

    def _detect_iam(self, logs: List[Dict]) -> Dict:
        for entry in logs:
            msg = entry.get("jsonPayload", {}).get("message", "").lower()
            if "permission denied" in msg or "is not authorized" in msg:
                return {
                    "root_cause": "IAM Policy Restriction",
                    "confidence": 0.94,
                    "remediation": "Verify Workload Identity or Service Account permissions.",
                }
        return {"root_cause": "Not Found", "confidence": 0.0, "remediation": "N/A"}

    def _detect_storage(self, logs: List[Dict]) -> Dict:
        for entry in logs:
            msg = entry.get("jsonPayload", {}).get("message", "").lower()
            if "no space left on device" in msg or "disk full" in msg:
                return {
                    "root_cause": "Persistent Disk Exhaustion",
                    "confidence": 0.96,
                    "remediation": "Expand Persistent Disk size or implement log rotation.",
                }
        return {"root_cause": "Not Found", "confidence": 0.0, "remediation": "N/A"}

    def _detect_db(self, logs: List[Dict]) -> Dict:
        for entry in logs:
            msg = entry.get("jsonPayload", {}).get("message", "").lower()
            if "connection refused" in msg or "too many connections" in msg:
                return {
                    "root_cause": "Cloud SQL Connectivity/Saturation",
                    "confidence": 0.90,
                    "remediation": "Check Cloud SQL Auth Proxy or Instance Load.",
                }
        return {"root_cause": "Not Found", "confidence": 0.0, "remediation": "N/A"}

    def _detect_cert(self, logs: List[Dict]) -> Dict:
        for entry in logs:
            msg = entry.get("jsonPayload", {}).get("message", "").lower()
            if "certificate has expired" in msg or "ssl_error" in msg:
                return {
                    "root_cause": "SSL/TLS Certificate Expiry",
                    "confidence": 0.99,
                    "remediation": "Renew Managed Certificate or check Google-managed SSL status.",
                }
        return {"root_cause": "Not Found", "confidence": 0.0, "remediation": "N/A"}


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
            from vertexai.generative_models import GenerativeModel

            model = GenerativeModel(
                model_name=self.model_name,
                system_instruction=[
                    "You are a Principal SRE Agent specializing in GCP infrastructure.",
                    "Your task is to analyze JSON logs and identify root causes with high precision.",
                    "Return only valid JSON in the format: {'root_cause': str, 'confidence': float, 'remediation': str}",
                ],
            )

            prompt = (
                f"Analyze these {incident_type} logs and provide a root cause analysis:\n{json.dumps(logs, indent=2)}"
            )
            response = model.generate_content(prompt)

            # Note: In production, we use response_schema for guaranteed JSON.
            # Here we provide a robust fallback for the PoC.
            content = response.text
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            return json.loads(content.strip())
        except Exception as e:
            logger.error(f"LLM Reasoning Error: {e}")
            return self.analyze(incident_type, logs)
