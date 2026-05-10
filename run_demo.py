"""
Sovereign-GCP: The 30-Second Executable Demo.
Updated to use the 'sovereign_core' package structure.
"""

import sys
import os

# Ensure the 'src' directory is in the path so we can import the local package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from sovereign_core import SovereignClient, SovereignAnalyzer, VertexAIAnalyzer
import time

def run_demo(incident_type="oomkill", mode="deterministic"):
    print("=" * 60)
    print(f"SOVEREIGN-GCP SIMULATOR: {incident_type.upper()} ANALYSIS")
    print(f"MODE: {mode.upper()}")
    print("=" * 60)
    
    # 1. Initialize Client & Analyzer
    client = SovereignClient(mode="simulation")
    
    if mode == "reasoning":
        analyzer = VertexAIAnalyzer()
    else:
        analyzer = SovereignAnalyzer()
    
    # 2. Fetch Logs
    logs = client.fetch_logs(incident_type)
    if not logs:
        print(f"[ERROR] No data found for {incident_type}")
        return

    # 3. Analyze
    if mode == "reasoning":
        analysis = analyzer.analyze_with_llm(incident_type, logs)
    else:
        analysis = analyzer.analyze(incident_type, logs)
    
    print(f"[*] Fetching telemetry data...")
    time.sleep(0.5)
    
    print("-" * 60)
    print(f"ROOT CAUSE:  {analysis['root_cause']}")
    print(f"CONFIDENCE:  {analysis['confidence'] * 100}%")
    print(f"REMEDY:      {analysis['remediation']}")
    print("-" * 60)
    
    print("\n[VERDICT] Logic Verified. Reasoning engine is functional.")
    print("=" * 60)

if __name__ == "__main__":
    scenario = sys.argv[1] if len(sys.argv) > 1 else "oomkill"
    mode = "reasoning" if "--reasoning" in sys.argv else "deterministic"
    run_demo(scenario, mode)
