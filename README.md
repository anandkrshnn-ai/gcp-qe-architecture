# GCP QE Architecture

![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![GKE](https://img.shields.io/badge/GKE-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-8E75F7?style=for-the-badge&logo=google&logoColor=white)

> Practical, production-focused Quality Engineering patterns for GCP.

**📖 View as Documentation Site**: [https://anandkrshnn-ai.github.io/gcp-qe-architecture/](https://anandkrshnn-ai.github.io/gcp-qe-architecture/) (after enabling GitHub Pages)

## Quick Navigation

- [Terraform Baseline](reference-implementations/terraform-baseline/)
- [End-to-End Example](examples/end-to-end-observable-app/)
- [Tools](tools/)
- [Patterns & Checklists](patterns/)
- [Evidence](evidence/)

Focused reference covering **GKE, Cloud Run, Cloud SQL, Observability, Resilience, and Modern AI Quality** (Gemini Agents + Agentic AI / RAG / MCP).

### Purpose
This repository contains patterns, implementations, and practices I use and refine as a **QA Architect Manager** on GCP. 

**Scope is deliberately narrow** — only high-impact areas that matter in real production environments.

### What's Inside

- **reference-implementations/** — Executable Terraform, k6, chaos experiments
- **guides/** — Practical service-level quality guides
- **frameworks/** — Gemini Agent QE + Agentic AI Quality
- **tools/** — Small, useful automation scripts
- **evidence/** — Screenshots, outputs, and real execution results

### Quick Start

```bash
git clone https://github.com/anandkrshnn-ai/gcp-qe-architecture.git
cd gcp-qe-architecture
```

Then explore:
- [Terraform Baseline](reference-implementations/terraform-baseline/)
- [GKE Testing Guide](guides/gke-testing-guide.md)
- [Gemini Agent QE](frameworks/gemini-agent-qe/)
- [End-to-End Observable App Example](examples/end-to-end-observable-app/)

## Key Patterns

- [Production Readiness Checklist](patterns/production-readiness-checklist.md)
- Modular Terraform Baseline
- Gemini-powered RCA
- Agentic AI Quality Framework

## CI/CD Validation

This repository uses GitHub Actions to automatically validate Terraform code on every push/PR.

## Evidence

See [`evidence/`](evidence/) folder for:
- Terraform plan/apply outputs
- k6 test reports
- Chaos experiment results
- Gemini Agent outputs

## Repository Maturity (Day 11)

**Completed**:
- Modular Terraform Baseline
- Service Quality Guides (GKE, Cloud Run, Cloud SQL)
- Working k6 Performance Suite
- Gemini RCA Agent + Agentic AI / RAG QA
- Production Readiness Checklist
- End-to-End Example
- Defect Escape Analyzer

**Still Evolving**: Real job usage documentation (will be added as I apply these patterns at work).

### Disclaimer
This is a **personal reference repository**. All patterns should be reviewed, tested, and adapted to your environment. No guarantees — use at your own risk.

**Last Updated:** May 2026

---

Made by Anandakrishnan – QA Architect Manager
