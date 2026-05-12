# Enterprise Cryptographic Consensus: Identity & Rotation

The consensus pattern ensures that autonomous remediation is a **multi-sig, verifiable operation**. In an enterprise context, this requires deep integration with GCP's identity and secret management systems.

## 1. Identity Propagation & Workload Identity
In this reference architecture, each agent (or agent pool) is mapped to a unique **Google Service Account (GSA)**.
- **Verification**: The `ConsensusGuardian` does not just verify a signature; it verifies that the `agent_id` in the signature matches the **Workload Identity** (KSA/GSA) of the pod that emitted the proposal.
- **Benefit**: Prevents identity spoofing within the GKE cluster. Even if an agent's private key is leaked, it cannot "act" as another agent without a valid Workload Identity binding.

## 2. Key Lifecycle & Secret Management
Private keys are never stored in the agent's filesystem or environment variables.
- **Storage**: Keys are provisioned as **RSA-2048/4096-bit** pairs and stored in **Google Cloud Secret Manager**.
- **Rotation Strategy**:
    - **Frequency**: Automatic rotation every 30 days via Cloud Functions.
    - **Grace Period**: The `ConsensusGuardian` maintains the `n-1` public key for 24 hours to allow in-flight proposals to complete before fully decommissioning the old key.
- **Audit Trail**: Every access to a private key triggers a **Secret Manager Access Audit Log**, providing a non-repudiable record of which agent signed which action.

## 3. Quorum Dynamics & Fleet Health
The consensus threshold is not static; it is proportional to the **Authorized Fleet Size**.
- **Source of Truth**: The fleet registry is managed via a **Terraform-provisioned AlloyDB** or Config Map (reference only).
- **ZOMBIE Protection**: Agents that have not emitted a "Heartbeat" (signed health check) in over 60 minutes are automatically excluded from the quorum calculation. This prevents "Dead Man's Quorum" failures.

## 4. Compliance Evidence (Audit-Ready)
Consensus results are serialized into **Canonical JSON** and stored in a "Safety Audit" Cloud Storage bucket. This provides an immutable timeline of:
1. Who proposed the action.
2. Who signed it (Majority Quorum).
3. The exact state of the world at the time of signing.

```bash
# Querying Consensus Audit Trails in Cloud Logging
resource.type="k8s_container"
jsonPayload.event="CONSENSUS_COMPLETE"
jsonPayload.quorum_reached=true
```
