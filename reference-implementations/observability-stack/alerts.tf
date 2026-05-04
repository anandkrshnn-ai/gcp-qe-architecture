# High Error Rate Alert
resource "google_monitoring_alert_policy" "error_rate" {
  display_name = "High Error Rate Alert"
  combiner     = "OR"
  conditions {
    display_name = "Error Rate > 1%"
    condition_threshold {
      filter          = "metric.type=\"kubernetes.io/container/error_rate\""
      duration        = "300s"
      comparison      = "COMPARISON_GT"
      threshold_value = 0.01
    }
  }
}
