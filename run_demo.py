"""
Sovereign-GCP: The Generalizable PoC Demo.
Proves multi-incident logic across real GCP structures.
"""

from frameworks.sovereign_core.client import SovereignClient, SovereignAnalyzer
import sys

def run_demo(incident_type="oomkill"):
    print("=" * 60)
    print(f"SOVEREIGN-GCP SIMULATOR: {incident_type.upper()} ANALYSIS")
    print("=" * 60)
    
    client = SovereignClient(mode="simulation")
    analyzer = SovereignAnalyzer()
    
    logs = client.fetch_logs(incident_type)
    if not logs:
        print(f"[ERROR] No data found for {incident_type}")
        return

    analysis = analyzer.analyze(incident_type, logs)
    
    print(f"[*] Analyzing {len(logs)} log entries...")
    print("-" * 60)
    print(f"ROOT CAUSE:  {analysis['root_cause']}")
    print(f"CONFIDENCE:  {analysis['confidence'] * 100}%")
    print(f"REMEDY:      {analysis['remediation']}")
    print("-" * 60)

if __name__ == "__main__":
    # Allow user to pick scenario
    scenario = sys.argv[1] if len(sys.argv) > 1 else "oomkill"
    run_demo(scenario)
    
    if scenario == "oomkill":
        print("\n[*] TIP: Try 'python run_demo.py latency' for the second scenario.")
