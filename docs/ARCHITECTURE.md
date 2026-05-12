# Safety Core: Architectural Blueprint

This document defines the structural patterns of the Agent Safety Core framework. It prioritizes **verifiable engineering** over opaque agentic decision-making.

## 1. The Verified OODA Loop
The core engine follows the Observe-Orient-Decide-Act (OODA) loop, with a heavy emphasis on the **Decide** and **Act** safety boundaries.

```mermaid
graph TD
    subgraph Observe
        A[Cloud Logging API] --> B[SafetyAnalyzer]
        C[Local JSON Data] --> B
    end

    subgraph Orient_Decide
        B --> D[Finding Generated]
        D --> E[Multi-Agent RSA Signing]
    end

    subgraph Act_Safety
        E --> F[Consensus Guardian\n(Verifies Majority Quorum)]
        F --> G[Safety Gate\n(Resource/Cost Validation)]
        G -->|Pass| H[Remediator Actuator]
        G -->|Fail| I[Rejection + Audit]
    end
```

## 2. Component Responsibility

### `SafetyAnalyzer` (The Observation Layer)
Responsible for identifying incidents from telemetry.
- **Deterministic**: Uses rule-based heuristics to identify known failure modes (OOMKill, latency spikes).
- **Attested**: Signs every finding using an agent-specific RSA private key to provide non-repudiable evidence for consensus.

### `ConsensusGuardian` (The Integrity Layer)
The "Truth Engine" of the system.
- **Quorum Verification**: Genuinely verifies that a specified majority (e.g., 66%) of unique authorized agents have signed the exact same finding hash.
- **RSA-PSS**: Uses standard cryptographic padding to ensure signature integrity.

### `SafetyGate` (The Policy Layer)
The "Brakes" of the system.
- **Resource Quotas**: Validates remediation proposals against strict limits (max replicas, max scale factor).
- **Operation Blocking**: Blocks dangerous operations (e.g., `DELETE`, `PURGE`) at the schema level.

### `SafetyRemediator` (The Actuation Layer)
The "Hands" of the system.
- **Gatekeeping**: Only proceeds if both the `ConsensusGuardian` and `SafetyGate` return a success status.
- **Idempotency**: Designed to trigger idempotent infrastructure updates via cloud APIs.

## 3. Trust Boundary & Security
- **Identity Integrity**: Each agent node has a hardware-backed or Secret Manager-stored identity.
- **Evidence Immutability**: By hashing and signing findings at the source, the system creates a verifiable audit trail that persists even if a central log is tampered with.
- **Defense in Depth**: Even if an LLM is compromised and proposes a "poisoned" patch, it must still pass the deterministic `SafetyGate` boundaries.
