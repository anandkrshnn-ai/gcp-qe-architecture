"""
Sovereign Core: Incident Pattern Analyzer.
Standardizes detection across 10+ enterprise GCP incident types.
"""

import json
import logging
import re
import time
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from .security import RuntimeSecurity

class IncidentResolution(BaseModel):
    """Structured response from the Epistemic Engine."""
    root_cause: str = Field(description="The identified root cause of the incident")
    confidence: float = Field(ge=0, le=1.0, description="Confidence score in the diagnosis")
    remediation: str = Field(description="The recommended remediation action")
    kubectl_patch: Optional[Dict] = Field(None, description="JSON Patch for Kubernetes remediation")
    reasoning: str = Field(description="Internal reasoning for the decision")
    engine: str = Field(description="The model or logic that produced this result")

logger = logging.getLogger("SovereignCore.Analyzer")

class SovereignTracer:
    """
    Simulates OpenTelemetry Tracing for the OODA loop.
    In production, this exports OTLP spans to Google Cloud Trace.
    """
    def __init__(self):
        self.trace_id = f"tr-{int(time.time())}"
        self.spans = []

    def start_span(self, name: str):
        logger.info(f"[TRACE] Start Span: {name} (ID: {self.trace_id})")
        self.spans.append({"name": name, "start": time.time()})

    def end_span(self, name: str):
        for span in self.spans:
            if span["name"] == name:
                span["end"] = time.time()
                duration = (span["end"] - span["start"]) * 1000
                logger.info(f"[TRACE] End Span: {name} ({duration:.2f}ms)")

