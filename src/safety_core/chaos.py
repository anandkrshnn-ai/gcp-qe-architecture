import random
import logging

logger = logging.getLogger("ChaosSimulator")

class ChaosSimulator:
    """
    Research-grade fault injection for resilience testing.
    """
    def __init__(self, failure_rate: float = 0.1):
        self.failure_rate = failure_rate

    def inject_telemetry_corruption(self, logs: list) -> list:
        """Simulates data corruption at the source."""
        if random.random() < self.failure_rate:
            logger.warning("[CHAOS] Injecting telemetry corruption...")
            return [{"jsonPayload": {"message": "Health status: OK (CORRUPTED)"}}]
        return logs
