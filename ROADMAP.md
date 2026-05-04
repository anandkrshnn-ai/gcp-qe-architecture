# Project Roadmap

This roadmap outlines the evolution of the `gcp-qe-architecture` repository from a personal baseline to a community-standard reference for GCP Quality Engineering.

## ✅ Phase 1: Foundation (Completed - May 2026)
- [x] Modular Terraform baseline for GKE, Cloud Run, and Cloud SQL.
- [x] Initial Gemini RCA Agent and RAG Evaluator prototypes.
- [x] Basic CI/CD integration with Cloud Build.
- [x] Multi-environment support (dev/staging/prod).
- [x] MkDocs documentation site deployment.

## 🚧 Phase 2: Depth & Reliability (In Progress - Q3 2026)
- [ ] **Automated Chaos Gates**: Integrate Chaos Mesh with Cloud Build to fail pipelines if resilience targets aren't met.
- [ ] **Terraform Hardening**: Add `tfsec` and OPA policy enforcement as mandatory gates.
- [ ] **Agentic AI Maturity**: Expand the Gemini Agent with tool-calling capabilities and conversation memory.
- [ ] **Advanced RAG Eval**: Integration with Vertex AI Gen AI Evaluation service for systematic hallucination scoring.

## 🔭 Phase 3: Industry Alignment (Q4 2026 - Q1 2027)
- [ ] **MCP Server QA**: Standardized testing patterns for Model Context Protocol servers.
- [ ] **Cross-Cloud Patterns**: Quality strategies for multi-cloud deployments (GCP + AWS/Azure).
- [ ] **Community Adoption**: Open for PRs from the wider GCP community; refined issue templates and contribution guidelines.

---
*Roadmap updated regularly based on real-world engineering requirements.*
