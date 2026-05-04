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
cd environments/dev
terraform init
terraform apply
```

**Recommended**: Start with `dev` environment.

## Policy as Code (OPA)

This foundation includes [Rego policies](policies/) to enforce security best practices (e.g., Workload Identity on GKE) as code. Use these in your CI pipeline to prevent insecure configurations from being deployed.
