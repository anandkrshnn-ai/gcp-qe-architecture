# SLO/SLI Engineering: From Definition to Enforcement

**A Practitioner's Guide to Service Level Objectives**

---

## Introduction

Service Level Objectives (SLOs) are the most operationally powerful quality tool available to cloud engineering organizations. When implemented correctly, they create a quantitative, shared language between engineering, product, and business stakeholders about what "reliable enough" means—and provide the data-driven mechanism for deployment and prioritization decisions.

Yet most SLO implementations fail. They become static targets no one monitors, or they are set so conservatively they never fire, or so aggressively that every alert becomes a crisis. This guide provides a rigorous, practitioner-tested framework from initial definition through automated enforcement.

---

## 1. Foundational Concepts

**The SLO Hierarchy**

- **SLI (Service Level Indicator)**: A quantitative measurement of a specific aspect of service behavior. Examples: request success rate, API P99 latency, processing throughput. The *signal*.
- **SLO (Service Level Objective)**: A target value for an SLI over a defined time window. Example: "99.9% of requests to the Payments API succeed over any rolling 28-day window." The *goal*.
- **SLA (Service Level Agreement)**: A contractual commitment with financial penalties, derived from SLOs. The *contract*.

Most engineering teams should focus primarily on SLOs. SLAs should only be derived from SLOs that have been operational for at least 3-6 months.

**Error Budgets**

The error budget is the most important concept in SLO engineering. It transforms an SLO from a static target into an operational resource.

At 99.9% availability over 30 days, the allowed downtime is:

```
30 days × 24 hours × 60 minutes × (1 - 0.999) = 43.2 minutes
```

This 43.2 minutes is your error budget. Every deployment, dependency failure, and chaos experiment consumes it. The budget creates alignment: product teams want to ship features (spending budget), engineering wants stability (preserving budget). The SLO framework makes this trade-off quantifiable and transparent.

---

## 2. Defining Meaningful SLIs

**The Four SLI Categories**

Google's SRE practices define four primary categories:

| Category | What It Measures | Typical Metric |
|----------|-----------------|----------------|
| Availability | Is the service responding? | Success rate of non-5xx HTTP responses |
| Latency | Is the service fast enough? | % of requests under a latency threshold |
| Throughput | Is the service processing enough? | Requests/sec or messages/sec |
| Quality | Are results correct? | % of responses passing correctness checks |

For most user-facing services, availability and latency are the minimum baseline.

**The SLI Specification Format**

Every SLI should be documented before implementation:

```yaml
sli_name: payments_api_availability
what_we_measure: "Fraction of HTTP requests that return a non-5xx response"
good_event: "HTTP 2xx or 4xx (client errors are not service failures)"
bad_event: "HTTP 5xx or request timeout > 10s"
measurement_window: "Rolling 28 days"
data_source: "Cloud Monitoring request logs"
```

The 4xx vs 5xx distinction is critical. A 404 is a client error—not a service failure. Including 4xx responses in "bad events" creates an SLI driven by client behavior rather than service health.

**Latency Threshold Starting Points**

- Interactive user-facing APIs: P95 < 200ms, P99 < 1000ms
- Background processing APIs: P95 < 500ms, P99 < 2000ms
- Cold-start scenarios (Cloud Run with 0 min-instances): P95 < 3000ms

Always use **percentile thresholds**, never averages. A service where 99% of requests complete in 100ms but 1% take 60 seconds has excellent average latency and catastrophic P99 latency.

---

## 3. Setting SLO Targets

**Measure First, Set Second**

The most common SLO mistake is setting targets before measuring current performance. An SLO of "99.9% availability" is meaningless if your service currently runs at 97%.

The correct process:
1. Instrument the SLI and measure for 4 weeks.
2. Calculate current performance.
3. Set the initial SLO *below* current performance.
4. Tighten incrementally as the system improves.

**SLO Tiers Based on User Impact**

| Tier | Description | Example | Suggested SLO |
|------|-------------|---------|---------------|
| Tier 1 | Revenue-critical, user-facing | Payment processing | 99.95% |
| Tier 2 | Important, non-transactional | Product catalog, search | 99.9% |
| Tier 3 | Background or batch processing | Report generation | 99.0% |

**The Error Budget Policy**

An SLO without an error budget policy is just a target. The policy defines consequences:

```markdown
## Error Budget Policy: Payments Service

Budget 0-50% consumed:    Full deployment velocity.
Budget 50-75% consumed:   Deployments require Service Owner sign-off.
Budget 75-100% consumed:  New feature deployments frozen; reliability work prioritized.
Budget exhausted (>100%): Incident declared; all hands on reliability.
```

