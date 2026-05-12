import pytest
import time
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from safety_core import (
    ConsensusGuardian, AgentSignature, SafetyGate, SafetyConfig, 
    SafetyAnalyzer, SafetyRemediator, AttestationVerifier,
    Finding
)

@pytest.fixture
def keys():
    """Generate RSA keys for testing."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_key, public_pem

def test_crypto_attestation(keys):
    """Verify RSA-based attestation works as intended."""
    private_key, public_pem = keys
    verifier = AttestationVerifier(public_pem)
    
    report = b"runtime_status_ok_v1.0"
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    
    signature = private_key.sign(
        report,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    
    assert verifier.verify_runtime_attestation(report, signature) is True
    assert verifier.verify_runtime_attestation(b"tampered", signature) is False

def test_consensus_quorum(keys):
    """Verify that ConsensusGuardian correctly calculates majority quorum."""
    private_key, public_pem = keys
    guardian = ConsensusGuardian(threshold=0.5)
    
    # Register two agents
    guardian.register_agent("agent_1", public_pem)
    guardian.register_agent("agent_2", public_pem) # Using same key for simplicity in test
    
    analyzer = SafetyAnalyzer("agent_1", private_key)
    finding_data = {
        "incident_id": "test_123",
        "incident_type": "oomkill",
        "severity": "HIGH",
        "proposed_remediation": {"operation": "SCALE_UP", "replicas": 1}
    }
    
    sig1_dict = analyzer.sign_finding(Finding(**finding_data))
    sig1 = AgentSignature(**sig1_dict)
    
    # Use the EXACT finding data that was signed
    proof = guardian.verify_quorum(sig1_dict["finding"], [sig1])
    assert proof.quorum_reached is True
    assert len(proof.signatures) == 1

def test_safety_gate_blocking():
    """Verify that SafetyGate blocks unsafe operations."""
    config = SafetyConfig(max_replicas_per_service=5, blocked_operations=["DELETE"])
    gate = SafetyGate(config)
    
    # 1. Blocked operation
    unsafe_op = {"operation": "DELETE", "target": "prod-db"}
    result = gate.validate_proposal(unsafe_op)
    assert result.is_safe is False
    assert "explicitly blocked" in result.reason
    
    # 2. Too many replicas
    high_scale = {"operation": "SCALE_UP", "replicas": 10}
    result = gate.validate_proposal(high_scale)
    assert result.is_safe is False
    assert "exceeds safety limit" in result.reason
    
    # 3. Valid operation
    safe_op = {"operation": "SCALE_UP", "replicas": 2}
    result = gate.validate_proposal(safe_op)
    assert result.is_safe is True

def test_end_to_end_pipeline(keys):
    """Verify the full pipeline from Analysis -> Consensus -> Remediation."""
    private_key, public_pem = keys
    
    # Setup
    guardian = ConsensusGuardian(threshold=1.0) # Require 100%
    guardian.register_agent("analyzer_alpha", public_pem)
    
    gate = SafetyGate(SafetyConfig())
    remediator = SafetyRemediator(guardian, gate)
    analyzer = SafetyAnalyzer("analyzer_alpha", private_key)
    
    # 1. Simulate Log Analysis
    logs = [{"jsonPayload": {"message": "Critical: OOMKilling pod-x"}}]
    findings = analyzer.analyze_logs(logs)
    assert len(findings) == 1
    
    # 2. Sign finding
    signed_finding_pkg = analyzer.sign_finding(findings[0])
    
    # 3. Process Remediation
    result = remediator.process_proposal(
        signed_finding_pkg["finding"], 
        [signed_finding_pkg]
    )
    
    assert result.success is True
    assert result.action_taken == "SCALE_UP"
    assert result.consensus_check_passed is True
    assert result.safety_check_passed is True
