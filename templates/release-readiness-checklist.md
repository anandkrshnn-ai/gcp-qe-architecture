# Release Readiness Checklist

**Service**: [Service Name]  
**Release Version**: [v1.x.x]  
**Release Date**: [YYYY-MM-DD]  
**Release Manager**: [Name]  
**QA Sign-off**: [Name]

---

> **How to Use This Checklist**: Complete each section sequentially. A release cannot proceed to the next section until the current section is fully signed off. Items marked `[BLOCK]` are hard gates—any unchecked item in this category blocks the release. Items marked `[RISK]` require documented risk acceptance if unchecked.

---

## Section 1: Code & Quality Gates `[MUST PASS]`

All CI gates must have passed against the release candidate commit.

| Check | Status | Evidence |
|-------|--------|---------|
| ☐ All unit tests passing | | [CI run link] |
| ☐ All integration tests passing | | [CI run link] |
| ☐ Contract tests passing (no consumer contracts broken) | | [CI run link] |
| ☐ SAST scan complete — zero Critical/High findings | | [Scan report link] |
| ☐ Dependency vulnerabilities — zero Critical/High unpatched | | [Scan report link] |
| ☐ Container image scanned — zero Critical CVEs | | [Scan report link] |
| ☐ No hardcoded secrets in codebase | | [Secret scan result] |
| ☐ Code review approved by >= 2 reviewers | | [PR link] |
| ☐ Terraform `validate` and `fmt` pass | | [CI run link] |
| ☐ OPA/policy checks pass | | [CI run link] |

**Section 1 Sign-off**: _____________________ Date: _____________

---

## Section 2: Performance Validation `[BLOCK]`

| Check | Status | Evidence |
|-------|--------|---------|
| ☐ Baseline load test executed — P95 within SLO threshold | | [k6 report link] |
| ☐ No performance regression vs. previous release (< 10% degradation) | | [Comparison report] |
| ☐ Memory usage stable over 30-minute soak test (no leak trend) | | [Report link] |
| ☐ Auto-scaling validated under 2x peak load | | [Test results] |

**Performance Thresholds (from NFR Spec)**:  
- P95 latency: < [X]ms  
- Error rate: < [Y]%  
- Maximum memory: < [Z]MB

**Section 2 Sign-off**: _____________________ Date: _____________

---

## Section 3: Staging Validation `[BLOCK]`

| Check | Status | Evidence |
|-------|--------|---------|
| ☐ Deployed to staging successfully | | [Deploy log] |
| ☐ Smoke tests pass (all critical journeys validated) | | [Test results] |
| ☐ Synthetic monitoring active and healthy for >= 1 hour | | [Dashboard link] |
| ☐ No anomalous error rates in staging logs | | [Log query link] |
| ☐ Database migrations tested on staging dataset (if applicable) | | [Migration log] |
| ☐ Rollback procedure tested in staging | | [Test notes] |

**Section 3 Sign-off**: _____________________ Date: _____________

---

## Section 4: Observability Readiness `[BLOCK]`

*The service must be observable before it is deployed. Deploying unobservable code is always a risk.*

| Check | Status | Owner |
|-------|--------|-------|
| ☐ Structured JSON logging implemented with correlation IDs | | |
| ☐ Four golden signals (Latency, Traffic, Errors, Saturation) instrumented | | |
| ☐ SLO dashboard published and reviewed | | |
| ☐ SLO burn rate alerts configured (Critical + High thresholds) | | |
| ☐ Custom business metric dashboards updated for new features | | |
| ☐ Distributed tracing enabled and traces visible in trace viewer | | |

**Section 4 Sign-off**: _____________________ Date: _____________

---

## Section 5: Operational Readiness `[BLOCK]`

| Check | Status | Owner |
|-------|--------|-------|
| ☐ On-call rotation updated and engineer briefed on this release | | |
| ☐ Runbook updated to cover new failure modes introduced by this release | | |
| ☐ Rollback procedure documented and tested | | |
| ☐ Deployment playbook reviewed with the team | | |
| ☐ Downstream service owners notified of breaking changes (if any) | | |
| ☐ Support / customer success briefed on user-visible changes | | |

**Section 5 Sign-off**: _____________________ Date: _____________

---

## Section 6: Error Budget Check `[BLOCK]`

*A release must not proceed if the service's error budget cannot absorb the expected deployment risk.*

| Metric | Current Value | Threshold | Pass? |
|--------|---------------|-----------|-------|
| Error budget consumed (this month) | [X]% | < 75% | ☐ |
| Last deployment failure rate | [X]% | < 5% | ☐ |
| Days since last production incident | [X days] | > 2 days | ☐ |

**If any threshold is not met**: The release requires explicit written approval from the Engineering Lead with documented risk acceptance.

**Risk acceptance (if required)**:  
Approved by: _____________________ Date: _____________  
Rationale: _______________________________________________________

**Section 6 Sign-off**: _____________________ Date: _____________

---

## Section 7: Security and Compliance `[RISK]`

| Check | Status | Owner |
|-------|--------|-------|
| ☐ DAST scan executed against staging environment | | |
| ☐ New API endpoints documented in security inventory | | |
| ☐ Data classification reviewed for new data types introduced | | |
| ☐ Privacy review completed (if PII-handling changes) | | |
| ☐ Compliance team review completed (if regulatory scope changes) | | |

**Section 7 Sign-off**: _____________________ Date: _____________

---

## Section 8: Release Execution Plan

### 8.1 Deployment Strategy

- **Strategy**: Blue/Green / Canary / Rolling / Feature flag
- **Initial traffic split**: [e.g., 5% canary]
- **Progression timeline**: [e.g., 5% → 25% → 100% at 30-minute intervals]
- **Automated rollback trigger**: [e.g., Error rate > 1% for 5 consecutive minutes]

### 8.2 Rollback Procedure

| Step | Command / Action | Estimated Time |
|------|-----------------|----------------|
| 1 | Trigger rollback | `[command]` | < 2 min |
| 2 | Verify rollback complete | [check] | < 3 min |
| 3 | Notify stakeholders | [channel] | < 1 min |
| 4 | Open post-mortem | [template link] | Immediate |

**Total estimated rollback time**: < [X] minutes

### 8.3 Go / No-Go Decision

**Scheduled release time**: [HH:MM UTC]  
**Go / No-Go call time**: [HH:MM UTC — 30 minutes before release]  
**Required approvers for Go**:
- [ ] Engineering Lead: _____________________
- [ ] QA Architect: _____________________
- [ ] On-Call SRE: _____________________

**Final Decision**: ☐ GO &nbsp;&nbsp; ☐ NO-GO  
**Decision time**: _____________  
**Decision notes**: _______________________________________________________

---

## Section 9: Post-Release Monitoring Plan

| Time After Deploy | Action | Owner |
|------------------|--------|-------|
| 0-5 minutes | Monitor error rate and latency on golden signals dashboard | On-call SRE |
| 5-15 minutes | Review application logs for anomalies | Release Manager |
| 15-30 minutes | Decision point: proceed to full rollout or hold | Engineering Lead |
| 1 hour | SLO burn rate check — confirm budget not at risk | QA Architect |
| 24 hours | Change failure rate assessment | QA Team |
| 1 week | Performance trend review vs. pre-release baseline | SRE |

**Monitoring dashboard**: [Link]  
**Slack channel for release watch**: [#channel-name]

---

*Related: [Post-Mortem Template](incident-postmortem-template.md) | [NFR Spec](nfr-spec-template.md) | [Production Readiness Guide](../guides/03-production-readiness.md)*
