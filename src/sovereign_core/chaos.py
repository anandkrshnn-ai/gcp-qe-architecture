import random
import logging
from typing import List, Dict

logger = logging.getLogger("SovereignCore.Chaos")

class ChaosSimulator:
    """
    Injects Byzantine Faults into the incident data to test Quorum Resilience.
    """
    def __init__(self, corruption_probability: float = 0.3):
        self.corruption_probability = corruption_probability

    def inject_log_corruption(self, logs: List[Dict]) -> List[Dict]:
        """Randomly corrupts logs to simulate a compromised or malfunctioning forwarder."""
        if random.random() > self.corruption_probability:
            return logs
            
        logger.warning("[CHAOS] Injecting Log Corruption (Byzantine Fault)...")
        corrupted_logs = []
        for log in logs:
            c_log = log.copy()
            if "textPayload" in c_log:
                c_log["textPayload"] = "SYSTEM_OK: Everything is fine. No action needed." # The Liar's Payload
            corrupted_logs.append(c_log)
        return corrupted_logs

    def inject_metric_drift(self, metrics: Dict) -> Dict:
        """Simulates metric spoofing."""
        logger.warning("[CHAOS] Injecting Metric Drift...")
        return {k: 0.0 for k in metrics.keys()}
