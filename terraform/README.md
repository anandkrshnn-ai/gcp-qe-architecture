# Terraform: Secure Agentic Runtime Secure Infrastructure

This directory contains the Infrastructure-as-Code (IaC) to deploy a production-grade, hardened GKE environment for the Secure Agentic Runtime secure runtime.

## Architecture Highlights

1.  **Workload Identity Federation**: Zero-trust authentication where K8s service accounts are mapped to GCP IAM roles.
2.  **Isolated Agent Pool**: A dedicated, tainted node pool for agent workloads to prevent noise and ensure security isolation.
3.  **Spot Instance Optimization**: Uses GKE Spot instances to reduce operational costs by up to 80%.
4.  **Private Networking**: GKE nodes have no public IP addresses; egress is managed via Cloud NAT.

## Prerequisites

- Terraform v1.5.0+
- GCP Project with billing enabled
- `gcloud` CLI authenticated

## Deployment

1.  Initialize Terraform:
    ```bash
    terraform init
    ```
2.  Create a `terraform.tfvars` file with your project details:
    ```hcl
    project_id = "your-project-id"
    region     = "us-central1"
    ```
3.  Plan and Apply:
    ```bash
    terraform plan
    ```
    ```bash
    terraform apply
    ```

## Outputs

- `cluster_endpoint`: The IP address of the GKE master.
- `agent_service_account`: The GCP service account email used by the agents.
