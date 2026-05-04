resource "google_monitoring_alert_policy" "slo_burn_rate" {
  display_name = "SLO Burn Rate Alert"
  combiner     = "OR"

  conditions {
    display_name = "High Burn Rate"
    condition_threshold {
      filter          = "metric.type=\"monitoring.googleapis.com/slo/burn_rate\""
      duration        = "300s"
      comparison      = "COMPARISON_GT"
      threshold_value = 1.5
    }
  }

  notification_channels = [var.notification_channel]
}
