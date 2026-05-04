# Performance Engineering Framework for GCP

Modern cloud applications require performance to be engineered into the architecture, not just tested at the end. This framework outlines how to shift performance testing left using GCP-native tools and k6.

## 1. The Performance Engineering Lifecycle
1.  **Define NFRs:** Use the [NFR Spec Template](../templates/nfr-spec-template.md) to define latency (P95/P99), throughput (RPS), and concurrency.
2.  **Establish Baselines:** Run tests on individual components (Cloud Run, GKE services) to understand their raw performance.
3.  **Continuous Validation:** Integrate k6 tests into [Cloud Build](../reference-implementations/cloudbuild-quality-gates/cloudbuild.yaml) to catch regressions early.
4.  **Analyze & Tune:** Use Cloud Profiler and Cloud Trace to identify bottlenecks.

## 2. Load Testing Strategy
-   **Unit Load Tests:** Test a single microservice with mocked dependencies.
-   **Integration Load Tests:** Test service-to-service communication.
-   **End-to-End Stress Tests:** Test the entire system under peak predicted load.
-   **Soak Tests:** Run tests for extended periods (e.g., 4-24 hours) to identify memory leaks.

## 3. GCP Performance Tuning Checklist
-   **GKE:** Vertical/Horizontal Pod Autoscaling (VPA/HPA), node auto-provisioning.
-   **Cloud Run:** Max instances, concurrency settings, and CPU allocation (always-on vs. request-based).
-   **Cloud SQL:** Instance sizing, connection pooling, and read replicas.
-   **Networking:** Use Premium Tier networking for lowest latency.

## 4. Pass/Fail Criteria (Quality Gates)
Performance tests must have hard thresholds:
-   `P95 Latency < 200ms`
-   `Error Rate < 0.1%`
-   `CPU Utilization < 80%` during peak load.

---

*See the [k6 Performance Tests](../reference-implementations/k6-performance-tests/) for executable examples.*
