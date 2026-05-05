# GCP QE Architecture

**Production-grade Quality Engineering patterns for cloud modernization.**

Built and maintained by a **QA Architecture Manager** specializing in GCP modernization — GKE, Cloud Run, Cloud SQL, Observability, and AI-powered quality systems.

![System Verification](https://github.com/anandkrshnn-ai/gcp-qe-architecture/actions/workflows/system-verification.yml/badge.svg)
![Terraform Validate](https://github.com/anandkrshnn-ai/gcp-qe-architecture/actions/workflows/terraform-validate.yml/badge.svg)
![Python Tools](https://github.com/anandkrshnn-ai/gcp-qe-architecture/actions/workflows/python-tools.yml/badge.svg)

---

## What This Is

A reference architecture for Quality Engineering on GCP. Not a tutorial—a working baseline with executable code, real test evidence, and industry-standard documentation that can be adapted to real modernization projects.

**Suitable for**: QA architects, SREs, platform engineers, and engineering leaders managing GCP modernization programs.

---

## Quick Reference

### 📚 Core Guides (Start Here)

Industry-standard, cloud-agnostic principles. No proprietary content.

| Guide | What You'll Learn |
|-------|------------------|
| [01 · QE Architecture Framework](guides/01-quality-engineering-architecture.md) | How to design quality as a platform capability, not a testing phase |
| [02 · SLO/SLI Engineering](guides/02-slo-sli-engineering.md) | From SLI definition to burn-rate alerting and error budget policy |
| [03 · Production Readiness](guides/03-production-readiness.md) | DORA-based quality gates, release governance, and the readiness checklist |
| [04 · AI-Powered Quality Engineering](guides/04-ai-powered-quality-engineering.md) | LLM-based RCA agents, RAG for observability, evaluation frameworks |

---

### 📋 Enterprise Templates (Copy and Adapt)

Drop-in templates for production engineering teams.

| Template | Use Case |
|----------|---------|
| [Architecture Decision Record (ADR)](templates/adr-template.md) | Document and track significant technical decisions |
| [NFR Specification](templates/nfr-spec-template.md) | Define performance, reliability, security, and operational requirements |
| [Test Strategy](templates/test-strategy-template.md) | Comprehensive test planning across all test levels |
| [Incident Post-Mortem](templates/incident-postmortem-template.md) | Blameless review format with timeline, RCA, and action items |
| [Release Readiness Checklist](templates/release-readiness-checklist.md) | Go/No-Go framework with hard gates and error budget checks |

---

### 🏗️ Reference Implementations (Deployable Code)

| Implementation | What It Provides |
|----------------|-----------------|
| [Terraform Baseline](reference-implementations/terraform-baseline/) | Modular, multi-environment IaC for GKE, Cloud Run, Cloud SQL |
| [Hardened Cloud Run Module](reference-implementations/terraform-baseline/modules/cloud-run/main.tf) | Production-grade Cloud Run with scaling, probes, and resource limits |
| [SLO Monitoring](reference-implementations/slo-monitoring/) | Terraform-defined SLOs for GKE, Cloud Run, and Cloud SQL |
| [k6 Performance Suite](reference-implementations/k6-performance/) | Load test + cold-start test scripts with defined SLO thresholds |
| [Observability Stack](reference-implementations/observability-stack/) | Cloud Monitoring dashboards and alert policies |

---

### 🤖 AI/QE Frameworks

| Framework | Description |
|-----------|-------------|
| [Gemini RCA Agent](frameworks/gemini-agent-qe/) | AI-powered Root Cause Analysis using Vertex AI (Gemini 1.5 Pro) |
| [Sovereign AI RCA](frameworks/sovereign-ai-qe/) | Privacy-preserving RCA using local LLMs + PTV attestation |
| [RAG Evaluator](frameworks/agentic-ai-qe/) | Quantitative evaluation framework for RAG-based QE systems |

---

### 📂 Case Studies

Real-world QE problems and solutions.

- [GKE Resilience Improvement](case-studies/gke-resilience-improvement.md) — Pod disruptions, node pool hardening, AI-assisted RCA
- [Cloud Run Performance Stabilization](case-studies/cloud-run-performance-stabilization.md) — Cold start mitigation, concurrency tuning, k6 gates
- [Sovereign AI RCA Integration](case-studies/sovereign-ai-rca.md) — Privacy-preserving quality engineering for regulated industries

---

## Getting Started

### Run the AI RCA Agent Locally (No GCP Required)

```bash
git clone https://github.com/anandkrshnn-ai/gcp-qe-architecture.git
cd gcp-qe-architecture
pip install -r requirements.txt

# Gemini agent (mock mode — no credentials needed)
python frameworks/gemini-agent-qe/tools/gemini-rca-agent.py \
  --mock frameworks/gemini-agent-qe/tools/sample_logs.json

# Sovereign AI agent (requires Ollama)
ollama pull llama3
python frameworks/sovereign-ai-qe/tools/sovereign-rca-agent.py \
  --logs frameworks/gemini-agent-qe/tools/sample_logs.json
```

### Run Performance Tests Locally

```bash
# Start mock server
node tools/mock-server/server.js

# Load test (separate terminal)
k6 run reference-implementations/k6-performance/cloud-run-load-test.js

# Cold-start test
k6 run reference-implementations/k6-performance/cold-start-test.js
```

### Deploy the Terraform Baseline

```bash
cd reference-implementations/terraform-baseline/environments/dev
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your GCP project_id
terraform init && terraform plan
```

See [QUICKSTART.md](QUICKSTART.md) for the full step-by-step guide.

---

## Real-World Application Patterns

### Pattern 1: New Service Launch
1. Complete [NFR Specification](templates/nfr-spec-template.md) with performance targets.
2. Create [Test Strategy](templates/test-strategy-template.md) covering all test levels.
3. Deploy using [Terraform Baseline](reference-implementations/terraform-baseline/).
4. Validate with [k6 Performance Suite](reference-implementations/k6-performance/).
5. Complete [Release Readiness Checklist](templates/release-readiness-checklist.md) before launch.

### Pattern 2: Production Incident Response
1. Use [Gemini RCA Agent](frameworks/gemini-agent-qe/) for automated log analysis.
2. Document findings using [Post-Mortem Template](templates/incident-postmortem-template.md).
3. Track action items against the [Production Readiness Guide](guides/03-production-readiness.md).

### Pattern 3: Architecture Decision
1. Research options using [QE Architecture Guide](guides/01-quality-engineering-architecture.md).
2. Document decision using [ADR Template](templates/adr-template.md).
3. Define reliability targets using [SLO/SLI Guide](guides/02-slo-sli-engineering.md).

---

## Evidence

All claims in this repository are backed by execution artifacts:
- [Terraform Plan Output](evidence/terraform/terraform-plan-dev.txt) — 12-resource dev environment plan
- [k6 Performance Report](evidence/k6/k6-load-test-report.txt) — P95: 192.8ms, 4,582 requests, 0 failures

---

## Documentation Site

Full documentation: [https://anandkrshnn-ai.github.io/gcp-qe-architecture/](https://anandkrshnn-ai.github.io/gcp-qe-architecture/)

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for standards and guidelines.

**Author**: Anandakrishnan · QA Architecture Manager · GCP Modernization
