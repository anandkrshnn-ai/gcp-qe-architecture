# Agent Safety Patterns – Multi-Agent Consensus Research PoC

**A focused research project exploring defensible safety patterns for AI agents on Google Cloud.**

This repository implements an **architecture reference** for adding safety gates to autonomous agentic loops. It demonstrates how to move beyond "single-agent black boxes" by using **cryptographic consensus**, **resource quotas**, and **verifiable attestation**.

**Status**: Research Proof-of-Concept (v7.0.0) — Focus on Patterns, not Production.

## Core Engineering Patterns

### 1. Verifiable Majority Consensus
- **Pattern**: Agents sign their proposals using individual RSA keys.
- **Rigor**: A `ConsensusGuardian` verifies that a 2/3 majority of unique, authorized agents have signed the exact same proposal hash before any action is taken.
- **Benefit**: Prevents a single compromised or "hallucinating" agent from taking destructive actions.

### 2. Strict Resource Quotas (Safety Gates)
- **Pattern**: Deterministic validation of agent-generated patches against hard-coded resource limits (CPU, Memory, Replicas).
- **Rigor**: Any proposal exceeding the `SafetyConfig` or attempting blocked operations (e.g., `DELETE`) is rejected before execution.

### 3. Verifiable Runtime Attestation
- **Pattern**: Simulated "Hardware-Rooted" trust.
- **Rigor**: Uses RSA digital signatures to verify that the agent's runtime environment is authorized by the trusted platform.

## Architecture

```mermaid
flowchart TD
    A[Telemetry / Metrics] --> B[Multi-Agent Fleet]
    B --> C[RSA Signing of Proposals]
    C --> D[Consensus Guardian\n(Verifiable Quorum)]
    D --> E{Safety Gate\n(Resource Quotas)}
    E -->|Pass| F[Dry-Run Remediation]
    E -->|Fail| G[Rejection + Audit Log]
    
    subgraph "Safety Core"
    D & E
    end
```

## Tech Stack

- **Security**: Python `cryptography` (RSA PSS, SHA256)
- **Validation**: Pydantic v2 (Strict schemas)
- **AI**: Gemini 1.5 Pro (Function calling for triage)
- **Orchestration**: Custom Safety-Core framework

---
**📂 Part of the [GCP Agentic Research Portfolio](https://github.com/anandkrshnn-ai/portfolio-overview)**
- **Related Project**: [AlloyDB Local-First Agent](https://github.com/anandkrshnn-ai/alloydb-local-first-agent) — Focusing on low-latency grounding.
---

**Disclaimer**: This project is an architectural pattern reference. It is designed to demonstrate **safety mechanisms** in agentic systems and is not a production-grade fault-tolerant system.
