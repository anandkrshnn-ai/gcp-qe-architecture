# The Quality Intelligence Layer

While the platform provides the infrastructure, the **Quality Intelligence Layer** provides the governance and verification. This layer is responsible for the interpretation of signals and the enforcement of safety.

## 1. Quality Intelligence Taxonomy

We categorize quality engineering into five distinct levels of verification, ensuring the AI-driven OODA loop is both accurate and safe.

| Level | Scope | Verification Mechanism |
| :--- | :--- | :--- |
| **Contract** | API Schema Alignment | Pydantic validation of `Finding` and `ActionProposal` objects. |
| **Synthetic** | RCA Accuracy | Replaying historical incident logs into the `SafetyAnalyzer`. |
| **Property** | Logic Resilience | **Hypothesis** property-based tests for quorum and nonce logic. |
| **Adversarial** | Security Hardening | Red-team suites for signature forgery and replay attacks. |
| **Drift** | Model Consistency | Quarterly benchmark runs to detect Gemini output regression. |

## 2. The Verification Workflow

Quality is not a post-facto audit; it is a **pre-actuation gate**.

1. **Static Analysis**: Ruff and Pydantic enforce schema integrity before an agent is allowed to sign a proposal.
2. **Logic Proof**: Property-based tests prove that the `ConsensusGuardian` is mathematically sound under extreme clock-skew (±60s).
3. **Adversarial Gate**: The test suite includes intentional forgery attempts. If the system fails to block a forged signature, the CI/CD pipeline is automatically frozen.

## 3. Failure Domain: Quality Intelligence Plane

If the Quality Intelligence plane fails (e.g., Gemini API outage or Consensus timeout), the system defaults to the **Platform Safety Boundary**. 

- **Intelligence Plane (Soft Fail)**: Returns a `RETRY_WITH_BACKOFF` or `HUMAN_ESCALATION` status.
- **Platform Plane (Hard Fail)**: The `SafetyGate` blocks all automated state-changes until the intelligence plane is recovered.

This separation ensures that a hallucination or failure in the AI layer never results in an unverified infrastructure change.
