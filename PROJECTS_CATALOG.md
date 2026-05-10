# GCP Agentic Frameworks: Project Catalog & Roadmap

This document serves as the high-level technical roadmap for the agentic tools built on the Sovereign-Core engine. These projects represent the transition from the current functional PoC to production-grade automated systems.

---

## 1. Automated Incident Analyzer (Refined)
**Goal**: A reasoning layer for GKE and Cloud Run that assists SREs in root-cause analysis.
- **Core Technology**: Gemini 1.5 Flash (Reasoning), Vertex AI Reasoning Engine, Cloud Logging.
- **Key Pattern**: "Reasoning Loops" where the agent analyzes a failure and proposes a structured remediation plan for human approval.
- **Path to Real**: Expand the `SovereignActuator` with full Kubernetes Python SDK support for live patching.

## 2. Agentic Supply Chain Orchestration
**Goal**: Multi-agent coordination for identifying and alerting on supply chain disruptions.
- **Core Technology**: LangGraph (Multi-agent orchestration), Vertex AI, AlloyDB.
- **Key Pattern**: Specialized agents (Risk, Logistics, Inventory) sharing a common state to provide a unified risk view to human operators.
- **Path to Real**: Build a Graph-based state machine that coordinates between specialized Gemini-powered agents.

## 3. Multimodal Compliance Auditor
**Goal**: Policy monitoring for regulated environments.
- **Core Technology**: Gemini Multimodal (Vision/Video), Cloud Asset Inventory.
- **Key Pattern**: Scanning Infrastructure-as-Code (Terraform) and comparing it against actual deployed state to detect non-compliant drift.
- **Path to Real**: Use Gemini's vision capabilities to audit architectural diagrams against real-world deployment snapshots.

## 4. High-Performance Agentic Analytics
**Goal**: Low-latency data access for reasoning agents.
- **Core Technology**: DuckDB, Apache Arrow, BigQuery Managed Storage.
- **Key Pattern**: Agents pulling data "slices" into local memory using Arrow Flight SQL to minimize reasoning latency during high-pressure incidents.
- **Path to Real**: Implement the `AgenticLakehouse` logic to fetch BQ data into DuckDB for local LLM context processing.

## 5. Secure Agent Runtime
**Goal**: Secure, isolated execution environments for autonomous agents.
- **Core Technology**: GKE Sandbox (gVisor), VPC Service Controls.
- **Key Pattern**: Isolating agent execution in a restricted runtime to prevent potential prompt injection from impacting the wider infrastructure.
- **Path to Real**: Deploy the `SovereignClient` inside a GKE Sandbox with strictly scoped IAM Workload Identity.

## 6. Hybrid Reasoning Layer (Gemma + Gemini)
**Goal**: Optimize cost and latency by routing diagnostic tasks between Local and Cloud models.
- **Core Technology**: Gemma 4 (Local Inference on GKE), Vertex AI (Cloud Reasoning), GKE Model Serving.
- **Key Pattern**: "Triage Routing" – Local Gemma models handle 80% of routine telemetry filtering and PII masking, escalating only complex "Black Swan" events to Gemini 1.5 Pro.
- **Path to Real**: Deploy a Gemma serving endpoint on GKE (via vLLM or TGI) and update the `SovereignAnalyzer` with a multi-model routing logic.

---

## 🛠️ Implementation Priorities
To move these frameworks into a production environment:
1. **State Persistence**: Transition from stateless scripts to Firestore-backed memory.
2. **Human-in-the-Loop (HITL)**: Mandatory approval gates for all destructive actions.
3. **Telemetry**: OpenTelemetry integration to track "Agent Reasoning" in Cloud Trace.
4. **Security**: Implementation of Model Armor for input/output sanitization.
