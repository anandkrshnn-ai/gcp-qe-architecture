# End-to-End Observable App Example

This is a complete example combining:
- Modular Terraform Baseline
- GKE + Cloud Run deployment
- SLO Monitoring
- Gemini RCA Agent
- k6 Performance Test

**Goal**: Deploy a production-like observable service in one flow.

## Deployment Steps

1. Update `environments/sandbox/terraform.tfvars` with your project_id
2. `terraform apply` (from `environments/sandbox/`)
3. Deploy sample application to Cloud Run
4. Run k6 performance test
5. Trigger Gemini RCA Agent on sample logs
