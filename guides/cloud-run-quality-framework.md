# Cloud Run Quality Framework

Cloud Run's serverless nature requires specific focus on cold starts, concurrency, and environment parity.

## 1. Fast Feedback Loop
-   **Local Run:** Use `gcloud code dev` for local testing.
-   **Container Optimization:** Keep image sizes small to reduce cold start latency. Use multi-stage builds.

## 2. Configuration Quality
-   **Concurrency:** Tune the `concurrency` setting based on the service's memory/CPU profile.
-   **Max Instances:** Set a ceiling to prevent runaway costs during load tests or attacks.
-   **Environment Variables:** Use Secret Manager for sensitive data, never hardcode.

## 3. Automated Validation
-   **Tag-based Testing:** Deploy to a new revision with a specific tag (e.g., `--tag green`). Run tests against this URL before routing traffic.
-   **Gradual Rollouts:** Use Traffic Splitting (Canary) to route 5%, 10%, 50% of traffic while monitoring SLOs.

## 4. Performance Gates
-   **Cold Start Latency:** Measure and set thresholds for cold start times.
-   **Request Timeout:** Ensure timeouts are aligned with the service's SLOs.

---

*See [Cloud Run Reference Implementation](../reference-implementations/cloud-run/) (Coming soon).*
