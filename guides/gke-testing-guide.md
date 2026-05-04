# GKE Testing Guide

**Last Updated:** May 2026

## Testing Layers

### 1. Infrastructure Layer
- Terraform validation + `terraform test`
- Policy as Code (OPA/Gatekeeper)
- Cluster config drift detection

### 2. Platform Layer
- Node pool scaling behavior
- Workload Identity & Network Policy validation
- Managed Prometheus + Cloud Monitoring

### 3. Application Layer
- Contract & Integration testing
- Performance testing with k6
- Canary deployments

### 4. Resilience Layer
- Chaos experiments (Pod Kill, Network Latency)
- SLO monitoring & alerting

**Key Recommendation**: Run chaos experiments weekly in lower environments.
