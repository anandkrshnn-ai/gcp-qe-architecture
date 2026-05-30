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

from safety.analyzer import VertexAIAnalyzer, Finding
from safety.remediator import DryRunRemediator
from safety.security import RuntimeSecurity
from safety.voting import VotingValidator
from safety.safety_gate import SafetyGate, SafetyConfig

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("SafetyDemo")

def run_Safety_demo(real_mode: bool = False):
    """
    Executes end-to-end safety demo cycle for multi-agent voting.
    """
    print("\n" + "="*60)
    print(f"Agent Safety Patterns Demo {'[REAL MODE]' if real_mode else ''}")
    print("Architect Reference Implementation")
    print("="*60 + "\n")

    # 1. SETUP
    key_a = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    key_b = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    voting = VotingValidator(threshold=1.0)
    
    def get_pem(key):
        return key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    voting.register_agent("agent_alpha", get_pem(key_a))
    voting.register_agent("agent_beta", get_pem(key_b))

    safety_config = SafetyConfig(max_replicas_per_service=20)
    gate = SafetyGate(safety_config)
    remediator = DryRunRemediator(voting, gate)

    # 2. ANALYSIS
    print(f"Step 1: Ingesting logs from environment ({'REAL' if real_mode else 'SIMULATED'} mode)...")
    logs = [
        {"jsonPayload": {"message": "Critical: OOMKilling pod 'api-service-x1'"}},
    ]

    analyzer_a = VertexAIAnalyzer("agent_alpha", key_a)
    findings = analyzer_a.analyze_logs(logs, mode="real" if real_mode else "simulate")

    if not findings:
        print("[-] No findings detected.")
        return

    proposal = findings[0]
    print(f"[+] Detection: {proposal.incident_type} (Severity: {proposal.severity})")

    # 3. VOTING
    print("\nStep 2: Collecting RSA-Signed Findings from Multi-Agent Fleet...")
    analyzer_b = VertexAIAnalyzer("agent_beta", key_b)
    
    sig_a = analyzer_a.sign_finding(proposal)
    sig_b = analyzer_b.sign_finding(proposal)
    
    print(f"   [Agent Alpha] Signed Finding: {sig_a['signature_hex'][:16]}...")
    print(f"   [Agent Beta]  Signed Finding: {sig_b['signature_hex'][:16]}...")

    # 4. REMEDIATION
    print("\nStep 3: Verifying Quorum and Safety Gate Boundaries...")
    
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
    parser.add_argument("--real", action="store_true", help="Use real Vertex AI (requires GCP auth)")
    args = parser.parse_args()
    
    run_Safety_demo(real_mode=args.real)
