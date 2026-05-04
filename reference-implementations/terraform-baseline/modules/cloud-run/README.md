# Cloud Run Module

**Purpose**: Deploys a Cloud Run service with secure default configurations.

**Inputs**
| Name          | Description               | Type   | Default     |
|---------------|---------------------------|--------|-------------|
| environment   | Environment name          | string | -           |
| region        | GCP Region                | string | asia-south1 |

**Outputs**
- `service_url`
- `service_name`
