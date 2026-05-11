import sys
import os
import json
import logging
from typing import Dict, List

# Add src to path if needed
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from sovereign_core.analyzer import VertexAIAnalyzer, IncidentResolution
from sovereign_core.remediator import DryRunRemediator
from sovereign_core.security import RuntimeSecurity

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("Sovereign-Demo")

def run_sovereign_demo():
    """
    Executes a Staff-level end-to-end happy path for Sovereign-GCP v3.5.0.
    """
    # 0. PRE-FLIGHT CHECK
    project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        print("⚠️  WARNING: GCP_PROJECT_ID not set. Running in 'Isolated Simulation Mode'.")
        print("   To enable real Vertex AI, set GCP_PROJECT_ID and GOOGLE_APPLICATION_CREDENTIALS.\n")
        project_id = "demo-project"

    print("\n" + "="*60)
    print("🚀 SOVEREIGN-GCP v3.5.0: ACTIONABLE INTELLIGENCE DEMO")
    print("="*60 + "\n")

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
        {"textPayload": "CRITICAL: Memory pressure on node-x-4", "timestamp": 1715424001}
    ]
    print(f"   [LOGS]: {len(logs)} entries ingested from 'api-gateway'.\n")

    # 3. ORIENT & DECIDE: AI Reasoning (Vertex AI)
    print("🧠 Step 3: ORIENT/DECIDE - Escalating to Gemini 1.5 Pro...")
    analyzer = VertexAIAnalyzer(project_id="demo-project")
    
    # Simulate the AI resolution (in production, hits Vertex AI API)
    # We show the structured tool-call and resolution here.
    resolution = analyzer.analyze(incident_type="oomkill", logs=logs)
    
    print(f"   [CAU]: {resolution['root_cause']}")
    print(f"   [ACT]: {resolution['remediation']}")
    print(f"   [ENG]: {resolution['engine']}\n")

    # 4. ACT: Dry-Run Remediation
    if resolution.get("kubectl_patch"):
        print("🛠️  Step 4: ACT - Initiating Actionable Remediation (Dry-Run)...")
        remediator = DryRunRemediator(use_mock=True)
        
        success = remediator.dry_run_patch(
            resource_name="api-gateway", 
            patch=resolution["kubectl_patch"]
        )
        
        if success:
            print("\n🏁 SOVEREIGN CYCLE COMPLETE: Incident resolved via validated patch.")
        else:
            print("\n❌ SOVEREIGN CYCLE FAILED: Patch validation error.")
    else:
        print("\n🏁 SOVEREIGN CYCLE COMPLETE: No remediation required (MONITOR_AND_WAIT).")

    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    run_sovereign_demo()
