import pytest

pytestmark = pytest.mark.post_incident
from safety.safety_gate import SafetyGate, SafetyConfig
from safety.remediator import DryRunRemediator
from safety.voting import VotingValidator

def test_rollback_gate_on_post_actuation_failure():
    """
    Simulates a post-incident scenario:
    After applying a remediation patch, metric telemetry indicates high regression or failure.
    The rollback gate triggers a rollback action or reverts changes.
    """
    # Initialize safety configuration
    config = SafetyConfig(
        max_replicas_per_service=10,
        allowed_operations=["SCALE_UP", "RESTART", "ROLLBACK"]
    )
    gate = SafetyGate(config)
    
    # Simulate a regression telemetry metric (e.g., error rate = 95%) after remediation action
    post_remediation_telemetry = {"error_rate": 0.95, "target_service": "api-gateway"}
    
    # Decide if rollback is required based on telemetry threshold (e.g., error_rate > 0.05)
    def evaluate_rollback_condition(telemetry):
        return telemetry["error_rate"] > 0.05
    
    should_rollback = evaluate_rollback_condition(post_remediation_telemetry)
    assert should_rollback is True
    
    # Evaluate rollback operation proposal against safety gate
    rollback_proposal = {
        "operation": "ROLLBACK",
        "target": "api-gateway",
        "current_state": {"error_rate": 0.95}
    }
    
    gate_result = gate.evaluate(rollback_proposal)
    assert gate_result.allowed is True
    assert gate_result.reason == "All gates passed."

def test_unapproved_operation_rollback_blocked():
    """
    Ensures that if the rollback operation uses an unapproved procedure/operation,
    it is safely blocked by the Safety Gate.
    """
    config = SafetyConfig(
        allowed_operations=["SCALE_UP", "RESTART"] # ROLLBACK not allowed in this config
    )
    gate = SafetyGate(config)
    
    rollback_proposal = {
        "operation": "ROLLBACK",
        "target": "api-gateway"
    }
    
    gate_result = gate.evaluate(rollback_proposal)
    assert gate_result.allowed is False
    assert "not in the approved safety allow-list" in gate_result.reason
