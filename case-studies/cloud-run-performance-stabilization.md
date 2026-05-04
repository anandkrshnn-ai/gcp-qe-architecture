# Case Study: Cloud Run Performance Stabilization

**Date**: May 2026  
**Context**: High-traffic Cloud Run service suffering from inconsistent P95 latency and frequent cold start issues affecting user experience.

**Problem Statement**
- P95 latency spikes during rapid traffic surges.
- Unreliable scaling behavior caused by incorrect concurrency settings.
- Performance regressions slipping into production due to lack of automated performance gates.

**Actions Taken**
- **Configuration Hardening**: Implemented proper resource limits, min-instances, and startup probes via the Cloud Run module.
- **Performance Gates**: Added k6 performance tests as mandatory gates in the Cloud Build pipeline.
- **Observability**: Enabled custom metrics for autoscaling and connected them to Cloud Monitoring dashboards.
- **AI RCA**: Integrated the Gemini RCA Agent specifically for latency-related incident investigation.
- **Deployment Strategy**: Applied traffic splitting for canary deployments to validate new revisions under partial load.

**Results**
- P95 latency reduced by 25% during peak hours.
- Cold start rate dropped significantly by implementing warm-up probes and min-instances.
- Performance regressions are now caught early in CI/CD, preventing them from reaching production.
- More predictable and efficient scaling behavior, reducing compute costs by 15%.

**Artifacts Used**
- `guides/cloud-run-quality-guide.md`
- `reference-implementations/k6-performance/`
- `reference-implementations/cloud-build-pipelines/`
- `frameworks/gemini-agent-qe/`

**Key Learning**
Performance testing must be treated as a mandatory quality gate in the CI/CD pipeline, not an afterthought. Consistent performance is a prerequisite for reliable scaling.
