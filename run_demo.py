# run_demo.py
import sys
import os
import argparse
import logging
from typing import Dict, List
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# FIXED IMPORTS - Use safety_core
from safety_core.analyzer import VertexAIAnalyzer, IncidentResolution
from safety_core.remediator import DryRunRemediator
from safety_core.security import RuntimeSecurity
from safety_core.chaos import ChaosSimulator
from safety_core.consensus import ConsensusGuardian
from safety_core.safety_gate import SafetyGate, SafetyConfig

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("SafetyDemo")

def run_sovereign_demo(chaos_mode: bool = False):
    """
    Executes end-to-end safety demo cycle for multi-agent consensus.
    """
    print("\n" + "="*60)
    print(f"Agent Safety Demo v7.0.0 {'[CHAOS MODE]' if chaos_mode else ''}")
    print("Research Proof of Concept")
    print("="*60 + "\n")

    # 1. SETUP
    key_a = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    key_b = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    guardian = ConsensusGuardian(threshold=1.0)
    
    def get_pem(key):
        return key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    guardian.register_agent("agent_alpha", get_pem(key_a))
    guardian.register_agent("agent_beta", get_pem(key_b))

    safety_config = SafetyConfig(max_replicas_per_service=5)
    gate = SafetyGate(safety_config)
    remediator = DryRunRemediator(guardian, gate)

    # 2. ANALYSIS
    print("Step 1: Ingesting logs from environment...")
    logs = [
        {"jsonPayload": {"message": "Critical: OOMKilling pod 'api-service-x1'"}},
    ]
    
    if chaos_mode:
        simulator = ChaosSimulator(failure_rate=1.0)
        logs = simulator.inject_telemetry_corruption(logs)

    analyzer_a = VertexAIAnalyzer("agent_alpha", key_a)
    findings = analyzer_a.analyze_logs(logs)

    if not findings:
        print("[-] No findings detected (or blocked by safety/chaos).")
        return

    proposal = findings[0]
    print(f"[+] Detection: {proposal.incident_type} (Severity: {proposal.severity})")

    # 3. CONSENSUS
    print("\nStep 2: Collecting RSA-Signed Findings from Multi-Agent Fleet...")
    analyzer_b = VertexAIAnalyzer("agent_beta", key_b)
    
    sig_a = analyzer_a.sign_finding(proposal)
    sig_b = analyzer_b.sign_finding(proposal)
    
    print(f"   [Agent Alpha] Signed Finding: {sig_a['signature_hex'][:16]}...")
    print(f"   [Agent Beta]  Signed Finding: {sig_b['signature_hex'][:16]}...")

    # 4. REMEDIATION
    print("\nStep 3: Verifying Consensus and Safety Gate Boundaries...")
    
    result = remediator.process_proposal(
        sig_a["finding"], 
        [sig_a, sig_b]
    )

    if result.success:
        print(f"[+] REMEDIATION APPROVED: {result.message}")
    else:
        print(f"[-] REMEDIATION BLOCKED: {result.message}")

    print("\n" + "="*60)
    print("FINISHED: Demo cycle completed successfully.")
    print("="*60 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--real", action="store_true", help="Use real Vertex AI (planned)")
    parser.add_argument("--chaos", action="store_true", help="Run with simulated telemetry corruption")
    args = parser.parse_args()
    
    run_sovereign_demo(chaos_mode=args.chaos)
