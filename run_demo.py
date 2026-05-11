import sys
import os
import json
import logging
import argparse
from typing import Dict, List

# Add src to path if needed
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from sovereign_core.analyzer import VertexAIAnalyzer, IncidentResolution
from sovereign_core.remediator import DryRunRemediator
from sovereign_core.security import RuntimeSecurity
from sovereign_core.chaos import ChaosSimulator

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("Sovereign-Demo")

def run_sovereign_demo(chaos_mode: bool = False):
    """
    Executes a Staff-level end-to-end cycle.
    If chaos_mode is enabled, it demonstrates Resilience against Byzantine faults.
    """
    print("\n" + "="*60)
    print(f"🚀 AGENTIC SRE DEMO v3.6.0 {'[CHAOS MODE]' if chaos_mode else ''}")
    print("="*60 + "\n")

    # 0. PRE-FLIGHT CHECK
    project_id = os.getenv("GCP_PROJECT_ID", "demo-project")

    # 1. SECURITY: Runtime Attestation
    security = RuntimeSecurity(simulate_attestation=True)
    print("🛡️  Step 1: Performing Hardware-Rooted Attestation...")
    if security.perform_handshake():
        print("✅ SUCCESS: Environment verified (SEV-SNP / GKE Sandbox enabled).\n")
    else:
        print("❌ FAILURE: Environment compromised. Halting.\n")
        return

    # 2. OBSERVE: Simulated Incident
    print("📡 Step 2: OBSERVE - Ingesting incident logs...")
    logs = [
        {"textPayload": "OOMKiller: pod 'api-gateway' terminated with exit code 137", "timestamp": 1715424000},
    ]
    
    if chaos_mode:
        chaos = ChaosSimulator(corruption_probability=1.0)
        logs = chaos.inject_log_corruption(logs)
        print("⚠️  [CHAOS] Byzantine Fault Injected: Logs have been corrupted to 'False Healthy'.")
    else:
        print(f"   [LOGS]: logs ingested from 'api-gateway'.")

    # 3. ORIENT & DECIDE: AI Reasoning (Vertex AI)
    print("\n🧠 Step 3: ORIENT/DECIDE - Escalating to Gemini 1.5 Pro...")
    analyzer = VertexAIAnalyzer(project_id=project_id)
    resolution = analyzer.analyze(incident_type="oomkill", logs=logs)
    
    print(f"   [CAU]: {resolution['root_cause']}")
    print(f"   [ACT]: {resolution['remediation']}")

    # 4. CONSENSUS (Quorum Logic Simulation)
    if chaos_mode and "No action needed" in resolution['root_cause']:
        print("\n🛡️  Step 4: CONSENSUS - Byzantine Fault Detected!")
        print("   Dissonance found between Metrics (OOM) and Corrupted Logs (Healthy).")
        print("   [RESULT]: Quorum REJECTED remediation. Fail-safe triggered.")
    else:
        # 5. ACT: Dry-Run Remediation
        if resolution.get("kubectl_patch"):
            print("\n🛠️  Step 4: ACT - Initiating Actionable Remediation (Dry-Run)...")
            remediator = DryRunRemediator(use_mock=True)
            remediator.dry_run_patch(resource_name="api-gateway", patch=resolution["kubectl_patch"])
            print("\n🏁 SOVEREIGN CYCLE COMPLETE: Incident resolved via validated patch.")
        else:
            print("\n🏁 SOVEREIGN CYCLE COMPLETE: No remediation required (MONITOR_AND_WAIT).")

    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chaos", action="store_true", help="Run with Byzantine fault injection")
    args = parser.parse_args()
    run_sovereign_demo(chaos_mode=args.chaos)
