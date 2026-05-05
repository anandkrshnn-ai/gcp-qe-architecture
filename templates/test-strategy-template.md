# Test Strategy Template

**Project / Service**: [Service Name]  
**Version**: [v1.0]  
**Author**: [Name]  
**Date**: [YYYY-MM-DD]  
**Related**: [NFR Spec](nfr-spec-template.md) | [ADR Log](../docs/decisions/)

---

## 1. Scope and Objectives

### 1.1 What This Strategy Covers
*Define the scope of this test strategy. Include:*
- Services / components in scope
- Integrations and dependencies in scope
- Environments covered (dev / staging / production)
- Release or milestone this strategy applies to

*Out of scope*: [Explicitly list what is NOT covered and why]

### 1.2 Quality Objectives
*State the specific, measurable quality goals this strategy is designed to achieve:*

- [ ] Change failure rate < 5% over the quarter
- [ ] P95 latency < [X]ms under [Y] concurrent users
- [ ] Zero Critical/High security vulnerabilities in production
- [ ] SLO compliance > 99.9% for Tier 1 services
- [ ] Test execution time in CI < [X] minutes

---

## 2. Risk Assessment

*Identify the highest-risk areas that should receive the most testing investment:*

| Risk Area | Likelihood | Impact | Risk Level | Testing Focus |
|-----------|------------|--------|------------|---------------|
| [e.g., Payment processing failure] | High | Critical | Critical | Contract + E2E + Chaos |
| [e.g., Auth token expiry edge case] | Medium | High | High | Unit + Integration |
| [e.g., Third-party API latency] | High | Medium | High | Performance + Circuit Breaker |
| [e.g., Database migration] | Low | Critical | High | Migration-specific test plan |

*Risk Mitigation Priority Order*: [List the top 3 risks the team will focus on reducing through testing investment]

---

## 3. Test Levels

### 3.1 Unit Tests

**Objective**: Validate individual component logic in isolation.

| Attribute | Target |
|-----------|--------|
| Coverage target | > 80% of business logic branches |
| Execution time | < 3 minutes |
| Framework | [pytest / Jest / Go test / JUnit] |
| Mocking strategy | [Library: unittest.mock / jest.mock / etc.] |
| CI integration | Runs on every commit / PR |

**What to unit test**: Business rules, data transformation logic, error handling paths, boundary conditions.  
**What NOT to unit test**: Framework internals, infrastructure code, trivial getters/setters.

---

### 3.2 Integration Tests

**Objective**: Validate service behavior with real dependency connections (databases, message queues, downstream services).

| Attribute | Target |
|-----------|--------|
| Scope | [Service + real DB / Service + downstream API stub] |
| Execution time | < 15 minutes |
| Environment | Containerized via docker-compose or Testcontainers |
| CI integration | Runs on PR merge to main |

**Test cases to include**:
- [ ] Happy path for each major user journey
- [ ] Dependency failure handling (DB unavailable, downstream timeout)
- [ ] Data integrity across service boundaries
- [ ] Authentication and authorization paths

---

### 3.3 Contract Tests

**Objective**: Ensure service API contracts are maintained as services evolve independently.

| Attribute | Target |
|-----------|--------|
| Framework | [Pact / gRPC schema validation / OpenAPI diff] |
| Execution time | < 5 minutes |
| CI integration | Runs on PR and blocks merge if contract broken |

**Consumer-Driven Contract Test Approach**:
1. Each consumer service defines the API contract it expects from the provider.
2. Contract tests run against the provider on every provider deployment.
3. A provider deployment that breaks a consumer contract fails CI.

---

### 3.4 Performance Tests

**Objective**: Validate that the service meets NFR latency and throughput targets under realistic load.

| Test Type | Tool | Scenario | Success Criteria |
|-----------|------|----------|-----------------|
| Baseline load | k6 | [X] concurrent users, [Y] min | P95 < [Z]ms |
| Peak load | k6 | [X] concurrent users (2x normal) | P95 < [Z]ms, error rate < 1% |
| Soak test | k6 | [X] users over [Y] hours | No memory leak, stable latency |
| Cold start | k6 | 10 cold VUs, 1 iteration each | P95 < 3000ms |
| Spike test | k6 | Traffic doubles in 30s | Autoscale completes in < 2 min |

**Performance Gate (CI)**: The baseline load test runs in CI on every merge. Failure blocks deployment to staging.

**Performance Test Data**: [Describe how test data is managed. Anonymized production snapshots? Synthetic data? What volume?]

---

### 3.5 Security Tests

**Objective**: Identify and prevent security vulnerabilities from reaching production.

