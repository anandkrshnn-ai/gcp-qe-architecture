import hashlib
import json
import time
from typing import List, Dict, Any, Optional
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from pydantic import BaseModel, Field

class AgentSignature(BaseModel):
    agent_id: str
    signature_hex: str
    timestamp: float

class ConsensusProof(BaseModel):
    decision_hash: str
    signatures: List[AgentSignature]
    quorum_reached: bool
    threshold_used: float

class ConsensusGuardian:
    """
    Staff-level Consensus Reference.
    Genuinely verifies majority quorum using RSA cryptographic signatures.
    """
    def __init__(self, threshold: float = 0.66):
        self.threshold = threshold
        self._authorized_keys = {} # Mapping of agent_id -> RSAPublicKey

    def register_agent(self, agent_id: str, public_key_pem: bytes):
        self._authorized_keys[agent_id] = serialization.load_pem_public_key(public_key_pem)

    def verify_quorum(self, proposal: Dict[str, Any], signatures: List[AgentSignature]) -> ConsensusProof:
        """
        Genuinely verifies that a majority of unique authorized agents 
        signed the exact same proposal hash.
        """
        proposal_json = json.dumps(proposal, sort_keys=True)
        decision_hash = hashlib.sha256(proposal_json.encode()).hexdigest()
        
        valid_signatures = []
        seen_agents = set()

        for sig in signatures:
            if sig.agent_id not in self._authorized_keys or sig.agent_id in seen_agents:
                continue
            
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
            except Exception:
                continue

        quorum_reached = len(valid_signatures) / max(len(self._authorized_keys), 1) >= self.threshold
        
        return ConsensusProof(
            decision_hash=decision_hash,
            signatures=valid_signatures,
            quorum_reached=quorum_reached,
            threshold_used=self.threshold
        )
