from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from .logging_utils import get_logger

logger = get_logger("SafetyGate")

class ActionProposal(BaseModel):
    """Schema for a remediation proposal."""
    operation: str
    target: str
    replicas: Optional[int] = 0
    scale_factor: Optional[float] = 1.0
    current_state: Optional[Dict[str, Any]] = {}

class SafetyConfig(BaseSettings):
    """
    Deterministic safety boundaries.
    Loads from environment variables with SAFETY_ prefix (e.g., SAFETY_MAX_REPLICAS).
    """
    max_replicas_per_service: int = 10
    max_scale_factor: float = 2.0
    max_estimated_cost_per_remediation: float = 50.0
    allowed_operations: List[str] = ["SCALE_UP", "RESTART", "NOTIFY"]
    cost_per_replica_hour: float = 0.05

    model_config = SettingsConfigDict(env_prefix='SAFETY_')

class SafetyValidationResult(BaseModel):
    is_safe: bool
    reason: str
    risk_score: float = 0.0
    estimated_cost_increase: float = 0.0

class SafetyGate:
    """
    Deterministic Safety Validation Gate.
    Enforces resource quotas, cost limits, and operational restrictions.
    """
    def __init__(self, config: SafetyConfig):
        self.config = config

    def validate_proposal(self, raw_proposal: Dict[str, Any]) -> SafetyValidationResult:
        """
        Validates a proposal against resource, operational, and cost boundaries.
        """
        try:
            proposal = ActionProposal(**raw_proposal)
        except Exception as e:
            logger.error(f"Invalid proposal schema: {e}")
            return SafetyValidationResult(
                is_safe=False,
                reason=f"Proposal failed schema validation: {e}"
            )

        # 1. Enforce Allow-List
        op = proposal.operation.upper()
        if op not in self.config.allowed_operations:
            logger.warning(f"Operation NOT in allow-list: {op}")
            return SafetyValidationResult(
                is_safe=False, 
                reason=f"Operation '{op}' is not in the approved safety allow-list.",
                risk_score=1.0
            )

        # 2. Check scale factor
        if proposal.scale_factor > self.config.max_scale_factor:
            logger.warning(f"Excessive scale factor: {proposal.scale_factor}")
            return SafetyValidationResult(
                is_safe=False,
                reason=f"Scale factor {proposal.scale_factor} exceeds safety limit.",
                risk_score=0.8
            )

        # 3. Check replica scaling
        if proposal.replicas > self.config.max_replicas_per_service:
            logger.warning(f"Excessive replicas: {proposal.replicas}")
            return SafetyValidationResult(
                is_safe=False,
                reason=f"Replica count {proposal.replicas} exceeds safety limit.",
                risk_score=0.9
            )

        # 4. Cost Guard
        estimated_cost = proposal.replicas * self.config.cost_per_replica_hour
        if estimated_cost > self.config.max_estimated_cost_per_remediation:
            logger.warning(f"Cost guard blocked remediation: ${estimated_cost:.2f}")
            return SafetyValidationResult(
                is_safe=False,
                reason=f"Estimated cost ${estimated_cost:.2f} exceeds threshold.",
                risk_score=0.7,
                estimated_cost_increase=estimated_cost
            )
        
        logger.info(f"Safety APPROVED for {proposal.target} ({op}) at estimated cost ${estimated_cost:.2f}")
        return SafetyValidationResult(
            is_safe=True,
            reason="Proposal within safety quotas.",
            estimated_cost_increase=estimated_cost
        )
