# Cloud Build Quality Pipeline

This pipeline enforces:
- Infrastructure as Code validation
- Performance testing
- AI-powered log analysis
- Quality gate enforcement

## How to Use
1. Create a Google Cloud Project.
2. Enable Cloud Build API.
3. Create a trigger in Cloud Build connected to this repository.
4. Map `cloudbuild.yaml` as the build configuration.
5. Set `_K6_CLOUD_TOKEN` as a substitution variable if using k6 cloud results.
