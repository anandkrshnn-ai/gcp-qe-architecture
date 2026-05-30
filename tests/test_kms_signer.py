import pytest
import unittest.mock as mock
from signing.kms_signer import KMSSigner

def test_kms_signer_local_fallback():
    """Verify that if KMS key path is None, local fallback private key is used."""
    signer = KMSSigner(key_path=None)
    assert signer._kms_client is None
    assert signer._local_key is not None

    payload = b"hello-world"
    signature = signer.sign_payload(payload)
    assert len(signature) > 0

    pub_pem = signer.get_public_key_pem()
    assert b"BEGIN PUBLIC KEY" in pub_pem

def test_kms_signer_with_mock_client():
    """Verify that if KMS path is present and API is mocked, it calls asymmetric_sign."""
    # Create mock KeyManagementServiceClient client and response payloads
    mock_client = mock.MagicMock()
    
    mock_response = mock.MagicMock()
    mock_response.signature = b"kms-signed-mock-signature-value"
    mock_client.asymmetric_sign.return_value = mock_response

    mock_pub_key = mock.MagicMock()
    mock_pub_key.pem = "mock-pem-data"
    mock_client.get_public_key.return_value = mock_pub_key

    # Mock the kms module in signing.kms_signer
    mock_kms = mock.MagicMock()
    mock_kms.KeyManagementServiceClient.return_value = mock_client

    with mock.patch("signing.kms_signer.HAS_KMS", True), \
         mock.patch("signing.kms_signer.kms", mock_kms, create=True):
         
        signer = KMSSigner(key_path="projects/p1/locations/l1/keyRings/kr1/cryptoKeys/k1/cryptoKeyVersions/1")
        
        # Verify it initialized the KMS client
        assert signer._kms_client == mock_client
        
        payload = b"test-data"
        sig = signer.sign_payload(payload)
        assert sig == b"kms-signed-mock-signature-value"
        mock_client.asymmetric_sign.assert_called_once()
        
        pub = signer.get_public_key_pem()
        assert pub == b"mock-pem-data"
        mock_client.get_public_key.assert_called_once()
