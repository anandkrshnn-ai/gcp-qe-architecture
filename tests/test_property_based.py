import pytest
import time
import secrets
from hypothesis import given, strategies as st
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from safety_core.consensus import ConsensusGuardian, AgentSignature
from safety_core.safety_gate import SafetyGate, SafetyConfig
from safety_core.analyzer import VertexAIAnalyzer, Finding

@pytest.fixture(scope="module")
def agent_keys():
    """Persistent keys for property tests."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_key, public_pem

@given(
    replicas=st.integers(min_value=1, max_value=100),
    scale_factor=st.floats(min_value=1.0, max_value=5.0)
)
def test_safety_gate_boundaries(replicas, scale_factor):
    """Property test for safety gate resource limits."""
    config = SafetyConfig(
        max_replicas_per_service=10,
        max_scale_factor=2.0,
        max_estimated_cost_per_remediation=50.0
    )
    gate = SafetyGate(config)
    
    proposal = {
        "operation": "SCALE_UP",
        "target": "test-svc",
        "replicas": replicas,
        "scale_factor": scale_factor
    }
    
    gate_result = gate.evaluate(proposal)
    
    # Assertions based on boundaries
    if replicas > 10 or scale_factor > 2.0 or (replicas * 0.05) > 50.0:
        assert gate_result.allowed is False
    else:
        assert gate_result.allowed is True

@given(
    nonce=st.text(min_size=1),
    timestamp_skew=st.floats(min_value=-500.0, max_value=500.0)
)
def test_consensus_replay_variants(agent_keys, nonce, timestamp_skew):
    """Property test for consensus replay protection."""
    private_key, public_pem = agent_keys
    guardian = ConsensusGuardian(threshold=0.5, max_clock_skew=30)
    guardian.register_agent("agent_1", public_pem)
    
    analyzer = VertexAIAnalyzer("agent_1", private_key)
    finding = Finding(
        agent_id="agent_1",
        incident_id="prop_test",
        incident_type="oomkill",
        severity="HIGH",
        proposed_remediation={"operation": "SCALE_UP", "replicas": 1},
        timestamp=int(time.time()),
        nonce="prop-nonce-1"
    )
    
    sig_data = analyzer.sign_finding(finding)
    
    # Inject property-generated values
    sig_data["nonce"] = nonce
    sig_data["timestamp"] = int(time.time() + timestamp_skew)
    
    sig = AgentSignature(**sig_data)
    proof = guardian.verify_quorum(sig_data["finding"], [sig])
    
    # Verification should fail if clock skew is exceeded
    if abs(timestamp_skew) > 30:
        assert proof.quorum_reached is False
    else:
        assert proof.quorum_reached is True

def test_nonce_reuse_prevention(agent_keys):
    """Explicitly verify that reusing a nonce fails."""
    private_key, public_pem = agent_keys
    guardian = ConsensusGuardian(threshold=1.0)
    guardian.register_agent("agent_1", public_pem)
    
    analyzer = VertexAIAnalyzer("agent_1", private_key)
    finding = Finding(
        agent_id="agent_1",
        incident_id="nonce_test",
        incident_type="oomkill",
        severity="H",
        proposed_remediation={"operation": "SCALE_UP", "replicas": 1},
        timestamp=int(time.time()),
        nonce="nonce-test-1"
    )
    
    sig_data = analyzer.sign_finding(finding)
    sig = AgentSignature(**sig_data)
    
    # 1. First use should pass
    proof1 = guardian.verify_quorum(sig_data["finding"], [sig])
    assert proof1.quorum_reached is True
    
    # 2. Reusing the SAME signature object (same nonce) should fail
    proof2 = guardian.verify_quorum(sig_data["finding"], [sig])
    assert proof2.quorum_reached is False
    assert len(proof2.signatures) == 0
