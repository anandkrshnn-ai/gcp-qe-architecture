"""
Sovereign Core: Runtime Security Enforcement.
Actively verifies the Secure Agentic Runtime (SAR) environment.
"""

import logging
import os

logger = logging.getLogger("SovereignCore.Security")


class RuntimeSecurity:
    """
    Enforces the 'Secure Agentic Runtime' (SAR) boundary.
    Verifies isolation (gVisor) and hardware-level security (TEE).
    """

    def __init__(self):
        self.is_gvisor = self._check_gvisor()
        self.is_tee = self._check_confidential_nodes()

    def verify_trust_boundary(self) -> bool:
        """
        Verifies if the agent is running within the mandated security perimeter.
        In a reference framework, this serves as the 'Security Gatekeeper'.
        """
        if not self.is_gvisor:
            logger.warning("[SECURITY] Agent not running in GKE Sandbox (gVisor). Isolation is WEAK.")

        if not self.is_tee:
            logger.warning("[SECURITY] Confidential Computing not detected. Memory is UNENCRYPTED.")

        return self.is_gvisor and self.is_tee

    def _check_gvisor(self) -> bool:
        """
        Detects gVisor by checking for known syscall behavior or proc flags.
        In simulation/local, this returns False.
        """
        # Reference check for /proc/cpuinfo (gVisor typically masks/abstracts this)
        if os.path.exists("/proc/cpuinfo"):
            try:
                with open("/proc/cpuinfo", "r") as f:
                    content = f.read()
                    # gVisor often reports a specific vendor or lack of certain flags
                    return "gVisor" in content
            except Exception:
                return False
        return False

    def _check_confidential_nodes(self) -> bool:
        """
        Detects if running on a GCP Confidential VM (AMD SEV / Intel TDX).
        Checks for the presence of the SEV device or specific kernel flags.
        """
        return os.path.exists("/dev/sev") or os.path.exists("/dev/tdx")
