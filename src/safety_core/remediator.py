from typing import List, Dict, Any
from pydantic import BaseModel
from .consensus import ConsensusGuardian, AgentSignature
from .safety_gate import SafetyGate
from .logging_utils import get_logger
from .ports import ActuationPort

logger = get_logger("SafetyRemediator")

class RemediationResult(BaseModel):
    success: bool
    action_taken: str
    message: str
    safety_check_passed: bool
    consensus_check_passed: bool

class DryRunRemediator(ActuationPort):
    """
    Verified actuator that checks consensus and safety gates before 'execution'.
    """
    def __init__(self, consensus: ConsensusGuardian, safety_gate: SafetyGate):
        self.consensus = consensus
        self.safety_gate = safety_gate

    def verify_remediation_signatures(self, finding: Dict[str, Any], agent_sigs: List[AgentSignature]) -> bool:
        """
        Enforces cryptographic attestation validation.
        Fails closed if the payload has not achieved quorum verification.
        """
        try:
            consensus_proof = self.consensus.verify_quorum(finding, agent_sigs)
            return consensus_proof.quorum_reached
        except Exception as e:
            logger.error(f"Attestation signature verification threw exception: {e}")
            return False

    def apply_patch(self, target: str, operation: str, params: Dict[str, Any]) -> bool:
        """Implements the ActuationPort interface."""
        action_msg = f"ActuationPort: Executed {operation} on {target}"
        logger.info(action_msg)
        return True

    def process_proposal(self, finding: Dict[str, Any], signatures: List[Dict[str, Any]]) -> RemediationResult:
        """
        Verifies and processes a remediation proposal based on multi-agent consensus.
        """
        # 1. Verify signatures format
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

        # 2. Cryptographic signature check (Fail closed)
        consensus_passed = self.verify_remediation_signatures(finding, agent_sigs)
        if not consensus_passed:
            logger.warning("Consensus validation FAILED. Rejecting state-changing action.")
            return RemediationResult(
                success=False,
                action_taken="NONE",
                message="Consensus quorum verification failed.",
                safety_check_passed=False,
                consensus_check_passed=False
            )

        # 3. Verify Safety Gate boundaries
        remediation = finding.get("proposed_remediation", {})
        if "target" not in remediation:
            remediation["target"] = finding.get("incident_id", "unknown-target")
            
        gate_result = self.safety_gate.evaluate(remediation)
        
        if not gate_result.allowed:
            logger.warning(f"Safety gate BLOCKED: {gate_result.reason}")
            return RemediationResult(
                success=False,
                action_taken="NONE",
                message=f"Safety gate blocked operation: {gate_result.reason}",
                safety_check_passed=False,
                consensus_check_passed=True
            )

        # 4. Execute Actuation using ports abstract boundary
        operation = remediation.get("operation", "UNKNOWN")
        target = remediation.get("target", "unknown-target")
        actuation_success = self.apply_patch(target, operation, remediation)
        
        return RemediationResult(
            success=actuation_success,
            action_taken=operation,
            message=f"Executed {operation} on {target} successfully.",
            safety_check_passed=True,
            consensus_check_passed=True
        )
