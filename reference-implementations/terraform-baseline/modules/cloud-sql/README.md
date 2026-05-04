# Cloud SQL Module

**Purpose**: Provisions a Regional High-Availability Cloud SQL (PostgreSQL) instance.

**Inputs**
| Name          | Description               | Type   | Default     |
|---------------|---------------------------|--------|-------------|
| environment   | Environment name          | string | -           |
| region        | GCP Region                | string | asia-south1 |

**Outputs**
- `db_instance_name`
- `db_connection_name`
- `db_private_ip`
