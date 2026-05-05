# Cloud SQL Resilience Guide

**Practical reliability patterns for Cloud SQL on GCP**

---

## 1. High Availability Configuration

Cloud SQL HA uses a standby instance in a different zone. Failover is automatic when the primary becomes unavailable.

**Terraform pattern**:
```hcl
resource "google_sql_database_instance" "primary" {
  name             = "${var.environment}-postgres"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier              = "db-custom-2-7680"
    availability_type = "REGIONAL"   # Enables HA with standby replica

    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = true
      start_time                     = "02:00"
      retained_backups               = 30
    }

    maintenance_window {
      day          = 7    # Sunday
      hour         = 3    # 03:00 UTC
      update_track = "stable"
    }
  }
}
```

**Recommended SLO**: Failover RTO < 60 seconds (Cloud SQL automatic failover is typically 30-60s).

---

## 2. Point-in-Time Recovery (PITR)

Enable PITR for all production databases. This provides recovery to any point within the retention window (up to 7 days) in the event of accidental deletion or data corruption.

- **Recovery test**: Perform a quarterly PITR test to a separate instance. Verify data integrity and measure actual RTO.
- **RTO target**: < 30 minutes for PITR restore.
- **RPO target**: < 5 minutes (continuous write-ahead log archival).

---

## 3. Replication Monitoring

Monitor replication lag for read replicas. High replication lag means:
- Read replicas are serving stale data.
- Failover will result in data loss up to the lag duration.

**Alert threshold**: `cloudsql.googleapis.com/database/replication/replica_lag > 30 seconds` → P2 ticket.

---

## 4. Connection Management

Cloud SQL connections are a finite resource. Connection exhaustion is one of the most common Cloud SQL failure modes.

| Pattern | Use Case |
|---------|---------|
| **Cloud SQL Auth Proxy** | All non-serverless workloads. Handles IAM auth and TLS automatically. |
| **Cloud SQL Connector** | Serverless workloads (Cloud Run, Cloud Functions). |
| **Connection pooling (PgBouncer)** | High-concurrency applications where each instance opens many connections. |

**Connection limit alert**: Alert when connection count exceeds 80% of `max_connections`.

---

## 5. Chaos Testing for Cloud SQL

Include these scenarios in the quarterly chaos testing calendar:

| Experiment | Method | Expected Outcome |
|------------|--------|-----------------|
| Primary instance failover | Manually trigger via Console or `gcloud sql instances failover` | Automatic failover in < 60s; application reconnects via Auth Proxy |
| Network partition (replica) | Remove replica's network access temporarily | Application falls back to primary; read replica lag clears on reconnect |
| Connection pool exhaustion | Simulate with load test exceeding pool limit | Circuit breaker activates; application returns 503 gracefully |

---

*Related: [GKE Testing Guide](gke-testing-guide.md) | [Production Readiness](03-production-readiness.md) | [SLO/SLI Engineering](02-slo-sli-engineering.md)*
