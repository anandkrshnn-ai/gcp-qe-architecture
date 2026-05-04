# Security & Compliance QA Guide

Practical security validation for GCP Quality Engineering.

## Key Areas
- **Workload Identity**: Ensure no default service accounts are used; bind K8s service accounts to IAM.
- **Secret Manager**: Validate that no secrets are hardcoded in environment variables or config files.
- **Container Analysis**: Enable vulnerability scanning for Artifact Registry.
- **IAM Least Privilege**: Use Policy Simulator to validate IAM roles.
- **Network Policy**: Enforce K8s network policies to restrict pod-to-pod communication.
- **Audit Logging**: Sink logs to BigQuery for long-term compliance analysis.

## Security Checklist
- [ ] Binary Authorization enabled (trusted images only)
- [ ] Pod Security Standards (restricted/baseline) enforced
- [ ] Gemini Agent used for security log analysis (anomaly detection)
- [ ] API keys restricted to specific services and IPs
