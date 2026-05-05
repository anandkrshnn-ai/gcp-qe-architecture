# Non-Functional Requirements (NFR) Specification Template

**Service**: [Service Name]  
**Version**: [v1.0]  
**Author**: [Name]  
**Date**: [YYYY-MM-DD]  
**Review Cycle**: Quarterly

---

## 1. Overview

This document specifies the non-functional requirements for **[Service Name]**. NFRs define the *quality attributes* of the system—how well it performs its functions under defined conditions—as distinct from functional requirements which define *what* the system does.

**Service Tier**: Tier 1 / Tier 2 / Tier 3 *(see [QE Architecture Guide](../guides/01-quality-engineering-architecture.md) for tier definitions)*  
**Criticality**: Revenue-Critical / Business-Important / Supporting

---

## 2. Performance Requirements

### 2.1 Latency

| Endpoint / Operation | P50 Target | P95 Target | P99 Target | Measurement Method |
|----------------------|------------|------------|------------|--------------------|
| [Primary API endpoint] | < Xms | < Xms | < Xms | Load balancer logs |
| [Secondary endpoint] | < Xms | < Xms | < Xms | Synthetic monitoring |
| [Batch operation] | N/A | < Xs | < Xs | Application metrics |

**Latency SLO**: *[Derived from above. Example: "95% of requests to the primary endpoint complete in under 200ms over any rolling 28-day window."]*

### 2.2 Throughput

| Scenario | Required Throughput | Peak Throughput | Notes |
|----------|---------------------|-----------------|-------|
| Normal load | X req/sec | Y req/sec | |
| Campaign/event peaks | X req/sec | Y req/sec | [Define event types] |
| Batch processing | X records/hour | Y records/hour | |

### 2.3 Concurrency

- **Maximum concurrent users**: [X]
- **Maximum concurrent API connections**: [X]
- **Database connection pool size**: [X]

---

## 3. Reliability Requirements

### 3.1 Availability

| Time Window | Target Availability | Maximum Allowed Downtime | Error Budget |
|-------------|---------------------|--------------------------|--------------|
| Monthly | [99.9%] | [43.2 minutes] | [43.2 minutes] |
| Quarterly | [99.9%] | [~2.2 hours] | [~2.2 hours] |
| Annual | [99.9%] | [~8.7 hours] | [~8.7 hours] |

**Availability SLI**: *[Define what counts as "available". Example: "Service is available when >= 99% of HTTP requests return non-5xx responses over any 5-minute window."]*

**Planned Maintenance Windows**: [Define windows, e.g., "Tuesdays 02:00-04:00 UTC are excluded from availability calculations."]

### 3.2 Fault Tolerance

- **Single point of failure tolerance**: [Yes/No — describe mitigations]
- **Dependency failure behavior**: When [Dependency X] is unavailable, the service [degrades gracefully / returns cached data / returns 503 / other]
- **Data loss tolerance**: [Zero data loss / up to X minutes / other]

### 3.3 Recovery Objectives

| Metric | Target | Notes |
|--------|--------|-------|
| **RTO** (Recovery Time Objective) | < [X] minutes | Time to restore service after failure |
| **RPO** (Recovery Point Objective) | < [X] minutes | Maximum acceptable data loss |
| **MTTR** (Mean Time to Restore) | < [X] minutes | Average incident recovery time |

### 3.4 Resilience Patterns

*Indicate which patterns are implemented:*

- [ ] Circuit breaker for external dependencies
- [ ] Retry with exponential backoff and jitter
- [ ] Timeout enforcement on all outbound calls
- [ ] Graceful degradation when non-critical dependencies fail
- [ ] Pod Disruption Budget (for Kubernetes deployments)
- [ ] Multi-zone deployment

---

## 4. Scalability Requirements

### 4.1 Horizontal Scaling

| Metric | Minimum Instances | Maximum Instances | Scale Trigger |
|--------|------------------|-------------------|---------------|
| Normal operation | [X] | [Y] | CPU > 60% or Requests/instance > Z |
| Known peak periods | [X] | [Y] | Pre-scaled via schedule |

### 4.2 Data Volume

- **Current data volume**: [X GB / records]
- **Expected growth rate**: [Y% per quarter]
- **Data retention policy**: [X days active, Y days archive, Z days deletion]
- **Storage scaling approach**: [Auto-scaling / Manual / Defined thresholds]