| Test Type | Tool | Frequency | Gate |
|-----------|------|-----------|------|
| SAST | [Bandit / Semgrep / SonarQube] | Every PR | Blocks merge on High/Critical |
| Dependency scan | [Dependabot / Snyk / Trivy] | Every PR + daily | Auto-PR for patches |
| Container scan | [Trivy / Grype] | Every build | Blocks on Critical CVEs |
| DAST | [OWASP ZAP] | Every staging deploy | Review High findings within 48h |
| Secret scanning | [git-secrets / truffleHog] | Pre-commit + PR | Blocks immediately |
| Pen testing | External firm | Annually | Sign-off required |

---

### 3.6 End-to-End Tests

**Objective**: Validate complete user journeys across the full service stack.

| Journey | Priority | Frequency |
|---------|----------|-----------|
| [e.g., User registration → login → [core action]] | Critical | Every staging deploy |
| [e.g., Checkout → payment → confirmation] | Critical | Every staging deploy |
| [e.g., [Secondary user journey]] | High | Daily |

**E2E Test Principles**:
- E2E tests are slow and flaky. Keep the suite small (< 20 tests) and focused on critical journeys.
- Each test must be independent—no shared state between tests.
- Flaky tests are treated as P1 defects.

---

### 3.7 Chaos and Resilience Tests

**Objective**: Validate system behavior under infrastructure failure conditions.

| Experiment | Target | Expected Behavior | Frequency |
|------------|--------|-------------------|-----------|
| Pod kill (20% of replicas) | [Service] | PDB maintained, zero downtime | Quarterly |
| Dependency timeout injection | [Upstream service] | Circuit breaker activates in < 5s | Quarterly |
| Network latency injection (200ms) | [Service ↔ DB] | Timeouts handled, user sees degraded response | Quarterly |
| Database failover | [Cloud SQL] | Failover complete in < 30s | Semi-annually |

**Chaos Test Prerequisites**: SLOs must be instrumented and alerting active before chaos tests run. Never run chaos experiments without an engineer actively monitoring.

---

## 4. Test Environments

| Environment | Purpose | Data | Refresh Cadence |
|-------------|---------|------|-----------------|
| Local | Developer testing, unit + integration | Synthetic / anonymized | On-demand |
| Dev | Branch integration testing | Synthetic | Auto on merge |
| Staging | Pre-production validation, E2E, perf | Anonymized production subset | Daily refresh |
| Production | Synthetic monitoring, canary validation | Live | Continuous |

---

## 5. Test Data Management

- **Data generation approach**: [Synthetic data factory / anonymized production export / hardcoded fixtures]
- **PII handling**: [All test data must be anonymized. No real customer data in non-production environments.]
- **Data isolation**: Each test run must create and clean up its own test data.
- **Test database refresh**: Staging database refreshed from anonymized production snapshot [frequency].

---

## 6. CI/CD Integration

```
PR Open          Merge to Main       Staging Deploy      Production Deploy
    |                   |                    |                    |
    ├─ Lint/SAST        ├─ Unit tests        ├─ E2E tests         ├─ Canary 5%
    ├─ Secret scan      ├─ Integration tests ├─ Performance gate  ├─ Monitor 30min
    ├─ Contract tests   ├─ Contract tests    ├─ Security scan     ├─ Canary 25%
    └─ Unit tests       └─ Perf gate (CI)    └─ Smoke tests       └─ Full rollout
```

**Deployment gate logic**:
- Any test failure in Gates 1-2 blocks the PR merge.
- Any test failure in Gate 3 blocks staging deployment.
- Error budget consumption > 75% blocks production deployment.

---

## 7. Defect Management

| Severity | Definition | Response SLA | Escalation |
|----------|------------|--------------|------------|
| Critical | Production down / Data loss | Fix within 4 hours | CTO + Incident bridge |
| High | Core journey broken / SLO at risk | Fix within 24 hours | Engineering Lead |
| Medium | Significant feature degraded | Fix within 1 sprint | Team backlog |
| Low | Minor UX issue / edge case | Fix within 2 sprints | Team backlog |

**Defect Escape Analysis**: Monthly review of defects found in production vs. pre-production. Target: < 10% defect escape rate.

---

## 8. Roles and Responsibilities

| Role | Testing Responsibilities |
|------|-------------------------|
| Developer | Unit tests, integration tests, local validation |
| QA Engineer | E2E tests, performance tests, test data management |
| QA Architect | Test strategy, quality gates, tooling standards |
| SRE | Chaos experiments, production monitoring, SLO enforcement |
| Security | Security scanning configuration, pen test coordination |

---

## 9. Review and Updates

This test strategy must be reviewed:
- When NFRs change significantly.
- When new services or major features are added to scope.
- After a production incident not covered by existing test cases.
- Quarterly as part of the production readiness review cycle.

---

*Related: [NFR Spec](nfr-spec-template.md) | [Release Readiness Checklist](release-readiness-checklist.md) | [QE Architecture Guide](../guides/01-quality-engineering-architecture.md)*
