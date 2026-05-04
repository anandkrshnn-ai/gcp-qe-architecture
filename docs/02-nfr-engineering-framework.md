# Non-Functional Requirements (NFR) Engineering Framework

Traditional NFRs ("The system must be fast and reliable") are unactionable. In modern GCP architectures, we translate NFRs into measurable, trackable Service Level Objectives (SLOs) and Service Level Indicators (SLIs).

This framework defines how to engineer for performance, reliability, and scale.

## 1. The SLO / SLI Model

Every critical user journey (CUJ) must have defined indicators and objectives.

- **SLI (Service Level Indicator):** A quantitative measure of some aspect of the level of service that is provided. (e.g., HTTP 5xx error rate).
- **SLO (Service Level Objective):** A target value or range of values for a service level that is measured by an SLI. (e.g., 99.9% of requests successful).
- **Error Budget:** `100% - SLO`. The acceptable amount of unreliability.

### Common GCP SLIs:
- **Availability:** (Successful Requests / Total Requests) measured via Cloud Load Balancing metrics.
- **Latency:** The proportion of requests faster than a threshold (e.g., < 200ms) measured via Cloud Run / GKE ingress metrics.
- **Freshness:** The proportion of data read that is more recent than a threshold (e.g., BigQuery streaming ingestion lag).

## 2. Defining NFRs by Tier

Not all services require 99.99% availability. Define service tiers to standardize NFRs.

### Tier 1: Mission Critical (e.g., Payment Gateway)
- **Availability SLO:** 99.99% (52 minutes downtime / year)
- **Latency SLO:** 99th percentile (P99) < 100ms
- **RTO (Recovery Time Obj):** < 15 minutes
- **RPO (Recovery Point Obj):** 0 (No data loss - requires Cloud Spanner or sync replication)

### Tier 2: Core Services (e.g., Product Catalog)
- **Availability SLO:** 99.9% (8.7 hours downtime / year)
- **Latency SLO:** 95th percentile (P95) < 300ms
- **RTO:** < 4 hours
- **RPO:** < 1 hour

### Tier 3: Internal/Batch (e.g., Nightly Reporting)
- **Availability SLO:** 99.0% (3.6 days downtime / year)
- **Latency SLO:** P90 < 2 seconds
- **RTO:** < 24 hours
- **RPO:** < 24 hours

## 3. Validating NFRs in the Pipeline

NFRs must be validated before reaching production.

### Performance Gates
- Run `k6` load tests against the staging environment.
- Fail the pipeline if the P95 latency exceeds the SLO threshold defined in the NFR spec.

### Chaos Gates
- Automate pod deletion or node pool cordon in GKE.
- Validate that the error rate SLI does not drop below the target during the experiment.

## 4. Monitoring and Alerting

Use **Burn Rate Alerting** rather than static thresholds.
- **Alert:** If the Error Budget is burning at 10x the allowed rate (meaning it will be exhausted in 3 days).
- **Action:** Halt feature deployments until the system stabilizes.
