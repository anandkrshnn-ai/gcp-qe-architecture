import pytest
from src.sovereign_core.analyzer import SovereignAnalyzer, IncidentResolution

def test_sovereign_analyzer_pattern_match():
    analyzer = SovereignAnalyzer()
    logs = [{"textPayload": "OOMKiller: pod 'api-gateway' terminated", "timestamp": 12345}]
    
    result = analyzer.analyze("oomkill", logs)
    
    assert "Memory Exhaustion" in result["root_cause"]
    assert result["remediation"] == "scale_up_memory"
    assert result["kubectl_patch"] is not None

def test_incident_resolution_schema():
    data = {
        "root_cause": "Test Cause",
        "confidence": 0.9,
        "remediation": "test_action",
        "reasoning": "Because I said so",
        "engine": "pytest"
    }
    resolution = IncidentResolution(**data)
    assert resolution.confidence == 0.9
    assert resolution.engine == "pytest"
