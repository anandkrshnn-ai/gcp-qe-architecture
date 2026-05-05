# Blameless Incident Post-Mortem

**Incident ID**: [INC-YYYY-NNNN]  
**Severity**: P1 / P2 / P3  
**Date of Incident**: [YYYY-MM-DD]  
**Date of Post-Mortem**: [YYYY-MM-DD]  
**Facilitator**: [Name]  
**Scribe**: [Name]  
**Participants**: [Names and roles]

---

> **Blameless Principle**: This post-mortem is a learning exercise, not a blame assignment. The goal is to understand the *system conditions* that allowed this incident to occur and to improve those conditions. Individual errors are symptoms of system-level gaps. We fix systems, not people.

---

## 1. Incident Summary

*A clear, non-technical summary of what happened, who was impacted, and for how long. Should be readable by non-engineers.*

**What happened**: [One paragraph describing the user-visible impact]

**Who was affected**: [Number of users / percentage of traffic / specific customer segments]

**Duration**: [Start time] → [End time] = [Total duration]

**Services affected**: [List of services and their roles in the incident]

**Maximum severity reached**: [P1 / P2 / P3]

---

## 2. Impact

### 2.1 User Impact

| Metric | Value |
|--------|-------|
| Users affected | [Number / %] |
| Requests failed | [Number / %] |
| Data affected | [None / Describe] |
| Geographic scope | [Global / Regional / Specific zones] |

### 2.2 Business Impact

| Metric | Value |
|--------|-------|
| Revenue impact | [$ estimate or N/A] |
| SLA breach | [Yes / No — if yes, affected customers] |
| Error budget consumed | [X minutes of Y minute monthly budget] |
| MTTR | [X minutes] |

---

## 3. Timeline

*Document the exact timeline with UTC timestamps. Be precise. This is the most important section for understanding detection and response gaps.*

| Time (UTC) | Event | Actor |
|------------|-------|-------|
| [HH:MM] | [Event description — what happened in the system] | System / [Name] |
| [HH:MM] | [Alert fired / first user report] | Monitoring / Customer |
| [HH:MM] | [On-call engineer paged] | PagerDuty |
| [HH:MM] | [First diagnosis hypothesis] | [Name] |
| [HH:MM] | [Mitigation action taken] | [Name] |
| [HH:MM] | [Service restored] | [Name] |
| [HH:MM] | [All-clear declared] | [Name] |

**Key timing metrics**:
- **Time to Detect** (incident start → alert fired): [X minutes]
- **Time to Acknowledge** (alert fired → engineer engaged): [X minutes]
- **Time to Mitigate** (acknowledged → service restored): [X minutes]
- **Total MTTR**: [X minutes]

---

## 4. Root Cause Analysis

### 4.1 Immediate Cause

*What was the direct technical cause of the failure? This is the "what broke."*

[Description of the immediate technical cause. Example: "A deployment of version 2.4.1 of the payments service included a database connection pool configuration change that set the maximum connections to 5 instead of 50, exhausting the pool within 3 minutes of peak traffic."]

### 4.2 Contributing Factors

*What system conditions made this failure possible or worse? Use the "5 Whys" technique.*

**Why did [immediate cause] happen?**
→ Because [Factor 1]

**Why did [Factor 1] happen?**
→ Because [Factor 2]

**Why did [Factor 2] happen?**
→ Because [Factor 3 — typically a system-level gap]

**Contributing factors identified**:
- [Factor]: [Description of how it contributed]
- [Factor]: [Description of how it contributed]

### 4.3 Detection Gap

*Why wasn't this caught earlier? What quality gate should have caught this?*

- [ ] Should have been caught by unit tests — why wasn't it?
- [ ] Should have been caught by integration tests — why wasn't it?
- [ ] Should have been caught by performance tests — why wasn't it?
- [ ] Should have been caught by staging validation — why wasn't it?
- [ ] Should have been caught by monitoring/alerting — why wasn't it?

*Example: "The connection pool configuration change was not covered by any test. The integration tests mock the database connection layer and would not have detected a pool exhaustion scenario."*

---

## 5. What Went Well

*Explicitly document what worked correctly during this incident. This reinforces good practices and prevents regressing them.*

- [Example: Automated rollback triggered within 8 minutes of deployment, limiting total impact duration]
- [Example: Runbook for database connection issues was clear and led to rapid diagnosis]
- [Example: Oncall rotation escalation worked correctly — backup engineer was engaged within 5 minutes]

---

## 6. What Went Poorly

*Document gaps without blame. Focus on system and process failures.*

- [Example: The connection pool alert threshold was set to fire only when connections reached 100% saturation. A threshold at 80% would have fired 7 minutes earlier.]
- [Example: The staging environment uses a mock database that does not enforce connection limits, so the regression was not detectable in pre-production testing.]
- [Example: The runbook for this service did not cover the connection pool failure mode.]

---

## 7. Action Items

*Specific, owned, time-bounded actions. Each action item must have a single owner and a due date. Generic actions ("improve monitoring") are not acceptable—be specific.*

| # | Action | Owner | Priority | Due Date | Status |
|---|--------|-------|----------|----------|--------|
| 1 | Add integration test for database connection pool exhaustion (> 80% pool usage) | [Name] | P1 | [Date] | Open |
| 2 | Update staging environment to use real connection limits (not mock) | [Name] | P1 | [Date] | Open |
| 3 | Add Cloud Monitoring alert for connection pool saturation > 80% | [Name] | P1 | [Date] | Open |
| 4 | Update runbook to include connection pool failure diagnosis steps | [Name] | P2 | [Date] | Open |
| 5 | Add connection pool config to NFR spec review checklist | [Name] | P2 | [Date] | Open |

**Action item tracking**: These items are tracked in [link to ticket system]. Review progress in the weekly SLO review.

---

## 8. Lessons Learned

*Synthesize the key learnings from this incident into generalizable principles. These should influence future architecture and process decisions.*

1. **[Lesson]**: [Explanation of the principle and how it applies beyond this incident]
2. **[Lesson]**: [Explanation]
3. **[Lesson]**: [Explanation]

*Example: "Configuration changes to resource limits (connection pools, concurrency, memory limits) require specific integration tests that validate behavior at limit boundaries, not just happy-path behavior. Our current test strategy does not require this category of test explicitly."*

---

## 9. SLO Impact Record

| SLO | Pre-Incident Budget | Consumed by Incident | Remaining Budget |
|-----|---------------------|----------------------|-----------------|
| [Service Availability SLO] | [X minutes] | [Y minutes] | [Z minutes] |
| [Latency SLO] | [X%] | [Y%] | [Z%] |

**Error budget policy triggered**: [Yes/No — if yes, what policy actions were taken?]

---

## 10. Post-Mortem Review

| Reviewer | Role | Date Reviewed | Approved |
|----------|------|---------------|----------|
| [Name] | Engineering Lead | [Date] | ☐ |
| [Name] | QA Architect | [Date] | ☐ |
| [Name] | SRE | [Date] | ☐ |

**Post-mortem published to**: [Link to team wiki / incident log]  
**Action items linked in**: [Link to ticket system]  
**Next review of open action items**: [Date of next weekly SLO review]

---

*Related: [Incident Runbook](../docs/runbooks/) | [SLO Dashboard](../evidence/) | [Production Readiness Guide](../guides/03-production-readiness.md)*
