# Model Armor: Enterprise Data Protection

Model Armor is not just a "filter"; it is a **Security Perimeter Guard** that ensures agentic autonomy does not result in data exfiltration or credential leakage.

## 1. Leak Shield (Operational Hardening)

### Sanitization Latency SLO
In a high-throughput QE environment, the sanitization layer must not become a bottleneck.
- **Target**: 99th percentile processing time **< 50ms** per finding.
- **Strategy**: Utilizes pre-compiled, high-fidelity regex patterns and local string manipulation to avoid external API round-trips for basic redaction.

### Regex Drift & Update Strategy
Regex patterns for secrets (API keys, Service Account IDs) are managed as **Code-as-Configuration**.
- **Update Cycle**: Patterns are synchronized bi-weekly from a centralized **Security Policy Repository**.
- **Testing**: Every pattern update is validated against a **"Secret Leak Test Set"** (synthetic keys) to ensure 0% false-negative rates before promotion to production.

## 2. Integration with VPC Service Controls (VPC-SC)

Model Armor acts as the final "Identity-Aware" checkpoint before a finding is allowed to egress the agent's private network.
- **Perimeter Enforcement**: If a finding contains data that matches **Restricted Data Patterns** (defined via DLP API profiles), the Armor triggers a `403 SECURITY_BLOCK` and prevents the agent from signing the proposal.
- **Audit Logging**: All redaction events are mirrored to the **Security Command Center (SCC)** as high-priority findings.

## 3. Compliance & PII Strategy

| Feature | Production Implementation | Verification |
| :--- | :--- | :--- |
| **GCP Secrets** | Regex Redaction (AIza...) | Verified (Test Suite) |
| **PII Detection** | Vertex AI Safety Filters (Pre-Inference) | In-Progress |
| **Audit Trails** | Cloud Audit Logs (Secret Access) | Active |

## Implementation Flow (Ruthless View)

The Model Armor sits **inside the TEE (Trusted Execution Environment)** or the private GKE pod. No finding is ever signed by an agent until the Armor sidecar has attached a `VERIFIED_CLEAN` cryptographic attestation to the metadata.
