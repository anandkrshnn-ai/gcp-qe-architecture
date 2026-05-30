import os
import logging
from typing import Dict, Any
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

try:
    from google.cloud import kms
    HAS_KMS = True
except ImportError:
    HAS_KMS = False

logger = logging.getLogger("KMSSigner")

class KMSSigner:
    """
    Production-style asymmetric signer implementing Google Cloud KMS
    with automated local mock fallback when credentials/SDK are missing.
    """
    def __init__(self, key_path: str = None):
        self.key_path = key_path or os.getenv("GCP_KMS_KEY_PATH")
        self._kms_client = None
        self._local_key = None

        if HAS_KMS and self.key_path:
            try:
                # Initializes official Google Cloud KMS client
                # Standard Workload Identity resolves credentials implicitly
                self._kms_client = kms.KeyManagementServiceClient()
                logger.info(f"Initialized Cloud KMS signer with key path: {self.key_path}")
            except Exception as e:
                logger.warning(f"Failed to initialize KMS client, falling back to local provider: {e}")
                self._init_local_fallback()
        else:
            self._init_local_fallback()

    def _init_local_fallback(self):
        logger.info("Using local mock key provider for signing.")
        self._local_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    def sign_payload(self, data: bytes) -> bytes:
        """
        Signs raw data payload using RSASSA-PSS-2048-SHA256.
        """
        if self._kms_client and self.key_path:
            try:
                # Calculate digest locally
                digest = hashes.Hash(hashes.SHA256())
                digest.update(data)
                digest_bytes = digest.finalize()

                # Call Google Cloud KMS to sign the digest
                # Using asymmetric sign
                response = self._kms_client.asymmetric_sign(
                    request={
                        "name": self.key_path,
                        "digest": {"sha256": digest_bytes}
                    }
                )
                return response.signature
            except Exception as e:
                logger.warning(f"KMS signing failed, using local key: {e}")
                
        # Fallback local signature using RSASSA-PSS
        return self._local_key.sign(
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

    def get_public_key_pem(self) -> bytes:
        """
        Retrieves the public key PEM bytes.
        """
        if self._kms_client and self.key_path:
            try:
                # Fetch public key from Google KMS
                response = self._kms_client.get_public_key(request={"name": self.key_path})
                return response.pem.encode("utf-8")
            except Exception as e:
                logger.warning(f"Failed to fetch public key from KMS: {e}")
                
        # Local fallback public key bytes
        return self._local_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
