# GCP QE Architecture

**A practical, executable reference for Quality Engineering on Google Cloud Platform.**

![System Verification](https://github.com/anandkrshnn-ai/gcp-qe-architecture/actions/workflows/system-verification.yml/badge.svg)
![Terraform Validate](https://github.com/anandkrshnn-ai/gcp-qe-architecture/actions/workflows/terraform-validate.yml/badge.svg)
![Python Tools](https://github.com/anandkrshnn-ai/gcp-qe-architecture/actions/workflows/python-tools.yml/badge.svg)

This repository provides a battle-tested baseline for engineers and architects managing **GKE, Cloud Run, Cloud SQL, and AI-powered observability**.

---

## ✅ Verified by CI: "Always Runnable" Policy
We enforce a strict "Always Runnable" policy. Our CI pipeline validates every commit:
- **AI RCA Agent**: Verified in mock mode using sample log datasets.
- **Performance Suite**: k6 suite verified against a local mock server.
- **Terraform Baseline**: `validate` and `fmt` checks passed across all environments (dev/staging/prod).

---

## 🚀 Hero Flow: Run Locally in 5 Minutes

### 1. Execute AI RCA Locally (No GCP Required)
Test the Gemini RCA Agent immediately using mock logs:
```bash
pip install -r requirements.txt
python frameworks/gemini-agent-qe/tools/gemini-rca-agent.py --mock frameworks/gemini-agent-qe/tools/sample_logs.json
```

### 2. Run Performance Tests Locally
Validate the k6 suite using the included mock server:
```bash
# Terminal 1: Start mock server
node tools/mock-server/server.js

# Terminal 2: Run k6
k6 run reference-implementations/k6-performance/cloud-run-load-test.js
```

---

## 📖 Key Sections

- **[Case Studies](case-studies/)**: Deep-dives into GKE resilience and Cloud Run stabilization.
- **[Frameworks](frameworks/)**: AI-QE agents, RAG evaluators, and Agentic AI quality practices.
- **[Tools](tools/)**: Python utilities for defect escape analysis and reliability metrics.
- **[Reproducible Proofs](evidence/)**: Actual execution logs and plan outputs validating the architecture.

## 📖 Documentation Site
Full documentation and guides are available at:  
[https://anandkrshnn-ai.github.io/gcp-qe-architecture/](https://anandkrshnn-ai.github.io/gcp-qe-architecture/)

---

## 🤝 Contributing
Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Author**: Anandakrishnan – QA Architect Manager
