import hashlib
import json
import time
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

class Finding(BaseModel):
    """Honest representation of an incident finding."""
    incident_id: str
    incident_type: str
    severity: str
    timestamp: float = Field(default_factory=time.time)
    metadata: Dict[str, Any] = {}
    proposed_remediation: Dict[str, Any]

IncidentResolution = Finding

class VertexAIAnalyzer:
    """
    Deterministic Log Analyzer with RSA signing capability.
    VertexAI integration is simulated for PoC portability.
    """
    
    # Standardized patterns for deterministic detection
    PATTERNS = {
        "oomkill": {
            "keywords": ["OOMKilling", "Out of memory", "terminated with 137"],
            "remediation": {"operation": "SCALE_UP", "replicas": 2},
            "severity": "CRITICAL"
        },
        "latency_spike": {
            "keywords": ["DeadlineExceeded", "Request timeout", "504 Gateway Timeout"],
            "remediation": {"operation": "SCALE_UP", "replicas": 1},
            "severity": "HIGH"
        },
        "storage_full": {
            "keywords": ["No space left on device", "Disk full"],
            "remediation": {"operation": "ALERT_ONLY", "action": "CLEANUP_TEMP"},
            "severity": "HIGH"
        }
    }

    def __init__(self, agent_id: str, private_key: rsa.RSAPrivateKey):
        self.agent_id = agent_id
        self._private_key = private_key

    def analyze_logs(self, logs: List[Dict[str, Any]]) -> List[Finding]:
        """
        Parses logs and returns a list of identified findings.
        """
        findings = []
        for log in logs:
            msg = str(log.get("jsonPayload", {}).get("message", ""))
            for incident_type, config in self.PATTERNS.items():
                if any(k in msg for k in config["keywords"]):
                    findings.append(Finding(
                        incident_id=hashlib.sha1(msg.encode()).hexdigest()[:8],
                        incident_type=incident_type,
                        severity=config["severity"],
                        proposed_remediation=config["remediation"],
                        metadata={"raw_log_snippet": msg[:100]}
                    ))
        return findings

    def sign_finding(self, finding: Finding) -> Dict[str, Any]:
        """
        Signs a finding to produce an attested signature for consensus.
        """
        finding_data = finding.model_dump()
        finding_json = json.dumps(finding_data, sort_keys=True)
        finding_hash = hashlib.sha256(finding_json.encode()).hexdigest()
        
        signature = self._private_key.sign(
            finding_hash.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        return {
            "agent_id": self.agent_id,
            "signature_hex": signature.hex(),
            "timestamp": time.time(),
            "finding": finding_data
        }
