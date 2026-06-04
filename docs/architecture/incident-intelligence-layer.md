# The Incident Intelligence Layer

While the platform provides the infrastructure, the **Incident Intelligence Layer** provides the governance and verification. This layer is responsible for the interpretation of signals and the enforcement of safety.

## 1. Incident Intelligence Taxonomy

We categorize incident verification into five distinct levels of verification, ensuring the AI-driven OODA loop is both accurate and safe.

| Level | Scope | Verification Mechanism |
| :--- | :--- | :--- |
| **Contract** | API Schema Alignment | Pydantic validation of `Finding` and `ActionProposal` objects. |
| **Synthetic** | RCA Accuracy | Replaying historical incident logs into the `SafetyAnalyzer`. |
| **Property** | Logic Resilience | **Hypothesis** property-based tests for quorum and nonce logic. |
| **Adversarial** | Security Hardening | Red-team suites for signature forgery and replay attacks. |
| **Recovery** | Post-Remediation Verification | Rollback gates evaluated based on telemetry regression signals. |

## 2. Test Suite Mapping

We maintain a flat, verified test suite mapped directly to our verification taxonomy:

| Test File | Verification Level | Scope & Objective |
| :--- | :--- | :--- |
| **[test_safety.py](https://github.com/anandkrshnn-ai/gcp-incident-analysis-demo/blob/main/tests/test_safety.py)** | **Contract & Synthetic** | Verifies standard Pydantic models (contract) and runs end-to-end simulation pipelines to verify root-cause analysis (synthetic). |
| **[test_property_based.py](https://github.com/anandkrshnn-ai/gcp-incident-analysis-demo/blob/main/tests/test_property_based.py)** | **Property** | Uses **Hypothesis** to prove quorum logic remains resilient under random nonce generation and varying system clock drifts. |
| **[test_adversarial.py](https://github.com/anandkrshnn-ai/gcp-incident-analysis-demo/blob/main/tests/test_adversarial.py)** | **Adversarial** | Evaluates response of safety modules against simulated attacks, including signature tampering, nonce reuse, and invalid agent keys. |
| **[test_recovery.py](https://github.com/anandkrshnn-ai/gcp-incident-analysis-demo/blob/main/tests/test_recovery.py)** | **Recovery** | Simulates post-actuation telemetry regressions (e.g. error rates) to verify that rollback gates trigger correctly. |
| **[test_kms_signer.py](https://github.com/anandkrshnn-ai/gcp-incident-analysis-demo/blob/main/tests/test_kms_signer.py)** | **Integration** | Verifies the Cloud KMS asymmetric signing adapter and its safe fallback to local in-memory keys. |

## 3. The Verification Workflow

Incident validation is not a post-facto audit; it is a **pre-actuation gate**.

1. **Static Analysis**: Ruff and Pydantic enforce schema integrity before an agent is allowed to sign a proposal.
2. **Logic Proof**: Property-based tests prove that the `VotingValidator` is mathematically sound under extreme clock-skew (±28s).
3. **Adversarial Gate**: The test suite includes intentional forgery attempts. If the system fails to block a forged signature, the CI/CD pipeline is automatically frozen.

## 4. Failure Domain: Incident Intelligence Plane

If the Incident Intelligence plane fails (e.g., Gemini API outage or Consensus timeout), the system defaults to the **Platform Safety Boundary**. 

- **Intelligence Plane (Soft Fail)**: Returns a `RETRY_WITH_BACKOFF` or `HUMAN_ESCALATION` status.
- **Platform Plane (Hard Fail)**: The `SafetyGate` blocks all automated state-changes until the intelligence plane is recovered.

This separation ensures that a hallucination or failure in the AI layer never results in an unverified infrastructure change.
