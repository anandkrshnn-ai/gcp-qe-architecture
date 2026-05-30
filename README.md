# Agent Safety Patterns for Multi-Agent Systems on GCP

**Traceable Reference Architecture (v8.2.1)**

**The Thesis**: Autonomous agents require traceable, policy-bound governance before any state-changing action. This repository defines a layered safety architecture that prioritizes **verifiable control points, deterministic boundaries, and auditable recovery paths**. This architecture prioritizes **traceability over certainty**, ensuring that every autonomous action is bounded by explicit policy and human-in-the-loop overrides.

---

Hardened framework for cryptographic consensus, resource-aware safety gates, and Model Armor sanitization for autonomous agents on Google Cloud Platform.

## 📋 Principal Reviewer TL;DR

```
  ┌────────────────────────────────────────────────────────────┐
  │                   PORT / ADAPTER BOUNDARY                  │
  │                                                            │
  │   [ GCP / Telemetry ] ──────> [ LogSourcePort ]            │
  │                                     │                      │
  │                                     ▼                      │
  │                            [ Safety Core Loop ]            │
  │                                     │                      │
  │                                     ▼                      │
  │   [ GCP / Actuators ] <────── [ ActuationPort ]            │
  └────────────────────────────────────────────────────────────┘
```

* **Core Decoupling**: Safety intelligence is separated from cloud environment interactions through explicit interfaces defined in `ports.py` (`LogSourcePort` and `ActuationPort`).
* **RSA-PSS Attestation Profile**: Cryptographic signature validation is executed inside the Remediator using SHA-256 digests and RSA-PSS padding with `salt_length=padding.PSS.MAX_LENGTH`. Quorum verification fails closed, blocking all actuation unless verified.
* **CI/CD Validation Gates**: Terraform manifests are validated in CI/CD via syntax/structure verification (`terraform validate`), layout enforcement (`terraform fmt -check`), and provider-specific best practice checks via `TFLint`. Python code is validated with 18 distinct test suites categorized into a 3-tier taxonomy.

## 🔍 Principal Reviewer Tour (7-Minute Guide)

This walkthrough highlights the architectural control points for auditing the repository.

### ⏱️ Minute 1-2: Core Interface Decoupling (Ports & Adapters)
Open [ports.py](file:///c:/Users/Admin/Documents/Github/gcp-qe-architecture/src/safety_core/ports.py) to audit the primary interface boundary:
- **`LogSourcePort`**: Abstracts metric telemetry and logging reads, preventing Vertex AI analyzer classes from coupling directly to GCP APIs.
- **`ActuationPort`**: Restricts active state modifications, implemented by `DryRunRemediator` (located in [remediator.py](file:///c:/Users/Admin/Documents/Github/gcp-qe-architecture/src/safety_core/remediator.py)) to decouple external GKE/Cloud Run triggers from the core evaluation loop.

### ⏱️ Minute 3-4: Fail-Closed Cryptographic Verification
Open [remediator.py](file:///c:/Users/Admin/Documents/Github/gcp-qe-architecture/src/safety_core/remediator.py) and view `verify_remediation_signatures()`:
- Remediation proposals are rejected immediately if signature consensus fails.
- Replay attacks are stopped before entering Safety evaluation by verifying unique nonces and enforcing clock skew validation inside [consensus.py](file:///c:/Users/Admin/Documents/Github/gcp-qe-architecture/src/safety_core/consensus.py).

### ⏱️ Minute 5-6: Test Taxonomy & Multi-Tier Audit
Tests are partitioned under `tests/` to align with the deployment and actuation cycle:
1. **Pre-Deploy Hygiene (`tests/pre_deploy/`)**: Focuses on core functionality like `test_safety_core.py` and authenticity scorer evaluations in `test_authenticity.py`.
2. **Pre-Actuation Verification (`tests/pre_actuation/`)**: Runs adversarial simulation tests (`test_adversarial.py`) and property-based verification checks (`test_property_based.py`) verifying boundary states.
3. **Post-Incident Recovery Gates (`tests/post_incident/`)**: Verifies recovery policies and rollback triggers (`test_recovery.py`) when regression metrics exceed thresholds.

### ⏱️ Minute 7: CI/CD Enforcement & Infrastructure Linting
Audit [.github/workflows/terraform-validate.yml](file:///c:/Users/Admin/Documents/Github/gcp-qe-architecture/.github/workflows/terraform-validate.yml) and the [terraform/.tflint.hcl](file:///c:/Users/Admin/Documents/Github/gcp-qe-architecture/terraform/.tflint.hcl) files.
CI guarantees:
- Syntactically correct configurations (`terraform validate`).
- Properly formatted code (`terraform fmt -check`).
- Strict best practices and provider rules checking via `tflint`.

---

## 🔑 RSA-PSS Cryptographic Verification Profile

To guarantee consistent interoperability and security across reference implementations, the safety core enforces the following signature validation parameters:

| Parameter | Configuration / Setting |
|---|---|
| **Padding Scheme** | RSA Probabilistic Signature Scheme (RSA-PSS) |
| **Mask Generation Function** | MGF1 configured with SHA-256 |
| **Hash Algorithm** | SHA-256 |
| **Salt Length** | Set dynamically to maximum size (`padding.PSS.MAX_LENGTH`) |
| **Fail-Closed Behavior** | Actuator fails closed immediately. Any consensus verification exception, quorum shortage, or signature mismatch blocks state modifications. |

---

## 🛡️ Problem Statement
Autonomous agents can exhibit destructive behaviors if left ungoverned. This repository demonstrates a layered, verifiable safety architecture that enforces multi-agent consensus and deterministic resource boundaries before any state-changing operation occurs.

## 🛠 Quick Start
```bash
# Install dependencies (including tenacity, vertexai)
pip install -e .[gcp,dev]

# Run reference simulation
python run_demo.py

# Run with Real Vertex AI (requires GCP ADC)
python run_demo.py --real --project YOUR_PROJECT_ID
```

## 🧪 Verification
The system is verified using:
- **Property-Based Testing**: Validating consensus resilience under clock-skew and nonce collision scenarios.
- **End-to-End Integration**: Full Analysis -> Consensus -> Safety pipeline verification.
- **Standardized Logging**: Structured, high-fidelity audit trails without cryptographic leakage.

## 📝 Compliance & Safety
- **Vertex AI Safety Filters**: BLOCK_ONLY_HIGH thresholds for professional autonomy.
- **Data Privacy**: Local Model Armor redaction of GCP API keys and secrets.