class SovereignAnalyzer:
    """
    Base analyzer with DeepScrub PII protection and OODA Tracing.
    """

    def __init__(self, security: Optional[RuntimeSecurity] = None):
        self.security = security or RuntimeSecurity()
        self.tracer = SovereignTracer()
        self.patterns = {
            "oomkill": ["OOMKiller", "OOMKilling", "Memory limit reached", "exit code 137"],
            "latency": ["request_latency", "slow_query", "timeout", "DeadlineExceeded"],
            "dns_fail": ["NXDOMAIN", "DNS_PROBE_FINISHED", "Could not resolve host"],
            "quota_exceeded": ["QUOTA_EXCEEDED", "Rate limit reached", "429 Too Many Requests"],
            "iam_denied": ["PermissionDenied", "AccessDenied", "Required 'iam.permissions.get'"],
            "storage_full": ["No space left on device", "disk full", "Storage quota reached"],
            "db_fail": ["Connection refused", "Deadlock found", "Database is in recovery mode"],
            "cert_expired": ["CERT_HAS_EXPIRED", "SSL certificate error", "Handshake failed"],
        }
        # Sensitive keys for DeepScrub
        self.sensitive_keys = ["PASSWORD", "API_KEY", "SSN", "SECRET", "TOKEN", "AUTH"]

    def _deep_scrub(self, data: Any) -> Any:
        """Recursively scrubs sensitive keys from dictionaries and strings."""
        if isinstance(data, dict):
            return {k: self._deep_scrub(v) if k.upper() not in self.sensitive_keys else "<SENSITIVE_KEY_REDACTED>" for k, v in data.items()}
        elif isinstance(data, list):
            return [self._deep_scrub(i) for i in data]
        elif isinstance(data, str):
            # Still use regex for IP/Email in strings
            text = re.sub(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", "<IP_REDACTED>", data)
            text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "<EMAIL_REDACTED>", text)
            return text
        return data

    def analyze(self, incident_type: str, logs: List[Dict], audit_logs: Optional[List[Dict]] = None) -> Dict:
        """
        Wave 8: Byzantine Quorum & Force-Sync Reconciliation.
        """
        self.tracer.start_span("orient_analysis")
        
        # 1. TEMPORAL PARADOX (Loophole #1 & #14: Clock Skew)
        # Loophole #14: Reject logs with >5m skew to prevent temporal leaks.
        now = time.time()
        max_skew = 300 
        for log in logs:
            if abs(now - log.get("timestamp", now)) > max_skew:
                logger.error("[CRITICAL] Loophole #14: Temporal Paradox (Clock Skew > 5m). FREEZING OBSERVATION.")
                return {"root_cause": "TEMPORAL_PARADOX", "conflict": 1.0, "remediation": "FREEZE_ENGINE"}

        # 2. BLIND-PERIOD RECONCILIATION (Loophole #1: Clock Drift Massacre)
        meta = self.store.get_resource_metadata("pipeline")
        skew_history = meta.get("skew_counts", 0)
        if skew_history >= 10: 
            logger.warning("[BYZANTINE] Blind Period Detected. Triggering FORCE_SYNC against GCP Resource APIs.")
            return {"root_cause": "BLIND_SYNC", "remediation": "FORCE_SYNC_RESOURCE_API"}

        # 3. QUORUM VERIFICATION (Loophole #4 & #10: Telemetry Blinding)
        # We require Quorum between Logs, Metrics, and Audit Logs.
        aligned_logs = [l for l in logs if l.get("timestamp", time.time()) >= (now - 60)]
        
        matches = [log["pattern"] for log in aligned_logs if "pattern" in log]
        audit_matches = [audit["pattern"] for audit in (audit_logs or []) if "pattern" in audit]
        
        # Loophole #10: Multi-source freeze trigger confirmation.
        if "ZONE_DOWN" in matches and not (audit_logs and any("ZONE_DOWN" in a["pattern"] for a in audit_logs)):
            logger.error("[BYZANTINE] Loophole #10: Falsified Zone Failure Detected. Rejecting Freeze.")
            return {"root_cause": "FALSIFIED_TELEMETRY", "conflict": 1.0, "remediation": "MONITOR_AND_WAIT"}

        # 4. PREDICTION FEEDBACK (Loophole #9: Closing the OODA Loop)
        prediction = meta.get("last_prediction", {})
        if prediction:
            actual_delta = self._calculate_delta(incident_type, aligned_logs)
            if actual_delta < prediction.get("expected_min_delta", 0):
                logger.error("[REASONING] Loophole #9: Remediation Ineffective.")
                return {"root_cause": "REMEDIATION_INEFFECTIVE", "conflict": 0.9, "remediation": "ESCALATE_CRITICAL"}

        self.store.update_resource_status("pipeline", "HEALTHY", {"skew_counts": 0})
        return {
            "root_cause": matches[0] if matches else "Unknown",
            "confidence": 0.9,
            "remediation": self._map_to_remediation(matches[0]) if matches else "MONITOR_AND_WAIT"
        }

    def _calculate_delta(self, incident: str, logs: List[Dict]) -> float:
        """Simulates delta calculation for prediction feedback."""
        return 0.4 # Simulated 40% improvement

        matches = []
        for log in logs:
            scrubbed_log = self._deep_scrub(log)
            payload = str(scrubbed_log.get("jsonPayload", scrubbed_log.get("textPayload", "")))

            for pattern in self.patterns.get(incident_type, []):
                if pattern.lower() in payload.lower():
                    matches.append(pattern)

        # 1. Uncertainty Quantification (Oracle Problem)
        # If we see multiple conflicting patterns (e.g., OOM vs. Batch), increase ConflictScore.
        conflict_score = 0.0
        if len(set(matches)) > 1:
            conflict_score = 0.6  # Multiple conflicting evidence paths
        elif not matches and logs:
            conflict_score = 0.9  # Latency Skew or Stale Data
        elif not matches:
            conflict_score = 1.0  # No evidence
        
        # 2. Logic: If conflict is high, do not remediate.
        if conflict_score > 0.4:
            reason = "Uncertain / Conflicting Evidence"
            if conflict_score == 0.9: reason = "Latency Skew / Data Misalignment"
            
            logger.warning(f"[EPISTEMIC] High Uncertainty Detected ({reason}). Conflict: {conflict_score}")
            self.tracer.end_span("orient_analysis")
            return {
                "root_cause": reason,
                "confidence": 1.0 - conflict_score,
                "conflict": conflict_score,
                "remediation": "MONITOR_AND_WAIT",
                "reasoning": f"Evidence matches: {matches}"
            }

        # Deterministic mapping if low conflict
        if matches:
            result = self._map_incident(incident_type, matches[0])
            result["conflict"] = conflict_score
            result["reasoning"] = f"Single-path match: {matches[0]}"
            self.tracer.end_span("orient_analysis")
            return result

        self.tracer.end_span("orient_analysis")
        return {"root_cause": "Not Found", "confidence": 0.0, "conflict": 1.0, "remediation": "N/A"}

    def _generate_kubectl_patch(self, remediation: str) -> Optional[Dict]:
        """Generates a JSON Patch for Kubernetes resources."""
        if remediation == "scale_up_memory":
            return {"spec": {"template": {"spec": {"containers": [{"name": "app", "resources": {"limits": {"memory": "2Gi"}}}]}}}}
        if remediation == "scale_out_replicas":
            return {"spec": {"replicas": 5}}
        return None

    def _map_incident(self, incident_type: str, match: str) -> Dict:
        """Maps a pattern match to a remediation strategy and patch."""
        base = {
            "oomkill": ("Memory Exhaustion", "scale_up_memory"),
            "latency": ("Resource Contention", "scale_out_replicas"),
            "dns_fail": ("Network Resolution Failure", "restart_dns_proxy"),
        }
        
        cause, remediation = base.get(incident_type, ("Generic Failure", "MONITOR_AND_WAIT"))
        patch = self._generate_kubectl_patch(remediation)
        
        return {
            "root_cause": f"{cause} (Pattern: {match})",
            "confidence": 0.9,
            "remediation": remediation,
            "kubectl_patch": patch
        }


