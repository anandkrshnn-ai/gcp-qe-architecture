# Service Level Objectives (SLOs) defined as Code

resource "google_monitoring_slo" "availability_slo" {
  service      = var.service_id
  slo_id       = "availability-99-9"
  display_name = "99.9% Availability SLO"

  goal                = 0.999
  rolling_period_days = 28

  basic_sli {
    availability {
      enabled = true
    }
  }
}

resource "google_monitoring_slo" "latency_slo" {
  service      = var.service_id
  slo_id       = "latency-p95-under-500ms"
  display_name = "P95 Latency under 500ms"

  goal                = 0.95
  rolling_period_days = 28

  basic_sli {
    latency {
      threshold = "0.5s"
    }
  }
}

# SLO Burn Rate Alert
resource "google_monitoring_alert_policy" "slo_burn_rate" {
  display_name = "High SLO Burn Rate (>10x)"
  combiner     = "OR"
  conditions {
    display_name = "SLO Burn Rate Condition"
    condition_threshold {
      filter     = "select_slo_burn_rate(\"${google_monitoring_slo.availability_slo.name}\", \"60m\")"
      duration   = "0s"
      comparison = "COMPARISON_GT"
      threshold_value = 10
    }
  }
  notification_channels = [var.notification_channel_id]
}