This must be agreed upon *before* the SLO goes live. Without it, the SLO has no teeth.

---

## 4. Implementing SLOs in Cloud Monitoring

**Measurement Architecture Options**

| Position | Source | Pros | Cons |
|----------|--------|------|------|
| Client-side | Real User Monitoring (RUM) | Actual user experience | Requires client instrumentation |
| Load Balancer | Access logs / proxy metrics | No code changes needed | Misses some backend failures |
| Service-side | Application metrics/logs | Full context | Potential self-reporting bias |

For most production services, **load balancer or proxy measurement** provides the best balance. It captures user experience without requiring application code changes.

**Terraform SLO Reference Pattern**

```hcl
resource "google_monitoring_slo" "payments_availability" {
  service      = google_monitoring_service.payments_api.service_id
  display_name = "Payments API Availability (99.9%)"
  goal         = 0.999
  rolling_period_days = 28

  request_based_sli {
    good_total_ratio {
      good_service_filter = join(" AND ", [
        "metric.type=\"loadbalancing.googleapis.com/https/request_count\"",
        "metric.labels.response_code_class!=\"500\""
      ])
      total_service_filter = "metric.type=\"loadbalancing.googleapis.com/https/request_count\""
    }
  }
}
```

**Burn Rate Alert Thresholds**

| Alert Severity | Burn Rate | Short Window | Long Window | Action |
|---------------|-----------|--------------|-------------|--------|
| Critical (Page) | 14x | 5 min | 1 hour | Immediate incident |
| High (Ticket) | 6x | 30 min | 6 hours | Priority ticket |
| Warning | 3x | 6 hours | 3 days | Scheduled work |

At 14x burn rate, the entire monthly budget is exhausted in ~2 hours. That warrants an immediate page.

---

## 5. SLO Review Cadence

**Weekly: Error Budget Status (15 minutes)**
- Current burn rate vs. target.
- Events that consumed the most budget this week.
- Upcoming deployments that carry reliability risk.

**Monthly: SLO Calibration**
- Is the SLO target still appropriate? (Too easy = no incentive, too hard = constant breach)
- New user journeys requiring new SLIs?
- Systematic reliability patterns suggesting process improvements?

**Quarterly: SLO Strategy**
- DORA metrics trend across the organization.
- Services consistently breaching SLOs (systemic problems).
- Services never close to breach (candidates for tightening).

---

## 6. Advanced Patterns

**Windowed vs. Calendar SLOs**

- **Rolling window** (last 28 days): Budget continuously replenishes. Recommended for operations.
- **Calendar window** (current month): Resets on a fixed date. Easier for business reporting but creates perverse incentives near month-end.

**Composite SLOs for User Journeys**

Individual service SLOs measure service health, not user experience. A journey SLO aggregates across the critical path:

```
Checkout Journey SLO = 
  Product Detail (avail.) × Add to Cart (avail. × latency) × Payment (avail. × latency)
```

If each component has 99.9% availability, the composite journey SLO is ~99.7%. Users always experience lower reliability than any individual service SLO. This is a critical insight for setting customer-facing commitments.

**SLOs for Async and Batch Systems**

- **Queue freshness SLO**: "95% of messages processed within 30 minutes of arrival."
- **Batch completion SLO**: "95% of nightly jobs complete by 06:00."
- **Data quality SLO**: "99% of processed records pass schema validation."

---

## 7. Common Failure Modes

- **SLOs set by committee, not measurement**: Negotiated targets reflect political compromise, not engineering reality. Measure first.
- **Measuring the monitoring system, not the service**: Self-reported health checks detect failure only if the application knows it is failing. Use external measurement.
- **Ignoring the long tail**: Average/P50 latency monitoring misses the users with the worst experience. Always track P95 and P99.
- **No post-mortem integration**: Every SLO breach should trigger a blameless review. Without this feedback loop, the same failure modes repeat.

---

## 8. Conclusion: SLOs as a Communication Protocol

The deepest value of SLO engineering is not the monitoring—it is the shared language it creates. "Our service is unreliable" is an argument. "Our service consumed 85% of its error budget this month due to two Tuesday deployments" is a data-driven escalation that leads to action.

For QA Architects, SLO engineering transforms the quality function from a subjective, approval-based process into an empirical, data-driven discipline.

---

*Related guides: [QE Architecture](01-quality-engineering-architecture.md) | [Production Readiness](03-production-readiness.md) | [AI-Powered QE](04-ai-powered-quality-engineering.md)*
