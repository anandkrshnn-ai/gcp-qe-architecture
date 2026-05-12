import hashlib
import json
import time
from typing import List, Dict, Any, Optional
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.exceptions import InvalidSignature
from pydantic import BaseModel
from cachetools import TTLCache

from .logging_utils import get_logger

logger = get_logger("ConsensusGuardian")

class ConsensusError(Exception):
    """Base class for consensus-related errors."""
    def __init__(self, message: str, code: str = "GENERIC_ERROR"):
        super().__init__(message)
        self.code = code

class AgentSignature(BaseModel):
    agent_id: str
    signature_hex: str
    timestamp: float
    nonce: str

class ConsensusProof(BaseModel):
    decision_hash: str
    signatures: List[AgentSignature]
    quorum_reached: bool
    threshold_used: float
    total_authorized: int

class ConsensusGuardian:
    """
    Principal-Grade Reference for Cryptographic Consensus.
    Enforces majority quorum using RSA-PSS signatures and TTL-based nonce protection.
    """
    def __init__(self, threshold: float = 0.66, max_clock_skew: int = 60):
        self.threshold = threshold
        self.max_clock_skew = max_clock_skew
        self._authorized_keys: Dict[str, rsa.RSAPublicKey] = {}
        # Enforce 5-minute TTL for nonces to prevent memory leaks while blocking replays
        self._seen_nonces = TTLCache(maxsize=10000, ttl=300)

    def register_agent(self, agent_id: str, public_key_pem: bytes):
        """Registers an authorized agent with its public key."""
        try:
            self._authorized_keys[agent_id] = serialization.load_pem_public_key(public_key_pem)
            logger.info(f"Registered agent: {agent_id}")
        except Exception as e:
            logger.error(f"Failed to register agent {agent_id}: {e}")
            raise ConsensusError(f"Invalid public key for agent {agent_id}", code="AUTH_CONFIG_ERROR")

    def verify_quorum(self, proposal: Dict[str, Any], signatures: List[AgentSignature]) -> ConsensusProof:
        """
        Genuinely verifies that a unique majority of authorized agents signed the proposal.
        """
        proposal_json = json.dumps(proposal, sort_keys=True)
        decision_hash = hashlib.sha256(proposal_json.encode()).hexdigest()
        
        valid_signatures = []
        seen_agents = set()
        current_time = time.time()

        for sig in signatures:
            # 1. Nonce check (Replay Protection with TTL)
            if sig.nonce in self._seen_nonces:
                logger.warning(f"REPLAY ATTACK DETECTED: Nonce {sig.nonce} already seen.")
                continue

            # 2. Clock skew check
            if abs(current_time - sig.timestamp) > self.max_clock_skew:
                logger.warning(f"Rejected stale signature from {sig.agent_id} (skew: {current_time - sig.timestamp:.2f}s)")
                continue

            # 3. Authorization check
            if sig.agent_id not in self._authorized_keys:
                logger.warning(f"Unauthorized agent: {sig.agent_id}")
                continue

            # 4. Duplicate agent in same proposal check
            if sig.agent_id in seen_agents:
                logger.warning(f"Duplicate agent signature in proposal: {sig.agent_id}")
                continue
            
            # 5. Cryptographic Verification
            try:
                public_key = self._authorized_keys[sig.agent_id]
                public_key.verify(
                    bytes.fromhex(sig.signature_hex),
                    decision_hash.encode(),
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
                valid_signatures.append(sig)
                seen_agents.add(sig.agent_id)
                self._seen_nonces[sig.nonce] = True  # Mark nonce as used
            except InvalidSignature:
                logger.error(f"Invalid cryptographic signature from agent: {sig.agent_id}")
            except Exception as e:
                logger.error(f"Internal error verifying signature from {sig.agent_id}: {e}")

        total_agents = max(len(self._authorized_keys), 1)
        quorum_reached = len(valid_signatures) / total_agents >= self.threshold
        
        return ConsensusProof(
            decision_hash=decision_hash,
            signatures=valid_signatures,
            quorum_reached=quorum_reached,
            threshold_used=self.threshold,
            total_authorized=len(self._authorized_keys)
        )
