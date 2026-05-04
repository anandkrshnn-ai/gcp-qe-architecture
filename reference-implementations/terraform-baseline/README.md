# Terraform Baseline - Secure & Observable GCP Foundation

Production-grade modular Terraform baseline for GKE + Cloud Run + Cloud SQL workloads.

**Features**:
- VPC with secure subnets
- GKE cluster (best practices 2026)
- Cloud Run service
- Cloud SQL (Regional HA)
- Built-in observability (Logging, Monitoring, Trace)

## Usage

```bash
cd environments/sandbox
terraform init
terraform apply
```

**Recommended**: Start with `sandbox` environment.
