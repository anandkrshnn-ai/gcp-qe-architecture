# Limitations and Scope

This document provides a realistic assessment of the boundaries, constraints, and limitations of the **gcp-incident-analysis-demo** repository. As an educational demonstration project, it simulates safety controls locally and should not be run in production environments without significant engineering modifications.

---

## 1. Local Simulation & Sandbox Boundaries
1. **No Live Infrastructure Actuation**: Remediation actions (such as `SCALE_UP` or `ROLLBACK`) do not update real GCP resources (e.g., GKE deployment resource counts or Cloud Run configurations). The remediator prints dry-run logs.
2. **In-Memory Registry**: The agent registration registry and trusted keys list exist purely in-memory. They do not persist across python executions.
3. **Simulated Telemetry Logs**: Input logs are local mock payloads instead of live feeds pulled dynamically from GCP Cloud Logging sinks.
4. **Transient Consensus State**: Verification nonces and timestamps are stored in a local transient cache. Stopping the process resets all replay-protection history.
5. **No Actual Byzantine Fault Tolerance (BFT)**: The voting validator is a simple threshold signature quorum check. It does not implement true distributed consensus protocols (e.g., PBFT, Raft-BFT, or Paxos) to handle compromised nodes on separate servers.
6. **Synchronous Execution**: All voting, signing, and evaluations run sequentially on a single thread. Network delays, node failures, and partitions are simulated locally.

---

## 2. Cryptographic & Security Constraints
7. **Mock Trust Anchors**: The platform security verification does not interface with a real hardware Trusted Platform Module (TPM) or Confidential VM Guest Attestation reports.
8. **In-Memory Key Fallbacks**: When Google Cloud KMS credentials are not detected, the signer falls back to local in-memory RSA key generation, which is unsuitable for secure production environments.
9. **No Identity Provider Integration**: Key verification is bound to simple RSA public key files instead of utilizing Google Cloud IAM, Identity-Aware Proxy (IAP), or external OpenID Connect (OIDC) identity pools.
10. **Lack of Automated Key Rotation**: The codebase has no provision for automated key rotation, key revocation checking (CRLs/OCSP), or KMS key version updates.
11. **Local Model Armor Limitations**: Secret and API key sanitization relies on local, regex-based matching rather than invoking Google Cloud's Sensitive Data Protection (DLP) API.
12. **Local OS Time Reliance**: Replay-protection timestamp validation relies on the host machine's system time. If the local system clock drifts or is spoofed, clock-skew verification is compromised.

---

## 3. Operations & Observability Limits
13. **Local Logging Only**: Logs and metrics are formatted and output to standard output/console. The demo does not export telemetry directly to Google Cloud Logging or Monitoring APIs.
14. **No Distributed Tracing**: There is no built-in OpenTelemetry or Cloud Trace support to trace parent-child execution spans across multiple autonomous agents.
15. **Static Resource Quotas**: Safety gate replica limits and cost thresholds are loaded from static, local configurations rather than fetching live GCP quotas or service billing limits.
16. **No Real Cost Billing Integration**: Estimated remediation pricing uses hardcoded cost approximations instead of query integrations with the Google Cloud Billing Catalog API.
17. **Simplistic Chaos Injections**: The simulation chaos injector modifies local arrays rather than triggering real system chaos events via tools like GKE Chaos Mesh or container deletion.
18. **No Authenticity Scoring**: Authenticity / LLM style classification features have been completely removed from the demo codebase to reduce unnecessary complexity and bloat.
19. **Fixed Schema Formats**: Remediation payloads must conform to simple, pre-defined Pydantic models. They cannot handle dynamic, unstructured cluster configurations.
20. **No IAM Authorization Checks**: The safety gate checks the operation type but does not verify whether the invoking agent's GSA possesses the required IAM permissions (e.g., `container.deployments.update`) on the target GCP resources.