### 4.3 Scalability Limits

*Document known or designed limits that, if exceeded, require architectural changes:*

- **Maximum supported request rate**: [X req/sec before architectural changes needed]
- **Maximum data volume**: [X TB before storage architecture changes needed]
- **Maximum concurrent users**: [X before horizontal scaling approach changes]

---

## 5. Security Requirements

### 5.1 Authentication and Authorization

- **Authentication mechanism**: [OAuth2 / API keys / mTLS / other]
- **Authorization model**: [RBAC / ABAC / other]
- **Session management**: [Token lifetime / refresh strategy]

### 5.2 Data Security

| Data Classification | Storage Encryption | Transit Encryption | Access Controls |
|--------------------|--------------------|--------------------|-----------------|
| PII | AES-256 at rest | TLS 1.3 | IAM role-based |
| Financial | AES-256 at rest | TLS 1.3 | IAM + audit log |
| Internal config | [Encryption type] | [Protocol] | [Controls] |

### 5.3 Compliance Requirements

- **Regulatory frameworks**: [GDPR / PCI-DSS / SOC 2 / HIPAA / other]
- **Audit logging requirements**: [What events must be logged, retention period]
- **Data residency requirements**: [Geographic constraints on data storage and processing]
- **Vulnerability remediation SLA**: Critical: 24h / High: 7 days / Medium: 30 days / Low: 90 days

---

## 6. Operational Requirements

### 6.1 Observability

- [ ] Structured JSON logging with correlation IDs
- [ ] Four golden signals instrumented (Latency, Traffic, Errors, Saturation)
- [ ] Distributed tracing enabled
- [ ] Custom business metrics emitted
- [ ] SLO dashboards published

**Log retention**: [X days]  
**Metrics retention**: [X days]  
**Trace retention**: [X days]

### 6.2 Alerting

| Alert | Condition | Severity | Response SLA |
|-------|-----------|----------|--------------|
| SLO Burn Rate - Critical | Error budget burn rate > 14x | P1 | 15 minutes |
| SLO Burn Rate - High | Error budget burn rate > 6x | P2 | 4 hours |
| Latency degradation | P99 > [X]ms for 5 minutes | P2 | 4 hours |
| Dependency failure | [Dependency] error rate > 5% | P2 | 4 hours |

### 6.3 Deployment Requirements

- **Deployment strategy**: Blue/Green / Canary / Rolling / Feature flag
- **Maximum deployment time**: [X minutes]
- **Rollback time**: < [X minutes]
- **Deployment windows**: [Define any blackout periods]
- **Change freeze periods**: [e.g., December 15 - January 5]

---

## 7. Capacity Planning

### 7.1 Resource Baselines (Current)

| Resource | Current Allocation | Actual Usage (P95) | Headroom |
|----------|-------------------|--------------------|----- ----|
| CPU | [X vCPU] | [Y vCPU] | [Z%] |
| Memory | [X GB] | [Y GB] | [Z%] |
| Storage | [X GB] | [Y GB] | [Z%] |
| Network | [X Mbps] | [Y Mbps] | [Z%] |

### 7.2 Growth Projections (Next 12 Months)

| Quarter | Expected Traffic Growth | Required Capacity Change | Action Required |
|---------|------------------------|--------------------------|-----------------|
| Q3 2026 | +[X]% | [Description] | [Action] |
| Q4 2026 | +[X]% | [Description] | [Action] |

---

## 8. NFR Validation

*How each NFR will be validated before production deployment:*

| NFR Category | Validation Method | Frequency | Owner |
|--------------|------------------|-----------|-------|
| Latency | k6 load test in CI | Every deployment | QE Team |
| Availability | SLO monitoring in Cloud Monitoring | Continuous | SRE |
| Scalability | Load test with 2x peak traffic | Quarterly | QE Team |
| Security | SAST/DAST scan + pen test | CI + Quarterly | Security |
| Resilience | Chaos experiments | Quarterly | SRE + QE |

---

## 9. Sign-off

| Role | Name | Date | Approved |
|------|------|------|----------|
| Engineering Lead | | | ☐ |
| QA Architect | | | ☐ |
| Security | | | ☐ |
| Product Owner | | | ☐ |

---

*Related: [Production Readiness Checklist](release-readiness-checklist.md) | [SLO/SLI Guide](../guides/02-slo-sli-engineering.md)*
