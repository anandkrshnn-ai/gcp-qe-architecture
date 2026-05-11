# Sovereign-GCP: Byzantine-Fault-Tolerant Incident Analysis (PoC)

## ⚠️ Project Status: Proof-of-Concept (Research Only)
This repository is a technical reference implementation of **Byzantine Fault Tolerance (BFT)** in cloud-native incident response. It is **NOT** a production-ready platform.

### 🏛️ Core Research Goal
Can we build an autonomous SRE agent that maintains **Epistemic Safety** in a hostile cloud environment? 

This PoC focuses on the **Sovereign Fleet**: a distributed group of agents that use PBFT (Practical Byzantine Fault Tolerance) to agree on incident root causes before taking remediation actions. This prevents a single compromised telemetry source or agent from triggering catastrophic infrastructure changes.

### 🛠️ Current Capabilities (The Reality)
1.  **Simplified PBFT Prototype (v3.4.0)**: A research-grade consensus layer for agent agreement (Research Implementation).
2.  **Merkle-Chained WAL**: Cryptographically immutable state logging.
3.  **Hardened GKE Infrastructure**: Terraform with **Confidential Nodes** and **gVisor** enabled.
4.  **Agentic SRE Utility**: Gemini 1.5 Pro **Function Calling** with **Kubectl Patch** generation and **Dry-Run Validation**.

### 🛤️ The Path to "Principal" Depth (Active R&D)
- [ ] **Hardware Trust**: Moving from standard nodes to GKE Confidential Computing (SEV-SNP).
- [ ] **Real AI**: Replacing regex-based logic with Vertex AI (Gemini 1.5 Pro) for multimodal log/metric reasoning.
- [ ] **Policy Enforcement**: Integrating Binary Authorization for all agent images.

---
**Disclaimer**: This is a professional development portfolio designed to demonstrate distributed systems thinking and GCP-native engineering. All "Demo Reports" are generated within this PoC's controlled environment.
