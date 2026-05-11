# Sovereign-GCP: Projects Catalog (v3.7.1)

This catalog tracks the evolution of the Sovereign-GCP research portfolio. Every project here is a **Research Proof-of-Concept** designed to demonstrate Staff-level architectural thinking on Google Cloud.

## 🏛️ Engineering Portfolio

| Repository | Status | Primary Capability | Key Engineering Depth |
| :--- | :--- | :--- | :--- |
| **[Agentic Incident Analyzer](https://github.com/anandkrshnn-ai/gcp-qe-architecture)** | **Engineering Reference** | Multi-Agent Consensus | Gemini Tool-Calling, OpenTelemetry, GKE Hardening |
| **[Compliance-as-Code](https://github.com/anandkrshnn-ai/compliance-guardian)** | **Planned** | Real-time Policy Guardrails | Binary Authorization, OPA Gatekeeper |
| **[Secure Telemetry Lake](https://github.com/anandkrshnn-ai/data-sovereignty)** | **Conceptual** | Cryptographic Logging | Merkle-Chained WAL, SEV-SNP Isolation |

---

## 🔬 Core Repository Spotlight: Agentic Incident Analyzer
The foundational engine for the Sovereign-GCP portfolio.

*   **Objective**: Solve the "Single Point of Failure" in autonomous SRE agents.
*   **Engineering Depth**:
    *   **Consensus**: Uses a Quorum-based voting model to validate telemetry before remediation.
    *   **AI Reasoning**: Leverages Vertex AI (Gemini 1.5 Pro) for structured Kubernetes Patch generation.
    *   **Security**: Terraform-driven GKE hardening (Confidential Nodes + gVisor).
    *   **Observability**: Full OpenTelemetry (OTEL) tracing of the OODA loop.

## 🏁 Operational Metrics
The metrics mentioned in early design drafts (e.g., MTTR reductions) are **Architectural Targets**. This portfolio focuses on **Verifiable Implementation** rather than theoretical performance claims.
