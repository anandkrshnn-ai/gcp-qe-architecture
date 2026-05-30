from abc import ABC, abstractmethod
from typing import Dict, Any, List

class LogSourcePort(ABC):
    """Port defining interface to extract log events and metric telemetry."""
    @abstractmethod
    def fetch_recent_logs(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Fetches telemetry logs matching query constraint."""
        pass

class ActuationPort(ABC):
    """Port defining interface to execute environment state modifications."""
    @abstractmethod
    def apply_patch(self, target: str, operation: str, params: Dict[str, Any]) -> bool:
        """Applies state changes or mitigations to the designated target resource."""
        pass
