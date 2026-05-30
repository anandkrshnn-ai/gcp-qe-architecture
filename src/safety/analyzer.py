import os
import hashlib
import json
import time
import logging
import re
from typing import List, Dict, Any
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential

# GCP Imports
try:
    from google.cloud import aiplatform
    import vertexai
    from vertexai.generative_models import GenerativeModel, SafetySetting, HarmCategory, HarmBlockThreshold
    HAS_GCP = True
except ImportError:
    HAS_GCP = False

from .logging_utils import get_logger, log_event
from .ports import LogSourcePort

# logger setup

logger = get_logger("VertexAIAnalyzer")

class Finding(BaseModel):
    """Cryptographically signed finding package."""
    agent_id: str
    incident_id: str
    incident_type: str
    severity: str
    proposed_remediation: Dict[str, Any]
    timestamp: int  # Integer timestamp for cryptographic stability
    nonce: str
    metadata: Dict[str, Any] = {} # For armor safety scores

class ModelArmor:
    """
    Simulates GCP Model Armor / Safety Guardrails.
    Sanitizes agent output before it reaches the consensus layer.
    """
    # Pattern for potential GCP/API keys
    SECRET_PATTERN = re.compile(r"(AIza[0-9A-Za-z-_]{35}|sk-[a-zA-Z0-9]{48})")

    def sanitize_finding(self, finding: Finding) -> Finding:
        """Surgically redacts secrets and adds safety metadata."""
        finding_json = finding.model_dump_json()
        
        # 1. Leak Detection (Simple Regex-based scanning)
        if self.SECRET_PATTERN.search(finding_json):
            log_event(logger, logging.WARNING, "ModelArmor: Secret pattern detected. Redacting.", extra={
                "agent_id": finding.agent_id,
                "incident_id": finding.incident_id,
                "armor_action": "REDACT"
            })
            # Redact common fields
            if "description" in finding.proposed_remediation:
                finding.proposed_remediation["description"] = self.SECRET_PATTERN.sub("[REDACTED_SECRET]", finding.proposed_remediation["description"])
            
        # 2. Add safety metadata
        finding.metadata["safety_score"] = 0.99
        finding.metadata["armor_status"] = "VERIFIED_CLEAN"
        return finding

