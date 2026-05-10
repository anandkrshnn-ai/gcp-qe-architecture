import pytest
import os
import json
from sovereign_core import SovereignClient, SovereignAnalyzer, SovereignActuator, VertexAIAnalyzer

def test_client_simulation_mode():
    """Verify the client correctly loads simulation data."""
    client = SovereignClient(mode="simulation")
    logs = client.fetch_logs("oomkill")
    assert isinstance(logs, list)
    assert len(logs) > 0
    assert "jsonPayload" in logs[0]

def test_analyzer_deterministic_oomkill():
    """Verify the deterministic analyzer catches OOMKill patterns."""
    analyzer = SovereignAnalyzer()
    mock_logs = [{"jsonPayload": {"message": "Pod OOMKilling"}}]
    analysis = analyzer.analyze("oomkill", mock_logs)
    assert analysis["root_cause"] == "Pod OOMKill"
    assert analysis["confidence"] == 0.95

def test_analyzer_deterministic_latency():
    """Verify the deterministic analyzer catches Latency patterns."""
    analyzer = SovereignAnalyzer()
    mock_logs = [{"jsonPayload": {"message": "DeadlineExceeded"}}]
    analysis = analyzer.analyze("latency", mock_logs)
    assert analysis["root_cause"] == "Service Timeout (60s)"
    assert analysis["confidence"] == 0.92

def test_vertex_ai_analyzer_fallback():
    """Verify VertexAIAnalyzer falls back to deterministic when SDK/Creds missing."""
    analyzer = VertexAIAnalyzer(project_id="non-existent-project")
    mock_logs = [{"jsonPayload": {"message": "Pod OOMKilling"}}]
    # This should trigger the fallback logic
    analysis = analyzer.analyze_with_llm("oomkill", mock_logs)
    assert analysis["root_cause"] == "Pod OOMKill"

def test_actuator_dry_run():
    """Verify the actuator generates the correct commands in dry-run mode."""
    actuator = SovereignActuator(dry_run=True)
    assert actuator.execute("oomkill", target="test-cluster") is True
    assert actuator.execute("latency", target="test-service") is True

def test_actuator_invalid_type():
    """Verify handling of unknown remediation types."""
    actuator = SovereignActuator()
    assert actuator.execute("unknown-type") is False
