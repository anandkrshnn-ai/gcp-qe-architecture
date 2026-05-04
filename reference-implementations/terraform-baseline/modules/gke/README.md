# GKE Module

**Purpose**: Provisions a secure, private GKE Autopilot or Standard cluster with Workload Identity.

**Inputs**
| Name          | Description               | Type   | Default     |
|---------------|---------------------------|--------|-------------|
| project_id    | GCP Project ID            | string | -           |
| environment   | Environment name          | string | -           |
| region        | GCP Region                | string | asia-south1 |
| vpc_id        | VPC Network ID            | string | -           |
| subnet_id     | Subnet ID                 | string | -           |

**Outputs**
- `cluster_name`
- `cluster_endpoint`
- `ca_certificate`
