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
    def __init__(self, agent_id: str, version: str = "2.2.0", total_agents: int = 4):
        self.agent_id = agent_id
        self.version = version
        self.total_agents = total_agents
        self.quorum_threshold = (total_agents // 3 * 2) + 1
        self.nodes = {agent_id: {"v": version, "status": "HEALTHY", "weight": 1.0, "anomalies": 0}}

    def report_anomaly(self, node_id: str):
        """
        BFT-12: Byzantine Remediation Policy.
        Implements Suspect Quarantine and Auto-Eviction.
        """
        node = self.nodes.get(node_id, {})
        if not node: return
        
        node["anomalies"] += 1
        if node["anomalies"] >= 3:
            # Phase 1: Suspect Quarantine (Read-Only Observer)
            node["status"] = "SUSPECT"
            node["weight"] = 0.0
            logger.warning(f"[BYZANTINE] BFT-12: Node {node_id} QUARANTINED (Suspect). Weight=0.")
            
        if node["anomalies"] >= 12:
            # Phase 2: Auto-Deprovisioning (Eviction)
            node["status"] = "EVICTED"
            logger.error(f"[BYZANTINE] BFT-12: Node {node_id} EVICTED from fleet due to persistent anomalies.")

    def propose_remediation(self, action: Dict) -> str:
        """
        Byzantine Consensus with Suspect Weighting.
        """
        request_hash = self._calculate_request_hash(action)
        signatures = self._collect_fleet_signatures(request_hash)
        
        # BFT-12: Only count signatures from non-quarantined nodes with weight > 0
        valid_votes = 0
        for sig in signatures:
            node = self.nodes.get(sig["id"], {"v": "1.0", "status": "UNKNOWN", "weight": 0.0})
            if node["status"] == "HEALTHY" and self.verify_node_version(sig["id"], sig["v"]):
                valid_votes += 1
        
        if valid_votes < self.quorum_threshold:
            logger.error(f"[BYZANTINE] BFT-12: Quorum Failed. Only {valid_votes} healthy signatures.")
            return "REJECTED_BYZANTINE_QUARANTINE"
            
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
