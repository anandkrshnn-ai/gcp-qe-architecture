# Non-Functional Requirements (NFR) Specification

## Service Details
*   **Service Name:** [e.g., Payment Gateway Service]
*   **Tier:** [Tier 1 / Tier 2 / Tier 3]
*   **Owner:** [Team Name]

## 1. Reliability & Availability
*   **Target Availability SLO:** [e.g., 99.99%]
*   **Error Budget:** [e.g., 52 minutes of downtime per year]
*   **Measurement (SLI):** [e.g., Percentage of successful HTTP responses (200s) measured at the Cloud Load Balancer]
*   **Graceful Degradation:** [What happens if a dependency fails? e.g., Return cached catalog data if the underlying database is slow]

## 2. Performance & Scalability
*   **Latency SLO (P95):** [e.g., < 200ms]
*   **Latency SLO (P99):** [e.g., < 500ms]
*   **Expected Peak Throughput:** [e.g., 5,000 requests per second]
*   **Auto-scaling Triggers:** [e.g., Scale out Cloud Run instances when CPU > 70%]

## 3. Disaster Recovery (DR)
*   **Recovery Time Objective (RTO):** [e.g., < 1 hour]
*   **Recovery Point Objective (RPO):** [e.g., < 5 minutes]
*   **Failover Strategy:** [e.g., Active-Passive multi-region routing via Cloud DNS]

## 4. Observability
*   **Logging:** [Are structured JSON logs being sent to Cloud Logging?]
*   **Tracing:** [Is distributed tracing enabled for this service?]
*   **Alerting:** [List the primary alerts, e.g., SLO burn rate > 10x, Pod crash loops]

## 5. Security & Compliance
*   **Data Classification:** [e.g., PII, PCI, Public]
*   **Encryption:** [e.g., Default CMEK via Cloud KMS]
*   **Access Control:** [e.g., Zero-trust via Identity-Aware Proxy (IAP)]
