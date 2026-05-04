# GCP QE Architecture

**A practical, executable reference for Quality Engineering on Google Cloud Platform.**

This repository provides a battle-tested baseline for engineers and architects managing **GKE, Cloud Run, Cloud SQL, and AI-powered observability**. It bridges the gap between infrastructure-as-code and automated quality gates.

---

## 🚀 Hero Flow: From Incident to Automated RCA
The core value of this repo is the integration of modern AI into the QE workflow.
1. **Infrastructure**: Deploy the [Modular Terraform Baseline](reference-implementations/terraform-baseline/).
2. **Observability**: Monitor with the [SLO Monitoring Stack](reference-implementations/slo-monitoring/).
3. **Intelligence**: Use the [Gemini RCA Agent](frameworks/gemini-agent-qe/) to analyze logs and recommend quality gates.

## 📖 Key Sections

- **[Case Studies](case-studies/)**: Deep-dives into GKE resilience and Cloud Run stabilization.
- **[Real-World Usage](docs/real-world-usage.md)**: Log of how these patterns are applied in professional environments.
- **[Frameworks](frameworks/)**: AI-QE agents, RAG evaluators, and Agentic AI quality practices.
- **[Tools](tools/)**: Python utilities for defect escape analysis and reliability metrics.
- **[Patterns & Checklists](patterns/)**: Production readiness checklists and QE strategy templates.

## 🛠️ Local Execution & Reproducibility
Every pattern in this repo is designed to be executable.
- **IaC**: `cd reference-implementations/terraform-baseline/environments/dev && terraform init`
- **AI Tools**: `pip install -r requirements.txt && python frameworks/gemini-agent-qe/tools/gemini-rca-agent.py`
- **Tests**: `pytest tools/ frameworks/`

## 📊 Reproducible Proofs (Evidence)
We maintain a [reproducible proofs directory](evidence/) containing actual execution logs and plan outputs to validate the current state of the architecture.

## 📖 Documentation Site
Full, searchable documentation is available at:  
[https://anandkrshnn-ai.github.io/gcp-qe-architecture/](https://anandkrshnn-ai.github.io/gcp-qe-architecture/)

---

## 🏗️ Project Maturity & Roadmap
This repository is a **living reference** used in a professional QA Architect Manager capacity. It is currently in a "Stabilized Baseline" phase.

### Roadmap
- **Q3 2026**: Automated Chaos Gates in Cloud Build.
- **Q4 2026**: MCP (Model Context Protocol) server testing patterns for Agentic AI.
- **Q1 2027**: Cross-cloud reliability benchmarks (GCP-AWS-Azure).

## 🤝 Contributing
Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to add new patterns or fix issues.

---
**Disclaimer**: This is a personal reference repository. All code and patterns should be reviewed and tested thoroughly in your own environment. No warranties provided.

**Author**: Anandakrishnan – QA Architect Manager