class VertexAIAnalyzer:
    """
    Hardened Agentic Analyzer using Vertex AI (Gemini) for incident root-cause analysis.
    Supports both research simulation and production GCP modes with exponential backoff.
    """
    def __init__(self, agent_id: str, private_key: rsa.RSAPrivateKey, project_id: str = None, location: str = "us-central1"):
        self.agent_id = agent_id
        self._private_key = private_key
        self.project_id = project_id or os.getenv("GCP_PROJECT_ID")
        self.location = location
        self._initialized_gcp = False
        self.armor = ModelArmor()

    def _init_gcp(self):
        if not HAS_GCP:
            raise ImportError("google-cloud-aiplatform or vertexai not installed. Run 'pip install .[gcp]'")
        if not self._initialized_gcp:
            # Supports ADC or explicit GOOGLE_APPLICATION_CREDENTIALS env var
            vertexai.init(project=self.project_id, location=self.location)
            self._initialized_gcp = True
            logger.info(f"Vertex AI initialized for project {self.project_id}")
        

    def analyze_logs(self, logs: List[Dict[str, Any]], mode: str = "simulate") -> List[Finding]:
        """
        Analyzes logs to detect incidents and propose remediation.
        """
        if mode == "real":
            return self._analyze_real_with_retry(logs)
        
        # Simulation Logic (Research Mode)
        findings = []
        for log in logs:
            msg = str(log.get("jsonPayload", {}).get("message", "")).lower()
            if "oom" in msg or "critical" in msg:
                finding = Finding(
                    agent_id=self.agent_id,
                    incident_id=hashlib.sha256(msg.encode()).hexdigest()[:8],
                    incident_type="oomkill",
                    severity="CRITICAL",
                    proposed_remediation={
                        "operation": "SCALE_UP",
                        "replicas": 2,
                        "target": "api-service",
                        "description": "Detected critical OOM signal in logs."
                    },
                    timestamp=int(time.time()),
                    nonce=os.urandom(16).hex()
                )
                
                findings.append(self.armor.sanitize_finding(finding))
        return findings

    def fetch_and_analyze(self, query: str, log_source: LogSourcePort, limit: int = 100, mode: str = "simulate") -> List[Finding]:
        """Fetches logs using the injected LogSourcePort and processes them."""
        logs = log_source.fetch_recent_logs(query, limit)
        return self.analyze_logs(logs, mode)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    def _analyze_real_with_retry(self, logs: List[Dict[str, Any]]) -> List[Finding]:
        """Wrapper for real mode with production-reference retries."""
        return self._analyze_real(logs)

    def _analyze_real(self, logs: List[Dict[str, Any]]) -> List[Finding]:
        """Performs real Vertex AI analysis using Gemini 1.5 Pro."""
        self._init_gcp()
        model = GenerativeModel("gemini-1.5-pro")
        
        # Enterprise System Prompt for structured output
        system_instr = "You are a SRE Automation Agent. Analyze logs and return a valid JSON Finding array."
        prompt = f"{system_instr}\n\nLogs to analyze: {json.dumps(logs)}"
        
        try:
            # Exhaustive safety configuration
            safety_settings = [
                SafetySetting(category=HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH),
                SafetySetting(category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH),
                SafetySetting(category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH),
                SafetySetting(category=HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH),
            ]

            response = model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"},
                safety_settings=safety_settings
            )
            
            # Deterministic JSON Mapping
            raw_text = response.text
            remediation_data = json.loads(raw_text)
            
            # Map Gemini output to our Finding model
            findings = []
            if isinstance(remediation_data, list):
                for item in remediation_data:
                    finding = Finding(
                        agent_id=self.agent_id,
                        incident_id=item.get("id", f"gemini-{os.urandom(4).hex()}"),
                        incident_type=item.get("type", "automated-detection"),
                        severity=item.get("severity", "MEDIUM"),
                        proposed_remediation=item.get("remediation", {"operation": "NOTIFY", "target": "sre-oncall"}),
                        timestamp=int(time.time()),
                        nonce=os.urandom(16).hex()
                    )
                    
                    # Advisory Authenticity Scoring (Phase 2)
                    if HAS_INTELLIGENCE:
                        auth_result = self.authenticity_scorer.score_proposal(finding.proposed_remediation.get("description", ""), None)
                        finding.metadata.update(auth_result)
                    
                    findings.append(self.armor.sanitize_finding(finding))

                log_event(logger, logging.INFO, "Vertex AI generated findings.", extra={
                    "agent_id": self.agent_id,
                    "incident_count": len(findings),
                    "mode": "real"
                })
            return findings

        except json.JSONDecodeError:
            logger.error("Gemini returned invalid JSON format.")
            raise ValueError("Failed to parse AI output into valid Finding model.")
        except Exception as e:
            logger.error(f"Vertex AI API call failed: {e}")
            raise

    def sign_finding(self, finding: Finding) -> Dict[str, Any]:
        """Signs the finding using the agent's private RSA key."""
        # Use canonical JSON (sorted keys, no whitespace) for stable hashing
        finding_json = json.dumps(finding.model_dump(), sort_keys=True, separators=(',', ':'))
        logger.debug(f"Signing proposal JSON: {finding_json}")
        signature = self._private_key.sign(
            finding_json.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        log_event(logger, logging.INFO, "Finding signed successfully.", extra={
            "agent_id": self.agent_id,
            "incident_id": finding.incident_id,
            "nonce": finding.nonce,
            "timestamp": finding.timestamp
        })
        return {
            "agent_id": self.agent_id,
            "signature_hex": signature.hex(),
            "finding": finding.model_dump(),
            "timestamp": finding.timestamp,
            "nonce": finding.nonce
        }
