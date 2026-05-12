from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from .consensus import ConsensusGuardian, AgentSignature
from .safety_gate import SafetyGate
from .logging_utils import get_logger

logger = get_logger("SafetyRemediator")

class RemediationResult(BaseModel):
    success: bool
    action_taken: str
    message: str
    safety_check_passed: bool
    consensus_check_passed: bool

class DryRunRemediator:
    """
    Verified actuator that checks consensus and safety gates before 'execution'.
    """
    def __init__(self, consensus: ConsensusGuardian, safety_gate: SafetyGate):
        self.consensus = consensus
        self.safety_gate = safety_gate

    def process_proposal(self, finding: Dict[str, Any], signatures: List[Dict[str, Any]]) -> RemediationResult:
        """
        Verifies and processes a remediation proposal based on multi-agent consensus.
        """
        # 1. Verify Consensus
        try:
            agent_sigs = [AgentSignature(**s) for s in signatures]
        except Exception as e:
            logger.error(f"Invalid signature format: {e}")
            return RemediationResult(
                success=False,
                action_taken="NONE",
                message=f"Invalid signature format: {e}",
                safety_check_passed=False,
                consensus_check_passed=False
            )

        consensus_proof = self.consensus.verify_quorum(finding, agent_sigs)
        
        if not consensus_proof.quorum_reached:
            logger.warning("Consensus quorum FAILED.")
            return RemediationResult(
                success=False,
                action_taken="NONE",
                message="Consensus quorum not reached.",
                safety_check_passed=False,
                consensus_check_passed=False
            )

        # 2. Verify Safety Gate
        remediation = finding.get("proposed_remediation", {})
        # Enrich remediation with target if missing
        if "target" not in remediation:
            remediation["target"] = finding.get("incident_id", "unknown-target")
            
        safety_result = self.safety_gate.validate_proposal(remediation)
        
        if not safety_result.is_safe:
            logger.warning(f"Safety gate BLOCKED: {safety_result.reason}")
            return RemediationResult(
                success=False,
                action_taken="NONE",
                message=f"Safety gate blocked operation: {safety_result.reason}",
                safety_check_passed=False,
                consensus_check_passed=True
            )

        # 3. Execute Remediation (Idempotent Simulation)
        operation = remediation.get("operation", "UNKNOWN")
        action_msg = f"Executed {operation} on {finding.get('incident_type')}"
        logger.info(action_msg)
        
        return RemediationResult(
            success=True,
            action_taken=operation,
            message=action_msg,
            safety_check_passed=True,
            consensus_check_passed=True
        )
