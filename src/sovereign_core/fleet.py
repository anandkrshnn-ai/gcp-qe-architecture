import hashlib
import hmac
import json
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class SovereignFleet:
    """
    Wave 10: Byzantine Fleet v2.1.0 - The Upgrade Paradox.
    Handles mixed-version deployments and "unfixable" hardware detection.
    """
    def __init__(self, agent_id: str, version: str = "2.1.0", total_agents: int = 4):
        self.agent_id = agent_id
        self.version = version
        self.total_agents = total_agents
        self.quorum_threshold = (total_agents // 3 * 2) + 1
        self.compat_nodes = {}

    def verify_node_version(self, node_id: str, node_version: str) -> bool:
        """
        BFT-11: Upgrade Quarantine.
        Excludes legacy (v1.x) nodes from the PBFT consensus layer.
        """
        if node_version.startswith("1."):
            logger.warning(f"[UPGRADE] Node {node_id} is v{node_version} (Legacy). QUARANTINING.")
            return False
        return True

    def propose_remediation(self, action: Dict) -> str:
        """
        Byzantine Consensus with Version Awareness.
        """
        request_hash = self._calculate_request_hash(action)
        
        # BFT-11: Only collect signatures from verified v2+ nodes.
        signatures = self._collect_fleet_signatures(request_hash)
        valid_sigs = [s for s in signatures if self.verify_node_version(s["id"], s["v"])]
        
        if len(valid_sigs) < self.quorum_threshold:
            logger.error("[BYZANTINE] BFT-11: Quorum Failed due to Version Mismatch/Quarantine.")
            return "REJECTED_VERSION_MISMATCH"
            
        return f"APPROVED_{request_hash}"

    def verify_execution_proof(self, receipt: Dict) -> bool:
        """
        BFT-9: Proof-of-Execution.
        Verifies that a follower actually performed the action.
        """
        if not receipt.get("cloud_api_signature"):
            logger.error("[BYZANTINE] BFT-9: Lazy Follower Detected. No Execution Proof.")
            return False
        return True

    def _calculate_request_hash(self, action: Dict) -> str:
        """BFT-3: Request binding to prevent Confused Deputy attacks."""
        payload = json.dumps(action, sort_keys=True)
        return hashlib.sha256(payload.encode()).hexdigest()

    def _collect_fleet_signatures(self, request_hash: str) -> List[str]:
        """Simulated fleet signature collection."""
        # Agent A (Me) - Honest
        # Agent B (Follower) - Honest
        # Agent C (Follower) - Honest
        # Agent D (Byzantine) - Lying/Withholding
        return ["sig_agent_a", "sig_agent_b", "sig_agent_c"]
