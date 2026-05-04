# The Quality Gates Model

Quality cannot be inspected into a product at the end of the lifecycle. It must be gated at every transition point. This model outlines the automated gates from code commit to production cutover in GCP.

## The 5-Stage Gate Model

### Gate 1: Developer PR Gate (The "Shift Left" Gate)
**Objective:** Catch basic code, security, and configuration errors before merging to the mainline.
- **Execution:** GitHub Actions / GitLab CI triggered on PR creation.
- **Checks:**
  - Static Code Analysis (SonarQube/Checkmarx)
  - Terraform Validation (`terraform validate`, `tflint`)
  - Unit Tests (>80% coverage)
  - Container Image Scanning (Trivy)

### Gate 2: Continuous Integration Gate (The "Build" Gate)
**Objective:** Ensure the integrated codebase compiles, passes baseline tests, and produces secure artifacts.
- **Execution:** Google Cloud Build triggered on merge to `main`.
- **Checks:**
  - Artifact pushed to Google Artifact Registry.
  - Policy as Code validation (Open Policy Agent/Rego checking for allowed base images or required labels).
  - Integration Tests (mocked external dependencies).

### Gate 3: Environment Deployment Gate (The "Staging" Gate)
**Objective:** Validate the application in a production-like environment.
- **Execution:** Cloud Deploy or ArgoCD deployment to Staging.
- **Checks:**
  - Automated deployment succeeds.
  - Smoke tests verify basic connectivity and health checks.

### Gate 4: Continuous Delivery Gate (The "NFR" Gate)
**Objective:** Validate performance, resilience, and security posture.
- **Execution:** Post-deployment automation against Staging.
- **Checks:**
  - **Performance:** k6 load test meets P95 latency SLO.
  - **Resilience:** Chaos test (e.g., node drain) does not drop availability below threshold.
  - **Security:** DAST (Dynamic Application Security Testing) scan passes.

### Gate 5: Production Release Gate (The "Cutover" Gate)
**Objective:** Safe release to users with automated rollback capabilities.
- **Execution:** Progressive delivery (Canary/Blue-Green) via Cloud Deploy.
- **Checks:**
  - Deployment strategy executes.
  - **Release Health Scoring:** Cloud Monitoring verifies error rates and latency on the canary footprint for 15 minutes.
  - **Automated Rollback:** If the error budget burn rate spikes, the release is automatically reverted.

## Implementing Gates as Code

Do not rely on manual sign-offs. Gates should be codified.

Example Policy (Rego) for Gate 2:
```rego
package cloudbuild.quality

deny[msg] {
    input.test_coverage < 80
    msg = sprintf("Test coverage is %v, must be at least 80", [input.test_coverage])
}
```

By enforcing these gates, defect escape rates to production are drastically reduced, and the deployment frequency (DORA metric) can safely increase.
