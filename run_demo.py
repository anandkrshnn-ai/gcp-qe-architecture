"""
Sovereign-GCP: The 30-Second Executable Demo.
Final Version: Observe -> Orient -> Decide -> Act (Closed Loop)
"""

import sys
import os
import time

# Ensure the 'src' directory is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from sovereign_core import SovereignClient, SovereignAnalyzer, VertexAIAnalyzer, SovereignActuator

def run_demo(incident_type="oomkill", mode="deterministic"):
    print("=" * 60)
    print(f"SOVEREIGN-GCP SIMULATOR: {incident_type.upper()} CLOSED-LOOP")
    print(f"REASONING MODE: {mode.upper()}")
    print("=" * 60)
    
    # 1. Initialize OODA Components
    client = SovereignClient(mode="simulation")
    actuator = SovereignActuator(dry_run=True)
    
    if mode == "reasoning":
        analyzer = VertexAIAnalyzer()
    else:
        analyzer = SovereignAnalyzer()
    
    # --- OBSERVE ---
    print("[*] STEP 1: Observing Telemetry...")
    logs = client.fetch_logs(incident_type)
    if not logs:
        print(f"[ERROR] No data found for {incident_type}")
        return
    time.sleep(0.5)

    # --- ORIENT & DECIDE ---
    print("[*] STEP 2: Analyzing Root Cause...")
    if mode == "reasoning":
        analysis = analyzer.analyze_with_llm(incident_type, logs)
    else:
        analysis = analyzer.analyze(incident_type, logs)
    
    time.sleep(0.5)
    print("-" * 60)
    print(f"DIAGNOSIS:  {analysis['root_cause']}")
    print(f"CONFIDENCE: {analysis['confidence'] * 100}%")
    print(f"PROPOSED:   {analysis['remediation']}")
    print("-" * 60)

    # --- ACT (Human-in-the-Loop) ---
    print("\n[*] STEP 3: Action Required")
    # Simulate HITL for the demo
    choice = "y" # In a real interactive session, we would use input()
    print(f"Execute remediation on target-service? [y/N]: {choice}")
    
    if choice.lower() == 'y':
        print("[*] STEP 4: Executing Remediation...")
        actuator.execute(incident_type, target="gke-prod-cluster" if incident_type == "oomkill" else "cloud-run-prod")
    else:
        print("[!] Action Cancelled.")

    print("\n[SUCCESS] Closed-Loop OODA cycle complete.")
    print("=" * 60)

if __name__ == "__main__":
    scenario = sys.argv[1] if len(sys.argv) > 1 else "oomkill"
    mode = "reasoning" if "--reasoning" in sys.argv else "deterministic"
    run_demo(scenario, mode)
