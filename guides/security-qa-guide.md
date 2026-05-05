# Security & Compliance QA Guide

**Security testing integration for GCP cloud-native workloads**

---

## 1. Security Testing in the QE Pipeline

Security is a quality attribute, not a separate discipline. It belongs in the same quality gate pipeline as performance and reliability.

| Gate | Tool | Trigger | Blocks |
|------|------|---------|--------|
| Pre-commit | `gitleaks` / `truffleHog` | Every commit | Secrets in code |
| PR | `ruff` / `bandit` (Python SAST) | Every PR | High severity findings |
| PR | `trivy` (container scan) | Every image build | Critical CVEs |
| PR | `dependabot` / `snyk` | Daily + PR | Unpatched High/Critical deps |
| Staging deploy | OWASP ZAP (DAST) | Every staging deploy | Critical findings |
| Quarterly | Penetration test | Scheduled | Sign-off required |

---

## 2. GCP Identity and Access

**Workload Identity (GKE)**

Never use default service accounts. Bind Kubernetes service accounts to IAM service accounts with the minimum required permissions.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: payments-api
  annotations:
    iam.gke.io/gcp-service-account: payments-api@PROJECT_ID.iam.gserviceaccount.com
```

**Validation**: Use the IAM Policy Simulator to verify that the service account cannot access resources beyond its scope. Run this as part of the production readiness review.

---

## 3. Secret Management

All secrets must be stored in **Secret Manager**. No exceptions.

Security QA checklist for secrets:
- [ ] Zero hardcoded secrets in application code (validated by `truffleHog` in CI).
- [ ] Zero secrets in environment variables passed directly (use Secret Manager volume mounts or `secretKeyRef`).
- [ ] Secret rotation policy defined (database passwords: 90 days, API keys: 180 days).
- [ ] Secret access is logged and alerts fire on unusual access patterns.

---

## 4. Container Security

**Binary Authorization**

Enable Binary Authorization to ensure only trusted images run in GKE:

```hcl
resource "google_binary_authorization_policy" "policy" {
  default_admission_rule {
    evaluation_mode         = "REQUIRE_ATTESTATION"
    enforcement_mode        = "ENFORCED_BLOCK_AND_AUDIT_LOG"
    require_attestations_by = [google_binary_authorization_attestor.qe_attestor.name]
  }
}
```

**Pod Security Standards**

Apply the `restricted` Pod Security Standard to all production namespaces:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
```

---

## 5. Network Security

**GKE Network Policies**

Restrict pod-to-pod communication to explicitly allowed paths only:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: payments-api-ingress
spec:
  podSelector:
    matchLabels:
      app: payments-api
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: api-gateway
```

**Principle**: Default deny all ingress/egress; allow only what is explicitly required.

---

## 6. Audit Logging and Compliance

Sink Cloud Audit Logs to BigQuery for long-term retention and compliance analysis:

- **Data Access logs**: Who accessed what data and when.
- **Admin Activity logs**: Infrastructure changes (instance creation, IAM changes).
- **System Event logs**: Automated GCP system actions.

**Retention**: Minimum 1 year for compliance workloads; 7 years for financial/healthcare.

**Alert**: Any IAM policy change on a production project → immediate P2 ticket.

---

## 7. AI-Assisted Security QA

The [Gemini RCA Agent](../frameworks/gemini-agent-qe/) can be extended for security log analysis:

- Feed Cloud Audit Logs to the agent to detect anomalous access patterns.
- Combine with Cloud Armor logs to identify DDoS or credential stuffing attack signatures.
- For sovereign/regulated environments, use the [Sovereign AI RCA](../frameworks/sovereign-ai-qe/) to ensure security logs never leave the VPC boundary.

---

*Related: [AI-Powered QE](04-ai-powered-quality-engineering.md) | [Production Readiness](03-production-readiness.md) | [GKE Testing Guide](gke-testing-guide.md)*
