# GKE Testing & Quality Guide

Google Kubernetes Engine (GKE) requires a multi-layered testing approach to ensure reliability and scalability.

## 1. Local Development Testing
-   **Skaffold:** Use Skaffold for continuous local development and testing.
-   **kind/minikube:** Validate manifest changes locally before pushing to CI.

## 2. CI/CD Quality Gates
-   **Kube-linter / Checkov:** Scan manifests for security misconfigurations (e.g., privileged containers, missing resource limits).
-   **Helm Unit Testing:** Test logic inside Helm templates.
-   **Policy Enforcement (OPA/Gatekeeper):** Ensure all deployments meet organizational standards (e.g., must have `app` label).

## 3. Integration & System Testing
-   **Ephemeral Environments:** Cloud Build should spin up a temporary GKE namespace for every PR to run integration tests.
-   **Internal LB Validation:** Ensure service-to-service communication works via internal load balancers.

## 4. Resilience Testing
-   **Node Failure:** Simulate node preemptions to ensure pods are rescheduled without downtime.
-   **HPA Validation:** Use load tests (k6) to verify that Horizontal Pod Autoscaler scales pods based on CPU/Memory/Custom Metrics.

---

*See [Quality Gates Model](../docs/03-quality-gates-model.md) for automated pipeline integration.*
