import logging
import hashlib
import json
import time
from typing import List, Dict, Any
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.exceptions import InvalidSignature
from pydantic import BaseModel
from cachetools import TTLCache

from .logging_utils import get_logger, log_event

logger = get_logger("VotingValidator")

class ValidationError(Exception):
    """Custom exception with context for validation failures."""
    def __init__(self, message: str, code: str, details: Dict = None):
        self.code = code
        self.details = details or {}
        super().__init__(message)

class AgentSignature(BaseModel):
    agent_id: str
    signature_hex: str
    timestamp: int  # Integer timestamp for cryptographic stability
    nonce: str

class VotingProof(BaseModel):
    decision_hash: str
    signatures: List[AgentSignature]
    quorum_reached: bool
    threshold_used: float
    total_authorized: int

class VotingValidator:
    """
    Validates agent signatures against a registered public key list
    to verify a quorum threshold has been reached.
    """
    def __init__(self, threshold: float = 0.66, max_clock_skew: int = 60):
        self.threshold = threshold
        self.max_clock_skew = max_clock_skew
        self._authorized_keys: Dict[str, rsa.RSAPublicKey] = {}
        self._seen_nonces = TTLCache(maxsize=10000, ttl=300)

    def register_agent(self, agent_id: str, public_key_pem: bytes):
        """Registers an authorized agent with its public key."""
        try:
            self._authorized_keys[agent_id] = serialization.load_pem_public_key(public_key_pem)
            logger.info(f"Registered agent: {agent_id}")
        except Exception as e:
            logger.error(f"Failed to register agent {agent_id}: {e}")
            raise ValidationError(f"Invalid public key for agent {agent_id}", "AUTH_CONFIG_ERROR")

    def verify_quorum(self, proposal: Dict[str, Any], signatures: List[AgentSignature]) -> VotingProof:
        """
        Verifies that a majority of registered agents signed the proposal.
        """
        # Use canonical JSON (sorted keys, no whitespace) for stable hashing
        proposal_json = json.dumps(proposal, sort_keys=True, separators=(',', ':'))
        decision_hash = hashlib.sha256(proposal_json.encode()).hexdigest()
        logger.debug(f"Hashed proposal: {decision_hash} | Content: {proposal_json[:50]}...")
        
        valid_signatures = []
        seen_agents = set()
        current_time = time.time()
        
        # Snapshot of seen nonces at start of verification run to allow same-nonce signatures in same batch
        initially_seen = set(self._seen_nonces.keys())

        for sig in signatures:
            try:
                # 1. Nonce check
                if sig.nonce in initially_seen:
                    raise ValidationError("Replay attack detected", "REPLAY_ATTACK", {"nonce": sig.nonce, "agent": sig.agent_id})

                # 2. Clock skew check
                skew = current_time - sig.timestamp
                if abs(skew) > self.max_clock_skew:
                    raise ValidationError("Proposal timestamp invalid", "STALE_PROPOSAL", {"timestamp": sig.timestamp, "skew": skew})

                # 3. Authorization check
                if sig.agent_id not in self._authorized_keys:
                    raise ValidationError("Unauthorized agent", "UNAUTHORIZED_AGENT", {"agent": sig.agent_id})

                # 4. Duplicate agent check
                if sig.agent_id in seen_agents:
                    raise ValidationError("Duplicate agent signature", "DUPLICATE_SIGNATURE", {"agent": sig.agent_id})
                
                # 5. Cryptographic Verification
                public_key = self._authorized_keys[sig.agent_id]
                public_key.verify(
                    bytes.fromhex(sig.signature_hex),
                    proposal_json.encode(),
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
                
                valid_signatures.append(sig)
                seen_agents.add(sig.agent_id)
                self._seen_nonces[sig.nonce] = True
                
            except InvalidSignature:
                log_event(logger, logging.ERROR, "Invalid crypto signature.", extra={
                    "agent_id": sig.agent_id,
                    "decision_hash": decision_hash
                })
            except ValidationError as e:
                log_event(logger, logging.WARNING, f"Validation check failed: {str(e)}", extra={
                    "code": e.code,
                    **e.details
                })
            except Exception as e:
                log_event(logger, logging.ERROR, f"Unexpected error: {e}", extra={
                    "agent_id": sig.agent_id
                })

        total_agents = max(len(self._authorized_keys), 1)
        quorum_reached = len(valid_signatures) / total_agents >= self.threshold
        
        log_event(logger, logging.INFO, "Voting quorum evaluation complete.", extra={
            "quorum_reached": quorum_reached,
            "ratio": len(valid_signatures) / total_agents,
            "valid_count": len(valid_signatures),
            "total_agents": total_agents
        })
        
        return VotingProof(
            decision_hash=decision_hash,
            signatures=valid_signatures,
            quorum_reached=quorum_reached,
            threshold_used=self.threshold,
            total_authorized=len(self._authorized_keys)
        )
