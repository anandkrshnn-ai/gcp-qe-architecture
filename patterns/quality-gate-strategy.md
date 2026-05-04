# Quality Gate Strategy

Opinionated quality gate strategy for automated promotion in CI/CD.

## Gate 1: Infrastructure Validation (Terraform)
- `terraform validate` + `tflint`
- `terraform plan` review (automated/manual)

## Gate 2: Application Quality (k6)
- Load test results within SLO thresholds.
- Smoke tests pass in staging environment.

## Gate 3: AI-Powered Insights (Gemini)
- Gemini RCA Agent analyzes logs for any hidden anomalies.
- RAG Evaluator validates AI-driven features (if any).

## Promotion Rule
All gates must be **GREEN** for automatic promotion to production.
