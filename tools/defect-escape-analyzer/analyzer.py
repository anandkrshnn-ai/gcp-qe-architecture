import argparse
import json

def analyze_defects(defect_log_path, quality_gates_path):
    """
    Correlates production defects to gaps in automated quality gates.
    """
    print(f"--- Defect Escape Analyzer ---")
    
    with open(defect_log_path, 'r') as f:
        defects = json.load(f)
    
    with open(quality_gates_path, 'r') as f:
        gates = json.load(f)
    
    analysis = []
    
    for defect in defects:
        # Simple heuristic: find if the defect category matches a gate
        missed_gate = "Unknown (Add manual gate)"
        for gate in gates:
            if gate['category'].lower() in defect['description'].lower():
                missed_gate = gate['name']
                break
        
        analysis.append({
            "defect_id": defect['id'],
            "severity": defect['severity'],
            "probable_root_cause": defect['description'],
            "missed_quality_gate": missed_gate
        })
    
    return analysis

if __name__ == "__main__":
    # Mock data for demonstration
    mock_defects = [
        {"id": "DEF-001", "severity": "High", "description": "Memory leak in payment-api under high load"},
        {"id": "DEF-002", "severity": "Critical", "description": "SQL injection vulnerability in login form"}
    ]
    
    mock_gates = [
        {"name": "k6 Load Test", "category": "load"},
        {"name": "Snyk Security Scan", "category": "vulnerability"},
        {"name": "Unit Tests", "category": "logic"}
    ]
    
    print("Analyzing mock data...")
    # In a real scenario, these would be loaded from files
    # results = analyze_defects('defects.json', 'gates.json')
    
    # Simulating analysis for display
    print("\n[Analysis Report]")
    print("-" * 30)
    for d in mock_defects:
        gate = "Unknown"
        for g in mock_gates:
            if g['category'].lower() in d['description'].lower():
                gate = g['name']
        print(f"ID: {d['id']} | Severity: {d['severity']}")
        print(f"Cause: {d['description']}")
        print(f"Missed Gate: {gate}")
        print("-" * 30)
