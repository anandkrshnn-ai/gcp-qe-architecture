"""
Unit Tests for Sovereign SRE v2 and Core SDK.
Demonstrates 'Production Readiness' via verification.
"""

import pytest
from frameworks.sovereign_core.client import MockGCPClient, ExponentialBackoff
from frameworks.sovereign_sre-v2.orchestrator import SovereignOrchestrator

def test_mock_gcp_client_success():
    client = MockGCPClient("test-project", failure_rate=0.0)
    response = client.call_api("Compute", "instances.get", name="test-instance")
    assert response["status"] == "SUCCESS"
    assert response["data"]["name"] == "test-instance"

def test_retry_mechanism_success():
    # Test that the decorator eventually succeeds
    class Counter:
        def __init__(self):
            self.count = 0
        
        @ExponentialBackoff.retry
        def fail_twice_then_succeed(self):
            self.count += 1
            if self.count < 3:
                raise ConnectionError("Fail")
            return "Success"

    c = Counter()
    result = c.fail_twice_then_succeed()
    assert result == "Success"
    assert c.count == 3

def test_sre_orchestrator_healing_flow():
    orchestrator = SovereignOrchestrator("test-project")
    # Force high confidence diagnosis to pass
    alert = {"type": "high_latency_alert"}
    result = orchestrator.execute_healing_workflow(alert)
    assert result["status"] == "SUCCESS"

@pytest.mark.parametrize("alert_type,expected_cause", [
    ("high_latency_alert", "Memory Fragmentation"),
    ("unknown_error", "Unknown")
])
def test_diagnostic_logic(alert_type, expected_cause):
    orchestrator = SovereignOrchestrator()
    diagnosis = orchestrator._diagnose_incident({"type": alert_type})
    assert diagnosis["cause"] == expected_cause
