# Example: GKE Availability SLO
resource "google_monitoring_slo" "gke_availability" {
  service      = "gke"
  display_name = "GKE Availability SLO"
  goal         = 0.995   # 99.5%
  rolling_period_days = 28

  request_based_sli {
    good_total_ratio {
      total_service_filter = "metric.type=\"kubernetes.io/container/uptime\" resource.type=\"k8s_container\""
      good_service_filter  = "metric.type=\"kubernetes.io/container/uptime\" resource.type=\"k8s_container\""
    }
  }
}

# Example: Cloud Run Latency SLO
resource "google_monitoring_slo" "cloud_run_latency" {
  service      = "cloud-run"
  display_name = "Cloud Run P95 Latency SLO"
  goal         = 0.95
  rolling_period_days = 28

  request_based_sli {
    distribution_cut {
      distribution_filter = "metric.type=\"run.googleapis.com/request_latencies\" resource.type=\"cloud_run_revision\""
      range {
        max = 800
      }
    }
  }
}

# Cloud SQL Failover Success Rate
resource "google_monitoring_slo" "cloud_sql_failover" {
  service      = "cloud-sql"
  display_name = "Cloud SQL Failover Success"
  goal         = 0.98
  rolling_period_days = 28

  request_based_sli {
    good_total_ratio {
      total_service_filter = "metric.type=\"cloudsql.googleapis.com/database/up\" resource.type=\"cloudsql_database\""
      good_service_filter  = "metric.type=\"cloudsql.googleapis.com/database/up\" resource.type=\"cloudsql_database\""
    }
  }
}

variable "notification_channel" {
  description = "Notification channel for alerts"
  type        = string
  default     = "projects/YOUR_PROJECT_ID/notificationChannels/12345"
}
