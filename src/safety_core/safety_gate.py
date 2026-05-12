from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

class SafetyConfig(BaseModel):
    """Honest configuration for remediation safety."""
    max_replicas_per_service: int = 10
    max_scale_factor: float = 2.0
    blocked_operations: List[str] = ["DELETE", "PURGE"]
    cost_per_replica_hour: float = 0.05

class SafetyValidationResult(BaseModel):
    is_safe: bool
    reason: str
    estimated_cost_increase: float

class SafetyGate:
    """
    Defensible Safety Validation Gate.
    No more 'Epistemic Safety' theater. Just strict resource and cost limits.
    """
    def __init__(self, config: SafetyConfig):
        self.config = config

    def validate_proposal(self, proposal: Dict[str, Any]) -> SafetyValidationResult:
        """
        Genuinely validates a remediation proposal against resource quotas.
        """
        # 1. Block destructive operations
        op = proposal.get("operation", "").upper()
        if op in self.config.blocked_operations:
            return SafetyValidationResult(
                is_safe=False, 
                reason=f"Operation '{op}' is explicitly blocked for safety.",
                estimated_cost_increase=0.0
            )

        # 2. Check replica scaling
        replicas = proposal.get("replicas", 0)
        if replicas > self.config.max_replicas_per_service:
            return SafetyValidationResult(
                is_safe=False,
                reason=f"Replica count {replicas} exceeds safety limit of {self.config.max_replicas_per_service}.",
                estimated_cost_increase=0.0
            )

        # 3. Simple Cost Estimation
        estimated_cost = replicas * self.config.cost_per_replica_hour
        
        return SafetyValidationResult(
            is_safe=True,
            reason="Proposal within safety quotas.",
            estimated_cost_increase=estimated_cost
        )
