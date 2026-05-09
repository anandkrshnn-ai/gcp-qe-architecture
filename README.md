# Sovereign-GCP: Incident Analyzer (PoC)

A working proof-of-concept for autonomous incident analysis on Google Cloud Platform.

## What This Is
This repository is a **Functional Proof-of-Concept** and **Architectural Reference** for building autonomous Quality Engineering (QE) systems on GCP. It focuses on parsing real-world telemetry patterns to identify root causes and remediations without requiring an LLM for basic control flow.

### 🚀 The 30-Second Win (Zero Credentials Needed)
Prove the logic works immediately on real GCP log structures:
```bash
python run_demo.py oomkill   # Scenario 1: GKE Pod OOM analysis
python run_demo.py latency   # Scenario 2: Cloud Run Timeout analysis
```

**What this demonstrates**:
- ✓ **Generalizable Logic**: Multi-scenario analysis via a pattern registry.
- ✓ **Real Data Patterns**: Logic is tested against **actual GCP log JSON payloads**.
- ✓ **Extensible Architecture**: Easy to add new incident types via the `SovereignAnalyzer`.

---

## 🛠️ Repository Substance

### 📂 Core Framework
- **[`frameworks/sovereign_core/`](frameworks/sovereign_core/)**: The extensible logic engine for incident parsing.
- **[`run_demo.py`](run_demo.py)**: The executable entry point for the architectural simulator.

### 📂 Infrastructure as Code (IaC)
- **[`terraform/`](terraform/)**: Production-grade Terraform modules for GKE, Cloud Run, and Networking. 
  - *Status: Reference material. Modular, secure, and structured for multi-environment deployment.*

### 📂 Engineering Guides
- [SLO/SLI Engineering](guides/02-slo-sli-engineering.md)
- [Production Readiness Checklist](guides/03-production-readiness.md)
- [Path to Production Deployment](guides/08-deployment-path.md)

---

## 🔍 Limitations & Intent
**This is NOT a turnkey production platform.** It is a high-fidelity simulator designed for:
1. **Architectural Study**: Understanding how to structure autonomous healing loops.
2. **SDK Reference**: Learning how to interact with real `google-cloud-sdk` patterns.
3. **Prototype Foundation**: A starting point for building real-world QE agents.

**Author**: Anandakrishnan Damodaran, Principal Architect
