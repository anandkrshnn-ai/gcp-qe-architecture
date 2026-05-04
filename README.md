# GCP QE Architecture

**A practical, executable reference for Quality Engineering on Google Cloud Platform.**

This repository provides a battle-tested baseline for engineers and architects managing **GKE, Cloud Run, Cloud SQL, and AI-powered observability**. 

---

## 🚀 Hero Flow: From Incident to Automated RCA
The core value of this repo is the integration of modern AI into the QE workflow.

### 1. Execute AI RCA Locally (No GCP Required)
You can test the Gemini RCA Agent immediately using mock logs:
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

### 3. Terraform Baseline
Review the [Modular Terraform Baseline](reference-implementations/terraform-baseline/). It is structured for multi-environment rollout and includes `terraform.tfvars.example` files for immediate use in your own projects.

---

## 📖 Key Sections

- **[Case Studies](case-studies/)**: Deep-dives into GKE resilience and Cloud Run stabilization.
- **[Frameworks](frameworks/)**: AI-QE agents, RAG evaluators, and Agentic AI quality practices.
- **[Tools](tools/)**: Python utilities for defect escape analysis and reliability metrics.
- **[Reproducible Proofs](evidence/)**: Actual execution logs and plan outputs validating the architecture.

## 📖 Documentation Site
Full, searchable documentation is available at:  
[https://anandkrshnn-ai.github.io/gcp-qe-architecture/](https://anandkrshnn-ai.github.io/gcp-qe-architecture/)

---

## 🤝 Contributing
Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Author**: Anandakrishnan – QA Architect Manager
