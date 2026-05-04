import json
from analyzer import analyze_defect_escape
import os

def test_analyzer_produces_report(tmp_path):
    # Setup mock data files
    incidents_file = tmp_path / "sample_incidents.json"
    gates_file = tmp_path / "sample_gates.json"
    
    incidents_data = [{"id": "1", "service": "test-service", "severity": "High", "date": "2026-01-01"}]
    gates_data = [{"gate": "k6", "status": "pass"}]
    
    incidents_file.write_text(json.dumps(incidents_data))
    gates_file.write_text(json.dumps(gates_data))
    
    # Change CWD to handle output file
    os.chdir(tmp_path)
    
    report = analyze_defect_escape(str(incidents_file), str(gates_file))
    
    assert "analysis_date" in report
    assert "recommendations" in report
    assert len(report["recommendations"]) > 0
    assert os.path.exists("defect_escape_report.json")
