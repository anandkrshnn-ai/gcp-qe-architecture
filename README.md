# GCP Incident Analyzer (PoC)
A working proof-of-concept for log analysis patterns on Google Cloud Platform.

## What This Is
This repository is a **Functional Proof-of-Concept** and **Baseline Reference** for building incident analysis tools on GCP.

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

### 📂 Core Components
- **[`src/sovereign_core/`](src/sovereign_core/)**: The primary Python engine (Client, Analyzer, LLM Skeleton).
- **[`terraform/`](terraform/)**: Production-grade IaC for GKE, IAM, and Networking.
- **[`PROJECTS_CATALOG.md`](PROJECTS_CATALOG.md)**: The strategic roadmap for Sovereign AI (ASCO, Compliance, etc.).

### 🚀 Get Started in 30 Seconds
```bash
# Clone and enter
git clone https://github.com/anandkrshnn-ai/gcp-qe-architecture
cd gcp-qe-architecture

# Install as a package
pip install -e .

# Run the Simulator
python run_demo.py oomkill
```
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

**Author**: Anandakrishnan Damodaran, Architect
