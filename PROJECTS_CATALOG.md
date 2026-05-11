# Sovereign-GCP: Projects Catalog

This catalog tracks the evolution of the Sovereign Cloud Engineering portfolio. 

## 1. Sovereign-Core (Active)
**Role**: The Byzantine-Fault-Tolerant Engine.
- **Goal**: Proving that autonomous agents can reach consensus on "Truth" using PBFT.
- **Current State**: Python-based consensus logic + Merkle state store.
- **Gap**: Missing real Vertex AI integration for log reasoning.

## 2. GKE Hardening (Planned)
**Role**: The Hardware Root of Trust.
- **Goal**: Secure the runtime environment for Sovereign-Core.
- **Expected Features**: GKE Confidential Nodes, Binary Authorization, Network Policies (Cilium).
- **Current State**: Basic GKE Terraform only.

## 3. Data-Sovereignty (Conceptual)
**Role**: Secure Telemetry Ingestion.
- **Goal**: End-to-end encryption of logs from source to agent.
- **Status**: **Conceptual**. No code exists yet.

---

## 🔬 Research & Development Notes
The "Masterpiece" metrics mentioned in earlier design drafts (e.g., 78% MTTR) are **Performance Targets** for a hypothetical production system, not measured results from this PoC. 

This repository is dedicated to the **Engineering Process**—proving individual BFT and security invariants one commit at a time.
