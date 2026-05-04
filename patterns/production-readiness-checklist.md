# Production Readiness Review Checklist (GCP QE)

Use this before every major release or Go-Live.

### 1. Infrastructure & Security
- [ ] Terraform baseline applied and validated
- [ ] Workload Identity enabled (no default service accounts)
- [ ] Network policies and Pod Security Standards enforced
- [ ] Secrets managed via Secret Manager
- [ ] Vulnerability scanning enabled (Container Analysis)

### 2. Observability
- [ ] Golden Signals monitored (Latency, Traffic, Errors, Saturation)
- [ ] SLOs defined and alerting configured
- [ ] Cloud Logging sink to BigQuery enabled
- [ ] Gemini RCA Agent integrated for incidents

### 3. Resilience & Chaos
- [ ] Chaos experiments executed (pod-kill, network latency)
- [ ] Failover tested (Cloud SQL, GKE multi-zone)
- [ ] Backup & restore validated

### 4. Performance & Quality Gates
- [ ] k6 performance tests passing in CI
- [ ] Load test results within SLOs
- [ ] Canary deployment strategy ready

### 5. Security & Compliance
- [ ] Workload Identity enabled (no default service accounts)
- [ ] Secrets managed via Secret Manager
- [ ] Vulnerability scanning enabled (Container Analysis)
- [ ] Binary Authorization enforced (if applicable)

### 6. Agentic AI / RAG (if applicable)
- [ ] RAG evaluation scores above threshold
- [ ] Hallucination guardrails implemented
- [ ] MCP Server security checklist completed

**Sign-off Required**: QA Architect + SRE Lead
