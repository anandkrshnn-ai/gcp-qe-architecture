# Security Policy

## Supported Versions

The following versions of `Safety-core` are currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 0.2.x   | :white_check_mark: |
| < 0.2   | :x:                |

## Reporting a Vulnerability

We take the security of this architectural baseline seriously. If you believe you have found a security vulnerability, please report it via the following process:

1. **Email**: Send a detailed report to [security@example.com](mailto:security@example.com).
2. **Details**: Include a description of the vulnerability, the potential impact, and steps to reproduce.
3. **Response**: We will acknowledge your report within 48 hours and provide a timeline for remediation.

**Please do not open a public issue for security vulnerabilities.**

---

## 🔑 GCP Trusted Platform Extension Path (Production Integration)

In production environments, agent signing keys should never be stored as local files. We recommend leveraging native GCP trust anchors:

### 1. Workload Identity Federation (GKE & Cloud Run)
Run your safety agents inside GKE or Cloud Run using a dedicated Google Service Account (GSA) bound to a Kubernetes Service Account (KSA) via Workload Identity. This eliminates static GCP credentials:
```bash
# Bind KSA to GSA
gcloud iam service-accounts add-iam-policy-binding GSA_NAME@PROJECT_ID.iam.gserviceaccount.com \
    --role roles/iam.workloadIdentityUser \
    --member "serviceAccount:PROJECT_ID.svc.id.goog[NAMESPACE/KSA_NAME]"
```

### 2. Secret Manager & CMEK for RSA Key Storage
Store private keys in Cloud Secret Manager, encrypted with a Customer-Managed Encryption Key (CMEK) via Cloud KMS. Below is the canonical adapter template for retrieving a key securely at runtime:

```python
from google.cloud import secretmanager
from google.auth import default

def load_verification_key_from_secret_manager(secret_id: str, version_id: str = "latest") -> bytes:
    """
    Retrieves the public RSA key securely from Google Cloud Secret Manager
    using credentials automatically resolved from Workload Identity.
    """
    # Initialize client using implicit default credentials (resolved via WIF)
    credentials, project = default()
    client = secretmanager.SecretManagerServiceClient(credentials=credentials)
    
    # Build secret resource path
    name = f"projects/{project}/secrets/{secret_id}/versions/{version_id}"
    
    # Retrieve secret payload
    response = client.access_secret_version(request={"name": name})
    return response.payload.data
```
