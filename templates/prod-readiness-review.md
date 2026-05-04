# Production Readiness Review (PRR) Checklist

Before any service goes live on GCP, it must pass this PRR.

## 1. Observability
-   [ ] **SLIs/SLOs:** Defined and dashboarded in Cloud Monitoring.
-   [ ] **Alerting:** PagerDuty/Slack integration verified.
-   [ ] **Logging:** Structured logging implemented; no PII in logs.
-   [ ] **Tracing:** Cloud Trace integrated for distributed services.

## 2. Scalability & Performance
-   [ ] **Autoscaling:** HPA/VPA (GKE) or Max Instances (Cloud Run) configured.
-   [ ] **Load Test:** Successfully passed 2x predicted peak load.
-   [ ] **Quotas:** GCP project quotas verified for peak load.

## 3. Reliability & Resilience
-   [ ] **HA:** Multi-zone deployment verified.
-   [ ] **Failover:** Database failover test successful.
-   [ ] **Backups:** Daily backups enabled and restoration verified.

## 4. Security & Compliance
-   [ ] **IAM:** Least privilege principle applied.
-   [ ] **Vulnerability:** Zero "High" vulnerabilities in container scans.
-   [ ] **Encryption:** Data encrypted at rest and in transit.

## 5. Operations
-   [ ] **Deployment:** Automated CI/CD pipeline verified.
-   [ ] **Rollback:** Automated rollback strategy tested.
-   [ ] **On-call:** Rotation schedule established.

---
**Status:** [APPROVED | REJECTED]
**Reviewer:** ____________________
