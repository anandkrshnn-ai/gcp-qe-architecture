# Guide 08: The Path to Production

This document outlines how to move from the **Sovereign-GCP Simulation** to a **Live Production Deployment**.

## Step 1: GCP Project Setup
1.  **Create a Project**: `gcloud projects create sovereign-qe-prod`
2.  **Enable APIs**:
    ```bash
    gcloud services enable \
      logging.googleapis.com \
      monitoring.googleapis.com \
      aiplatform.googleapis.com
    ```

## Step 2: Infrastructure Deployment
1.  Navigate to `terraform-baseline/`.
2.  Update `terraform.tfvars` with your project details.
3.  Execute:
    ```bash
    terraform init
    terraform apply
    ```

## Step 3: Agent Configuration
The agents are designed to use **Dependency Injection**. To switch from Simulation to Production:

1.  Update `config.yaml`:
    ```yaml
    execution_mode: production
    project_id: "your-project-id"
    credentials_path: "/path/to/sa-key.json"
    ```
2.  The `SovereignGCPClient` will automatically switch from mock behavior to real SDK calls.

## Step 4: Verification
Run the real-world verification suite:
```bash
pytest tests/integration/test_gcp_real.py
```
