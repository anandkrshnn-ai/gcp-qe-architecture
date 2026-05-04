# Cloud SQL Resilience Testing

The database is often the single point of failure. Resilience engineering for Cloud SQL focuses on failover, backups, and connection stability.

## 1. High Availability (HA) Validation
-   **Manual Failover Test:** Trigger a failover via `gcloud sql instances failover`.
-   **Client-side Resilience:** Ensure applications use connection pooling (e.g., HikariCP, Cloud SQL Proxy) and handle reconnections gracefully.

## 2. Backup & Recovery Gates
-   **Point-in-Time Recovery (PITR):** Verify that binary logging is enabled.
-   **Restoration Test:** Monthly automated restoration of a backup to a temporary instance to verify data integrity.

## 3. Performance & Capacity
-   **Storage Auto-resize:** Ensure auto-resize is enabled but monitored for cost.
-   **Read Replicas:** Validate that read-heavy workloads are correctly offloaded to replicas.

## 4. Security Gates
-   **IAM Authentication:** Use IAM-based authentication instead of static passwords.
-   **Private IP:** Ensure instances are only accessible via Private IP within the VPC.

---

*See [Chaos Engineering Playbook](../docs/06-chaos-engineering-playbook.md) for database failure experiments.*
