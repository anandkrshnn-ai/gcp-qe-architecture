import pytest
from analyzer import analyze_defect_escape
import os
import json

def test_analyze_defect_escape(tmp_path):
    # Setup mock data
    incidents_file = tmp_path / "incidents.json"
    gates_file = tmp_path / "gates.json"
    
    incidents_file.write_text(json.dumps([{"id": "1", "service": "test", "severity": "High", "date": "2026-01-01"}]))
    gates_file.write_text(json.dumps([{"gate": "test", "status": "pass"}]))
    
    # Change CWD to tmp_path to handle output file
    os.chdir(tmp_path)
    
    report = analyze_defect_escape(str(incidents_file), str(gates_file))
    
    assert report["total_incidents"] == 1
    assert "common_gaps" in report
    assert os.path.exists("defect_escape_report.json")