class GemmaAnalyzer(SovereignAnalyzer):
    """
    Simulates Local Inference (Gemma 4) running inside the VPC.
    Focuses on high-speed pattern triage and PII masking.
    """

    def analyze(self, incident_type: str, logs: List[Dict]) -> Dict:
        self.tracer.start_span("local_triage_gemma")
        logger.info("[SOVEREIGN] Initiating Security Handshake...")
        
        # Mandatory Remote Attestation Verification
        if not self.security.verify_trust_boundary():
            logger.error("[SOVEREIGN] Security Handshake FAILED. Attestation token invalid.")
            self.tracer.end_span("local_triage_gemma")
            return {
                "root_cause": "Access Denied: Attestation Failed",
                "confidence": 0.0,
                "remediation": "abort_execution",
                "engine": "Sovereign-Security-Gate"
            }
            
        logger.info("[SOVEREIGN] Security Handshake VERIFIED. Running Local Triage (Gemma)...")
        result = super().analyze(incident_type, logs)
        result["engine"] = "Gemma-4 (Local-Sovereign)"
        self.tracer.end_span("local_triage_gemma")
        return result


class VertexAIAnalyzer(SovereignAnalyzer):
    """
    Cloud-based Deep Reasoning (Gemini 1.5 Pro).
    Used for complex Root Cause Analysis (RCA).
    """

    def __init__(self, model_name: str = "gemini-1.5-pro", project_id: str = "demo-project", security: Optional[RuntimeSecurity] = None):
        super().__init__(security=security)
        self.model_name = model_name
        self.project_id = project_id
        self._initialized = False

    def _initialize_sdk(self):
        """Initializes Vertex AI if credentials are present."""
        if self._initialized:
            return True
        try:
            import vertexai
            from vertexai.generative_models import GenerativeModel
            vertexai.init(project=self.project_id, location="us-central1")
            self.model = GenerativeModel(self.model_name)
            self._initialized = True
            return True
        except Exception as e:
            logger.warning(f"Vertex AI initialization failed: {e}")
            return False

    def analyze(self, incident_type: str, logs: List[Dict]) -> Dict:
        self.tracer.start_span("cloud_rca_gemini")
        logger.info(f"[CLOUD] Escalating to {self.model_name} for RCA...")
        
        if not self._initialize_sdk():
            return super().analyze(incident_type, logs)

        # 2026 Sovereign SRE Logic: Structured Reasoning
        log_payloads = [str(l.get("jsonPayload", l.get("textPayload", ""))) for l in logs]
        
        schema = IncidentResolution.schema_json(indent=2)
        prompt = f"""
        Role: Principal GCP SRE Agent.
        Task: Analyze the following {incident_type} logs and identify the Root Cause.
        
        LOG CONTEXT:
        {json.dumps(log_payloads, indent=2)}
        
        YOU MUST RESPOND IN VALID JSON MATCHING THIS SCHEMA:
        {schema}
        """
        
        try:
            response = self.model.generate_content(prompt)
            res_text = response.text.strip()
            # Handle Markdown blocks in Gemini output
            if "```json" in res_text:
                res_text = res_text.split("```json")[1].split("```")[0].strip()
            
            # Validate with Pydantic
            result_obj = IncidentResolution.parse_raw(res_text)
            result_obj.engine = f"{self.model_name} (Sovereign-Cloud)"
            
            self.tracer.end_span("cloud_rca_gemini")
            return result_obj.dict()
        except Exception as e:
            logger.error(f"[AI] Gemini reasoning failed: {e}. Falling back to heuristics.")
            fallback = super().analyze(incident_type, logs)
            # Wrap heuristic in Pydantic for consistency
            result_obj = IncidentResolution(
                root_cause=fallback["root_cause"],
                confidence=fallback.get("confidence", 0.5),
                remediation=fallback["remediation"],
                reasoning="Heuristic fallback due to AI failure",
                engine="Heuristic-Fallback"
            )
            self.tracer.end_span("cloud_rca_gemini")
            return result_obj.dict()


class HybridSovereignAnalyzer:
    """
    Orchestrates the Hybrid Reasoning Tier.
    Triage (Local) -> Escalation (Cloud).
    """

    def __init__(self, security: Optional[RuntimeSecurity] = None):
        self.security = security or RuntimeSecurity()
        self.local_tier = GemmaAnalyzer(security=self.security)
        self.cloud_tier = VertexAIAnalyzer(security=self.security)

    def analyze(self, incident_type: str, logs: List[Dict]) -> Dict:
        """Runs the tiered reasoning OODA Loop."""
        # 1. Mandatory Sovereign Triage (Local Gemma)
        local_result = self.local_tier.analyze(incident_type, logs)

        # 2. Heuristic Escalation: If confidence is low, escalate to Cloud
        if local_result.get("confidence", 0) < 0.8:
            logger.warning("[HYBRID] Low confidence in Local Tier. Escalating to Cloud...")
            cloud_result = self.cloud_tier.analyze(incident_type, logs)
            cloud_result["escalated"] = True
            return cloud_result

        return local_result
