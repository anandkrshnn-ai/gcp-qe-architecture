#!/usr/bin/env python3
import sys
import os
import time
import json
import hashlib
from typing import Dict, Any, List
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# Ensure src/ is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from safety_core.analyzer import VertexAIAnalyzer, Finding, ModelArmor
from safety_core.remediator import DryRunRemediator
from safety_core.consensus import ConsensusGuardian, AgentSignature
from safety_core.safety_gate import SafetyGate, SafetyConfig

def print_header(title: str):
    print("\n" + "=" * 80)
    print(f" {title.upper()} ".center(80, "="))
    print("=" * 80)

def main():
    print_header("GCP Verifiable AI Safety Gate - Golden Path Demo")
    print("This scenario demonstrates the end-to-end OODA safety cycle:")
    print("Anomaly Ingestion -> Model Armor Sanitization -> RSA-PSS Multi-Agent Consensus")
    print("-> Safety Gate Evaluation -> Actuation -> Post-Actuation Telemetry Regression -> Rollback")
    
    # 0. Setup Keys & Identities
    print("\n[Stage 0] Initializing Trust Anchors and Registering Agent Keys...")
    key_alpha = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    key_beta = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    def get_public_pem(key):
        return key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    guardian = ConsensusGuardian(threshold=1.0) # Require unanimous consensus
    guardian.register_agent("agent_alpha", get_public_pem(key_alpha))
    guardian.register_agent("agent_beta", get_public_pem(key_beta))

    safety_config = SafetyConfig(
        max_replicas_per_service=10,
        allowed_operations=["SCALE_UP", "RESTART", "ROLLBACK"]
    )
    gate = SafetyGate(safety_config)
    remediator = DryRunRemediator(guardian, gate)

    # 1. Ingestion
    print("\n[Stage 1] Observe: Ingesting raw telemetry signal containing sensitive API key...")
    sensitive_key = "AIzaSyB-R-9_V0L-1-2-3-4-5-6-7-8-9-0-1-2"
    raw_logs = [
        {
            "jsonPayload": {
                "message": f"Critical: OOMKilling pod 'api-service-x1'. Internal auth key used: {sensitive_key}",
                "severity": "CRITICAL"
            }
        }
    ]
    print(f"  Raw Signal: {raw_logs[0]['jsonPayload']['message']}")

    # 2. Sanitization
    print("\n[Stage 2] Orient: Applying Model Armor Sanitization & Schema Compliance...")
    armor = ModelArmor()
    analyzer_alpha = VertexAIAnalyzer("agent_alpha", key_alpha)
    findings = analyzer_alpha.analyze_logs(raw_logs, mode="simulate")
    
    if not findings:
        print("  [-] Error parsing log telemetry.")
        return
        
    sanitized_finding = armor.sanitize_finding(findings[0])
    print(f"  Sanitized Signal: {sanitized_finding.proposed_remediation['description']}")
    
    # Calculate deterministic SHA256 digest of sanitized payload
    payload_bytes = json.dumps(sanitized_finding.model_dump(), sort_keys=True).encode("utf-8")
    payload_digest = hashlib.sha256(payload_bytes).hexdigest()
    print(f"  Payload SHA256 Digest: {payload_digest}")

    # 3. Consensus Signing
    print("\n[Stage 3] Decide: Gathering RSA-PSS Quorum Attestations...")
    analyzer_beta = VertexAIAnalyzer("agent_beta", key_beta)
    
    sig_alpha = analyzer_alpha.sign_finding(sanitized_finding)
    sig_beta = analyzer_beta.sign_finding(sanitized_finding)
    
    print(f"  [Agent Alpha] Signature (RSA-PSS): {sig_alpha['signature_hex'][:32]}...")
    print(f"  [Agent Beta]  Signature (RSA-PSS): {sig_beta['signature_hex'][:32]}...")

    # 4. Actuation Evaluation
    print("\n[Stage 4] Act: Verifying Cryptographic Attestation and Safety Gate Rules...")
    remediation_proposal = sanitized_finding.model_dump()
    
    # Execute the evaluation and actuation path
    remediator_result = remediator.process_proposal(
        remediation_proposal, 
        [sig_alpha, sig_beta]
    )

    if remediator_result.success:
        print(f"  [+] Gate Decision: ALLOWED")
        print(f"  [+] Action Executed: {remediator_result.message}")
    else:
        print(f"  [-] Gate Decision: BLOCKED - {remediator_result.message}")

    # 5. Post-Incident Rollback
    print("\n[Stage 5] Post-Incident: Evaluating telemetry regression rules...")
    # Simulate a regression after scale-up (e.g. error rate spiked to 98%)
    post_telemetry = {"error_rate": 0.98, "remediation_target": "api-service-x1"}
    print(f"  Post-Actuation Telemetry: Error Rate = {post_telemetry['error_rate']*100}%")
    
    rollback_triggered = post_telemetry["error_rate"] > 0.05
    rollback_gate_decision = "BLOCKED"
    rollback_execution = "NONE"
    
    if rollback_triggered:
        print("  [!] Regression Detected! Triggering rollback gate evaluation...")
        rollback_proposal = {
            "operation": "ROLLBACK",
            "target": "api-service-x1",
            "current_state": {"error_rate": 0.98}
        }
        gate_result = gate.evaluate(rollback_proposal)
        if gate_result.allowed:
            rollback_gate_decision = "ALLOWED"
            rollback_execution = "Executed state rollback to baseline image replica configuration."
            print(f"  [+] Rollback Gate: ALLOWED - {rollback_execution}")
        else:
            rollback_gate_decision = "BLOCKED"
            print(f"  [-] Rollback Gate: BLOCKED - {gate_result.reason}")

    # 6. Structured Evidence Package
    print("\n[Stage 6] Evidence: Emitting Signed Attestation Evidence Bundle...")
    
    evidence_bundle = {
        "schema_version": "https://json-schema.org/draft/2020-12/schema",
        "scenario": "GCP Multi-Agent Autonomous Safety Gate & Remediation Attestation Flow",
        "input_signal": raw_logs[0],
        "sanitized_signal": sanitized_finding.model_dump(),
        "consensus": {
            "threshold": guardian.threshold,
            "quorum_reached": remediator_result.consensus_check_passed,
            "agent_signatures": [sig_alpha, sig_beta]
        },
        "signature_profile": {
            "padding_scheme": "RSASSA-PSS",
            "hash_algorithm": "SHA-256",
            "mask_generation_function": "MGF1-SHA256",
            "salt_length": "padding.PSS.MAX_LENGTH"
        },
        "safety_gate_decision": {
            "allowed": remediator_result.safety_check_passed,
            "config_limits": {
                "max_replicas_per_service": safety_config.max_replicas_per_service,
                "allowed_operations": safety_config.allowed_operations
            }
        },
        "actuation_result": {
            "success": remediator_result.success,
            "action_taken": remediator_result.action_taken,
            "message": remediator_result.message
        },
        "post_incident_assessment": {
            "anomaly_metric": "error_rate",
            "metric_value": post_telemetry["error_rate"],
            "threshold_exceeded": rollback_triggered
        },
        "rollback_decision": {
            "triggered": rollback_triggered,
            "gate_decision": rollback_gate_decision,
            "execution": rollback_execution
        },
        "issued_at": int(time.time()),
        "payload_digest_sha256": payload_digest
    }

    evidence_dir = os.path.join(os.path.dirname(__file__), "evidence")
    os.makedirs(evidence_dir, exist_ok=True)
    evidence_path = os.path.join(evidence_dir, "golden_path_attestation.json")
    
    with open(evidence_path, "w") as f:
        json.dump(evidence_bundle, f, indent=2)
        
    print(f"  [+] Evidence bundle successfully generated and written to:")
    print(f"      {evidence_path}")
    print("\n" + "=" * 80)
    print("GOLDEN PATH WALKTHROUGH COMPLETED SUCCESSFULLY".center(80))
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
