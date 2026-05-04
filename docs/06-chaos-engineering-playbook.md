# GCP Chaos Engineering Playbook

Chaos engineering is the discipline of experimenting on a software system in production in order to build confidence in the system's capability to withstand turbulent conditions.

## 1. Prerequisites
-   **Observability:** You must have SLOs and Dashboards set up (see [SLO Monitoring](../reference-implementations/slo-monitoring/)).
-   **Blast Radius Control:** Start in Staging/UAT before Production.
-   **Automated Rollback:** Ensure you can stop experiments instantly if SLOs are breached.

## 2. Common GCP Chaos Experiments
| Experiment | Target | Failure Mode | Success Metric |
| :--- | :--- | :--- | :--- |
| **Zone Outage** | GKE / Cloud SQL | Simulate one zone failing. | System remains available via other zones. |
| **Network Latency** | Inter-service comms | Inject 500ms latency between services. | Error rate does not exceed 1%. |
| **Resource Exhaustion** | Cloud Run / GKE | Fill up disk or max out CPU. | Autoscaler triggers or graceful degradation. |
| **Dependency Failure** | External API / Pub/Sub | Block access to a critical dependency. | Circuit breaker trips; system fails gracefully. |

## 3. Experiment Lifecycle
1.  **Steady State:** Define the "normal" behavior (e.g., Latency < 100ms).
2.  **Hypothesis:** "If we kill one pod in the payment service, the system will continue to process requests without errors."
3.  **Inject Failure:** Run the experiment (see [Chaos Experiments](../reference-implementations/chaos-experiments/)).
4.  **Observe:** Did the hypothesis hold?
5.  **Improve:** Fix the architectural gap found.

## 4. Tools
-   **Chaos Toolkit:** Open-source automation.
-   **LitmusChaos:** For GKE-native chaos.
-   **GCP Fault Injection Simulator (FIS):** Managed chaos service.

---

*See the [Chaos Experiments](../reference-implementations/chaos-experiments/) for JSON experiment definitions.*
