# GCP Incident Analysis Demo

[![CI/CD Pipeline](https://github.com/anandkrshnn-ai/gcp-incident-analysis-demo/actions/workflows/main.yml/badge.svg)](https://github.com/anandkrshnn-ai/gcp-incident-analysis-demo/actions/workflows/main.yml)
[![Version](https://img.shields.io/badge/version-3.0.0--verified--soak-blue)](VERSION)

This repository provides a reference implementation showcasing secure, self-healing agentic architectures on Google Cloud. It demonstrates how autonomous remediation operations can be constrained under strict, deterministic safety gate boundaries, multi-agent voting quorums, and regex-based input sanitization.

> [!NOTE]
> **Educational Simulation Disclaimer**  
> This is an educational demonstration project and proof-of-concept. It is a simulation only and not production ready. It should not be used in real environments without significant additional hardening.

---

## 🛡️ Project Overview
This repository provides a local simulation harness demonstrating how multiple software agents can collaborate to analyze telemetry logs, validate remediation actions against static safety boundaries, and cryptographically sign off on state-changing operations. 

It serves as a clean architectural blueprint for developers looking to understand gate-based automation, threshold signatures, and input sanitization on Google Cloud.

## 🚀 Key Patterns Demonstrated
1. **Multi-Agent Voting Quorum**: Multiple agent identities are registered with public keys, requiring a majority threshold of cryptographic signatures before any action is approved.
2. **Deterministic Safety Gates**: Incident proposals are validated against local resource limits (e.g. replica count ceilings) and simulated cost thresholds.
3. **Regex Secret Scrubbing**: Demonstrates input filtering to redact Google API keys and sensitive tokens before passing telemetry payloads to LLM analyzers.
4. **Cloud KMS Adapter**: Provides a production-ready extension path showing how to sign payloads using Google Cloud Key Management Service (KMS) asymmetric keys.

## 🛠 Quick Start
First, install the local packages and dependencies:
```bash
pip install -e .[gcp,dev]
```

To run the simulation, we provide two entry point scripts:
1. **`run_golden_path.py` (Recommended First Step)**: Runs the complete end-to-end incident analysis loop (OOM logs ingestion, analysis, quorum signature check, safety gate validation, and simulated remediation) and outputs a signed verification package in `evidence/golden_path_attestation.json`.
   ```bash
   python run_golden_path.py
   ```
2. **`run_demo.py`**: A simpler CLI validation demo highlighting individual step components.
   ```bash
   python run_demo.py
   ```

## 🔍 Codebase Directory Tour

* **`src/safety/`**: Core validation components, including the threshold signature validator (`voting.py`), the quota evaluation engine (`safety_gate.py`), and the dry-run execution adapter (`remediator.py`).
  - **Ports & Adapters (`ports.py`)**: Declares decouple ports (`LogSourcePort`, `ActuationPort`) to isolate core safety logic from underlying cloud resources or logging frameworks.
* **`src/signing/`**: Cryptographic signing utilities, including the Cloud KMS adapter (`kms_signer.py`).
* **`tests/`**: Flat test suite directly in the root `tests/` directory (e.g. `test_safety.py`, `test_kms_signer.py`, `test_property_based.py`, etc.), eliminating unnecessary test taxonomy structures.

## ⚠️ Limitations & Real-world Gaps
For a detailed list of all simulator assumptions, transient caches, and production deployment requirements, please read the [LIMITATIONS.md](LIMITATIONS.md) file.

## 📈 Technical Evolution
To track the technical pivot, cleanups, and version changes, check the [Technical Evolution & Integrity Log (HISTORY.md)](HISTORY.md).
