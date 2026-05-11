# Agentic Incident Analyzer – Multi-Agent Consensus Research PoC

**A focused research project demonstrating agentic SRE patterns on Google Cloud.**

This repository implements a **multi-agent system** that ingests Kubernetes incidents, reasons using Gemini 1.5 Pro (with function calling), reaches consensus via a simplified voting mechanism, and generates safe, dry-run validated Kubernetes JSON patches.

**Status**: Research Proof-of-Concept (v3.7.0) — Not production ready.

## Key Capabilities

- Real Gemini 1.5 Pro integration with structured function calling + Pydantic validation
- Multi-agent consensus (simplified PBFT-inspired voting)
- Safe remediation proposal with dry-run validation using Kubernetes Python client
- Chaos engineering mode (fault injection + resilience testing)
- Hardened GKE reference Terraform (Confidential Nodes, gVisor, Binary Authorization)

---
**📂 Part of the [GCP Agentic Research Portfolio](https://github.com/anandkrshnn-ai/portfolio-overview)**
- **Next Project**: [AlloyDB-Grounded Local-First Agent](https://github.com/anandkrshnn-ai/alloydb-local-first-agent) — Focusing on sub-10ms decisioning.
---

## Quick Start

```bash
git clone https://github.com/anandkrshnn-ai/gcp-qe-architecture.git
cd gcp-qe-architecture
make demo          # Happy path
make chaos         # Resilience test
```

## Architecture

```mermaid
flowchart TD
    A[Incident Logs / Metrics] --> B[Analyzer Agent]
    B --> C[Gemini 1.5 Pro Reasoning\n(Function Calling)]
    C --> D[Multi-Agent Fleet\n(Consensus Voting)]
    D --> E[Remediator\n(JSON Patch + Dry-Run)]
    E --> F{Safety Gates}
    F -->|Pass| G[Approved Remediation Proposal]
    F -->|Fail| H[Quorum Reject + Alert]
    
    subgraph "GCP Hardened Runtime"
    I[Confidential GKE Nodes + gVisor]
    end
```

## Demo Outputs

**Happy Path** → Analyzes incident → Proposes safe patch  
**Chaos Mode** → Injects corrupted logs → Consensus rejects false diagnosis

*(Screenshots / terminal output included in `evidence/`)*

## Tech Stack

- **AI**: Gemini 1.5 Pro + Vertex AI SDK + Function Calling
- **Orchestration**: Pydantic + Multi-agent voting
- **Kubernetes**: Official Python client (dry-run patches)
- **Infrastructure**: Terraform + Confidential GKE + Binary Authorization
- **Quality**: 92%+ test coverage, Ruff, Chaos simulator

## Purpose

This project serves as a **reference implementation** for agentic SRE thinking — showing how to combine LLM reasoning, multi-agent consensus, and strict safety controls in regulated environments.
