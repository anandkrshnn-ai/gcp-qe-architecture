import pytest

pytestmark = pytest.mark.pre_actuation
import time
import os
import hashlib
import json
from cryptography.hazmat.primitives.asymmetric import rsa
from safety.voting import VotingValidator, AgentSignature, ValidationError
from safety.analyzer import VertexAIAnalyzer, Finding, ModelArmor

@pytest.fixture
def keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

@pytest.fixture
def validator(keys):
    _, pub = keys
    import cryptography.hazmat.primitives.serialization as serialization
    pub_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    v = VotingValidator(threshold=1.0) # Require absolute quorum for audit
    v.register_agent("agent_alpha", pub_pem)
    return v

def test_adversarial_replay_attack(validator, keys):
    """FAIL CASE: Reusing a nonce should be blocked."""
    priv, _ = keys
    analyzer = VertexAIAnalyzer("agent_alpha", priv)
    
    finding = Finding(
        agent_id="agent_alpha",
        incident_id="attack-001",
        incident_type="oom",
        severity="HIGH",
        proposed_remediation={"operation": "SCALE_UP", "target": "api"},
        timestamp=int(time.time()),
        nonce="constant-nonce"
    )
    
    signed = analyzer.sign_finding(finding)
    sig_obj = AgentSignature(**signed)
    
    # First submission - should pass
    validator.verify_quorum({"id": "attack-001"}, [sig_obj])
    
    # Second submission with same nonce - should fail
    # Note: verify_quorum doesn't raise, it returns proof.
    # But in our implementation, if any signature fails verification (like replay), it's excluded.
    proof = validator.verify_quorum({"id": "attack-001"}, [sig_obj])
    assert proof.quorum_reached is False
    assert len(proof.signatures) == 0
 
def test_adversarial_clock_skew(validator, keys):
    """FAIL CASE: Proposal from the distant past should be blocked."""
    priv, _ = keys
    analyzer = VertexAIAnalyzer("agent_alpha", priv)
    
    # 1 hour in the past
    stale_time = int(time.time()) - 3600
    
    finding = Finding(
        agent_id="agent_alpha",
        incident_id="stale-001",
        incident_type="oom",
        severity="HIGH",
        proposed_remediation={"operation": "SCALE_UP", "target": "api"},
        timestamp=stale_time,
        nonce=os.urandom(16).hex()
    )
    
    signed = analyzer.sign_finding(finding)
    sig_obj = AgentSignature(**signed)
    
    proof = validator.verify_quorum({"id": "stale-001"}, [sig_obj])
    assert proof.quorum_reached is False
 
def test_adversarial_unauthorized_key(validator):
    """FAIL CASE: Signature from a non-registered key should be rejected."""
    attacker_priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    analyzer = VertexAIAnalyzer("agent_alpha", attacker_priv) # Using legitimate ID but wrong key
    
    finding = Finding(
        agent_id="agent_alpha",
        incident_id="forgery-001",
        incident_type="oom",
        severity="HIGH",
        proposed_remediation={"operation": "SCALE_UP", "target": "api"},
        timestamp=int(time.time()),
        nonce=os.urandom(16).hex()
    )
    
    signed = analyzer.sign_finding(finding)
    sig_obj = AgentSignature(**signed)
    
    proof = validator.verify_quorum({"id": "forgery-001"}, [sig_obj])
    assert proof.quorum_reached is False

def test_model_armor_nested_leak_prevention():
    """SUCCESS CASE: Model Armor must redact secrets even in nested fields."""
    armor = ModelArmor()
    fake_key = "AIzaSyB-R-9_V0L-1-2-3-4-5-6-7-8-9-0-1-2"
    
    finding = Finding(
        agent_id="agent_alpha",
        incident_id="leak-001",
        incident_type="oom",
        severity="HIGH",
        proposed_remediation={
            "operation": "NOTIFY",
            "target": "slack",
            "description": f"Urgent: Use key {fake_key} to fix."
        },
        timestamp=int(time.time()),
        nonce="nonce-1"
    )
    
    sanitized = armor.sanitize_finding(finding)
    description = sanitized.proposed_remediation["description"]
    assert fake_key not in description
    assert "[REDACTED_SECRET]" in description
    assert sanitized.metadata["armor_status"] == "VERIFIED_CLEAN"
