# GCP Incident Analysis Demo

This is an **educational demonstration project** and proof-of-concept for multi-agent incident analysis using Gemini on Google Cloud. It is a **simulation only** and **not production ready**. It should not be used in real environments without significant additional hardening.

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
```bash
# Install dependencies
pip install -e .[gcp,dev]

# Run the incident analysis simulation
python run_golden_path.py

# Run the basic demo
python run_demo.py
```

Running `run_golden_path.py` outputs the step-by-step simulation run and generates a verification package in:
* `evidence/golden_path_attestation.json`

## 🔍 Codebase Directory Tour

* **`src/safety/`**: Core validation components, including the threshold signature validator (`voting.py`), the quota evaluation engine (`safety_gate.py`), and the dry-run execution adapter (`remediator.py`).
* **`src/signing/`**: Cryptographic signing utilities, including the Cloud KMS adapter (`kms_signer.py`).
* **`tests/`**: Flat test suite directly in the root `tests/` directory (e.g. `test_safety.py`, `test_kms_signer.py`, `test_property_based.py`, etc.), eliminating unnecessary test taxonomy structures.

## ⚠️ Limitations & Real-world Gaps
For a detailed list of all simulator assumptions, transient caches, and production deployment requirements, please read the [LIMITATIONS.md](LIMITATIONS.md) file.
