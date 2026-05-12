# The Opinionated Safety Stack

This architecture defines a **Winning Default** for each plane, ensuring clear ownership and a single source of truth for autonomous governance.

## 1. The Stack Map

| Plane | Winning Default | Responsibility |
| :--- | :--- | :--- |
| **Compute** | **GKE (Autopilot)** | Isolated execution of agent pods using gVisor (Sandbox). |
| **Identity** | **Workload Identity** | Securely mapping Kubernetes service accounts to GCP IAM. |
| **Secrets** | **Secret Manager** | Hardened storage and automatic rotation of RSA keys. |
| **Observability** | **Cloud Logging** | Centralized Source of Truth for all agentic audit trails. |
| **Inference** | **Vertex AI (Gemini)** | LLM analysis with safety filter enforcement. |
| **Sanitization** | **Model Armor** | Proactive redaction of secrets/PII before consensus. |
| **Governance** | **Safety Gate** | Deterministic enforcement of resource and cost boundaries. |

## 2. Why This Stack?

- **Zero-Trust Identity**: By using **Workload Identity**, we eliminate the need for long-lived service account keys, reducing the blast radius of a compromised agent pod.
- **Unified Observability**: Rather than splitting telemetry across multiple vendors, we use **Cloud Logging** as the primary sink. This simplifies the `SafetyAnalyzer` logic and ensures audit trails are compliant with Google Cloud's data residency standards.
- **Deterministic Guardrails**: The **Safety Gate** sits at the end of the pipeline, ensuring that even if the AI (Vertex AI) suggests a high-risk action, the infrastructure boundaries are physically enforced.

## 3. Control Points & Ownership Boundaries

A governable platform is defined by clear ownership of its safety boundaries.

| Control Point | Mechanism | Ownership | Responsibility |
| :--- | :--- | :--- | :--- |
| **Provenance** | Workload Identity | Platform Team | Verifying that pods originate from the trusted GKE pool. |
| **Authorization** | RSA-PSS Quorum | Security Team | Cryptographic attestation of multi-agent agreement. |
| **Sanitization** | Model Armor | Privacy Team | Proactive enforcement of data-residency and PII policies. |
| **Boundary** | Safety Gate | SRE Team | Fiscal and resource quota enforcement. |

## 4. Platform vs. Quality Layer

This architecture makes a sharp distinction between the **Platform Plane** (GCP/GKE) and the **Quality Intelligence Layer** (The Agent Framework). 

- The **Platform** provides the *capabilities* (compute, logs, identity).
- The **Quality Layer** provides the *governance* (consensus, sanitization, safety gates).

Separating these layers ensures that the platform remains stable even as the AI models and safety policies evolve.
