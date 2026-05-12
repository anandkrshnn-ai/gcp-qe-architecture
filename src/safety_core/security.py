from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import time

class RuntimeSecurity:
    """
    Verifies cryptographic identity of agents.
    """
    def __init__(self, platform_public_key_pem: bytes):
        self.public_key = serialization.load_pem_public_key(platform_public_key_pem)

    def verify_runtime_attestation(self, attestation_report: bytes, signature: bytes) -> bool:
        """
        Verifies that the runtime attestation report was signed by the 
        trusted platform (e.g. simulated TPM or Cloud HSM).
        """
        try:
            self.public_key.verify(
                signature,
                attestation_report,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False

    def check_freshness(self, timestamp: float, max_age_seconds: int = 60) -> bool:
        """Ensures the attestation is not a replay attack."""
        return (time.time() - timestamp) < max_age_seconds
