# VPC Module

**Purpose**: Creates a secure, private VPC with subnets for GKE + Cloud Run workloads.

**Inputs**
| Name          | Description               | Type   | Default     |
|---------------|---------------------------|--------|-------------|
| environment   | Environment name          | string | -           |
| region        | GCP Region                | string | asia-south1 |
| subnet_cidr   | Private subnet CIDR       | string | 10.0.0.0/20 |

**Outputs**
- `vpc_id`
- `subnet_id`
- `vpc_name`
